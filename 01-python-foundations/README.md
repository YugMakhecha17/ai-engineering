# 01 · Python foundations

The language mechanics that later systems code depends on: object references, scope, failure
handling, laziness, resource cleanup and imports.

| Topic | Code | Tests | Why it matters for infrastructure |
|-------|------|-------|-----------------------------------|
| [Mutability](mutability/) | `mutability_demo.py` | `test_mutability.py` | Shared state between requests; defensive copies |
| [Functions](functions/) | `scope_and_functions.py` | `test_scope_and_functions.py` | Pure functions, closures, callbacks |
| [Exceptions](exceptions/) | `request_validation.py` | `test_request_validation.py` | Boundary validation, error taxonomies |
| [Iterators and generators](iterators-generators/) | `generators_demo.py` | `test_generators.py` | Streaming tokens, batching, bounded memory |
| [Context managers](context-managers/) | `resource_managers.py` | `test_resource_managers.py` | Connection, lock and GPU-buffer lifecycles |
| [Modules and packages](modules-packages/) | `inventory_pkg/` | `test_modules_packages.py` | Project structure, entry points |

Run this section: `python -m pytest 01-python-foundations`

**Provenance.** Implementations are AI-assisted reference material and do not raise any status in the
[progress tracker](../docs/progress-tracker.md). Unresolved exercises E-01 to E-04 apply here.

Not yet covered in this section: shallow-vs-deep copy of custom classes (`__copy__`),
`__slots__`, descriptors, decorators. Type hints and unit-testing strategy live in
[03-software-engineering](../03-software-engineering/).
