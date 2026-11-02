#!/usr/bin/env python3
"""Build the Corylus site: one content source, one template, two languages.

    python3 build.py

Writes index.html (English) and es/index.html (Spanish). Edit the copy in
STRINGS below — never the generated HTML, which is overwritten on every run.
"""
import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = "https://ludobermejoes.github.io/corylus-web"
REPO = "https://github.com/LudoBermejoES/corylus"
RELEASES_RAW = "https://raw.githubusercontent.com/LudoBermejoES/corylus-releases/main"

# Fill this in once the Patreon page exists; the support section hides itself
# while it is empty, so the site never ships a dead link.
PATREON = "https://www.patreon.com/c/corylus"

# Fallbacks, used only if the live manifest cannot be fetched. Keep in step with
# whatever is actually published.
FALLBACK = {"mac": "1.91.0", "win": "1.90.1"}

STRINGS = {
    "en": {
        "lang": "en",
        "dir_prefix": "",
        "other": ("es/", "Español"),
        "title": "Corylus — a writing tool that treats your words as yours",
        "description": (
            "A writing tool for novels and long work. Binder, corkboard, outliner, "
            "story bible, snapshots, export to Word, PDF and EPUB — built on plain "
            "Markdown files in an ordinary folder. No account, no cloud, no subscription."
        ),
        "skip": "Skip to content",
        "nav": [("#why", "Why"), ("#features", "Features"), ("#private", "Privacy"), ("#get", "Download")],
        "hero_h": "Your novel should outlive the app you wrote it in.",
        "hero_p": (
            "Corylus is a writing tool for long work — the organisation of a professional "
            "writing studio, built on plain Markdown files in a folder you own."
        ),
        "hero_note": "Free. No account. macOS, Windows, iPhone, iPad and Android.",
        "dl_mac": "Download for macOS",
        "dl_win": "Download for Windows",
        "dl_ver": "version",
        "dl_mobile": (
            "iPhone, iPad and Android builds exist and are tested on real devices, but are "
            "not on the stores yet — that needs developer accounts. Build them from source, "
            "or wait for the stores."
        ),
        "dl_gatekeeper": (
            "Corylus is not notarized yet. macOS will say the developer cannot be verified: "
            "right-click Corylus.app, choose Open, then Open again. Once per download. "
            "Fixing that properly costs $99 a year, which is the first thing support pays for."
        ),
        "why_h": "Files on disk, not a format you cannot open",
        "why_p1": (
            "Most writing software for long work puts your manuscript into a database, a "
            "bundle, or a cloud account, and you can only reach it through the one "
            "application that understands it. That is fine until the application stops being "
            "maintained, or changes its pricing, or you change computers."
        ),
        "why_p2": (
            "Corylus keeps every document as a plain Markdown file in a normal folder on your "
            "own disk. Not as an export option — as the live format. Open the folder while "
            "the app is running and your chapters are there, readable in any text editor. The "
            "database Corylus uses is a cache it rebuilds from those files, not where your "
            "work lives."
        ),
        "why_pull": (
            "If Corylus vanished tomorrow, your entire body of work would still be clean, "
            "portable, future-proof text."
        ),
        "tree_cap": "A Corylus project, as your file manager sees it.",
        "features_h": "What it does",
        "features": [
            ("Binder", "Folders, chapters and scenes in a tree you can drag around. A novel is 200 pieces, not one document."),
            ("Corkboard &amp; outliner", "The same structure as index cards or as a table of synopses, statuses and word counts."),
            ("Story Bible", "Characters, places, objects and notes, with relationships, backlinks and templates for the kind of thing each one is."),
            ("Snapshots", "Every draft of every document, with a full diff and one-click rollback. Plain timestamped files — no Git required."),
            ("Compile", "Assemble the binder in order and export to Word, PDF or EPUB, with real typography."),
            ("Spelling &amp; grammar", "Hunspell spell-check with a per-project dictionary, and an optional LanguageTool engine that runs locally."),
            ("Read aloud", "Hear your prose in your system's voices, or download natural neural voices that run on your own machine."),
            ("Your own sync", "Optional sync to your WebDAV, Dropbox or Drive. Atomic, conflict-aware writes. There is no Corylus server."),
        ],
        "private_h": "Nothing leaves your machine",
        "private": [
            ("No account", "There is no sign-up, because there is nothing to sign up to."),
            ("No server", "Corylus has no backend. Sync, if you want it, goes somewhere you control."),
            ("Local AI only", "Grammar, natural voices and the assistant are optional downloads that run on your own hardware. Your manuscript is never uploaded, because there is nowhere to upload it to."),
            ("Open format", "YAML front matter and Markdown. Readable in 2045 with a text editor."),
        ],
        "langs_h": "In English and Spanish",
        "langs_p": (
            "Interface, spell-check, grammar, thesaurus and reading voices — in both languages, "
            "not a translated menu bar. Most writing software treats Spanish as an afterthought."
        ),
        "support_h": "Support the work",
        "support_p": (
            "Corylus is built by one person and is free, with nothing behind a paywall. "
            "Support pays for the developer certificates that make it install like a real "
            "app, and then for the time to keep building it."
        ),
        "support_cta": "Become a supporter",
        "support_costs_h": "What support pays for",
        "support_costs": [
            ("$99 / year", "Apple Developer Program. This is what removes the \u201cdeveloper cannot be verified\u201d warning on macOS, and the only sane way to get iPhone and iPad builds to testers."),
            ("$200\u2013400 / year", "A Windows code-signing certificate, so SmartScreen stops telling people the installer is suspicious."),
            ("$25 once", "The Google Play developer account."),
            ("Then: time", "Corylus is currently built in the gaps around other work."),
        ],
        "get_h": "Get Corylus",
        "foot_src": "Source code",
        "foot_rel": "All releases",
        "foot_priv": "Privacy",
        "foot_note": "Corylus is the botanical name of the hazel — the old European tree of writing and wisdom.",
    },
    "es": {
        "lang": "es",
        "dir_prefix": "../",
        "other": ("../", "English"),
        "title": "Corylus — una herramienta de escritura donde tus palabras siguen siendo tuyas",
        "description": (
            "Una herramienta para escribir novela y obra larga. Cuaderno, corcho, esquema, "
            "biblia del guion, instantáneas, exportación a Word, PDF y EPUB, sobre archivos "
            "Markdown normales en una carpeta tuya. Sin cuenta, sin nube, sin suscripción."
        ),
        "skip": "Ir al contenido",
        "nav": [("#why", "Por qué"), ("#features", "Qué hace"), ("#private", "Privacidad"), ("#get", "Descargar")],
        "hero_h": "Tu novela debería durar más que el programa con el que la escribiste.",
        "hero_p": (
            "Corylus es una herramienta para obra larga: la organización de un estudio de "
            "escritura profesional, sobre archivos Markdown normales en una carpeta que es tuya."
        ),
        "hero_note": "Gratis. Sin cuenta. macOS, Windows, iPhone, iPad y Android.",
        "dl_mac": "Descargar para macOS",
        "dl_win": "Descargar para Windows",
        "dl_ver": "versión",
        "dl_mobile": (
            "Las versiones de iPhone, iPad y Android existen y están probadas en dispositivos "
            "reales, pero todavía no están en las tiendas: eso requiere cuentas de "
            "desarrollador. Puedes compilarlas desde el código, o esperar a las tiendas."
        ),
        "dl_gatekeeper": (
            "Corylus todavía no está notarizada. macOS dirá que no se puede verificar al "
            "desarrollador: haz clic derecho en Corylus.app, elige Abrir, y Abrir otra vez. "
            "Una vez por descarga. Arreglarlo de verdad cuesta 99 $ al año, y es lo primero "
            "que paga el apoyo."
        ),
        "why_h": "Archivos en tu disco, no un formato que no puedes abrir",
        "why_p1": (
            "Casi todos los programas para obra larga meten tu manuscrito en una base de "
            "datos, un paquete o una cuenta en la nube, y solo puedes llegar a él a través de "
            "la única aplicación que lo entiende. Eso va bien hasta que la aplicación deja de "
            "mantenerse, o cambia de precio, o cambias de ordenador."
        ),
        "why_p2": (
            "Corylus guarda cada documento como un archivo Markdown normal, en una carpeta "
            "normal, en tu propio disco. No como opción de exportar: como el formato real. "
            "Abre la carpeta con la aplicación funcionando y ahí están tus capítulos, "
            "legibles en cualquier editor de texto. La base de datos que usa Corylus es una "
            "caché que reconstruye a partir de esos archivos, no el sitio donde vive tu obra."
        ),
        "why_pull": (
            "Si Corylus desapareciera mañana, toda tu obra seguiría siendo texto limpio, "
            "portable y legible dentro de veinte años."
        ),
        "tree_cap": "Un proyecto de Corylus, tal y como lo ve tu gestor de archivos.",
        "features_h": "Qué hace",
        "features": [
            ("Cuaderno", "Carpetas, capítulos y escenas en un árbol que puedes reordenar arrastrando. Una novela son 200 piezas, no un documento."),
            ("Corcho y esquema", "La misma estructura en fichas, o en una tabla de sinopsis, estados y recuento de palabras."),
            ("Biblia del guion", "Personajes, lugares, objetos y notas, con relaciones, enlaces inversos y plantillas según el tipo de ficha."),
            ("Instantáneas", "Cada versión de cada documento, con diferencias completas y vuelta atrás en un clic. Archivos con fecha, sin necesidad de Git."),
            ("Compilar", "Monta el cuaderno en orden y exporta a Word, PDF o EPUB, con tipografía de verdad."),
            ("Ortografía y gramática", "Corrector Hunspell con diccionario por proyecto, y un motor LanguageTool opcional que funciona en local."),
            ("Lectura en voz alta", "Escucha tu prosa con las voces del sistema, o descarga voces naturales que funcionan en tu propia máquina."),
            ("Tu propia sincronización", "Sincronización opcional con tu WebDAV, Dropbox o Drive. Escrituras atómicas y conscientes de conflictos. No hay servidor de Corylus."),
        ],
        "private_h": "Nada sale de tu máquina",
        "private": [
            ("Sin cuenta", "No hay registro, porque no hay nada en lo que registrarse."),
            ("Sin servidor", "Corylus no tiene backend. La sincronización, si la quieres, va a donde tú decidas."),
            ("IA solo en local", "La gramática, las voces naturales y el asistente son descargas opcionales que funcionan en tu propio equipo. Tu manuscrito no se sube nunca, porque no hay ningún sitio al que subirlo."),
            ("Formato abierto", "Cabecera YAML y Markdown. Legible en 2045 con un editor de texto."),
        ],
        "langs_h": "En español e inglés",
        "langs_p": (
            "Interfaz, corrector ortográfico, gramática, diccionario de sinónimos y voces de "
            "lectura, en los dos idiomas, no un menú traducido. Casi todos los programas de "
            "escritura tratan el español como un añadido."
        ),
        "support_h": "Apoya el proyecto",
        "support_p": (
            "Corylus lo hace una sola persona y es gratis, sin nada detrás de un muro de pago. "
            "El apoyo paga los certificados de desarrollador que hacen que se instale como "
            "una aplicación de verdad, y después el tiempo para seguir construyéndola."
        ),
        "support_cta": "Hazte mecenas",
        "support_costs_h": "Qu\u00e9 paga el apoyo",
        "support_costs": [
            ("99 $ al a\u00f1o", "Programa de desarrollador de Apple. Es lo que quita el aviso de \u00abno se puede verificar al desarrollador\u00bb en macOS, y la \u00fanica forma sensata de hacer llegar versiones de iPhone y iPad a quien las prueba."),
            ("200\u2013400 $ al a\u00f1o", "Un certificado de firma para Windows, para que SmartScreen deje de decir que el instalador es sospechoso."),
            ("25 $ una vez", "La cuenta de desarrollador de Google Play."),
            ("Y despu\u00e9s: tiempo", "Corylus se construye ahora en los ratos que deja otro trabajo."),
        ],
        "get_h": "Consigue Corylus",
        "foot_src": "Código fuente",
        "foot_rel": "Todas las versiones",
        "foot_priv": "Privacidad",
        "foot_note": "Corylus es el nombre botánico del avellano, el viejo árbol europeo de la escritura y la sabiduría.",
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
└── Snapshots/
    └── Chapter I/
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
└── Snapshots/
    └── Capitulo I/
        └── 2026-11-02T09-14-22.md""",
}


def esc(s):
    return html.escape(s, quote=True)


def page(t):
    p = t["dir_prefix"]
    other_href, other_label = t["other"]
    nav = "".join(f'<a href="{h}">{esc(l)}</a>' for h, l in t["nav"])
    features = "".join(
        f"<li><h3>{h}</h3><p>{b}</p></li>" for h, b in t["features"]
    )
    private = "".join(
        f"<li><h3>{esc(h)}</h3><p>{esc(b)}</p></li>" for h, b in t["private"]
    )
    alt_en = SITE + "/"
    alt_es = SITE + "/es/"
    canonical = alt_es if t["lang"] == "es" else alt_en

    support = ""
    if PATREON:
        costs = "".join(
            f"<li><h3>{esc(a)}</h3><p>{esc(b)}</p></li>" for a, b in t["support_costs"]
        )
        support = f"""
    <section class="band" id="support">
      <div class="wrap narrow">
        <h2>{esc(t['support_h'])}</h2>
        <p>{esc(t['support_p'])}</p>
        <h3 class="costs-h">{esc(t['support_costs_h'])}</h3>
        <ul class="grid two costs">{costs}</ul>
        <p class="cta"><a class="btn" href="{PATREON}" rel="noopener">{esc(t['support_cta'])}</a></p>
      </div>
    </section>"""

    return f"""<!doctype html>
<html lang="{t['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
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
  </section>

  <section id="features">
    <div class="wrap">
      <h2>{esc(t['features_h'])}</h2>
      <ul class="grid">{features}</ul>
    </div>
  </section>

  <section class="band" id="private">
    <div class="wrap">
      <h2>{esc(t['private_h'])}</h2>
      <ul class="grid two">{private}</ul>
    </div>
  </section>

  <section id="langs">
    <div class="wrap narrow">
      <h2>{esc(t['langs_h'])}</h2>
      <p>{esc(t['langs_p'])}</p>
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
      <a href="{REPO}" rel="noopener">{esc(t['foot_src'])}</a>
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
        "lang": "en", "dir_prefix": "../", "other": ("../es/privacy/", "Espa\u00f1ol"),
        "title": "Privacy \u2014 Corylus",
        "description": "Corylus collects nothing. No accounts, no telemetry, no analytics, no server.",
        "h": "Privacy", "updated": "Last updated 2 November 2026.",
        "lead": "Corylus collects no personal data. This page explains what that means in practice, and names every third party your device talks to because of something Corylus does.",
        "sections": [('What Corylus collects', ['Nothing.', 'Corylus is a desktop and mobile writing application. It has no user accounts, no telemetry, no analytics and no crash reporting. There is no Corylus server for it to send anything to. Your documents are plain Markdown files in a folder you chose on your own device, and they stay there.']), ('Optional downloads', ['Some features are optional downloads: a grammar engine, natural read-aloud voices, dictionaries and thesauruses. When you choose to install one, your device fetches it from Hugging Face or GitHub. Those providers see the request, as they would for any download. Corylus sends them nothing about you or your writing, and the components run entirely on your own machine once installed.']), ('Synchronisation', ["Sync is optional and off by default. If you turn it on, your files go to a destination you configure and control — your own WebDAV server, Dropbox or Google Drive. Corylus is not a party to that transfer and keeps no copy. Your credentials for that service are stored in your operating system's keychain, never in the project and never transmitted anywhere else."]), ('Updates', ['On desktop, Corylus checks a static file on GitHub to see whether a newer version exists. That request reaches GitHub, which sees your IP address as it would for any web request. The check sends no identifier of any kind, and it can be switched off in Settings.']), ('This website', ['This site is hosted on GitHub Pages. It sets no cookies and runs no analytics. GitHub records server logs, including IP addresses, under its own privacy policy. The site loads fonts from Google Fonts, which means Google serves those font files and sees the request.']), ('Children', ['Corylus is not directed at children and collects no information from anyone, of any age.']), ('Changes', ['If this policy changes, the new version appears on this page with a new date. Since Corylus collects nothing, a change here would most likely mean a new optional component with its own download source.']), ('Contact', ["Questions about this policy: open an issue on the project's GitHub repository."])],
        "back": "Back to Corylus",
    },
    "es": {
        "lang": "es", "dir_prefix": "../../", "other": ("../../privacy/", "English"),
        "title": "Privacidad \u2014 Corylus",
        "description": "Corylus no recoge nada. Sin cuentas, sin telemetr\u00eda, sin anal\u00edtica, sin servidor.",
        "h": "Privacidad", "updated": "\u00daltima actualizaci\u00f3n: 2 de noviembre de 2026.",
        "lead": "Corylus no recoge datos personales. Esta p\u00e1gina explica qu\u00e9 significa eso en la pr\u00e1ctica y nombra a cada tercero con el que tu dispositivo habla por algo que haga Corylus.",
        "sections": [('Qué recoge Corylus', ['Nada.', 'Corylus es una aplicación de escritura para ordenador y móvil. No tiene cuentas de usuario, ni telemetría, ni analítica, ni informes de fallos. No hay ningún servidor de Corylus al que enviar nada. Tus documentos son archivos Markdown normales en una carpeta que tú elegiste, en tu propio dispositivo, y ahí se quedan.']), ('Descargas opcionales', ['Algunas funciones son descargas opcionales: un motor gramatical, voces naturales para la lectura en voz alta, diccionarios y sinónimos. Cuando decides instalar una, tu dispositivo la descarga de Hugging Face o de GitHub. Esos proveedores ven la petición, como en cualquier descarga. Corylus no les envía nada sobre ti ni sobre lo que escribes, y una vez instalados los componentes funcionan íntegramente en tu propia máquina.']), ('Sincronización', ['La sincronización es opcional y está desactivada por defecto. Si la activas, tus archivos van a un destino que tú configuras y controlas: tu propio servidor WebDAV, tu Dropbox o tu Google Drive. Corylus no interviene en esa transferencia ni guarda copia alguna. Las credenciales de ese servicio se guardan en el llavero de tu sistema operativo, nunca en el proyecto y nunca se envían a ningún otro sitio.']), ('Actualizaciones', ['En el escritorio, Corylus consulta un archivo estático en GitHub para saber si hay una versión más nueva. Esa petición llega a GitHub, que ve tu dirección IP como en cualquier petición web. La consulta no envía ningún identificador y se puede desactivar en los ajustes.']), ('Esta web', ['Este sitio está alojado en GitHub Pages. No pone cookies ni usa analítica. GitHub guarda registros de servidor, con direcciones IP incluidas, según su propia política de privacidad. La web carga tipografías de Google Fonts, así que Google sirve esos archivos y ve la petición.']), ('Menores', ['Corylus no se dirige a menores y no recoge información de nadie, de ninguna edad.']), ('Cambios', ['Si esta política cambia, la nueva versión aparecerá en esta página con una fecha nueva. Como Corylus no recoge nada, un cambio aquí significaría casi con seguridad un componente opcional nuevo con su propio origen de descarga.']), ('Contacto', ['Dudas sobre esta política: abre una incidencia en el repositorio del proyecto en GitHub.'])],
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
    <nav><a href="{REPO}" rel="noopener">GitHub</a><a class="lang" href="{other_href}">{other_label}</a></nav>
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
