#!/usr/bin/env python3
"""A mintapéldák metszet- és alaprajzi ábráinak paraméteres előállítása (statikus SVG az index.html-be).
használat: python3 _tools/mpfig.py            → az index.html 2–15. <figure><svg> ábráit cseréli
           python3 _tools/mpfig.py --out DIR  → csak önálló .svg fájlokat ír (ellenőrzéshez)
Rajzszabályok: a beton alaptest téglalap, vízszintes felső síkkal; a teher-nyilak a fal tetején végződnek;
a méretszöveg soha nem keresztez vonalat; alsó index dy-eltolással (nem baseline-shift); minden szöveg fehér
körvonallal (halo); egységes, visszafogott talajszínek finom mintával."""
import re, sys, pathlib, math
ROOT = pathlib.Path(__file__).resolve().parent.parent
INK, DIM, MUTE, WATER = '#2E2620', '#3D4852', '#5F5546', '#1E78C8'
PERM, VAR, RES, ACT = '#B5341F', '#1E63B0', '#2E7D4F', '#C96A12'
SOIL = {  # szín, minta
    'fill':   ('#EADFB6', 'dot'), 'gravel': ('#E3D3A0', 'dot2'), 'silty': ('#DCC08E', 'dash'),
    'bearing': ('#D5CE93', 'dot'), 'clay':  ('#C2B29C', 'hatch'), 'silt': ('#D8C39A', 'dash'),
}
def num(v, d=None):
    if isinstance(v, str): return v
    s = (f'{v:.{d}f}' if d is not None else (f'{v:g}')).replace('.', ',')
    return s
def rich(t):
    """'G_{z,k} = 250 kN/m' → tspan-ok (alsó index dy-nal)"""
    out, pos = '', 0
    for m in re.finditer(r'_\{([^}]*)\}', t):
        out += esc(t[pos:m.start()]) + f'<tspan dy="3" font-size="78%">{esc(m.group(1))}</tspan><tspan dy="-3">​</tspan>'
        pos = m.end()
    return out + esc(t[pos:])
def esc(s): return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
class Fig:
    def __init__(s, W, H, pid): s.W, s.H, s.pid, s.g, s.t = W, H, pid, [], []
    def add(s, x): s.g.append(x)
    def text(s, x, y, t, anchor='start', size=12, weight=600, fill=DIM, italic=False):
        s.t.append(f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" fill="{fill}"'
                   + (' font-style="italic"' if italic else '') + f'>{rich(t)}</text>')
    def line(s, x1, y1, x2, y2, col=DIM, w=1, dash=None):
        s.add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="{w}"' + (f' stroke-dasharray="{dash}"' if dash else '') + '/>')
    def arrow(s, x1, y1, x2, y2, col, w=4, head=11):
        a = math.atan2(y2 - y1, x2 - x1); bx, by = x2 - head * 1.25 * math.cos(a), y2 - head * 1.25 * math.sin(a)
        px, py = -math.sin(a) * head * 0.62, math.cos(a) * head * 0.62
        s.add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{bx:.1f}" y2="{by:.1f}" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>'
              f'<polygon points="{x2:.1f},{y2:.1f} {bx+px:.1f},{by+py:.1f} {bx-px:.1f},{by-py:.1f}" fill="{col}"/>')
    def dimv(s, x, y1, y2, label, side='left', gap=8):
        s.line(x, y1, x, y2, DIM, 0.9); [s.line(x - 4, y, x + 4, y, DIM, 0.9) for y in (y1, y2)]
        s.text(x - gap if side == 'left' else x + gap, (y1 + y2) / 2 + 4, label, 'end' if side == 'left' else 'start')
    def dimh(s, x1, x2, y, label, below=True):
        s.line(x1, y, x2, y, DIM, 0.9); [s.line(x, y - 4, x, y + 4, DIM, 0.9) for x in (x1, x2)]
        s.text((x1 + x2) / 2, y + 17 if below else y - 7, label, 'middle')
    def svg(s):
        p = s.pid
        defs = (f'<defs><pattern id="{p}dot" width="14" height="14" patternUnits="userSpaceOnUse"><circle cx="3" cy="4" r="1" fill="#8C7A4E" opacity=".45"/><circle cx="10" cy="11" r="0.8" fill="#8C7A4E" opacity=".4"/></pattern>'
                f'<pattern id="{p}dot2" width="18" height="16" patternUnits="userSpaceOnUse"><circle cx="4" cy="5" r="1.7" fill="none" stroke="#8C7A4E" stroke-width=".7" opacity=".5"/><circle cx="13" cy="12" r="1.2" fill="#8C7A4E" opacity=".4"/></pattern>'
                f'<pattern id="{p}dash" width="20" height="12" patternUnits="userSpaceOnUse"><path d="M2 4h7M12 10h6" stroke="#8A6C3F" stroke-width=".8" opacity=".45"/></pattern>'
                f'<pattern id="{p}hatch" width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><path d="M0 0v10" stroke="#6E5C48" stroke-width=".8" opacity=".4"/></pattern>'
                f'<pattern id="{p}conc" width="22" height="22" patternUnits="userSpaceOnUse"><path d="M3 5l2 1M14 4l1 2M8 14l2-1M17 16l1 1M4 19l1-1" stroke="#7B848B" stroke-width=".8" opacity=".55"/></pattern></defs>')
        return (f'<svg viewBox="0 0 {s.W} {s.H}" xmlns="http://www.w3.org/2000/svg" font-family="Inter, system-ui, sans-serif"' + (' style="min-width:620px"' if s.W > 600 else '') + '>' + defs + ''.join(s.g)
                + '<g paint-order="stroke" stroke="#fff" stroke-opacity=".78" stroke-width="2.8" stroke-linejoin="round">' + ''.join(s.t) + '</g></svg>')
