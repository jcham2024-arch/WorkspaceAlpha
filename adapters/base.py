#!/usr/bin/env python3
"""ModelAdapter contract — abstract base class for all model adapters.

Every model adapter must implement this interface. The dispatcher
rejects any adapter that does not implement capability_manifest.
"""
from __future__ import annotations

import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class DispatchResult:
    """Result of dispatching a prompt to a model adapter.

    Attributes:
        payload: The request payload to send to the model API.
        model: The model name that will be invoked.
        tier: The target tier (thinking, low_thinking, non_thinking).
        max_tokens: Max tokens setting.
        temperature: Temperature setting.
        thinking: Thinking configuration (dict or None).
        reasoning_effort: Reasoning effort level.
    """

    payload: dict[str, Any]
    model: str
    tier: str
    max_tokens: int
    temperature: float
    thinking: dict | None
    reasoning_effort: str | None


@dataclass
class ValidationResult:
    """Result of validating a model response.

    Attributes:
        valid: Whether the response is valid.
        errors: List of validation error messages.
        parsed: Parsed response if valid, None if invalid.
    """

    valid: bool
    errors: list[str]
    parsed: dict[str, Any] | None


@dataclass
class CapabilityManifest:
    """Describes what an adapter can do.

    Attributes:
        model_id: Unique model identifier.
        provider: Model provider name.
        context_window: Maximum context window in tokens.
        max_tokens_floor: Minimum max_tokens value.
        production_allowed: Whether this adapter can be used in production.
        reasoning_modes: List of supported reasoning modes.
        format_preferences: Format preferences for prompt construction.
        conformance_suite: Path to conformance test file.
    """

    model_id: str
    provider: str
    context_window: int
    max_tokens_floor: int
    production_allowed: bool
    reasoning_modes: list[str]
    format_preferences: dict[str, str]
    conformance_suite: str


class ModelAdapter(ABC):
    """Abstract base class for model adapters.

    Every adapter must implement this interface. The dispatcher
    rejects any adapter that does not implement capability_manifest.
    """

    @abstractmethod
    def build_dispatch(
        self,
        target_tier: str,
        max_tokens: int | None = None,
        temperature: float = 0.0,
        extra_params: dict[str, Any] | None = None,
    ) -> DispatchResult:
        """Build dispatch parameters for a model and tier.

        Args:
            target_tier: Target tier ("thinking", "low_thinking", "non_thinking")
            max_tokens: Requested max_tokens
            temperature: Temperature setting
            extra_params: Additional parameters

        Returns:
            DispatchResult with payload, model, tier, max_tokens, temperature,
            thinking, and reasoning_effort

        Raises:
            ValueError: If max_tokens is below the tier floor or model not supported
        """
        ...

    @abstractmethod
    def validate_dispatch(self, dispatch: dict[str, Any]) -> str | None:
        """Validate a dispatch dict. Returns None if OK, or BLOCKED reason string."""
        ...

    @abstractmethod
    def capability_manifest(self) -> CapabilityManifest:
        """Return the capability manifest for this adapter."""
        ...

    @abstractmethod
    def count_tokens(self, text: str, model_id: str | None = None) -> int:
        """Count tokens using the adapter's tokenizer."""
        ...


class ModelAdapterError(Exception):
    """Base exception for adapter errors."""
    pass


class ModelNotFoundError(ModelAdapterError):
    """Raised when a model adapter is not found."""
    pass


class BudgetFloorViolationError(ModelAdapterError):
    """Raised when max_tokens is below the tier floor."""
    pass
