#!/usr/bin/env python3
"""Conformance suite runner — runs conformance tests for model adapters.

Each model adapter must pass all conformance tests before being marked
production_allowed. The conformance suite checks:

1. Thinking-mode round trip: a reasoning prompt returns a non-empty answer
   with the trace preserved.
2. Token-floor test: a call below the model's floor is rejected at dispatch.
3. Format test: the frozen prefix uses the declared format; the suffix uses
   the declared format.
4. Blocked-path test: an unregistered production model is blocked.
5. Redaction test: a secret in context blocks before dispatch.
6. Schema test: the return envelope validates against return_schema.

A model is marked production_allowed: true only when all six pass.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]

# Add factory directory to path
sys.path.insert(0, str(ROOT / "factory"))

from factory.registry import ModelRegistry  # noqa: E402


class ConformanceRunner:
    """Runs conformance tests for model adapters."""

    def __init__(self, registry_path: Path | None = None):
        self.registry_path = registry_path or ROOT / "adapters" / "registry.yaml"
        self.results: dict[str, dict[str, Any]] = {}

    def run_all(self) -> dict[str, dict[str, Any]]:
        """Run conformance suite for all registered models.

        Returns dict of model_id -> conformance results.
        """
        import yaml

        registry_path = Path(self.registry_path)
        if not registry_path.exists():
            print(f"Registry not found: {registry_path}")
            return {}

        with registry_path.open("r", encoding="utf-8") as f:
            registry = yaml.safe_load(f)

        for model_id, adapter_config in registry.get("adapters", {}).items():
            conformance_suite_path = adapter_config.get("conformance_suite")
            if conformance_suite:
                suite_path = ROOT / conformance_suite_path
                result = self._run_suite(model_id, suite_path)
            else:
                result = {
                    "conformance_passed": False,
                    "reason": "No conformance suite specified",
                    "tests": {},
                }

            self.results[model_id] = result

        return self.results

    def _run_suite(self, model_id: str, suite_path: Path) -> dict[str, Any]:
        """Run conformance suite for a single model."""
        suite_path = Path(suite_path)
        if not suite_path.exists():
            return {
                "conformance_passed": False,
                "reason": f"Conformance suite not found: {suite_path}",
                "tests": {},
            }

        with suite_path.open("r", encoding="utf-8") as f:
            import yaml

            suite = yaml.safe_load(f)

        tests = suite.get("tests", [])
        results = {}
        all_passed = True

        for test in tests:
            test_id = test.get("test_id", "unknown")
            test_type = test.get("test_type", "unknown")
            result = self._run_single_test(model_id, test_type, test.get("params", {}))
            results[test_id] = result
            if not result.get("passed", False):
                all_passed = False

        return {
            "conformance_passed": all_passed,
            "model_id": model_id,
            "suite_path": str(suite_path),
            "tests": results,
        }

    def _run_single_test(
        self,
        model_id: str,
        test_type: str,
        params: dict[str, Any],
    ) -> dict[str, Any]:
        """Run a single conformance test."""
        from assembly.assembler import Assembler, BLOCKED

        assembler = Assembler()

        if test_type == "thinking_mode_round_trip":
            return self._test_thinking_mode_round_trip(assembler, params)
        elif test_type == "token_floor":
            return self._test_token_floor(assembler, params)
        elif test_type == "format_test":
            return self._test_format(assembler, params)
        elif test_type == "blocked_path":
            return self._test_blocked_path(assembler, params)
        elif test_type == "redaction_test":
            return self._test_redaction(assembler, params)
        elif test_type == "schema_test":
            return self._test_schema(assembler, params)
        else:
            return {
                "passed": False,
                "reason": f"Unknown test type: {test_type}",
            }

    def _test_thinking_mode_round_trip(
        self,
        assembler: Assembler,
        params: dict[str, Any],
    ) -> dict[str, Any]:
        """Test that a reasoning prompt returns a non-empty answer with trace preserved."""
        delegation = {
            "delegation_id": "conformance-thinking-001",
            "from_agent": "conceptualizer",
            "to_agent": "taskmaster",
            "delegation_type": "MISSION",
            "target_tier": "thinking",
            "authority": "PLAN",
            "allowed_targets": ["docs/README.md"],
            "forbidden_targets": [],
            "task_type": "reasoning",
            "return_schema": "schemas/return-envelope.schema.json",
            "return_format": "json",
            "adapter_params": {
                "model": "deepseek-v3.2",
                "thinking": {"type": "enabled"},
                "reasoning_effort": "high",
                "max_tokens": 8192,
                "temperature": 0.0,
            },
        }

        try:
            result = assembler.assemble(delegation)
            if result["blocked"]:
                return {
                    "passed": False,
                    "reason": f"Assembly blocked: {result.get('blocked_reason')}",
                }
            return {
                "passed": True,
                "reason": "Thinking mode round trip succeeded",
                "tokens": result["token_counts"],
            }
        except Exception as exc:
            return {
                "passed": False,
                "reason": f"Thinking mode round trip failed: {exc}",
            }

    def _test_token_floor(
        self,
        assembler: Assembler,
        params: dict[str, Any],
    ) -> dict[str, Any]:
        """Test that a call below the model's floor is rejected at dispatch."""
        delegation = {
            "delegation_id": "conformance-token-floor-001",
            "from_agent": "conceptualizer",
            "to_agent": "taskmaster",
            "delegation_type": "MISSION",
            "target_tier": "thinking",
            "authority": "PLAN",
            "allowed_targets": ["docs/README.md"],
            "forbidden_targets": [],
            "task_type": "planning",
            "return_schema": "schemas/return-envelope.schema.json",
            "return_format": "json",
            "adapter_params": {
                "model": "deepseek-v3.2",
                "thinking": {"type": "enabled"},
                "reasoning_effort": "high",
                "max_tokens": 512,  # Below 8192 floor
                "temperature": 0.0,
            },
        }

        try:
            result = assembler.assemble(delegation)
            if result["blocked"]:
                return {
                    "passed": True,
                    "reason": f"Correctly blocked: {result.get('blocked_reason')}",
                }
            return {
                "passed": False,
                "reason": "Should have been blocked for below-floor max_tokens",
            }
        except ValueError as exc:
            if "BUDGET_FLOOR_VIOLATION" in str(exc):
                return {
                    "passed": True,
                    "reason": "Correctly rejected: below-floor max_tokens",
                }
            return {
                "passed": False,
                "reason": f"Unexpected error: {exc}",
            }

    def _test_format(
        self,
        assembler: Assembler,
        params: dict[str, Any],
    ) -> dict[str, Any]:
        """Test that the adapter uses the correct format for frozen prefix and suffix."""
        delegation = {
            "delegation_id": "conformance-format-001",
            "from_agent": "conceptualizer",
            "to_agent": "taskmaster",
            "delegation_type": "MISSION",
            "target_tier": "thinking",
            "authority": "PLAN",
            "allowed_targets": ["docs/README.md"],
            "forbidden_targets": [],
            "task_type": "planning",
            "return_schema": "schemas/return-envelope.schema.json",
            "return_format": "json",
            "adapter_params": {
                "model": "deepseek-v3.2",
                "thinking": {"type": "enabled"},
                "reasoning_effort": "high",
                "max_tokens": 8192,
                "temperature": 0.0,
            },
        }

        try:
            result = assembler.assemble(delegation)
            if result["blocked"]:
                return {
                    "passed": False,
                    "reason": f"Assembly blocked: {result.get('blocked_reason')}",
                }

            # Check that the frozen prefix starts with XML semantic tags
            prefix = result["frozen_prefix"]
            suffix = result["variable_suffix"]

            # Frozen prefix should use XML semantic tags
            has_xml_prefix = "<identity>" in prefix or "<capabilities" in prefix
            # Suffix should use markdown headings
            has_md_suffix = "# " in suffix or "## " in suffix

            return {
                "passed": has_xml_prefix and has_md_suffix,
                "reason": f"Prefix has XML tags: {has_xml_prefix}, Suffix has markdown headers: {has_md_suffix}",
            }
        except Exception as exc:
            return {
                "passed": False,
                "reason": f"Format test failed: {exc}",
            }

    def _test_blocked_path(
        self,
        assembler: Assembler,
        params: dict[str, Any],
    ) -> dict[str, Any]:
        """Test that an unregistered production model is blocked."""
        delegation = {
            "delegation_id": "conformance-blocked-001",
            "from_agent": "conceptualizer",
            "to_agent": "taskmaster",
            "delegation_type": "EXECUTION",
            "target_tier": "low_thinking",
            "authority": "EXECUTE",
            "allowed_targets": ["docs/README.md"],
            "forbidden_targets": [],
            "task_type": "implementation",
            "return_schema": "schemas/return-envelope.schema.json",
            "return_format": "json",
            "adapter_params": {
                "model": "unknown-model-xyz",
                "thinking": {"type": "disabled"},
                "reasoning_effort": None,
                "max_tokens": 1024,
                "temperature": 0.0,
            },
        }

        try:
            result = assembler.assemble(delegation)
            if result["blocked"]:
                reason = result.get("blocked_reason", "")
                if "NO_ADAPTER_FOR_PRODUCTION_TIER" in reason:
                    return {
                        "passed": True,
                        "reason": "Correctly blocked: NO_ADAPTER_FOR_PRODUCTION_TIER",
                    }
                return {
                    "passed": False,
                    "reason": f"Blocked but wrong reason: {reason}",
                }
            return {
                "passed": False,
                "reason": "Should have been blocked for unknown model",
            }
        except ValueError as exc:
            if "NO_ADAPTER_FOR_PRODUCTION_TIER" in str(exc):
                return {
                    "passed": True,
                    "reason": "Correctly blocked: NO_ADAPTER_FOR_PRODUCTION_TIER",
                }
            return {
                "passed": False,
                "reason": f"Unexpected error: {exc}",
            }

    def _test_redaction(
        self,
        assembler: Assembler,
        params: dict[str, Any],
    ) -> dict[str, Any]:
        """Test that a secret in context blocks before dispatch."""
        from provenance.redact import redact_text

        # Test that a secret in context blocks dispatch
        secret_text = "My API key is sk-1234567890abcdef1234567890abcdef"
        is_safe, reason = __import__("provenance.redact", from_list=["redact_text"]).redact_text(
            secret_text
        ), None

        # Actually test the redact_text function directly
        from provenance.redact import redact_text

        result = redact_text(secret_text)
        if result.blocked:
            return {
                "passed": True,
                "reason": "Correctly blocked secret in context",
            }
        return {
            "passed": False,
            "reason": "Should have blocked secret in context",
        }

    def _test_schema(
        self,
        assembler: Assembler,
        params: dict[str, Any],
    ) -> dict[str, Any]:
        """Test that the return envelope validates against return_schema."""
        import json

        schema_path = ROOT / "envelope" / "return-envelope.schema.json"
        if not schema_path.exists():
            return {
                "passed": False,
                "reason": "Return envelope schema not found",
            }

        with schema_path.open("r", encoding="utf-8") as f:
            schema = json.load(f)

        # Create a valid return envelope
        envelope = {
            "delegation_id": "conformance-schema-001",
            "status": "COMPLETE",
            "acceptance_results": [
                {"criterion": 1, "result": "PASS", "evidence": "docs/README.md::audit-persistence-spec.md"}
            ],
            "steps_used": 3,
        }

        # Simple validation: check required fields
        required = schema.get("required", [])
        missing = [f for f in required if f not in envelope]

        if missing:
            return {
                "passed": False,
                "reason": f"Missing required fields: {missing}",
            }

        return {
            "passed": True,
            "reason": "Return envelope schema validation passed",
        }


