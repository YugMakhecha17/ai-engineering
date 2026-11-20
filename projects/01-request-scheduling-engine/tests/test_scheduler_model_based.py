"""Model-based test: compare each scheduler to a brute-force reference.

The reference keeps live requests in a plain dict and picks the next one by scanning for
the minimum key. It is deliberately slow and obviously correct. Thousands of seeded random
operations (submit / next / cancel / complete) must produce identical behaviour.
"""

import random
from collections.abc import Callable
from typing import Any

import pytest
from request_scheduler import (
    EmptyQueueError,
    FifoScheduler,
    PriorityScheduler,
    RequestState,
    Scheduler,
)


@pytest.mark.parametrize(
    ("scheduler_cls", "key"),
    [
        (FifoScheduler, lambda priority, seq: seq),
        (PriorityScheduler, lambda priority, seq: (priority, seq)),
    ],
    ids=["fifo", "priority"],
)
@pytest.mark.parametrize("seed", range(5))
def test_scheduler_matches_brute_force_reference(
    scheduler_cls: type[Scheduler],
    key: Callable[[int, int], Any],
    seed: int,
) -> None:
    rng = random.Random(seed)
    scheduler = scheduler_cls()
    queued: dict[str, tuple[int, int]] = {}  # id -> (priority, seq)
    running: set[str] = set()
    states: dict[str, RequestState] = {}
    seq = 0

    for _ in range(3_000):
        action = rng.choices(
            ["submit", "next", "cancel_queued", "cancel_running", "complete"],
            weights=[40, 25, 12, 5, 18],
        )[0]

        if action == "submit":
            priority = rng.randint(-2, 3)
            rid = f"r{seq}"
            scheduler.submit(f"p{seq}", priority=priority, request_id=rid)
            queued[rid] = (priority, seq)
            states[rid] = RequestState.QUEUED
            seq += 1

        elif action == "next":
            if queued:
                expected = min(queued, key=lambda r: key(*queued[r]))
                assert scheduler.next_request().request_id == expected
                del queued[expected]
                running.add(expected)
                states[expected] = RequestState.RUNNING
            else:
                with pytest.raises(EmptyQueueError):
                    scheduler.next_request()

        elif action == "cancel_queued" and queued:
            rid = rng.choice(sorted(queued))
            scheduler.cancel(rid)
            del queued[rid]
            states[rid] = RequestState.CANCELLED

        elif action == "cancel_running" and running:
            rid = rng.choice(sorted(running))
            scheduler.cancel(rid)
            running.remove(rid)
            states[rid] = RequestState.CANCELLED

        elif action == "complete" and running:
            rid = rng.choice(sorted(running))
            scheduler.complete(rid)
            running.remove(rid)
            states[rid] = RequestState.COMPLETED

        assert len(scheduler) == len(queued)

    assert all(scheduler.get_state(rid) is state for rid, state in states.items())
