# Complexity analysis

Code: [`searching_sorting.py`](searching_sorting.py) · Tests: [`test_searching_sorting.py`](test_searching_sorting.py)

## 1. Problem
"This is O(log n)" is easy to say and easy to get wrong. How can the claim be checked on any machine?

## 2. First-principles explanation
Time and space complexity describe how cost grows with input size n, ignoring constant factors.
Count a **basic operation** (comparison, copy, shift) instead of seconds. Operation counts are
deterministic, so a test can assert an exact bound; wall-clock time depends on hardware, caches,
load and the interpreter.

## 3. Technical details
| Algorithm | Best | Worst | Extra space | Needs |
|-----------|------|-------|-------------|-------|
| Linear search | O(1) | O(n) | O(1) | nothing |
| Binary search | O(1) | O(log n) | O(1) | **sorted** input |
| Insertion sort | O(n) | O(n²) | O(1) | nothing |
| Merge sort | O(n log n) | O(n log n) | O(n) | nothing |

Asserted bounds: binary search ≤ ⌊log₂ n⌋ + 1 probes; insertion sort exactly n − 1 comparisons
when sorted and n(n−1)/2 when reversed; merge sort ≤ n⌈log₂ n⌉ comparisons.

## 4. Runnable implementation
`linear_search`, `binary_search` (return probes), `insertion_sort`, `merge_sort` (return comparisons).

## 5. Expected behaviour
For n = 1,000,000 the tests show linear search of the last element needs 1,000,000 probes and binary
search at most 20.

## 6. Tests
Exact bounds over many n and every present/absent target; empty input; precondition violation gives
a wrong answer (binary search on unsorted data misses a present item); best/worst cases; agreement
with `sorted`; no input mutation; quadratic vs n log n gap.

## 7. Engineering trade-offs
Asymptotics predict behaviour at scale, not at small n: for a handful of items a linear scan beats a
hash map. Sorting once to enable many binary searches pays off only if the number of searches is
large enough to amortise the sort. Space matters too: merge sort buys speed with O(n) memory.

## 8. AI-infrastructure connection
Queue depth under load is the "n" that makes a quadratic operation fatal, and p99 latency is where
accidental O(n) shows up first. Complexity budgets belong in scheduler design reviews.

## 9. Common mistakes
Confusing average with worst case; ignoring the cost of building an index; reading a timing on tiny
inputs as evidence of asymptotic behaviour; forgetting that binary search requires sorted data.

## 10. References
* Python time complexity: <https://wiki.python.org/moin/TimeComplexity>
* `bisect` (library binary search): <https://docs.python.org/3/library/bisect.html>
