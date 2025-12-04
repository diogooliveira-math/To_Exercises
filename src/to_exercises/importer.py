import os
import json
import hashlib
from typing import List
from sqlmodel import Session
from .database import get_session
from .models import Exercise


def compute_checksum(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def discover_exercises_from_folder(folder_path: str) -> List[str]:
    matches = []
    for root, dirs, files in os.walk(folder_path):
        for f in files:
            if f.endswith('.tex') or f.endswith('.md'):
                matches.append(os.path.join(root, f))
    return matches


def load_file_content(path: str) -> str:
    with open(path, 'r', encoding='utf-8', errors='ignore') as fh:
        return fh.read()


def dry_run_import(folder_path: str, session: Session) -> dict:
    """Discover files and report anomalies without writing to DB."""
    files = discover_exercises_from_folder(folder_path)
    report = {
        'total_files': len(files),
        'anomalies': [],
        'discovered': []
    }
    for p in files:
        content = load_file_content(p)
        checksum = compute_checksum(content)
        # naive metadata extraction: title from filename
        title = os.path.splitext(os.path.basename(p))[0]
        # check for existing checksum using SQLModel select
        from sqlmodel import select
        stmt = select(Exercise).where(Exercise.checksum == checksum)
        existing = session.exec(stmt).first()
        if existing:
            report['anomalies'].append({'path': p, 'issue': 'duplicate_checksum', 'checksum': checksum})
            continue
        report['discovered'].append({'path': p, 'title': title, 'checksum': checksum})
    return report


def import_folder(folder_path: str, session: Session) -> dict:
    files = discover_exercises_from_folder(folder_path)
    report = {
        'total_files': len(files),
        'imported': 0,
        'errors': []
    }
    for p in files:
        try:
            content = load_file_content(p)
            checksum = compute_checksum(content)
            title = os.path.splitext(os.path.basename(p))[0]
            # Persist minimal metadata only; do not store full content in DB for MVP
            ex = Exercise(checksum=checksum, checksum_algorithm='sha256', file_path=p)
            session.add(ex)
            session.commit()
            # append history entry
            try:
                from .models import ExerciseChecksumHistory
                history = ExerciseChecksumHistory(exercise_id=ex.id, checksum=checksum, file_path=p)
                session.add(history)
                session.commit()
            except Exception:
                session.rollback()
            report['imported'] += 1
        except Exception as e:
            session.rollback()
            report['errors'].append({'path': p, 'error': str(e)})
    return report
