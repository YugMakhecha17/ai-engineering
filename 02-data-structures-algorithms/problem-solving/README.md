# Problem decomposition: a sliding-window rate limiter

Code: [`sliding_window.py`](sliding_window.py) · Tests: [`test_sliding_window.py`](test_sliding_window.py)

## 1. Problem
Allow at most N requests in any rolling T-second window, rejecting the rest.

## 2. First-principles explanation (the decomposition)
1. **State**: what must be remembered? Timestamps of *accepted* requests, oldest first.
2. **Invariant**: after discarding timestamps older than T, at most N remain.
3. **Operation `allow()`**: read the clock → evict expired → if N remain reject, else record and accept.
4. **Data structure**: appends at the back, evictions at the front → a deque (FIFO).
5. **Edge cases**: a timestamp exactly T old is expired; rejected requests are not recorded; invalid
   configuration.
6. **Complexity**: each timestamp is added once and removed once → O(1) amortised per call;
   memory O(N) regardless of traffic.

## 3. Technical details
The clock is an injected callable, so tests control time exactly and never sleep. The boundary rule
(`timestamp <= now - window` is expired) means a window is half-open.

## 4. Runnable implementation
`SlidingWindowRateLimiter(limit, window_seconds, clock)` with `allow()`, `current_count`,
`retry_after()`.

## 5. Expected behaviour
With limit 2, window 10 s: requests at t = 0 and 5 accepted; a third at t = 9.99 rejected; at t = 10 the
t = 0 request has expired, so one more is accepted.

## 6. Tests
Limit then reject; capacity returns at the exact boundary; hammering while blocked does not extend
the block; memory bounded by `limit` over 10,000 requests; `retry_after`; invalid configuration.

## 7. Engineering trade-offs
| Algorithm | Memory | Accuracy | Notes |
|-----------|--------|----------|-------|
| Sliding-window log (this) | O(N) | Exact | Simple, per-key memory can be large for big N |
| Fixed window counter | O(1) | Allows up to 2N across a window boundary | Cheapest |
| Token bucket | O(1) | Allows controlled bursts | Common for API gateways |

This implementation is single-process and not thread-safe; a shared limiter needs a lock or an
external store (not built here).

## 8. AI-infrastructure connection
Rate limiting and admission control protect an inference backend from overload and enforce per-tenant
quotas at the model gateway (section 07, planned).

## 9. Common mistakes
Counting rejected requests (a client retrying in a loop is never released); using wall-clock time that
can jump backwards instead of a monotonic clock; unbounded timestamp storage.

## 10. References
* `collections.deque`: <https://docs.python.org/3/library/collections.html#collections.deque>
* `time.monotonic`: <https://docs.python.org/3/library/time.html#time.monotonic>
