# Benchmark methodology

Rules every benchmark in this repository follows. A benchmark that breaks a rule must say which.

1. **Label the data.** Each result file has `data_kind`: `measured` (code actually executed on the
   recorded machine) or `simulated` (synthetic or modelled behaviour). Simulated results are never
   presented as hardware measurements, and never mixed in one table.
2. **Record the environment** in the result file: Python version and implementation, OS, CPU model and
   count, GPU (or "not used"), and the exact command run. Numbers from different environments are not compared.
3. **Warm up, then repeat.** One untimed warm-up run, then at least five timed runs; report the median and the
   range, not a single run.
4. **Use a monotonic high-resolution clock** (`time.perf_counter`), and time only the operation of interest.
5. **Fix the inputs.** Seeded random generators; same data for every candidate.
6. **Prefer operation counts for complexity claims.** Wall-clock time depends on cache, load and
   interpreter; counting comparisons or copies does not. Tests assert counts; benchmarks report time.
7. **Separate observation from explanation.** State what was measured; label any explanation as a
   hypothesis unless a further experiment tested it.
8. **Report sample sizes** next to percentiles; a percentile higher than the sample can resolve is
   noise (see project 03).
9. **Never hand-edit results.** Regenerate with the script.
10. **Say what the benchmark cannot show** (shared noisy hardware, few sizes, no isolation of components).

## Known weaknesses of the current benchmarks
* Single-CPU shared VM: other tenants and the scheduler add noise.
* Three input sizes cannot establish a growth rate; they can only be *consistent with* one.
* No CPU frequency pinning, no process isolation, no GC control.

## Result file fields
`benchmark`, `data_kind`, `recorded_utc`, `command`, `environment`, plus benchmark-specific
`description`, parameters and `results`. Written by `bench_common.write_results`.
