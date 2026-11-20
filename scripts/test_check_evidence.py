"""Tests for the evidence checker: the rule-enforcement tool must itself be trustworthy."""

from pathlib import Path

import check_evidence as ce


def _repo(tmp_path: Path) -> Path:
    (tmp_path / "pkg").mkdir()
    (tmp_path / "pkg" / "impl.py").write_text("class Heap:\n    def push(self):\n        pass\n")
    (tmp_path / "pkg" / "test_impl.py").write_text("def test_push():\n    assert True\n")
    (tmp_path / "pkg" / "notes.md").write_text("# Heap trade-offs\n")
    return tmp_path


def _run(tmp_path: Path, rows: str) -> ce.Report:
    return ce.check_claims(ce.parse_register(rows), _repo(tmp_path))


def test_valid_claim_with_test_and_impl_passes(tmp_path: Path) -> None:
    row = (
        "| C-001 | Push works | "
        "`impl:pkg/impl.py::Heap.push`<br>`test:pkg/test_impl.py::test_push` |"
    )
    report = _run(tmp_path, row)
    assert report.errors == []
    assert report.with_tests == 1
    assert report.with_impl == 1
    assert report.warnings == []


def test_claim_without_evidence_is_an_error(tmp_path: Path) -> None:
    report = _run(tmp_path, "| C-001 | Heaps are fast |  |")
    assert any("no evidence" in e for e in report.errors)


def test_missing_file_is_an_error(tmp_path: Path) -> None:
    report = _run(tmp_path, "| C-001 | x | `impl:pkg/ghost.py::Heap` |")
    assert any("file not found" in e for e in report.errors)


def test_missing_symbol_is_an_error(tmp_path: Path) -> None:
    report = _run(tmp_path, "| C-001 | x | `impl:pkg/impl.py::Queue` |")
    assert any("'Queue' not defined" in e for e in report.errors)


def test_test_evidence_must_name_a_test_function(tmp_path: Path) -> None:
    report = _run(tmp_path, "| C-001 | x | `test:pkg/test_impl.py` |")
    assert any("must name a test_* function" in e for e in report.errors)


def test_test_evidence_must_be_in_a_test_file(tmp_path: Path) -> None:
    report = _run(tmp_path, "| C-001 | x | `test:pkg/impl.py::test_push` |")
    assert any("must be a test_*.py file" in e for e in report.errors)


def test_duplicate_ids_are_rejected(tmp_path: Path) -> None:
    rows = "| C-001 | a | `doc:pkg/notes.md` |\n| C-001 | b | `doc:pkg/notes.md` |"
    assert any("duplicate" in e for e in _run(tmp_path, rows).errors)


def test_unknown_kind_and_non_https_ref_are_errors(tmp_path: Path) -> None:
    report = _run(tmp_path, "| C-001 | a | `magic:foo` |\n| C-002 | b | `ref:http://x.org` |")
    assert any("unknown evidence kind" in e for e in report.errors)
    assert any("https URL" in e for e in report.errors)


def test_prose_only_claim_is_a_warning_not_an_error(tmp_path: Path) -> None:
    report = _run(tmp_path, "| C-001 | a | `doc:pkg/notes.md::Heap trade-offs` |")
    assert report.errors == []
    assert len(report.warnings) == 1


def test_non_claim_lines_are_ignored() -> None:
    text = "# Title\n\n| ID | Claim | Evidence |\n|----|-------|----------|\nprose C-001\n"
    assert ce.parse_register(text) == []
