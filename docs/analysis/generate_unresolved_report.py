import sqlite3, os, json, csv, re
root = r"C:\Users\diogo\projects\To_Exercises"
db_path = os.path.join(root, 'docs', 'analysis', 'exercises-normalized.sqlite')
out_json = os.path.join(root, 'docs', 'analysis', 'unresolved-report-2025-12-03.json')
out_csv = os.path.join(root, 'docs', 'analysis', 'unresolved-report-2025-12-03.csv')

conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute("SELECT id, exercise_id, folder, metadata_file, added_at FROM exercises WHERE status='auto-added' ORDER BY folder")
rows = cur.fetchall()

pattern = re.compile(r'^(?P<base>.+?)(?:\.agentfix|\.bak_agent_[0-9T]+|_solution|\.bak)$', re.IGNORECASE)
report = {'generated_at': __import__('datetime').datetime.now().isoformat(), 'count': len(rows), 'entries': []}

for r in rows:
    rid, exid, folder, meta, added = r
    suggested = None
    m = pattern.match(exid)
    if m:
        suggested = m.group('base')
    # check if suggested file exists in folder
    suggested_exists = False
    suggested_path = None
    if suggested and folder:
        candidate = os.path.join(folder, suggested + '.tex')
        if os.path.exists(candidate):
            suggested_exists = True
            suggested_path = os.path.relpath(candidate, root).replace('/', '\\')
    # also check if any .tex in folder contains internal Exercise ID == exid or suggested
    file_candidates = []
    if folder and os.path.isdir(folder):
        for fn in os.listdir(folder):
            if fn.lower().endswith('.tex'):
                fp = os.path.join(folder, fn)
                try:
                    with open(fp, 'r', encoding='utf-8') as f:
                        first = f.readline()
                        # look for comment Exercise ID
                        if exid in first or (suggested and suggested in first):
                            file_candidates.append(os.path.relpath(fp, root).replace('/', '\\'))
                except Exception:
                    pass
    entry = {'row_id': rid, 'exercise_id': exid, 'folder': folder, 'metadata_file': meta, 'added_at': added, 'suggested_canonical': suggested, 'suggested_exists': suggested_exists, 'suggested_path': suggested_path, 'file_candidates_in_folder': file_candidates}
    report['entries'].append(entry)

# write json
with open(out_json, 'w', encoding='utf-8') as f:
    json.dump(report, f, indent=2, ensure_ascii=False)
# write csv
with open(out_csv, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['row_id','exercise_id','folder','metadata_file','added_at','suggested_canonical','suggested_exists','suggested_path','file_candidates_in_folder'])
    for e in report['entries']:
        writer.writerow([e['row_id'], e['exercise_id'], e['folder'], e['metadata_file'], e['added_at'], e['suggested_canonical'], e['suggested_exists'], e['suggested_path'] or '', ';'.join(e['file_candidates_in_folder'])])

conn.close()
print('Wrote', report['count'], 'unresolved entries to', out_json, 'and', out_csv)
