# Claims register

The repository rule ([ADR 0001](decisions/0001-evidence-rule.md)):

> Every important technical claim must be supported by an explanation, an implementation, a test,
> or a reliable reference.

This register lists the claims that matter most and points to their evidence. It is verified by
`python scripts/check_evidence.py` (also `make evidence`, and CI).

## How to read a row
| Evidence kind | Meaning | What the checker verifies |
|---------------|---------|----------------------------|
| `test:path::test_name` | A test asserts the claim | File exists, is `test_*.py`, defines that `test_*` function |
| `impl:path::Symbol` | The claim is implemented here | File exists and defines the class or function |
| `doc:path[::Heading]` | An explanation or recorded measurement | File exists (and heading text, for `.md`) |
| `ref:https://...` | An external primary source | The URL is `https` (reachability is **not** checked) |

A claim with only `doc:` or `ref:` evidence is **weak**: allowed by the rule, reported as a warning,
and a candidate for a test or implementation. The checker proves evidence *exists*, not that it is
*sufficient*; sufficiency is a review judgement.

## Adding a claim
Add a row with the next free ID in the same commit as its evidence. Claims about performance must cite
a result file whose `data_kind` and environment are recorded.

## Python foundations

| ID | Claim | Evidence |
|----|-------|----------|
| C-001 | Assigning a list to a second name creates an alias: mutation through one name is visible through the other. | `test:01-python-foundations/mutability/test_mutability.py::test_alias_shares_identity_and_mutation_is_visible_through_both_names`<br>`impl:01-python-foundations/mutability/mutability_demo.py::append_in_place`<br>`ref:https://docs.python.org/3/reference/datamodel.html` |
| C-002 | `copy.copy` shares nested objects with the original; `copy.deepcopy` isolates them. | `test:01-python-foundations/mutability/test_mutability.py::test_shallow_copy_shares_nested_lists`<br>`test:01-python-foundations/mutability/test_mutability.py::test_deep_copy_isolates_nested_lists`<br>`ref:https://docs.python.org/3/library/copy.html` |
| C-003 | A mutable default argument is created once and persists across calls. | `test:01-python-foundations/mutability/test_mutability.py::test_mutable_default_argument_persists_across_calls`<br>`impl:01-python-foundations/mutability/mutability_demo.py::safe_collect` |
| C-004 | `[row] * n` repeats one row object, so writing to one row changes all of them. | `test:01-python-foundations/mutability/test_mutability.py::test_multiplied_rows_are_one_object` |
| C-005 | Closures capture variables, not values: closures created in a loop all see the final value unless the value is bound. | `test:01-python-foundations/functions/test_scope_and_functions.py::test_late_binding_closures_all_see_the_final_loop_value`<br>`test:01-python-foundations/functions/test_scope_and_functions.py::test_default_argument_binding_captures_each_value` |
| C-006 | Assigning to a name anywhere in a function makes it local for the whole function (UnboundLocalError on earlier reads). | `test:01-python-foundations/functions/test_scope_and_functions.py::test_assigning_to_a_name_makes_it_local_for_the_whole_function` |
| C-007 | `bool` passes `isinstance(x, int)`, so integer validation must reject it explicitly. | `test:01-python-foundations/exceptions/test_request_validation.py::test_bool_is_rejected_even_though_it_is_an_int_subclass`<br>`impl:01-python-foundations/exceptions/request_validation.py::_require_int` |
| C-008 | `raise ... from exc` preserves the original exception as `__cause__`. | `test:01-python-foundations/exceptions/test_request_validation.py::test_exception_chaining_preserves_original_cause`<br>`ref:https://peps.python.org/pep-3134/` |
| C-009 | Generators are lazy: creating one runs no code and only requested items are produced. | `test:01-python-foundations/iterators-generators/test_generators.py::test_generators_are_lazy_only_requested_items_are_produced`<br>`ref:https://docs.python.org/3/reference/expressions.html#yield-expressions` |
| C-010 | A generator function's argument validation is deferred to the first `next()`; validating in a wrapper makes it eager. | `test:01-python-foundations/iterators-generators/test_generators.py::test_a_plain_generator_defers_validation_until_first_next`<br>`test:01-python-foundations/iterators-generators/test_generators.py::test_chunked_validates_size_eagerly` |
| C-011 | A `with` block inside a generator releases the file on exhaustion and on early `close()`. | `test:01-python-foundations/iterators-generators/test_generators.py::test_read_lines_closes_the_file_when_exhausted`<br>`test:01-python-foundations/iterators-generators/test_generators.py::test_read_lines_closes_the_file_on_early_close` |
| C-012 | A generator object's size does not depend on how many items it will yield (it is not the size of the data). | `test:01-python-foundations/iterators-generators/test_generators.py::test_generator_object_size_is_constant_while_a_list_grows` |
| C-013 | A context manager's `__exit__` runs when the body raises, and the exception still propagates. | `test:01-python-foundations/context-managers/test_resource_managers.py::test_resource_is_closed_when_the_body_raises_and_the_error_propagates`<br>`ref:https://peps.python.org/pep-0343/` |
| C-014 | `ExitStack` closes already-opened resources, in reverse order, when a later acquisition fails. | `test:01-python-foundations/context-managers/test_resource_managers.py::test_exit_stack_cleans_up_partial_acquisition_on_failure`<br>`test:01-python-foundations/context-managers/test_resource_managers.py::test_exit_stack_closes_everything_opened_in_reverse_order` |
| C-015 | The `__main__` guard prevents `main()` from running on import; `python -m package` runs the package entry point. | `test:01-python-foundations/modules-packages/test_modules_packages.py::test_importing_the_entry_module_does_not_run_main`<br>`test:01-python-foundations/modules-packages/test_modules_packages.py::test_python_dash_m_runs_the_package_entry_point`<br>`ref:https://docs.python.org/3/library/__main__.html` |
| C-016 | Running a module inside a package directly as a script breaks its relative imports. | `test:01-python-foundations/modules-packages/test_modules_packages.py::test_running_a_package_module_as_a_script_breaks_relative_imports` |

