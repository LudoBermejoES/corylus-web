# Website screenshots

Real captures of the Corylus app as WebP, 2208x1242 (a 1472x828 viewport at 1.5x), taken
from the e2e dev build with `web/tools/shots.mjs`. The copy refers to them by id.

| id | What it shows |
|---|---|
| `editor` | Hero. Binder with the Manuscript and Drafts folders (labels, status badges), the chapter "By the Lake" in the Novela preset, the inspector with synopsis, label and status. |
| `corkboard` | The Manuscript folder as index cards: synopsis, label colour bar, status. |
| `outliner` | The same folder as outliner rows: title, synopsis, label, status, words. |
| `continuous` | The six chapters read as one scroll. |
| `story-bible-entry` | Victor Frankenstein's character sheet: portrait, role, want/need, ghost-to-truth spine, goal/motivation/conflict. |
| `relationship-map` | Relationship map: four portrait cards, edges labelled "creator of", "lives at", "betrothed to". |
| `analysis-repetition` | Repeated words highlighted in a rough draft, with the hover tooltip ("night" appears 3 times). |
| `analysis-structure` | Same sentence openings and a run of equal-length sentences marked. |
| `analysis-style` | Adverbs, gerunds and adjectives marked in colour. |
| `rhyme` | End rhymes underlined (light / bright / sight / white / night). |
| `thesaurus` | Right-click on "happier": the Synonyms (and Antonyms) menu. |
| `grammar` | LanguageTool flagging "He have waited", with its suggestion menu. |
| `distraction-free` | Distraction-free mode over a background video, with the HUD (width, opacity, text size, fullscreen). |
| `ambient-sounds` | The ambient sounds mixer: presets, and a mix of Rain on Window and Campfire (paused). |
| `snapshots` | The Snapshots tab: three snapshots and the diff of "First draft" against the current text. |
| `compile` | The compile dialog: scope tree, status filter, format, Word / PDF / EPUB. |
| `read-aloud` | Read aloud paused on the first sentence: highlighted sentence and the player bar. |
| `comments` | A comment thread on a highlighted passage. |
| `sync` | Settings > Cloud Sync, the provider list open (pCloud, Google Drive, Dropbox, OneDrive, Box, Amazon S3…). |
| `backups` | Settings > Backups & Snapshots: interval, last backup, backup history with Restore. |
| `themes` | The chapter "The Spark" in the Catppuccin Mocha theme with the Night page. |
| `spanish` | The interface in Spanish, with a Spanish chapter ("I. La llegada") and its inspector. |
| `statistics` | Project Statistics for the Manuscript folder: words, pages, reading time, word frequency. |
| `methodology` | The Methodology Wizard: plot-structure and character methods. |
| `diagnostics` | Settings > About with the Send diagnostics dialog on top: the template description ("What I was doing, what I expected, and what happened instead."), name and email empty, the notice about what travels. Never sent: closed with Cancel after capture. |

## Re-capturing

The demo books are built by the script, never a real project:
`C:\tmp\corylus-site\Frankenstein.corylus` (the e2e demo seed's Story Bible plus six
chapters, a rough draft, snapshots) and `C:\tmp\corylus-site\El faro de Arnela.corylus`
(Spanish). The prose lives in `web/tools/shots-content.mjs`.

On Windows, with the dev app running with the e2e bridge and the WebView2 debug port
(`WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS=--remote-debugging-port=9222`, as the video
engine needs):

```powershell
cd C:\code\corylus\web\tools
node shots.mjs --seed          # (re)build both demo books
node shots.mjs                 # every shot
node shots.mjs editor themes   # just these ids
```

## Spanish set (`es/`)

`es/<id>.webp` are the same shots for the Spanish site: Spanish interface and a Spanish
book, `C:\tmp\corylus-site\Frankenstein (es).corylus` (Frankenstein retold in Spanish so
the four demo portraits fit; prose, Story Bible and relationship labels such as
"creador de" / "creado por" in `web/tools/shots-content-es.mjs`). The page prefers these
and falls back to the English shot per id. There is no `es/spanish.webp`: the English
`spanish` shot already shows the Spanish interface, so the fallback covers it.

```powershell
node shots.mjs --lang es --seed   # (re)build the Spanish book
node shots.mjs --lang es          # every shot into es/
```

The Spanish thesaurus is a download; the `thesaurus` shot installs it into the e2e app on
first run. Proper names the bundled Spanish dictionary lacks (Elizabeth, Londres…) are
ignored for the session so only the planted misspelling ("inmediatamante") is flagged.
The run always ends with the app back in English.

The script leaves the app light, English, with every analysis off. 24 Spanish shots: about 2.7 MB.

Each shot is written straight from WebView2 as lossy WebP, quality 85, rendered
at 1.5x (2208x1242). No post-processing step. `SHOTS_SCALE=2` renders at 2x
(2944x1656) instead. The script also turns off LCD (ClearType) text antialiasing
while it captures, so letter edges carry no colour fringes. Total for the 25 shots: about 2.7 MB.

Side effects, all inside the e2e app's own data: `grammar` starts LanguageTool,
`sync` starts the rclone engine (it never connects), `ambient-sounds` installs the
sound pack on first run, `distraction-free` stores a background video
(`assets/distractionfree-wallpaper/videos/abstract/18849-297379170_medium.webm`),
`read-aloud` plays about two seconds of audio, and `backups` writes up to three
backups to `C:\tmp\corylus-site\Corylus backups`.
