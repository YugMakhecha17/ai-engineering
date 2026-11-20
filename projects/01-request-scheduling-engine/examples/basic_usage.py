"""Run:  python projects/01-request-scheduling-engine/examples/basic_usage.py"""

import itertools
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from request_scheduler import FifoScheduler, PriorityScheduler  # noqa: E402


def main() -> None:
    counter = itertools.count(1)
    ids = lambda: f"req-{next(counter)}"  # noqa: E731

    print("== FIFO ==")
    fifo = FifoScheduler(id_factory=ids)
    for prompt in ("summarise report", "translate memo", "classify ticket"):
        fifo.submit(prompt)
    while len(fifo):
        request = fifo.next_request()
        print(f"{request.request_id}: {request.payload}")
        fifo.complete(request.request_id)

    print("== Priority (lower number = more urgent) ==")
    counter = itertools.count(1)
    sched = PriorityScheduler(id_factory=ids)
    sched.submit("batch job", priority=5)
    sched.submit("interactive A", priority=0)
    sched.submit("interactive B", priority=0)
    cancelled = sched.submit("abandoned", priority=0)
    sched.submit("background", priority=9)
    sched.cancel(cancelled.request_id)
    print(f"queued after cancel: {len(sched)}")
    while len(sched):
        request = sched.next_request()
        print(f"{request.request_id} (p={request.priority}): {request.payload}")
        sched.complete(request.request_id)


if __name__ == "__main__":
    main()
