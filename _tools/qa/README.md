# Átnéző és ellenőrző eszközök

Helyi szerver a repó gyökerében (`python3 -m http.server 8851`), Playwright + Chromium szoftveres WebGL-lel.

| Eszköz | Mire való |
|---|---|
| `verify.py` | az N-táblázat és az MP1–MP11 mintapéldák független újraszámolása (nem az app kódja) |
| `calcs.py` | a mini-kalkulátorok és a kalkulátor-presetek számainak kiolvasása (HU ↔ EN összevetéshez) |
| `audit.py url hu\|en [szélességek] --tabs '#chTabs button'` | fejezetenként: túlcsordulás, lyukas sorkizárt sor, tiltott sorvég, dobozcím, U+200B (SVG-n kívül), konzolhiba, tétlen DOM-módosítás; angolban magyar szó és tizedesvessző |
| `tabs_full.py url mappa szélesség '#chTabs button'` | fejezetenként teljes oldalas kép |
| `scan.py`, `els.py`, `sheet.py`, `cvshots.py`, `figs2.py` | végigfényképezés, elem-, vászon- és ábraképek, áttekintő lapok |
| `../mpfig.py`, `../figpolish.py` | a mintapélda-ábrák paraméteres generátora és az elméleti ábrák egységesítője |
