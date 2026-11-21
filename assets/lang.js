/* Spanish-speaking browsers get the Spanish page; everyone else stays on English.
 *
 * GitHub Pages cannot read Accept-Language, so this runs in the page, loaded in
 * <head> without defer so the English page never flashes first. A language
 * picked with the site's own link wins over the browser's and is remembered, so
 * nobody is sent back to a language they just left. */
(function () {
  "use strict";
  var KEY = "corylus-lang";
  function get() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function set(v) { try { localStorage.setItem(KEY, v); } catch (e) { /* private mode */ } }

  // Remember an explicit choice: the language switch is <a class="lang" hreflang="...">.
  document.addEventListener("click", function (e) {
    var a = e.target && e.target.closest ? e.target.closest("a.lang") : null;
    if (!a) return;
    var href = a.getAttribute("href") || "";
    set(/(^|\/)es\//.test(href) ? "es" : "en");
  });

  // Only the English home page redirects; /es/ and the privacy pages never do.
  var path = location.pathname.replace(/index\.html$/, "");
  if (path !== "/" || document.documentElement.lang !== "en") return;
  var langs = navigator.languages && navigator.languages.length ? navigator.languages : [navigator.language || ""];
  var wanted = get() || (/^es\b/i.test(langs[0] || "") ? "es" : "en");
  if (wanted === "es") location.replace("es/" + location.search + location.hash);
})();