## Data structures and algorithms

| ID | Claim | Evidence |
|----|-------|----------|
| C-017 | Appending to a doubling dynamic array is amortised O(1): total element copies stay below 2n. | `test:02-data-structures-algorithms/lists-arrays/test_dynamic_array.py::test_append_is_amortised_constant_total_copies_are_linear`<br>`impl:02-data-structures-algorithms/lists-arrays/dynamic_array.py::DynamicArray._grow`<br>`ref:https://wiki.python.org/moin/TimeComplexity` |
| C-018 | Inserting at the front of an array-backed list shifts every element (O(n)); appending shifts none. | `test:02-data-structures-algorithms/lists-arrays/test_dynamic_array.py::test_insert_at_front_shifts_every_element_but_append_shifts_none` |
| C-019 | Set-based duplicate detection is a single pass with early exit. | `test:02-data-structures-algorithms/sets-hashmaps/test_hash_structures.py::test_has_duplicates_stops_early_on_infinite_input`<br>`impl:02-data-structures-algorithms/sets-hashmaps/hash_structures.py::has_duplicates` |
| C-020 | A hash map stays correct under total hash collision but degrades to O(n) lookups (one chain of length n). | `test:02-data-structures-algorithms/sets-hashmaps/test_hash_structures.py::test_correct_under_total_collision_but_chains_degrade_to_linear` |
| C-021 | Resizing keeps the load factor bounded and preserves every entry. | `test:02-data-structures-algorithms/sets-hashmaps/test_hash_structures.py::test_resizing_keeps_load_factor_bounded_and_preserves_all_entries`<br>`test:02-data-structures-algorithms/sets-hashmaps/test_hash_structures.py::test_behaviour_matches_dict_under_random_operations` |
| C-022 | `1`, `True` and `1.0` are the same dictionary key because they are equal and hash equally. | `test:02-data-structures-algorithms/sets-hashmaps/test_hash_structures.py::test_equal_hash_and_equality_define_key_identity_like_dict` |
| C-023 | Dequeuing from the front of a list (`list.pop(0)`) is O(n); `collections.deque.popleft` is O(1). Measured: 2,657 ms vs 1.1 ms at n = 50,000 on one machine. | `impl:02-data-structures-algorithms/queues-deques/fifo_queues.py::ListQueue`<br>`impl:02-data-structures-algorithms/queues-deques/fifo_queues.py::DequeQueue`<br>`doc:benchmarks/results/queue-pop.json`<br>`doc:benchmarks/queue_pop_benchmark.py`<br>`ref:https://wiki.python.org/moin/TimeComplexity`<br>`ref:https://docs.python.org/3/library/collections.html#collections.deque` |
| C-024 | A ring-buffer queue reuses its array by wrapping indexes and grows correctly even when the head is not at index 0. | `test:02-data-structures-algorithms/queues-deques/test_fifo_queues.py::test_ring_buffer_wraps_around_without_growing`<br>`test:02-data-structures-algorithms/queues-deques/test_fifo_queues.py::test_ring_buffer_grows_correctly_when_head_is_not_at_zero` |
| C-025 | The hand-written ring buffer is slower than C-implemented `deque` (measured about 18x at n = 50,000); it is a teaching implementation. | `impl:benchmarks/queue_pop_benchmark.py::drain_ring`<br>`doc:benchmarks/results/queue-pop.json`<br>`doc:02-data-structures-algorithms/queues-deques/README.md` |
| C-026 | Heap push costs at most floor(log2 n) comparisons. | `test:02-data-structures-algorithms/heaps-priority-queues/test_binary_heap.py::test_push_costs_at_most_log2_n_comparisons`<br>`impl:02-data-structures-algorithms/heaps-priority-queues/binary_heap.py::BinaryHeap._sift_up` |
| C-027 | Heap pop costs at most 2*floor(log2 n) comparisons. | `test:02-data-structures-algorithms/heaps-priority-queues/test_binary_heap.py::test_pop_costs_at_most_two_log2_n_comparisons`<br>`impl:02-data-structures-algorithms/heaps-priority-queues/binary_heap.py::BinaryHeap._sift_down` |
| C-028 | Building a heap from n items with bottom-up heapify takes at most 2n comparisons (linear, not n log n). | `test:02-data-structures-algorithms/heaps-priority-queues/test_binary_heap.py::test_heapify_is_linear_not_n_log_n` |
| C-029 | A bare binary heap does not preserve arrival order for equal priorities; a sequence-number tie-breaker restores it. | `test:02-data-structures-algorithms/heaps-priority-queues/test_binary_heap.py::test_heap_alone_is_not_stable_for_equal_priorities`<br>`test:02-data-structures-algorithms/heaps-priority-queues/test_binary_heap.py::test_stable_priority_queue_keeps_arrival_order_within_a_priority`<br>`ref:https://docs.python.org/3/library/heapq.html` |
| C-030 | Binary search needs at most floor(log2 n) + 1 probes. | `test:02-data-structures-algorithms/complexity-analysis/test_searching_sorting.py::test_binary_search_never_exceeds_floor_log2_n_plus_1_probes` |
| C-031 | Binary search on unsorted input can miss a present element (the sortedness precondition is real). | `test:02-data-structures-algorithms/complexity-analysis/test_searching_sorting.py::test_binary_search_gives_a_wrong_answer_if_the_precondition_is_violated` |
| C-032 | Insertion sort is linear on sorted input and quadratic on reversed input. | `test:02-data-structures-algorithms/complexity-analysis/test_searching_sorting.py::test_insertion_sort_best_and_worst_case_comparison_counts` |
| C-033 | Merge sort uses at most n*ceil(log2 n) comparisons. | `test:02-data-structures-algorithms/complexity-analysis/test_searching_sorting.py::test_merge_sort_comparison_count_is_bounded_by_n_log_n` |
| C-034 | A sliding-window-log rate limiter uses memory bounded by its limit regardless of traffic. | `test:02-data-structures-algorithms/problem-solving/test_sliding_window.py::test_memory_is_bounded_by_limit_regardless_of_traffic` |
| C-035 | Not recording rejected requests means a client that keeps retrying is released as soon as old accepted requests expire. | `test:02-data-structures-algorithms/problem-solving/test_sliding_window.py::test_rejected_requests_are_not_recorded` |

