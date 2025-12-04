import os, json, shutil, datetime
preview_path = r"C:\Users\diogo\projects\To_Exercises\docs\analysis\metadata-normalization-preview-2025-12-03.json"
now = datetime.datetime.now().strftime('%Y%m%dT%H%M%S')
changes_log = []

with open(preview_path, 'r', encoding='utf-8') as f:
    preview = json.load(f).get('preview', {})

for file_path, changes in preview.items():
    # backup original
    if not os.path.exists(file_path):
        continue
    bak_path = file_path + f'.bak.{now}'
    shutil.copy2(file_path, bak_path)
    # load json
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        changes_log.append({'file': file_path, 'error': str(e)})
        continue
    applied = []
    # apply changes
    def walk_and_replace(obj, jpath=''):
        if isinstance(obj, dict):
            for k in list(obj.keys()):
                v = obj[k]
                new_v = walk_and_replace(v, jpath + '/' + str(k))
                obj[k] = new_v
            return obj
        elif isinstance(obj, list):
            for i in range(len(obj)):
                obj[i] = walk_and_replace(obj[i], jpath + '/' + str(i))
            return obj
        elif isinstance(obj, str):
            for ch in changes:
                if ch.get('old') == obj:
                    applied.append({'json_path': jpath, 'old': ch.get('old'), 'new': ch.get('new')})
                    return ch.get('new')
            return obj
        else:
            return obj
    new_data = walk_and_replace(data)
    # write back
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(new_data, f, indent=2, ensure_ascii=False)
        changes_log.append({'file': file_path, 'backup': bak_path, 'applied': applied})
    except Exception as e:
        changes_log.append({'file': file_path, 'error': str(e)})

out_path = r"C:\Users\diogo\projects\To_Exercises\docs\analysis\metadata-normalization-applied-2025-12-03.json"
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump({'generated_at': datetime.datetime.now().isoformat(), 'results': changes_log}, f, indent=2, ensure_ascii=False)
print('Applied normalization. Log at', out_path)
