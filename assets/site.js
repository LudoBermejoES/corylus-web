/* Keep the download buttons pointing at whatever is actually published.
 *
 * The per-platform manifests in corylus-releases carry the live version; the
 * installer filenames follow from it. The HTML ships a working fallback link,
 * so the page is correct with JavaScript disabled and merely becomes current
 * with it enabled. */
(function () {
  "use strict";
  var RAW = "https://raw.githubusercontent.com/LudoBermejoES/corylus-releases/main";
  var TARGETS = [
    { id: "dl-mac", manifest: "latest-darwin-aarch64.json", file: function (v) { return "Corylus_" + v + "_aarch64.dmg"; } },
    { id: "dl-win", manifest: "latest-windows-x86_64.json", file: function (v) { return "Corylus_" + v + "_x64-setup.exe"; } }
  ];

  TARGETS.forEach(function (t) {
    var el = document.getElementById(t.id);
    if (!el) return;
    fetch(RAW + "/" + t.manifest, { cache: "no-cache" })
      .then(function (r) { return r.ok ? r.json() : Promise.reject(r.status); })
      .then(function (m) {
        if (!m || typeof m.version !== "string" || !/^\d+\.\d+\.\d+$/.test(m.version)) return;
        el.href = RAW + "/" + t.file(m.version);
        var ver = el.querySelector(".ver");
        if (ver) ver.textContent = ver.getAttribute("data-ver-label") + " " + m.version;
      })
      .catch(function () { /* the fallback link in the HTML stands */ });
  });
})();

/* Lightbox: a screenshot opens large over the page. Each one is already a link
 * to the full image, so without JavaScript (or with a modifier key) the browser
 * just opens it; <dialog> gives Escape, focus handling and a backdrop for free. */
(function () {
  "use strict";
  if (typeof HTMLDialogElement !== "function") return;
  var es = document.documentElement.lang === "es";
  var dlg = document.createElement("dialog");
  dlg.className = "lightbox";
  dlg.innerHTML =
    '<button type="button" class="lightbox-close" aria-label="' + (es ? "Cerrar" : "Close") + '">✕</button>' +
    '<figure><img alt=""><figcaption></figcaption></figure>';
  document.body.appendChild(dlg);
  var img = dlg.querySelector("img"), cap = dlg.querySelector("figcaption");

  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("a.zoom");
    if (!a || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    e.preventDefault();
    var thumb = a.querySelector("img");
    img.src = a.getAttribute("href");
    img.alt = thumb ? thumb.alt : "";
    cap.textContent = img.alt;
    dlg.showModal();
  });
  // Any click closes it: on the image, the backdrop or the button.
  dlg.addEventListener("click", function () { dlg.close(); });
  dlg.addEventListener("close", function () { img.removeAttribute("src"); });
})();
