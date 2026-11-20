"""The model-backend seam: the one interface a real inference engine must satisfy.

Everything above this boundary (API, scheduler, metrics) depends only on `ModelBackend`.
`SimulatedBackend` is a deterministic stand-in so the rest of the system can be built and
tested without a GPU. IT IS NOT A MODEL: its output is meaningless, and any timing involving
it must be labelled "simulated" (see benchmarks/methodology.md).
"""

from __future__ import annotations

import time
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from typing import Protocol

_VOCAB = ("alpha", "bravo", "charlie", "delta", "echo", "foxtrot", "golf", "hotel")


class ModelBackend(Protocol):
    name: str

    def generate(self, prompt: str, max_tokens: int) -> Iterator[str]:
        """Yield generated tokens one at a time (streaming-friendly by construction)."""
        ...


@dataclass
class SimulatedBackend:
    """Deterministic fake: token i is `_VOCAB[(len(prompt) + i) % len(_VOCAB)]`."""

    name: str = "simulated"
    per_token_delay_s: float = 0.0
    sleep: Callable[[float], None] = time.sleep

    def generate(self, prompt: str, max_tokens: int) -> Iterator[str]:
        if max_tokens < 1:
            raise ValueError("max_tokens must be >= 1")
        return self._stream(prompt, max_tokens)

    def _stream(self, prompt: str, max_tokens: int) -> Iterator[str]:
        for i in range(max_tokens):
            if self.per_token_delay_s > 0:
                self.sleep(self.per_token_delay_s)
            yield _VOCAB[(len(prompt) + i) % len(_VOCAB)]
