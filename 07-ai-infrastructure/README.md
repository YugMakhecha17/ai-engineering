# 07 · AI infrastructure

**Status: planned. No code, tests or benchmarks exist in this section.** This is the primary
specialisation; it is built last because every topic depends on the earlier ones
([ADR 0003](../docs/decisions/0003-no-empty-directories.md)).

## How the foundations connect (already built vs still needed)

| AI-infra concept | Foundation it rests on | Built in this repo? |
|------------------|------------------------|---------------------|
| Request routing and scheduling | Queues, heaps, state machines | Yes: [project 01](../projects/01-request-scheduling-engine/) (single process) |
| Admission control, rate limiting | Bounded queues, sliding window | Partly: [`sliding_window.py`](../02-data-structures-algorithms/problem-solving/) |
| Token streaming | Generators | Yes: generator pattern; [`ModelBackend`](../projects/02-model-serving-api/) interface |
| Latency/throughput measurement | Percentiles, counters | Yes: [project 03](../projects/03-inference-observability/) primitives |
| Dynamic / continuous batching | Scheduling, concurrency | No |
| KV cache and its memory management | Allocators, paging | No |
| Quantisation, FP16/BF16/FP32 | Numerical precision | No |
| GPU profiling | Profilers, memory hierarchy | No |
| Tensor / pipeline parallelism, distributed inference | Networking, distributed systems | No |
| Model gateways, autoscaling, cost analysis | APIs, observability | No |

## Topic map and first planned implementations

| Topic | First planned implementation |
|-------|------------------------------|
| inference-serving | Project 02 request lifecycle with a simulated, then a real, backend |
| tokenization | Byte-level BPE walkthrough with a tested toy tokenizer; compare with a library tokenizer |
| batching-scheduling | Max-batch-size and token-budget batching on project 01; then a continuous-batching *simulator*, labelled as simulated |
| kv-cache | KV-cache memory calculator with tested formulas; block-allocator simulation |
| quantization | Tested int8 quantise/dequantise round trip with measured error |
| gpu-profiling | Profile a small PyTorch model (needs a GPU; otherwise documentation only) |
| distributed-inference | Design document with cost reasoning; no multi-GPU claims without hardware |
| model-gateways | Routing and rate-limit layer over multiple simulated backends |
| inference-observability | Project 03 benchmark suite |

Diagrams: [serving and inference flow](../docs/architecture/diagrams/model-serving-and-inference-flow.md),
[distributed inference](../docs/architecture/diagrams/ml-lifecycle-and-distributed-inference.md) (planned designs).

## Reference papers (verified to exist at these locations)
* Yu et al., *Orca: A Distributed Serving System for Transformer-Based Generative Models*, OSDI 2022:
  <https://www.usenix.org/conference/osdi22/presentation/yu>. Its core idea is iteration-level
  scheduling: the scheduler invokes the engine for one model iteration at a time, so a newly arrived request
  waits for one iteration rather than for the whole batch.
* Kwon et al., *Efficient Memory Management for Large Language Model Serving with PagedAttention*, 2023:
  <https://arxiv.org/abs/2309.06180>. Its core idea is storing the KV cache in non-contiguous paged
  blocks, inspired by operating-system virtual memory, to reduce waste and enable sharing.

These two statements are recorded in the [claims register](../docs/claims-register.md) as
reference-only evidence, the weakest kind. They become stronger when a simulator here reproduces the
described behaviour.

## Other primary references
* NVIDIA CUDA: <https://docs.nvidia.com/cuda/> · PyTorch: <https://pytorch.org/docs/stable/> ·
  Hugging Face: <https://huggingface.co/docs> · Kubernetes: <https://kubernetes.io/docs/>
