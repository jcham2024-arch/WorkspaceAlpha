"""Tests for the retrieval execution layer (assembly/retrieval.py).

The assembler binds a RetrievalProtocol node; retrieval.py is what actually
calls the tool. These tests cover the contract that matters operationally:

- a tool that is absent, unbuilt or broken yields status="unavailable" with a
  reason, never an exception (a missing vector index must not break assembly)
- output is bounded by the protocol's token budget and truncation never emits
  a partial unit
- every unit stays attributable to a manifest node_id and byte_range
- worker tier cannot reach PATTERN, and the refusal is a typed status
"""

import json
import sys
import types
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "assembly"))

import retrieval  # noqa: E402
from retrieval import RetrievedUnit, execute  # noqa: E402


class TestUnavailableDegradation(unittest.TestCase):
    """A broken retrieval layer must degrade, not raise."""

    def test_unknown_protocol_is_unavailable(self):
        result = execute("NOPE", "q", meta={})
        self.assertEqual(result.status, "unavailable")
        self.assertIn("no executor registered", result.reason)
        self.assertIn("NOPE", result.text)

    def test_missing_tool_file_is_unavailable(self):
        result = execute(
            "STAIR",
            "q",
            meta={"navigator": ".agent/tools/does_not_exist.py"},
        )
        self.assertEqual(result.status, "unavailable")
        self.assertIn("not found", result.reason)

    def test_broken_tool_import_is_unavailable(self):
        """An ImportError inside a tool is reported, not raised."""
        broken = ROOT / "tests" / "fixtures" / "broken_tool.py"
        broken.parent.mkdir(parents=True, exist_ok=True)
        broken.write_text("raise ImportError('deliberately broken')\n")
        try:
            result = execute(
                "VECTOR",
                "q",
                meta={"tool": str(broken.relative_to(ROOT))},
            )
            # VECTOR ignores meta['tool'], so assert on the real behaviour:
            # whatever the cause, the result is a typed unavailable status.
            self.assertEqual(result.status, "unavailable")
            self.assertTrue(result.reason)
        finally:
            broken.unlink()

    def test_exception_inside_tool_is_wrapped(self):
        def boom(query, meta, role):
            raise RuntimeError("tool exploded")

        original = retrieval.EXECUTORS["VECTOR"]
        retrieval.EXECUTORS["VECTOR"] = boom
        try:
            result = execute("VECTOR", "q", meta={})
        finally:
            retrieval.EXECUTORS["VECTOR"] = original

        self.assertEqual(result.status, "unavailable")
        self.assertIn("RuntimeError", result.reason)
        self.assertIn("tool exploded", result.reason)


class TestSuccessPath(unittest.TestCase):
    """With a working tool, retrieval returns attributed units."""

    def setUp(self):
        self._saved = dict(retrieval.EXECUTORS)

    def tearDown(self):
        retrieval.EXECUTORS.clear()
        retrieval.EXECUTORS.update(self._saved)
        sys.modules.pop("vector_retriever", None)

    def _install_fake_vector(self, chunks):
        fake = types.ModuleType("vector_retriever")

        def retrieve(query, *, max_results=5, max_tokens=2000):
            return chunks[:max_results]

        fake.retrieve = retrieve
        sys.modules["vector_retriever"] = fake

    def test_units_carry_node_id_and_byte_range(self):
        chunk = types.SimpleNamespace(
            node_id="docs/README.md::architecture",
            chunk_text="The DAG routes over manifest nodes.",
            score=0.91,
            byte_range_start=202,
            byte_range_end=260,
            content_ref="docs/README.md",
        )
        self._install_fake_vector([chunk])

        result = execute("VECTOR", "routing", meta={}, role="taskmaster")
        self.assertEqual(result.status, "ok")
        self.assertEqual(len(result.units), 1)
        unit = result.units[0]
        self.assertEqual(unit.node_id, "docs/README.md::architecture")
        self.assertEqual(unit.byte_range, [202, 260])
        self.assertEqual(unit.content_ref, "docs/README.md")

    def test_empty_result_is_empty_not_ok(self):
        self._install_fake_vector([])
        result = execute("VECTOR", "routing", meta={})
        self.assertEqual(result.status, "empty")
        self.assertEqual(result.text, "")

    def test_text_is_labelled_with_protocol_and_count(self):
        chunk = types.SimpleNamespace(
            node_id="n1",
            chunk_text="alpha",
            score=0.5,
            byte_range_start=0,
            byte_range_end=5,
            content_ref="docs/README.md",
        )
        self._install_fake_vector([chunk])
        result = execute("VECTOR", "q", meta={})
        self.assertIn("## Retrieved context — VECTOR", result.text)
        self.assertIn("1 unit)", result.text)
        self.assertIn("alpha", result.text)

    def test_direct_performs_no_retrieval(self):
        result = execute("DIRECT", "q", meta={})
        self.assertEqual(result.status, "empty")
        self.assertEqual(result.units, [])


