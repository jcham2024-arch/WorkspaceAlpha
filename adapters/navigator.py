#!/usr/bin/env python3
"""STAIR navigator adapter — single-shot manager-tier prediction dispatch.

Extracted from stair_navigator.py. LLM dispatch is the adapter layer's job:
manager tier only, a hard wall-clock cap, and no retries. The navigator
predicts exactly once; fallback to VECTOR is the router's decision.
"""
from __future__ import annotations

import signal
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(0, str(ROOT / "adapters"))
from dispatch import AdapterDispatch  # noqa: E402

MANAGER_TIER = "thinking"
TIMEOUT_SECONDS = 15.0


class NavigatorTimeout(Exception):
    """The navigator's prediction call exceeded its hard wall-clock cap."""


class NavigatorDispatchError(Exception):
    """The adapter layer failed to produce a prediction."""


def _alarm_handler(signum, frame):  # noqa: ARG001
    raise NavigatorTimeout(f"prediction exceeded {TIMEOUT_SECONDS}s")


def dispatch_prediction(query: str, toc: dict, *, max_depth: int = 6) -> dict | None:
    """Single-shot prediction. No retries, no self-correction.

    Runs the manager-tier adapter under a hard wall-clock cap. If the cap is
    exceeded, raises NavigatorTimeout — never retries. Returns the adapter
    payload dict, or None if none was produced.
    """
    old_handler = signal.signal(signal.SIGALRM, _alarm_handler)
    signal.setitimer(signal.ITIMER_REAL, TIMEOUT_SECONDS)
    try:
        dispatcher = AdapterDispatch()
        try:
            dispatch_result = dispatcher.dispatch(
                model="nemotron-3.5",
                target_tier=MANAGER_TIER,
                max_tokens=16384,
                temperature=0.0,
                extra_params={
                    "prompt": query,
                    "toc": toc,
                    "max_depth": max_depth,
                },
            )
        except ValueError as exc:
            raise NavigatorDispatchError(str(exc)) from exc
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, old_handler)

    if not isinstance(dispatch_result, dict):
        return None
    payload = dispatch_result.get("payload", {})
    return payload or None
