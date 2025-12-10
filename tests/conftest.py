import pytest
from sqlmodel import SQLModel, create_engine, Session
from fastapi.testclient import TestClient
from to_exercises.main import app
import to_exercises.database as db
import to_exercises.models as models  # ensure models are imported so SQLModel metadata is populated

@pytest.fixture(name="engine")
def engine_fixture():
    """Create a temporary SQLite file engine and override application engine for tests"""
    # Use a file-backed SQLite DB so the TestClient and endpoints share the same schema across connections
    engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
    # Ensure schema exists on test engine
    SQLModel.metadata.create_all(engine)
    # Override the application's engine so endpoints use the test DB
    db._engine = engine
    # Recreate tables on the overridden engine to be safe
    SQLModel.metadata.create_all(db._engine)
    return engine

@pytest.fixture
def client(engine):
    """FastAPI TestClient fixture that depends on engine to ensure DB override before app startup"""
    return TestClient(app)