## Software engineering and SQL

| ID | Claim | Evidence |
|----|-------|----------|
| C-036 | Type hints are not enforced at runtime, but a static checker rejects the violating call. | `test:03-software-engineering/type-safety/test_typed_predictors.py::test_type_hints_are_not_enforced_at_runtime`<br>`test:03-software-engineering/type-safety/test_typed_predictors.py::test_mypy_rejects_what_runtime_accepts`<br>`ref:https://peps.python.org/pep-0484/` |
| C-037 | A Protocol lets unrelated classes satisfy an interface without inheritance. | `test:03-software-engineering/type-safety/test_typed_predictors.py::test_structural_typing_accepts_unrelated_classes_with_the_right_method`<br>`ref:https://peps.python.org/pep-0544/` |
| C-038 | In a duration grammar `5ms` must be read as milliseconds, not minutes plus seconds; the regex order and a test pin this. | `test:03-software-engineering/testing/test_duration_parser.py::test_ms_is_milliseconds_not_minutes_plus_seconds`<br>`impl:03-software-engineering/testing/duration_parser.py::parse_duration` |
| C-039 | A regression test pins the off-by-one that drops the final moving-average window. | `test:03-software-engineering/debugging/test_moving_average.py::test_regression_last_window_is_included`<br>`test:03-software-engineering/debugging/test_moving_average.py::test_matches_naive_recomputation` |
| C-040 | `WHERE` filters rows before grouping, so it changes what an aggregate is computed over. | `test:05-backend-distributed-systems/databases-postgresql/test_where_vs_group_by.py::test_where_runs_before_grouping_so_it_changes_what_is_averaged`<br>`ref:https://www.postgresql.org/docs/current/tutorial-agg.html` |
| C-041 | `HAVING` filters groups after aggregation; an aggregate in `WHERE` is an error. | `test:05-backend-distributed-systems/databases-postgresql/test_where_vs_group_by.py::test_having_filters_groups_after_aggregation`<br>`test:05-backend-distributed-systems/databases-postgresql/test_where_vs_group_by.py::test_aggregate_in_where_is_a_syntax_error_because_it_does_not_exist_yet`<br>`ref:https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-GROUP` |

