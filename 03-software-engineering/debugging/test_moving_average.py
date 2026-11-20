import logging

import pytest
from moving_average import moving_average


def test_basic_windows() -> None:
    assert moving_average([1, 2, 3, 4, 5], 3) == [2.0, 3.0, 4.0]


def test_regression_last_window_is_included() -> None:
    # The original bug used range(window, len(values) - 1), silently dropping the final window.
    values = [10, 20, 30, 40]
    result = moving_average(values, 2)
    assert len(result) == len(values) - 2 + 1
    assert result[-1] == 35.0


def test_window_of_one_returns_input_and_full_window_returns_the_mean() -> None:
    assert moving_average([4, 8], 1) == [4.0, 8.0]
    assert moving_average([4, 8], 2) == [6.0]


def test_matches_naive_recomputation() -> None:
    values = [3.5, -1.0, 8.25, 0.0, 12.0, 7.5, 2.0]
    for window in range(1, len(values) + 1):
        naive = [sum(values[i : i + window]) / window for i in range(len(values) - window + 1)]
        assert moving_average(values, window) == pytest.approx(naive)


@pytest.mark.parametrize("window", [0, -1, 6])
def test_invalid_windows_raise(window: int) -> None:
    with pytest.raises(ValueError):
        moving_average([1, 2, 3, 4, 5], window)


def test_debug_logging_is_available_without_print_statements(
    caplog: pytest.LogCaptureFixture,
) -> None:
    with caplog.at_level(logging.DEBUG, logger="moving_average"):
        moving_average([1, 2, 3], 2)
    assert any("current_sum" in r.message for r in caplog.records)
