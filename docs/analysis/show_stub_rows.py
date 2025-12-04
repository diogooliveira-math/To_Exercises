import sqlite3, json, os
project_root = r"C:\Users\diogo\projects\To_Exercises"
db_path = os.path.join(project_root, r"docs\analysis\exercises-normalized.sqlite")
conn = sqlite3.connect(db_path)
cur = conn.cursor()
query = '''SELECT id, exercise_id, file_path, checksum, folder, rel_folder, metadata_file, status, provenance, added_at
FROM exercises
WHERE exercise_id IN (?, ?) OR file_path LIKE ? OR file_path LIKE ?
'''
params = ('MAT_A8MODELO_1SX_NFX_014','MAT_P2ESTATI_REVI_D_002','%MAT_A8MODELO_1SX_NFX_014.tex','%MAT_P2ESTATI_REVI_D_002.tex')
cur.execute(query, params)
rows = cur.fetchall()
cols = ['id','exercise_id','file_path','checksum','folder','rel_folder','metadata_file','status','provenance','added_at']
result = [dict(zip(cols, r)) for r in rows]
print(json.dumps(result, indent=2, ensure_ascii=False))
conn.close()