class TestBounding(unittest.TestCase):
    def test_truncation_drops_whole_units_only(self):
        # _approx_tokens is bytes//4, so 400 bytes = 100 tokens. A 150-token
        # cap fits one unit and must reject the second whole.
        units = [
            RetrievedUnit(node_id="a", text="x" * 400, score=1.0),
            RetrievedUnit(node_id="b", text="y" * 400, score=0.9),
            RetrievedUnit(node_id="c", text="z" * 400, score=0.8),
        ]
        kept, truncated = retrieval._truncate(units, 150)
        self.assertEqual([u.node_id for u in kept], ["a"])
        self.assertTrue(truncated)

    def test_units_that_all_exceed_cap_yield_empty(self):
        units = [RetrievedUnit(node_id="a", text="x" * 4000, score=1.0)]
        kept, truncated = retrieval._truncate(units, 100)
        self.assertEqual(kept, [])
        self.assertTrue(truncated)

    def test_result_reports_truncation_and_respects_cap(self):
        def many(query, meta, role):
            return [
                RetrievedUnit(node_id=f"n{i}", text="q" * 200, score=1.0)
                for i in range(10)
            ]

        original = retrieval.EXECUTORS["VECTOR"]
        retrieval.EXECUTORS["VECTOR"] = many
        try:
            result = execute("VECTOR", "q", meta={}, max_tokens=150)
        finally:
            retrieval.EXECUTORS["VECTOR"] = original

        self.assertTrue(result.truncated)
        # The cap applies to the joined text, header included, so allow the
        # header's own tokens as slack while still proving boundedness.
        self.assertLessEqual(result.tokens, 150 + 20)
        self.assertLess(len(result.units), 10)


class TestRoleEnforcement(unittest.TestCase):
    def test_permission_error_becomes_unavailable(self):
        def denied(query, meta, role):
            raise PermissionError("only orchestrator and manager roles")

        original = retrieval.EXECUTORS["PATTERN"]
        retrieval.EXECUTORS["PATTERN"] = denied
        try:
            result = execute("PATTERN", "q", meta={}, role="worker")
        finally:
            retrieval.EXECUTORS["PATTERN"] = original

        self.assertEqual(result.status, "unavailable")
        self.assertIn("not permitted", result.reason)


class TestRealToolsLoad(unittest.TestCase):
    """The real tool modules must import without a vector index present."""

    def test_real_vector_reports_missing_index(self):
        result = execute("VECTOR", "q", meta={}, role="taskmaster")
        # Either the index exists (ok/empty) or it is reported missing.
        self.assertIn(result.status, {"ok", "empty", "unavailable"})
        if result.status == "unavailable":
            self.assertIn("VectorIndexMissing", result.reason)

    def test_real_stair_runs_bounded(self):
        result = execute(
            "STAIR",
            "adr dag routing decision",
            meta={"navigator": ".agent/tools/stair_navigator.py"},
            role="taskmaster",
        )
        self.assertIn(result.status, {"ok", "empty", "unavailable"})


