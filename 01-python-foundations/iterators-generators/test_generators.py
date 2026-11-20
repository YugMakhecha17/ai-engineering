import sys
from collections.abc import Iterator
from pathlib import Path

import pytest
from generators_demo import (
    Countdown,
    CountdownIterable,
    chunked,
    non_blank,
    read_lines,
    running_total,
    take,
)


def test_iterator_is_exhausted_after_one_pass() -> None:
    it = Countdown(3)
    assert list(it) == [3, 2, 1]
    assert list(it) == []  # the same object cannot be replayed


def test_iterable_can_be_traversed_repeatedly() -> None:
    iterable = CountdownIterable(3)
    assert list(iterable) == [3, 2, 1]
    assert list(iterable) == [3, 2, 1]


def test_for_loop_protocol_is_iter_then_next_until_stop_iteration() -> None:
    it = iter(Countdown(1))
    assert next(it) == 1
    with pytest.raises(StopIteration):
        next(it)


def test_chunked_groups_and_keeps_the_short_tail() -> None:
    assert list(chunked(range(7), 3)) == [[0, 1, 2], [3, 4, 5], [6]]
    assert list(chunked([], 3)) == []


def test_chunked_validates_size_eagerly() -> None:
    with pytest.raises(ValueError, match="size"):
        chunked([1, 2, 3], 0)  # raises at the call, before any iteration


def test_a_plain_generator_defers_validation_until_first_next() -> None:
    def lazy_chunks(size: int) -> Iterator[list[int]]:
        if size < 1:
            raise ValueError("size")
        yield [size]

    gen = lazy_chunks(0)  # no error yet: the body has not started running
    with pytest.raises(ValueError):
        next(gen)


def test_generators_are_lazy_only_requested_items_are_produced() -> None:
    produced: list[int] = []

    def source() -> Iterator[int]:
        for i in range(1_000_000):
            produced.append(i)
            yield i

    gen = source()
    assert produced == []  # creating the generator runs nothing
    assert next(gen) == 0
    assert next(gen) == 1
    assert produced == [0, 1]  # a million items were never materialised


def test_chunked_consumes_source_only_as_needed() -> None:
    consumed: list[int] = []

    def source() -> Iterator[int]:
        for i in range(100):
            consumed.append(i)
            yield i

    first = next(chunked(source(), 4))
    assert first == [0, 1, 2, 3]
    assert consumed == [0, 1, 2, 3]


def test_take_does_not_over_consume_an_infinite_source() -> None:
    def naturals() -> Iterator[int]:
        n = 0
        while True:
            yield n
            n += 1

    assert list(take(naturals(), 3)) == [0, 1, 2]
    assert list(take(naturals(), 0)) == []
    with pytest.raises(ValueError):
        list(take([1], -1))


def test_generator_pipeline_composes_lazily(tmp_path: Path) -> None:
    f = tmp_path / "data.txt"
    f.write_text("1\n\n2\n   \n3\n", encoding="utf-8")
    numbers = (float(line) for line in non_blank(read_lines(f)))
    assert list(running_total(numbers)) == [1.0, 3.0, 6.0]


def test_read_lines_closes_the_file_when_exhausted(tmp_path: Path) -> None:
    f = tmp_path / "data.txt"
    f.write_text("a\nb\n", encoding="utf-8")
    assert list(read_lines(f)) == ["a", "b"]
    f.unlink()  # on Windows this raises PermissionError if the handle were still open


def test_read_lines_closes_the_file_on_early_close(tmp_path: Path) -> None:
    f = tmp_path / "data.txt"
    f.write_text("a\nb\nc\n", encoding="utf-8")
    gen = read_lines(f)
    assert next(gen) == "a"
    gen.close()  # raises GeneratorExit inside the generator, unwinding the `with`
    f.unlink()


def test_exhausted_generator_cannot_be_reused() -> None:
    gen = (x for x in range(3))
    assert list(gen) == [0, 1, 2]
    assert list(gen) == []


def test_generator_object_size_is_constant_while_a_list_grows() -> None:
    small = (x * x for x in range(10))
    large = (x * x for x in range(10_000_000))
    assert sys.getsizeof(small) == sys.getsizeof(large)
    assert sys.getsizeof([x * x for x in range(10_000)]) > sys.getsizeof(small)
