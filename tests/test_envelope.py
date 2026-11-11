#!/usr/bin/env python3
"""Tests for envelope schema validation.

Tests that handoff and return envelopes validate against their JSON schemas.
"""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS_DIR = ROOT / "schemas"
ENVELOPE_DIR = ROOT / "envelope"


def load_schema(name: str) -> dict:
    # Try envelope/ first, then schemas/
    for directory in [ENVELOPE_DIR, SCHEMAS_DIR]:
        path = directory / name
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    raise FileNotFoundError(f"Schema not found: {name}")


class TestEnvelopeSchema(unittest.TestCase):
    """Test envelope schema validation (manual validation since jsonschema may not be installed)."""

    def test_handoff_envelope_schema_has_required_fields(self):
        schema = load_schema("handoff-envelope.schema.json")
        self.assertEqual(schema["$id"].endswith("handoff-envelope.schema.json"), True)
        required = schema.get("required", [])
        self.assertIn("envelope_version", required)
        self.assertIn("delegation_id", required)
        self.assertIn("from_agent", required)
        self.assertIn("to_agent", required)
        self.assertIn("delegation_type", required)
        self.assertIn("target_tier", required)
        self.assertIn("authority", required)
        self.assertIn("return_schema", required)
        self.assertIn("return_format", required)

    def test_handoff_envelope_delegation_type_enum(self):
        schema = load_schema("handoff-envelope.schema.json")
        prop = schema["properties"]["delegation_type"]
        self.assertEqual(prop["enum"], ["MISSION", "EXECUTION"])

    def test_handoff_envelope_target_tier_enum(self):
        schema = load_schema("handoff-envelope.schema.json")
        prop = schema["properties"]["target_tier"]
        self.assertEqual(prop["enum"], ["thinking", "low_thinking", "non_thinking"])

    def test_handoff_envelope_authority_enum(self):
        schema = load_schema("handoff-envelope.schema.json")
        prop = schema["properties"]["authority"]
        self.assertIn("ANALYZE", prop["enum"])
        self.assertIn("PLAN", prop["enum"])
        self.assertIn("EXECUTE", prop["enum"])
        self.assertIn("REVIEW", prop["enum"])
        self.assertIn("APPROVE", prop["enum"])

    def test_handoff_envelope_return_format_enum(self):
        schema = load_schema("handoff-envelope.schema.json")
        prop = schema["properties"]["return_format"]
        self.assertEqual(prop["enum"], ["json", "diff", "markdown_summary"])

    def test_return_envelope_schema_has_required_fields(self):
        schema = load_schema("return-envelope.schema.json")
        required = schema.get("required", [])
        self.assertIn("delegation_id", required)
        self.assertIn("status", required)
        self.assertIn("acceptance_results", required)
        self.assertIn("steps_used", required)

    def test_return_envelope_status_enum(self):
        schema = load_schema("return-envelope.schema.json")
        prop = schema["properties"]["status"]
        self.assertEqual(prop["enum"], ["COMPLETE", "BLOCKED", "FAILED", "PARTIAL"])

    def test_return_envelope_acceptance_result_structure(self):
        schema = load_schema("return-envelope.schema.json")
        items = schema["properties"]["acceptance_results"]["items"]
        self.assertIn("criterion", items["required"])
        self.assertIn("result", items["required"])
        self.assertIn("evidence", items["required"])

    def test_sample_handoff_envelope_matches_schema(self):
        """A sample handoff envelope should satisfy all required fields and enum constraints."""
        schema = load_schema("handoff-envelope.schema.json")
        envelope = {
            "envelope_version": "1.0",
            "delegation_id": "del-test-001",
            "from_agent": "conceptualizer",
            "to_agent": "taskmaster",
            "delegation_type": "MISSION",
            "target_tier": "thinking",
            "authority": "PLAN",
            "allowed_targets": ["docs/README.md"],
            "forbidden_targets": [".agent/.env"],
            "max_steps": 12,
            "termination_signal": "MISSION_COMPLETE",
            "return_schema": "schemas/return-envelope.schema.json",
            "return_format": "json",
        }
        for field in schema["required"]:
            self.assertIn(field, envelope, f"Missing required field: {field}")
        self.assertIn(envelope["delegation_type"], schema["properties"]["delegation_type"]["enum"])
        self.assertIn(envelope["target_tier"], schema["properties"]["target_tier"]["enum"])
        self.assertIn(envelope["authority"], schema["properties"]["authority"]["enum"])
        self.assertIn(envelope["return_format"], schema["properties"]["return_format"]["enum"])

    def test_sample_return_envelope_matches_schema(self):
        """A sample return envelope should satisfy all required fields and enum constraints."""
        schema = load_schema("return-envelope.schema.json")
        envelope = {
            "delegation_id": "del-test-001",
            "status": "COMPLETE",
            "acceptance_results": [
                {"criterion": 1, "result": "PASS", "evidence": "auth.py:142"}
            ],
            "artifacts": [{"type": "diff", "path": "auth.py.patch"}],
            "residual_risks": [],
            "steps_used": 7,
        }
        for field in schema["required"]:
            self.assertIn(field, envelope, f"Missing required field: {field}")
        self.assertIn(envelope["status"], schema["properties"]["status"]["enum"])
        for ar in envelope["acceptance_results"]:
            self.assertIn(ar["result"], ["PASS", "FAIL", "SKIP"])


if __name__ == "__main__":
    unittest.main()
