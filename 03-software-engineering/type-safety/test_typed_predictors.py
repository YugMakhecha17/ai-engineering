import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path

import pytest
from typed_predictors import (
    ConstantModel,
    LinearModel,
    ModelRegistry,
    Predictor,
    UnknownModelError,
    predict_batch,
)


def test_linear_model_predicts_and_validates_feature_count() -> None:
    model = LinearModel(weights=(2.0, 3.0), bias=1.0)
    assert model.predict([1.0, 2.0]) == 9.0
    with pytest.raises(ValueError, match="expected 2 features"):
        model.predict([1.0])


def test_structural_typing_accepts_unrelated_classes_with_the_right_method() -> None:
    class Doubler:  # inherits from nothing
        def predict(self, features: Sequence[float]) -> float:
            return 2 * sum(features)

    model: Predictor = Doubler()
    assert predict_batch(model, [[1.0, 2.0], [3.0]]) == [6.0, 6.0]


def test_predict_batch_works_with_any_predictor() -> None:
    assert predict_batch(ConstantModel(7.0), [[1.0], [2.0], []]) == [7.0, 7.0, 7.0]
    assert predict_batch(LinearModel((1.0,)), []) == []


def test_frozen_dataclass_rejects_mutation() -> None:
    model = ConstantModel(1.0)
    with pytest.raises(AttributeError):
        model.value = 2.0  # type: ignore[misc]


def test_registry_register_get_and_errors() -> None:
    registry: ModelRegistry[LinearModel] = ModelRegistry()
    registry.register("a", LinearModel((1.0,)))
    assert registry.get("a").weights == (1.0,)
    assert registry.names() == ["a"]
    with pytest.raises(ValueError, match="already registered"):
        registry.register("a", LinearModel((2.0,)))
    with pytest.raises(UnknownModelError):
        registry.get("zzz")


def test_unknown_model_error_hides_the_internal_keyerror() -> None:
    registry: ModelRegistry[ConstantModel] = ModelRegistry()
    with pytest.raises(UnknownModelError) as info:
        registry.get("x")
    assert info.value.__suppress_context__  # `from None` keeps the traceback clean


def test_type_hints_are_not_enforced_at_runtime() -> None:
    # `value: float` is only an annotation: Python stores a str without complaint...
    model = ConstantModel(value="not a float")  # type: ignore[arg-type]
    stored: object = model.predict([])
    assert stored == "not a float"


@pytest.mark.slow
def test_mypy_rejects_what_runtime_accepts(tmp_path: Path) -> None:
    """...but a static checker catches the mistake before the code ever runs."""
    snippet = tmp_path / "bad_call.py"
    snippet.write_text(
        "from collections.abc import Sequence\n"
        "def total(xs: Sequence[float]) -> float:\n"
        "    return sum(xs)\n"
        "total('not a sequence of floats')\n"
        "total(123)\n",
        encoding="utf-8",
    )
    result = subprocess.run(
        [sys.executable, "-m", "mypy", "--strict", "--no-incremental", str(snippet)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 1
    assert "arg-type" in result.stdout
