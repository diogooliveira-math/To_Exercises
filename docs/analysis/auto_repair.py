import os, json, shutil, datetime

project_root = r"C:\Users\diogo\projects\To_Exercises"
report_path = os.path.join(project_root, r"docs\analysis\import-dry-run-report-2025-12-02.json")
repair_report_path = os.path.join(project_root, r"docs\analysis\auto-repair-report-2025-12-02.json")

with open(report_path, 'r', encoding='utf-8') as f:
    report = json.load(f)

changes = {
    'generated_at': datetime.datetime.now().isoformat(),
    'modified_metadata_files': [],
    'skipped': [],
}

for entry in report.get('summary_by_folder', []):
    folder = entry['folder']
    metadata_file = entry.get('metadata_file')
    # only handle json metadata files
    if not metadata_file or not metadata_file.lower().endswith('.json'):
        changes['skipped'].append({'folder': folder, 'reason': 'no-json-metadata-file'})
        continue
    metadata_path = os.path.join(folder, metadata_file)
    if not os.path.exists(metadata_path):
        changes['skipped'].append({'folder': folder, 'reason': 'metadata-file-missing', 'metadata_file': metadata_path})
        continue
    try:
        with open(metadata_path, 'r', encoding='utf-8') as mf:
            meta = json.load(mf)
    except Exception as e:
        changes['skipped'].append({'folder': folder, 'reason': 'metadata-parse-error', 'error': str(e)})
        continue
    # ensure exercicios object exists and is a dict
    exs = meta.get('exercicios')
    if exs is None:
        meta['exercicios'] = {}
        exs = meta['exercicios']
    elif isinstance(exs, list):
        # convert list to dict using ids as keys with minimal placeholder
        newex = {}
        for k in exs:
            if isinstance(k, str):
                newex[k] = {
                    'created': None,
                    'modified': None,
                    'author': 'converted-from-list',
                    'difficulty': None,
                    'points': 0,
                    'time_estimate_minutes': 0,
                    'has_multiple_parts': False,
                    'parts_count': 1,
                    'tags': [],
                    'status': 'converted'
                }
        meta['exercicios'] = newex
        exs = newex
    elif not isinstance(exs, dict):
        # unsupported type
        changes['skipped'].append({'folder': folder, 'reason': 'exercicios-not-dict-or-list', 'type': type(exs).__name__})
        continue

    modified = False
    added_ids = []
    # handle unreferenced files
    for uf in entry.get('unreferenced_tex_files', []):
        fname = os.path.basename(uf['file_path'] if isinstance(uf, dict) else uf)
        base, ext = os.path.splitext(fname)
        if base in exs:
            continue
        # only auto-add if base looks like an exercise id (contains underscores and uppercase letters)
        if base.count('_') >= 2 and any(c.isupper() for c in base):
            exs[base] = {
                'created': datetime.date.today().isoformat(),
                'modified': datetime.date.today().isoformat(),
                'author': 'auto-repair',
                'difficulty': meta.get('difficulty_min') or None,
                'points': 0,
                'time_estimate_minutes': 0,
                'has_multiple_parts': False,
                'parts_count': 1,
                'tags': [],
                'status': 'auto-added'
            }
            if isinstance(meta.get('sample_exercises'), list):
                if base not in meta['sample_exercises']:
                    meta['sample_exercises'].append(base)
            else:
                meta['sample_exercises'] = [base]
            modified = True
            added_ids.append(base)
        else:
            changes['skipped'].append({'folder': folder, 'file': fname, 'reason': 'filename-not-id-like'})
    # handle missing_exercises reported (try to find file in folder)
    for mid in entry.get('missing_exercises', []):
        if mid in exs:
            continue
        candidate = None
        for root, dirs, files in os.walk(folder):
            for f in files:
                if f.lower().startswith(mid.lower()) and f.lower().endswith('.tex'):
                    candidate = os.path.relpath(os.path.join(root, f), project_root)
                    break
            if candidate:
                break
        if candidate:
            exs[mid] = {
                'created': datetime.date.today().isoformat(),
                'modified': datetime.date.today().isoformat(),
                'author': 'auto-repair',
                'difficulty': meta.get('difficulty_min') or None,
                'points': 0,
                'time_estimate_minutes': 0,
                'has_multiple_parts': False,
                'parts_count': 1,
                'tags': [],
                'status': 'auto-added'
            }
            if isinstance(meta.get('sample_exercises'), list):
                if mid not in meta['sample_exercises']:
                    meta['sample_exercises'].append(mid)
            else:
                meta['sample_exercises'] = [mid]
            modified = True
            added_ids.append(mid)
        else:
            changes['skipped'].append({'folder': folder, 'missing_id': mid, 'reason': 'no-matching-tex-file'})
    if modified:
        # backup original if not already backed up
        bak = metadata_path + '.bak'
        if not os.path.exists(bak):
            shutil.copy2(metadata_path, bak)
        # write updated metadata
        with open(metadata_path, 'w', encoding='utf-8') as mf:
            json.dump(meta, mf, indent=2, ensure_ascii=False)
        changes['modified_metadata_files'].append({'metadata_file': metadata_path, 'added_exercises': added_ids})

# write repair report
with open(repair_report_path, 'w', encoding='utf-8') as rf:
    json.dump(changes, rf, indent=2, ensure_ascii=False)

print('Auto-repair completed, report written to', repair_report_path)
