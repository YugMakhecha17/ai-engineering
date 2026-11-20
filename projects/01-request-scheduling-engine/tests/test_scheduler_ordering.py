"""Ordering guarantees: FIFO, priority, and stability for equal priorities."""

from collections.abc import Callable

import pytest
from request_scheduler import EmptyQueueError, FifoScheduler, PriorityScheduler, Scheduler


def drain(scheduler: Scheduler) -> list[str]:
    order = []
    while len(scheduler):
        order.append(scheduler.next_request().payload)
    return order


def test_fifo_serves_in_arrival_order_and_ignores_priority(
    id_factory: Callable[[], str],
) -> None:
    s = FifoScheduler(id_factory=id_factory)
    for payload, priority in [("a", 9), ("b", 0), ("c", 5)]:
        s.submit(payload, priority=priority)
    assert drain(s) == ["a", "b", "c"]


def test_priority_serves_lowest_number_first(id_factory: Callable[[], str]) -> None:
    s = PriorityScheduler(id_factory=id_factory)
    for payload, priority in [("low", 9), ("high", 0), ("mid", 5)]:
        s.submit(payload, priority=priority)
    assert drain(s) == ["high", "mid", "low"]


def test_negative_priorities_are_more_urgent_than_zero(id_factory: Callable[[], str]) -> None:
    s = PriorityScheduler(id_factory=id_factory)
    s.submit("zero", priority=0)
    s.submit("urgent", priority=-10)
    assert drain(s) == ["urgent", "zero"]


@pytest.mark.parametrize("count", [2, 3, 4, 5, 10, 100])
def test_equal_priorities_are_served_in_arrival_order(count: int) -> None:
    # A bare binary heap reorders equal keys (see 02-data-structures-algorithms); this
    # fails if the sequence tie-breaker is removed from the heap entries.
    s = PriorityScheduler()
    for i in range(count):
        s.submit(f"job-{i}", priority=1)
    assert drain(s) == [f"job-{i}" for i in range(count)]


def test_stability_holds_for_interleaved_submits_and_dispatches() -> None:
    s = PriorityScheduler()
    s.submit("a1", priority=1)
    s.submit("b1", priority=1)
    assert s.next_request().payload == "a1"
    s.submit("c1", priority=1)
    s.submit("urgent", priority=0)
    s.submit("d1", priority=1)
    assert drain(s) == ["urgent", "b1", "c1", "d1"]


def test_late_urgent_request_overtakes_older_lower_priority_ones() -> None:
    s = PriorityScheduler()
    for i in range(5):
        s.submit(f"old-{i}", priority=5)
    s.submit("urgent", priority=0)
    assert s.next_request().payload == "urgent"


@pytest.mark.parametrize("scheduler_cls", [FifoScheduler, PriorityScheduler])
def test_next_request_on_empty_queue_raises(scheduler_cls: type[Scheduler]) -> None:
    with pytest.raises(EmptyQueueError):
        scheduler_cls().next_request()


@pytest.mark.parametrize("scheduler_cls", [FifoScheduler, PriorityScheduler])
def test_scheduler_is_reusable_after_draining(scheduler_cls: type[Scheduler]) -> None:
    s = scheduler_cls()
    s.submit("x")
    s.next_request()
    s.submit("y")
    assert s.next_request().payload == "y"


def test_sequence_numbers_increase_with_arrival(id_factory: Callable[[], str]) -> None:
    s = PriorityScheduler(id_factory=id_factory)
    sequences = [s.submit(f"p{i}", priority=10 - i).sequence for i in range(4)]
    assert sequences == [0, 1, 2, 3]


def test_sustained_urgent_traffic_starves_a_low_priority_request() -> None:
    """Documents a LIMITATION (see the project README): strict priority can starve work.

    One priority-9 request waits while urgent requests keep arriving; it is never dispatched.
    This test passing means the scheduler has no ageing or fairness mechanism yet. If
    fairness is added, this test should be inverted rather than deleted.
    """
    s = PriorityScheduler()
    victim = s.submit("low priority", priority=9)
    for i in range(500):
        s.submit(f"urgent-{i}", priority=0)
        assert s.next_request().payload == f"urgent-{i}"
    assert len(s) == 1
    assert s.get_state(victim.request_id).value == "queued"
