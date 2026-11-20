import math
import random

import pytest
from inference_observability import (
    inter_token_latencies,
    percentile,
    summarize,
    throughput,
    time_to_first_token,
)


def test_nearest_rank_on_one_to_one_hundred() -> None:
    data = list(range(1, 101))
    assert percentile(data, 50) == 50
    assert percentile(data, 95) == 95
    assert percentile(data, 99) == 99
    assert percentile(data, 100) == 100
    assert percentile(data, 0) == 1  # rank 0 is clamped to the minimum


def test_input_order_does_not_matter_and_input_is_not_mutated() -> None:
    data = [5.0, 1.0, 3.0]
    assert percentile(data, 50) == 3.0
    assert data == [5.0, 1.0, 3.0]


def test_result_is_always_an_observed_value_never_interpolated() -> None:
    rng = random.Random(0)
    data = [rng.random() for _ in range(37)]
    for p in (1, 25, 50, 90, 99, 99.9):
        assert percentile(data, p) in data


def test_small_sample_tail_percentiles_collapse_to_the_maximum() -> None:
    assert percentile([10, 20, 30], 99) == 30  # with 3 samples p99 *is* the max: low confidence


def test_float_error_does_not_shift_the_rank() -> None:
    # 0.07 * 100 == 7.000000000000001 in binary floating point; a naive ceil() gives rank 8.
    assert 0.07 * 100 > 7
    data = list(range(1, 101))
    assert percentile(data, 7) == 7
    # Fractional percentiles are exact too: rank = ceil(99.9% of 1000) = 999.
    assert percentile(list(range(1, 1001)), 99.9) == 999


def test_integer_percentiles_match_exact_integer_rank_for_many_sizes() -> None:
    # Reference rank computed with pure integer arithmetic: ceil(p * n / 100) == -(-p * n // 100).
    for n in range(1, 201):
        data = list(range(1, n + 1))  # value == its rank, so the result IS the rank
        for p in range(0, 101):
            expected_rank = max(-(-p * n // 100), 1)
            assert percentile(data, p) == expected_rank, (p, n)


def test_fractional_percentiles_match_exact_integer_rank() -> None:
    # p = k / 10 percent, so rank = ceil(k * n / 1000) in pure integer arithmetic.
    for n in range(1, 121):
        data = list(range(1, n + 1))
        for k in range(0, 1001):
            expected_rank = max(-(-k * n // 1000), 1)
            assert percentile(data, k / 10) == expected_rank, (k / 10, n)


def test_single_value() -> None:
    assert percentile([42.0], 99) == 42.0


@pytest.mark.parametrize("p", [-1, 100.1, True, float("nan")])
def test_invalid_percentiles_are_rejected(p: float) -> None:
    with pytest.raises(ValueError):
        percentile([1.0], p)


def test_empty_and_nan_inputs_are_rejected() -> None:
    with pytest.raises(ValueError, match="empty"):
        percentile([], 50)
    with pytest.raises(ValueError, match="NaN"):
        percentile([1.0, math.nan], 50)


def test_summary_of_known_data() -> None:
    summary = summarize([float(x) for x in range(1, 101)])
    assert summary.count == 100
    assert (summary.minimum, summary.maximum) == (1.0, 100.0)
    assert summary.mean == pytest.approx(50.5)
    assert (summary.p50, summary.p95, summary.p99) == (50.0, 95.0, 99.0)


def test_one_outlier_moves_p99_and_mean_but_not_the_median() -> None:
    base = [10.0] * 99
    summary = summarize([*base, 5_000.0])
    assert summary.p50 == 10.0
    assert summary.p99 == 10.0  # nearest-rank p99 of 100 samples is the 99th value
    assert summary.maximum == 5_000.0
    assert summary.mean > 50  # the mean is dragged up: why tail percentiles are reported


def test_summary_rejects_empty_and_negative_latencies() -> None:
    with pytest.raises(ValueError):
        summarize([])
    with pytest.raises(ValueError, match="non-negative"):
        summarize([1.0, -0.1])


def test_throughput() -> None:
    assert throughput(500, 2.0) == 250.0
    assert throughput(0, 1.0) == 0.0
    with pytest.raises(ValueError):
        throughput(1, 0)
    with pytest.raises(ValueError):
        throughput(-1, 1.0)


def test_time_to_first_token_and_inter_token_latency() -> None:
    token_times = [10.5, 10.6, 10.8, 11.1]
    assert time_to_first_token(10.0, token_times) == pytest.approx(0.5)
    assert inter_token_latencies(token_times) == pytest.approx([0.1, 0.2, 0.3])
    assert inter_token_latencies([1.0]) == []
    assert inter_token_latencies([]) == []


def test_timing_helpers_reject_impossible_timestamps() -> None:
    with pytest.raises(ValueError, match="no tokens"):
        time_to_first_token(0.0, [])
    with pytest.raises(ValueError, match="precedes"):
        time_to_first_token(5.0, [4.0])
    with pytest.raises(ValueError, match="non-decreasing"):
        inter_token_latencies([1.0, 3.0, 2.0])
