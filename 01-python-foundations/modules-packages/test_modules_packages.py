import subprocess
import sys
from pathlib import Path

import inventory_pkg
import pytest
from inventory_pkg import Inventory, Item
from inventory_pkg.report import render

PACKAGE_PARENT = Path(__file__).parent


def test_public_api_is_declared_by_dunder_all() -> None:
    assert sorted(inventory_pkg.__all__) == ["Inventory", "Item"]


def test_relative_and_absolute_imports_resolve_to_the_same_objects() -> None:
    from inventory_pkg import models, service

    assert vars(service)["Item"] is models.Item is Item  # `from .models import Item`
    assert inventory_pkg.Inventory is service.Inventory


def test_inventory_accumulates_and_reports_in_sorted_order() -> None:
    inv = Inventory()
    inv.add("widget", 3)
    inv.add("gadget", 1)
    inv.add("widget", 2)
    assert inv.quantity("widget") == 5
    assert inv.quantity("missing") == 0
    assert render(inv) == "gadget: 1\nwidget: 5"


def test_inventory_rejects_non_positive_quantities() -> None:
    with pytest.raises(ValueError):
        Inventory().add("widget", 0)


def test_importing_the_entry_module_does_not_run_main(capsys: pytest.CaptureFixture[str]) -> None:
    import importlib

    importlib.import_module("inventory_pkg.__main__")
    assert capsys.readouterr().out == ""  # the __main__ guard prevented execution


def test_python_dash_m_runs_the_package_entry_point() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "inventory_pkg"],
        cwd=PACKAGE_PARENT,
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout.splitlines() == ["gadget: 1", "widget: 5"]


def test_running_a_package_module_as_a_script_breaks_relative_imports() -> None:
    script = PACKAGE_PARENT / "inventory_pkg" / "service.py"
    result = subprocess.run(
        [sys.executable, str(script)], capture_output=True, text=True, check=False
    )
    assert result.returncode != 0
    assert "attempted relative import with no known parent package" in result.stderr
