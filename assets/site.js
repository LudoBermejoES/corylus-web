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
