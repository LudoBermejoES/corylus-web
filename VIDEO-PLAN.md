# The video series on the website: plan and copy

Brief for whoever builds it. Copy is final unless marked **[CHECK]**. Nothing here
is built yet; `build.py` is untouched.

Sources: `~/.config/corylus/upload_state.series-2026-11.json` (IDs),
`.claude/skills/corylus-youtube/metadata/series-2026-11.json` (titles and
descriptions), the masters in `C:\code\corylus-video-masters\2026-11-22\`
(durations measured with ffprobe). All 21 video IDs and both playlists were
checked on 2026-11-22 and are public. The channel is `@corylus-editor`.

---

## 1. Where each video goes

### The rule

- **One player per place, next to the screenshots that show the same thing.** A
  group's video goes straight after the group's lead paragraph (`<p class="lead">`
  in `tour()`), before its feature rows. Read aloud is the one exception: it sits
  beside the `read-aloud` feature row, because the Revise group already opens
  with the craft-tools video.
- **Each page gets its own language's videos.** The English page uses only the
  English videos; the Spanish page uses only the Spanish ones.
- **A slot with no video renders nothing**, the same way `shot_img()` returns ""
  when a capture is missing. That is how video 12 waits for its upload.

### Placement table

| # | Video | Place on the page | Next to | EN id | EN length | ES id | ES length |
|---|---|---|---|---|---|---|---|
| 01 | Trailer | Hero, in `figure.media`, **replacing the editor screenshot** | the hero copy and download buttons | `fz2q5GGS75w` | 1:25 | `NrK_Sep8m0g` | 1:44 |
| 02 | Your words | Tour group `safety` | snapshots, backups, sync | `hZ1cwTO7igA` | 4:12 | `8y8laprSBSA` | 5:13 |
| 03 | Two hundred pieces | Tour group `structure` | corkboard, outliner | `N-0uLr5TS2s` | 3:41 | `J0I9Ukqst14` | 4:16 |
| 04 | Craft tools | Tour group `revise` | repetition, structure, style, rhyme | `obfF5Uef2rQ` | 2:22 | `b4rsl6WUxsw` | 3:00 |
| 05 | Workshop diary 2 | **Not in the tour.** Section `#support`, as "From the workshop" | the Ko-fi ask | `qkOYZW6D9UA` | 2:10 | `1AALrm2ANbs` | 2:41 |
| 06 | Story bible | Tour group `bible` | entry, relationship map | `P4cMXc4OirQ` | 3:34 | `u6rPogkU30Q` | 4:12 |
| 07 | Writing environment | Tour group `environment` | distraction-free, ambient sounds, themes | `kN2WJV-iD6Y` | 2:34 | `uVxwszwxb-U` | 3:01 |
| 08 | Finishing | Tour group `finish` | compile | `0gLDxraAzQ4` | 1:26 | `3u5rcd4sC4w` | 1:42 |
| 09 | The desk | Tour group `writing` | binder/tabs, comments, find, statistics | `jqCa2NjBkWo` | 1:42 | `AQ-8G3jMrxM` | 2:03 |
| 10 | En español | Tour group `languages`, **ES page only** | the Spanish feature | none (see below) | | `LZ2FLWUHbE4` | 2:30 |
| 11 | Read aloud | Tour group `revise`, beside the `read-aloud` feature row | read-aloud screenshot | `ZA-lxCCVUzM` | 1:00 | `QPjC2yXTsQk` | 1:08 |
| 12 | The AI parts | Tour group `extras`, **reserved** | assistant, MCP | not uploaded | | not uploaded | |

Playlists: EN `PLM2yuZIkkOv4` → `https://www.youtube.com/playlist?list=PLM2yuZIkkOv4`,
ES `PLAx-paBq5bo8` → `https://www.youtube.com/playlist?list=PLAx-paBq5bo8`.

Why these choices:

