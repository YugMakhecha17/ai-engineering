# SQL filtering, grouping and aggregation

Code: [`where_vs_group_by.py`](where_vs_group_by.py) · Tests: [`test_where_vs_group_by.py`](test_where_vs_group_by.py)

This topic exists to resolve a specific, recorded confusion: **row-level filtering (`WHERE`) vs
group aggregation (`GROUP BY`) and group filtering (`HAVING`)**.

## 1. Problem
"Show me models with at least two errors, and their average latency over successful requests."
Which clause handles which part?

## 2. First-principles explanation
SQL is declarative, but the engine evaluates clauses in a fixed *logical* order:

`FROM` → `WHERE` → `GROUP BY` → `HAVING` → `SELECT` → `ORDER BY`

* `WHERE` sees **individual rows** and removes rows *before* any grouping.
* `GROUP BY` collapses the remaining rows into **one row per group**; aggregates (`COUNT`, `AVG`,
  `SUM`, …) are computed per group.
* `HAVING` sees **groups** and removes groups *after* aggregation, so it can test an aggregate.

Because aggregates do not exist yet when `WHERE` runs, `WHERE COUNT(*) > 1` is an error.

## 3. Technical details
Table `inference_log(request_id, model, status, latency_ms)` with 7 rows (see the test fixture):

| Question | Query shape |
|----------|-------------|
| Which individual requests were slow? | `WHERE latency_ms > 100` |
| Average latency per model, all requests | `GROUP BY model` with `AVG(latency_ms)` |
| Average latency per model, **successful requests only** | `WHERE status = 'ok'` then `GROUP BY model` |
| Models with at least N errors | `WHERE status = 'error'` then `GROUP BY model` then `HAVING COUNT(*) >= N` |

Rule of thumb: if the condition mentions a **column of a row**, it belongs in `WHERE`; if it mentions
an **aggregate**, it belongs in `HAVING`. Filtering rows early (`WHERE`) usually also reduces the
work done before aggregation, though the planner decides.

## 4. Runnable implementation
Uses the standard-library `sqlite3` so it runs anywhere. These queries are plain ANSI SQL and are
expected to behave the same in PostgreSQL, but **that has not been run against PostgreSQL here**.
SQLite is also more permissive than PostgreSQL about column types (it uses type affinity), so do not
infer PostgreSQL behaviour from SQLite in general; re-run against PostgreSQL before relying on it.

## 5. Expected behaviour
Averages per model over all rows: `large` 375.0, `small` 120.0. Over `status = 'ok'` only: `large`
150.0, `small` 30.0. Models with ≥ 2 errors: `large` (2).

## 6. Tests
Row filter (note `100` is not `> 100`); group collapse with counts and averages; `WHERE`-then-`GROUP BY`
changes what is averaged; `HAVING` thresholds 1, 2, 3; aggregate in `WHERE` raises
`sqlite3.OperationalError` ("misuse of aggregate").

## 7. Engineering trade-offs
`WHERE` conditions on indexed columns can use those indexes; `HAVING` operates on already-grouped
data. A condition on a grouping column may be accepted in `HAVING`, but it obscures intent and its
cost depends on the planner; check with `EXPLAIN` rather than assuming.

## 8. AI-infrastructure connection
Inference logs and metrics stores are queried exactly this way: error counts per model per hour,
average latency over successful requests, tenants exceeding a quota.

## 9. Common mistakes
Using an aggregate in `WHERE`; selecting a non-grouped column with `GROUP BY`; assuming `HAVING`
replaces `WHERE`; counting `NULL`s without realising `COUNT(col)` skips them but `COUNT(*)` does not.

## 10. References
* PostgreSQL tutorial, aggregate functions: <https://www.postgresql.org/docs/current/tutorial-agg.html>
* PostgreSQL, `GROUP BY` and `HAVING`: <https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-GROUP>
* `sqlite3`: <https://docs.python.org/3/library/sqlite3.html>

## Exercises (unresolved: E-07, for the owner)
Design your own table (for example `jobs(id, queue, state, duration_ms)`), then write five queries
mixing `WHERE`, `GROUP BY` and `HAVING`. For each, write one sentence stating **which rows each
clause sees**. Verify results with a test or by hand-computed expected output. Do this before
extending the example above.
