from fastapi import FastAPI
from .database import init_db
from .api.v1.exercises import router as exercises_router

app = FastAPI(title="To_Exercises API")

app.include_router(exercises_router)

@app.on_event("startup")
def on_startup():
    # Initialize DB tables if not present (safe for dev)
    init_db()
