// Website screenshots of the real Corylus app (web/assets/shots/<id>.webp).
//
// Run on Windows, against the e2e dev build started with
// WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS=--remote-debugging-port=9222:
//   node shots.mjs --seed        build the demo books under C:\tmp\corylus-site
//   node shots.mjs [ids…]        capture every shot, or just the ids given
//   add --lang es to either      the Spanish book and interface, into shots/es/
//
// Only ever opens the demo books it builds itself.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { connect, prepareApp, STORE } from '../../.claude/skills/corylus-video/assets/motor/lib/app.mjs';
import { CHAPTERS, ROUGH, SPARK_FIRST_DRAFT, SPANISH } from './shots-content.mjs';
import * as ESB from './shots-content-es.mjs';

const ARGS = process.argv.slice(2);
const LANG = ARGS.includes('--lang') ? ARGS[ARGS.indexOf('--lang') + 1] : 'en';
const ES = LANG === 'es';
// The words the shots point at in the English book; the Spanish book maps titles and these.
const EN_T = {
  repeated: 'night', thesaurus: 'happier', grammar: 'have', diffAnchor: 'stormy',
  commentQuote: 'rather let me say such the words of fate',
  commentText: 'Too knowing this early? Let the reader feel the fate before Victor names it.',
  commentReply: 'Agreed. Cut the aside and keep "the words of fate".',
  commentAuthor: 'Margaret', me: 'You',
  backupLabel: 'Before the read-through', snapFirst: 'First draft', snapSecond: 'After the read-through',
  diagTemplate: 'What I was doing, what I expected, and what happened instead.',
};
const T = (k) => (ES && ESB.T[k] !== undefined ? ESB.T[k] : EN_T[k] !== undefined ? EN_T[k] : k);

const HERE = path.dirname(fileURLToPath(import.meta.url));
const REPO = path.resolve(HERE, '../..');
const OUT = path.join(REPO, 'web/assets/shots', ES ? 'es' : '');
const SITE = 'C:\\tmp\\corylus-site';
const BOOK = path.join(SITE, ES ? 'Frankenstein (es).corylus' : 'Frankenstein.corylus');
const LIBRO = path.join(SITE, 'El faro de Arnela.corylus');

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
let slot = 0;

/** Run an async JS body in the app and return its (JSON-able) result.
 *  Never hand `evaluate` a promise (the bridge times out): fire into a slot, poll. */
async function run(page, body, timeout = 60000) {
  const k = `__shot${++slot}`;
  await page.evaluate(`(() => { window.${k} = { busy: true };
    (async () => { const invoke = window.__TAURI__.core.invoke; ${body} })()
      .then((v) => { window.${k} = { v: v === undefined ? null : v }; })
      .catch((e) => { window.${k} = { e: String(e && (e.message || JSON.stringify(e)) || e) }; });
    return 'fired'; })()`);
  await poll(page, `!window.${k}.busy`, timeout);  // the bridge caps one wait at 30 s
  const r = JSON.parse(await page.evaluate(`JSON.stringify(window.${k})`));
  if (r.e) throw new Error(r.e);
  return r.v;
}

async function openProject(page, root) {
  await run(page, `
    await invoke('open_project_cmd', { path: ${JSON.stringify(root)} });
    window.__router.push('/project/' + encodeURIComponent(${JSON.stringify(root)}));`);
  await page.waitForSelector('.binder', 15000);
  // The binder store can keep the previous project's tree; reload it from disk.
  await run(page, `const b = ${STORE('binder')}; if (b && b.load) await b.load();
    if (b && b.loadMeta) await b.loadMeta();  // the tab bar's project word total reads these
    const pm = ${STORE('projectMeta')}; if (pm) await pm.load();
    const t = ${STORE('storyBibleTree')}; if (t) { try { await t.loadBibleTree(); await t.loadEntries(); } catch (e) {} }`);
  await sleep(1500);
}

const SPANISH_META = { default_language: 'es',
  labels: [{ id: 'red', name: 'Tormenta', color: '#c0392b' }, { id: 'blue', name: 'Inés', color: '#2980b9' }],
  statuses: [{ id: 'outline', name: 'Esquema' }, { id: 'draft', name: 'Borrador' }, { id: 'revised', name: 'Revisado' }, { id: 'done', name: 'Terminado' }] };

// ── Seeding ──────────────────────────────────────────────────────────────────

const LABELS = [
  { id: 'red', name: 'Victor', color: '#c0392b' },
  { id: 'orange', name: 'Rough', color: '#e67e22' },
  { id: 'yellow', name: 'Research', color: '#f1c40f' },
  { id: 'green', name: 'Elizabeth', color: '#27ae60' },
  { id: 'blue', name: 'Walton', color: '#2980b9' },
  { id: 'purple', name: 'The Creature', color: '#8e44ad' },
];

async function addChapters(page, parentTitle, chapters) {
  return run(page, `
    const folder = await invoke('create_node', { args: { kind: 'folder', parent_ulid: null, title: ${JSON.stringify(parentTitle)} } });
    const out = {};
    for (const c of ${JSON.stringify(chapters)}) {
      const n = await invoke('create_node', { args: { kind: 'document', parent_ulid: folder.ulid, title: c.title } });
      await invoke('write_document_cmd', { args: { path: n.disk_path,
        meta: { id: n.ulid, title: c.title, synopsis: c.synopsis, label: c.label, status: c.status },
        body: c.body, expected_hash: '' } });
      out[c.title] = { ulid: n.ulid, path: n.disk_path };
    }
    return out;`);
}

async function setMeta(page, patch) {
  await run(page, `
    const m = await invoke('get_project_meta');
    await invoke('set_project_meta', { args: Object.assign({}, m, ${JSON.stringify(patch)}) });`);
}

