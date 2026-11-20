# Contributing

This is a personal engineering laboratory, but it is run like an open-source project so the history
and the review habits are real. These rules apply to the owner's own changes as much as to anyone else's.

## The one rule

> **Every important technical claim must be supported by an explanation, an implementation, a test,
> or a reliable reference.**

Do not write "a heap gives efficient priority scheduling" and stop. Implement the scheduler, test
equal-priority requests, analyse the complexity, state the limitations. Details and the table of
adequate evidence: [ADR 0001](docs/decisions/0001-evidence-rule.md).

When you add or change a claim:

1. Add or update a row in [docs/claims-register.md](docs/claims-register.md) with the next free ID.
2. Put the evidence in the **same commit**: the test, the implementation, the result file or the citation.
3. Run `python scripts/check_evidence.py`. It must report 0 errors.
4. Performance claims need a result file whose `data_kind` is `measured` or `simulated` and whose
   environment is recorded ([methodology](benchmarks/methodology.md)). Never invent a number.
5. Reference only primary sources and verify the URL exists. Never invent a paper, URL, API or option.

## Honest progress and provenance
* Files written with AI assistance carry a `Provenance:` line in the module docstring.
* A reference implementation never changes a status in [docs/progress-tracker.md](docs/progress-tracker.md).
  Independent work goes in `<topic>/exercises/` with its own tests and is reviewed first
  ([ADR 0004](docs/decisions/0004-provenance-and-honest-progress.md)).
* Do not describe planned work as implemented. Use these four labels exactly:
  **Implemented and verified**, **Implemented but not verified**, **Documented only**, **Planned**.

## Setup
Python 3.12 or newer.

```bash
python -m venv .venv
# Linux/macOS:  source .venv/bin/activate
# Windows (PowerShell):  .venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

## Commands
With `make` (Linux/macOS, or Windows with GNU Make):

| Command | Runs |
|---------|------|
| `make check` | everything CI runs |
| `make test` | `python -m pytest` |
| `make lint` | `ruff check` and `ruff format --check` |
| `make format` | apply ruff fixes and formatting |
| `make typecheck` | `mypy --strict` over the source trees |
| `make evidence` | `python scripts/check_evidence.py` |

Without `make` (identical commands; works on Windows):

```bash
python -m ruff check .
python -m ruff format --check .
python -m mypy 01-python-foundations 02-data-structures-algorithms 03-software-engineering 05-backend-distributed-systems projects scripts benchmarks
python scripts/check_evidence.py
python -m pytest
```
Optional, slower: `python scripts/mutation_spot_check.py` checks that key tests can actually fail.

Skip the one slow test (it runs `mypy` in a subprocess): `python -m pytest -m "not slow"`.

## Project-level testing strategy
* `pytest`; tests live beside study modules and in `tests/` for projects.
* Every unit has normal, edge and failure cases. A test must be able to fail.
* Deterministic by construction: injected clocks, sleeps and ID factories; seeded randomness; no
  network; no real sleeping.
* Complexity claims are asserted with operation counts, not stopwatches. Benchmarks report time and
  are never asserted in tests.
* Model-based tests (compare with a slow, obviously correct reference) for stateful components.
* Module file names are unique across the repository (see
  [repository architecture](docs/architecture/repository-architecture.md)); avoid standard-library names.

## Documentation
Concept pages use the ten headings in [engineering principles](docs/engineering-principles.md#9-documentation-template).
Use relative links, language-tagged code blocks, and Mermaid only when it explains a real relationship.
State what a diagram describes (implemented or planned).

## Commits and pull requests
Small, single-purpose commits; imperative subject ≤ 72 characters; body explains *why*. A PR is ready
when CI is green and the review checklist in
[engineering-principles](03-software-engineering/engineering-principles/README.md#code-review-checklist) is satisfied.

## Dependencies
Runtime code is standard-library only ([ADR 0002](docs/decisions/0002-minimal-toolchain.md)). Adding a
dependency requires a stated need and a new ADR.
