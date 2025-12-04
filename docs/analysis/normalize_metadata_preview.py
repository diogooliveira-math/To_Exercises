import os, json, re
root = r"C:\Users\diogo\projects\To_Exercises\ExerciseDatabase"
preview = {}
pattern = re.compile(r'^(?P<base>[A-Z0-9_]+?)(?:\.agentfix|\.bak_agent_[0-9T]+|_solution|\.bak)$', re.IGNORECASE)

for dirpath, dirnames, filenames in os.walk(root):
    for fn in filenames:
        if not fn.lower().endswith('.json'):
            continue
        path = os.path.join(dirpath, fn)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception:
            continue
        changes = []
        def walk(obj, jpath=''):
            if isinstance(obj, dict):
                for k,v in obj.items():
                    walk(v, jpath + '/' + str(k))
            elif isinstance(obj, list):
                for i,v in enumerate(obj):
                    walk(v, jpath + '/' + str(i))
            elif isinstance(obj, str):
                m = pattern.match(obj)
                if m:
                    base = m.group('base')
                    if base != obj:
                        changes.append({'json_path': jpath, 'old': obj, 'new': base})
        walk(data)
        if changes:
            preview[path] = changes

out_path = os.path.join(r"C:\Users\diogo\projects\To_Exercises\docs\analysis", 'metadata-normalization-preview-2025-12-03.json')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump({'generated_at': __import__('datetime').datetime.now().isoformat(), 'preview': preview}, f, indent=2, ensure_ascii=False)
print('Preview written to', out_path)
