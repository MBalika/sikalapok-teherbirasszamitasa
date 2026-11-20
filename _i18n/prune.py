#!/usr/bin/env python3
"""A fel nem használt (a magyar forrásból már eltűnt) fordítási sorok törlése a TSV-kből.
használat: python3 build_en.py (→ unused.txt), majd python3 prune.py"""
import pathlib
R = pathlib.Path(__file__).parent
U = set((R / 'unused.txt').read_text(encoding='utf-8').split())
n = 0
for fn in ('en_page.tsv', 'en_script.tsv', 'en_keys.tsv'):
    L = (R / fn).read_text(encoding='utf-8').split('\n'); K = []
    for l in L:
        k = l.split('\t')[0]
        if not l.startswith('#') and (k in U or k.split('@')[0] in U and k in U): n += 1; continue
        K.append(l)
    (R / fn).write_text('\n'.join(K), encoding='utf-8')
print('törölve:', n)
