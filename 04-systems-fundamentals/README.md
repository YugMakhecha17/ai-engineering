# 04 · Systems fundamentals

**Status: planned. No code or tests exist in this section yet.** The directory contains this
topic map only ([ADR 0003](../docs/decisions/0003-no-empty-directories.md)); a topic directory is
created in the commit that adds its first tested implementation.

## Prerequisites
Sections [01](../01-python-foundations/) to [03](../03-software-engineering/): functions and
exceptions, queues and complexity, testing and debugging. Do not start concurrency before the
independent exercises E-01…E-08 are reviewed.

## Topic map

| Topic | Question to answer with evidence | First planned implementation |
|-------|----------------------------------|------------------------------|
| operating-systems | What does the OS do between my code and the hardware? | Annotated `strace`/`psutil` observations of a Python process |
| memory-processes-threads | Process vs thread: isolation, cost, sharing | Measure process vs thread startup and shared-state behaviour |
| networking | TCP vs UDP; where does latency come from? | Socket echo server/client with measured round-trip time |
| concurrency | Concurrency vs parallelism; the GIL; races and locks | A reproducible race on a shared counter, then the lock fix, with a test |
| async-programming | When does `asyncio` help? | I/O-bound task runner compared with threads, with measurements |
| performance | How to find a bottleneck | Profile project 01 with `cProfile` and record before/after |

CPU scheduling, memory management and I/O are studied through these implementations rather than as theory alone.

## Exit evidence (see [roadmap](../docs/learning-roadmap.md), phase 2)
A reproduced race condition and its fix with a test; a profile-driven optimisation with before and
after measurements; thread-safety added to the project 01 scheduler.

## References (primary)
* Python `threading`, `multiprocessing`, `asyncio`: <https://docs.python.org/3/library/concurrency.html>
* Linux man pages: <https://man7.org/linux/man-pages/>
* `cProfile`: <https://docs.python.org/3/library/profile.html>
