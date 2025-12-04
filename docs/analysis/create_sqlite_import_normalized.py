import json
import sqlite3
import os
import datetime

project_root = r"C:\Users\diogo\projects\To_Exercises"
report_path = os.path.join(project_root, r"docs\analysis\import-dry-run-report-2025-12-02.json")
db_path = os.path.join(project_root, r"docs\analysis\exercises-normalized.sqlite")
log_path = os.path.join(project_root, r"docs\analysis\import-log-2025-12-03-normalized.json")

with open(report_path, 'r', encoding='utf-8') as f:
    report = json.load(f)

conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Create tables
cur.execute('''
CREATE TABLE IF NOT EXISTS exercises (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    exercise_id TEXT,
    file_path TEXT,
    checksum TEXT,
    folder TEXT,
    rel_folder TEXT,
    metadata_file TEXT,
    status TEXT,
    provenance TEXT,
    added_at TEXT
)
''')
# Unique constraint for resolved files: file_path + checksum
cur.execute('CREATE UNIQUE INDEX IF NOT EXISTS ux_file_checksum_norm ON exercises(file_path, checksum)')
cur.execute('CREATE INDEX IF NOT EXISTS ix_exercise_id_norm ON exercises(exercise_id)')
conn.commit()

inserted_resolved = 0
inserted_auto = 0
skipped_existing = 0
skipped_solution = 0
skipped_backup = 0
warnings = []

now = lambda: datetime.datetime.now().isoformat()

def is_solution(basename):
    return basename.lower().endswith('_solution') or basename.lower().endswith('solution')

def is_backup(basename):
    return '.agentfix' in basename or 'bak_agent' in basename or basename.lower().endswith('.backup')

for entry in report.get('summary_by_folder', []):
    folder = entry.get('folder')
    rel = entry.get('rel_folder')
    mfile = entry.get('metadata_file')
    # resolved
    for r in entry.get('resolved_exercises', []):
        fpath = r.get('file_path')
        chk = r.get('checksum')
        if not fpath:
            continue
        basename = os.path.splitext(os.path.basename(fpath))[0]
        # Skip solution files entirely per choice B
        if is_solution(basename):
            skipped_solution += 1
            continue
        # Skip backup/agentfix files entirely
        if is_backup(basename):
            skipped_backup += 1
            continue
        # canonical id from basename
        canonical = basename
        # check existing by file_path+checksum
        cur.execute('SELECT id, exercise_id FROM exercises WHERE file_path=? AND checksum=?', (fpath, chk))
        row = cur.fetchone()
        if row:
            skipped_existing += 1
            existing_exid = row[1]
            if existing_exid and existing_exid != canonical:
                warnings.append({'type': 'exercise_id_mismatch', 'file_path': fpath, 'existing_exercise_id': existing_exid, 'new_exercise_id': canonical})
            continue
        cur.execute('''INSERT INTO exercises (exercise_id, file_path, checksum, folder, rel_folder, metadata_file, status, provenance, added_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (canonical, fpath, chk, folder, rel, mfile, 'resolved', 'normalized-import', now()))
        inserted_resolved += 1
    # missing / auto-added
    for exid in entry.get('missing_exercises', []):
        # skip if already exists
        cur.execute('SELECT id FROM exercises WHERE exercise_id=? AND (file_path IS NULL OR file_path="")', (exid,))
        if cur.fetchone():
            skipped_existing += 1
            continue
        cur.execute('''INSERT INTO exercises (exercise_id, file_path, checksum, folder, rel_folder, metadata_file, status, provenance, added_at)
                       VALUES (?, NULL, NULL, ?, ?, ?, ?, ?, ?)''',
                    (exid, folder, rel, mfile, 'auto-added', 'auto-repair', now()))
        inserted_auto += 1

conn.commit()
cur.execute('SELECT COUNT(*) FROM exercises')
total_rows = cur.fetchone()[0]

log = {
    'generated_at': now(),
    'db_path': db_path,
    'inserted_resolved': inserted_resolved,
    'inserted_auto_added': inserted_auto,
    'skipped_existing': skipped_existing,
    'skipped_solution_files': skipped_solution,
    'skipped_backup_files': skipped_backup,
    'total_rows_after': total_rows,
    'warnings': warnings
}

with open(log_path, 'w', encoding='utf-8') as lf:
    json.dump(log, lf, indent=2, ensure_ascii=False)

print('Normalized import complete. DB written to', db_path)
print('Import log written to', log_path)

conn.close()
