# Glossary

Terms are defined briefly and linked to where the repository demonstrates them. Entries marked
*(planned)* have no implementation yet.

| Term | Definition | Where |
|------|------------|-------|
| **Alias** | Two names bound to the same object; mutation through one is visible through the other | [mutability](../01-python-foundations/mutability/) |
| **Amortised O(1)** | Average cost per operation over a sequence is constant even if single operations occasionally cost more (e.g. append with array doubling) | [lists-arrays](../02-data-structures-algorithms/lists-arrays/) |
| **Backpressure** *(planned)* | A signal that makes producers slow down or stop when a consumer cannot keep up | 05 |
| **Batching** *(planned)* | Processing several requests in one model call to raise throughput at some cost to latency | 07 |
| **Cancellation, lazy** | Marking a queued item cancelled in O(1) and discarding it when it reaches the front, instead of removing it from the middle of the queue | [project 01](../projects/01-request-scheduling-engine/) |
| **Closure** | A function that keeps access to variables of its defining scope after that scope has returned | [functions](../01-python-foundations/functions/) |
| **Context manager** | An object with `__enter__`/`__exit__` that guarantees cleanup around a `with` block | [context-managers](../01-python-foundations/context-managers/) |
| **Decode** | Autoregressive generation of one token per step after prefill | [diagrams](architecture/diagrams/model-serving-and-inference-flow.md) |
| **Deque** | Double-ended queue with O(1) append and pop at both ends | [queues-deques](../02-data-structures-algorithms/queues-deques/) |
| **Hash collision** | Two distinct keys mapping to the same bucket | [sets-hashmaps](../02-data-structures-algorithms/sets-hashmaps/) |
| **Heap** | A tree-shaped structure, stored in an array, where each parent is ≤ its children (min-heap) | [heaps-priority-queues](../02-data-structures-algorithms/heaps-priority-queues/) |
| **Idempotent** | Repeating the operation has the same effect as doing it once (e.g. `close()`) | [context-managers](../01-python-foundations/context-managers/) |
| **Iterable / iterator** | An iterable can produce iterators; an iterator yields items and is exhausted after one pass | [iterators-generators](../01-python-foundations/iterators-generators/) |
| **KV cache** *(planned)* | Stored attention keys and values from previous tokens, reused at each decode step | 07 |
| **Lazy evaluation** | Producing values only when requested | [iterators-generators](../01-python-foundations/iterators-generators/) |
| **Load factor** | Entries ÷ buckets in a hash table; resizing keeps it bounded | [sets-hashmaps](../02-data-structures-algorithms/sets-hashmaps/) |
| **Nearest-rank percentile** | The value at rank ⌈p·n/100⌉ in sorted order; always an observed value | [project 03](../projects/03-inference-observability/) |
| **Prefill** | Processing the entire prompt in one pass before decoding | [diagrams](architecture/diagrams/model-serving-and-inference-flow.md) |
| **Protocol (typing)** | A structural interface: any class with the right methods satisfies it | [type-safety](../03-software-engineering/type-safety/) |
| **P50 / P95 / P99** | Latency below which 50 / 95 / 99 % of requests fall | [project 03](../projects/03-inference-observability/) |
| **Stable ordering** | Items with equal keys keep their arrival order | [heaps-priority-queues](../02-data-structures-algorithms/heaps-priority-queues/) |
| **Time to first token (TTFT)** | Delay from request start to the first generated token | [project 03](../projects/03-inference-observability/) |
| **Throughput** | Completed requests or tokens per unit time | [project 03](../projects/03-inference-observability/) |