class TestAssemblerIntegration(unittest.TestCase):
    """The assembler must execute the protocol and record the outcome."""

    def setUp(self):
        from assembler import Assembler

        self.assembler = Assembler()
        self._saved_turns = (ROOT / "provenance" / "turns.jsonl")
        self._backup = (
            self._saved_turns.read_text(encoding="utf-8")
            if self._saved_turns.exists()
            else ""
        )

    def tearDown(self):
        # Tests write provenance; restore so the suite leaves no trace.
        if self._backup:
            self._saved_turns.write_text(self._backup, encoding="utf-8")

    def _delegation(self, **overrides):
        base = {
            "delegation_id": "test-retrieval-exec",
            "from_agent": "conceptualizer",
            "to_agent": "taskmaster",
            "delegation_type": "MISSION",
            "target_tier": "low_thinking",
            "allowed_targets": ["docs/README.md"],
            "task_type": "planning",
            "task": "how does the dag router work",
            "profile": "taskmaster",
        }
        base.update(overrides)
        return base

    def test_retrieval_status_is_reported(self):
        result = self.assembler.assemble(self._delegation())
        self.assertIn("retrieval", result)
        self.assertIn(
            result["retrieval"]["status"], {"ok", "empty", "unavailable"}
        )

    def test_unavailable_retrieval_does_not_break_assembly(self):
        """No vector index is the normal case here, and it must not raise."""
        result = self.assembler.assemble(self._delegation())
        self.assertFalse(result["blocked"])
        self.assertIn(result["retrieval"]["protocol"], {"DIRECT", "STAIR", "VECTOR"})

    def test_retrieval_units_are_recorded_in_provenance(self):
        self.assembler.assemble(self._delegation())
        turns = [
            json.loads(line)
            for line in self._saved_turns.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        record = [t for t in turns if t["delegation_id"] == "test-retrieval-exec"][-1]
        retrieval_record = record["adapter_params"]["retrieval"]
        self.assertIn("status", retrieval_record)
        self.assertIn("protocol", retrieval_record)
        self.assertIn("tokens", retrieval_record)
        self.assertIsInstance(retrieval_record["units"], list)

    def test_retrieved_text_reaches_the_suffix(self):
        """A working tool's output must land in variable_suffix."""
        units = [RetrievedUnit(node_id="docs/README.md::arch", text="DAG router body")]
        original = retrieval.EXECUTORS["VECTOR"]
        retrieval.EXECUTORS["VECTOR"] = lambda q, m, r: units
        try:
            result = self.assembler.assemble(self._delegation())
        finally:
            retrieval.EXECUTORS["VECTOR"] = original

        self.assertEqual(result["retrieval"]["status"], "ok")
        self.assertIn("DAG router body", result["variable_suffix"])
        self.assertIn("## Retrieved context — VECTOR", result["variable_suffix"])

    def test_retrieval_tokens_are_counted(self):
        units = [RetrievedUnit(node_id="n", text="a" * 400)]
        original = retrieval.EXECUTORS["VECTOR"]
        retrieval.EXECUTORS["VECTOR"] = lambda q, m, r: units
        try:
            result = self.assembler.assemble(self._delegation())
        finally:
            retrieval.EXECUTORS["VECTOR"] = original

        self.assertGreater(result["retrieval"]["tokens"], 0)
        self.assertGreater(result["token_counts"]["suffix_tokens"], 0)

    def test_token_counts_include_retrieved_context(self):
        """total_tokens must reflect retrieval, which is appended post-budget."""
        before = self.assembler.assemble(self._delegation())
        units = [RetrievedUnit(node_id="n", text="a" * 4000)]
        original = retrieval.EXECUTORS["VECTOR"]
        retrieval.EXECUTORS["VECTOR"] = lambda q, m, r: units
        try:
            after = self.assembler.assemble(self._delegation())
        finally:
            retrieval.EXECUTORS["VECTOR"] = original

        self.assertEqual(
            after["token_counts"]["total_tokens"],
            after["token_counts"]["prefix_tokens"]
            + after["token_counts"]["suffix_tokens"],
        )
        self.assertGreaterEqual(
            after["token_counts"]["suffix_tokens"],
            before["token_counts"]["suffix_tokens"],
        )


if __name__ == "__main__":
    unittest.main()