def m(v):
    """hossz méterben: legalább egy tizedes (1,0 m; 0,95 m)"""
    t = f'{v:.2f}'.rstrip('0'); return (t + '0' if t.endswith('.') else t).replace('.', ',') + ' m'
def free(lo, hi, obst, cap=None):
    """a legnagyobb akadálymentes sáv közepe [lo, hi]-ben (cap: legfeljebb ennyivel a sáv teteje alatt)"""
    ys = [lo] + sorted(o for o in obst if lo < o < hi) + [hi]; a, b = max(zip(ys, ys[1:]), key=lambda q: q[1] - q[0])
    return a + min((b - a) / 2, cap) if cap else (a + b) / 2
def section(pid, sc, B, h, b, t, layers, loads, hload=None, gw=None, wdim=None, tfill=None, note='Sávalap (L ≫ B)', W=760, cx=330, hw=0.55,
            alpha=0, Blabel=None, blabel=None, eb=0, front=None, base=None, rear=None, depth=None, thdim=True, gwlabel='talajvíz'):
    D = t + h; top = 26 + 92; gy = top + hw * sc
    zmax = depth or max(D + 0.8, (gw or 0) + 0.45, sum(L[0] for L in layers if L[0]) + 0.8)
    H = round(gy + zmax * sc + 6); F = Fig(W, H, pid); X0, X1 = 28, W - 28
    Y = lambda z: gy + z * sc
    xl, xr = cx - B * sc / 2, cx + B * sc / 2; cw = cx + eb * sc; wl, wr = cw - b * sc / 2, cw + b * sc / 2; yT, yB, wt = Y(t), Y(D), gy - hw * sc
    dy = math.tan(math.radians(alpha)) * B * sc / 2
    bounds = []; z = 0
    for k, (th, name, par, kind) in enumerate(layers):
        z2 = zmax if th is None else z + th; col, pat = SOIL[kind]
        F.add(f'<rect x="{X0}" y="{Y(z):.1f}" width="{X1-X0}" height="{Y(z2)-Y(z):.1f}" fill="{col}"/><rect x="{X0}" y="{Y(z):.1f}" width="{X1-X0}" height="{Y(z2)-Y(z):.1f}" fill="url(#{pid}{pat})"/>')
        if k: F.line(X0, Y(z), X1, Y(z), '#8A7550', 1.1); bounds.append(Y(z))
        z = z2
    F.line(X0, gy, X1, gy, '#5C7A52', 2.2)
    F.add('<path d="' + ''.join(f'M{x} {gy}l-6 -7' for x in range(X0 + 10, X1, 14)) + '" stroke="#5C7A52" stroke-width="1" fill="none"/>')
    F.text(X0 + 6, gy - 13, 'terepszint', size=11.5, fill='#4A6542')
    obst = list(bounds); yw = None
    if gw is not None:  # talajvíz: az alaptest mögött futó szaggatott vonal, a felirat a vonal fölött
        yw = Y(gw); obst.append(yw); F.line(X0, yw, X1, yw, WATER, 1.6, '9 5')
        F.add(f'<polygon points="{X0+34},{yw-11} {X0+48},{yw-11} {X0+41},{yw-1}" fill="{WATER}"/>'); F.text(X0 + 54, yw + 15 if hload and abs(yw - yT) < 1 else yw - 6, gwlabel, size=12, weight=700, fill=WATER)
        if hload and abs(yw - yT) < 1: obst.append(yw + 12)
    F.add(f'<polygon points="{xl:.1f},{yT:.1f} {xr:.1f},{yT:.1f} {xr:.1f},{yB-dy:.1f} {xl:.1f},{yB+dy:.1f}" fill="#C9CDD1" stroke="{INK}" stroke-width="1.6"/>'
          f'<polygon points="{xl:.1f},{yT:.1f} {xr:.1f},{yT:.1f} {xr:.1f},{yB-dy:.1f} {xl:.1f},{yB+dy:.1f}" fill="url(#{pid}conc)"/>')
    F.add(f'<rect x="{wl:.1f}" y="{wt:.1f}" width="{wr-wl:.1f}" height="{yT-wt:.1f}" fill="#B4BABF" stroke="{INK}" stroke-width="1.4"/>')
    if B * sc >= 110: F.text(cx, yB - 12, 'γ_{b} = 25 kN/m³', 'middle', 11.5, 600, INK)
    else: note += ' · γ_{b} = 25 kN/m³'
    # függőleges terhek: a nyíl a fal tetején végződik; a külpontos teher hatásvonala szaggatott
    ya = top - 84
    for (lab, e, col, side) in loads:
        x = cw + e * sc
        if abs(e) > b / 2 + 1e-9: F.line(x, wt, x, yT, col, 1.2, '4 4')
        F.arrow(x, ya, x, wt - 2, col, 4.2, 12)
        for k, l in enumerate(lab if isinstance(lab, list) else [lab]): F.text(x + (10 if side == 'r' else -10), ya + 14 + k * 17, l, 'start' if side == 'r' else 'end', 13, 700, col)
    es = [e for (_, e, _, _) in loads if abs(e) > 1e-9]
    if es:
        e = es[0]; ye = wt - 26; F.line(cw, wt - 40, cw, wt - 4, DIM, 0.8, '2 3'); F.line(cw + e * sc, ye, cw, ye, DIM, 0.9); [F.line(x, ye - 4, x, ye + 4, DIM, 0.9) for x in (cw, cw + e * sc)]
        F.text(max(cw, cw + e * sc) + 8, ye + 4, ('e_{q}' if len(loads) > 1 else 'e_{B}') + ' = ' + m(abs(e)))
    xd = xl - (80 if rear else 30)
    if hload:  # vízszintes teher az alaptest felső síkján; a felirat a nyíl fölött, szűk helyen az alaptestben
        lab, d, col = hload; yh = yT - 10; above = (wl - 104 > xd) or t * sc > 70
        if d > 0: F.arrow(wl - 84, yh, wl - 3, yh, col, 4.2, 12); F.text(*((wl - 46, yh - 10, lab, 'middle') if above else (xl + 8, yT + 18, lab, 'start')), 13, 700, col)
        else: F.arrow(wr + 84, yh, wr + 3, yh, col, 4.2, 12); F.text(wr + 8, yh - 11, lab, 'start', 13, 700, col)
    ym = max((yT + yB) / 2 + 8, (yw or 0) + 18) if yw and yT < yw < yB else (yT + yB) / 2 + 8
    if wdim:  # a talajvíz és az alapsík távolsága a bal szélen, a felirat a vonal jobb oldalán
        lab, za, zb = wdim; ywd = free(Y(za), Y(zb), bounds) + 4; F.line(X0 + 16, Y(za), X0 + 16, Y(zb), DIM, 0.9); [F.line(X0 + 12, y, X0 + 20, y, DIM, 0.9) for y in (Y(za), Y(zb))]
        F.text(X0 + 24, ywd, lab); obst.append(ywd - 4)
    if thdim:
        for (y1, y2, lab) in ((gy, yT, 't = ' + m(t)), (yT, yB + dy, 'h = ' + m(h))):
            F.line(xd, y1, xd, y2, DIM, 0.9); [F.line(xd - 4, y, xd + 4, y, DIM, 0.9) for y in (y1, y2)]; F.text(xd - 8, free(y1, y2, obst + ([ym] if rear else [])) + 4, lab, 'end')
    F.dimh(xl, xr, yB + abs(dy) + 28, Blabel or 'B = ' + m(B))
    yb = gy - hw * sc * 0.42; F.line(wl - 12, yb, wl, yb, DIM, 0.9); F.line(wr, yb, wr + 12, yb, DIM, 0.9)
    F.add(f'<path d="M{wl:.1f} {yb:.1f}l-6 -3v6zM{wr:.1f} {yb:.1f}l6 -3v6z" fill="{DIM}"/>'); F.text(wr + 17, yb + 4, blabel or 'b = ' + m(b))
    # ellenállások (elcsúszás): a teherrel szemben, az alaptest homlokoldalán és a talpon; a hátoldalon az aktív földnyomás
    if front: F.arrow(xr + 70, ym, xr + 3, ym, RES, 3.6, 10); F.text(xr + 76, ym + 4, front, 'start', 12, 700, RES)
    if base: yb2 = yB + 10; F.arrow(cx + 44, yb2, cx - 44, yb2, RES, 3.6, 10); F.text(xl - 8, yB + 16, base, 'end', 12, 700, RES)
    if rear: F.arrow(xl - 62, ym, xl - 3, ym, ACT, 3.6, 10); F.text(xl - 36, ym + 18, rear, 'middle', 12, 700, ACT)
    if alpha:
        x, y = xr, yB - dy; F.line(x, y, x + 86, y, DIM, 0.9, '5 4'); F.line(x, y, x + 86, y - 86 * math.tan(math.radians(alpha)), INK, 1, '5 4')
        F.text(x + 92, y + 1, f'α = {alpha}°', size=12.5, weight=700, fill=PERM); F.text(x + 8, y + 18, 'ferde alapsík', size=11.5, fill=MUTE, italic=True)
    # talajfeliratok: a réteg legnagyobb szabad sávjában (talajvíz-vonal és nyilak nélkül)
    z = 0; rev = bool(hload and hload[1] < 0); yc1 = None
    for k, (th, name, par, kind) in enumerate(layers):
        xs = max(xr + 46, cx + 150) + (70 if (alpha and k) or (rev and not k) else 0)
        z2 = zmax if th is None else z + th; yc = free(Y(z), Y(z2), ([yw] if yw else []) + ([ym] if front else []), cap=None if k == 0 else 46)
        if k == 0: yc1 = yc
        F.text(xs, yc - 10, name, size=13, weight=700, fill=MUTE)
        for j, q in enumerate(par): F.text(xs, yc + 7 + j * 15, q, size=11.5, weight=600, fill=MUTE)
        z = z2
    if tfill: F.line(X1 - 26, gy, X1 - 26, Y(tfill), DIM, 0.9); [F.line(X1 - 30, y, X1 - 22, y, DIM, 0.9) for y in (gy, Y(tfill))]; F.text(X1 - 34, (free(yw, Y(tfill), []) if rev and yw and gy < yw < Y(tfill) else free(gy, Y(tfill), obst + [yc1 + 4])) + 4, 't_{fill} = ' + m(tfill), 'end')
    F.text(X0 + 10, H - 14, note, size=12, weight=700, fill=MUTE)
    return F.svg()
