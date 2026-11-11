#!/usr/bin/env python3
"""Secret scanner for pre-commit hook.

Scans staged files for common secret patterns (API keys, tokens, passwords,
private keys). Blocks commit if any match is found.

Usage: python3 tools/scan_secrets.py
Or as pre-commit hook: exec python3 tools/scan_secrets.py
"""
from __future__ import annotations

import re
import subprocess
import sys

# Patterns that indicate potential secrets
SECRET_PATTERNS = [
    (r"(?i)(api[_-]?key|apikey)\s*[:=]\s*['\"]?[a-z0-9]{20,}", "API key"),
    (r"(?i)(secret[_-]?key|secretkey)\s*[:=]\s*['\"]?[a-z0-9]{20,}", "Secret key"),
    (r"(?i)(private[_-]?key|privatekey)\s*[:=]\s*['\"]?[a-z0-9]{20,}", "Private key"),
    (r"(?i)(token|access[_-]?token)\s*[:=]\s*['\"]?[a-z0-9]{20,}", "Access token"),
    (r"(?i)(password|passwd|pwd)\s*[:=]\s*['\"]?[a-z0-9]{8,}", "Password"),
    (r"(?i)(ghp_[a-z0-9]{36,})", "GitHub personal access token"),
    (r"(?i)(glpat-[a-z0-9]{20,})", "GitLab personal access token"),
    (r"(?i)(xoxb-[a-z0-9-]{20,})", "Slack bot token"),
    (r"(?i)(sk-[a-z0-9]{20,})", "OpenAI API key"),
    (r"-----BEGIN [A-Z ]+PRIVATE KEY-----", "Private key block"),
]

# Files to exclude from scanning
EXCLUDE_PATTERNS = [
    r"\.env\.example",
    r"THIRD_PARTY_NOTICES",
    r"LICENSE",
    r"tests/",
    r"\.git/",
]


def get_staged_files() -> list[str]:
    """Get list of staged files."""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
            capture_output=True, text=True, check=True
        )
        return [f for f in result.stdout.splitlines() if f]
    except subprocess.CalledProcessError:
        return []


def should_exclude(filepath: str) -> bool:
    for pat in EXCLUDE_PATTERNS:
        if re.search(pat, filepath):
            return True
    return False


def scan_file(filepath: str) -> list[tuple[int, str, str]]:
    """Scan a single file for secrets. Returns list of (line_num, pattern_name, line_content)."""
    findings = []
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            for i, line in enumerate(f, 1):
                for pattern, name in SECRET_PATTERNS:
                    if re.search(pattern, line):
                        findings.append((i, name, line.strip()[:100]))
    except Exception:
        pass
    return findings


def main():
    staged = get_staged_files()
    if not staged:
        print("No staged files to scan.")
        return

    total_findings = 0
    for filepath in staged:
        if should_exclude(filepath):
            continue
        findings = scan_file(filepath)
        for line_num, pattern_name, content in findings:
            print(f"SECRET DETECTED: {filepath}:{line_num} [{pattern_name}]")
            print(f"  {content}")
            total_findings += 1

    if total_findings > 0:
        print(f"\nFAIL: {total_findings} potential secret(s) found in staged files.")
        print("Remove secrets before committing. Use .agent/.env (gitignored) for keys.")
        sys.exit(1)

    print(f"PASS: no secrets found in {len(staged)} staged file(s)")


if __name__ == "__main__":
    main()
