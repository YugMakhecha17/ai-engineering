# Inference observability: design notes (planned)

Design intent only; nothing beyond `metrics.py` exists.

## Why open-loop load generation
A closed-loop client (send, wait for the reply, send again) slows down when the server slows down, so
it under-reports latency during overload ("coordinated omission"). An open-loop generator sends at a
scheduled rate regardless, so queueing delay appears in the data. The harness will be open-loop; the
claim should be demonstrated with the simulated backend before it is relied on.

## Result schema (draft)
```json
{
  "benchmark": "name",
  "data_kind": "measured | simulated",
  "recorded_utc": "ISO-8601",
  "command": "exact command line",
  "environment": {"python": "...", "platform": "...", "cpu_count": 0, "gpu": "..."},
  "parameters": {"...": "..."},
  "samples": [{"request_id": "...", "latency_s": 0.0, "ttft_s": 0.0, "tokens": 0, "error": false}],
  "summary": {"p50_s": 0.0, "p95_s": 0.0, "p99_s": 0.0, "throughput_rps": 0.0}
}
```
`benchmarks/bench_common.py` already writes the top-level fields (`benchmark`, `data_kind`,
`recorded_utc`, `command`, `environment`).

## Interpretation rules
* Report sample counts next to every percentile; flag percentiles above what the sample can support.
* Never compare numbers from different environments without saying so.
* Explain a difference with a hypothesis and say whether it was tested.
