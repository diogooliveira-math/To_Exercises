import os, re, json
root = r"C:\Users\diogo\projects\To_Exercises\ExerciseDatabase"
preview = {}
count = 0
patterns = [r"\.agentfix","bak_agent_[0-9T]+","_agentfix","_solution","_bak_agent_[0-9T]+","\.bak"]
strip_re = re.compile(r"(\.agentfix|bak_agent_[0-9T]+|_agentfix|_solution|_bak_agent_[0-9T]+|\.bak)$")

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
        edits = []
        for key in list(data.keys()):
            if re.search(r'(?:_solution|\.agentfix|bak_agent|_agentfix|\.bak)', key):
                canonical = strip_re.sub('', key)
                action = 'rename_key'
                if canonical in data:
                    action = 'merge_into_existing'
                edits.append({'original': key, 'canonical': canonical, 'action': action})
                count += 1
        if edits:
            preview[path] = edits

outpath = os.path.join(os.path.dirname(root), 'docs', 'analysis', 'metadata-normalization-preview-2025-12-03.json')
with open(outpath, 'w', encoding='utf-8') as outf:
    json.dump({'generated_at': __import__('datetime').datetime.now().isoformat(), 'files': preview, 'total_candidates': count}, outf, indent=2, ensure_ascii=False)
print('Preview written to', outpath)
