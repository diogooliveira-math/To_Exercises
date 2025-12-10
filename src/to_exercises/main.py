from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database import init_db
from .api.v1.exercises import router as exercises_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB tables on startup (safe for dev)
    init_db()
    try:
        yield
    finally:
        # Place shutdown logic here if needed
        pass

app = FastAPI(title="To_Exercises API", lifespan=lifespan)

app.include_router(exercises_router)
