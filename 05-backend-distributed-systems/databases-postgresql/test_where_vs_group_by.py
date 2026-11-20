import sqlite3

import pytest
from where_vs_group_by import (
    avg_latency_by_model,
    avg_latency_ok_only,
    make_connection,
    models_with_many_errors,
    slow_requests,
)

ROWS = [
    ("r1", "small", "ok", 20),
    ("r2", "small", "ok", 40),
    ("r3", "small", "error", 300),
    ("r4", "large", "ok", 200),
    ("r5", "large", "error", 500),
    ("r6", "large", "error", 700),
    ("r7", "large", "ok", 100),
]


@pytest.fixture
def conn() -> sqlite3.Connection:
    return make_connection(ROWS)


def test_where_filters_individual_rows(conn: sqlite3.Connection) -> None:
    assert slow_requests(conn) == ["r3", "r4", "r5", "r6"]  # 100 is not > 100


def test_group_by_collapses_rows_to_one_per_group(conn: sqlite3.Connection) -> None:
    result = avg_latency_by_model(conn)
    assert [(m, n) for m, n, _ in result] == [("large", 4), ("small", 3)]
    assert {m: avg for m, _, avg in result} == {"large": 375.0, "small": 120.0}


def test_where_runs_before_grouping_so_it_changes_what_is_averaged(
    conn: sqlite3.Connection,
) -> None:
    assert avg_latency_ok_only(conn) == [("large", 150.0), ("small", 30.0)]


def test_having_filters_groups_after_aggregation(conn: sqlite3.Connection) -> None:
    assert models_with_many_errors(conn, 2) == [("large", 2)]
    assert models_with_many_errors(conn, 1) == [("large", 2), ("small", 1)]
    assert models_with_many_errors(conn, 3) == []


def test_aggregate_in_where_is_a_syntax_error_because_it_does_not_exist_yet(
    conn: sqlite3.Connection,
) -> None:
    with pytest.raises(sqlite3.OperationalError, match="misuse of aggregate"):
        conn.execute("SELECT model FROM inference_log WHERE COUNT(*) > 1 GROUP BY model")
