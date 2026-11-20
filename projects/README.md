# Projects

Three flagship projects, built in order, each depending on the previous one's ideas. Status is stated
exactly; nothing is described as working unless a test shows it.

| # | Project | Purpose | Status |
|---|---------|---------|--------|
| 01 | [Request scheduling engine](01-request-scheduling-engine/) | Queues, heaps, state machines, resource management | **Initial version implemented and tested** (FIFO + priority, lifecycle, cancellation, validation). Batching, token budgets, expiry, queue limits: planned |
| 02 | [Model serving API](02-model-serving-api/) | How inference requests enter and move through a service | **Specification + `ModelBackend` seam with a simulated backend.** No API, no real model |
| 03 | [Inference observability](03-inference-observability/) | Measure latency, throughput and trade-offs | **Metric primitives implemented and tested.** No benchmark harness over a serving system yet |

## Shared rules
* Evidence rule: every important claim has evidence ([ADR 0001](../docs/decisions/0001-evidence-rule.md)).
* Simulated and measured data are never mixed or presented as one another
  ([methodology](../benchmarks/methodology.md)).
* Runtime code is standard-library only until a stated need appears
  ([ADR 0002](../docs/decisions/0002-minimal-toolchain.md)).
* Source is AI-assisted reference material and does not raise any status in the
  [progress tracker](../docs/progress-tracker.md); the owner's extensions are added and labelled separately.
