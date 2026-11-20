# Diagrams

Each diagram states whether it describes something **implemented** in this repository or a design
that is **planned**. Planned diagrams are design intent and carry no evidence of working code.

| Diagram | Subject | Status |
|---------|---------|--------|
| [request-lifecycle.md](request-lifecycle.md) | Request states and dispatch with lazy cancellation | Implemented (project 01) |
| [scheduling.md](scheduling.md) | FIFO and priority scheduling data flow | Implemented (project 01) |
| [resource-lifecycle.md](resource-lifecycle.md) | Context-manager resource lifecycle | Implemented (01 context managers) |
| [model-serving-and-inference-flow.md](model-serving-and-inference-flow.md) | Serving architecture, prefill/decode flow | Planned (project 02, section 07) |
| [ml-lifecycle-and-distributed-inference.md](ml-lifecycle-and-distributed-inference.md) | Training/deployment lifecycle, distributed inference | Planned (sections 06, 07) |

Repository-level diagrams live in [../repository-architecture.md](../repository-architecture.md).
