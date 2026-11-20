# Angol változat (en.html → /en)

A magyar `index.html` a forrás. Szerkesztés után:

    cd _i18n
    npm install          # egyszer (acorn, acorn-walk, parse5)
    python3 build_en.py  # → ../en.html

- `en_page.tsv` – az oldal HTML-szövegei és attribútumai, `en_script.tsv` – a `<script>` blokkok karakterláncai,
  `en_keys.tsv` – sorhoz kötött kulcsok (kódban kulcsként is használt szavak, pl. talajnevek).
- Sorformátum: `<azonosító><TAB><angol>`; az azonosító a magyar szöveg sha1-ének első 7 jegye
  (`node -e "import('./catalog.mjs').then(m=>console.log(m.hid('magyar szöveg')))"`). `=` → változatlan, `⏎` → sortörés.
- Ha a magyar szöveg változik, a build leáll, és a hiányzó egységeket a `missing.tsv`-be írja: ezeket kell lefordítani.
- Az angol oldal: `lang="en-GB"`, en-gb elválasztás, tizedespont; a HU | EN váltó a választást megjegyzi (`localStorage 'alap-lang'`).

## Segédeszközök szövegváltozás után

- `python3 rekey.py [<git-rev>]` – a sorhoz kötött kulcsok (`en_keys.tsv`) átszámozása, ha a magyar forrás sorai elcsúsztak
  (a kulcsoknak a megadott revízióra kell érvényesnek lenniük; alapértelmezés: HEAD).
- `node carry.mjs <régi index.html könyvtára>` majd `python3 carry.py` – fordítás-átvitel: a megváltozott magyar egységekhez
  megkeresi a korábbi változat fordítását; a nyelvfüggetlen változásokat (számok, jelölések, HTML-jelek) automatikusan átvezeti
  (`carry_auto.tsv`), a többit `carry_todo.txt`-be írja kézi fordításra.
- `python3 prune.py` – a már nem használt fordítási sorok törlése (a build `unused.txt` listája alapján).
- Kódnak osztályozott (`code`) karakterlánc fordítása: `<azonosító>!<TAB><angol>` (minden előfordulásra, osztálytól függetlenül).
- A csak számot, jelet és indexet tartalmazó képletcímkékben (pl. `V<sub>d</sub> = 1,35·G<sub>k</sub>`) a tizedesvessző
  automatikusan ponttá válik (`units.mjs: numLike`).
