# Project structure

Status: documented practice. The evidence is this repository's own layout, which CI exercises
(imports, test discovery, lint and type checks on Linux and Windows).

## 1. Problem
Where do code, tests, configuration and docs go so that a newcomer, a test runner and a build tool all
find them?

## 2. First-principles explanation
A layout is a contract between humans and tools. Tools need to import code and discover tests; humans
need to know where to look.

## 3. Technical details: what this repository does
* `src/<package>/` for each project: tests import the installed/`pythonpath` package, never a file
  relative to the working directory, which catches packaging mistakes.
* Tests beside the code in study modules (small, one concept per directory) and in `tests/` for projects.
* One `pyproject.toml` configures pytest, ruff and mypy; no setup.py, no tool-specific dotfiles.
* Unique module names across the repository (pytest without `__init__.py` shares one namespace).
  Avoid names that shadow the standard library (`queue.py`, `copy.py`).
* `Makefile` wraps the exact commands CI runs; CONTRIBUTING lists them for Windows without `make`.
* Dependencies: runtime code is standard-library only
  ([ADR 0002](../../docs/decisions/0002-minimal-toolchain.md)).

## 4. Runnable implementation
Run `make check` (or the commands in [CONTRIBUTING.md](../../CONTRIBUTING.md)) from the repository root.

## 5. Expected behaviour
Lint clean, type check clean, evidence register valid, all tests pass.

## 6. Tests
CI matrix: Ubuntu and Windows × Python 3.12 and 3.13 (see `.github/workflows/ci.yml`; the matrix has
not yet run on GitHub, only the Linux/3.12 sandbox run is verified).

## 7. Engineering trade-offs
`src` layout needs installation or a `pythonpath` setting but prevents accidental imports from the
working directory; a flat layout is simpler for scripts. Monorepo (this repository) shares tooling but
couples release cycles.

## 8. AI-infrastructure connection
Serving systems ship as containers built from a package; a clean entry point (`python -m pkg`) and
pinned configuration make builds reproducible.

## 9. Common mistakes
Tests that only pass from one working directory; circular imports; configuration scattered over many
files; committing virtual environments or caches.

## 10. References
* Python Packaging User Guide, `src` layout vs flat layout:
  <https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/>
* `pyproject.toml` specification: <https://packaging.python.org/en/latest/specifications/pyproject-toml/>
