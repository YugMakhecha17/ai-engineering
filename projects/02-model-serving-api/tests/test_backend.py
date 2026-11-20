import pytest
from model_serving import ModelBackend, SimulatedBackend


def test_output_is_deterministic_and_respects_max_tokens() -> None:
    backend = SimulatedBackend()
    first = list(backend.generate("hello", 5))
    assert first == list(backend.generate("hello", 5))
    assert len(first) == 5
    assert first != list(backend.generate("hello!", 5))  # depends on the prompt


def test_generation_is_a_lazy_stream() -> None:
    stream = SimulatedBackend().generate("p", 1_000_000)
    assert [next(stream) for _ in range(3)] == ["bravo", "charlie", "delta"]


def test_invalid_max_tokens_fails_at_call_time_not_first_token() -> None:
    with pytest.raises(ValueError):
        SimulatedBackend().generate("p", 0)


def test_per_token_delay_uses_the_injected_sleep_not_real_time() -> None:
    slept: list[float] = []
    backend = SimulatedBackend(per_token_delay_s=0.05, sleep=slept.append)
    assert len(list(backend.generate("x", 4))) == 4
    assert slept == [0.05] * 4


def test_no_sleep_when_delay_is_zero() -> None:
    slept: list[float] = []
    list(SimulatedBackend(sleep=slept.append).generate("x", 3))
    assert slept == []


def test_simulated_backend_satisfies_the_protocol_that_real_engines_must_implement() -> None:
    backend: ModelBackend = SimulatedBackend(name="sim-1")  # checked statically by mypy
    assert backend.name == "sim-1"
