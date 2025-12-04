from typing import List, Optional
from sqlmodel import Session, select
from .models import Exercise, ExerciseChecksumHistory
from datetime import datetime

def create_exercise(session: Session, exercise: Exercise) -> Exercise:
    session.add(exercise)
    session.commit()
    session.refresh(exercise)
    return exercise

def get_exercise(session: Session, exercise_id: int) -> Optional[Exercise]:
    return session.get(Exercise, exercise_id)

def list_exercises(session: Session, limit: int = 50, offset: int = 0) -> List[Exercise]:
    stmt = select(Exercise).limit(limit).offset(offset)
    results = list(session.exec(stmt))
    return results

def upsert_by_checksum(session: Session, *, checksum: str, checksum_algorithm: str = "sha256", **fields) -> Exercise:
    stmt = select(Exercise).where(Exercise.checksum == checksum, Exercise.checksum_algorithm == checksum_algorithm)
    existing = session.exec(stmt).first()
    now = datetime.utcnow()
    if existing:
        # Update fields
        for k, v in fields.items():
            if hasattr(existing, k):
                setattr(existing, k, v)
        existing.updated_at = now
        session.add(existing)
        session.commit()
        # append history if file_path changed
        if "file_path" in fields and fields["file_path"] != existing.file_path:
            history = ExerciseChecksumHistory(exercise_id=existing.id, checksum=checksum, file_path=fields.get("file_path", existing.file_path))
            session.add(history)
            session.commit()
        session.refresh(existing)
        return existing
    else:
        ex = Exercise(checksum=checksum, checksum_algorithm=checksum_algorithm, **fields, created_at=now, updated_at=now)
        session.add(ex)
        session.commit()
        session.refresh(ex)
        # create history entry
        history = ExerciseChecksumHistory(exercise_id=ex.id, checksum=checksum, file_path=ex.file_path)
        session.add(history)
        session.commit()
        return ex
