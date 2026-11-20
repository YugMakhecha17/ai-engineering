# Modules, packages and imports

Code: [`inventory_pkg/`](inventory_pkg/) · Tests: [`test_modules_packages.py`](test_modules_packages.py)

## 1. Problem
Code beyond one file needs structure: reusable units, a public API, and a defined way to run it.

## 2. First-principles explanation
A module is a `.py` file; a package is a directory of modules with an `__init__.py`. `import x`
finds the module via `sys.path`, executes it once, and caches it in `sys.modules`. Every module has
a `__name__`: `"__main__"` when run as the program, its dotted path when imported.

## 3. Technical details
* Absolute import (`from inventory_pkg.service import Inventory`) names the full path.
  Relative import (`from .models import Item`) is resolved against the module's own package.
* `__init__.py` defines the package's public API (`__all__`). Keep it free of side effects.
* `python -m package` runs `package/__main__.py` with the package context intact.
* `if __name__ == "__main__":` keeps import free of side effects.
* Running a file *inside* a package directly (`python inventory_pkg/service.py`) loses the package
  context and breaks relative imports.

## 4. Runnable implementation
`inventory_pkg/` with `models.py`, `service.py`, `report.py`, `__main__.py`.

## 5. Expected behaviour
```text
$ cd 01-python-foundations/modules-packages
$ python -m inventory_pkg
gadget: 1
widget: 5
```

## 6. Tests
Public API and `__all__`; relative and absolute imports resolve to the same objects; importing
`__main__` does not run `main()`; `python -m` output; running a package module as a script fails with
the documented `ImportError`.

## 7. Engineering trade-offs
Relative imports survive renaming the package but cannot be used from scripts; absolute imports are
clearer but couple a module to the package name. Re-exporting in `__init__` gives a tidy API at the
cost of import-time work.

## 8. AI-infrastructure connection
Serving projects are packages with an entry point (`python -m model_serving`); consistent layout
makes them testable, containerisable and installable. The three projects here follow the
`src/<package>` layout.

## 9. Common mistakes
Circular imports; shadowing standard-library names (`queue.py`, `copy.py`); depending on the current
working directory; heavy work at import time.

## 10. References
* Modules tutorial: <https://docs.python.org/3/tutorial/modules.html>
* Import system: <https://docs.python.org/3/reference/import.html>
* `__main__`: <https://docs.python.org/3/library/__main__.html>
