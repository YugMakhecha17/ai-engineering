# Hash sets and hash maps

Code: [`hash_structures.py`](hash_structures.py) · Tests: [`test_hash_structures.py`](test_hash_structures.py)

## 1. Problem
Finding "have I seen this ID?" or "which request has ID X?" by scanning a list costs O(n) per query.

## 2. First-principles explanation
Compute `hash(key)`, reduce it to a bucket index (`hash % buckets`), and look only in that bucket.
Different keys can land in the same bucket (a **collision**), so each bucket's entries are compared
with `==`. If buckets stay short, lookup is O(1) on average.

## 3. Technical details
* Requirements: keys are hashable, and equal keys have equal hashes. Lists and dicts are not
  hashable.
* `ChainedHashMap` resolves collisions by chaining (a list per bucket) and doubles the table when
  the load factor exceeds 0.75, rehashing every entry (bucket index depends on table size).
* Worst case, every key collides and lookup degrades to O(n).
* `1`, `True` and `1.0` are equal and hash equally, so they are the same key, in `dict` too.
* CPython's `dict` uses open addressing, not chaining; the principle is the same, the memory layout
  and probing differ.

## 4. Runnable implementation
`has_duplicates`, `duplicates`, `find_by_id_linear` vs `index_by_id`, `ChainedHashMap`.

## 5. Expected behaviour
```python
>>> has_duplicates([1, 2, 3, 1]); duplicates([1, 2, 1, 3, 2, 1, 1])
True
[1, 2]
```

## 6. Tests
Early exit on an infinite stream; unhashable item raises `TypeError`; dict index equals linear scan;
overwrite, delete, missing key; load factor ≤ 0.75 across 1,000 inserts with all entries preserved;
total-collision keys still correct but longest chain = 50; `1 == True == 1.0` key identity;
5,000 seeded random operations compared with `dict`.

## 7. Engineering trade-offs: dict vs list for finding a request by ID
| | list of requests | dict keyed by ID |
|---|---|---|
| Lookup by ID | O(n) scan | O(1) expected |
| Preserves arrival order | Yes | Yes (insertion-ordered since 3.7) |
| Extra memory | None | Hash table overhead |
| Needs hashable, stable IDs | No | Yes |
| Range / ordered queries | Easy if sorted | Not supported |

Use a list for a few items or when order and ranges matter; a dict once lookups dominate. Project 01
keeps a dict of records for this reason and a separate ordering structure for dispatch order.

## 8. AI-infrastructure connection
Request tables, prompt-prefix caches, model registries and idempotency-key stores are hash maps.
Poorly distributed or adversarial keys are a known denial-of-service vector, one reason CPython
randomises string hashes per process.

## 9. Common mistakes
Using mutable objects as keys; relying on `hash()` values being stable between runs; assuming O(1) is
guaranteed rather than expected; mutating a dict while iterating it.

## 10. References
* Data model, `__hash__`: <https://docs.python.org/3/reference/datamodel.html#object.__hash__>
* `dict` and mapping types: <https://docs.python.org/3/library/stdtypes.html#mapping-types-dict>
* Time complexity table: <https://wiki.python.org/moin/TimeComplexity>
