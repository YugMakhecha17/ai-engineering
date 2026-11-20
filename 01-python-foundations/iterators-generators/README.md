# Iterators, generators and lazy evaluation

Code: [`generators_demo.py`](generators_demo.py) · Tests: [`test_generators.py`](test_generators.py)

## 1. Problem
Processing a large or unbounded stream (a log file, a token stream) by building a full list first
wastes memory or never finishes.

## 2. First-principles explanation
A `for` loop calls `iter(x)` to get an iterator, then calls `next()` until `StopIteration`. A
**generator function** (any function containing `yield`) returns an iterator that runs its body
only as far as the next `yield` each time `next()` is called, then pauses with its locals intact.

## 3. Technical details
* **Iterable** (`__iter__` returns a new iterator each time, so it can be replayed) vs **iterator**
  (`__next__`, exhausted after one pass).
* Generators are lazy: creating one runs no code; each item is produced on demand.
* A `with` block inside a generator is released when the generator finishes, is `.close()`d, or is
  garbage-collected.
* A generator function's body, including argument validation, does not run until the first
  `next()`. To validate eagerly, validate in a normal function that returns the generator
  (`chunked` does this).

## 4. Runnable implementation
`Countdown`/`CountdownIterable`, `chunked`, `read_lines`, `take`, `running_total`, `non_blank`.

## 5. Expected behaviour
```python
>>> list(chunked(range(7), 3))
[[0, 1, 2], [3, 4, 5], [6]]
>>> list(take(itertools.count(), 3))
[0, 1, 2]
```

## 6. Tests
Exhaustion vs replay; laziness proven with a side-effect log (only requested items produced); an
infinite source; file closed on exhaustion and on early `close()` (on Windows `unlink()` would fail
otherwise); eager vs deferred validation; constant generator object size.

## 7. Engineering trade-offs
Generators give O(1) memory and early termination but are single-use, cannot be indexed or
measured with `len`, and make errors surface late. Use a list when you need random access or
several passes.

## 8. AI-infrastructure connection
Streaming token output, micro-batching a request stream (`chunked`) and reading datasets larger than
memory are all generator patterns. `ModelBackend.generate` in project 02 is specified as an
iterator of tokens for this reason.

## 9. Common mistakes
Iterating an exhausted generator twice; assuming validation ran at call time; holding a generator
open and never closing it; `sys.getsizeof(gen)` is not the memory of the data it will produce.

## 10. References
* Iterators and generators: <https://docs.python.org/3/tutorial/classes.html#iterators>
* Yield expressions: <https://docs.python.org/3/reference/expressions.html#yield-expressions>
* PEP 255, simple generators: <https://peps.python.org/pep-0255/>
