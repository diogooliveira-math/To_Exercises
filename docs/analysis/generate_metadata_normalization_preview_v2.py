import os, re, json
root = r"C:\Users\diogo\projects\To_Exercises\ExerciseDatabase"
preview = {}
count = 0
strip_re = re.compile(r"(?:\.agentfix|\.bak_agent_[0-9T]+|bak_agent_[0-9T]+|_agentfix|_solution|\.bak)$", re.IGNORECASE)

for dirpath, dirnames, filenames in os.walk(root):
    for fn in filenames:
        if not fn.endswith('.json'):
            continue
        path = os.path.join(dirpath, fn)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception:
            continue
        if not isinstance(data, dict):
            continue
        exerc = data.get('exercicios') or data.get('exercises')
        if not isinstance(exerc, dict):
            continue
        edits = []
        for key in list(exerc.keys()):
            if strip_re.search(key):
                canonical = strip_re.sub('', key)
                action = 'rename_key'
                if canonical in exerc:
                    action = 'merge_into_existing'
                edits.append({'original': key, 'canonical': canonical, 'action': action})
                count += 1
        if edits:
            preview[path] = edits

outpath = os.path.join(os.path.dirname(root), 'docs', 'analysis', 'metadata-normalization-preview-2025-12-03.json')
with open(outpath, 'w', encoding='utf-8') as outf:
    json.dump({'generated_at': __import__('datetime').datetime.now().isoformat(), 'files': preview, 'total_candidates': count}, outf, indent=2, ensure_ascii=False)
print('Preview written to', outpath, 'candidates=', count)
