#!/usr/bin/env python3
"""Build the Corylus site: one content source, one template, two languages.

    python3 build.py

Writes index.html (English) and es/index.html (Spanish). Edit the copy in
STRINGS below — never the generated HTML, which is overwritten on every run.
"""
import html
import os
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = "https://corylus.ludobermejo.es"
RELEASES_RAW = "https://raw.githubusercontent.com/LudoBermejoES/corylus-releases/main"

# Fill this in once the Ko-fi page exists; the support section hides itself
# while it is empty, so the site never ships a dead link.
KOFI = "https://ko-fi.com/corylus"

# The versions baked into the HTML, used when JavaScript is off: site.js rewrites
# the links from the live manifests for everyone else. Fetched at build time so
# they cannot quietly rot - they had drifted two releases behind before this.
# Offline, the last known values below are used and the build says so.
_FALLBACK_LAST_KNOWN = {"mac": "1.91.1", "win": "1.91.1"}


def _published_versions():
    """Copy each platform's update manifest into the site root, byte for byte, and
    return the versions they carry.

    The app's updater asks https://corylus.ludobermejo.es/latest-<target>-<arch>.json
    first (releases repo second), so this copy is what publishes an update on the
    domain. It reads the local ../releases checkout when there is one — exactly
    what was just pushed — and fetches the raw URL otherwise, which a CDN may
    serve a few minutes stale."""
    import glob
    import json as _json
    import urllib.request

    local = os.path.join(HERE, "..", "releases")
    names = sorted({os.path.basename(p) for p in glob.glob(os.path.join(local, "latest-*-*.json"))}
                   | {"latest-darwin-aarch64.json", "latest-windows-x86_64.json"})
    out = dict(_FALLBACK_LAST_KNOWN)
    for name in names:
        try:
            src = os.path.join(local, name)
            if os.path.exists(src):
                with open(src, "rb") as f:
                    raw = f.read()
            else:
                with urllib.request.urlopen(f"{RELEASES_RAW}/{name}", timeout=10) as r:
                    raw = r.read()
            version = _json.loads(raw)["version"]
        except Exception as exc:
            print(f"  ! {name}: {exc} — not copied")
            continue
        with open(os.path.join(HERE, name), "wb") as f:
            f.write(raw)
        key = {"latest-darwin-aarch64.json": "mac", "latest-windows-x86_64.json": "win"}.get(name)
        if key and version:
            out[key] = version
    return out


FALLBACK = _published_versions()

# The feature tour, in page order: (group id, [(feature key, screenshot id or None)]).
# Copy lives in STRINGS[lang]["groups"] and ["feats"]; screenshot ids are the ones in
# the shared shot list, captured to assets/shots/<id>.png. A feature whose shot has not
# been captured yet drops into the group's text-only list instead of breaking the page.
TOUR = [
    ("writing", [("binder", None), ("continuous", "continuous"), ("inspector", None),
                 ("comments", "comments"), ("find", None), ("typing", None),
                 ("statistics", "statistics")]),
    ("structure", [("corkboard", "corkboard"), ("outliner", "outliner"),
                   ("methodology", "methodology")]),
    ("bible", [("story-bible-entry", "story-bible-entry"),
               ("relationship-map", "relationship-map"), ("bible-import", None)]),
    ("revise", [("analysis-repetition", "analysis-repetition"),
                ("analysis-structure", "analysis-structure"),
                ("analysis-style", "analysis-style"), ("rhyme", "rhyme"),
                ("thesaurus", "thesaurus"), ("grammar", "grammar"), ("spelling", None),
                ("read-aloud", "read-aloud")]),
    ("environment", [("distraction-free", "distraction-free"),
                     ("ambient-sounds", "ambient-sounds"), ("focus", None),
                     ("themes", "themes")]),
    ("safety", [("snapshots", "snapshots"), ("backups", "backups"), ("sync", "sync"),
                ("moving", None)]),
    ("finish", [("compile", "compile")]),
    ("languages", [("spanish", "spanish")]),
    ("extras", [("assistant", None), ("mcp", None)]),
]