def plan(pid, B, L, b, Gl, Ql, note, eb=0, W=420):
    sc = 150 / max(B, L) if max(B, L) > 1.6 else 112; w, hh = B * sc, L * sc; x0 = (W - w) / 2 + 14; y0 = 58; H = round(y0 + hh + 74); F = Fig(W, H, pid)
    F.add(f'<rect x="{x0:.1f}" y="{y0}" width="{w:.1f}" height="{hh:.1f}" fill="#C9CDD1" stroke="{INK}" stroke-width="1.6"/><rect x="{x0:.1f}" y="{y0}" width="{w:.1f}" height="{hh:.1f}" fill="url(#{pid}conc)"/>')
    cx, cy = x0 + w / 2 + eb * sc, y0 + hh / 2; bs = b * sc
    F.line(x0 + w / 2, y0 - 6, x0 + w / 2, cy - bs / 2, DIM, 0.7, '8 3 2 3'); F.line(x0 + w / 2, y0 + hh - 12, x0 + w / 2, y0 + hh + 6, DIM, 0.7, '8 3 2 3'); F.line(cx + bs / 2, cy, x0 + w + 6, cy, DIM, 0.7, '8 3 2 3')
    F.add(f'<rect x="{cx-bs/2:.1f}" y="{cy-bs/2:.1f}" width="{bs:.1f}" height="{bs:.1f}" fill="#9AA3AA" stroke="{INK}" stroke-width="1.3"/><circle cx="{cx:.1f}" cy="{cy:.1f}" r="4.5" fill="{PERM}"/>')
    F.arrow(x0 - 112, cy, cx - bs / 2 - 3, cy, VAR, 4, 11); F.text(x0 - 10, cy - 11, Ql, 'end', 12.5, 700, VAR)
    for k, g in enumerate(Gl): F.text(cx, cy + bs / 2 + 18 + k * 16, g, 'middle', 12.5, 700, PERM)
    F.dimh(x0, x0 + w, y0 - 22, 'B = ' + m(B), below=False); F.dimv(x0 + w + 24, y0, y0 + hh, 'L = ' + m(L), 'right')
    if eb: F.text(x0 + w / 2 + 7, y0 + hh + 17, 'e_{b} = ' + m(abs(eb)), 'start', 11.5)
    F.text(W / 2, H - 30, 'alaprajzi nézet', 'middle', 12, 700, MUTE); F.text(W / 2, H - 12, note, 'middle', 11.5, 500, '#8F3A1B', True)
    return F.svg()