## Project 01: request scheduling engine

| ID | Claim | Evidence |
|----|-------|----------|
| C-042 | Heap-based priority scheduling serves equal-priority requests in arrival order. | `test:projects/01-request-scheduling-engine/tests/test_scheduler_ordering.py::test_equal_priorities_are_served_in_arrival_order`<br>`test:projects/01-request-scheduling-engine/tests/test_scheduler_ordering.py::test_stability_holds_for_interleaved_submits_and_dispatches`<br>`impl:projects/01-request-scheduling-engine/src/request_scheduler/scheduler.py::PriorityScheduler` |
| C-043 | Both schedulers behave identically to a brute-force reference under thousands of random submit/dispatch/cancel/complete operations. | `test:projects/01-request-scheduling-engine/tests/test_scheduler_model_based.py::test_scheduler_matches_brute_force_reference` |
| C-044 | Cancellation is O(1) via lazy deletion; stale entries hold memory until they surface at dispatch (stated trade-off). | `test:projects/01-request-scheduling-engine/tests/test_scheduler_lifecycle.py::test_lazy_deletion_leaves_stale_entries_until_they_surface`<br>`impl:projects/01-request-scheduling-engine/src/request_scheduler/scheduler.py::Scheduler.cancel` |
| C-045 | A cancelled queued request is never dispatched. | `test:projects/01-request-scheduling-engine/tests/test_scheduler_lifecycle.py::test_cancelled_queued_request_is_never_dispatched` |
| C-046 | Terminal request states are final and invalid transitions are rejected without changing state. | `test:projects/01-request-scheduling-engine/tests/test_scheduler_lifecycle.py::test_terminal_states_are_final`<br>`test:projects/01-request-scheduling-engine/tests/test_scheduler_lifecycle.py::test_cannot_complete_a_request_that_never_started`<br>`doc:docs/architecture/diagrams/request-lifecycle.md` |
| C-047 | A rejected submission leaves the scheduler unchanged. | `test:projects/01-request-scheduling-engine/tests/test_scheduler_lifecycle.py::test_failed_submit_leaves_no_trace` |
| C-048 | Request IDs are never reused, even after completion or cancellation. | `test:projects/01-request-scheduling-engine/tests/test_scheduler_lifecycle.py::test_duplicate_ids_are_rejected_even_after_the_request_finished` |
| C-049 | Request metadata is a deep, read-only snapshot unaffected by later caller mutation. | `test:projects/01-request-scheduling-engine/tests/test_scheduler_lifecycle.py::test_metadata_is_a_deep_read_only_snapshot` |
| C-050 | Priority must be a true int: bool and float are rejected. | `test:projects/01-request-scheduling-engine/tests/test_scheduler_validation.py::test_priority_must_be_a_real_int_not_bool_or_float` |
| C-051 | The documented example produces exactly the output shown in the README. | `test:projects/01-request-scheduling-engine/tests/test_example_output.py::test_example_runs_and_prints_the_documented_output` |
| C-052 | Measured on one machine, priority scheduling costs more per request than FIFO and the gap widens with n (5.72 vs 2.60 microseconds at n = 100,000). Not a proof of growth rate. | `impl:projects/01-request-scheduling-engine/benchmarks/bench_schedulers.py::run`<br>`doc:benchmarks/results/request-scheduler.json`<br>`doc:projects/01-request-scheduling-engine/README.md::Benchmarks` |
| C-053 | Starvation of low-priority requests is possible and is not mitigated (stated limitation, demonstrated by a test). | `test:projects/01-request-scheduling-engine/tests/test_scheduler_ordering.py::test_sustained_urgent_traffic_starves_a_low_priority_request`<br>`doc:projects/01-request-scheduling-engine/README.md::Known limitations`<br>`doc:02-data-structures-algorithms/heaps-priority-queues/README.md::Engineering trade-offs and limitations` |