- **Trailer replaces the hero screenshot.** Its poster frame already shows a
  chapter open in Corylus, so the hero loses nothing. The same editor
  screenshot stays on the page in `#why` ("The same chapter, twice"). The
  existing CSS comment in `style.css` ("heading, lead, buttons and the trailer
  share one left edge") shows the hero was laid out for a video here before.
- **02 goes in `safety`, not `#why`.** Three of its four failures are snapshots,
  backups and the index, which is where the `safety` screenshots are. `#why` is
  already two blocks deep.
- **03 goes in `structure`, 09 in `writing`.** 03's title is binder, corkboard and
  outliner, and the corkboard and outliner screenshots live in `structure`. 09
  (tabs, split panes, comments, search, targets) matches the `writing` group
  feature for feature.
- **10 on the English page** gets a plain text link in the `languages` group, not
  a player (copy below). A link loads nothing until it is clicked. The English
  craft-tools description already points English viewers to it the same way.
- **The workshop diary goes in `#support`.** It is dated by nature (it covers up
  to 1.93.3) and the tour describes the current app. On the support section it
  shows what the time goes on. Keep it as a single "latest diary" slot, so
  Diary 3 replaces it by changing one ID.

### "Watch the tour": a list, not a second set of players

Add a short block with `id="videos"` at the end of `section.tour-head`. It holds
a heading, one line, an ordered list of the tour videos, and the playlist link.
Each list item is an **in-page link to the group** where that video's player
sits (`#safety`, `#bible`…), with the length. It contains no players or posters,
so it costs nothing and duplicates nothing.

- Order: the series order (01 to 11; 05 is left out of this list, since it is not
  a tour video and has its own place).
- Count the videos from the data, so video 12 updates the number by itself.
- Under the trailer, a text link points to `#videos`.
- Header nav: leave it as it is. On phones the CSS already hides every in-page
  anchor except Download.

### Suggested data shape (for `build.py`)

A single dict, next to `TOUR`, so both languages read from one place:

```python
# slot -> {lang: (youtube id, length)}; poster = assets/videos/<lang>/<slot>.webp
VIDEOS = {
    "hero":        {"en": ("fz2q5GGS75w", "1:25"), "es": ("NrK_Sep8m0g", "1:44")},
    "writing":     {"en": ("jqCa2NjBkWo", "1:42"), "es": ("AQ-8G3jMrxM", "2:03")},
    # … one entry per row of the table; "read-aloud" for the feature-row slot,
    # "support" for the diary, "languages" with "es" only, "extras" empty until 12 lands.
}
```

Copy (titles and captions) goes in `STRINGS[lang]["videos"][slot]` as
`(short title, caption)`, like `feats`.

---

## 2. Copy

House voice: plain, first person singular, no exclamation marks. Spanish is
written in Spanish, in *tú*. The videos carry the detail, so each caption is one
or two sentences.

### Trailer (hero)

| | EN | ES |
|---|---|---|
| Caption | The trailer: one chapter in Corylus, the same chapter as a file on disk, and the rest of the app in a minute and a half. | El tráiler: un capítulo en Corylus, ese mismo capítulo como archivo en el disco y el resto del programa, en menos de dos minutos. |
| Link under it | The whole tour: {n} short videos | El recorrido entero: {n} vídeos cortos |

`{n}` = number of tour videos on that page (EN 9, ES 10 today, the trailer
included; +1 when video 12 lands). The link points to `#videos`.

### "Watch the tour" block (`#videos`, in `tour-head`)

| | EN | ES |
|---|---|---|
| Heading (h3) | Watch the tour | Mira el recorrido |
| Line | Short videos, one part of Corylus each, filmed on demo books. Each one also sits next to the part of this page it shows. I wrote them; the narrator is a synthetic voice. | Vídeos cortos, cada uno sobre una parte de Corylus, grabados con libros de ejemplo. Cada uno está también junto a la parte de esta página que enseña. Los he escrito yo; la voz que narra es sintética. |
| Playlist link | Open the playlist on YouTube | Abre la lista en YouTube |

List item format: `{short title} · {length}`.

### Per video: short title and caption

Short titles are for the list and the player's accessible name. The YouTube
titles are search titles; don't reuse them on the site.

**English**

| Slot | Short title | Caption |
|---|---|---|
| hero | The trailer | (above) |
| writing (09) | The desk | Tabs and split panes, comments, a search of the whole book and word targets: the part you use every day. |
| structure (03) | Two hundred pieces | Binder, corkboard and outliner over the same plain files, and how to bring a book in from Scrivener or Word. |
| bible (06) | The Story Bible | Characters, places and their relationships, filmed with the cast of Frankenstein. The map draws its lines from the entries, so the two cannot disagree. |
| revise (04) | When you stop seeing your words | The marks for repeated words, monotonous rhythm and accidental rhyme. Each one is off until you switch it on, and none of them rewrites a word. |
| read-aloud (11) | Read aloud | Corylus reads your chapter one sentence at a time and keeps that sentence lit. One minute. |
| environment (07) | Just you and the text | Distraction-free mode, a video behind the page, ambient sounds, focus mode and themes. Escape brings everything back. |
| safety (02) | Four ways to lose a book | Four failures, from the app disappearing to a dead computer, and what is still on your disk after each one. |
| finish (08) | Compile | The book put back together in Binder order and exported to Word, PDF or EPUB, inside Corylus, with nothing else to install. |
| extras (12) | The optional AI parts | **[CHECK against the final video]** The assistant that runs on your computer, and how an AI app such as Claude connects to a project, with a permission you set per project. Both stay off until you install them. |
| languages (EN page, link only) | | Link label: **There is also a video about writing in Spanish, narrated in Spanish.** → `https://youtu.be/LZ2FLWUHbE4` |

**Español**

| Slot | Título corto | Pie |
|---|---|---|
| hero | El tráiler | (arriba) |
| writing (09) | La mesa de trabajo | Pestañas y dos paneles, comentarios, búsqueda en todo el libro y objetivos de palabras: lo que usas a diario. |
| structure (03) | Doscientas piezas | La Carpeta, el Tablero y el Esquema sobre los mismos archivos de texto, y cómo traer un libro desde Scrivener o Word. |
| bible (06) | La Biblia de la historia | Personajes, lugares y sus relaciones, con el reparto de Frankenstein. El mapa saca sus líneas de las entradas, así que no puede contradecirlas. |
| revise (04) | Dejas de ver tus propias palabras | Las marcas de palabras repetidas, ritmo monótono y rimas involuntarias. Todas están apagadas hasta que las enciendes, y ninguna reescribe nada. |
| read-aloud (11) | En voz alta | Corylus te lee el capítulo frase a frase y deja iluminada la que está leyendo. Un minuto. |
| environment (07) | Solo tú y el texto | El modo sin distracciones, un vídeo detrás de la página, sonidos ambientales, el modo enfoque y los temas. Con Escape vuelve todo a su sitio. |
| safety (02) | Cuatro formas de perder un libro | Cuatro fallos, desde que el programa desaparece hasta que el ordenador se muere, y lo que sigue en tu disco después de cada uno. |
| finish (08) | Compilar | Las piezas juntas otra vez en el orden de la Carpeta y exportadas a Word, PDF o EPUB, dentro de Corylus y sin instalar nada más. |
| languages (10) | En español | Repeticiones contadas por la raíz, rima consonante y asonante, comillas angulares y comprobaciones que solo existen en español. |
| extras (12) | Las partes opcionales con IA | **[CHECK con el vídeo final]** El asistente que funciona en tu ordenador, y cómo se conecta a un proyecto una aplicación de IA como Claude, con el permiso que tú das proyecto a proyecto. Las dos están apagadas hasta que las instalas. |

### Workshop diary (`#support`)

Put it after the Ko-fi button, so the ask stays where it is.

| | EN | ES |
|---|---|---|
| Heading (h3) | From the workshop | Desde el taller |
| Line | Now and then I film what I built, what broke and what is still not right. The latest: | De vez en cuando grabo lo que he hecho, lo que se ha roto y lo que todavía no va bien. El último: |
| Short title | Workshop diary 2: the map that deleted its own lines | Diario de taller 2: el mapa que borraba sus propias líneas |
| Caption | Up to version 1.93.3. A relationship map could delete relationships from your files when you moved a card. This is why, and how it was fixed. | Hasta la versión 1.93.3. Un mapa de relaciones podía borrar relaciones de tus archivos al mover una tarjeta. Por qué pasaba y cómo se arregló. |

### Player labels (every player)

| | EN | ES |
|---|---|---|
| Play button, accessible name | Play “{short title}” (loads YouTube) | Reproducir «{título corto}» (carga YouTube) |
| Note under each player | The video plays from YouTube, which loads only when you press play. | El vídeo se reproduce desde YouTube, que solo se carga cuando le das a reproducir. |
| Link in that note | Watch on YouTube | Verlo en YouTube |
| Length badge | `1:25` (no word needed) | `1:44` |
| iframe `title` | the short title | el título corto |

---

## 3. Privacy requirements

The site promises "no cookies, no analytics". It has to stay true for every
visitor who never presses play, and stay accurate for those who do.

### Hard requirements

1. **Nothing from YouTube before a click.** No `<iframe>` in the HTML, not even
   with `loading="lazy"` (a lazy iframe still loads when it nears the viewport).
   No requests to `youtube.com`, `youtube-nocookie.com`, `ytimg.com`,
   `googlevideo.com` or `doubleclick.net` on page load or scroll. No
   `<link rel="preconnect">` or `dns-prefetch` to them. No YouTube thumbnail URLs
   (`i.ytimg.com/vi/…`). No oEmbed calls, no YouTube IFrame API script, no
   lite-youtube library that warms connections on hover.
2. **Posters are local files.** One WebP per video per language, under
   `web/assets/videos/<lang>/<slot>.webp` (for example `assets/videos/es/languages.webp`).
3. **The swap happens only on click.** On a plain left click (no modifier keys,
   the same test the lightbox in `site.js` uses), replace the poster with:

   ```html
   <iframe src="https://www.youtube-nocookie.com/embed/{ID}?autoplay=1&rel=0&playsinline=1"
           title="{short title}" allow="autoplay; encrypted-media; picture-in-picture; fullscreen"
           allowfullscreen referrerpolicy="strict-origin-when-cross-origin"></iframe>
   ```

   - Keep `referrerpolicy="strict-origin-when-cross-origin"`. YouTube now refuses
     embeds that send no referrer (player error 153), so `no-referrer` breaks
     the player.
   - Move focus into the iframe after the swap.
   - No `cc_load_policy`: the subtitles are burned into the masters.
4. **It still works without JavaScript.** The poster is an `<a>` to
   `https://www.youtube.com/watch?v={ID}`, so a click with JS off (or a
   Ctrl/Cmd-click) opens YouTube in the normal way. That is also a click, so it
   keeps the promise.
5. **A note under each player** (copy above) says it loads YouTube.
6. **Optional guard:** `<meta http-equiv="Content-Security-Policy" content="frame-src https://www.youtube-nocookie.com">`
   in `<head>`. It restricts only frames, so Google Fonts and the manifest
   fetches are unaffected, and an accidental `youtube.com` embed fails loudly.

### Poster frames: take them at 0.4 s, not 1 s

Every master has a burned-in subtitle from 0.6–0.7 s onward, so the 1 s frame
has a caption bar across the bottom. At 0.4 s the tour videos show their clean
title card (big number, title, subtitle, Corylus mark). The trailer shows the
app with a chapter open. Both were checked by eye.

```sh
# per video; 1280 wide is enough for the widest column, ~40-90 KB each
ffmpeg -ss 0.4 -i "<master>.mp4" -frames:v 1 -vf scale=1280:-2 -c:v libwebp -quality 80 web/assets/videos/<lang>/<slot>.webp
```

`build.py` already has `webp_size()`; use it for `width`/`height` so the box
does not shift (or set `aspect-ratio: 16 / 9`). The hero poster is the page's
largest image: no `loading="lazy"`, and add `fetchpriority="high"`. Every other
poster is lazy.

### Player look (for the designer, from the house rules)

- A play button that is Corylus's own (brand tokens in `style.css`), not the
  YouTube logo, with a 44 px minimum target and a visible focus ring.
- The length badge sits on the poster. The note goes under it in `.note` style.
- Nothing moves before the click, so `prefers-reduced-motion` needs no special
  case. Autoplay happens only after the click, which is what the visitor asked for.

### Acceptance check

Load `/` and `/es/` in a fresh profile, scroll to the bottom and hover every
poster. DevTools → Network, filtered by
`youtube|ytimg|googlevideo|doubleclick`, shows **zero** requests. Application →
Cookies shows **none** for any domain. Then press play once: the requests that
appear go to `youtube-nocookie.com` (and from there to YouTube's other servers).

### The privacy page needs a new paragraph

It does: the page names every third party the site talks to (GitHub, Google
Fonts), so YouTube has to be named too. In `PRIVACY[lang]["sections"]`, section
"This website" / "Esta web":

**Change** "It sets no cookies and runs no analytics." →
"It sets no cookies of its own and runs no analytics." Before a click there are
none at all. After a click, YouTube's player may set its own, and "of its own"
keeps the sentence true.
ES: "No pone cookies ni usa analítica." → "No pone cookies propias ni usa analítica."

**Add** as a second paragraph of that section:

> EN: The videos on this site are on YouTube. Until you press play on one, your
> browser asks YouTube for nothing: the picture you see is a still image stored
> on this site. When you press play, the player loads from youtube-nocookie.com.
> YouTube then sees the request and your IP address, and from then on it may
> store data in your browser under Google's privacy policy. The links to the
> playlists open YouTube itself.

> ES: Los vídeos de esta web están en YouTube. Hasta que le das a reproducir
> uno, tu navegador no le pide nada a YouTube: la imagen que ves es una foto fija
> guardada en esta web. Al darle a reproducir, el reproductor se carga desde
> youtube-nocookie.com. YouTube ve entonces la petición y tu dirección IP, y a
> partir de ahí puede guardar datos en tu navegador según la política de
> privacidad de Google. Los enlaces a las listas abren el propio YouTube.

Also update `"updated"` on both privacy pages to the day this ships. The
`description` meta ("Corylus collects nothing…") is about the app and stays as
it is.

---

## 4. What is out of date on the site (noted only, not rewritten)

1. **Assistant (`feats.assistant`, both languages).** It doesn't mention the
   graphics card (1.96), and "about 4 to 8 GB" is probably wrong now: the model
   catalog includes `qwen3:1.7b`, 1.95.2 suggests a model sized to the
   computer's memory, and video 12 says "a few gigabytes". **[CHECK]** the sizes
   against the catalog. A sentence to add: "On Windows it can run on an NVIDIA,
   AMD or Intel graphics card, which answers much faster; Corylus downloads only
   the add-on that card needs." (ES: "En Windows puede funcionar en una tarjeta
   gráfica NVIDIA, AMD o Intel, que responde mucho más deprisa; Corylus descarga
   solo el complemento que necesita esa tarjeta.") The mascot window, which
   video 12 shows, isn't on the site at all.
2. **Gallery links (1.95).** `feats.distraction-free` says "There is a gallery
   of backgrounds to download". Since 1.95 the gallery page
   (https://ludobermejoes.github.io/corylus-distractionfree-wallpaper) has
   "Add to Corylus", which shows the size, credit and licence and asks before
   downloading, and Settings lists "My backgrounds". Worth one sentence and a
   link.
3. **Settings redesign (1.94).** `sync.webp` and `backups.webp` (EN and ES) were
   captured on 21 November, before the redesign, so they show the old Settings.
   Recapture both. Their alt texts and captions name old pages: "Settings, Cloud
   sync" and "Settings, Snapshots & Backups" are now **Cloud Sync** and
   **Backups & Snapshots** (ES **Nube** and **Copias e instantáneas**).
   `themes`/typography moved into project settings too, but no copy names that page.
4. **An exclamation mark in the hero.** `hero_p2` ends "And it's free!" / "¡Y es
   gratis!", which breaks the house rule for product copy. Suggested fix: "It's in
   English and Spanish, for Mac and Windows, and it's free." / "Está en español e
   inglés, para Mac y Windows, y es gratis."
5. **The old self-hosted trailer.** `assets/corylus-trailer.mp4` (2.9 MB),
   `corylus-trailer.vtt` and `trailer-poster.jpg` are referenced by nothing and
   show an older app. Delete them when the new trailer goes in. If YouTube is
   unwanted even after a click, there is another route for the hero only:
   self-host the new trailer (the EN master is 7.9 MB at 1080p, less once
   re-encoded) in a plain `<video preload="none" poster=…>`. That loads nothing
   from a third party at all.
6. **`web/README.md` "Before launch"** still says to set `PATREON` and add
   screenshots. Both are done, and Patreon is cancelled.
7. **The Windows certificate price.** The site and `corpo/kofi/` say "about €253
   a year, VAT included". `BRAND.md` §8 and `.agents/product-marketing.md` say
   "about €209". These agree (209 + 21 % VAT ≈ 253), but the brand files should
   say "€209 + VAT" so nobody "corrects" the site downwards.
