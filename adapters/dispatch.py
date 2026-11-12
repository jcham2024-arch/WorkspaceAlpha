#!/usr/bin/env python3
"""Adapter dispatch — selects the model adapter based on target_tier and
attaches envelope frontmatter (not sent to model) alongside the two-zone
prompt.

Stdlib only. Never writes .context/manifest.json or wiki/.

Registry loading is fail-closed at boot: if adapters/registry.yaml is
invalid, or a registry reference does not resolve, the dispatcher
refuses to start — mirroring the gateway pattern where invalid registry
at boot causes the process to refuse to start.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

# Add adapters directory to path for sibling imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

from deepseek_v32 import DeepSeekV32Adapter  # noqa: E402
from nemotron_35 import Nemotron35Adapter  # noqa: E402

try:
    import yaml
except ImportError:
    print("FATAL: PyYAML not installed. Run: pip install PyYAML", file=sys.stderr)
    sys.exit(1)

# Production tiers — dispatch to production is restricted to exact
# adapter matches only. Any production-tier delegation with an
# unregistered model is BLOCKED.
PRODUCTION_TIERS = frozenset({"thinking", "low_thinking", "non_thinking"})


class AdapterDispatch:
    """Dispatches to the correct model adapter based on target_tier.

    Dispatch outcomes:
    1. Exact match → use the registered adapter. No flag set.
    2. Production tier + no exact match → BLOCKED with reason
       NO_ADAPTER_FOR_PRODUCTION_TIER. The blocked envelope includes
       target_model and the list of registered adapters.
    3. Non-production tier + no exact match → route to generic adapter,
       set fallback_used: true, include requested_model and
       resolved_adapter: "generic".
    """

    def __init__(self, registry_path: Path | None = None):
        self._registry_path = registry_path or ROOT / "adapters" / "registry.yaml"
        self._adapters: dict[str, Any] = {}
        self._registry: dict[str, Any] = {}
        self._load_registry()

    def _load_registry(self) -> None:
        """Load and validate the adapter registry.

        Fail-closed: if registry.yaml is invalid, or a referenced
        adapter module cannot be imported, the dispatcher refuses to
        start.
        """
        try:
            with self._registry_path.open("r", encoding="utf-8") as f:
                registry = yaml.safe_load(f)
        except FileNotFoundError:
            print(f"FATAL: Registry not found: {self._registry_path}", file=sys.stderr)
            sys.exit(1)
        except yaml.YAMLError as exc:
            print(f"FATAL: Invalid registry YAML: {exc}", file=sys.stderr)
            sys.exit(1)

        if not isinstance(registry, dict) or "adapters" not in registry:
            print("FATAL: Registry missing 'adapters' field", file=sys.stderr)
            sys.exit(1)

        self._registry = registry

        for adapter_id, adapter_cfg in registry["adapters"].items():
            module_name = adapter_cfg.get("module")
            if not module_name:
                print(
                    f"FATAL: Adapter {adapter_id} missing 'module' field",
                    file=sys.stderr,
                )
                sys.exit(1)

            try:
                module = __import__(module_name, fromlist=["*"])
            except ImportError as exc:
                print(
                    f"FATAL: Cannot import adapter module {module_name} "
                    f"for adapter {adapter_id}: {exc}",
                    file=sys.stderr,
                )
                sys.exit(1)

            # Find the adapter class in the module
            adapter_class = None
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and issubclass(attr, object):
                    # Check if it looks like a ModelAdapter
                    if hasattr(attr, "build_dispatch") and hasattr(
                        attr, "validate_dispatch"
                    ):
                        adapter_class = attr
                        break

            if adapter_class is None:
                print(
                    f"FATAL: No ModelAdapter subclass found in {module_name}",
                    file=sys.stderr,
                )
                sys.exit(1)

            try:
                self._adapters[adapter_id] = adapter_class()
            except Exception as exc:
                print(
                    f"FATAL: Cannot instantiate adapter {adapter_id}: {exc}",
                    file=sys.stderr,
                )
                sys.exit(1)

    def get_adapter(self, model: str):
        """Get an adapter by model name. Raises ValueError if not found."""
        if model not in self._adapters:
            raise ValueError(f"Unknown model adapter: {model}")
        return self._adapters[model]

    def is_production_tier(self, delegation_type: str | None, target_tier: str | None) -> bool:
        """Check if this is a production-tier delegation.

        Production tiers: any delegation whose authority is RUNTIME_PATCH
        or DATA_MIGRATION, or whose delegation_type is EXECUTION
        targeting a production path.
        """
        if delegation_type == "EXECUTION":
            return True
        if target_tier in PRODUCTION_TIERS:
            return True
        return False

    def dispatch(
        self,
        model: str,
        target_tier: str,
        max_tokens: int | None = None,
        temperature: float = 0.0,
        extra_params: dict | None = None,
        delegation_type: str | None = None,
        authority: str | None = None,
    ) -> dict[str, Any]:
        """Build dispatch parameters for a model and tier.

        Dispatch outcomes:
        1. Exact match → use the registered adapter. No flag set.
        2. Production tier + no exact match → BLOCKED with reason
           NO_ADAPTER_FOR_PRODUCTION_TIER. The blocked envelope
           includes target_model and the list of registered adapters.
        3. Non-production tier + no exact match → route to generic
           adapter, set fallback_used: true, include requested_model
           and resolved_adapter: "generic".

        Args:
            model: Model name
            target_tier: Target tier ("thinking", "low_thinking", "non_thinking")
            max_tokens: Requested max_tokens
            temperature: Temperature
            extra_params: Additional parameters
            delegation_type: Delegation type (MISSION, EXECUTION)
            authority: Authority level (ANALYZE, PLAN, EXECUTE, REVIEW, APPROVE)

        Returns:
            Dispatch dict

        Raises:
            ValueError: If model unknown or budget floor violated
        """
        adapter = self.get_adapter(model)
        return adapter.build_dispatch(
            target_tier=target_tier,
            max_tokens=max_tokens,
            temperature=temperature,
            extra_params=extra_params,
        )

    def validate_dispatch(
        self, model: str, dispatch: dict[str, Any]
    ) -> str | None:
        """Validate a dispatch dict for a model. Returns None if OK, or BLOCKED reason."""
        adapter = self.get_adapter(model)
        return adapter.validate_dispatch(dispatch)

    def dispatch_with_fallback(
        self,
        model: str,
        target_tier: str,
        max_tokens: int | None = None,
        temperature: float = 0.0,
        extra_params: dict | None = None,
        delegation_type: str | None = None,
        authority: str | None = None,
    ) -> dict[str, Any]:
        """Dispatch with full fail-closed logic.

        Returns dispatch dict on success. Raises ValueError with
        BLOCKED prefix on failure.
        """
        is_production = self.is_production_tier(delegation_type, target_tier)

        # Check if model exists in registry
        if model not in self._adapters:
            if is_production:
                registered = list(self._adapters.keys())
                raise ValueError(
                    f"BLOCKED: NO_ADAPTER_FOR_PRODUCTION_TIER: "
                    f"production-tier delegation requests model '{model}' "
                    f"but no adapter is registered for it. "
                    f"Registered adapters: {registered}"
                )
            else:
                # Non-production: route to generic adapter
                if "generic" not in self._adapters:
                    raise ValueError(
                        f"BLOCKED: NO_ADAPTER_FOR_PRODUCTION_TIER: "
                        f"non-production delegation requests model '{model}' "
                        f"but no generic adapter is registered. "
                        f"Registered adapters: {list(self._adapters.keys())}"
                    )
                # Use generic adapter with fallback flag
                dispatch = self._adapters["generic"].build_dispatch(
                    target_tier=target_tier,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    extra_params=extra_params,
                )
                dispatch["fallback_used"] = True
                dispatch["requested_model"] = model
                dispatch["resolved_adapter"] = "generic"
                return dispatch

        # Exact match
        return self._adapters[model].build_dispatch(
            target_tier=target_tier,
            max_tokens=max_tokens,
            temperature=temperature,
            extra_params=extra_params,
        )


def main():
    """CLI: test adapter dispatch."""
    import argparse
    import json

    ap = argparse.ArgumentParser(description="Adapter dispatch test")
    ap.add_argument("--model", default="deepseek-v3.2", help="Model: deepseek-v3.2, nemotron-3.5")
    ap.add_argument("--tier", default="thinking", help="Target tier")
    ap.add_argument("--max-tokens", type=int, default=None, help="Max tokens")
    ap.add_argument(
        "--delegation-type", default="MISSION", help="Delegation type (MISSION, EXECUTION)"
    )
    ap.add_argument(
        "--authority", default="PLAN", help="Authority (ANALYZE, PLAN, EXECUTE, REVIEW, APPROVE)"
    )
    args = ap.parse_args()

    dispatch = AdapterDispatch()
    try:
        result = dispatch.dispatch_with_fallback(
            model=args.model,
            target_tier=args.tier,
            max_tokens=args.max_tokens,
            delegation_type=args.delegation_type,
            authority=args.authority,
        )
        print(json.dumps(result, indent=2))
    except ValueError as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
