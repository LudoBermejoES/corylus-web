# corylus-web

The website for [Corylus](https://github.com/LudoBermejoES/corylus) — a writing
tool that treats your words as yours. A static, bilingual GitHub Pages site whose
job is to explain Corylus well enough that someone downloads it, and to support
it.

**Live:** https://corylus.ludobermejo.es/

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
  videos/<lang>/  Poster per video (WebP, 1280x720), see Videos below
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

- [x] Ko-fi: `KOFI` in `build.py` is set; the support section renders from it.
- [ ] Re-shoot `sync.webp` and `backups.webp` (EN and ES): they predate the 1.94 Settings redesign.
- [ ] If a custom domain is ever added, put it in `CNAME` and update `SITE` in
      `build.py`, plus `robots.txt` and `sitemap.xml`.

## Brand

Colours, type and logo rules come from
[corylus-corpo](https://github.com/LudoBermejoES/corylus-corpo). Do not invent new
ones here; change them there and copy across.

## Videos

`VIDEOS` in `build.py` holds each slot's YouTube id and length per language; a slot
with no id for a language renders nothing, so video 12 (`extras`) goes live by
filling in its two ids. Copy is in `STRINGS[lang]["videos"]`. Posters are local, so
the page asks YouTube for nothing until someone presses play (`site.js` then swaps
in a youtube-nocookie iframe). Plan and privacy rules: `VIDEO-PLAN.md`.

Posters come from the masters, frame at 0.4 s (before the burned-in subtitle):

```sh
ffmpeg -ss 0.4 -i <master>.mp4 -frames:v 1 -vf scale=1280:720 -c:v libwebp -quality 80 assets/videos/<lang>/<slot>.webp
```
