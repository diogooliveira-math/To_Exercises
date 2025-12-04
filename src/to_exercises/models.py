from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

class Exercise(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    checksum: str = Field(index=True)
    checksum_algorithm: str = Field(default="sha256")
    file_path: str
    parent_exercise_id: Optional[int] = Field(default=None, foreign_key="exercise.id")
    tags_json: Optional[str] = None  # JSON-serialized list
    metadata_json: Optional[str] = None  # JSON-serialized dict
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ExerciseChecksumHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    exercise_id: int = Field(foreign_key="exercise.id")
    checksum: str
    file_path: str
    recorded_at: datetime = Field(default_factory=datetime.utcnow)
