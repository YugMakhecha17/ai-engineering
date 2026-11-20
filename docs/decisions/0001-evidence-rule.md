# ADR 0001: Every important technical claim needs evidence

**Status:** Accepted, in force from the first commit.

## Context

Engineering notes drift into assertions that sound right and are never checked: "heaps give
efficient priority scheduling", "deque is faster than a list", "generators save memory". In a
technical interview each of these invites the follow-up *"how do you know?"*, and a note that
only restates the textbook answer has no reply.

## Decision

> **Every important technical claim in this repository must be supported by at least one of:
> an explanation, an implementation, a test, or a reliable reference.**

An *important technical claim* is any statement a reader could act on or repeat as fact:
complexity, correctness, stability, safety, performance, or "X is better than Y when ...".
Plain definitions do not need evidence.

### What counts as adequate evidence

| Kind of claim | Adequate evidence | Example in this repo |
|---------------|-------------------|----------------------|
| Behaviour / correctness | A test, including edge and failure cases | Equal-priority requests keep arrival order |
| Algorithmic complexity | An implementation instrumented with operation counts **and** a test asserting the bound; wall-clock is secondary | Heap `pop` ≤ 2·log₂ n comparisons |
| Performance | A reproducible benchmark with environment recorded, labelled *measured* or *simulated* | `list.pop(0)` vs `deque` |
| Trade-off ("X over Y when ...") | Explanation **plus** a demonstration of where the alternative fails | Heap alone is unstable; sequence tie-breaker fixes it |
| External fact | A primary reference (official docs, paper) | Orca iteration-level scheduling |
| Limitation | Stated explicitly next to the claim it limits | Lazy deletion holds memory until entries surface |

Prefer the strongest evidence available. A claim backed only by prose or only by a citation is
legal but *weak*; the tooling reports it so it can be strengthened.

### Worked example (the rule applied)

Claim: *"A heap provides efficient priority scheduling."* That sentence is not allowed to stand
alone. The repository instead provides:

1. **Implementation**: `PriorityScheduler` (heap-based) in project 01, and a hand-written
   `BinaryHeap` in `02-data-structures-algorithms/heaps-priority-queues/`.
2. **Tests**: equal-priority requests are served in arrival order; a seeded model-based test
   compares the scheduler to a brute-force reference over thousands of random operations.
3. **Complexity analysis**: push ≤ ⌊log₂ n⌋ comparisons, pop ≤ 2⌊log₂ n⌋, asserted by tests
   that count comparisons.
4. **Limitations**: a bare heap is not stable; cancellation needs lazy deletion; priority
   starvation is possible; see the project README.

### How the rule is enforced

* `docs/claims-register.md` lists the claims, each with typed evidence pointers
  (`impl:`, `test:`, `doc:`, `ref:`).
* `scripts/check_evidence.py` fails if a claim has no evidence, a cited file or symbol does not
  exist, or a `test:` pointer does not name a real `test_*` function. It runs in CI and via
  `make evidence`.
* CONTRIBUTING.md requires every pull request that adds a claim to add or update a register row.

## Consequences

* Slower to write, much easier to defend. Every register row is a prepared interview answer.
* The register is not exhaustive: it covers claims chosen as *important*. Prose elsewhere in the
  repository is still expected to follow the rule, and reviewers should flag violations.
* The checker verifies that evidence **exists**, not that it is **sufficient**. Sufficiency is a
  human judgement made in review.
