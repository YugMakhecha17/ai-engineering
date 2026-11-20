"""Static typing in practice: Protocols, generics and frozen dataclasses.

`Predictor` is the same kind of seam used later by the model-serving project: callers
depend on a behaviour, not on a concrete class.

Provenance: reference implementation written with AI assistance (see docs/progress-tracker.md).
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Generic, Protocol, TypeVar


class Predictor(Protocol):
    """Anything with a compatible `predict` method qualifies; no inheritance needed."""

    def predict(self, features: Sequence[float]) -> float: ...


@dataclass(frozen=True)
class LinearModel:
    weights: tuple[float, ...]
    bias: float = 0.0

    def predict(self, features: Sequence[float]) -> float:
        if len(features) != len(self.weights):
            raise ValueError(f"expected {len(self.weights)} features, got {len(features)}")
        return sum(w * x for w, x in zip(self.weights, features, strict=True)) + self.bias


@dataclass(frozen=True)
class ConstantModel:
    value: float

    def predict(self, features: Sequence[float]) -> float:
        return self.value


def predict_batch(model: Predictor, batch: Sequence[Sequence[float]]) -> list[float]:
    return [model.predict(row) for row in batch]


M = TypeVar("M", bound=Predictor)


class UnknownModelError(LookupError):
    pass


class ModelRegistry(Generic[M]):
    """A registry typed by what it stores: ModelRegistry[LinearModel].get() -> LinearModel."""

    def __init__(self) -> None:
        self._models: dict[str, M] = {}

    def register(self, name: str, model: M) -> None:
        if name in self._models:
            raise ValueError(f"model {name!r} is already registered")
        self._models[name] = model

    def get(self, name: str) -> M:
        try:
            return self._models[name]
        except KeyError:
            raise UnknownModelError(f"unknown model: {name!r}") from None

    def names(self) -> list[str]:
        return sorted(self._models)
