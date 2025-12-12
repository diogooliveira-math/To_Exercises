from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List, Dict
from sqlalchemy.exc import IntegrityError
from ...database import get_session
from ... import crud
from ...models import Exercise

router = APIRouter(prefix="/v1/exercises", tags=["exercises"])

@router.post("/", response_model=Exercise)
def create_exercise(payload: Exercise, session: Session = Depends(get_session)):
    # Upsert by checksum
    if not payload.checksum:
        raise HTTPException(status_code=400, detail="checksum required")
    try:
        ex = crud.upsert_by_checksum(
            session,
            checksum=payload.checksum,
            checksum_algorithm=payload.checksum_algorithm,
            file_path=getattr(payload, "file_path", None),
            tags_json=getattr(payload, "tags_json", None),
            metadata_json=getattr(payload, "metadata_json", None),
        )
    except IntegrityError as e:
        # Represent checksum conflict as a 409 with structured payload
        raise HTTPException(status_code=409, detail={"error": "checksum_conflict", "message": "Exercise with same checksum exists"})

    # Return pydantic model for FastAPI to serialize cleanly
    if hasattr(Exercise, "model_validate"):
        return Exercise.model_validate(ex)
    else:
        return Exercise.from_orm(ex)

@router.get("/{exercise_id}", response_model=Exercise)
def read_exercise(exercise_id: int, session: Session = Depends(get_session)):
    ex = crud.get_exercise(session, exercise_id)
    if not ex:
        raise HTTPException(status_code=404, detail="not found")
    if hasattr(Exercise, "model_validate"):
        return Exercise.model_validate(ex)
    else:
        return Exercise.from_orm(ex)

@router.get("/")
def list_exercises(limit: int = 50, offset: int = 0, session: Session = Depends(get_session)) -> Dict:
    items = crud.list_exercises(session, limit=limit, offset=offset)
    total = len(items)
    return {"items": items, "limit": limit, "offset": offset, "total": total}

@router.put("/{exercise_id}", response_model=Exercise)
def update_exercise(exercise_id: int, payload: Exercise, session: Session = Depends(get_session)):
    ex = crud.get_exercise(session, exercise_id)
    if not ex:
        raise HTTPException(status_code=404, detail="not found")
    # Update allowed fields
    update_fields = ["file_path", "tags_json", "metadata_json"]
    for f in update_fields:
        if hasattr(payload, f):
            setattr(ex, f, getattr(payload, f))
    # update checksum fields only if provided
    if getattr(payload, "checksum", None):
        ex.checksum = payload.checksum
    if getattr(payload, "checksum_algorithm", None):
        ex.checksum_algorithm = payload.checksum_algorithm
    session.add(ex)
    session.commit()
    session.refresh(ex)
    if hasattr(Exercise, "model_validate"):
        return Exercise.model_validate(ex)
    else:
        return Exercise.from_orm(ex)

@router.delete("/{exercise_id}")
def delete_exercise(exercise_id: int, session: Session = Depends(get_session)):
    ex = crud.get_exercise(session, exercise_id)
    if not ex:
        raise HTTPException(status_code=404, detail="not found")
    session.delete(ex)
    session.commit()
    return {"status": "deleted", "id": exercise_id}