async function seed(page) {
  fs.mkdirSync(SITE, { recursive: true });
  for (const p of [BOOK, LIBRO]) if (fs.existsSync(p)) fs.rmSync(p, { recursive: true });

  // Frankenstein: the tour's Story Bible seed, then a manuscript around it.
  await run(page, `await invoke('create_project_cmd', { path: ${JSON.stringify(BOOK)}, name: 'Frankenstein' });`);
  await openProject(page, BOOK);
  const { seedDemoProject } = await import(pathToFileURL(path.join(REPO, 'e2e/fixtures/demo-project/seed.ts')).href);
  await seedDemoProject(page);
  // Two names per relationship, as sembrar.mjs gives them.
  await run(page, `
    const pares = { creator: ['creator of', 'created by'], betrothed: ['betrothed to', 'betrothed to'],
      residence: ['lives at', 'home of'], friend: ['closest friend', 'closest friend'], family: ['family', 'family'] };
    const sbt = ${STORE('storyBibleTree')};
    if (sbt && !(sbt.entries || []).length) await sbt.loadEntries();
    for (const e of (sbt.entries || [])) {
      const rels = (await invoke('get_relationships_cmd', { args: { ulid: e.ulid } }) || []).filter((r) => r.outbound);
      if (!rels.length) continue;
      await invoke('set_relationships_cmd', { args: { fromUlid: e.ulid, relationships: rels.map((r) => ({
        toUlid: r.toUlid, relType: r.relType,
        forwardLabel: (pares[r.relType] || [r.forwardLabel])[0], reverseLabel: (pares[r.relType] || [0, r.reverseLabel])[1] })) } });
    }`);
  // The seed's two-line "Chapter One" would sit at the top of the binder; drop it.
  await run(page, `
    const n = (await invoke('list_binder')).find((x) => x.title === 'Chapter One');
    if (n) await invoke('trash_node', { ulid: n.ulid });`);
  const docs = await addChapters(page, 'Manuscript', CHAPTERS);
  Object.assign(docs, await addChapters(page, 'Drafts', [ROUGH]));
  // Snapshots of The Spark: an earlier wording, then the current one.
  const spark = docs['The Spark'];
  const cur = CHAPTERS.find((c) => c.title === 'The Spark');
  await run(page, `
    const s = ${JSON.stringify(spark)}, c = ${JSON.stringify(cur)};
    const meta = { id: s.ulid, title: c.title, synopsis: c.synopsis, label: c.label, status: c.status };
    await invoke('write_document_cmd', { args: { path: s.path, meta, body: ${JSON.stringify(SPARK_FIRST_DRAFT)}, expected_hash: '' } });
    await invoke('create_snapshot_cmd', { ulid: s.ulid, label: 'First draft' });
    await invoke('write_document_cmd', { args: { path: s.path, meta, body: c.body, expected_hash: '' } });
    await invoke('create_snapshot_cmd', { ulid: s.ulid, label: 'After the read-through' });`);
  await setMeta(page, { labels: LABELS, word_target: 80000 });
  console.log('seeded', BOOK);

  // The Spanish book.
  await run(page, `await invoke('create_project_cmd', { path: ${JSON.stringify(LIBRO)}, name: ${JSON.stringify(SPANISH.name)} });`);
  await openProject(page, LIBRO);
  await addChapters(page, 'Manuscrito', SPANISH.chapters);
  await setMeta(page, SPANISH_META);
  console.log('seeded', LIBRO);

  // Every save through write_document_cmd indexes the document with a word count of 0;
  // only a full rebuild (an empty index) counts words. Drop each book's index while
  // it is closed so the next open rebuilds it, or the tab bar shows "Project: 0 / …".
  dropIndex(BOOK);
  await openProject(page, BOOK);
  dropIndex(LIBRO);
}

