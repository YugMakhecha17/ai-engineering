# Project 02 · Model serving API

**Status: specification, plus one implemented seam.** Implemented and tested: the `ModelBackend`
protocol and a deterministic `SimulatedBackend` (`src/model_serving/backend.py`, 6 tests). **Not
implemented:** the API, FastAPI/Pydantic layer, scheduling integration, streaming over HTTP,
batching, timeouts, health checks, metrics, any real model.

`SimulatedBackend` is not a model. Its output is meaningless; timing involving it is simulated.

## Purpose
Show how an inference request enters a service, is validated, scheduled and executed, and how results
stream back, with a clean boundary so that the simulated backend can be replaced by a real inference
engine.

## Target architecture (design intent)
See [serving and inference flow](../../docs/architecture/diagrams/model-serving-and-inference-flow.md).

```text
client -> API (validate) -> admission control -> scheduler (project 01) -> batcher -> ModelBackend -> token stream
```

## The seam that exists today
```python
class ModelBackend(Protocol):
    name: str

    def generate(self, prompt: str, max_tokens: int) -> Iterator[str]: ...
```
A real engine (a local Hugging Face model, `llama.cpp` bindings, a remote server) must implement
exactly this. Everything above it depends only on the protocol. Evidence:
`test_simulated_backend_satisfies_the_protocol_that_real_engines_must_implement` (checked by `mypy`),
`test_generation_is_a_lazy_stream`.

## Staged roadmap
| Stage | Deliverable | Entry condition | Evidence when done |
|-------|-------------|-----------------|--------------------|
| 0 | `ModelBackend` + `SimulatedBackend` | none | **Done** |
| 1 | Request/response models and validation (stdlib dataclasses first, then Pydantic) | roadmap phase 3 | Tests for each invalid field; structured error bodies |
| 2 | Synchronous `POST /generate` with FastAPI; `GET /health` | Stage 1 | `TestClient` tests; error contract documented |
| 3 | Scheduler integration (project 01) and request IDs in logs | Stage 2 | Priority honoured end-to-end; cancellation test |
| 4 | Async endpoints, streaming output, timeouts, concurrency limit | phase 2 concurrency done | Timeout and overload tests with an injected slow backend |
| 5 | Metrics endpoint wired to project 03 | project 03 harness exists | Counters match known synthetic traffic |
| 6 | Model selection; local real model where hardware permits | Stage 4 | Real-vs-simulated results labelled separately |

No paid cloud service is required at any stage.

## Draft error contract (not implemented)
| Condition | HTTP status | Body `error.code` |
|-----------|-------------|-------------------|
| Malformed or out-of-range field | 422 | `validation_error` |
| Queue full / rate limited | 429 | `overloaded` |
| Backend timeout | 504 | `backend_timeout` |
| Unknown model | 404 | `unknown_model` |
| Unexpected failure | 500 | `internal_error` (no internals leaked) |

## Test plan
Validation matrix; lifecycle state transitions via the scheduler; failure injection (backend raises,
backend is slow, client disconnects mid-stream); concurrency limit respected under parallel requests;
documented examples executed in CI, as with project 01.

Design notes: [docs/design.md](docs/design.md).
