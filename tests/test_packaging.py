def test_import_package():
    import importlib

    # Attempt to import the package by name
    importlib.import_module("to_exercises")

    # Basic attribute check
    from to_exercises import __version__
    assert isinstance(__version__, str)
