#!/usr/bin/env python3
"""Az angol változat (en.html → /en) összeállítása a magyar index.html-ből.

Használat:  cd _i18n && npm install   (egyszer)
            python3 build_en.py
A magyar oldal (index.html) a forrás: azt szerkesztjük, utána ezt a szkriptet futtatjuk.
Az apply.mjs a fordítási egységeket (HTML-szövegek, attribútumok, a <script>-ek karakterláncai) az en_*.tsv
párjai szerint cseréli. Hiányzó fordításnál, hibás párnál vagy elcsúszott sorkulcsnál leáll; a hiányzók: missing.tsv.
"""
import os, pathlib, re, shutil, subprocess, sys
R = pathlib.Path(__file__).parent
ROOT = R.parent
OUT = R / '.en'
shutil.rmtree(OUT, ignore_errors=True); OUT.mkdir()
tsv = ','.join(str(p) for p in sorted(R.glob('en_*.tsv')))
r = subprocess.run(['node', str(R / 'apply.mjs'), str(ROOT), str(OUT), tsv, 'index.html'], capture_output=True, text=True,
                   env={**os.environ, 'STRICT': '1', 'NUMFIX': '1'})
print(r.stdout.strip())
if r.returncode:
    print(r.stderr[-2000:]); print('Az angol változat nem készült el (a hiányzó fordítások: _i18n/missing.tsv).'); sys.exit(1)
(R / 'missing.tsv').unlink(missing_ok=True)
s = (OUT / 'index.html').read_text()

def rep(a, b):
    global s
    assert s.count(a) == 1, a
    s = s.replace(a, b)

rep('<html lang="hu">', '<html lang="en-GB">')
rep('require: { "hu": "FORCEHYPHENOPOLY" }', 'require: { "en-gb": "FORCEHYPHENOPOLY" }')
s, n = re.subn(r"<script>/\*nyelv\*/.*?</script>\n", '', s); assert n == 1          # az átirányítás csak a magyar oldalon kell
rep('id="langSw" href="en" hreflang="en" lang="en"', 'id="langSw" href="./" hreflang="hu" lang="hu"')
# tizedesvessző → pont a le nem fordított HTML-szövegekben (képletek, számok) — a <script> és <style> blokkokon kívül
parts = re.split(r'(<script\b.*?</script>|<style\b.*?</style>)', s, flags=re.S)
for i in range(0, len(parts), 2):
    parts[i] = re.sub(r'>([^<]*)<', lambda m: '>' + re.sub(r'(?<=\d),(?=\d)', '.', m.group(1)) + '<', parts[i])
s = ''.join(parts)
(ROOT / 'en.html').write_text(s)
print('en.html', len(s) // 1024, 'KB')
