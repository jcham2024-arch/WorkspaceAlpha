#!/usr/bin/env python3
"""OpenTelemetry GenAI instrumentation for WorkspaceAlpha.

Implements OpenTelemetry GenAI semantic conventions for LLM observability:

- `gen_ai.operation.name` — operation type (chat, invoke_agent, execute_tool)
- `gen_ai.system` — model provider (deepseek, nemotron, etc.)
- `gen_ai.request.model` — requested model name
- `gen_ai.response.model` — responding model name
- `gen_ai.usage.input_tokens` — input token count
- `gen_ai.usage.output_tokens` — output token count
- `gen_ai.response.finish_reasons` — why the model stopped
- `gen_ai.request.temperature` — temperature setting
- `gen_ai.request.max_tokens` — max tokens setting

Content-capture contract:
- Default: do NOT capture inputs/outputs (opt-in only)
- Recommended: store content externally, record references (pointer IDs) on spans
- This is the OWASP content-poisoning defense for observability

Stdlib only — no OpenTelemetry SDK dependency. Emits structured log records
that can be consumed by any OTel-compatible collector.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
LOG_PATH = ROOT / "telemetry" / "otel_genai.jsonl"


class OTelGenAIRecorder:
    """Records OpenTelemetry GenAI spans as JSONL records.

    Each record represents one span with GenAI semantic convention attributes.
    Content capture is opt-in — by default only metadata is recorded.
    """

    def __init__(self, log_path: Path | None = None, capture_content: bool = False):
        self.log_path = log_path or LOG_PATH
        self.capture_content = capture_content
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def record_chat_span(
        self,
        span_id: str,
        trace_id: str,
        model_name: str,
        provider: str = "deepseek",
        input_tokens: int = 0,
        output_tokens: int = 0,
        finish_reason: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        system_prompt_hash: str | None = None,
        request_ref: str | None = None,
        response_ref: str | None = None,
        duration_ms: float | None = None,
        status: str = "ok",
        error_message: str | None = None,
        span_kind: str = "client",
    ) -> dict:
        """Record a chat span (model invocation).

        Args:
            span_id: Unique span identifier.
            trace_id: Trace identifier for distributed tracing.
            model_name: Name of the model used.
            provider: Model provider name (deepseek, nemotron, etc.)
            input_tokens: Number of input tokens.
            output_tokens: Number of output tokens.
            finish_reason: Why the model stopped (stop, length, etc.)
            temperature: Temperature setting.
            max_tokens: Max tokens setting.
            system_prompt_hash: Hash of the system prompt (not the text).
            request_ref: Reference to stored request content (opt-in).
            response_ref: Reference to stored response content (opt-in).
            duration_ms: Span duration in milliseconds.
            status: Span status (ok, error).
            error_message: Error message if status is error.
            span_kind: Span kind (client, server, etc.)

        Returns:
            The span record dict.
        """
        span = {
            "span_id": span_id,
            "trace_id": trace_id,
            "span_name": f"chat {model_name}",
            "span_kind": span_kind,
            "start_time": datetime.now(timezone.utc).isoformat(),
            # GenAI semantic conventions
            "gen_ai.operation.name": "chat",
            "gen_ai.system": provider,
            "gen_ai.request.model": model_name,
            "gen_ai.response.model": model_name,
            "gen_ai.usage.input_tokens": input_tokens,
            "gen_ai.usage.output_tokens": output_tokens,
            "gen_ai.response.finish_reasons": [finish_reason] if finish_reason else [],
            # Optional attributes
        }

        if temperature is not None:
            span["gen_ai.request.temperature"] = temperature
        if max_tokens is not None:
            span["gen_ai.request.max_tokens"] = max_tokens

        # Content references (opt-in — never raw content)
        if system_prompt_hash:
            span["gen_ai.request.system_prompt_hash"] = system_prompt_hash
        if request_ref:
            span["gen_ai.request.content_ref"] = request_ref
        if response_ref:
            span["gen_ai.response.content_ref"] = response_ref

        if duration_ms is not None:
            span["duration_ms"] = duration_ms
        if status:
            span["status"] = status
        if error_message:
            span["error.message"] = error_message

        self._write_record(span)
        return span

    def record_invoke_agent_span(
        self,
        span_id: str,
        trace_id: str,
        agent_name: str,
        agent_type: str = "taskmaster",
        input_tokens: int = 0,
        output_tokens: int = 0,
        finish_reason: str | None = None,
        duration_ms: float | None = None,
        status: str = "ok",
        error_message: str | None = None,
    ) -> dict:
        """Record an invoke_agent span (agent-to-agent delegation).

        Args:
            span_id: Unique span identifier.
            trace_id: Trace identifier.
            agent_name: Name of the agent being invoked.
            agent_type: Type of agent (taskmaster, coder, researcher, etc.)
            input_tokens: Input token count.
            output_tokens: Output token count.
            finish_reason: Why the agent stopped.
            duration_ms: Span duration.
            status: Span status.
            error_message: Error message if error.

        Returns:
            The span record dict.
        """
        span = {
            "span_id": span_id,
            "trace_id": trace_id,
            "span_name": f"invoke_agent {agent_name}",
            "span_kind": "client",
            "start_time": datetime.now(timezone.utc).isoformat(),
            "gen_ai.operation.name": "invoke_agent",
            "gen_ai.system": agent_type,
            "gen_ai.request.model": agent_name,
            "gen_ai.response.model": agent_name,
            "gen_ai.usage.input_tokens": input_tokens,
            "gen_ai.usage.output_tokens": output_tokens,
            "gen_ai.response.finish_reasons": [finish_reason] if finish_reason else [],
        }

        if duration_ms is not None:
            span["duration_ms"] = duration_ms
        if status:
            span["status"] = status
        if error_message:
            span["error.message"] = error_message

        self._write_record(span)
        return span

    def record_tool_span(
        self,
        span_id: str,
        trace_id: str,
        tool_name: str,
        input_tokens: int = 0,
        output_tokens: int = 0,
        finish_reason: str | None = None,
        duration_ms: float | None = None,
        status: str = "ok",
        error_message: str | None = None,
    ) -> dict:
        """Record an execute_tool span (tool execution).

        Args:
            span_id: Unique span identifier.
            trace_id: Trace identifier.
            tool_name: Name of the tool executed.
            input_tokens: Input token count.
            output_tokens: Output token count.
            finish_reason: Why the tool stopped.
            duration_ms: Span duration.
            status: Span status.
            error_message: Error message if error.

        Returns:
            The span record dict.
        """
        span = {
            "span_id": span_id,
            "trace_id": trace_id,
            "span_name": f"execute_tool {tool_name}",
            "span_kind": "client",
            "start_time": datetime.now(timezone.utc).isoformat(),
            "gen_ai.operation.name": "execute_tool",
            "gen_ai.system": tool_name,
            "gen_ai.request.model": tool_name,
            "gen_ai.response.model": tool_name,
            "gen_ai.usage.input_tokens": input_tokens,
            "gen_ai.usage.output_tokens": output_tokens,
            "gen_ai.response.finish_reasons": [finish_reason] if finish_reason else [],
        }

        if duration_ms is not None:
            span["duration_ms"] = duration_ms
        if status:
            span["status"] = status
        if error_message:
            span["error.message"] = error_message

        self._write_record(span)
        return span

    def _write_record(self, span: dict) -> None:
        """Append a span record to the JSONL file."""
        with self.log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(span, ensure_ascii=False) + "\n")


def main():
    """CLI: test OTel GenAI recorder."""
    import argparse

    ap = argparse.ArgumentParser(description="OTel GenAI recorder test")
    ap.add_argument(
        "--record-chat",
        action="store_true",
        help="Record a test chat span",
    )
    ap.add_argument(
        "--record-invoke-agent",
        action="store_true",
        help="Record a test invoke_agent span",
    )
    ap.add_argument(
        "--record-execute-tool",
        action="store_true",
        help="Record a test execute_tool span",
    )
    args = ap.parse_args()

    recorder = OTelGenAIRecorder()

    if args.record_chat:
        span = recorder.record_chat_span(
            span_id="span-001",
            trace_id="trace-001",
            model_name="deepseek-v3.2",
            provider="deepseek",
            input_tokens=1500,
            output_tokens=800,
            finish_reason="stop",
            temperature=0.7,
            max_tokens=8192,
            system_prompt_hash="sha256:abc123",
            request_ref="req-001",
            response_ref="resp-001",
            duration_ms=1250.5,
        )
        print(json.dumps(span, indent=2))
    elif args.record_invoke_agent:
        span = recorder.record_invoke_agent_span(
            span_id="span-002",
            trace_id="trace-001",
            agent_name="taskmaster",
            agent_type="taskmaster",
            input_tokens=2000,
            output_tokens=1200,
            finish_reason="stop",
            duration_ms=3400.0,
        )
        print(json.dumps(span, indent=2))
    elif args.record_execute_tool:
        span = recorder.record_execute_tool_span(
            span_id="span-003",
            trace_id="trace-001",
            tool_name="read_section",
            input_tokens=100,
            output_tokens=300,
            finish_reason="stop",
            duration_ms=45.2,
        )
        print(json.dumps(span, indent=2))
    else:
        print("Use --record-chat, --record-invoke-agent, or --record-execute-tool")


if __name__ == "__main__":
    main()
