"""Request lifecycle, cancellation (including lazy deletion), IDs, clock and metadata."""

from collections.abc import Callable
from typing import Any

import pytest
from conftest import FakeClock
from request_scheduler import (
    DuplicateRequestError,
    EmptyQueueError,
    FifoScheduler,
    InvalidStateTransitionError,
    PriorityScheduler,
    RequestState,
    Scheduler,
    UnknownRequestError,
)

BOTH = pytest.mark.parametrize("scheduler_cls", [FifoScheduler, PriorityScheduler])


@BOTH
def test_happy_path_queued_running_completed(scheduler_cls: type[Scheduler]) -> None:
    s = scheduler_cls()
    r = s.submit("work", request_id="r1")
    assert s.get_state("r1") is RequestState.QUEUED
    assert len(s) == 1
    assert s.next_request() is r
    assert s.get_state("r1") is RequestState.RUNNING
    assert len(s) == 0  # running requests are no longer "waiting"
    s.complete("r1")
    assert s.get_state("r1") is RequestState.COMPLETED


@BOTH
def test_cancelled_queued_request_is_never_dispatched(scheduler_cls: type[Scheduler]) -> None:
    s = scheduler_cls()
    s.submit("keep-1", request_id="a")
    s.submit("drop", request_id="b")
    s.submit("keep-2", request_id="c")
    s.cancel("b")
    assert s.get_state("b") is RequestState.CANCELLED
    assert len(s) == 2
    assert [s.next_request().request_id, s.next_request().request_id] == ["a", "c"]
    with pytest.raises(EmptyQueueError):
        s.next_request()


@BOTH
def test_cancelling_the_head_of_the_queue_works(scheduler_cls: type[Scheduler]) -> None:
    s = scheduler_cls()
    s.submit("first", request_id="a")
    s.submit("second", request_id="b")
    s.cancel("a")
    assert s.next_request().request_id == "b"


@BOTH
def test_running_request_can_be_cancelled(scheduler_cls: type[Scheduler]) -> None:
    s = scheduler_cls()
    s.submit("w", request_id="r")
    s.next_request()
    s.cancel("r")
    assert s.get_state("r") is RequestState.CANCELLED
    assert len(s) == 0  # queue length must not go negative


@BOTH
@pytest.mark.parametrize("terminal_action", ["complete", "cancel"])
def test_terminal_states_are_final(scheduler_cls: type[Scheduler], terminal_action: str) -> None:
    s = scheduler_cls()
    s.submit("w", request_id="r")
    s.next_request()
    getattr(s, terminal_action)("r")
    for action in (s.complete, s.cancel):
        with pytest.raises(InvalidStateTransitionError):
            action("r")


@BOTH
def test_cannot_complete_a_request_that_never_started(scheduler_cls: type[Scheduler]) -> None:
    s = scheduler_cls()
    s.submit("w", request_id="r")
    with pytest.raises(InvalidStateTransitionError, match="queued to completed"):
        s.complete("r")
    assert s.get_state("r") is RequestState.QUEUED  # failed transition changed nothing
    assert len(s) == 1


@BOTH
def test_unknown_ids_raise(scheduler_cls: type[Scheduler]) -> None:
    s = scheduler_cls()
    for action in (s.complete, s.cancel, s.get_state, s.get_request):
        with pytest.raises(UnknownRequestError):
            action("nope")


@BOTH
def test_duplicate_ids_are_rejected_even_after_the_request_finished(
    scheduler_cls: type[Scheduler],
) -> None:
    s = scheduler_cls()
    s.submit("w", request_id="r")
    with pytest.raises(DuplicateRequestError):
        s.submit("w2", request_id="r")
    s.cancel("r")
    with pytest.raises(DuplicateRequestError):  # IDs are never recycled
        s.submit("w3", request_id="r")
    assert len(s) == 0


@BOTH
def test_failed_submit_leaves_no_trace(scheduler_cls: type[Scheduler]) -> None:
    s = scheduler_cls()
    with pytest.raises(ValueError):
        s.submit("")
    assert len(s) == 0
    assert s.physical_size == 0
    assert "anything" not in s


def test_lazy_deletion_leaves_stale_entries_until_they_surface() -> None:
    s = PriorityScheduler()
    ids = [s.submit(f"j{i}", priority=i).request_id for i in range(1_000)]
    for rid in ids:
        s.cancel(rid)
    assert len(s) == 0  # logically empty...
    assert s.physical_size == 1_000  # ...but memory is still held (the documented trade-off)
    with pytest.raises(EmptyQueueError):
        s.next_request()
    assert s.physical_size == 0  # the failed dispatch purged every stale entry


def test_dispatch_skips_a_long_run_of_cancelled_entries_to_reach_a_live_one() -> None:
    s = FifoScheduler()
    for i in range(500):
        s.submit("x", request_id=f"dead-{i}")
    s.submit("live", request_id="live")
    for i in range(500):
        s.cancel(f"dead-{i}")
    assert s.next_request().request_id == "live"


def test_generated_ids_are_unique_and_deterministic_when_injected(
    id_factory: Callable[[], str],
) -> None:
    s = PriorityScheduler(id_factory=id_factory)
    assert [s.submit("w").request_id for _ in range(3)] == ["req-1", "req-2", "req-3"]
    default = PriorityScheduler()
    generated = {default.submit("w").request_id for _ in range(1_000)}
    assert len(generated) == 1_000


def test_submission_time_comes_from_the_injected_clock(clock: FakeClock) -> None:
    s = FifoScheduler(clock=clock)
    assert [s.submit("w").submitted_at for _ in range(3)] == [0.0, 1.0, 2.0]


def test_metadata_is_a_deep_read_only_snapshot() -> None:
    s = PriorityScheduler()
    original: dict[str, Any] = {"tags": ["a"], "user": "alice"}
    request = s.submit("w", metadata=original)
    original["tags"].append("mutated-later")
    original["user"] = "mallory"
    assert request.metadata == {"tags": ["a"], "user": "alice"}
    with pytest.raises(TypeError):
        request.metadata["user"] = "x"  # type: ignore[index]


def test_request_is_immutable() -> None:
    request = PriorityScheduler().submit("w")
    with pytest.raises(AttributeError):
        request.priority = 0  # type: ignore[misc]


def test_requests_are_hashable_despite_carrying_metadata() -> None:
    request = PriorityScheduler().submit("w", metadata={"k": [1]})
    assert hash(request) == hash(request)
