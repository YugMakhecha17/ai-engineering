import random
from collections import deque
from collections.abc import Callable

import pytest
from fifo_queues import DequeQueue, FifoQueue, ListQueue, QueueEmptyError, RingBufferQueue

FACTORIES: list[Callable[[], FifoQueue[int]]] = [ListQueue, DequeQueue, RingBufferQueue]


@pytest.fixture(params=FACTORIES, ids=["list", "deque", "ring"])
def queue(request: pytest.FixtureRequest) -> FifoQueue[int]:
    return request.param()  # type: ignore[no-any-return]


def test_items_leave_in_arrival_order(queue: FifoQueue[int]) -> None:
    for i in range(10):
        queue.enqueue(i)
    assert [queue.dequeue() for _ in range(10)] == list(range(10))


def test_interleaved_operations_preserve_order(queue: FifoQueue[int]) -> None:
    queue.enqueue(1)
    queue.enqueue(2)
    assert queue.dequeue() == 1
    queue.enqueue(3)
    assert queue.dequeue() == 2
    assert queue.dequeue() == 3
    assert len(queue) == 0


def test_dequeue_from_empty_raises(queue: FifoQueue[int]) -> None:
    with pytest.raises(QueueEmptyError):
        queue.dequeue()


def test_queue_is_reusable_after_draining(queue: FifoQueue[int]) -> None:
    queue.enqueue(1)
    queue.dequeue()
    queue.enqueue(2)
    assert queue.dequeue() == 2


def test_ring_buffer_wraps_around_without_growing() -> None:
    q: RingBufferQueue[int] = RingBufferQueue(initial_capacity=4)
    for round_number in range(100):  # head circles the array many times
        q.enqueue(round_number)
        q.enqueue(round_number + 1000)
        assert q.dequeue() == round_number
        assert q.dequeue() == round_number + 1000
    assert q.capacity == 4
    assert len(q) == 0


def test_ring_buffer_grows_correctly_when_head_is_not_at_zero() -> None:
    q: RingBufferQueue[int] = RingBufferQueue(initial_capacity=4)
    for i in range(4):
        q.enqueue(i)
    q.dequeue()
    q.dequeue()  # head == 2, buffer logically wraps once we add more
    for i in range(4, 8):
        q.enqueue(i)  # forces growth while wrapped
    assert q.capacity == 8
    assert [q.dequeue() for _ in range(len(q))] == [2, 3, 4, 5, 6, 7]


def test_ring_buffer_peek_and_reference_release() -> None:
    q: RingBufferQueue[object] = RingBufferQueue()
    sentinel = object()
    q.enqueue(sentinel)
    assert q.peek() is sentinel
    q.dequeue()
    assert all(slot is None for slot in q._buffer)
    with pytest.raises(QueueEmptyError):
        q.peek()


def test_all_implementations_match_a_reference_deque_under_random_operations() -> None:
    for factory in FACTORIES:
        rng = random.Random(7)
        mine = factory()
        reference: deque[int] = deque()
        for step in range(3_000):
            if reference and rng.random() < 0.45:
                assert mine.dequeue() == reference.popleft()
            else:
                mine.enqueue(step)
                reference.append(step)
            assert len(mine) == len(reference)
