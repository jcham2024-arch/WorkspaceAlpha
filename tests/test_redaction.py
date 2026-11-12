#!/usr/bin/env python3
"""Tests for redaction module."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "provenance"))

from redact import Redactor, redact_text, is_safe_to_dispatch  # noqa: E402


class TestRedactor(unittest.TestCase):
    """Test redaction module."""

    def test_secret_blocked(self):
        """Secret in context blocks dispatch."""
        redactor = Redactor()
        result = redactor.redact("my API key is sk-1234567890abcdef1234567890abcdef")
        assert result.blocked is True
        assert result.block_reason is not None
        assert "secret" in result.block_reason.lower()

    def test_secret_not_in_output(self):
        """Raw secret never appears in output."""
        redactor = Redactor()
        result = redactor.redact("my API key is sk-1234567890abcdef1234567890abcdef")
        assert "sk-1234567890abcdef1234567890abcdef" not in result.text
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


class TestConvenienceFunctions:
    """Test convenience functions."""

    def test_is_safe_to_dispatch_safe(self):
        """Safe text passes."""
        is_safe, reason = is_safe_to_dispatch("hello world")
        assert is_safe is True
        assert reason is None

    def test_is_safe_to_dispatch_blocked(self):
        """Secret text is blocked."""
        is_safe, reason = is_safe_to_dispatch("my key is sk-1234567890abcdef1234567890abcdef")
        assert is_safe is False
        assert reason is not None
        assert "secret" in reason.lower()


if __name__ == "__main__":
    import unittest
    unittest.main()
