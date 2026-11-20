"""Context managers and resource lifecycle management.

Provenance: reference implementation written with AI assistance (see docs/progress-tracker.md).
"""

from __future__ import annotations

import time
from collections.abc import Callable, Iterator, MutableMapping
from contextlib import ExitStack, contextmanager
from types import TracebackType
from typing import Any, Literal


class ResourceClosedError(RuntimeError):
    """Raised when a closed resource is used."""


class ManagedResource:
    """A resource with an explicit lifecycle: created -> open -> closed.

    `events` records every lifecycle transition, which makes resource-management
    behaviour directly assertable in tests.
    """

    def __init__(self, name: str, log: list[str] | None = None) -> None:
        self.name = name
        self.state = "created"
        self._log = log if log is not None else []

    @property
    def events(self) -> list[str]:
        return self._log

    def open(self) -> ManagedResource:
        if self.state != "created":
            raise RuntimeError(f"{self.name}: cannot open from state {self.state!r}")
        self.state = "open"
        self._log.append(f"open:{self.name}")
        return self

    def close(self) -> None:
        """Idempotent: closing twice is safe, which keeps cleanup code simple."""
        if self.state == "closed":
            return
        self.state = "closed"
        self._log.append(f"close:{self.name}")

    def read(self) -> str:
        if self.state != "open":
            raise ResourceClosedError(f"{self.name} is {self.state}")
        return f"data from {self.name}"

    def __enter__(self) -> ManagedResource:
        return self.open()

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> Literal[False]:
        self.close()  # runs on success AND on exceptions
        return False  # never swallow exceptions implicitly


@contextmanager
def timed(
    label: str,
    sink: MutableMapping[str, float],
    clock: Callable[[], float] = time.perf_counter,
) -> Iterator[None]:
    """Record elapsed time even if the body raises (try/finally around the yield)."""
    start = clock()
    try:
        yield
    finally:
        sink[label] = clock() - start


@contextmanager
def temporary_setting(config: dict[str, Any], key: str, value: Any) -> Iterator[None]:
    """Override a setting for the duration of a block, then restore the previous state."""
    missing = object()
    previous = config.get(key, missing)
    config[key] = value
    try:
        yield
    finally:
        if previous is missing:
            del config[key]
        else:
            config[key] = previous


def read_all(names: list[str], log: list[str], fail_on: str | None = None) -> list[str]:
    """Open a variable number of resources; ExitStack closes them in reverse order.

    If opening one fails, those already opened are still closed.
    """
    with ExitStack() as stack:
        resources = []
        for name in names:
            if name == fail_on:
                raise RuntimeError(f"cannot open {name}")
            resources.append(stack.enter_context(ManagedResource(name, log)))
        return [r.read() for r in resources]
