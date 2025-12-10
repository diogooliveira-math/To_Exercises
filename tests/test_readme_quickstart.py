def test_readme_quickstart_contains_commands():
    import pathlib

    readme = pathlib.Path("README.md").read_text(encoding="utf-8")

    # Common dev commands
    assert "pip install -e .[dev]" in readme
    assert "uvicorn to_exercises.main:app --reload" in readme

    # Windows variants (cmd and PowerShell)
    assert ".venv\\Scripts\\activate" in readme or ".venv\\Scripts\\Activate.ps1" in readme

    # Unix variant
    assert "source .venv/bin/activate" in readme or "source .venv/bin/activate" in readme
