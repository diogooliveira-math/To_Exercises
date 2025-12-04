import os, json, csv, datetime, glob
root = r"C:\Users\diogo\projects\To_Exercises\ExerciseDatabase"
out_dir = r"C:\Users\diogo\projects\To_Exercises\docs\analysis"
os.makedirs(out_dir, exist_ok=True)
now = datetime.datetime.now().strftime('%Y-%m-%d')
rows = []
for p in glob.glob(os.path.join(root, '**', '*.json'), recursive=True):
    try:
        with open(p, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        # skip unreadable
        rows.append({
            'folder_path': os.path.dirname(p),
            'metadata_file': os.path.basename(p),
            'error': str(e)
        })
        continue
    folder = os.path.dirname(p)
    # gather other json files in same folder
    sibling_jsons = [os.path.basename(x) for x in glob.glob(os.path.join(folder, '*.json')) if os.path.basename(x)!=os.path.basename(p)]
    # fields extraction with many fallbacks
    tipo = data.get('tipo') or data.get('type') or (data.get('classification') or {}).get('tipo') or data.get('id')
    tipo_nome = data.get('tipo_nome') or data.get('type') or None
    conceito = data.get('conceito') or data.get('concept') or (data.get('classification') or {}).get('concept')
    conceito_nome = data.get('conceito_nome') or data.get('concept_name') or None
    tema = data.get('tema') or data.get('module') or (data.get('classification') or {}).get('module')
    tema_nome = data.get('tema_nome') or data.get('module_name') or None
    disciplina = data.get('disciplina') or (data.get('classification') or {}).get('discipline')
    descricao = data.get('descricao') or data.get('description') or (data.get('classification') or {}).get('description')
    tags = data.get('tags_tipo') or data.get('tags') or (data.get('classification') or {}).get('tags') or []
    # difficulty range
    diff = data.get('dificuldade_sugerida') or data.get('difficulty_range') or data.get('classification',{}).get('difficulty')
    diff_min = diff_max = None
    if isinstance(diff, dict):
        diff_min = diff.get('min')
        diff_max = diff.get('max')
    elif isinstance(diff, int):
        diff_min = diff_max = diff
    # exercises list
    ex = data.get('exercicios') or data.get('exercises') or (data.get('classification') or {}).get('exercicios') or []
    # normalize to list of ids
    ex_ids = []
    if isinstance(ex, dict):
        ex_ids = list(ex.keys())
    elif isinstance(ex, list):
        ex_ids = ex
    # count
    num_ex = len(ex_ids)
    sample = ex_ids[:3]
    has_sub = data.get('has_subvariants') or data.get('has_subvariants', False) or False
    # check for important fields
    warnings = []
    if not disciplina:
        warnings.append('missing_disciplina')
    if not tema:
        warnings.append('missing_tema')
    if not conceito:
        warnings.append('missing_conceito')
    if num_ex==0:
        warnings.append('no_exercises_listed')
    row = {
        'folder_path': folder,
        'metadata_file': os.path.basename(p),
        'tipo': tipo,
        'tipo_nome': tipo_nome,
        'disciplina': disciplina,
        'tema': tema,
        'tema_nome': tema_nome,
        'conceito': conceito,
        'conceito_nome': conceito_nome,
        'descricao': descricao,
        'tags': tags,
        'difficulty_min': diff_min,
        'difficulty_max': diff_max,
        'has_subvariants': bool(has_sub),
        'num_exercises_listed': num_ex,
        'sample_exercises': sample,
        'sibling_jsons': sibling_jsons,
        'warnings': warnings
    }
    rows.append(row)
# write json
out_json = os.path.join(out_dir, f"metadata-summary-{now}.json")
with open(out_json, 'w', encoding='utf-8') as f:
    json.dump(rows, f, indent=2, ensure_ascii=False)
# write csv (flatten some fields)
out_csv = os.path.join(out_dir, f"metadata-summary-{now}.csv")
keys = ['folder_path','metadata_file','disciplina','tema','conceito','tipo','descricao','tags','difficulty_min','difficulty_max','has_subvariants','num_exercises_listed','sample_exercises','sibling_jsons','warnings']
with open(out_csv, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=keys)
    writer.writeheader()
    for r in rows:
        rr = {k: r.get(k) for k in keys}
        # stringify lists
        for lk in ['tags','sample_exercises','sibling_jsons','warnings']:
            v = rr.get(lk)
            rr[lk] = json.dumps(v, ensure_ascii=False)
        writer.writerow(rr)
print('WROTE', out_json, out_csv)
