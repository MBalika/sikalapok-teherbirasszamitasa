#!/usr/bin/env python3
"""Fordítás-átvitel: a carry.json (node carry.mjs) alapján a nyelvfüggetlen változásokat (számok, jelölések,
HTML-jelek) automatikusan átvezeti a régi angol fordításba; a többit carry_todo.txt-be írja kézi fordításra.
használat: python3 carry.py  → carry_auto.tsv (kész sorok: id<TAB>angol<TAB>page|script), carry_todo.txt"""
import json, re, difflib, pathlib
R = pathlib.Path(__file__).parent
C = json.loads((R / 'carry.json').read_text(encoding='utf-8'))
TOK = re.compile(r'\d+(?:,\d+)?|<[^>]*>|&[a-z]+;|[A-Za-zÀ-ɏͰ-Ͽ]+|\s+|.', re.S)
dec = lambda s: re.sub(r'(?<=\d),(?=\d)', '.', s)
HUW = re.compile(r'[áéíóöőúüűÁÉÍÓÖŐÚÜŰ]|[A-Za-z]{4,}')
auto, todo = [], []
for c in C:
    hu, oh, oe = c['hu'], c['oldHu'], c['oldEn']
    ok = oh is not None and c['sim'] >= 0.6 and oe not in (None, '=')
    en = oe
    if ok:
        a, b = TOK.findall(oh), TOK.findall(hu)
        ops = [o for o in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes() if o[0] != 'equal']
        for tag, i1, i2, j1, j2 in reversed(ops):
            lo, hi = i1, i2
            frag = ''.join(a[lo:hi]); new = ''.join(b[j1:j2])
            if HUW.search(re.sub(r'<[^>]*>|&[a-z]+;', '', frag + new)): ok = False; break
            pre = post = ''
            while (oh.count(pre + frag + post) != 1 or en.replace('⏎', '\n').count(dec(pre + frag + post)) != 1 or not frag) and (lo > 0 or hi < len(a)):
                if lo > 0: lo -= 1; pre = a[lo] + pre
                if hi < len(a): post = post + a[hi]; hi += 1
                if HUW.search(re.sub(r'<[^>]*>|&[a-z]+;', '', pre + post)): break
            src = dec(pre + frag + post); dst = dec(pre + new + post)
            e2 = en.replace('⏎', '\n')
            if e2.count(src) != 1: ok = False; break
            en = e2.replace(src, dst).replace('\n', '⏎')
    (auto if ok else todo).append((c, en))
with open(R / 'carry_auto.tsv', 'w', encoding='utf-8') as f:
    for c, en in auto: f.write(f"{c['id']}\t{en}\t{'script' if c['js'] else 'page'}\n")
with open(R / 'carry_todo.txt', 'w', encoding='utf-8') as f:
    for c, en in todo:
        f.write(f"### {c['id']} {'script' if c['js'] else 'page'} sor {c['line']} sim {c['sim']} régi {c['oldId']}\nÚJ : {c['hu']}\nRÉGI: {c['oldHu']}\nEN  : {c['oldEn']}\n\n")
print('automatikus:', len(auto), '· kézi:', len(todo))
