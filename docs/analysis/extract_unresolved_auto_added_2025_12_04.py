import csv, sqlite3, os

db='docs/analysis/exercises-normalized.sqlite'
out='docs/analysis/unresolved-auto-added-rows-2025-12-04.csv'
if not os.path.exists(db):
    print('DB not found', db)
else:
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute("SELECT id,exercise_id,file_path,metadata_file,status,provenance,added_at FROM exercises WHERE provenance='auto-added' OR status!='resolved'")
    rows=cur.fetchall()
    with open(out,'w',newline='',encoding='utf-8') as f:
        w=csv.writer(f)
        w.writerow(['id','exercise_id','file_path','metadata_file','status','provenance','added_at'])
        for r in rows:
            w.writerow(r)
    print('WROTE', out, 'ROWS', len(rows))
