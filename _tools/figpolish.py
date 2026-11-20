#!/usr/bin/env python3
"""A kézzel írt elméleti ábrák (az index.html 0. és 1. <figure><svg>-je) egységesítése: Inter betű, nagyobb,
olvasható feliratok, alsó index dy-eltolással (a baseline-shift nem minden böngészőben működik). Idempotens."""
import re, pathlib
p = pathlib.Path(__file__).resolve().parent.parent / 'index.html'; s = p.read_text(encoding='utf-8')
ms = list(re.finditer(r'(<figure[^>]*>\s*)(<svg.*?</svg>)', s, re.S))
SIZE = {'7': '9', '8': '10', '9': '11.5', '10': '12', '12': '13', '12.5': '13.5'}
def polish(t):
    if 'data-polished' in t: return t
    t = t.replace('<svg ', '<svg data-polished="1" ', 1)
    t = re.sub(r'font-family="(Fraunces|JetBrains Mono)"', 'font-family="Inter" font-weight="600"', t)
    t = re.sub(r'font-size="([\d.]+)"', lambda m: f'font-size="{SIZE.get(m.group(1), m.group(1))}"', t)
    t = re.sub(r'(<text[^>]*?) font-style="italic"([^>]*>)(?!oldalnézet)', r'\1\2', t)
    t = re.sub(r'<tspan baseline-shift="sub" font-size="([\d.]+)">([^<]*)</tspan>([^<]*)',
               lambda m: f'<tspan dy="2.6" font-size="{m.group(1)}">{m.group(2)}</tspan>' + (f'<tspan dy="-2.6">{m.group(3)}</tspan>' if m.group(3) else ''), t)
    return t
for k in (1, 0):
    m = ms[k]; t = polish(m.group(2))
    if k == 1: t = t.replace('viewBox="0 0 560 300"', 'viewBox="-28 0 588 300"')
    if k == 0 and 'min-width' not in t: t = t.replace('<svg data-polished="1" ', '<svg data-polished="1" style="min-width:620px" ', 1)
    s = s[:m.start(2)] + t + s[m.end(2):]
p.write_text(s, encoding='utf-8'); print('kész')
