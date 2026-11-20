# Lists and dynamic arrays

Code: [`dynamic_array.py`](dynamic_array.py) · Tests: [`test_dynamic_array.py`](test_dynamic_array.py)

## 1. Problem
Contiguous storage gives fast indexing, but its size is fixed when allocated. How can a list grow
without making every append expensive?

## 2. First-principles explanation
Allocate a block with spare capacity. Appending fills a spare slot (cheap). When full, allocate a
larger block and copy everything across (expensive, but rare). Growing by a constant *factor*
(doubling) makes the copies add up to about as many as the elements appended.

## 3. Technical details
* Index, set: O(1). `append`: O(1) **amortised**, O(n) in the worst single call.
* `insert(i, x)` and `pop(i)`: O(n − i) because later elements shift.
* Doubling: total copies for n appends < 2n. Growing by a constant *amount* instead would be
  O(n²) in total (not implemented; follows from the arithmetic series).
* CPython's `list` is a dynamic array with a smaller, irregular growth factor; this module uses a
  clean factor of 2 so the argument is exact.

## 4. Runnable implementation
`DynamicArray` with counters `element_copies`, `element_shifts`, `resizes`. It stores data in a
pre-sized Python list as a stand-in for a raw memory block, since Python has no fixed arrays.

## 5. Expected behaviour
```python
>>> arr = DynamicArray(); [arr.append(i) for i in range(100)]
>>> arr.capacity, arr.element_copies
(128, 124)            # 4+8+16+32+64 copies in five resizes
>>> arr.insert(0, -1); arr.element_shifts
100
```

## 6. Tests
Index and negative index; out-of-range; capacity sequence 4→128; total copies < 2n for n = 10,
1,000, 100,000; front insert shifts n elements; end pop shifts none; stale reference cleared; seeded
comparison against `list` under 2,000 random operations; invalid parameters.

## 7. Engineering trade-offs
Doubling wastes up to half the memory and has latency spikes at resize time; a smaller factor wastes
less but copies more often. For frequent front insertion or removal use a deque, not a list.

## 8. AI-infrastructure connection
Pre-allocating a buffer and tracking a fill level is exactly how token buffers and KV-cache blocks
are managed; resize spikes are a real source of tail latency, which is why serving systems
pre-allocate.

## 9. Common mistakes
Using a list as a queue; inserting in a loop at index 0; assuming "O(1) append" means every append
is cheap.

## 10. References
* Python time complexity table: <https://wiki.python.org/moin/TimeComplexity>
* Lists tutorial: <https://docs.python.org/3/tutorial/datastructures.html#more-on-lists>