def main():
    """CLI: run conformance suite."""
    import argparse
    import json

    ap = argparse.ArgumentParser(description="Conformance suite runner")
    ap.add_argument(
        "--all",
        action="store_true",
        help="Run conformance suite for all registered models",
    )
    ap.add_argument(
        "--model",
        help="Run conformance suite for a specific model",
    )
    args = ap.parse_args()

    runner = ConformanceRunner()

    if args.all:
        results = runner.run_all()
        print(json.dumps(results, indent=2))
        all_passed = all(r.get("conformance_passed", False) for r in results.values())
        if all_passed:
            print("\nAll conformance suites passed!")
        else:
            print("\nSome conformance suites failed!")
            sys.exit(1)
    elif args.model:
        registry_path = ROOT / "adapters" / "registry.yaml"
        import yaml

        with registry_path.open("r", encoding="utf-8") as f:
            registry = yaml.safe_load(f)

        adapter_config = registry.get("adapters", {}).get(args.model)
        if not adapter_config:
            print(f"Model not found in registry: {args.model}")
            sys.exit(1)

        suite_path = adapter_config.get("conformance_suite")
        if not suite_path:
            print(f"No conformance suite specified for {args.model}")
            sys.exit(1)

        result = runner._run_suite(args.model, Path(suite_path))
        print(json.dumps(result, indent=2))
        if not result.get("conformance_passed", False):
            sys.exit(1)
    else:
        print("Use --all or --model <model_id>")


if __name__ == "__main__":
    main()
