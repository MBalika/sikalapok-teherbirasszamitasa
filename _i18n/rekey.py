#!/usr/bin/env python3
"""A sorhoz kötött kulcsok (en_keys.tsv: <id>@index.html:<sor>) átszámozása, ha az index.html sorai elcsúsztak.
Használat: python3 rekey.py [<git-rev>]   – a <git-rev> (alapértelmezés: HEAD) index.html-jéhez képest
számolja át a sorszámokat (difflib), feltéve, hogy az en_keys.tsv a <git-rev> állapotához volt érvényes.
"""
import difflib, re, subprocess, sys, pathlib
rev = sys.argv[1] if len(sys.argv) > 1 else 'HEAD'
root = pathlib.Path(__file__).resolve().parent.parent
old = subprocess.run(['git', 'show', f'{rev}:index.html'], cwd=root, capture_output=True, text=True, check=True).stdout.split('\n')
new = (root / 'index.html').read_text(encoding='utf-8').split('\n')
sm = difflib.SequenceMatcher(None, old, new, autojunk=False)
mp = {}
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        for k in range(i2 - i1): mp[i1 + k + 1] = j1 + k + 1
    elif tag == 'replace' and (i2 - i1) == (j2 - j1):
        for k in range(i2 - i1): mp[i1 + k + 1] = j1 + k + 1
p = root / '_i18n' / 'en_keys.tsv'
out, ch, bad = [], 0, []
for ln in p.read_text(encoding='utf-8').split('\n'):
    m = re.match(r'^([0-9a-f]{7}[!]?)@index\.html:(\d+)(.*)$', ln)
    if m:
        o = int(m.group(2)); n = mp.get(o)
        if n is None: bad.append(ln); out.append(ln); continue
        if n != o: ch += 1
        ln = f'{m.group(1)}@index.html:{n}{m.group(3)}'
    out.append(ln)
p.write_text('\n'.join(out), encoding='utf-8')
print(f'átszámozva: {ch}', ('· NEM található: ' + ' | '.join(bad)) if bad else '')
