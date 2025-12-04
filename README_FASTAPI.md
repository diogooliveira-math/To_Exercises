To_Exercises FastAPI service

Quickstart

1. Create a virtualenv and install requirements:

   python -m venv .venv
   .venv\Scripts\activate    (Windows)
   pip install -r requirements.txt

2. Run the app:

   uvicorn to_exercises.main:app --reload

3. API endpoints:
   - POST /exercises
   - GET /exercises/{id}
   - PUT /exercises/{id}
   - DELETE /exercises/{id}
   - GET /exercises?tag=...&difficulty_min=...&module=...

4. Run tests:
   pytest
