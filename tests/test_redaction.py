#!/usr/bin/env python3
"""Tests for redaction module."""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "provenance"))

from redact import Redactor, redact_text, is_safe_to_dispatch  # noqa: E402

# A syntactically valid but entirely fake GitHub token. Redaction tests need
# input that actually matches SECRET_PATTERNS: the patterns require a known
# key name (api_key, token, ...) followed by ':' or '=' and a 20+ char value,
# or a vendor prefix such as 'ghp_'. The earlier version passed the literal
# string "[redacted]", which matches nothing, so the test asserted a block the
# redactor correctly never raised.
FAKE_TOKEN = "ghp_" + "0123456789abcdef0123456789abcdef0123"
FAKE_KEY_VALUE = "api_key=" + "A" * 24


class TestRedactor(unittest.TestCase):
    """Test redaction module."""

    def test_secret_blocked(self):
        """A matched secret blocks dispatch."""
        redactor = Redactor()
        result = redactor.redact(f"my API key is {FAKE_TOKEN}")
        assert result.blocked is True
        assert result.block_reason is not None
        assert "secret" in result.block_reason.lower()

    def test_secret_not_in_output(self):
        """Raw secret never appears in output."""
        redactor = Redactor()
        result = redactor.redact(f"my API key is {FAKE_TOKEN}")
        assert FAKE_TOKEN not in result.text
        assert "[REDACTED:SECRET]" in result.text

    def test_key_value_secret_blocked(self):
        """A key=value secret is blocked and replaced."""
        redactor = Redactor()
        result = redactor.redact(f"config: {FAKE_KEY_VALUE}")
        assert result.blocked is True
        assert FAKE_KEY_VALUE not in result.text
        assert "[REDACTED:SECRET]" in result.text

    def test_pii_redacted(self):
        """PII is redacted but dispatch proceeds."""
        redactor = Redactor()
        result = redactor.redact("contact me at john.doe@example.com")
        assert result.blocked is False
        assert result.redacted is True
        assert "john.doe@example.com" not in result.text
        assert "[REDACTED:PII]" in result.text

    def test_no_secrets_no_block(self):
        """No secrets means no block."""
        redactor = Redactor()
        result = redactor.redact("hello world, this is safe text")
        assert result.blocked is False
        assert result.redacted is False
        assert result.text == "hello world, this is safe text"


class TestConvenienceFunctions(unittest.TestCase):
    """Test convenience functions.

    These previously subclassed nothing, so unittest discovery skipped them
    entirely and they never ran.
    """

    def test_is_safe_to_dispatch_safe(self):
        """Safe text passes."""
        is_safe, reason = is_safe_to_dispatch("hello world")
        assert is_safe is True
        assert reason is None

    def test_is_safe_to_dispatch_blocked(self):
        """Secret text is blocked."""
        is_safe, reason = is_safe_to_dispatch(f"token: {FAKE_TOKEN}")
        assert is_safe is False
        assert reason is not None
        assert "secret" in reason.lower()

    def test_redact_text_returns_result(self):
        """The convenience wrapper returns a RedactionResult."""
        result = redact_text(f"token: {FAKE_TOKEN}")
        assert result.blocked is True
        assert FAKE_TOKEN not in result.text


if __name__ == "__main__":
    unittest.main()
