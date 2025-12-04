import os, json, shutil, datetime, sqlite3

root = r"C:\Users\diogo\projects\To_Exercises"
arch_index = os.path.join(root, 'docs', 'analysis', 'archived-files-2025-12-03.json')
db_path = os.path.join(root, 'docs', 'analysis', 'exercises-normalized.sqlite')

# backup DB
ts = datetime.datetime.now().strftime('%Y%m%dT%H%M%S')
backup_path = db_path + f'.bak.{ts}'
shutil.copy2(db_path, backup_path)

with open(arch_index, 'r', encoding='utf-8') as f:
    idx = json.load(f)
moved = idx.get('moved', [])

# collect basenames
basenames = set()
orig_map = {}
for it in moved:
    orig = it.get('orig_path')
    bn = os.path.basename(orig)
    basenames.add(bn)
    orig_map[bn] = orig

conn = sqlite3.connect(db_path)
cur = conn.cursor()
# ensure columns
try:
    cur.execute("ALTER TABLE exercises ADD COLUMN archived_at TEXT")
except Exception:
    pass
try:
    cur.execute("ALTER TABLE exercises ADD COLUMN archived_from TEXT")
except Exception:
    pass
conn.commit()

# build selection
patterns = ["%agentfix%", "%bak_agent%", "%_solution%", "%solution%"]
# also add basenames patterns
for bn in basenames:
    patterns.append('%' + bn)

# find affected rows
params = tuple(patterns)
# build SQL with many ORs
sql = 'SELECT id, exercise_id, file_path FROM exercises WHERE ' + ' OR '.join(['file_path LIKE ?' for _ in patterns])
cur.execute(sql, params)
rows = cur.fetchall()

updated = []
now = datetime.datetime.now().isoformat()
for r in rows:
    rid, exid, fpath = r
    archived_from = None
    bn = os.path.basename(fpath) if fpath else ''
    if bn in orig_map:
        archived_from = orig_map[bn]
    else:
        # try to match any archive basename contained in fpath
        for ab in basenames:
            if ab and ab in (fpath or ''):
                archived_from = orig_map.get(ab)
                break
    if not archived_from:
        archived_from = 'pattern-match'
    cur.execute('UPDATE exercises SET status=?, provenance=?, archived_at=?, archived_from=? WHERE id=?', ('archived','archived', now, archived_from, rid))
    updated.append({'id': rid, 'exercise_id': exid, 'file_path': fpath, 'archived_from': archived_from})

conn.commit()
log = {
    'generated_at': now,
    'db_path': db_path,
    'backup_path': backup_path,
    'updated_count': len(updated),
    'updated_rows': updated[:100]
}
log_path = os.path.join(root, 'docs', 'analysis', 'mark-archived-pattern-log-2025-12-03.json')
with open(log_path, 'w', encoding='utf-8') as f:
    json.dump(log, f, indent=2, ensure_ascii=False)

print('Updated', len(updated), 'rows. Log at', log_path)
conn.close()