async function seedEs(page) {
  fs.mkdirSync(SITE, { recursive: true });
  if (fs.existsSync(BOOK)) fs.rmSync(BOOK, { recursive: true });
  await run(page, `await invoke('create_project_cmd', { path: ${JSON.stringify(BOOK)}, name: ${JSON.stringify(ESB.BOOK_NAME)} });`);
  await openProject(page, BOOK);
  await setMeta(page, { default_language: 'es', labels: ESB.LABELS, statuses: ESB.STATUSES, word_target: 80000 });

  // Story Bible: bare entries, covers, then the fields (as the English seed does).
  const IMG = path.join(REPO, 'doc/img');
  const ref = {};
  const entries = [...ESB.CHARACTERS.map((c) => ['Character', c]), ...ESB.LOCATIONS.map((l) => ['Location', l]), ['Theme', ESB.THEME]];
  for (const [type, e] of entries) {
    ref[e.title] = await run(page, `const c = await invoke('create_story_entry_cmd', { args: { entryType: ${JSON.stringify(type)}, title: ${JSON.stringify(e.title)} } });
      return { ulid: c.ulid, relPath: c.relPath };`);
  }
  for (const [type, e] of entries) {
    const { title, synopsis, cover, ...fields } = e;
    const extra = { type, ...fields };
    if (cover) {
      const bytes = Array.from(fs.readFileSync(path.join(IMG, cover)));
      extra.cover = await run(page, `return (await invoke('storybible_save_asset_cmd', { args: { bytes: ${JSON.stringify(bytes)}, ext: 'png' } })).relPath;`, 120000);
    }
    await run(page, `await invoke('write_document_cmd', { args: { path: ${JSON.stringify(ref[title].relPath)},
      meta: { id: ${JSON.stringify(ref[title].ulid)}, title: ${JSON.stringify(title)}, synopsis: ${JSON.stringify(synopsis)}, extra: ${JSON.stringify(extra)} },
      body: '', expected_hash: '' } });`);
  }
  // Relationships last (a later frontmatter write would drop them), one call per source.
  const bySource = {};
  for (const [from, to, relType, fwd, rev] of ESB.RELATIONSHIPS) {
    (bySource[from] ||= []).push({ toUlid: ref[to].ulid, relType, forwardLabel: fwd, reverseLabel: rev });
  }
  for (const [from, rels] of Object.entries(bySource)) {
    await run(page, `await invoke('set_relationships_cmd', { args: { fromUlid: ${JSON.stringify(ref[from].ulid)}, relationships: ${JSON.stringify(rels)} } });`);
  }

  const docs = await addChapters(page, ESB.T['Manuscript'], ESB.CHAPTERS);
  Object.assign(docs, await addChapters(page, ESB.T['Drafts'], [ESB.ROUGH]));
  const spark = docs[ESB.T['The Spark']];
  const cur = ESB.CHAPTERS.find((c) => c.title === ESB.T['The Spark']);
  await run(page, `
    const s = ${JSON.stringify(spark)}, c = ${JSON.stringify(cur)};
    const meta = { id: s.ulid, title: c.title, synopsis: c.synopsis, label: c.label, status: c.status };
    await invoke('write_document_cmd', { args: { path: s.path, meta, body: ${JSON.stringify(ESB.SPARK_FIRST_DRAFT)}, expected_hash: '' } });
    await invoke('create_snapshot_cmd', { ulid: s.ulid, label: ${JSON.stringify(ESB.T.snapFirst)} });
    await invoke('write_document_cmd', { args: { path: s.path, meta, body: c.body, expected_hash: '' } });
    await invoke('create_snapshot_cmd', { ulid: s.ulid, label: ${JSON.stringify(ESB.T.snapSecond)} });`);
  await run(page, `const t = ${STORE('storyBibleTree')}; await t.loadBibleTree(); await t.loadEntries(); await ${STORE('binder')}.load();`);
  console.log('seeded', BOOK);
}

function dropIndex(root) {
  const marker = fs.readdirSync(root).find((f) => f.startsWith('.corylus-id-'));
  const dir = path.join(process.env.APPDATA, 'com.corylus.app.e2e', 'projects', marker.slice('.corylus-id-'.length));
  try { fs.rmSync(dir, { recursive: true, force: true }); } catch (e) { console.log(`could not drop the index of ${root}: ${e.message}`); }
}

// ── Driving the app ──────────────────────────────────────────────────────────

const ANALYSES = ['repetitionEnabled', 'rhymeEnabled', 'adjectiveEnabled', 'adverbEnabled', 'gerundEnabled',
  'structureSkeletonEnabled', 'structureOpeningsEnabled', 'structureLengthEnabled', 'structureAdverbPileupEnabled',
  'structureNominalEnabled', 'structureGerundFreqEnabled', 'structureAdjPositionEnabled', 'structureIngOpenerEnabled',
  'multipleSpacesEnabled'];

/** A clean, light, English app: no dialogs, no analyses, no modes. */
async function reset(page, { theme = 'system-light', canvas = 'white', locale = LANG } = {}) {
  await prepareApp(page);
  await page.evaluate(`(() => {
    const ui = ${STORE('ui')}, s = ${STORE('settings')}, th = ${STORE('theming')}, pm = ${STORE('projectMeta')};
    ['closeSettings','closeCompile','closeStatistics','closeAmbientMixer','closePalette','closeImport']
      .forEach((f) => { try { ui[f](); } catch (e) {} });
    ${JSON.stringify(ANALYSES)}.forEach((k) => { s[k] = false; });
    s.grammarEnabled = false;  // LanguageTool squiggles only in the grammar shot
    // Names the bundled dictionary lacks; the planted misspelling stays flagged.
    try { ${JSON.stringify(ES ? ['Elizabeth', 'Londres', 'Ingolstadt', 'Walton', 'Clerval', 'Lacey', 'Frankenstein', 'Margarita', 'Ginebra'] : [])}.forEach((w) => ${STORE('spellcheck')}.ignore(w)); } catch (e) {}
    s.locale = ${JSON.stringify(locale)};
    try { window.__i18n.global.locale.value = ${JSON.stringify(locale)}; } catch (e) {}
    th.applyChrome(${JSON.stringify(theme)}); th.applyCanvas(${JSON.stringify(canvas)});
    if (pm.distractionFree) pm.toggleDistractionFree();
    pm.setFocusUnit('off'); if (pm.typewriter) pm.toggleTypewriter();
    try { ${STORE('readAloud')}.stop(); } catch (e) {}
    try { ${STORE('ambientSoundsPlayback')}.resetAll(); } catch (e) {}
    const m = document.querySelector('.mode-btn--active'); if (m) m.click();
    document.querySelectorAll('.editor-wrapper').forEach((w) => w.click());  // closes a context menu
    try { ${STORE('tabs')}.closeAll(); } catch (e) {}
    document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
    return 'ok';
  })()`);
  await sleep(400);
}

async function inspector(page, tab) {
  await page.evaluate(`(() => { const ui = ${STORE('ui')};
    if (ui.inspectorOpen !== ${!!tab}) ui.toggleInspector();
    ${tab ? `ui.setInspectorTab(${JSON.stringify(tab)});` : ''} return 'ok'; })()`);
  await sleep(500);
}

