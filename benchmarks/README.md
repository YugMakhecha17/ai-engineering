# Benchmarks

Reproducible measurements. Method and rules: [methodology.md](methodology.md).

| Script | Measures | Result file | Data kind |
|--------|----------|-------------|-----------|
| [`queue_pop_benchmark.py`](queue_pop_benchmark.py) | Draining a FIFO queue: `list.pop(0)` vs `deque` vs ring buffer | [`results/queue-pop.json`](results/queue-pop.json) | measured |
| [`../projects/01-request-scheduling-engine/benchmarks/bench_schedulers.py`](../projects/01-request-scheduling-engine/benchmarks/bench_schedulers.py) | Project 01 FIFO vs priority scheduler | [`results/request-scheduler.json`](results/request-scheduler.json) | measured |

Both result files were produced in a single-CPU shared sandbox VM (see the `environment` block in each
file) and are **not representative of other hardware**. Re-run on your machine and commit the new file
with its environment; do not edit result files by hand.

Run from the repository root: `python benchmarks/queue_pop_benchmark.py`.

No inference benchmarks exist yet (project 03 harness is planned).
