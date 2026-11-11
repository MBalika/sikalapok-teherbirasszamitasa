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
