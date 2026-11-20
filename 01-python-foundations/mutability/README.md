# Mutability, references and copying

Code: [`mutability_demo.py`](mutability_demo.py) · Tests: [`test_mutability.py`](test_mutability.py)

## 1. Problem
Two parts of a program share a list and one changes it; the other sees data change underneath it.
In a server, one request mutating a "default" object silently corrupts the next request.

## 2. First-principles explanation
A Python variable is a *name bound to an object*, not a box holding a value. `b = a` binds a second
name to the **same** object. Lists, dicts and sets can be changed in place (mutable); ints, strings
and tuples cannot (immutable). Mutating through any name is visible through every name.

## 3. Technical details
* `is` compares identity; `==` compares value.
* `copy.copy` copies the container only (**shallow**); nested objects stay shared. `copy.deepcopy`
  copies recursively and keeps internal sharing consistent via a memo table.
* Default argument values are evaluated **once**, when `def` executes, so a mutable default is
  shared by every call.
* `[row] * n` repeats one reference; a comprehension builds distinct rows.
* `lst += x` mutates in place; `tup += x` rebinds the name to a new tuple.

## 4. Runnable implementation
`mutability_demo.py` has paired buggy/fixed functions: `buggy_collect`/`safe_collect`,
`grid_aliased`/`grid_independent`, `shallow_copy`/`deep_copy`. Run `python mutability_demo.py`.

## 5. Expected behaviour
```text
a=[1, 2, 3, 4] b=[1, 2, 3, 4] same object: True
buggy: ['x'] then ['x', 'y']
safe:  ['x'] then ['y']
```

## 6. Tests
Normal: identity, non-mutating function. Pitfalls demonstrated: shallow copy leak, shared default,
aliased grid, tuple containing a list, `+=` semantics, deepcopy memo behaviour.

## 7. Engineering trade-offs
Mutating in place is cheap but creates hidden coupling; returning new objects is safer but allocates.
Deep copies cost O(size of object graph) and can be surprising for objects holding resources
(sockets, locks). Prefer immutable data (frozen dataclasses, tuples) at API boundaries.

## 8. AI-infrastructure connection
Request metadata, sampling parameters and batch buffers are shared between pipeline stages.
Project 01 deep-copies metadata into a read-only mapping so later caller mutations cannot change a
queued request (`test_metadata_is_a_deep_read_only_snapshot`).

## 9. Common mistakes
Mutable default arguments; `[[0]*c]*r`; believing `copy.copy` isolates nested data; mutating a list
while iterating it; assuming a tuple is deeply immutable.

## 10. References
* Python data model: <https://docs.python.org/3/reference/datamodel.html>
* `copy` module: <https://docs.python.org/3/library/copy.html>
* Function definitions (default evaluation): <https://docs.python.org/3/reference/compound_stmts.html#function-definitions>
