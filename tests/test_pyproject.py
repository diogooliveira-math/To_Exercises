def test_pyproject_packages_find():
    import tomllib
    import pathlib
    import importlib

    data = tomllib.loads(pathlib.Path("pyproject.toml").read_text(encoding="utf-8"))

    # Verify setuptools dynamic package discovery configured for src/ layout
    assert "tool" in data and "setuptools" in data["tool"]
    packages_cfg = data["tool"]["setuptools"].get("packages")
    assert packages_cfg is not None
    assert "find" in packages_cfg and "where" in packages_cfg["find"]
    assert "src" in packages_cfg["find"]["where"]

    # Also ensure package is importable
    importlib.import_module("to_exercises")
