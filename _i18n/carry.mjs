// Fordítás-átvitel szövegváltozás után: a régi (git) index.html egységeit a mostaniakhoz párosítja.
// használat: python3 build_en.py (→ missing.tsv), majd: node carry.mjs <régi index.html könyvtára>  → carry.json (hiányzó egységek: új HU, legközelebbi régi HU, régi EN)
import fs from 'node:fs'; import path from 'node:path'; import { collect } from './catalog.mjs';
const oldRoot = process.argv[2];
const tsv = (f) => { const m = new Map(); for (const l of fs.readFileSync(f, 'utf8').split('\n')) { if (!l || l.startsWith('#')) continue; const i = l.indexOf('\t'); if (i < 0) continue; m.set(l.slice(0, i), l.slice(i + 1)); } return m; };
const T = new Map([...tsv('en_page.tsv'), ...tsv('en_script.tsv')]);
const txt = (u) => u.t;
const NEW = collect('..', ['index.html']), OLD = collect(oldRoot, ['index.html']);
const oldById = new Map(); for (const u of OLD) if (!oldById.has(u.id)) oldById.set(u.id, u);
const newIds = new Set(NEW.map((u) => u.id));
const gone = [...oldById.values()].filter((u) => !newIds.has(u.id) && T.has(u.id));
const bi = (s) => { const m = new Map(); for (let i = 0; i < s.length - 1; i++) { const k = s.slice(i, i + 2); m.set(k, (m.get(k) || 0) + 1); } return m; };
const sim = (a, b) => { const A = bi(a), B = bi(b); let c = 0; for (const [k, v] of A) c += Math.min(v, B.get(k) || 0); return 2 * c / (a.length + b.length - 2 || 1); };
const out = []; const seen = new Set();
const MISS = new Set(fs.readFileSync('missing.tsv', 'utf8').split('\n').map((l) => l.split('\t')[0]).filter(Boolean));
for (const u of NEW) { if (!MISS.has(u.id) || seen.has(u.id)) continue; seen.add(u.id); const t = txt(u); let best = null, bs = 0; for (const g of gone) { const s = sim(t, txt(g)); if (s > bs) { bs = s; best = g; } }
  out.push({ id: u.id, js: !!u.q, line: u.line, hu: t, sim: +bs.toFixed(3), oldId: best?.id, oldHu: best ? txt(best) : null, oldEn: best ? T.get(best.id) : null }); }
fs.writeFileSync('carry.json', JSON.stringify(out, null, 1)); console.log('hiányzó:', out.length, '· párosítva (≥0,6):', out.filter((o) => o.sim >= 0.6).length);
