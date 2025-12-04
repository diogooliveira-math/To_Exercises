from typing import Generator
from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///./dev.db"

_engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

def get_engine():
    return _engine

def init_db():
    SQLModel.metadata.create_all(_engine)

def get_session() -> Generator[Session, None, None]:
    with Session(_engine) as session:
        yield session
