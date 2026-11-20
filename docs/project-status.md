# Project status

Four labels are used, exactly: **Implemented and verified**, **Implemented but not verified**,
**Documented only**, **Planned**. "Verified" means the check was actually run; where it was run is
stated. Last verification: 2026-11-20, Linux x86-64, Python 3.12.3, 1-CPU sandbox, local (not GitHub).

## Implemented and verified

| Item | Evidence |
|------|----------|
| Section 01: mutability, functions, exceptions, iterators/generators, context managers, modules/packages | 76 tests passing |
| Section 02: dynamic array, hash structures, FIFO queues, binary heap, search/sort, rate limiter | 85 tests, including operation-count bounds |
| Section 03: duration parser (TDD), moving average (debugging), typed predictors | 43 tests, including one that runs `mypy` |
| Section 05: SQL `WHERE`/`GROUP BY`/`HAVING` worked example (SQLite) | 5 tests |
| Project 01: FIFO and priority schedulers, lifecycle, lazy cancellation, validation, example | 92 tests incl. model-based comparison against a brute-force reference |
| Project 02: `ModelBackend` protocol, `SimulatedBackend` | 6 tests |
| Project 03: percentile, summary, throughput, TTFT, inter-token latency | 19 tests incl. exactness over ~20,000 (p, n) pairs |
| Evidence tooling: `check_evidence.py` | 10 tests; run against the real register (61 claims, 0 errors) |
| Quality gates | `ruff` clean · `mypy --strict` clean on 59 files · 334 tests pass · 18/18 mutants killed |
| Benchmarks: queue draining, scheduler throughput | Result files with environment recorded; **measured**, single-CPU shared VM, not portable |
| 14 Mermaid diagrams | Parsed with `mermaid` 11 under Node 22 (negative control confirmed the parser rejects bad syntax). Parse validity only; rendering was not inspected |
| 178 relative Markdown links and anchors | One-off script, all resolve |
| Clean-room run: fresh copy, new venv, `pip install -e ".[dev]"`, then `make check` | Exit code 0 on Linux/Python 3.12.3: ruff lint and format, `mypy --strict`, evidence register, 334 tests |

## Implemented but not verified

| Item | What is unverified |
|------|--------------------|
| GitHub Actions workflow (`.github/workflows/ci.yml`) | Never executed on GitHub. Commands were run locally. The Windows and Python 3.13 legs have never run. `actions/checkout@v6` and `actions/setup-python@v6` were checked against public sources, not run |
| Windows compatibility generally | Code uses `pathlib`, `sys.executable` and no POSIX-only calls, but nothing was executed on Windows |
| SQL examples against PostgreSQL | Verified on SQLite only |
| `make` on Windows, and the mutation script on Windows | Not run (`make check` was verified on Linux only) |

## Documented only

Section 04 to 07 topic maps and prerequisites · Project 02 staged roadmap, draft error contract and
open design questions · Project 03 metric plan, benchmark plan and draft result schema · ADRs 0001–0004 ·
learning roadmap.

## Planned (no implementation)

Everything in sections 04, 06 and 07; sections of 05 other than the SQL example; Project 01 progressive
features (queue limit, expiry, batching, token budget, fairness); Project 02 API, streaming, scheduling
integration, real model; Project 03 load generator, plots, any inference benchmark. Diagrams for
serving, ML lifecycle and distributed inference are **design intent**, not architecture that exists.

## Known limitations of what exists

* Project 01 is single-process, not thread-safe, keeps every request record forever, can starve
  low-priority work, and has no backpressure.
* The two benchmarks cover few input sizes on one noisy machine; they are consistent with, not proof
  of, the stated growth rates. The operation-count tests are the proof.
* The evidence checker confirms that evidence **exists**, not that it is **sufficient**, and does not
  check that `ref:` URLs are reachable.
* The two paper claims rest on references only (weakest evidence class).
* All reference implementations are AI-assisted; none is the owner's independent work.
