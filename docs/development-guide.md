# Development Guide (generated)

## Quickstart

1. Create and activate virtual environment:

   python -m venv .venv
   .venv\Scripts\activate   # Windows

2. Install dependencies:

   pip install -e .[dev]

3. Initialize database (dev):

   python -c "from to_exercises.database import init_db; init_db()"

4. Run the app locally:

   uvicorn src.to_exercises.main:app --reload --port 8000

5. Run tests:

   pytest -q

## Notes

- Tests use an in-memory SQLite engine (see tests/conftest.py). Ensure tests run against clean DB state.
- CI (GitHub Actions) runs pytest on push to main (see .github/workflows/ci.yml).
- To generate PDFs locally, run the generator CLI (if LaTeX installed) or use preview mode.
