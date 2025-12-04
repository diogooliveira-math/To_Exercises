import os, json, glob, hashlib, datetime
project_root = r"C:\Users\diogo\projects\To_Exercises"
metadata_summary_path = os.path.join(project_root, r"docs\analysis\metadata-summary-2025-12-02.json")
out_path = os.path.join(project_root, r"docs\analysis\import-dry-run-report-2025-12-02.json")
root_exdb = os.path.join(project_root, 'ExerciseDatabase')

with open(metadata_summary_path, 'r', encoding='utf-8') as f:
    summaries = json.load(f)

report = {
    'generated_at': datetime.datetime.now().isoformat(),
    'total_metadata_files': len(summaries),
    'parents_candidates': [],
    'unreferenced_files_report': [],
    'missing_exercises': [],
    'summary_by_folder': []
}

for row in summaries:
    folder = row['folder_path']
    metadata_file = row['metadata_file']
    rel_folder = os.path.relpath(folder, project_root)
    entry = {
        'folder': folder,
        'rel_folder': rel_folder,
        'metadata_file': metadata_file,
        'has_subvariants_flag': row.get('has_subvariants', False),
        'num_exercises_listed': row.get('num_exercises_listed', 0),
        'resolved_exercises': [],
        'missing_exercises': [],
        'unreferenced_tex_files': [],
        'notes': []
    }
    # load original metadata if exists
    metadata_path = os.path.join(folder, metadata_file)
    meta = None
    try:
        with open(metadata_path, 'r', encoding='utf-8') as mf:
            meta = json.load(mf)
    except Exception:
        # already in summary, skip
        meta = None
    # extract exercise ids from original metadata if possible
    ex_ids = []
    if meta:
        ex = meta.get('exercicios') or meta.get('exercises') or {}
        if isinstance(ex, dict):
            ex_ids = list(ex.keys())
        elif isinstance(ex, list):
            ex_ids = ex
    # fallback to sample_exercises from summary
    if not ex_ids:
        ex_ids = row.get('sample_exercises', [])
    # for each exercise id, try to find .tex files
    for exid in ex_ids:
        # search patterns: exid*.tex within folder and immediate subdirs
        pattern1 = os.path.join(folder, f"{exid}*.tex")
        pattern2 = os.path.join(folder, '**', f"{exid}*.tex")
        found = glob.glob(pattern1)
        if not found:
            found = glob.glob(pattern2, recursive=True)
        if not found:
            # also try prefix match lower/upper variations
            found = glob.glob(os.path.join(folder, '**', f"{exid.lower()}*.tex"), recursive=True)
        if found:
            for fpath in found:
                rel = os.path.relpath(fpath, project_root)
                entry['resolved_exercises'].append({'exercise_id': exid, 'file_path': rel})
        else:
            entry['missing_exercises'].append(exid)
            report['missing_exercises'].append({'folder': folder, 'exercise_id': exid})
    # detect unreferenced .tex files in folder
    tex_files = glob.glob(os.path.join(folder, '**', '*.tex'), recursive=True)
    referenced_paths = {os.path.normpath(os.path.join(project_root, r['file_path'])) for r in entry['resolved_exercises'] if 'file_path' in r}
    unreferenced = []
    for tf in tex_files:
        norm_tf = os.path.normpath(tf)
        if norm_tf not in referenced_paths:
            unreferenced.append(os.path.relpath(tf, project_root))
    entry['unreferenced_tex_files'] = unreferenced
    # compute checksums for resolved and unreferenced files
    for r in entry['resolved_exercises']:
        if 'file_path' in r and r['file_path']:
            ffull = os.path.normpath(os.path.join(project_root, r['file_path']))
            try:
                with open(ffull, 'rb') as fh:
                    r['checksum'] = hashlib.sha256(fh.read()).hexdigest()
            except Exception:
                r['checksum'] = None
    unref_with_checksums = []
    for uf in unreferenced:
        ffull = os.path.normpath(os.path.join(project_root, uf))
        try:
            with open(ffull, 'rb') as fh:
                chk = hashlib.sha256(fh.read()).hexdigest()
        except Exception:
            chk = None
        unref_with_checksums.append({'file_path': uf, 'checksum': chk})
    entry['unreferenced_tex_files'] = unref_with_checksums
    # parent candidate detection
    if row.get('has_subvariants') or any('subvariant' in os.path.basename(x).lower() for x in tex_files) or any(len(glob.glob(os.path.join(folder, '**', f"{ex}*.tex"), recursive=True))>1 for ex in ex_ids):
        report['parents_candidates'].append({'folder': folder, 'num_listed': len(ex_ids), 'num_resolved': len(entry['resolved_exercises'])})
    # collect brief note if many unreferenced files
    if len(unreferenced) > 0:
        entry['notes'].append(f"{len(unreferenced)} unreferenced .tex files in folder")
    report['summary_by_folder'].append(entry)

# produce a separate list of top 20 folders with most missing
missing_count_by_folder = {}
for m in report['missing_exercises']:
    missing_count_by_folder.setdefault(m['folder'], 0)
    missing_count_by_folder[m['folder']] += 1
report['top_missing_folders'] = sorted(missing_count_by_folder.items(), key=lambda x: x[1], reverse=True)[:20]

with open(out_path, 'w', encoding='utf-8') as outf:
    json.dump(report, outf, indent=2, ensure_ascii=False)

print('Dry-run report written to', out_path)