/** Open a binder node (document tab, or just select a folder). */
async function open(page, title) {
  title = T(title);
  const r = await page.evaluate(`(() => {
    const binder = ${STORE('binder')}, tabs = ${STORE('tabs')};
    const n = binder.nodes.find((x) => x.title === ${JSON.stringify(title)} && !String(x.disk_path || '').startsWith('StoryBible'));
    if (!n) return 'not found';
    const m = document.querySelector('.mode-btn--active'); if (m) m.click();
    binder.selectNode(n.ulid);
    if (n.kind === 'document') tabs.open({ type: 'document', ulid: n.ulid, diskPath: n.disk_path, title: n.title });
    return 'ok'; })()`);
  if (r !== 'ok') throw new Error(`open ${title}: ${r}`);
  await sleep(1500);
}

async function mode(page, m) {
  await page.evaluate(`(() => { const b = document.querySelector('[data-testid="workspace-mode-${m}"]'); if (b) b.click(); return !!b; })()`);
  await sleep(1500);
}

async function analyses(page, keys) {
  await page.evaluate(`(() => { const s = ${STORE('settings')}; ${JSON.stringify(keys)}.forEach((k) => { s[k] = true; }); return 'ok'; })()`);
}

/** Expand every folder in the binder so the shot shows the book's shape. */
async function expandBinder(page) {
  await page.evaluate(`(() => { const b = ${STORE('binder')};
    let open = b.tree.expandedUlids; if (open && open.value !== undefined) open = open.value;
    const isOpen = (u) => open instanceof Set ? open.has(u) : Array.isArray(open) ? open.includes(u) : !!(open && open[u]);
    b.nodes.filter((n) => n.kind === 'folder' && !String(n.disk_path || '').startsWith('StoryBible'))
      .forEach((n) => { if (!isOpen(n.ulid)) b.toggleExpand(n.ulid); });
    return 'ok'; })()`);
}

const RETRATO = `Array.from(document.querySelectorAll('img')).some((i) => i.complete && i.naturalWidth > 80 && i.offsetParent && i.getBoundingClientRect().width > 60)`;

async function openBible(page, title) {
  title = T(title);
  await run(page, `
    const sbt = ${STORE('storyBibleTree')}, tabs = ${STORE('tabs')}, es = ${STORE('storyBibleEntry')};
    const m = document.querySelector('.mode-btn--active'); if (m) m.click();
    if (!(sbt.bibleNodes || []).length) await sbt.loadBibleTree();
    const n = sbt.bibleNodes.find((x) => x.title === ${JSON.stringify(title)});
    try { sbt.bibleSingle(n.ulid); } catch (e) {}
    const key = tabs.open({ type: 'entry', ulid: n.ulid, diskPath: n.disk_path, title: n.title });
    if (!sbt.entries || !sbt.entries.length) await sbt.loadEntries();
    const row = sbt.entries.find((e) => e.ulid === n.ulid) || sbt.entries.find((e) => e.title === n.title);
    await es.openEntryById(row, key);`);
  await page.waitForFunction(RETRATO, 15000).catch(() => {});
  await sleep(800);
}

// ── The shots ────────────────────────────────────────────────────────────────

// Clean-up a shot needs once captured, run even if it failed.
const AFTER = {
  diagnostics: (page) => page.evaluate(`(() => { const c = document.querySelector('[data-testid="send-diagnostics-cancel"]'); if (c) c.click();
    ${STORE('ui')}.closeSettings(); return 'ok'; })()`),
};

