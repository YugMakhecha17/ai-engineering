# 03 · Software engineering

Habits that make code trustworthy: tests that can fail, a method for debugging, types a tool
checks, a project layout that scales, and disciplined Git.

| Topic | Contents | Evidence |
|-------|----------|----------|
| [Testing](testing/) | Strategy, TDD worked example, test patterns | `duration_parser.py` + tests |
| [Debugging](debugging/) | A repeatable method, `pdb`, logging, regression tests | `moving_average.py` + tests |
| [Type safety](type-safety/) | Hints, `Protocol`, generics, `mypy --strict` | `typed_predictors.py` + tests |
| [Project structure](project-structure/) | Layouts, imports, tooling config | This repository, documented |
| [Git workflows](git-workflows/) | Commit hygiene, branching, review | Documented practice |
| [Engineering principles](engineering-principles/) | Clean code, cohesion/coupling, error handling, logging, code review, with examples from this repo | Cited code |

Run the executable parts: `python -m pytest 03-software-engineering`
(includes one `slow` test that invokes `mypy`; deselect with `-m "not slow"`).

**Provenance.** Reference implementations are AI-assisted and raise no status in the
[progress tracker](../docs/progress-tracker.md). Exercise E-08 (write tests *before* reading existing
ones) belongs here.