STRINGS = {
    "en": {
        "lang": "en",
        "dir_prefix": "",
        "other": ("es/", "Español"),
        "title": "Corylus: a writing app for novels, kept in plain files on your disk",
        "description": (
            "A free writing app for novels and other long work, for Mac and Windows. Every "
            "chapter is a plain Markdown file in a folder of your own. Binder, corkboard, "
            "outliner, Story Bible, checks for repeated words and monotonous sentences, "
            "distraction-free mode, snapshots, and export to Word, PDF and EPUB. No account."
        ),
        "skip": "Skip to content",
        "nav": [("#why", "Why"), ("#tour", "Features"), ("#private", "Privacy"), ("#get", "Download")],
        "hero_h": "Corylus is the writing app I always wanted to make.",
        "hero_p": (
            "It keeps every chapter as a plain text file in a folder of your own, and it helps "
            "you revise what you write. It points out repeated words, runs of sentences with "
            "the same length or the same opening, and paragraphs that turn monotonous."
        ),
        "hero_p2": (
            "It has a distraction-free mode with background video and ambient sounds, so it's "
            "just you and the text. It works offline, and if you want, you can sync your "
            "projects with Dropbox, pCloud or Google Drive. It's in English and Spanish, for "
            "Mac and Windows. And it's free!"
        ),
        "hero_note": "No account and no subscription. The Mac version needs Apple silicon (M1 or later).",
        "hero_alt": (
            "Corylus with a novel open: the Binder of chapters on the left, a chapter in the "
            "middle, and the Inspector with its synopsis, label and status on the right."
        ),
        "dl_mac": "Download for Mac",
        "dl_win": "Download for Windows",
        "dl_ver": "version",
        "dl_mobile": (
            "iPhone, iPad and Android versions exist and run on real devices, but they are "
            "not in any app store yet. They are coming."
        ),
        "dl_gatekeeper": (
            "Corylus is not notarized by Apple yet, so the first time you open it macOS says "
            "the developer cannot be verified. Right-click Corylus.app, choose Open, then "
            "Open again. On macOS 15 or later, go to System Settings, then Privacy & Security, "
            "and click Open Anyway. You only do this once per download."
        ),
        "why_h": "Every chapter is a file on your disk",
        "why_p1": (
            "Most writing software for long work keeps your manuscript in a database, a "
            "bundle or a cloud account, and only that one application can open it. That works "
            "until the application stops being maintained, changes its price, or will not run "
            "on your next computer."
        ),
        "why_p2": (
            "Corylus keeps each document as a plain Markdown file in an ordinary folder. That "
            "is the format it works in every day, so there is nothing to export. Open the "
            "folder while Corylus is running and your chapters are there, readable in any text "
            "editor. Corylus also keeps a search index, and rebuilds it from those files "
            "whenever it needs to."
        ),
        "why_pull": (
            "If Corylus vanished tomorrow, your work would still be plain Markdown files in an "
            "ordinary folder, and any text editor opens them."
        ),
        "tree_cap": "A Corylus project, as your file manager sees it.",
        "shot_files_cap": "The same chapter in Corylus, and as the file on your disk.",
        "tour_h": "Everything Corylus does",
        "tour_p": (
            "A tour of the whole app. All of it is in the free download. A few parts, such as "
            "grammar and the natural voices, are extra downloads you choose from inside Corylus."
        ),
        "groups": {
            "writing": ("Writing a book in pieces",
                        "In Corylus a novel is a tree of folders, chapters and scenes in the Binder, on the left. Every piece is a file of its own."),
            "structure": ("Seeing the shape of the book",
                          "The Corkboard and the Outliner show the same chapters from further away, in the Binder's order."),
            "bible": ("The Story Bible",
                      "Characters, places, objects, organisations, plots, scenes, themes, timeline events, lore and research. Each kind of entry has fields of its own, and every entry is a Markdown file in the project's StoryBible folder."),
            "revise": ("Help with revising",
                       "These checks mark the text and explain each mark when you hover over it. Every check has its own switch, so you turn on only the ones you want. They work in English and Spanish and run on your computer. Most need language data that downloads once, and Corylus offers it when you switch the check on."),
            "environment": ("Just you and the text",
                            "Corylus can hide everything but the page, set a video behind it and play the rain while you write."),
            "safety": ("Your files, and copies of them",
                       "Your project is a folder you chose. Corylus adds copies of its own, in ordinary formats you can open without it."),
            "finish": ("When the book is done", ""),
            "languages": ("In English and Spanish", ""),
            "extras": ("Optional extras that use AI",
                       "Two parts of Corylus use AI. Both stay off until you install them, and everything above works without them."),
        },
        "feats": {
            "binder": ("Binder, tabs and split panes",
                       "Drag chapters and scenes to put them in order. Open several at once in tabs, split the window to keep your notes beside a chapter, or pull a tab out into a window of its own."),
            "continuous": ("Continuous text",
                           "Select a folder, or a handful of chapters, and read them as one long page. You can edit there as well, and each chapter is still saved to its own file.",
                           "Several chapters shown one after another on a single scrolling page, each under a divider with its title."),
            "inspector": ("Synopsis, label and status",
                          "Each chapter carries a synopsis, notes, a label and a status, edited in the Inspector on the right. They are stored at the top of the chapter's own file, where any text editor can read them."),
            "comments": ("Comments",
                         "Select a passage and leave a note on it. Reply to it, resolve it or delete it. The comment follows its passage as you edit. Its text is kept in a separate file, so the chapter holds only an invisible marker where the comment sits.",
                         "A passage highlighted in a chapter, with its comment shown in the comments panel beside it."),
            "find": ("Find and search",
                     "Find and replace inside a chapter, matching case or whole words if you want. Search the whole project for a phrase, with or without accents, and narrow the results by label, status or folder."),
            "typing": ("Dashes and quotes as you type",
                       "Two hyphens become a dash and three dots an ellipsis. Straight quotes curl as you type, and in a Spanish document they become « ». One undo gives you back exactly what you typed."),
            "statistics": ("Word counts and targets",
                           "Give a chapter or the whole book a word target and watch the progress as you write, along with the words you have added this session. Project Statistics counts words, sentences and paragraphs, estimates pages and reading time, and lists the words you use most.",
                           "The Project Statistics window, with word, sentence and paragraph counts, page and reading-time estimates, and a list of the most frequent words."),
            "corkboard": ("Corkboard",
                          "A folder's chapters as index cards in a grid, each with its title and synopsis, or its opening lines if it has no synopsis yet.",
                          "The Corkboard: a folder's chapters as index cards, each with a title and a short synopsis."),
            "outliner": ("Outliner",
                         "The same chapters as a table with their title, synopsis, label, status and word count. Change any of them right there in the table.",
                         "The Outliner: one row per chapter, with columns for title, synopsis, label, status and word count."),
            "methodology": ("Methodology wizard",
                            "Pick a story structure, such as three acts, Save the Cat or the hero's journey, and Corylus sets it up in the Story Bible as a folder with one entry per beat. Mark each beat done and link the scenes that carry it. There are methods for characters, scenes, themes and worldbuilding as well.",
                            "The methodology wizard, with a list of story structures and a preview of the one selected."),
            "story-bible-entry": ("Entries with portraits",
                                  "Give a character a portrait and fill in what matters: what they want and what they need, the wound, the lie they believe, the arc. Type [[ to link to any other entry by name. Links survive renames, and every entry lists the places that mention it.",
                                  "A character entry in the Story Bible, with a portrait on the left and fields such as Want vs. Need beside it."),
            "relationship-map": ("Relationships with both names",
                                 "A relationship is written once and appears on both entries, and each end can have its own name: “creator of” from Victor, “created by” from the Creature. On a relationship map the lines are drawn from the entries themselves, so the map and the entries always agree. There are scene corkboards and mood boards for images too.",
                                 "A relationship map: character cards with portraits, joined by lines labelled with the relationship, such as “creator of”."),
            "bible-import": ("Notes you already have",
                             "Drop a Word, OpenDocument, RTF, HTML, Markdown or plain text file on the Story Bible and it becomes an entry, formatting and images included. Tag entries, nest tags such as faction/rebels, and filter the tree by them."),
            "analysis-repetition": ("Repeated words",
                                    "Corylus marks a word that comes back too soon, and counts the forms of a word together: “forest” and “forests”, “walk” and “walked”. You decide how near is too near and which words never count.",
                                    "A paragraph with several repeated words underlined."),
            "analysis-structure": ("Monotonous sentences",
                                   "Corylus can highlight three or more sentences in a row that open the same way or share the same build, stretches of sentences of nearly equal length, and paragraphs heavy with nouns. It also looks for stacked prepositions and filter words such as “she saw” and “he felt”, and in English for piles of “-ing” openers and of “as” and “but”.",
                                   "A passage with a run of sentences highlighted as monotonous."),
            "analysis-style": ("Adverbs, adjectives and gerunds",
                               "Highlight the adverbs, the adjectives or the gerunds to see where the prose leans on them. Project Statistics gives their density across the whole book.",
                               "A paragraph with its adverbs, adjectives and gerunds highlighted."),
            "rhyme": ("Accidental rhymes",
                      "Corylus underlines words close together that rhyme, the kind of echo you only notice when the text is read aloud. In Spanish it tells full rhyme from assonance, and you choose which to look for.",
                      "A paragraph with pairs of rhyming words underlined."),
            "thesaurus": ("Synonyms on right-click",
                          "Right-click a word to see its synonyms and antonyms, and click one to put it in. A dictionary card lists them by meaning, with definitions. The thesaurus is built from Wiktionary, in English and Spanish.",
                          "The right-click menu on a word, listing synonyms to replace it with."),
            "grammar": ("Grammar",
                        "Grammar and style checking by LanguageTool, in English and Spanish. It downloads once, then runs on your computer without a connection. It needs Java, and Corylus fetches a small Java runtime if your computer has none.",
                        "A sentence with a grammar mark and LanguageTool's suggested correction."),
            "spelling": ("Spelling",
                         "Spell-checking with Hunspell, plus a dictionary in each project for your characters' names and the words you invent."),
            "read-aloud": ("Read aloud",
                           "Corylus reads your text sentence by sentence, from the cursor or from a selection, and highlights the sentence it is on. Use your system's voices, or download natural voices for English and Spanish that run on your computer. You can also save the reading as a WAV file.",
                           "The read-aloud player, with the sentence being read highlighted in the chapter."),
            "distraction-free": ("Distraction-free mode",
                                 "One shortcut hides the Binder, the toolbar and the panels and takes the window full screen. Put a looping video or a picture of your own behind a translucent page and choose how much of it shows through. There is a gallery of backgrounds to download. Esc brings everything back.",
                                 "Distraction-free mode: a chapter on a translucent page over a background video, with the floating control bar."),
            "ambient-sounds": ("Ambient sounds",
                               "A mixer of background sounds: rain, waves, café chatter and many more, each at its own volume. Save the mixes you like, and play or stop them from the toolbar, in distraction-free mode too. The sounds are a single download.",
                               "The Ambient Sounds mixer, with sounds grouped by category and a volume slider for each."),
            "focus": ("Focus and typewriter scrolling",
                      "Focus mode dims everything except the sentence or the paragraph you are in. Typewriter scrolling keeps the line you are typing in the middle of the screen."),
            "themes": ("Themes and typography",
                       "Pick a colour theme for the window, among them Nord, Solarized, Dracula and two high-contrast ones, and a separate page colour: white, sepia, parchment or night. Typography presets set the font, spacing and indents, from modern block paragraphs to a double-spaced manuscript for submissions, and you can make your own. None of this changes your files.",
                       "A chapter shown in a different colour theme."),
            "snapshots": ("Snapshots",
                          "While you work on a chapter, Corylus keeps a copy of it every ten minutes, and you can take one yourself at any moment and give it a name. Compare any two to see what changed, or go back to one. Each snapshot is a plain text file inside the project.",
                          "The Snapshots panel: a list of saved versions of a chapter, and two of them compared with the changes marked."),
            "backups": ("Backups",
                        "Corylus backs the whole project up as a ZIP file on a schedule you set and keeps the most recent ones. Settings lists them, and Restore puts the one you pick in a new folder, never over the files you have. A copy of each backup can go to your cloud account as well.",
                        "Settings, Snapshots & Backups: a list of backup files with their dates, and a Restore button."),
            "sync": ("Sync with your own cloud",
                     "If you write on more than one computer, connect your own pCloud, Google Drive, Dropbox, OneDrive, Box or Amazon S3 account and Corylus keeps the project in step on each. When two computers change the same chapter, neither version is lost. Your files go straight to your account, with no Corylus server in between.",
                     "Settings, Cloud sync: the providers you can connect, among them pCloud, Google Drive and Dropbox."),
            "moving": ("Moving in and moving around",
                       "Import a manuscript from Scrivener, Word, EPUB or HTML into a new project. Save a whole project as a single .cory file to take it to another computer, where a double-click opens it."),
            "compile": ("Compile to Word, PDF or EPUB",
                        "Compile puts the chapters together in Binder order. Tick the parts that go in, leave out chapters by status, choose a format and export a Word document, a PDF or an EPUB. Chapter titles, scene separators, headers, footers and page numbers are set in the same dialog. Corylus needs no other program to do it.",
                        "The Compile dialog, with the parts of the book to include, the format, and the choice of Word, PDF or EPUB."),
            "spanish": ("Spanish as a first language",
                        "The interface, spell-check, grammar, thesaurus, repetition and rhyme checks and the read-aloud voices all work in both languages. Each document has its own language, so a Spanish novel gets Spanish quotes, Spanish hyphenation and Spanish checks while the menus stay in English, or the other way round.",
                        "Corylus with its interface in Spanish and a chapter in Spanish open."),
            "assistant": ("A local assistant",
                          "An assistant panel that answers questions about your own book, using a Qwen3 model that runs on your computer through Ollama. It is a large download, about 4 to 8 GB, and it cannot change your text."),
            "mcp": ("AI apps, through MCP",
                    "If you use an AI app that supports MCP, such as Claude Desktop or Claude Code, you can let it read your project and, if you allow it, edit it. You choose per project: nothing, read only, ask before each change, or change freely. Corylus takes a snapshot before every change and keeps a log where you can undo any of them. What the app reads goes to that app's own service, under its terms."),
        },
        "private_h": "What stays on your computer",
        "private": [
            ("No account", "There is nothing to sign up for. Corylus has no server of its own, so there is nowhere for an account to live."),
            ("The AI runs on your computer", "Grammar, the natural voices and the assistant are optional downloads. Once installed they run on your computer, and the text they check, read or answer about stays there."),
            ("What does go online", "Sync, if you turn it on, sends the project to the cloud account you chose. Some system voices are online ones, and the voice list marks them “(online)”. Corylus checks for a new version at start-up, which you can switch off in Settings. Optional downloads come from their publishers' servers. If you connect an AI app such as Claude Desktop, it reads what you allow, project by project."),
            ("Open format", "Markdown, with a short YAML header at the top of each file. Any text editor opens it."),
        ],
        "support_h": "Support Corylus",
        "support_p": (
            "Corylus is free, and every feature is in the free app. One person builds it. "
            "Support on Ko-fi pays for the certificates that let it install without warnings "
            "and for the store accounts the phone versions need. After that, it pays for time."
        ),
        "support_cta": "Support Corylus on Ko-fi",
        "support_soon": "The Ko-fi page opens soon. Until then, the best help is telling another writer about Corylus.",
        "support_costs_h": "What support pays for",
        "support_costs": [
            ("€99 a year", "The Apple Developer Program. It removes the “developer cannot be verified” warning on the Mac, and it is what puts the iPhone and iPad versions in the App Store."),
            ("About €253 a year", "A Windows code-signing certificate, VAT included. Windows warns about any installer from an unknown publisher; a signed one builds trust with every download until the warning stops."),
            ("About €22 once", "The $25 Google Play developer account, which the Android version needs to reach the store."),
            ("Then: time", "Corylus is built in the hours left over from a day job."),
        ],
        "get_h": "Download Corylus",
        "foot_rel": "All releases",
        "foot_priv": "Privacy",
        "foot_note": "Corylus is the botanical name of the hazel, the old European tree of writing and wisdom.",
        "maker_h": "Who makes it",
        "maker_p": (
            "I'm Ludo Bermejo, and I make Corylus on my own, with a lot of help from AI coding "
            "tools. I lead software teams for a living and write fiction. My science-fiction "
            "story “Azul” won the 2023 Premio Domingo Santos, awarded by the Asociación Pórtico "
            "and announced at HispaCon. Corylus is the app I built to write my own novels in."
        ),
    },
    "es": {
        "lang": "es",
        "dir_prefix": "../",
        "other": ("../", "English"),
        "title": "Corylus: un programa para escribir novelas en archivos que son tuyos",
        "description": (
            "Un programa gratuito para escribir novelas y otras obras largas, para Mac y "
            "Windows. Cada capítulo es un archivo Markdown normal en una carpeta tuya. Carpeta, "
            "tablero, esquema, Biblia de la historia, avisos de palabras repetidas y frases "
            "monótonas, modo sin distracciones, instantáneas y exportación a Word, PDF y EPUB. "
            "Sin cuenta."
        ),
        "skip": "Ir al contenido",
        "nav": [("#why", "Por qué"), ("#tour", "Qué hace"), ("#private", "Privacidad"), ("#get", "Descargar")],
        "hero_h": "Corylus es el editor que siempre quise crear.",
        "hero_p": (
            "Guarda cada capítulo como un archivo de texto normal, en una carpeta tuya, y además "
            "te ayuda a revisar lo que escribes: te señala las palabras repetidas, las rachas de "
            "frases con la misma longitud o el mismo arranque y los párrafos que se vuelven "
            "monótonos."
        ),
        "hero_p2": (
            "Tiene un modo sin distracciones con vídeo y sonidos de fondo, para que solo quedéis "
            "tú y el texto. Funciona sin conexión, y si quieres puedes sincronizar tus proyectos "
            "con Dropbox, pCloud o Google Drive. Está en español e inglés, para Mac y Windows. "
            "¡Y es gratis!"
        ),
        "hero_note": "Sin cuenta y sin suscripción. La versión de Mac necesita un chip de Apple (M1 o posterior).",
        "hero_alt": (
            "Corylus con una novela abierta: la Carpeta con los capítulos a la izquierda, un "
            "capítulo en el centro y, a la derecha, el Inspector con la sinopsis, la etiqueta y "
            "el estado."
        ),
        "dl_mac": "Descargar para Mac",
        "dl_win": "Descargar para Windows",
        "dl_ver": "versión",
        "dl_mobile": (
            "Las versiones de iPhone, iPad y Android ya existen y funcionan en dispositivos "
            "reales, pero todavía no están en ninguna tienda de aplicaciones. Están en camino."
        ),
        "dl_gatekeeper": (
            "Corylus todavía no está notarizado por Apple, así que la primera vez que lo abras "
            "macOS te dirá que no puede verificar al desarrollador. Haz clic derecho en "
            "Corylus.app, elige Abrir y después Abrir otra vez. En macOS 15 o posterior, ve a "
            "Ajustes del Sistema, entra en Privacidad y seguridad y pulsa Abrir igualmente. "
            "Solo hace falta una vez por descarga."
        ),
        "why_h": "Cada capítulo es un archivo de tu disco",
        "why_p1": (
            "Casi todos los programas para obra larga guardan tu manuscrito en una base de "
            "datos, en un paquete o en una cuenta en la nube, y solo esa aplicación sabe "
            "abrirlo. Eso funciona hasta que la aplicación deja de mantenerse, cambia de "
            "precio o no arranca en tu próximo ordenador."
        ),
        "why_p2": (
            "Corylus guarda cada documento como un archivo Markdown normal, en una carpeta "
            "normal. Es el formato con el que trabaja a diario, así que no hay nada que "
            "exportar. Abre la carpeta con Corylus en marcha y ahí están tus capítulos, "
            "legibles con cualquier editor de texto. Corylus también mantiene un índice de "
            "búsqueda, y lo reconstruye a partir de esos archivos cuando hace falta."
        ),
        "why_pull": (
            "Si Corylus desapareciera mañana, tu obra seguiría siendo archivos Markdown en "
            "una carpeta normal, y cualquier editor de texto los abre."
        ),
        "tree_cap": "Un proyecto de Corylus, tal y como lo ve tu gestor de archivos.",
        "shot_files_cap": "El mismo capítulo en Corylus, y como archivo en tu disco.",
        "tour_h": "Todo lo que hace Corylus",
        "tour_p": (
            "Un recorrido por todo el programa. Todo viene en la descarga gratuita. Algunas "
            "partes, como la gramática o las voces naturales, son descargas adicionales que "
            "eliges desde dentro de Corylus."
        ),
        "groups": {
            "writing": ("Escribir un libro por piezas",
                        "En Corylus una novela es un árbol de carpetas, capítulos y escenas que ves en la Carpeta, a la izquierda. Cada pieza es un archivo propio."),
            "structure": ("Ver la forma del libro",
                          "El Tablero y el Esquema muestran los mismos capítulos desde más lejos, en el orden de la Carpeta."),
            "bible": ("La Biblia de la historia",
                      "Personajes, lugares, objetos, organizaciones, tramas, escenas, temas, cronologías, lore e investigación. Cada tipo de entrada tiene sus propios campos, y cada entrada es un archivo Markdown en la carpeta StoryBible del proyecto."),
            "revise": ("Ayuda para revisar",
                       "Estas comprobaciones marcan el texto y explican cada marca cuando pasas el ratón por encima. Cada una tiene su propio interruptor, así que activas solo las que quieras. Funcionan en español y en inglés, y en tu ordenador. Casi todas necesitan unos datos de idioma que se descargan una vez, y Corylus te los ofrece al activarlas."),
            "environment": ("Solo tú y el texto",
                            "Corylus puede esconderlo todo menos la página, ponerle un vídeo detrás y hacer que llueva mientras escribes."),
            "safety": ("Tus archivos, y copias de ellos",
                       "Tu proyecto es una carpeta que tú eliges. Corylus añade sus propias copias, en formatos normales que se abren sin él."),
            "finish": ("Cuando el libro está terminado", ""),
            "languages": ("En español e inglés", ""),
            "extras": ("Extras opcionales con IA",
                       "Dos partes de Corylus usan IA. Las dos están apagadas hasta que las instalas, y todo lo anterior funciona sin ellas."),
        },
        "feats": {
            "binder": ("Carpeta, pestañas y paneles",
                       "Arrastra capítulos y escenas para ordenarlos. Abre varios a la vez en pestañas, divide la ventana para tener tus notas junto al capítulo o saca una pestaña a su propia ventana."),
            "continuous": ("Texto continuo",
                           "Elige una carpeta, o unos cuantos capítulos, y léelos seguidos como una sola página larga. También puedes editar ahí, y cada capítulo se sigue guardando en su propio archivo.",
                           "Varios capítulos seguidos en una sola página con desplazamiento, cada uno bajo un separador con su título."),
            "inspector": ("Sinopsis, etiqueta y estado",
                          "Cada capítulo lleva una sinopsis, notas, una etiqueta y un estado, que editas en el Inspector, a la derecha. Se guardan al principio del propio archivo del capítulo, donde cualquier editor de texto puede leerlos."),
            "comments": ("Comentarios",
                         "Selecciona un pasaje y déjale una nota. Respóndela, dala por resuelta o bórrala. El comentario sigue a su pasaje mientras editas. Su texto se guarda en un archivo aparte, y en el capítulo solo queda una marca invisible donde está el comentario.",
                         "Un pasaje resaltado en un capítulo, con su comentario al lado, en el panel de comentarios."),
            "find": ("Buscar y reemplazar",
                     "Busca y reemplaza dentro de un capítulo, distinguiendo mayúsculas o palabras completas si quieres. Busca una frase en todo el proyecto, con tildes o sin ellas, y filtra los resultados por etiqueta, estado o carpeta."),
            "typing": ("Rayas y comillas al escribir",
                       "Dos guiones se convierten en raya y tres puntos en puntos suspensivos. Las comillas rectas se cambian solas, y en un documento en español pasan a ser « ». Un solo deshacer te devuelve exactamente lo que tecleaste."),
            "statistics": ("Recuentos y objetivos",
                           "Ponle a un capítulo o al libro entero un objetivo de palabras y mira el progreso mientras escribes, junto con las palabras que llevas en esta sesión. Estadísticas del proyecto cuenta palabras, frases y párrafos, calcula páginas y tiempo de lectura y te enseña las palabras que más usas.",
                           "La ventana Estadísticas del proyecto, con el recuento de palabras, frases y párrafos, la estimación de páginas y de tiempo de lectura y la lista de las palabras más frecuentes."),
            "corkboard": ("Tablero",
                          "Los capítulos de una carpeta como fichas en una cuadrícula, cada una con su título y su sinopsis, o con sus primeras líneas si todavía no tiene sinopsis.",
                          "El Tablero: los capítulos de una carpeta como fichas, cada una con un título y una sinopsis breve."),
            "outliner": ("Esquema",
                         "Los mismos capítulos en una tabla, con su título, sinopsis, etiqueta, estado y número de palabras. Cualquiera de ellos se cambia ahí mismo, en la tabla.",
                         "El Esquema: una fila por capítulo, con columnas de título, sinopsis, etiqueta, estado y número de palabras."),
            "methodology": ("Asistente de metodología",
                            "Elige una estructura, como los tres actos, Save the Cat o el viaje del héroe, y Corylus la monta en la Biblia de la historia: una carpeta con una entrada por cada punto de la estructura. Marca los puntos que ya están escritos y enlaza las escenas que los cumplen. También hay métodos para personajes, escenas, temas y construcción de mundos.",
                            "El asistente de metodología, con una lista de estructuras narrativas y la vista previa de la elegida."),
            "story-bible-entry": ("Entradas con retrato",
                                  "Ponle retrato a un personaje y rellena lo que importa: lo que quiere y lo que necesita, su herida, la mentira que se cree, su arco. Escribe [[ para enlazar cualquier otra entrada por su nombre. Los enlaces sobreviven a los cambios de nombre, y cada entrada muestra dónde se la menciona.",
                                  "Una entrada de personaje en la Biblia de la historia, con el retrato a la izquierda y, al lado, campos como Deseo vs. Necesidad."),
            "relationship-map": ("Relaciones con sus dos nombres",
                                 "Una relación se escribe una vez y aparece en las dos entradas, y cada extremo puede tener su propio nombre: «creador de» desde Victor, «creado por» desde la Criatura. En un mapa de relaciones las líneas salen de las propias entradas, así que el mapa y las entradas siempre dicen lo mismo. También hay tableros de escenas y paneles de inspiración con imágenes.",
                                 "Un mapa de relaciones: tarjetas de personajes con retrato, unidas por líneas con el nombre de la relación, como «creador de»."),
            "bible-import": ("Las notas que ya tienes",
                             "Arrastra a la Biblia de la historia un archivo de Word, OpenDocument, RTF, HTML, Markdown o texto y se convierte en una entrada, con su formato y sus imágenes. Pon etiquetas a las entradas, anídalas como en faccion/rebeldes y filtra el árbol por ellas."),
            "analysis-repetition": ("Palabras repetidas",
                                    "Corylus marca la palabra que vuelve demasiado pronto, y cuenta juntas las formas de una misma palabra: «bosque» y «bosques», «corrió» y «corría». Tú decides a qué distancia es demasiado pronto y qué palabras no cuentan nunca.",
                                    "Un párrafo con varias palabras repetidas subrayadas."),
            "analysis-structure": ("Frases monótonas",
                                   "Corylus puede resaltar tres o más frases seguidas que empiezan igual o están construidas igual, tramos de frases casi de la misma longitud y párrafos cargados de sustantivos. También busca preposiciones encadenadas y verbos de percepción que filtran la escena, como «vio» o «sintió», y en español el exceso de gerundios y de pronombres sujeto que sobran.",
                                   "Un pasaje con una racha de frases resaltada por monótona."),
            "analysis-style": ("Adverbios, adjetivos y gerundios",
                               "Resalta los adverbios, los adjetivos o los gerundios para ver dónde se apoya demasiado la prosa. Estadísticas del proyecto te da su densidad en todo el libro.",
                               "Un párrafo con sus adverbios, adjetivos y gerundios resaltados."),
            "rhyme": ("Rimas sin querer",
                      "Corylus subraya las palabras cercanas que riman, ese eco que solo se nota al leer en voz alta. En español distingue la rima consonante de la asonante, y tú eliges cuál buscar o si buscar las dos.",
                      "Un párrafo con parejas de palabras que riman subrayadas."),
            "thesaurus": ("Sinónimos con el botón derecho",
                          "Haz clic derecho en una palabra para ver sus sinónimos y antónimos, y pulsa uno para ponerlo en su lugar. Una ficha de diccionario los ordena por significado, con sus definiciones. El diccionario de sinónimos sale de Wiktionary, en español y en inglés.",
                          "El menú del botón derecho sobre una palabra, con sinónimos para sustituirla."),
            "grammar": ("Gramática",
                        "Revisión de gramática y estilo con LanguageTool, en español y en inglés. Se descarga una vez y después funciona en tu ordenador, sin conexión. Necesita Java, y si tu ordenador no lo tiene, Corylus descarga un Java mínimo.",
                        "Una frase con una marca gramatical y la corrección que propone LanguageTool."),
            "spelling": ("Ortografía",
                         "Corrector ortográfico Hunspell, con un diccionario propio en cada proyecto para los nombres de tus personajes y las palabras que inventas."),
            "read-aloud": ("Lectura en voz alta",
                           "Corylus lee tu texto frase a frase, desde el cursor o desde lo que hayas seleccionado, y resalta la frase por la que va. Usa las voces de tu sistema o descarga voces naturales en español y en inglés que funcionan en tu ordenador. También puedes guardar la lectura como archivo WAV.",
                           "El reproductor de lectura en voz alta, con la frase que se está leyendo resaltada en el capítulo."),
            "distraction-free": ("Modo sin distracciones",
                                 "Con un atajo desaparecen la Carpeta, la barra de herramientas y los paneles, y la ventana pasa a pantalla completa. Pon detrás de una página translúcida un vídeo en bucle o una imagen tuya, y elige cuánto se transparenta. Hay una galería de fondos para descargar. Esc lo devuelve todo a su sitio.",
                                 "El modo sin distracciones: un capítulo sobre una página translúcida delante de un vídeo de fondo, con la barra de controles flotante."),
            "ambient-sounds": ("Sonidos ambientales",
                               "Un mezclador de sonidos de fondo: lluvia, olas, murmullo de cafetería y muchos más, cada uno con su volumen. Guarda las mezclas que te gusten y ponlas o páralas desde la barra de herramientas, también en el modo sin distracciones. Los sonidos son una sola descarga.",
                               "El mezclador de Sonidos Ambientales, con los sonidos agrupados por categoría y un control de volumen para cada uno."),
            "focus": ("Enfoque y máquina de escribir",
                      "El modo enfoque atenúa todo menos la frase o el párrafo en el que estás. El desplazamiento máquina de escribir mantiene la línea que escribes en el centro de la pantalla."),
            "themes": ("Temas y tipografía",
                       "Elige un tema de color para la ventana, entre ellos Nord, Solarized, Dracula y dos de alto contraste, y aparte un color de página: blanco, sepia, pergamino o noche. Los estilos de tipografía fijan la letra, el interlineado y las sangrías, desde párrafos modernos en bloque hasta un manuscrito a doble espacio para enviar a editoriales, y puedes crear los tuyos. Nada de esto cambia tus archivos.",
                       "Un capítulo con otro tema de color."),
            "snapshots": ("Instantáneas",
                          "Mientras trabajas en un capítulo, Corylus guarda una copia cada diez minutos, y tú puedes sacar una cuando quieras y ponerle nombre. Compara dos cualesquiera para ver qué cambió, o vuelve a una. Cada instantánea es un archivo de texto normal dentro del proyecto.",
                          "El panel Instantáneas: una lista de versiones guardadas de un capítulo y dos de ellas comparadas, con los cambios marcados."),
            "backups": ("Copias de seguridad",
                        "Corylus guarda una copia del proyecto entero en un archivo ZIP con la frecuencia que elijas, y conserva las más recientes. Los Ajustes te las enseñan, y Restaurar pone la que elijas en una carpeta nueva, nunca encima de los archivos que ya tienes. Cada copia puede ir también a tu cuenta en la nube.",
                        "Ajustes, Instantáneas y copias: una lista de copias de seguridad con su fecha y un botón Restaurar."),
            "sync": ("Sincronización con tu propia nube",
                     "Si escribes en más de un ordenador, conecta tu cuenta de pCloud, Google Drive, Dropbox, OneDrive, Box o Amazon S3 y Corylus mantiene el proyecto al día en todos. Si dos ordenadores cambian el mismo capítulo, no se pierde ninguna de las dos versiones. Tus archivos van directos a tu cuenta, sin ningún servidor de Corylus por medio.",
                     "Ajustes, Sincronización en la nube: los servicios que puedes conectar, entre ellos pCloud, Google Drive y Dropbox."),
            "moving": ("Traer tu libro y llevártelo",
                       "Importa un manuscrito de Scrivener, Word, EPUB o HTML a un proyecto nuevo. Guarda el proyecto entero en un solo archivo .cory para llevarlo a otro ordenador, donde se abre con doble clic."),
            "compile": ("Compilar a Word, PDF o EPUB",
                        "Compilar junta los capítulos en el orden de la Carpeta. Marca las partes que entran, deja fuera capítulos según su estado, elige un formato y exporta un documento de Word, un PDF o un EPUB. Los títulos de capítulo, los separadores de escena, los encabezados, los pies y los números de página se ajustan en el mismo cuadro. Corylus no necesita ningún otro programa para hacerlo.",
                        "El cuadro Compilar manuscrito, con las partes del libro que se incluyen, el formato y la elección entre Word, PDF y EPUB."),
            "spanish": ("El español como primera lengua",
                        "La interfaz, el corrector, la gramática, los sinónimos, las comprobaciones de repeticiones y de rimas y las voces de lectura funcionan en los dos idiomas. Cada documento tiene su propio idioma, así que una novela en español tiene comillas españolas, partición de palabras española y revisiones en español aunque tengas los menús en inglés, y al revés.",
                        "Corylus con la interfaz en español y un capítulo en español abierto."),
            "assistant": ("Un asistente local",
                          "Un panel que responde preguntas sobre tu propio libro con un modelo Qwen3 que funciona en tu ordenador a través de Ollama. Es una descarga grande, de 4 a 8 GB, y no puede cambiar tu texto."),
            "mcp": ("Aplicaciones de IA, por MCP",
                    "Si usas una aplicación de IA compatible con MCP, como Claude Desktop o Claude Code, puedes dejar que lea tu proyecto y, si se lo permites, que lo edite. Lo decides proyecto a proyecto: nada, solo lectura, preguntar antes de cada cambio o cambiar con libertad. Corylus saca una instantánea antes de cada cambio y lleva un registro desde el que puedes deshacer cualquiera. Lo que esa aplicación lee va a su propio servicio, con sus propias condiciones."),
        },
        "private_h": "Qué se queda en tu ordenador",
        "private": [
            ("Sin cuenta", "No hay nada en lo que registrarse. Corylus no tiene servidor propio, así que no hay dónde guardar una cuenta."),
            ("La IA funciona en tu ordenador", "La gramática, las voces naturales y el asistente son descargas opcionales. Una vez instalados funcionan en tu ordenador, y el texto que revisan, leen o consultan se queda ahí."),
            ("Lo que sí sale", "La sincronización, si la activas, envía el proyecto a la cuenta en la nube que elegiste. Algunas voces del sistema funcionan por internet, y la lista las marca como «(en línea)». Corylus comprueba si hay versión nueva al arrancar, y eso se desactiva en los Ajustes. Las descargas opcionales vienen de los servidores de quien las publica. Si conectas una aplicación de IA como Claude Desktop, lee lo que tú le permitas, proyecto a proyecto."),
            ("Formato abierto", "Markdown, con una cabecera YAML breve al principio de cada archivo. Cualquier editor de texto lo abre."),
        ],
        "support_h": "Apoya Corylus",
        "support_p": (
            "Corylus es gratis, y todas sus funciones están en la versión gratuita. Lo hace "
            "una sola persona. El apoyo en Ko-fi paga los certificados que permiten instalarlo "
            "sin avisos y las cuentas de tienda que necesitan las versiones para móvil. "
            "Después, paga tiempo."
        ),
        "support_cta": "Apoya Corylus en Ko-fi",
        "support_soon": "La página de Ko-fi abre pronto. Hasta entonces, la mejor ayuda es hablarle de Corylus a otra persona que escriba.",
        "support_costs_h": "Qué paga el apoyo",
        "support_costs": [
            ("99 € al año", "El programa de desarrolladores de Apple. Quita el aviso de «no se puede verificar al desarrollador» en el Mac, y es lo que lleva las versiones de iPhone y iPad a la App Store."),
            ("Unos 253 € al año", "Un certificado de firma para Windows, IVA incluido. Windows avisa de cualquier instalador de un editor desconocido; uno firmado gana confianza con cada descarga hasta que el aviso desaparece."),
            ("Unos 22 € una vez", "La cuenta de desarrollador de Google Play (25 $), que la versión de Android necesita para llegar a la tienda."),
            ("Y después: tiempo", "Corylus se hace en las horas que deja libres otro trabajo."),
        ],
        "get_h": "Descarga Corylus",
        "foot_rel": "Todas las versiones",
        "foot_priv": "Privacidad",
        "foot_note": "Corylus es el nombre botánico del avellano, el viejo árbol europeo de la escritura y la sabiduría.",
        "maker_h": "Quién lo hace",
        "maker_p": (
            "Soy Ludo Bermejo y hago Corylus yo solo, con mucha ayuda de herramientas de "
            "programación con IA. Dirijo equipos de software y escribo ficción. Mi relato de "
            "ciencia ficción «Azul» ganó el Premio Domingo Santos 2023, que concede la "
            "Asociación Pórtico; el fallo se anunció en la HispaCon. Corylus es el programa "
            "que me hice para escribir mis propias novelas."
        ),
    },
}

