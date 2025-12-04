import os, shutil, hashlib, json, datetime, zipfile
root = r"C:\Users\diogo\projects\To_Exercises"
exroot = os.path.join(root, 'ExerciseDatabase')
support = os.path.join(exroot, '_support')
backups_dir = os.path.join(support, 'backups')
solutions_dir = os.path.join(support, 'solutions')
sebentas_dir = os.path.join(support, 'sebentas')

os.makedirs(backups_dir, exist_ok=True)
os.makedirs(solutions_dir, exist_ok=True)
os.makedirs(sebentas_dir, exist_ok=True)

candidates = []
for dirpath, dirnames, filenames in os.walk(exroot):
    # skip support
    if dirpath.startswith(support):
        continue
    for fn in filenames:
        if fn.endswith('.agentfix.tex') or 'bak_agent' in fn or fn.endswith('.bak.tex'):
            cat='backup'
            dest_dir=backups_dir
        elif fn.endswith('_solution.tex') or fn.endswith('solution.tex'):
            cat='solution'
            dest_dir=solutions_dir
        elif os.path.basename(dirpath)=='build' and fn.startswith('sebenta_'):
            cat='sebenta'
            dest_dir=sebentas_dir
        else:
            continue
        orig_path=os.path.join(dirpath,fn)
        # checksum
        h=hashlib.sha256()
        with open(orig_path,'rb') as f:
            while True:
                b=f.read(8192)
                if not b: break
                h.update(b)
        sha=h.hexdigest()
        rel=os.path.relpath(orig_path, root)
        new_name=fn
        target=os.path.join(dest_dir,new_name)
        # ensure unique target
        i=1
        base,ext=os.path.splitext(new_name)
        while os.path.exists(target):
            target=os.path.join(dest_dir,f"{base}.{i}{ext}")
            i+=1
        # move
        shutil.move(orig_path, target)
        candidates.append({'category':cat, 'orig_path':orig_path, 'new_path':target, 'sha256':sha})

# write index
ts=datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
index={'generated_at':ts, 'root':root, 'moved':candidates}
idx_path=os.path.join(root,'docs','analysis','archived-files-2025-12-03.json')
with open(idx_path,'w',encoding='utf-8') as f:
    json.dump(index,f,indent=2,ensure_ascii=False)

# create zip
zip_path=os.path.join(root,'docs','analysis','archived-backup-2025-12-03.zip')
with zipfile.ZipFile(zip_path,'w',compression=zipfile.ZIP_DEFLATED) as zf:
    for c in candidates:
        zf.write(c['new_path'], arcname=os.path.relpath(c['new_path'], root))

print('Moved',len(candidates),'files. Index at',idx_path)
print('Zip at',zip_path)