const SHOTS = {
  editor: async (page) => {
    await reset(page);
    await expandBinder(page);
    await open(page, 'By the Lake');
    await inspector(page, 'metadata');
  },
  corkboard: async (page) => {
    await reset(page);
    await inspector(page, null);
    await open(page, 'Manuscript');
    await mode(page, 'corkboard');
  },
  outliner: async (page) => {
    await reset(page);
    await inspector(page, null);
    await open(page, 'Manuscript');
    await mode(page, 'outliner');
  },
  'story-bible-entry': async (page) => {
    await reset(page);
    await inspector(page, null);
    await openBible(page, 'Victor Frankenstein');
  },
  'relationship-map': async (page) => {
    await reset(page);
    await inspector(page, null);
    const titles = ['Victor Frankenstein', 'The Creature', 'Elizabeth Lavenza', 'Villa Frankenstein'].map(T);
    const ulids = await page.evaluate(`JSON.stringify(${JSON.stringify(titles)}.map((t) => (${STORE('storyBibleTree')}.bibleNodes.find((n) => n.title === t) || {}).ulid))`).then(JSON.parse);
    // Reuse the canvas from an earlier run, so re-captures do not pile them up.
    const canvasUlid = await run(page, `
      const tabs = ${STORE('tabs')}, canvas = ${STORE('storyBibleCanvas')};
      const name = ${JSON.stringify(T('Character Map'))};
      let c = (await invoke('list_binder')).find((n) => n.kind === 'canvas' && n.title === name && !n.trashed);
      const fresh = !c;
      if (!c) c = await invoke('create_node', { args: { parent_ulid: null, kind: 'canvas', title: name, canvas_kind: 'relationship-map' } });
      const key = 'canvas:' + c.ulid;
      tabs.open({ type: 'canvas', ulid: c.ulid, diskPath: c.disk_path, title: name });
      await canvas.openCanvas({ ulid: c.ulid, diskPath: c.disk_path, kind: 'relationship-map', name }, key);
      return c.ulid;`);
    await page.waitForSelector(`[data-testid="sb-canvas-flow-${canvasUlid}"]`, 15000);
    await sleep(1000);
    for (const u of ulids) {
      if (await page.evaluate(`!!document.querySelector('[data-testid="canvas-node-entry-${u}"]')`)) continue;
      await page.click('[data-testid="sb-canvas-tool-entry"]').catch(() => {});
      await page.waitForSelector('[data-testid="sb-canvas-entry-picker"]', 8000).catch(() => {});
      await page.click(`[data-testid="sb-canvas-picker-entry-${u}"]`).catch(() => {});
      await page.waitForSelector(`[data-testid="canvas-node-entry-${u}"]`, 8000).catch(() => {});
      await sleep(500);
    }
    await page.evaluate(`(() => { const u = ${JSON.stringify(ulids)}; const pos = {};
      pos[u[0]] = { x: 420, y: 372 };
      u.slice(1).forEach((x, i) => { const a = -Math.PI / 2 + i * 2 * Math.PI / 3;
        pos[x] = { x: Math.round(420 + 300 * Math.cos(a)), y: Math.round(372 + 260 * Math.sin(a)) }; });
      window.__canvas.setEntryNodePositions(pos, 0.42); return 'ok'; })()`);
    await sleep(1000);
    await page.evaluate('window.__canvas.fitView()');
    await page.waitForFunction(`document.querySelectorAll('.vue-flow__edge').length >= 3`, 10000).catch(() => {});
    await sleep(1500);
    await page.evaluate('window.__canvas.fitView()');
    await sleep(1000);
  },
  continuous: async (page) => {
    await reset(page);
    await inspector(page, null);
    await expandBinder(page);
    await open(page, 'Manuscript');
    // view.openContinuous is Mod+Shift+C.
    await page.evaluate(`(() => { window.dispatchEvent(new KeyboardEvent('keydown', { key: 'C', code: 'KeyC', ctrlKey: true, shiftKey: true, bubbles: true })); return 'ok'; })()`);
    await sleep(2500);
    // Land between two chapters, so the shot shows the seam.
    // Land on the seam between the first two chapters. Each chapter starts at an <hr>;
    // its title is drawn by CSS, so there is no heading element to find.
    await page.evaluate(`(() => { const h = document.querySelectorAll('.continuous-view .ProseMirror > hr')[1];
      if (h) h.scrollIntoView({ block: 'center' }); return !!h; })()`);
    await sleep(800);
  },
  'analysis-repetition': async (page) => {
    await reset(page);
    await inspector(page, null);
    await analyses(page, ['repetitionEnabled']);
    await open(page, 'The Spark (rough draft)');
    await page.waitForSelector('.repetition-mark', 8000);
    await page.evaluate(`(() => { const el = Array.from(document.querySelectorAll('.repetition-mark')).find((e) => e.textContent.toLowerCase() === ${JSON.stringify(T('repeated'))}) || document.querySelector('.repetition-mark');
      const r = el.getBoundingClientRect();
      el.dispatchEvent(new MouseEvent('mousemove', { bubbles: true, clientX: r.left + r.width / 2, clientY: r.top + r.height / 2 })); return 'ok'; })()`);
    await page.waitForSelector('.analysis-tooltip', 5000).catch(() => {});
  },
  'analysis-structure': async (page) => {
    await reset(page);
    await inspector(page, null);
    await analyses(page, ['structureOpeningsEnabled', 'structureLengthEnabled']);
    await open(page, 'The Spark (rough draft)');
    await page.waitForSelector('.structure-openings-mark, .structure-length-mark', 8000);
  },
  'analysis-style': async (page) => {
    await reset(page);
    await inspector(page, null);
    await analyses(page, ['adverbEnabled', 'gerundEnabled', 'adjectiveEnabled']);
    await open(page, 'The Spark (rough draft)');
    await page.waitForSelector('.pos-adverb-mark', 8000);
  },
  rhyme: async (page) => {
    await reset(page);
    await inspector(page, null);
    await analyses(page, ['rhymeEnabled']);
    await open(page, 'The Spark (rough draft)');
    await page.waitForSelector('[class*="rhyme"]', 8000);
  },
  thesaurus: async (page) => {
    await reset(page);
    await inspector(page, null);
    await open(page, 'By the Lake');
    // The Spanish thesaurus is a download; fetch it into the e2e app the first time.
    await run(page, `
      if ((await invoke('thesaurus_get_status', { lang: ${JSON.stringify(LANG)} })).kind === 'ready') return;
      await invoke('thesaurus_install', { lang: ${JSON.stringify(LANG)} });
      for (let i = 0; i < 300; i++) { if ((await invoke('thesaurus_get_status', { lang: ${JSON.stringify(LANG)} })).kind === 'ready') return; await new Promise((r) => setTimeout(r, 2000)); }
      throw new Error('thesaurus did not install');`, 700000);
    await rightClickWord(page, T('thesaurus'));
    await page.waitForSelector('.spell-context-menu', 5000);
    await sleep(1500);
  },
  grammar: async (page) => {
    await reset(page);
    await inspector(page, null);
    // Status can say "ready" while the server no longer answers; a real check is the only test.
    await run(page, `
      const ok = async () => { try { await invoke('check_grammar', { text: 'He have waited.', lang: 'en' }); return true; } catch (e) { return false; } };
      if ((await invoke('lt_get_status')).kind === 'ready' && await ok()) return;
      try { await invoke('lt_stop'); } catch (e) {}
      await invoke('lt_start');
      for (let i = 0; i < 90; i++) { if ((await invoke('lt_get_status')).kind === 'ready' && await ok()) return; await new Promise((r) => setTimeout(r, 2000)); }
      throw new Error('LanguageTool did not come up');`, 300000);
    await page.evaluate(`${STORE('settings')}.grammarEnabled = true`);
    // The check runs when a document loads; a load that raced the engine's start gets none, so reopen.
    for (let i = 0; ; i++) {
      await page.evaluate(`${STORE('tabs')}.closeAll()`);
      await open(page, 'The Spark (rough draft)');
      try { await poll(page, `!!document.querySelector('.grammar-error')`, 30000); break; } catch (e) { if (i === 3) throw e; }
    }
    await sleep(1000);
    await page.evaluate(`(() => { const all = Array.from(document.querySelectorAll('.grammar-error'));
      const el = all.find((e) => e.textContent.trim() === ${JSON.stringify(T('grammar'))}) || all[0];
      const r = el.getBoundingClientRect();
      el.dispatchEvent(new MouseEvent('contextmenu', { bubbles: true, cancelable: true, view: window, clientX: r.left + r.width / 2, clientY: r.top + r.height / 2 })); return 'ok'; })()`);
    await sleep(1500);
  },
  'distraction-free': async (page) => {
    await reset(page);
    await inspector(page, null);
    // The background is the gallery's train (video/vehicles/train-scene-1), added through the
    // same path as the gallery's «Add to Corylus» link (a public file, 61.8 MB) if not kept yet.
    await run(page, `const g = ${STORE('galleryLink')}; await g.loadLibrary();
      let it = (g.library.items || []).find((i) => i.id === 'video/vehicles/train-scene-1');
      if (!it) { g.offer('video/vehicles/train-scene-1');
        for (let i = 0; i < 100 && g.phase !== 'confirm' && g.phase !== 'error'; i++) await new Promise((r) => setTimeout(r, 300));
        if (g.phase !== 'confirm') throw new Error('gallery: ' + g.phase + ' ' + g.errorReason);
        await g.confirm(true); for (let i = 0; i < 600 && g.phase === 'downloading'; i++) await new Promise((r) => setTimeout(r, 300));
        if (g.phase !== 'done') throw new Error('gallery download: ' + g.phase); g.close?.();
        await g.loadLibrary(); it = g.library.items.find((i) => i.id === 'video/vehicles/train-scene-1'); }
      await g.useFromLibrary(it.file, it.kind);`, 240000);
    await open(page, 'The Spark');
    await page.evaluate(`(() => { const s = ${STORE('settings')}; s.dfPageOpacity = 0.94; ${STORE('theming')}.applyDfPageOpacity(0.94); ${STORE('projectMeta')}.toggleDistractionFree(); return 'ok'; })()`);
    // Mid-motion, not a first or black frame: the train playing, several seconds in.
    await poll(page, `(() => { const v = document.querySelector('[data-testid="df-background-video"]'); return !!v && !v.paused && v.readyState >= 3 && v.currentTime > 6; })()`, 30000);
    // Wake the HUD: it shows on pointer movement.
    await page.evaluate(`(() => { document.querySelector('.editor-main').dispatchEvent(new MouseEvent('mousemove', { bubbles: true, clientX: 700, clientY: 790 })); return 'ok'; })()`);
    await sleep(600);
  },
  'ambient-sounds': async (page) => {
    await reset(page);
    await inspector(page, null);
    await open(page, 'The Hovel');
    const st = await run(page, `return (await invoke('ambient_sounds_get_status')).kind;`);
    if (st !== 'ready') {
      await run(page, `await invoke('ambient_sounds_install');`, 600000);
      await poll(page, `(window.__amb = window.__amb || (window.__TAURI__.core.invoke('ambient_sounds_get_status').then((s) => { window.__ambkind = s.kind; window.__amb = null; }), 1)) && window.__ambkind === 'ready'`, 600000);
      await run(page, `await ${STORE('ambientSoundsStatus')}.ensureInitialized();`);
    }
    await page.evaluate(`${STORE('ui')}.openAmbientMixer()`);
    await sleep(1500);
    // A mix in progress; paused at once so the capture run stays quiet.
    await run(page, `const p = ${STORE('ambientSoundsPlayback')};
      for (const [c, id, v] of [['rain', 'rain_on_window', 0.7], ['nature', 'campfire', 0.45], ['nature', 'distant_thunder', 0.25]]) await p.setVolume(c, id, v);
      p.pauseAll();`);
    await sleep(800);
  },
  snapshots: async (page) => {
    await reset(page);
    await open(page, 'The Spark');
    await inspector(page, 'snapshots');
    await run(page, `const b = ${STORE('binder')}; const n = b.nodes.find((x) => x.title === ${JSON.stringify(T('The Spark'))}); await ${STORE('snapshot')}.loadSnapshots(n.ulid);`);
    await page.waitForSelector('.snapshot-item', 8000);
    await page.evaluate(`(() => { const items = document.querySelectorAll('.snapshot-item');
      const it = Array.from(items).find((i) => i.textContent.includes(${JSON.stringify(T('snapFirst'))}));
      const btn = it && it.querySelector('.snapshot-item__actions .btn--sm'); if (btn) btn.click(); return !!btn; })()`);
    await page.waitForSelector('.snapshot-panel__diff', 8000).catch(() => {});
    await sleep(1000);
    // The diff opens on the front matter; scroll to where the prose changes.
    await page.evaluate(`(() => { const d = document.querySelector('.snapshot-panel__diff');
      const w = document.createTreeWalker(d, NodeFilter.SHOW_TEXT); let n;
      while ((n = w.nextNode())) if (n.textContent.includes(${JSON.stringify(T('diffAnchor'))})) {
        const el = n.parentElement; let p = el.parentElement;
        while (p && p.scrollHeight <= p.clientHeight + 2) p = p.parentElement;
        if (p) p.scrollTop += el.getBoundingClientRect().top - p.getBoundingClientRect().top - 60;
        return !!p; }
      return false; })()`);
    await sleep(500);
  },
  compile: async (page) => {
    await reset(page);
    await inspector(page, null);
    await open(page, 'Manuscript');
    await page.evaluate(`${STORE('ui')}.openCompile()`);
    await page.waitForSelector('[data-testid="compile-dialog"]', 8000);
    await sleep(1500);
  },
  'read-aloud': async (page) => {
    await reset(page);
    await inspector(page, null);
    await open(page, 'Letter I');
    await page.evaluate(`(() => { window.__tiptap__.commands.setTextSelection(1); ${STORE('readAloud')}.start(); return 'ok'; })()`);
    await page.waitForFunction(`${STORE('readAloud')}.status === 'playing' || !!${STORE('readAloud')}.error`, 20000);
    await sleep(2500);
    await page.evaluate(`${STORE('readAloud')}.pause()`);
    await sleep(500);
  },
  comments: async (page) => {
    await reset(page);
    await open(page, 'The University');
    await inspector(page, 'comments');
    await sleep(800);
    if (!(await page.evaluate(`document.querySelectorAll('[data-testid^="comment-item-"]').length`))) {
      // What addCommentToSelection does, but with the comment's text filled in.
      await run(page, `
        const ed = window.__tiptap__, cs = ${STORE('comments')}, b = ${STORE('binder')};
        const node = b.nodes.find((x) => x.title === ${JSON.stringify(T('The University'))});
        const q = ${JSON.stringify(T('commentQuote'))};
        let from = -1;
        ed.state.doc.descendants((n, pos) => { if (from < 0 && n.isText) { const i = n.text.indexOf(q); if (i >= 0) from = pos + i; } });
        ed.chain().setTextSelection({ from, to: from + q.length }).setMark('comment', { id: '01M7SHOTC0MMENT0000000001' }).run();
        const at = new Date().toISOString();
        await cs.addComment(node.ulid, '01M7SHOTC0MMENT0000000001', q, ${JSON.stringify(T('commentText'))}, ${JSON.stringify(T('commentAuthor'))}, at);
        await cs.addReply('01M7SHOTC0MMENT0000000001', ${JSON.stringify(T('commentReply'))}, ${JSON.stringify(T('me'))}, at);
        if (window.__docSave__) await window.__docSave__();`);
      await sleep(1500);
      // Reopen so the comment highlight is drawn from the saved file.
      await page.evaluate(`${STORE('tabs')}.closeAll()`);
      await open(page, 'The University');
      await inspector(page, 'comments');
    }
    await page.evaluate(`window.__tiptap__.commands.setTextSelection(1)`);
    await sleep(800);
  },
  sync: async (page) => {
    await reset(page);
    await inspector(page, null);
    await open(page, 'Letter I');
    await page.evaluate(`(() => { const ui = ${STORE('ui')}; ui.openSettings(); ui.openSettingsCategory('cloud'); return 'ok'; })()`);
    await sleep(500);
    await page.click('[data-testid="settings-cat-cloud"]').catch(() => {});
    await sleep(1500);
    if (!(await page.evaluate(`!!document.querySelector('[data-testid="cloud-provider-select"]')`))) {
      await page.evaluate(`(() => { const b = document.querySelector('[data-testid="cloud-rclone-start-btn"]'); if (b) b.click(); return !!b; })()`);
      await poll(page, `!!document.querySelector('[data-testid="cloud-provider-select"]')`, 60000);
      await sleep(800);
    }
    // Show the provider list open: a native <select> popup is not in the page's pixels.
    await page.evaluate(`(() => { const sel = document.querySelector('[data-testid="cloud-provider-select"]');
      sel.size = Math.min(sel.options.length, 9); sel.scrollIntoView({ block: 'center' }); return sel.options.length; })()`);
    await sleep(500);
  },
  backups: async (page) => {
    await reset(page);
    await inspector(page, null);
    // Backups are named by the second; space them out or they overwrite each other.
    // Retention keeps one backup per stretch of time, so a burst of three leaves one: make it a named one.
    const latest = await run(page, `const b = await invoke('list_backups'); return b.length ? b[0].label : null;`);
    if (latest !== T('backupLabel')) await run(page, `await invoke('run_backup_cmd', { label: ${JSON.stringify(T('backupLabel'))} });`);
    await open(page, 'Letter I');
    await page.evaluate(`(() => { const ui = ${STORE('ui')}; ui.openSettings(); ui.openSettingsCategory('snapshots'); return 'ok'; })()`);
    await sleep(500);
    await page.click('[data-testid="settings-cat-snapshots"]').catch(() => {});
    await sleep(1500);
  },
  // The Send diagnostics dialog over Settings → About: the template description, name and
  // email empty. Never sends: AFTER.diagnostics closes it with Cancel once captured.
  diagnostics: async (page) => {
    await reset(page);
    await inspector(page, null);
    await open(page, 'Letter I');
    await page.evaluate(`(() => { const ui = ${STORE('ui')}; ui.openSettings(); ui.openSettingsCategory('about'); return 'ok'; })()`);
    await sleep(500);
    await page.click('[data-testid="settings-cat-about"]').catch(() => {});
    await sleep(800);
    await page.evaluate(`(() => { document.querySelector('[data-setting="diagnostics"]').scrollIntoView({ block: 'center' }); document.querySelector('[data-testid="settings-send-diagnostics"]').click(); return 'ok'; })()`);
    await poll(page, `!!document.querySelector('[data-testid="send-diagnostics-message"]')`, 8000);
    await page.evaluate(`(() => { const t = document.querySelector('[data-testid="send-diagnostics-message"]');
      Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, 'value').set.call(t, ${JSON.stringify(T('diagTemplate'))});
      t.dispatchEvent(new Event('input', { bubbles: true })); t.blur(); return 'ok'; })()`);
    await sleep(500);
  },
  themes: async (page) => {
    await reset(page, { theme: 'catppuccin-mocha', canvas: 'night' });
    await expandBinder(page);
    await open(page, 'The Spark');
    await inspector(page, null);
  },
  spanish: async (page) => {
    await setMeta(page, SPANISH_META);
    await run(page, `await ${STORE('projectMeta')}.load();`);
    await reset(page, { locale: 'es' });
    await expandBinder(page);
    await open(page, 'I. La llegada');
    await inspector(page, 'metadata');
  },
  statistics: async (page) => {
    await reset(page);
    await inspector(page, null);
    await open(page, 'The Spark');
    await open(page, 'Manuscript');
    await page.evaluate(`${STORE('ui')}.openStatistics()`);
    await sleep(2500);
  },
  methodology: async (page) => {
    await reset(page);
    await inspector(page, null);
    await open(page, 'Letter I');
    await page.click('[data-testid="sb-tree-wizard-btn"]');
    await sleep(2000);
  },
};

