# corylus-web

The website for [Corylus](https://github.com/LudoBermejoES/corylus) — a writing
tool that treats your words as yours. A static, bilingual GitHub Pages site whose
job is to explain Corylus well enough that someone downloads it, and to support
it.

**Live:** https://ludobermejoes.github.io/corylus-web/

## Editing the copy

Both language versions are generated from one source. **Edit `build.py`, never
`index.html` or `es/index.html`** — those are overwritten on every build.

```sh
python3 build.py
```

`STRINGS["en"]` and `STRINGS["es"]` hold every piece of text, side by side, so a
change to one language is impossible to forget in the other. The structure comes
from a single template, so the two pages cannot drift apart.

## Layout

```
index.html        English   (generated)
es/index.html     Spanish   (generated)
404.html          Bilingual not-found page
build.py          Content and template — the only file to edit for copy
assets/
  style.css       Brand tokens from corylus-corpo
  site.js         Resolves download links against the live release manifests
  lockup*.svg     Logo, light and dark
  mark.svg        Mark, used in the footer
  favicon.svg     Small mark (three text lines, legible at 16px)
  og.png          1200x630 social preview
robots.txt, sitemap.xml, .nojekyll
```

## Download links

The buttons point at the real installers in
[corylus-releases](https://github.com/LudoBermejoES/corylus-releases). The HTML
ships a hard-coded fallback link, and `assets/site.js` then reads
`latest-darwin-aarch64.json` and `latest-windows-x86_64.json` at page load and
rewrites the links to whatever is actually published.

**So the site does not need rebuilding when a new version ships.** The fallbacks
in `build.py` (`FALLBACK`) only matter when JavaScript is off; refresh them
whenever it is convenient, not urgently.

## Before launch

- [ ] Set `PATREON` in `build.py`. The support section renders only when it is
      non-empty, so the site never ships a dead link — but that also means the
      ask is currently invisible.
- [ ] Add screenshots. The page argues entirely in prose right now. The one image
      that matters is the manuscript in the app beside the same text as a `.md`
      file in the file manager — see
      [`corylus-corpo/social/asset-specs.md`](https://github.com/LudoBermejoES/corylus-corpo/blob/main/social/asset-specs.md).
- [ ] If a custom domain is ever added, put it in `CNAME` and update `SITE` in
      `build.py`, plus `robots.txt` and `sitemap.xml`.

## Brand

Colours, type and logo rules come from
[corylus-corpo](https://github.com/LudoBermejoES/corylus-corpo). Do not invent new
ones here; change them there and copy across.
