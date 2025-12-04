import sqlite3, shutil, os, json, datetime
root = r"C:\Users\diogo\projects\To_Exercises"
db_path = os.path.join(root, 'docs', 'analysis', 'exercises-normalized.sqlite')
arch_index = os.path.join(root, 'docs', 'analysis', 'archived-files-2025-12-03.json')

# backup DB
ts = datetime.datetime.now().strftime('%Y%m%dT%H%M%S')
backup_path = db_path + f'.bak.{ts}'
shutil.copy2(db_path, backup_path)

with open(arch_index, 'r', encoding='utf-8') as f:
    idx = json.load(f)

moved = idx.get('moved', [])

conn = sqlite3.connect(db_path)
cur = conn.cursor()
# add columns if not present
try:
    cur.execute("ALTER TABLE exercises ADD COLUMN archived_at TEXT")
except Exception:
    pass
try:
    cur.execute("ALTER TABLE exercises ADD COLUMN archived_from TEXT")
except Exception:
    pass
conn.commit()

updated = []
for item in moved:
    orig = item.get('orig_path')
    # compute relative path as stored in DB
    rel = os.path.relpath(orig, root)
    # normalize backslashes
    rel = rel.replace('/', '\\')
    # update rows where file_path equals rel
    now = datetime.datetime.now().isoformat()
    cur.execute('SELECT id, exercise_id FROM exercises WHERE file_path = ?', (rel,))
    rows = cur.fetchall()
    if not rows:
        continue
    ids = [r[0] for r in rows]
    exids = [r[1] for r in rows]
    cur.execute('UPDATE exercises SET status = ?, provenance = ?, archived_at = ?, archived_from = ? WHERE file_path = ?', ('archived', 'archived', now, orig, rel))
    updated.append({'orig_path': orig, 'rel_path': rel, 'row_ids': ids, 'exercise_ids': exids})

conn.commit()
log = {
    'generated_at': datetime.datetime.now().isoformat(),
    'db_path': db_path,
    'backup_path': backup_path,
    'updated_count': len(updated),
    'details': updated
}
log_path = os.path.join(root, 'docs', 'analysis', 'mark-archived-log-2025-12-03.json')
with open(log_path, 'w', encoding='utf-8') as f:
    json.dump(log, f, indent=2, ensure_ascii=False)

print('Updated', len(updated), 'file entries. Log at', log_path)
conn.close()
