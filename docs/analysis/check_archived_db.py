import sqlite3, json
db=r"C:\Users\diogo\projects\To_Exercises\docs\analysis\exercises-normalized.sqlite"
conn=sqlite3.connect(db)
cur=conn.cursor()
cur.execute("SELECT COUNT(*) FROM exercises WHERE status='archived'")
arch_count=cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM exercises WHERE file_path LIKE '%solution%' OR file_path LIKE '%agentfix%' OR file_path LIKE '%bak_agent%'")
pattern_count=cur.fetchone()[0]
cur.execute("SELECT id, exercise_id, file_path, status FROM exercises LIMIT 10")
sample=cur.fetchall()
print(json.dumps({'archived_count':arch_count,'pattern_count':pattern_count,'sample':sample}, ensure_ascii=False, indent=2))
conn.close()
