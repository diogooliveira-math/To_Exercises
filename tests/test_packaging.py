import importlib
import os
import tomllib


def test_src_layout_has_package_init():
    assert os.path.exists(os.path.join("src", "to_exercises", "__init__.py")), "src/to_exercises/__init__.py must exist"


def test_pyproject_configures_src_find():
    with open("pyproject.toml", "rb") as f:
        data = tomllib.load(f)
    where = data.get("tool", {}).get("setuptools", {}).get("packages", {}).get("find", {}).get("where")
    assert where and "src" in where, "pyproject.toml must configure setuptools.packages.find.where to include 'src'"


def test_import_package_available():
    # Attempt to import the package by name
    mod = importlib.import_module("to_exercises")
    assert hasattr(mod, "main") or hasattr(mod, "__main__"), "to_exercises package should expose entry points (main or __main__)"
