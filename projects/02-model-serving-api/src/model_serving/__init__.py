"""model_serving: backend abstraction for the model-serving API (API layer not yet built)."""

from .backend import ModelBackend, SimulatedBackend

__all__ = ["ModelBackend", "SimulatedBackend"]
