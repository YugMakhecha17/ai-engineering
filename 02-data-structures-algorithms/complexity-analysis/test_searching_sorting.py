import math
import random

import pytest
from searching_sorting import binary_search, insertion_sort, linear_search, merge_sort


def test_linear_search_finds_present_and_reports_absent() -> None:
    data = [5, 3, 9, 1]
    assert linear_search(data, 9).index == 2
    assert linear_search(data, 9).probes == 3
    assert linear_search(data, 7).index is None
    assert linear_search(data, 7).probes == 4  # worst case examines all n
    assert linear_search([], 1).index is None


@pytest.mark.parametrize("n", [1, 2, 3, 7, 8, 100, 1023, 1024, 5000])
def test_binary_search_never_exceeds_floor_log2_n_plus_1_probes(n: int) -> None:
    data = list(range(0, 2 * n, 2))  # even numbers, so odd targets are absent
    bound = math.floor(math.log2(n)) + 1
    for target in [*data, *(t + 1 for t in data), -1, 2 * n + 1]:
        result = binary_search(data, target)
        assert result.probes <= bound
        if target % 2 == 0 and 0 <= target < 2 * n:
            assert result.index == target // 2
        else:
            assert result.index is None


def test_binary_search_on_empty_input() -> None:
    assert binary_search([], 3).index is None
    assert binary_search([], 3).probes == 0


def test_binary_search_gives_a_wrong_answer_if_the_precondition_is_violated() -> None:
    unsorted = [5, 1, 4, 2, 3]
    assert 3 in unsorted
    assert binary_search(unsorted, 3).index is None  # present, but not found: input must be sorted


def test_binary_search_beats_linear_search_by_orders_of_magnitude() -> None:
    n = 1_000_000
    data = list(range(n))
    assert linear_search(data, n - 1).probes == n
    assert binary_search(data, n - 1).probes <= 20


def test_insertion_sort_best_and_worst_case_comparison_counts() -> None:
    n = 200
    _, best = insertion_sort(list(range(n)))
    _, worst = insertion_sort(list(range(n, 0, -1)))
    assert best == n - 1  # already sorted: one comparison per element
    assert worst == n * (n - 1) // 2  # reversed: quadratic


def test_merge_sort_comparison_count_is_bounded_by_n_log_n() -> None:
    rng = random.Random(11)
    for n in (2, 10, 100, 1000, 4096):
        data = [rng.random() for _ in range(n)]
        result, comparisons = merge_sort(data)
        assert result == sorted(data)
        assert comparisons <= n * math.ceil(math.log2(n))


def test_both_sorts_match_builtin_sorted_on_random_input() -> None:
    rng = random.Random(12)
    for _ in range(50):
        data = [rng.randint(-20, 20) for _ in range(rng.randint(0, 60))]
        assert insertion_sort(data)[0] == sorted(data)
        assert merge_sort(data)[0] == sorted(data)


def test_sorting_does_not_mutate_the_input() -> None:
    data = [3, 1, 2]
    insertion_sort(data)
    merge_sort(data)
    assert data == [3, 1, 2]


def test_quadratic_sort_overtakes_n_log_n_sort_as_input_grows() -> None:
    rng = random.Random(13)
    data = [rng.random() for _ in range(2000)]
    assert insertion_sort(data)[1] > 20 * merge_sort(data)[1]
