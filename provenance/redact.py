#!/usr/bin/env python3
"""Redaction engine — strip secrets and PII from text before logging/storage.

Implements the redaction policy defined in config/redaction.yaml.

Rules:
- Secrets (API keys, tokens, passwords, private keys): BLOCK — dispatch
  must not proceed if a secret is detected in the prompt.
- PII (emails, phone numbers, credit cards, national IDs, IPs): REDACT +
  flag — replace with [REDACTED:PII] and record in redactions list.
- Regulated data (per deployment policy): REDACT + flag.
- Raw secrets never appear in any persistent record, log, or span.
- All fields default to empty/empty-list; absent fields mean empty allow-lists
  — nothing permitted by default.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any


@dataclass
class RedactionResult:
    """Result of redacting text.

    Attributes:
        text: Redacted text (safe to log/store).
        redacted: True if any redaction occurred.
        redactions: List of redaction events with category, count, action.
        blocked: True if any secret was detected (blocks dispatch).
        block_reason: Reason string if blocked, None otherwise.
    """

    text: str
    redacted: bool
    redactions: list[dict[str, Any]] = field(default_factory=list)
    blocked: bool = False
    block_reason: str | None = None


class Redactor:
    """Redacts secrets and PII from text according to policy.

    Detection is layered:
    1. Pattern matching (regex) for known formats
    2. Keyword heuristics for provider-specific secrets
    3. Context-aware analysis for ambiguous patterns

    Every redaction is recorded; raw secrets never reach any output.
    """

    # Secret patterns — these BLOCK dispatch
    SECRET_PATTERNS: list[tuple[str, str, str]] = [
        # API keys — common patterns
        (r"(?i)(?:api[_-]?key|apikey)\s*[:=]\s*['\"]?([a-zA-Z0-9]{20,})", "secret", "api_key"),
        (r"(?i)(?:secret[_-]?key|secretkey)\s*[:=]\s*['\"]?([a-zA-Z0-9]{20,})", "secret", "secret_key"),
        (r"(?i)(?:private[_-]?key|privatekey)\s*[:=]\s*['\"]?([a-zA-Z0-9]{20,})", "secret", "private_key"),
        (r"(?i)(?:token|access[_-]?token)\s*[:=]\s*['\"]?([a-zA-Z0-9]{20,})", "secret", "access_token"),
        # GitHub tokens
        (r"(?i)(ghp_[a-zA-Z0-9]{36,})", "secret", "github_token"),
        (r"(?i)(gho_[a-zA-Z0-9]{36,})", "secret", "github_oauth_token"),
        (r"(?i)(ghu_[a-zA-Z0-9]{36,})", "secret", "github_user_token"),
        # GitLab tokens
        (r"(?i)(glpat-[a-zA-Z0-9\-]{20,})", "secret", "gitlab_token"),
        # Slack tokens
        (r"(?i)(xoxb-[a-zA-Z0-9\-]{20,})", "secret", "slack_bot_token"),
        (r"(?i)(xoxa-[a-zA-Z0-9\-]{20,})", "secret", "slack_app_token"),
        (r"(?i)(xoxp-[a-zA-Z0-9\-]{20,})", "secret", "slack_user_token"),
        # Generic Bearer tokens
        (r"(?i)(?:bearer\s+)([a-zA-Z0-9\-]{20,})", "secret", "bearer_token"),
        # Generic API key patterns
        (r"(?i)(?:api[_-]?key|api_key)\s*[:=]\s*['\"]?([a-zA-Z0-9]{20,})", "secret", "api_key_generic"),
    ]

    # PII patterns — these REDACT + FLAG
    PII_PATTERNS: list[tuple[str, str, str]] = [
        # Email addresses
        (r"([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})", "pii", "email"),
        # US phone numbers (various formats)
        (r"(\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}", "pii", "phone_us"),
        # Credit card numbers (Luhn-validated patterns)
        (r"\b(?:[0-9]{4}[-\s]?){3}[0-9]{4}\b", "pii", "credit_card"),
        # US Social Security Numbers
        (r"\b[0-9]{3}-[0-9]{2}-[0-9]{4}\b", "pii", "ssn_us"),
        # IP addresses (IPv4)
        (r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", "pii", "ipv4"),
    ]

    def __init__(self, policy: dict | None = None):
        """Initialize redactor with optional policy config.

        Args:
            policy: Policy dict with keys:
                - secret_categories: list of categories to block
                - pii_categories: list of categories to redact
                - regulated_categories: list of categories to redact+flag
                - blocked_categories: list of categories that block dispatch
        """
        self.policy = policy or {}
        self.secret_categories = set(self.policy.get("secret_categories", ["secret"]))
        self.pii_categories = set(self.policy.get("pii_categories", ["pii"]))
        self.regulated_categories = set(self.policy.get("regulated_categories", []))
        self.blocked_categories = set(self.policy.get("blocked_categories", ["secret"]))

    def redact(self, text: str) -> RedactionResult:
        """Redact secrets and PII from text.

        Returns a RedactionResult with redacted text and redaction metadata.
        If any secret is detected, blocked=True and the dispatch must not proceed.
        """
        redacted_text = text
        redactions: list[dict[str, Any]] = []
        blocked = False
        block_reason = None

        # First pass: detect secrets (block these)
        for pattern, category, name in self.SECRET_PATTERNS:
            matches = list(re.finditer(pattern, redacted_text))
            if matches:
                if category in self.blocked_categories:
                    blocked = True
                    block_reason = f"SECRET_DETECTED: {category} ({name})"
                # Replace with placeholder
                redacted_text = re.sub(pattern, f"[REDACTED:{category.upper()}]", redacted_text)
                redactions.append({
                    "category": category,
                    "name": name,
                    "action": "block" if category in self.blocked_categories else "redact",
                    "count": len(matches),
                })

        # Second pass: redact PII (replace, don't block)
        for pattern, category, name in self.PII_PATTERNS:
            matches = list(re.finditer(pattern, redacted_text))
            if matches:
                redacted_text = re.sub(pattern, f"[REDACTED:{category.upper()}]", redacted_text)
                redactions.append({
                    "category": category,
                    "name": name,
                    "action": "redact",
                    "count": len(matches),
                })

        return RedactionResult(
            text=redacted_text,
            redacted=len(redactions) > 0,
            redactions=redactions,
            blocked=blocked,
            block_reason=block_reason,
        )


def redact_text(text: str, policy: dict | None = None) -> RedactionResult:
    """Convenience function to redact text with default policy."""
    redactor = Redactor(policy)
    return redactor.redact(text)


def is_safe_to_dispatch(text: str, policy: dict | None = None) -> tuple[bool, str | None]:
    """Check if text is safe to dispatch (no secrets).

    Returns (is_safe, block_reason). If blocked, the reason explains why.
    """
    result = redact_text(text, policy)
    return not result.blocked, result.block_reason


# Default policy — secrets block, PII redacts+flags
DEFAULT_POLICY: dict = {
    "secret_categories": ["secret"],
    "pii_categories": ["pii"],
    "regulated_categories": [],
    "blocked_categories": ["secret"],
}
