"""WHERE filters rows; GROUP BY forms groups; HAVING filters groups.

Runnable with the standard-library sqlite3 module. The queries used here are plain
ANSI SQL and behave identically in PostgreSQL; engine differences are noted in README.md.

Provenance: worked example written with AI assistance. The exercises in README.md are
for the repository owner to solve independently (see docs/progress-tracker.md).
"""

from __future__ import annotations

import sqlite3

SCHEMA = """
CREATE TABLE inference_log (
    request_id  TEXT PRIMARY KEY,
    model       TEXT NOT NULL,
    status      TEXT NOT NULL CHECK (status IN ('ok', 'error')),
    latency_ms  INTEGER NOT NULL
)
"""

# 1. Row-level filter: runs BEFORE any grouping, one row at a time.
SLOW_REQUESTS = "SELECT request_id FROM inference_log WHERE latency_ms > 100 ORDER BY request_id"

# 2. Aggregation: collapses rows into one row per group.
AVG_LATENCY_BY_MODEL = (
    "SELECT model, COUNT(*) AS n, AVG(latency_ms) AS avg_ms "
    "FROM inference_log GROUP BY model ORDER BY model"
)

# 3. WHERE then GROUP BY: only 'ok' rows are averaged.
AVG_LATENCY_OK_ONLY = (
    "SELECT model, AVG(latency_ms) AS avg_ms FROM inference_log "
    "WHERE status = 'ok' GROUP BY model ORDER BY model"
)

# 4. HAVING: a condition on the aggregate itself. WHERE cannot do this because the
#    count does not exist yet when WHERE runs.
MODELS_WITH_MANY_ERRORS = (
    "SELECT model, COUNT(*) AS errors FROM inference_log "
    "WHERE status = 'error' GROUP BY model HAVING COUNT(*) >= :minimum ORDER BY model"
)

# Logical evaluation order: FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY.


def make_connection(rows: list[tuple[str, str, str, int]]) -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.execute(SCHEMA)
    conn.executemany("INSERT INTO inference_log VALUES (?, ?, ?, ?)", rows)
    return conn


def slow_requests(conn: sqlite3.Connection) -> list[str]:
    return [r[0] for r in conn.execute(SLOW_REQUESTS)]


def avg_latency_by_model(conn: sqlite3.Connection) -> list[tuple[str, int, float]]:
    return list(conn.execute(AVG_LATENCY_BY_MODEL))


def avg_latency_ok_only(conn: sqlite3.Connection) -> list[tuple[str, float]]:
    return list(conn.execute(AVG_LATENCY_OK_ONLY))


def models_with_many_errors(conn: sqlite3.Connection, minimum: int) -> list[tuple[str, int]]:
    return list(conn.execute(MODELS_WITH_MANY_ERRORS, {"minimum": minimum}))
