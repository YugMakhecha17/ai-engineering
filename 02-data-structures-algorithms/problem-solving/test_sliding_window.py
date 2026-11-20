import pytest
from sliding_window import SlidingWindowRateLimiter


class FakeClock:
    def __init__(self) -> None:
        self.now = 0.0

    def __call__(self) -> float:
        return self.now


def make(limit: int = 3, window: float = 10.0) -> tuple[SlidingWindowRateLimiter, FakeClock]:
    clock = FakeClock()
    return SlidingWindowRateLimiter(limit, window, clock=clock), clock


def test_allows_up_to_limit_then_rejects() -> None:
    limiter, _ = make(limit=3)
    assert [limiter.allow() for _ in range(5)] == [True, True, True, False, False]


def test_capacity_returns_as_old_requests_leave_the_window() -> None:
    limiter, clock = make(limit=2, window=10)
    assert limiter.allow()  # t=0
    clock.now = 5
    assert limiter.allow()  # t=5
    assert not limiter.allow()
    clock.now = 9.99
    assert not limiter.allow()  # t=0 request still inside the window
    clock.now = 10
    assert limiter.allow()  # exactly one window after t=0: evicted
    assert not limiter.allow()  # t=5 and t=10 are in the window


def test_rejected_requests_are_not_recorded() -> None:
    limiter, clock = make(limit=1, window=10)
    assert limiter.allow()
    for t in (1, 2, 3, 4, 5):
        clock.now = t
        assert not limiter.allow()  # hammering must not extend the block
    clock.now = 10
    assert limiter.allow()


def test_memory_is_bounded_by_limit_regardless_of_traffic() -> None:
    limiter, clock = make(limit=5, window=1)
    for i in range(10_000):
        clock.now = i * 0.01
        limiter.allow()
        assert len(limiter._accepted) <= 5


def test_retry_after_reports_time_until_next_acceptance() -> None:
    limiter, clock = make(limit=1, window=10)
    assert limiter.retry_after() == 0.0
    limiter.allow()
    clock.now = 4
    assert limiter.retry_after() == pytest.approx(6.0)
    clock.now = 10
    assert limiter.retry_after() == 0.0


def test_current_count_reflects_eviction() -> None:
    limiter, clock = make(limit=3, window=10)
    limiter.allow()
    limiter.allow()
    assert limiter.current_count == 2
    clock.now = 11
    assert limiter.current_count == 0


@pytest.mark.parametrize(("limit", "window"), [(0, 1.0), (-1, 1.0), (1, 0.0), (1, -5.0)])
def test_invalid_configuration_is_rejected(limit: int, window: float) -> None:
    with pytest.raises(ValueError):
        SlidingWindowRateLimiter(limit, window)