TREES = {
    "en": """My novel.corylus/
├── settings.json
├── Manuscript/
│   ├── Chapter I.md
│   ├── Chapter II.md
│   └── Chapter III.md
├── StoryBible/
│   ├── Characters/
│   └── Places/
└── .corylus/
    └── snapshots/
        └── 01JCB7R2M8X4QYV3T9K5N6PZ0A/
            └── 2026-11-02T09-14-22.md""",
    "es": """Mi novela.corylus/
├── settings.json
├── Manuscrito/
│   ├── Capitulo I.md
│   ├── Capitulo II.md
│   └── Capitulo III.md
├── StoryBible/
│   ├── Personajes/
│   └── Lugares/
└── .corylus/
    └── snapshots/
        └── 01JCB7R2M8X4QYV3T9K5N6PZ0A/
            └── 2026-11-02T09-14-22.md""",
}


def esc(s):
    return html.escape(s, quote=True)


def png_size(path):
    """(width, height) from a PNG's IHDR chunk, so every <img> carries its real size."""
    with open(path, "rb") as f:
        head = f.read(24)
    assert head[:8] == b"\x89PNG\r\n\x1a\n", f"{path} is not a PNG"
    return struct.unpack(">II", head[16:24])


def webp_size(path):
    """(width, height) of a WebP file, read from its header (VP8, VP8L or VP8X)."""
    with open(path, "rb") as f:
        head = f.read(30)
    assert head[:4] == b"RIFF" and head[8:12] == b"WEBP", f"{path} is not a WebP"
    kind = head[12:16]
    if kind == b"VP8 ":
        w, h = struct.unpack("<HH", head[26:30])
        return w & 0x3FFF, h & 0x3FFF
    if kind == b"VP8L":
        b = head[21:25]
        bits = b[0] | b[1] << 8 | b[2] << 16 | b[3] << 24
        return (bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1
    if kind == b"VP8X":
        return (int.from_bytes(head[24:27], "little") + 1,
                int.from_bytes(head[27:30], "little") + 1)
    raise ValueError(f"{path}: unknown WebP chunk {kind!r}")


def shot_img(p, sid, alt, lazy=True, lang="en"):
    """<img> for a screenshot: assets/shots/<lang>/<sid> first for Spanish (the app in
    Spanish), then the English one; WebP before PNG. "" while no capture has landed."""
    dirs = ([lang] if lang != "en" else []) + [""]
    for sub in dirs:
        for ext, size in (("webp", webp_size), ("png", png_size)):
            rel = "/".join(x for x in ("assets", "shots", sub, f"{sid}.{ext}") if x)
            path = os.path.join(HERE, *rel.split("/"))
            if os.path.exists(path):
                w, h = size(path)
                loading = ' loading="lazy"' if lazy else ""
                return f'<img src="{p}{rel}" alt="{esc(alt)}" width="{w}" height="{h}"{loading}>'
    return ""


def tour(t, p):
    out = []
    for i, (gid, items) in enumerate(TOUR):
        h, intro = t["groups"][gid]
        rows, rest = [], []
        for key, sid in items:
            title, body, *alt = t["feats"][key]
            img = shot_img(p, sid, alt[0], lang=t["lang"]) if sid else ""
            text = f"<h3>{esc(title)}</h3><p>{esc(body)}</p>"
            if img:
                rows.append(f'<div class="feature"><div>{text}</div><figure class="feature-shot">{img}</figure></div>')
            else:
                rest.append(f"<li>{text}</li>")
        lead = f'<p class="lead">{esc(intro)}</p>' if intro else ""
        features = "".join(rows)
        grid = '<ul class="grid two">' + "".join(rest) + "</ul>" if rest else ""
        band = " band" if i % 2 else ""
        out.append(f"""
  <section class="group{band}" id="{gid}">
    <div class="wrap">
      <h2>{esc(h)}</h2>
      {lead}
      {features}
      {grid}
    </div>
  </section>""")
    return "".join(out)


def page(t):
    p = t["dir_prefix"]
    other_href, other_label = t["other"]
    nav = "".join(f'<a href="{h}">{esc(l)}</a>' for h, l in t["nav"])
    private = "".join(
        f"<li><h3>{esc(h)}</h3><p>{esc(b)}</p></li>" for h, b in t["private"]
    )
    alt_en = SITE + "/"
    alt_es = SITE + "/es/"
    canonical = alt_es if t["lang"] == "es" else alt_en

    # The hero falls back to the older editor screenshot until the new capture lands.
    hero_img = shot_img(p, "editor", t["hero_alt"], lazy=False, lang=t["lang"]) or (
        f'<img src="{p}assets/editor.png" alt="{esc(t["hero_alt"])}" width="1500" height="900">'
    )

    # Always shown: the costs explain why support is asked for; only the button
    # waits for the Ko-fi address.
    costs = "".join(
        f"<li><h3>{esc(a)}</h3><p>{esc(b)}</p></li>" for a, b in t["support_costs"]
    )
    cta = (f'<a class="btn" href="{KOFI}" rel="noopener">{esc(t["support_cta"])}</a>'
           if KOFI else esc(t["support_soon"]))
    support = f"""
    <section class="band" id="support">
      <div class="wrap narrow">
        <h2>{esc(t['support_h'])}</h2>
        <p>{esc(t['support_p'])}</p>
        <h3 class="costs-h">{esc(t['support_costs_h'])}</h3>
        <ul class="grid two costs">{costs}</ul>
        <p class="cta">{cta}</p>
      </div>
    </section>"""

    return f"""<!doctype html>
<html lang="{t['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script src="{p}assets/lang.js"></script>
<title>{esc(t['title'])}</title>
<meta name="description" content="{esc(t['description'])}">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="en" href="{alt_en}">
<link rel="alternate" hreflang="es" href="{alt_es}">
<link rel="alternate" hreflang="x-default" href="{alt_en}">
<link rel="icon" href="{p}assets/favicon.svg" type="image/svg+xml">
<meta name="theme-color" content="#F7F3EA" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0E1713" media="(prefers-color-scheme: dark)">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(t['title'])}">
<meta property="og:description" content="{esc(t['description'])}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/assets/og.png">
<meta property="og:locale" content="{'es_ES' if t['lang'] == 'es' else 'en_GB'}">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Literata:wght@400;700&family=Source+Sans+3:wght@400;600&display=swap">
<link rel="stylesheet" href="{p}assets/style.css">
</head>
<body>
<a class="skip" href="#main">{esc(t['skip'])}</a>

<header class="site">
  <div class="wrap row">
    <a class="brand" href="{p if p else './'}" aria-label="Corylus">
      <img src="{p}assets/lockup.svg" alt="Corylus" width="232" height="64" class="only-light">
      <img src="{p}assets/lockup-dark.svg" alt="Corylus" width="232" height="64" class="only-dark">
    </a>
    <nav>{nav}<a class="lang" href="{other_href}" hreflang="{'en' if t['lang'] == 'es' else 'es'}">{esc(other_label)}</a></nav>
  </div>
</header>

<main id="main">

  <section class="hero">
    <div class="wrap narrow">
      <h1>{esc(t['hero_h'])}</h1>
      <p class="lead">{esc(t['hero_p'])}</p>
      <p>{esc(t['hero_p2'])}</p>
      <p class="downloads">
        <a class="btn" id="dl-mac" href="{RELEASES_RAW}/Corylus_{FALLBACK['mac']}_aarch64.dmg">
          {esc(t['dl_mac'])} <span class="ver" data-ver-label="{esc(t['dl_ver'])}">{esc(t['dl_ver'])} {FALLBACK['mac']}</span>
        </a>
        <a class="btn ghost" id="dl-win" href="{RELEASES_RAW}/Corylus_{FALLBACK['win']}_x64-setup.exe">
          {esc(t['dl_win'])} <span class="ver" data-ver-label="{esc(t['dl_ver'])}">{esc(t['dl_ver'])} {FALLBACK['win']}</span>
        </a>
      </p>
      <p class="note">{esc(t['hero_note'])}</p>
    </div>
    <div class="wrap">
      <figure class="media">{hero_img}</figure>
    </div>
  </section>

  <section class="band" id="why">
    <div class="wrap split">
      <div>
        <h2>{esc(t['why_h'])}</h2>
        <p>{esc(t['why_p1'])}</p>
        <p>{esc(t['why_p2'])}</p>
        <blockquote>{esc(t['why_pull'])}</blockquote>
      </div>
      <figure class="tree">
        <pre>{esc(TREES[t['lang']])}</pre>
        <figcaption>{esc(t['tree_cap'])}</figcaption>
      </figure>
    </div>
    <div class="wrap">
      <figure class="media wide">
        <img src="{p}assets/files-on-disk.png" alt="{esc(t['shot_files_cap'])}" width="1800" height="878" loading="lazy">
        <figcaption>{esc(t['shot_files_cap'])}</figcaption>
      </figure>
    </div>
  </section>

  <section class="tour-head" id="tour">
    <div class="wrap narrow">
      <h2>{esc(t['tour_h'])}</h2>
      <p>{esc(t['tour_p'])}</p>
    </div>
  </section>
{tour(t, p)}

  <section class="band" id="private">
    <div class="wrap">
      <h2>{esc(t['private_h'])}</h2>
      <ul class="grid two">{private}</ul>
    </div>
  </section>

  <section class="maker" id="maker">
    <div class="wrap narrow">
      <h2>{esc(t['maker_h'])}</h2>
      <p>{esc(t['maker_p'])}</p>
    </div>
  </section>
{support}
  <section class="band" id="get">
    <div class="wrap narrow">
      <h2>{esc(t['get_h'])}</h2>
      <p class="downloads">
        <a class="btn" href="{RELEASES_RAW}/Corylus_{FALLBACK['mac']}_aarch64.dmg">{esc(t['dl_mac'])}</a>
        <a class="btn ghost" href="{RELEASES_RAW}/Corylus_{FALLBACK['win']}_x64-setup.exe">{esc(t['dl_win'])}</a>
      </p>
      <p class="note">{esc(t['dl_mobile'])}</p>
      <p class="note">{esc(t['dl_gatekeeper'])}</p>
    </div>
  </section>

</main>

<footer class="site">
  <div class="wrap row">
    <p><img src="{p}assets/mark.svg" alt="" width="28" height="28" aria-hidden="true"> {esc(t['foot_note'])}</p>
    <nav>
      <a href="https://github.com/LudoBermejoES/corylus-releases" rel="noopener">{esc(t['foot_rel'])}</a>
      <a href="{p}{'es/privacy/' if t['lang'] == 'es' else 'privacy/'}">{esc(t['foot_priv'])}</a>
      <a class="lang" href="{other_href}">{esc(other_label)}</a>
    </nav>
  </div>
</footer>

<script src="{p}assets/site.js" defer></script>
</body>
</html>
"""


PRIVACY = {
    "en": {
        "lang": "en", "dir_prefix": "../", "other": ("../es/privacy/", "Español"),
        "title": "Privacy — Corylus",
        "description": "Corylus collects nothing. No account, no telemetry, no analytics, and no Corylus server.",
        "h": "Privacy", "updated": "Last updated 21 November 2026.",
        "lead": "Corylus collects no personal data. This page explains what that means in practice, and names every third party your computer talks to because of something Corylus does.",
        "sections": [
            ("What Corylus collects", [
                "Nothing.",
                "Corylus is a writing app for Mac and Windows. It has no user accounts, no telemetry, no analytics and no crash reporting, and there is no Corylus server for it to send anything to. Your documents are plain Markdown files in a folder you chose, on your own computer, and they stay there.",
            ]),
            ("What can leave your computer", [
                "Only what follows. Each item is something you turn on, or something you can turn off.",
                "Sync. If you connect a cloud account (pCloud, Google Drive, Dropbox, OneDrive, Box or Amazon S3), your project is copied to that account, and so are your backups if you choose. The files go from your computer to the provider you picked. Corylus is not a party to that transfer and keeps no copy. The connection details are stored on your computer.",
                "Online voices. Read aloud can use the voices your operating system provides. Some of them are online voices, marked “(online)” in the voice list, and when one of those reads, the text goes to the service behind it. The natural voices Corylus offers as a download run on your computer.",
                "The update check. At start-up Corylus fetches a small file from this website or from GitHub to see whether a newer version exists. The request carries no identifier, though the server sees your IP address as it would for any web request. You can switch the check off in Settings.",
                "AI apps you connect. If you install the MCP module and connect an AI app such as Claude Desktop or Claude Code, that app can read what you allow, project by project, and can edit only if you allow that too. What it reads goes to that app’s own service, under that service’s privacy policy. Corylus accepts these connections only from your own computer, and only while Corylus is open.",
                "A background from a web address. If you give distraction-free mode a background by its web address, Corylus downloads it from that address.",
            ]),
            ("Optional downloads", [
                "Some features are downloads you choose: dictionaries, the thesaurus, language data for the style checks, the grammar engine, the natural voices, the ambient sounds, the sync program and the assistant. Each comes from where its publisher hosts it: GitHub, Hugging Face, languagetool.org, rclone.org or ollama.com. Those servers see the request, as they would for any download. Corylus sends them nothing about you or your writing, and once installed these components run on your computer.",
            ]),
            ("This website", [
                "This site is hosted on GitHub Pages. It sets no cookies and runs no analytics. GitHub keeps server logs, including IP addresses, under its own privacy policy. The site loads its fonts from Google Fonts, so Google serves those files and sees the request. The download buttons ask GitHub for the current version number. If you pick a language with the site’s language link, your browser stores that choice on your device.",
            ]),
            ("Children", ["Corylus is not directed at children and collects no information from anyone, of any age."]),
            ("Changes", ["If this policy changes, the new version appears on this page with a new date. Since Corylus collects nothing, a change here would most likely mean a new optional component with its own download source."]),
        ],
        "back": "Back to Corylus",
    },
    "es": {
        "lang": "es", "dir_prefix": "../../", "other": ("../../privacy/", "English"),
        "title": "Privacidad — Corylus",
        "description": "Corylus no recoge nada. Sin cuenta, sin telemetría, sin analítica y sin servidor de Corylus.",
        "h": "Privacidad", "updated": "Última actualización: 21 de noviembre de 2026.",
        "lead": "Corylus no recoge datos personales. Esta página explica qué significa eso en la práctica y nombra a cada tercero con el que tu ordenador habla por algo que haga Corylus.",
        "sections": [
            ("Qué recoge Corylus", [
                "Nada.",
                "Corylus es un programa de escritura para Mac y Windows. No tiene cuentas de usuario, ni telemetría, ni analítica, ni informes de fallos, y no hay ningún servidor de Corylus al que enviar nada. Tus documentos son archivos Markdown normales en una carpeta que tú elegiste, en tu propio ordenador, y ahí se quedan.",
            ]),
            ("Qué puede salir de tu ordenador", [
                "Solo lo que sigue. Cada cosa es algo que tú activas o que puedes desactivar.",
                "Sincronización. Si conectas una cuenta en la nube (pCloud, Google Drive, Dropbox, OneDrive, Box o Amazon S3), tu proyecto se copia en esa cuenta, y tus copias de seguridad también si así lo eliges. Los archivos van de tu ordenador al servicio que elegiste. Corylus no interviene en esa transferencia ni guarda copia alguna. Los datos de la conexión se guardan en tu ordenador.",
                "Voces en línea. La lectura en voz alta puede usar las voces de tu sistema operativo. Algunas funcionan por internet y la lista de voces las marca como «(en línea)»; cuando lee una de ellas, el texto va al servicio que hay detrás. Las voces naturales que Corylus ofrece como descarga funcionan en tu ordenador.",
                "La comprobación de versiones. Al arrancar, Corylus descarga un archivo pequeño de esta web o de GitHub para saber si hay una versión más nueva. La petición no lleva ningún identificador, aunque el servidor ve tu dirección IP como en cualquier petición web. Puedes desactivar la comprobación en los Ajustes.",
                "Las aplicaciones de IA que conectes. Si instalas el módulo MCP y conectas una aplicación de IA como Claude Desktop o Claude Code, esa aplicación puede leer lo que tú permitas, proyecto a proyecto, y solo edita si también se lo permites. Lo que lee va a su propio servicio, con su propia política de privacidad. Corylus solo acepta esas conexiones desde tu propio ordenador y mientras Corylus está abierto.",
                "Un fondo desde una dirección web. Si le das al modo sin distracciones un fondo con su dirección web, Corylus lo descarga de esa dirección.",
            ]),
            ("Descargas opcionales", [
                "Algunas funciones son descargas que tú eliges: diccionarios, el diccionario de sinónimos, los datos de idioma para las comprobaciones de estilo, el motor gramatical, las voces naturales, los sonidos ambientales, el programa de sincronización y el asistente. Cada una viene de donde la aloja quien la publica: GitHub, Hugging Face, languagetool.org, rclone.org u ollama.com. Esos servidores ven la petición, como en cualquier descarga. Corylus no les envía nada sobre ti ni sobre lo que escribes, y una vez instalados estos componentes funcionan en tu ordenador.",
            ]),
            ("Esta web", [
                "Este sitio está alojado en GitHub Pages. No pone cookies ni usa analítica. GitHub guarda registros de servidor, con direcciones IP incluidas, según su propia política de privacidad. La web carga sus tipografías de Google Fonts, así que Google sirve esos archivos y ve la petición. Los botones de descarga consultan a GitHub el número de la versión actual. Si eliges idioma con el enlace de idioma de la web, tu navegador guarda esa elección en tu dispositivo.",
            ]),
            ("Menores", ["Corylus no se dirige a menores y no recoge información de nadie, de ninguna edad."]),
            ("Cambios", ["Si esta política cambia, la nueva versión aparecerá en esta página con una fecha nueva. Como Corylus no recoge nada, un cambio aquí significaría casi con seguridad un componente opcional nuevo con su propio origen de descarga."]),
        ],
        "back": "Volver a Corylus",
    },
}


def privacy(t):
    p = t["dir_prefix"]
    other_href, other_label = t["other"]
    body = "".join(
        f"<h2>{esc(h)}</h2>" + "".join(f"<p>{esc(x)}</p>" for x in paras)
        for h, paras in t["sections"]
    )
    canonical = SITE + ("/es/privacy/" if t["lang"] == "es" else "/privacy/")
    return f"""<!doctype html>
<html lang="{t['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(t['title'])}</title>
<meta name="description" content="{esc(t['description'])}">
<meta name="theme-color" content="#F7F3EA" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0E1713" media="(prefers-color-scheme: dark)">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="en" href="{SITE}/privacy/">
<link rel="alternate" hreflang="es" href="{SITE}/es/privacy/">
<link rel="icon" href="{p}assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Literata:wght@400;700&family=Source+Sans+3:wght@400;600&display=swap">
<link rel="stylesheet" href="{p}assets/style.css">
</head>
<body>
<header class="site">
  <div class="wrap row">
    <a class="brand" href="{p}" aria-label="Corylus">
      <img src="{p}assets/lockup.svg" alt="Corylus" width="232" height="64" class="only-light">
      <img src="{p}assets/lockup-dark.svg" alt="Corylus" width="232" height="64" class="only-dark">
    </a>
    <nav><a href="{p}">{esc(t['back'])}</a><a class="lang" href="{other_href}">{esc(other_label)}</a></nav>
  </div>
</header>
<main id="main">
  <section class="hero">
    <div class="wrap narrow">
      <h1>{esc(t['h'])}</h1>
      <p class="lead">{esc(t['lead'])}</p>
      <p class="note">{esc(t['updated'])}</p>
    </div>
  </section>
  <section>
    <div class="wrap narrow prose">{body}</div>
  </section>
</main>
<footer class="site">
  <div class="wrap row">
    <p><img src="{p}assets/mark.svg" alt="" width="28" height="28" aria-hidden="true"> Corylus</p>
    <nav><a class="lang" href="{other_href}">{esc(other_label)}</a></nav>
  </div>
</footer>
</body>
</html>
"""


if __name__ == "__main__":
    out = {
        os.path.join(HERE, "index.html"): page(STRINGS["en"]),
        os.path.join(HERE, "es", "index.html"): page(STRINGS["es"]),
        os.path.join(HERE, "privacy", "index.html"): privacy(PRIVACY["en"]),
        os.path.join(HERE, "es", "privacy", "index.html"): privacy(PRIVACY["es"]),
    }
    for d in ("es", "privacy", "es/privacy"):
        os.makedirs(os.path.join(HERE, d), exist_ok=True)
    for path, body in out.items():
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(body)
        print("wrote", os.path.relpath(path, HERE))
