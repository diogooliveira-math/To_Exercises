from sqlmodel import SQLModel, create_engine, Session
from to_exercises.models import Exercise
from to_exercises import crud


def test_upsert_creates_and_appends_history():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        # create initial record
        ex = crud.upsert_by_checksum(session, checksum="abc123", checksum_algorithm="sha256", file_path="/path/a.txt", title="A")
        assert ex.id is not None
        # update with same checksum but different file_path
        ex2 = crud.upsert_by_checksum(session, checksum="abc123", checksum_algorithm="sha256", file_path="/path/b.txt", title="A")
        assert ex2.id == ex.id
        # Verify history rows exist
        from sqlalchemy import text
        histories = session.exec(text("SELECT * FROM exercise_checksum_history")).all()
        assert len(histories) >= 1