/** Windows renders text with ClearType colour fringes; a 256-colour palette turns
 *  those into yellow smudges. A composited #app layer makes Chromium use greyscale
 *  antialiasing for the capture only. */
async function grayscaleText(page, on) {
  await page.evaluate(`(() => { let s = document.getElementById('shot-aa');
    if (${on} && !s) { s = document.createElement('style'); s.id = 'shot-aa';
      s.textContent = '#app { will-change: transform; }'; document.head.appendChild(s); }
    if (!${on} && s) s.remove(); return 'ok'; })()`);
}

async function poll(page, expr, ms) {
  const end = Date.now() + ms;
  while (Date.now() < end) { if (await page.evaluate(expr)) return; await sleep(1000); }
  throw new Error(`timed out: ${expr}`);
}

async function rightClickWord(page, word) {
  await page.evaluate(`(() => { const pm = document.querySelector('.ProseMirror');
    const walk = document.createTreeWalker(pm, NodeFilter.SHOW_TEXT); let node, idx = -1;
    while ((node = walk.nextNode())) { idx = node.textContent.indexOf(${JSON.stringify(word)}); if (idx >= 0) break; }
    const range = document.createRange(); range.setStart(node, idx); range.setEnd(node, idx + ${word.length});
    const r = range.getBoundingClientRect();
    pm.dispatchEvent(new MouseEvent('contextmenu', { bubbles: true, cancelable: true, view: window, clientX: r.left + r.width / 2, clientY: r.top + r.height / 2 }));
    return 'ok'; })()`);
}

