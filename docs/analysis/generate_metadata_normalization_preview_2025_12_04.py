import os
import json
import re

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
out_path = os.path.join(os.path.dirname(__file__), 'metadata-normalization-preview-2025-12-04.json')

patterns = [
    (re.compile(r'(?:_|\.)solution$', re.IGNORECASE), 'strip_solution_suffix'),
    (re.compile(r'\.agentfix$', re.IGNORECASE), 'strip_dot_agentfix'),
    (re.compile(r'(?:_|\.)bak_agent$', re.IGNORECASE), 'strip_bak_agent'),
    (re.compile(r'(?:_|\.)bak$', re.IGNORECASE), 'strip_bak'),
    (re.compile(r'([._]\d{6,})$'), 'strip_trailing_digits'),
    (re.compile(r'_[a-f0-9]{6,}$', re.IGNORECASE), 'strip_hex_suffix'),
]

results = []
scan_count = 0
for dirpath, dirnames, filenames in os.walk(repo_root):
    if 'ExerciseDatabase' not in dirpath:
        # only inspect paths under ExerciseDatabase for speed
        continue
    for fname in filenames:
        if fname != 'metadata.json':
            continue
        scan_count += 1
        full = os.path.join(dirpath, fname)
        try:
            with open(full, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            results.append({
                'metadata_file': os.path.relpath(full, repo_root).replace('\\', '/'),
                'error': str(e),
            })
            continue
        if not isinstance(data, dict):
            results.append({
                'metadata_file': os.path.relpath(full, repo_root).replace('\\', '/'),
                'error': 'metadata.json is not a JSON object',
            })
            continue
        keys = list(data.keys())
        file_issues = []
        key_set = set(keys)
        for key in keys:
            reasons = []
            for patt, reason in patterns:
                if patt.search(key):
                    reasons.append(reason)
            # also detect obvious dot-extensions like '.tex' or file-like names
            if re.search(r'\.(tex|pdf|bak|zip)$', key, re.IGNORECASE):
                reasons.append('looks_like_filename_extension')

            # detect keys with two or more consecutive dots or trailing punctuation
            if re.search(r'[._][-+]\d+$', key):
                reasons.append('trailing_numeric_suffix')

            if reasons:
                # propose canonical by stripping known suffixes
                canonical = key
                canonical = re.sub(r'(?:_|\.)solution$', '', canonical, flags=re.IGNORECASE)
                canonical = re.sub(r'\.agentfix$', '', canonical, flags=re.IGNORECASE)
                canonical = re.sub(r'(?:_|\.)bak_agent$', '', canonical, flags=re.IGNORECASE)
                canonical = re.sub(r'(?:_|\.)bak$', '', canonical, flags=re.IGNORECASE)
                canonical = re.sub(r'([._]\d{6,})$', '', canonical)
                canonical = re.sub(r'_[a-f0-9]{6,}$', '', canonical, flags=re.IGNORECASE)
                canonical = canonical.rstrip('._- ')
                canonical_exists = canonical in key_set
                file_issues.append({
                    'original_key': key,
                    'suggested_canonical': canonical,
                    'canonical_exists_in_same_file': canonical_exists,
                    'reasons': reasons,
                })
        if file_issues:
            results.append({
                'metadata_file': os.path.relpath(full, repo_root).replace('\\', '/'),
                'issues': file_issues,
                'total_keys': len(keys),
            })

out = {
    'scan_root': os.path.relpath(repo_root).replace('\\', '/'),
    'metadata_files_scanned': scan_count,
    'files_with_issues': len(results),
    'results': results,
}

os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(out, f, indent=2, ensure_ascii=False)

print('WROTE', out_path)
