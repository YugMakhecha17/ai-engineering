# ai-infrastructure-engineering

**From software engineering fundamentals to production-minded AI infrastructure.**

An engineering laboratory documenting the design, implementation, testing, benchmarking and
architectural reasoning behind modern software systems and AI infrastructure.

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
<!-- After publishing, add the CI badge for .github/workflows/ci.yml:
     [![CI](https://github.com/<user>/ai-infrastructure-engineering/actions/workflows/ci.yml/badge.svg)](https://github.com/<user>/ai-infrastructure-engineering/actions/workflows/ci.yml) -->

## Mission

Build, from first principles and with evidence, the software and systems foundations needed for
AI-infrastructure work (model serving, inference scheduling, ML platforms), and keep a public,
checkable record of the progress.

This is **early-stage learning work**, not a finished system and not a claim of professional
infrastructure expertise. What exists, and what does not, is stated precisely in
[project status](docs/project-status.md).

## The one rule

> **Every important technical claim is supported by an explanation, an implementation, a test, or a
> reliable reference.**

"A heap gives efficient priority scheduling" is not allowed to stand alone. Here it is backed by a
[heap scheduler](projects/01-request-scheduling-engine/), a test that equal-priority requests keep
arrival order, comparison-count tests for the O(log n) bounds, and a written list of limitations
(starvation, unbounded records, lazy-deletion memory). The rule is enforced by tooling:
[`docs/claims-register.md`](docs/claims-register.md) lists 61 claims with typed evidence pointers, and
`scripts/check_evidence.py` fails CI if a pointer is missing or wrong. Details:
[ADR 0001](docs/decisions/0001-evidence-rule.md).

## Honest representation

* Code in this repository was written with **AI assistance** and is labelled as such. It is reference
  material and **does not count as the owner's independent skill**.
* The [progress tracker](docs/progress-tracker.md) uses five statuses (Introduced → Mastered), starts
  every concept at *Introduced*, and lists the exercises still to be completed independently.
* Benchmarks are labelled **measured** or **simulated**, record their environment, and are never
  mixed. No inference benchmark exists yet.

## Areas of technical focus

Python and software-engineering fundamentals · data structures and algorithms · systems and
concurrency · backend and distributed systems · ML infrastructure · inference serving, batching,
KV cache, GPUs. Sections 01–03 hold real code; 04–07 are planned
([why](docs/decisions/0003-no-empty-directories.md)).

## Featured projects

| Project | What it demonstrates | Status |
|---------|----------------------|--------|
| [01 Request scheduling engine](projects/01-request-scheduling-engine/) | Heaps, deques, hash maps, an enforced request state machine, lazy cancellation, validation, model-based testing | Initial version implemented and verified |
| [02 Model serving API](projects/02-model-serving-api/) | A `ModelBackend` seam that a real inference engine must satisfy | Specification plus a simulated backend; no API yet |
| [03 Inference observability](projects/03-inference-observability/) | Percentile, throughput, TTFT and inter-token-latency primitives with exact arithmetic | Primitives implemented; no benchmark harness yet |

## Repository navigation

| Path | Contents |
|------|----------|
| [`01-python-foundations/`](01-python-foundations/) | Mutability, functions, exceptions, generators, context managers, packages |
| [`02-data-structures-algorithms/`](02-data-structures-algorithms/) | Dynamic array, hash map, queues, binary heap, search/sort, rate limiter, with operation-count tests |
| [`03-software-engineering/`](03-software-engineering/) | Testing and TDD, debugging, type safety, project structure, Git, review practice |
| [`04-systems-fundamentals/`](04-systems-fundamentals/) · [`06-ml-infrastructure/`](06-ml-infrastructure/) · [`07-ai-infrastructure/`](07-ai-infrastructure/) | **Planned**: topic maps and prerequisites only |
| [`05-backend-distributed-systems/`](05-backend-distributed-systems/) | One implemented example (SQL `WHERE` vs `HAVING`); the rest planned |
| [`projects/`](projects/) | The three flagship projects |
| [`benchmarks/`](benchmarks/) | Benchmark scripts, [methodology](benchmarks/methodology.md), recorded results |
| [`docs/`](docs/) | [Roadmap](docs/learning-roadmap.md), [principles](docs/engineering-principles.md), [glossary](docs/glossary.md), [progress](docs/progress-tracker.md), [status](docs/project-status.md), [claims](docs/claims-register.md), [architecture](docs/architecture/repository-architecture.md), [diagrams](docs/architecture/diagrams/), [decisions](docs/decisions/) |

## Learning and implementation roadmap

Phases are gated by reviewed evidence, not by calendar. Full version:
[learning-roadmap.md](docs/learning-roadmap.md).

0. Close the baseline: finish the unresolved exercises independently
1. Independent fundamentals: extend project 01 (batching, token budget, expiry, queue limit)
2. Systems and concurrency: races, locks, `asyncio`, profiling
3. Backend and reliability: FastAPI, PostgreSQL, Docker, timeouts and retries
4. Model serving: streaming, scheduling, admission control, a real local model where hardware allows
5. Inference optimisation: batching, KV cache, quantisation, GPU profiling, distributed inference
6. ML platform: data validation, versioning, tracking, registry, drift (parallel to 4–5)

## Engineering standards

Python ≥ 3.12 · standard-library-only runtime code · `pytest` · `ruff` (lint and format) ·
`mypy --strict` · GitHub Actions on Linux and Windows · tests include failure cases and use injected
clocks, seeded randomness and operation counts · every limitation stated next to its feature.
See [CONTRIBUTING.md](CONTRIBUTING.md) and [engineering principles](docs/engineering-principles.md).

## Setup and testing

```bash
python -m venv .venv
source .venv/bin/activate          # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"

python -m pytest                   # tests
python -m ruff check . && python -m ruff format --check .
python -m mypy 01-python-foundations 02-data-structures-algorithms 03-software-engineering \
    05-backend-distributed-systems projects scripts benchmarks
python scripts/check_evidence.py   # claims register
make check                         # all of the above, where make is available
```

Run the first project's example: `python projects/01-request-scheduling-engine/examples/basic_usage.py`

## Current progress

| Measure | Value | Verified |
|---------|-------|----------|
| Tests | 334 passing | Yes, Linux, Python 3.12.3 |
| Lint / format (`ruff`) | clean | Yes |
| Types (`mypy --strict`) | clean, 59 source files | Yes |
| Claims register | 61 claims, 55 with test evidence, 0 broken pointers, 2 reference-only | Yes |
| Mutation spot-check | 18 of 18 deliberate bugs caught by the tests | Yes (`scripts/mutation_spot_check.py`) |
| Mermaid diagrams | 14 parse with the real `mermaid` library | Yes, one-off check |
| Windows and Python 3.13 CI | configured | **Not yet run on GitHub** |

Owner's independent work reviewed so far: **none**. Every concept is at *Introduced*
([tracker](docs/progress-tracker.md)).

## Future development

Project 01 progressive features (queue limit, expiry, batching, token budget, fairness) · FastAPI layer
for project 02 · open-loop benchmark harness for project 03 · thread-safety and `asyncio` in section 04 ·
PostgreSQL transaction demonstrations in section 05 · simulators for continuous batching and KV-cache
allocation in section 07. Each lands with tests and a claims-register entry, or it does not land.

## References

Primary sources only; each topic page lists its own.
* Python documentation: <https://docs.python.org/3/> · PEPs: <https://peps.python.org/>
* PostgreSQL: <https://www.postgresql.org/docs/current/> · FastAPI: <https://fastapi.tiangolo.com/>
* PyTorch: <https://pytorch.org/docs/stable/> · Hugging Face: <https://huggingface.co/docs> ·
  NVIDIA CUDA: <https://docs.nvidia.com/cuda/> · Docker: <https://docs.docker.com/> ·
  Kubernetes: <https://kubernetes.io/docs/>
* Yu et al., *Orca*, OSDI 2022: <https://www.usenix.org/conference/osdi22/presentation/yu>
* Kwon et al., *PagedAttention*, 2023: <https://arxiv.org/abs/2309.06180>

## License

MIT, see [LICENSE](LICENSE).
