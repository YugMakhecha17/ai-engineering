# Project 03 · Inference observability and benchmarking

**Status: measurement primitives implemented and tested. The benchmark harness, visualisations and
any inference measurements do not exist yet.** The repository contains **no inference benchmark
results**; do not infer any.

## Purpose
Measure inference performance and the trade-offs between latency, throughput and resource use,
with methodology that lets someone else reproduce or challenge the numbers.

## What is implemented (`src/inference_observability/metrics.py`)
| Function | Computes |
|----------|----------|
| `percentile(values, p)` | Nearest-rank percentile (always an observed value), exact arithmetic |
| `summarize(latencies)` | count, min, max, mean, P50, P95, P99 |
| `throughput(completed, duration)` | requests or tokens per second |
| `time_to_first_token(start, token_times)` | TTFT |
| `inter_token_latencies(token_times)` | gaps between tokens |

Verified by 14 tests, including:
* the float-rounding trap (`0.07 * 100 == 7.000000000000001` would shift a naive rank) is avoided
  (`test_float_error_does_not_shift_the_rank`);
* with few samples, P99 is the maximum, so a P99 over 3 samples carries almost no information
  (`test_small_sample_tail_percentiles_collapse_to_the_maximum`);
* one outlier among 100 samples leaves P50 **and** nearest-rank P99 unchanged but drags the mean and
  shows only in the maximum (`test_one_outlier_moves_p99_and_mean_but_not_the_median`). Seeing a 1 %
  tail needs P99 over more than 100 samples, or a high percentile such as P99.9 on enough data.

**Percentile definition matters.** This module uses nearest-rank. Libraries that interpolate
(for example NumPy's default) report different numbers on small samples; always state the method.

## Metrics to be tracked (planned)
| Metric | Definition | Status |
|--------|------------|--------|
| Request latency, P50/P95/P99 | End-to-end time per request | primitives done |
| Throughput | Completed requests (or tokens) / wall-clock seconds | primitive done |
| Time to first token | Request start → first token | primitive done |
| Inter-token latency | Gap between consecutive tokens | primitive done |
| Tokens per second | Output tokens / generation time | planned (derivable from the above) |
| Error rate | Failed / total requests | planned |
| Queue waiting time | Dispatch time − submission time (project 01 records `submitted_at`) | planned |
| Batch size distribution | Per dispatched batch | planned (needs batching) |
| Resource utilisation | CPU, memory; GPU where measurable | planned |

## Benchmark plan
1. A load generator with fixed arrival process and seed (open-loop, so queueing delay is not hidden).
2. Sweep one variable at a time (concurrency, batch size, prompt length).
3. Warm-up discarded; repeated runs; raw samples saved as JSON/CSV with environment metadata.
4. Plots generated from the saved raw data by a script, never hand-edited.
5. Every result file declares `data_kind`: `measured` (real hardware/software, environment recorded)
   or `simulated` (synthetic backend). The two are reported in separate tables.

Methodology: [../../benchmarks/methodology.md](../../benchmarks/methodology.md).
Design notes: [docs/design.md](docs/design.md).

## Run
`python -m pytest projects/03-inference-observability`