/** WebP straight from WebView2, at the 2x viewport app.mjs sets (lossy, quality 85).
 *  A second CDP session: app.mjs's own capture only does PNG. */
// 1.5x rendered natively (2208x1242): as sharp as 2x for the site, a quarter smaller.
const SCALE = Number(process.env.SHOTS_SCALE || 1.5);
async function webp(port = Number(process.env.CORYLUS_VIDEO_CDP_PORT || 9222)) {
  const targets = await (await fetch(`http://127.0.0.1:${port}/json`)).json();
  const t = targets.find((x) => x.type === 'page' && /localhost:1420|tauri\.localhost/.test(x.url));
  const ws = new WebSocket(t.webSocketDebuggerUrl);
  await new Promise((ok, fail) => { ws.onopen = ok; ws.onerror = fail; });
  let n = 0;
  const send = (method, params) => new Promise((ok) => {
    const id = ++n;
    ws.onmessage = (e) => { const m = JSON.parse(e.data); if (m.id === id) ok(m); };
    ws.send(JSON.stringify({ id, method, params }));
  });
  // The metrics override is per CDP session, so this one needs its own.
  await send('Emulation.setDeviceMetricsOverride', { width: 1472, height: 828, deviceScaleFactor: SCALE, mobile: false });
  await sleep(400);
  const r = await send('Page.captureScreenshot', { format: 'webp', quality: 85 });
  ws.close();
  if (!r.result) throw new Error(`WebP capture failed: ${JSON.stringify(r.error)}`);
  return Buffer.from(r.result.data, 'base64');
}

