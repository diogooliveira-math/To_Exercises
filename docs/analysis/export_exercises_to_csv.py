import sqlite3, csv, os

project_root = r"C:\Users\diogo\projects\To_Exercises"
db_path = os.path.join(project_root, r"docs\analysis\exercises-normalized.sqlite")
csv_path = os.path.join(project_root, r"docs\analysis\exercises-normalized.csv")

conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute('PRAGMA case_sensitive_like = ON')
cur.execute('SELECT id, exercise_id, file_path, checksum, folder, rel_folder, metadata_file, status, provenance, added_at FROM exercises')
rows = cur.fetchall()

with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['id','exercise_id','file_path','checksum','folder','rel_folder','metadata_file','status','provenance','added_at'])
    for r in rows:
        writer.writerow(r)

conn.close()
print('Wrote', len(rows), 'rows to', csv_path)