## Projects 02 and 03

| ID | Claim | Evidence |
|----|-------|----------|
| C-054 | The simulated backend is deterministic, streams lazily and takes an injected sleep so tests never wait. | `test:projects/02-model-serving-api/tests/test_backend.py::test_generation_is_a_lazy_stream`<br>`test:projects/02-model-serving-api/tests/test_backend.py::test_per_token_delay_uses_the_injected_sleep_not_real_time`<br>`test:projects/02-model-serving-api/tests/test_backend.py::test_output_is_deterministic_and_respects_max_tokens` |
| C-055 | Nearest-rank percentile arithmetic must be exact: float rounding (0.07*100 > 7) would shift the rank. | `test:projects/03-inference-observability/tests/test_metrics.py::test_float_error_does_not_shift_the_rank`<br>`impl:projects/03-inference-observability/src/inference_observability/metrics.py::percentile` |
| C-056 | With few samples, P99 equals the maximum and carries almost no information. | `test:projects/03-inference-observability/tests/test_metrics.py::test_small_sample_tail_percentiles_collapse_to_the_maximum` |
| C-057 | One outlier among 100 samples moves the mean but neither P50 nor nearest-rank P99; only the maximum shows it. | `test:projects/03-inference-observability/tests/test_metrics.py::test_one_outlier_moves_p99_and_mean_but_not_the_median` |

## Tooling

| ID | Claim | Evidence |
|----|-------|----------|
| C-058 | The evidence checker rejects claims without evidence, missing files, missing symbols and non-test `test:` pointers. | `test:scripts/test_check_evidence.py::test_claim_without_evidence_is_an_error`<br>`test:scripts/test_check_evidence.py::test_missing_symbol_is_an_error`<br>`test:scripts/test_check_evidence.py::test_test_evidence_must_name_a_test_function`<br>`doc:docs/decisions/0001-evidence-rule.md` |
| C-059 | The test suite detects 18 deliberately injected bugs covering scheduler ordering, heap correctness, resource cleanup, validation and percentile arithmetic; one equivalent mutant is documented and excluded. | `impl:scripts/mutation_spot_check.py::run_mutation`<br>`doc:scripts/README.md` |

## External references (reference-only evidence, the weakest kind)

| ID | Claim | Evidence |
|----|-------|----------|
| C-060 | Orca's iteration-level scheduling lets a newly arrived request be considered after a single model iteration instead of waiting for a whole batch to finish. | `ref:https://www.usenix.org/conference/osdi22/presentation/yu`<br>`doc:07-ai-infrastructure/README.md` |
| C-061 | PagedAttention stores the KV cache in non-contiguous paged blocks, inspired by operating-system virtual memory, to reduce waste and enable sharing. | `ref:https://arxiv.org/abs/2309.06180`<br>`doc:07-ai-infrastructure/README.md` |

