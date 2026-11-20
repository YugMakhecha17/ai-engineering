# ADR 0002: Stdlib-only runtime code; pytest, ruff, mypy for development

**Status:** Accepted

**Context.** The goal is to understand mechanisms, not to wrap frameworks. Dependencies hide the
mechanism and add install friction on Windows and Linux.

**Decision.** All study modules and project code depend only on the Python standard library.
Development uses `pytest` (tests), `ruff` (lint and format) and `mypy --strict` (types), declared
in `pyproject.toml` under the `dev` extra. Python ≥ 3.12. FastAPI and Pydantic are introduced
only when project 02 reaches its API stage. C++ or Go are introduced only when a measured
bottleneck justifies them.

**Consequences.** Standard-library `heapq`, `deque` and `sqlite3` are used where the lesson is
about *using* them; hand-written versions exist where the lesson is how they work.