P = lambda g, gs, phi, c, cu=None: ([f'γ = {num(g)} · γ_{{sat}} = {num(gs)} kN/m³'] if gs else [f'γ = {num(g)} kN/m³']) + ([f'φ = {num(phi)}° · c = {num(c)} kPa'] if cu is None else [f'φ_{{u}} = 0° · c_{{u}} = {num(cu)} kPa'])
def mp37(pid, eq=0.3, gw=0.8, wdim=('h_{MTV} = 0,6 m', 0.8, 1.4), d=1, alpha=0, hl='G_{x,k} = 30 kN/m', depth=None):
    return section(pid, 118, 1.3, 1.0, 0.3, 0.4, [(1.1, 'homok feltöltés', P(18, 19, 30, 5), 'fill'), (None, 'iszapos homok', P(18, 20, 26, 30), 'silty')],
                   [('G_{z,k} = 250 kN/m', 0, PERM, 'r'), ('Q_{z,k} = 170 kN/m', -eq, VAR, 'l')], (hl, d, PERM), gw, wdim, 1.1, alpha=alpha, depth=depth)
def build():
    F = {}
    F[2] = section('m1', 150, 1.1, 0.6, 0.3, 0.5, [(0.8, 'homokos kavics feltöltés', P(17, None, 30, 10), 'gravel'), (None, 'iszapos homok', P(18, None, 24, 12), 'silty')],
                   [(['G_{v,k} = 220 kN/m', 'Q_{v,k} = 70 kN/m'], 0, PERM, 'r')], tfill=0.8)
    F[3] = mp37('m3'); F[4] = mp37('m4', gw=2.8, wdim=('t_{wd} = 1,4 m', 1.4, 2.8), depth=3.3)
    F[5] = mp37('m5', d=-1, hl='G_{x,k} = 30 kN/m (fordított)'); F[6] = mp37('m6', eq=0.5); F[7] = mp37('m7', alpha=5)
    pad = dict(B=2.0, h=1.2, b=0.4, t=0.4, gw=1.0, wdim=('h_{MTV} = 0,6 m', 1.0, 1.6), tfill=1.5, note='Pilléralap (L = 1,5 m)', blabel='b = l = 0,4 m', cx=340)
    F[8] = section('m8', 100, layers=[(1.5, 'homok feltöltés', P(18, 19, 30, 5), 'fill'), (None, 'homokos kavics', P(19, 20, 32, 0), 'gravel')],
                   loads=[('G_{z,k} = 1000 kN', 0, PERM, 'r')], hload=('Q_{x,k} = 100 kN', 1, VAR), **pad)
    F[9] = plan('p8', 2.0, 1.5, 0.4, ['G_{z,k} = 1000 kN'], 'Q_{x,k} = 100 kN', 'a vizsgálatot B és L irányban is el kell végezni')
    F[10] = section('m9', 112, 1.75, 0.55, 0.3, 1.1, [(1.65, '1. réteg (feltöltés)', P(19, 20, 15, 5), 'fill'), (None, '2. réteg (teherbíró)', P(19, 20, 30, 0), 'bearing')],
                    [('V_{d} = 255 kN/m', 0.02, PERM, 'r')], gw=1.65, tfill=1.65, Blabel='B = ?', thdim=False, gwlabel='talajvíz (az alapsíkon)')
    F[11] = section('m10', 100, layers=[(1.5, 'homok feltöltés', P(18, 19, 30, 0), 'fill'), (None, 'iszapos homok', P(19, 20, 28, 0), 'silty')],
                    loads=[('G_{z,k} = 320 kN', 0, PERM, 'r')], hload=('Q_{x,k} = 100 kN', 1, VAR), front='E_{0} → R_{p;d}', base='R_{d} (talp-súrlódás)', rear='E_{a}', **pad)
    F[12] = plan('p10', 2.0, 1.5, 0.4, ['G_{z,k} = 320 kN'], 'Q_{x,k} = 100 kN', 'a vízszintes teher a B oldallal párhuzamos')
    F[13] = section('m10u', 100, layers=[(1.6, 'homok feltöltés', P(18, 19, 30, 5), 'fill'), (None, 'agyag (kohézív)', P(19, 20, 0, 0, 65), 'clay')],
                    loads=[('G_{z,k} = 320 kN', 0, PERM, 'r')], hload=('Q_{x,k} = 100 kN', 1, VAR), base='R_{d} (talp-adhézió)', rear='E_{a}', **dict(pad, tfill=1.6))
    F[14] = section('m11', 78, 0.95, 0.95, 0.4, 2.05, [(3.0, 'homok feltöltés', P(19.5, 20.5, 32, 0), 'fill'), (None, 'iszap', P(19.5, 20.5, 16, 40), 'silt')],
                    [(['G_{z,k} = 490 kN', 'Q_{z,k} = 610 kN'], 0, PERM, 'r')], ('Q_{x,k} = 250 kN', 1, VAR), 2.05, None, 3.0,
                    note='Pilléralap (L = 1,45 m)', eb=0.04, front='E_{p} → R_{p;d} (passzív)', base='R_{d} (talp-súrlódás)', rear='E_{a}', cx=340, hw=0.7)
    F[15] = plan('p11', 0.95, 1.45, 0.4, ['G_{z,k} = 490 kN', 'Q_{z,k} = 610 kN'], 'Q_{x,k} = 250 kN', 'a vízszintes teher a B oldallal párhuzamos', eb=0.04)
    return F
if __name__ == '__main__':
    F = build()
    if '--out' in sys.argv:
        d = pathlib.Path(sys.argv[sys.argv.index('--out') + 1]); d.mkdir(parents=True, exist_ok=True)
        for k, v in F.items(): (d / f'fig{k:02d}.svg').write_text(v, encoding='utf-8')
        print('kiírva:', len(F)); sys.exit()
    p = ROOT / 'index.html'; s = p.read_text(encoding='utf-8'); ms = list(re.finditer(r'(<figure[^>]*>\s*)<svg.*?</svg>', s, re.S)); assert len(ms) == 16, len(ms)
    for k in sorted(F, reverse=True): m = ms[k]; s = s[:m.start()] + m.group(1) + F[k] + s[m.end():]
    p.write_text(s, encoding='utf-8'); print('beillesztve:', len(F))
