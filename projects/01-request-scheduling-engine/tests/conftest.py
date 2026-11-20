import itertools
from collections.abc import Callable

import pytest


class FakeClock:
    """Deterministic clock: advances by `step` on every reading."""

    def __init__(self, step: float = 1.0) -> None:
        self._t = itertools.count()
        self._step = step

    def __call__(self) -> float:
        return next(self._t) * self._step


@pytest.fixture
def clock() -> FakeClock:
    return FakeClock()


@pytest.fixture
def id_factory() -> Callable[[], str]:
    counter = itertools.count(1)
    return lambda: f"req-{next(counter)}"
