import json, re
p=r"C:\Users\diogo\projects\To_Exercises\docs\analysis\import-log-2025-12-03.json"
with open(p,'r',encoding='utf-8') as f:
    data=json.load(f)
warns=data.get('warnings',[])
patterns={'zero_padding':[], 'solution_suffix':[], 'agentfix':[], 'bak_agent':[], 'other':[]}
for w in warns:
    fp=w.get('file_path','')
    new=w.get('new_exercise_id','') or ''
    existing=w.get('existing_exercise_id','') or ''
    if re.search(r'_solution(\.tex)?$', fp, re.I) or re.search(r'_solution$', new, re.I):
        patterns['solution_suffix'].append(w)
        continue
    if '.agentfix' in fp or new.endswith('.agentfix') or 'agentfix' in fp:
        patterns['agentfix'].append(w)
        continue
    if 'bak_agent' in fp or 'bak_agent' in new:
        patterns['bak_agent'].append(w)
        continue
    def last_num(s):
        m=re.search(r'(\d+)(?!.*\d)', s)
        return m.group(1) if m else None
    n1=last_num(existing)
    n2=last_num(new)
    if n1 and n2 and n1.lstrip('0')==n2.lstrip('0') and n1!=n2:
        patterns['zero_padding'].append(w)
        continue
    patterns['other'].append(w)

for k in patterns:
    print(k, len(patterns[k]))
print('\nSamples:')
for k in patterns:
    print('\n---',k,'sample 5 ---')
    for s in patterns[k][:5]:
        print(s.get('file_path'), 'existing=>', s.get('existing_exercise_id'), 'new=>', s.get('new_exercise_id'))
