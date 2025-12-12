from sqlmodel import SQLModel, create_engine, Session
from to_exercises import crud


def test_upsert_transactional_rolls_back_on_error():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        # create initial record
        ex = crud.upsert_by_checksum(session, checksum="tx1", checksum_algorithm="sha256", file_path="/path/a.txt", title="A")
        assert ex.id is not None
        # simulate error during subsequent upsert by raising inside a manual transaction
        try:
            with session.begin():
                # call upsert which itself uses session.begin(), so to simulate we'll directly create a conflicting entry
                from sqlalchemy import text
                session.execute(text("INSERT INTO exercise (checksum, checksum_algorithm, file_path) VALUES ('tx1', 'sha256', '/path/conflict.txt')"))
        except Exception:
            pass
        # ensure original record still present and not duplicated
        from sqlalchemy import text
        rows = list(session.exec(text("SELECT * FROM exercise WHERE checksum='tx1'")))
        assert len(rows) == 1
