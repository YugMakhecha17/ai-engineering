"""Verify docs/claims-register.md against the repository.

The repository rule (docs/decisions/0001-evidence-rule.md):

    Every important technical claim must be supported by an explanation, an
    implementation, a test, or a reliable reference.

This script makes the rule mechanically checkable. Each row of the register is

    | C-001 | <claim> | `impl:path::Symbol`<br>`test:path::test_name`<br>`ref:https://...` |

and the script fails if

* a claim ID is duplicated or a claim has no evidence;
* an evidence kind is unknown;
* a cited local file does not exist;
* a cited ``::symbol`` is not defined (``def``/``class`` in Python, a heading in Markdown);
* a ``test:`` citation does not point to a ``test_*.py`` file and a ``test_*`` function.

Claims backed *only* by prose (``doc:``) or *only* by an external reference are
reported as warnings: they are allowed by the rule, but an interviewer will
probe them, so they are listed for follow-up.

Usage:  python scripts/check_evidence.py [--root PATH] [--register PATH]
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

EVIDENCE_PATTERN = re.compile(r"`([a-z]+):([^`]+)`")
VALID_KINDS = {"test", "impl", "doc", "ref"}
ROW_PATTERN = re.compile(r"^\|\s*(C-\d{3})\s*\|")


@dataclass(frozen=True)
class Evidence:
    kind: str
    target: str


@dataclass
class Claim:
    claim_id: str
    text: str
    evidence: list[Evidence] = field(default_factory=list)


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    total: int = 0
    with_tests: int = 0
    with_impl: int = 0


def parse_register(text: str) -> list[Claim]:
    """Parse claim rows from the register's Markdown tables."""
    claims: list[Claim] = []
    for line in text.splitlines():
        match = ROW_PATTERN.match(line)
        if not match:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3:
            claims.append(Claim(match.group(1), cells[1] if len(cells) > 1 else ""))
            continue
        evidence = [Evidence(k, t.strip()) for k, t in EVIDENCE_PATTERN.findall(cells[2])]
        claims.append(Claim(cells[0], cells[1], evidence))
    return claims


def _symbol_defined(path: Path, symbol: str) -> bool:
    """True if `symbol` (last dotted component) is defined in `path`."""
    name = symbol.split(".")[-1]
    content = path.read_text(encoding="utf-8")
    if path.suffix == ".py":
        return (
            re.search(rf"^\s*(?:async\s+def|def|class)\s+{re.escape(name)}\b", content, re.M)
            is not None
        )
    if path.suffix == ".md":
        return re.search(rf"^#+\s.*{re.escape(symbol)}", content, re.M) is not None
    return symbol in content


def _check_local(ev: Evidence, root: Path, claim_id: str, report: Report) -> None:
    rel, _, symbol = ev.target.partition("::")
    path = root / rel
    if not path.is_file():
        report.errors.append(f"{claim_id}: {ev.kind}: file not found: {rel}")
        return
    if ev.kind == "test":
        if not path.name.startswith("test_") or path.suffix != ".py":
            report.errors.append(f"{claim_id}: test evidence must be a test_*.py file: {rel}")
        if not symbol.split(".")[-1].startswith("test_"):
            report.errors.append(
                f"{claim_id}: test evidence must name a test_* function: {ev.target}"
            )
    if symbol and not _symbol_defined(path, symbol):
        report.errors.append(f"{claim_id}: {ev.kind}: '{symbol}' not defined in {rel}")


def check_claims(claims: list[Claim], root: Path) -> Report:
    report = Report(total=len(claims))
    seen: set[str] = set()
    for claim in claims:
        if claim.claim_id in seen:
            report.errors.append(f"{claim.claim_id}: duplicate claim ID")
        seen.add(claim.claim_id)
        if not claim.text:
            report.errors.append(f"{claim.claim_id}: empty claim text")
        if not claim.evidence:
            report.errors.append(f"{claim.claim_id}: no evidence given")
            continue
        for ev in claim.evidence:
            if ev.kind not in VALID_KINDS:
                report.errors.append(f"{claim.claim_id}: unknown evidence kind '{ev.kind}'")
            elif ev.kind == "ref":
                if not ev.target.startswith("https://"):
                    report.errors.append(f"{claim.claim_id}: ref must be an https URL: {ev.target}")
            else:
                _check_local(ev, root, claim.claim_id, report)
        kinds = {e.kind for e in claim.evidence}
        report.with_tests += "test" in kinds
        report.with_impl += "impl" in kinds
        if not kinds & {"test", "impl"}:
            report.warnings.append(
                f"{claim.claim_id}: explanation/reference only (no implementation or test)"
            )
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--register", type=Path, default=None)
    args = parser.parse_args(argv)
    register = args.register or args.root / "docs" / "claims-register.md"
    if not register.is_file():
        print(f"error: register not found: {register}", file=sys.stderr)
        return 2
    claims = parse_register(register.read_text(encoding="utf-8"))
    report = check_claims(claims, args.root)
    for message in report.errors:
        print(f"ERROR   {message}")
    for message in report.warnings:
        print(f"WARNING {message}")
    print(
        f"{report.total} claims | {report.with_tests} with test evidence | "
        f"{report.with_impl} with implementation | {len(report.warnings)} weak | "
        f"{len(report.errors)} errors"
    )
    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main())
