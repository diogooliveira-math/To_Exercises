import sqlite3, shutil, os, datetime, json

project_root = r"C:\Users\diogo\projects\To_Exercises"
db_path = os.path.join(project_root, r"docs\analysis\exercises-normalized.sqlite")
# backup
ts = datetime.datetime.now().strftime('%Y%m%dT%H%M%S')
backup_path = db_path + f'.bak.{ts}'
shutil.copy2(db_path, backup_path)

conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Find exercise_ids that have at least one placeholder (file_path IS NULL, status='auto-added')
cur.execute("SELECT DISTINCT exercise_id FROM exercises WHERE file_path IS NULL AND status='auto-added'")
placeholders = [r[0] for r in cur.fetchall()]
merged = []
skipped = []
actions = []
for exid in placeholders:
    # find resolved rows for this exid
    cur.execute("SELECT id, exercise_id, file_path, checksum, folder, rel_folder, metadata_file, status, provenance, added_at FROM exercises WHERE exercise_id=? AND file_path IS NOT NULL", (exid,))
    resolved_rows = cur.fetchall()
    if not resolved_rows:
        skipped.append(exid)
        continue
    # pick first resolved row to keep
    keep = resolved_rows[0]
    keep_id = keep[0]
    keep_file_path = keep[2]
    # find all placeholder rows
    cur.execute("SELECT id, folder, rel_folder, metadata_file, added_at FROM exercises WHERE exercise_id=? AND (file_path IS NULL OR file_path='') AND status='auto-added'", (exid,))
    ph_rows = cur.fetchall()
    # merge metadata from placeholders into keep if missing
    updates = {}
    for ph in ph_rows:
        ph_id, ph_folder, ph_rel, ph_meta, ph_added = ph
        # update folder/rel_folder/metadata_file if keep has null/empty
        cur.execute('SELECT folder, rel_folder, metadata_file FROM exercises WHERE id=?', (keep_id,))
        kfolder, krel, kmeta = cur.fetchone()
        if (not kfolder) and ph_folder:
            updates['folder'] = ph_folder
        if (not krel) and ph_rel:
            updates['rel_folder'] = ph_rel
        if (not kmeta) and ph_meta:
            updates['metadata_file'] = ph_meta
    # apply updates
    if updates:
        set_clause = ', '.join(f"{k}=?" for k in updates.keys())
        params = list(updates.values()) + [keep_id]
        cur.execute(f"UPDATE exercises SET {set_clause} WHERE id=?", params)
    # delete placeholders
    ph_ids = [str(p[0]) for p in ph_rows]
    if ph_ids:
        cur.execute(f"DELETE FROM exercises WHERE id IN ({','.join(ph_ids)})")
    actions.append({'exercise_id': exid, 'kept_id': keep_id, 'deleted_placeholder_ids': ph_ids, 'applied_updates': updates})
    merged.append(exid)

conn.commit()
# write log
log = {
    'generated_at': datetime.datetime.now().isoformat(),
    'db_path': db_path,
    'backup_path': backup_path,
    'merged_count': len(merged),
    'merged_exercise_ids': merged,
    'skipped_exercise_ids': skipped,
    'actions': actions
}
log_path = os.path.join(project_root, r"docs\analysis\merge-placeholders-log-2025-12-03.json")
with open(log_path, 'w', encoding='utf-8') as f:
    json.dump(log, f, indent=2, ensure_ascii=False)

print('Merge complete. Backup at', backup_path)
print('Log written to', log_path)

conn.close()
