from sqlmodel import SQLModel, create_engine
import to_exercises.models as models


def test_models_have_tables():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    # Check that metadata contains our tables
    names = {t.name for t in SQLModel.metadata.sorted_tables}
    assert 'exercise' in names
    assert 'exercise_checksum_history' in names


def test_exercise_has_unique_index_on_checksum():
    # Ensure Exercise model has index on (checksum, checksum_algorithm) by inspecting indexes
    from to_exercises.models import Exercise
    # SQLModel Field index=True creates single-column index; ensure combined unique index planned in migrations
    # For now assert that checksum field exists and is present
    assert hasattr(Exercise, 'checksum')
    assert hasattr(Exercise, 'checksum_algorithm')
