from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from ...database import get_session
from ... import crud
from ...models import Exercise

router = APIRouter(prefix="/v1/exercises", tags=["exercises"])

@router.post("/", response_model=Exercise)
def create_exercise(payload: Exercise, session: Session = Depends(get_session)):
    # Upsert by checksum
    if not payload.checksum:
        raise HTTPException(status_code=400, detail="checksum required")
    ex = crud.upsert_by_checksum(session, checksum=payload.checksum, checksum_algorithm=payload.checksum_algorithm, file_path=payload.file_path, tags_json=payload.tags_json if hasattr(payload, 'tags_json') else None, metadata_json=payload.metadata_json if hasattr(payload, 'metadata_json') else None)
    return ex

@router.get("/{exercise_id}", response_model=Exercise)
def read_exercise(exercise_id: int, session: Session = Depends(get_session)):
    ex = crud.get_exercise(session, exercise_id)
    if not ex:
        raise HTTPException(status_code=404, detail="not found")
    return ex

@router.get("/", response_model=List[Exercise])
def list_exercises(limit: int = 50, offset: int = 0, session: Session = Depends(get_session)):
    return crud.list_exercises(session, limit=limit, offset=offset)
