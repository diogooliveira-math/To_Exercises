import sqlite3, json, os
project_root = r"C:\Users\diogo\projects\To_Exercises"
db_path = os.path.join(project_root, r"docs\analysis\exercises-normalized.sqlite")
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# 1) counts by folder (top 10)
cur.execute('SELECT folder, COUNT(*) as cnt FROM exercises GROUP BY folder ORDER BY cnt DESC LIMIT 20')
by_folder = cur.fetchall()

# 2) unresolved count (file_path IS NULL)
cur.execute('SELECT COUNT(*) FROM exercises WHERE file_path IS NULL')
unresolved = cur.fetchone()[0]

# 3) counts by status
cur.execute('SELECT status, COUNT(*) FROM exercises GROUP BY status')
by_status = cur.fetchall()

# 4) top metadata files
cur.execute('SELECT metadata_file, COUNT(*) as cnt FROM exercises GROUP BY metadata_file ORDER BY cnt DESC LIMIT 20')
by_meta = cur.fetchall()

# 5) sample unresolved entries (first 20)
cur.execute('SELECT id, exercise_id, folder, metadata_file, added_at FROM exercises WHERE file_path IS NULL ORDER BY added_at LIMIT 20')
sample_unresolved = cur.fetchall()

# 6) total rows
cur.execute('SELECT COUNT(*) FROM exercises')
total = cur.fetchone()[0]

out = {
    'total_rows': total,
    'unresolved_count': unresolved,
    'counts_by_folder': [{'folder': f[0], 'count': f[1]} for f in by_folder],
    'counts_by_status': [{'status': s[0], 'count': s[1]} for s in by_status],
    'top_metadata_files': [{'metadata_file': m[0], 'count': m[1]} for m in by_meta],
    'sample_unresolved': [{'id': r[0], 'exercise_id': r[1], 'folder': r[2], 'metadata_file': r[3], 'added_at': r[4]} for r in sample_unresolved]
}
print(json.dumps(out, indent=2, ensure_ascii=False))
conn.close()
