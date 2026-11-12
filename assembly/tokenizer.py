#!/usr/bin/env python3
"""TokenCounter — pluggable token counting for the DAG compiler budgeter.

Provides three counter implementations:

- TiktokenCounter: OpenAI/tiktoken-compatible (DeepSeek, Nemotron 3.5 BPE)
- HuggingFaceCounter: sentence-transformers / transformers tokenizers
- HeuristicCounter: bytes // 4 — estimation ONLY, compaction-trigger only

The heuristic counter is NOT suitable for budget enforcement (5-20% error).
It is used only as a fast pre-check to decide whether a precise count is
needed. When enforce_budget=True, the heuristic counter is rejected and the
assembler falls back to BLOCKED with TOKEN_COUNTER_UNAVAILABLE if no
accurate counter is available.
"""
from __future__ import annotations

import importlib
from abc import ABC, abstractmethod


class TokenCounter(ABC):
    """Abstract token counter interface.

    Implementations must provide accurate token counts for a given model.
    The counter is selected per adapter based on the model's vocabulary family.
    """

    @abstractmethod
    def count(self, text: str, model_id: str | None = None) -> int:
        """Return the estimated token count for *text*.

        Args:
            text: The text to count tokens for.
            model_id: Optional model identifier to select the correct
                tokenizer variant (e.g., different DeepSeek models).

        Returns:
            Estimated token count.
        """
        ...


class TiktokenCounter(TokenCounter):
    """Token counter using the `tiktoken` library.

    Supports OpenAI-family models and compatible BPE tokenizers
    (DeepSeek, Nemotron, etc.) via cl100k_base or other encodings.
    """

    def __init__(self, encoding_name: str = "cl100k_base") -> None:
        try:
            import tiktoken

            self._encoding = tiktoken.get_encoding(encoding_name)
        except ImportError as exc:
            raise ImportError(
                "tiktoken not installed. Run: pip install tiktoken"
            ) from exc

    def count(self, text: str, model_id: str | None = None) -> int:
        return len(self._encoding.encode(text))


class HuggingFaceCounter(TokenCounter):
    """Token counter using HuggingFace tokenizers library.

    Supports models with HuggingFace-compatible tokenizers
    (LLaMA, Mistral, etc.).
    """

    def __init__(self, tokenizer_name: str) -> None:
        try:
            from transformers import AutoTokenizer

            self._tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
        except ImportError as exc:
            raise ImportError(
                "transformers not installed. Run: pip install transformers"
            ) from exc

    def count(self, text: str, model_id: str | None = None) -> int:
        return len(self._tokenizer.encode(text))


class HeuristicCounter(TokenCounter):
    """Estimator counter: bytes // 4.

    NOT suitable for budget enforcement — error margin is 5-20%.
    Used only as a fast pre-check to decide whether a precise count
    is needed. When enforce_budget=True, this counter is rejected
    and the assembler falls back to BLOCKED with
    TOKEN_COUNTER_UNAVAILABLE if no accurate counter is available.
    """

    def count(self, text: str, model_id: str | None = None) -> int:
        return len(text.encode("utf-8")) // 4


# Registry of available counters by name
COUNTER_REGISTRY: dict[str, type[TokenCounter]] = {
    "tiktoken": TiktokenCounter,
    "huggingface": HuggingFaceCounter,
    "heuristic": HeuristicCounter,
}


def get_counter(counter_type: str, **kwargs: Any) -> TokenCounter:
    """Create a TokenCounter instance by type name.

    Args:
        counter_type: One of "tiktoken", "huggingface", "heuristic".
        **kwargs: Passed to the counter constructor.

    Returns:
        A TokenCounter instance.

    Raises:
        ValueError: If counter_type is unknown.
        ImportError: If the required package is not installed.
    """
    if counter_type not in COUNTER_REGISTRY:
        raise ValueError(f"Unknown token counter type: {counter_type}")
    return COUNTER_REGISTRY[counter_type](**kwargs)