// ── Main ─────────────────────────────────────────────────────────────────────

const args = ARGS.filter((a, i) => a !== '--lang' && ARGS[i - 1] !== '--lang');
const { page, close } = await connect();
try {
  if (args.includes('--seed')) await (ES ? seedEs(page) : seed(page));
  else if (args[0] === '--eval') console.log(await page.evaluate(fs.readFileSync(args[1], 'utf8')));
  else if (args[0] === '--run') console.log(JSON.stringify(await run(page, fs.readFileSync(args[1], 'utf8')), null, 1));
  else {
    fs.mkdirSync(OUT, { recursive: true });
    const ids = args.length ? args : Object.keys(SHOTS);
    let current = null;
    for (const id of ids) {
      if (!SHOTS[id]) { console.log(`unknown id ${id}`); continue; }
      // The English "spanish" shot already shows the Spanish interface and book.
      if (ES && id === 'spanish') { console.log('skip spanish (the English set covers it)'); continue; }
      const want = id === 'spanish' ? LIBRO : BOOK;
      if (current !== want) { await openProject(page, want); current = want; }
      try {
        await SHOTS[id](page);
        await grayscaleText(page, true);
        await sleep(700);
        fs.writeFileSync(path.join(OUT, `${id}.webp`), await webp());
        await grayscaleText(page, false);
        console.log(`ok   ${id}`);
      } catch (e) {
        console.log(`FAIL ${id}: ${e.message}`);
      } finally {
        if (AFTER[id]) await AFTER[id](page);
      }
    }
    await reset(page, { locale: 'en' });
    await page.evaluate(`(() => { const s = ${STORE('settings')}; s.grammarEnabled = true; s.commentAuthor = 'You'; return 'ok'; })()`);
  }
} finally {
  close();
}
