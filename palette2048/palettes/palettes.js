/* Palette pages — copy buttons + GA events. */
(function () {
  "use strict";
  function track(n, p) { try { if (typeof window.gtag === "function") window.gtag("event", n, p || {}); } catch (e) { /* ignore */ } }
  function copy(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) return navigator.clipboard.writeText(text);
    return new Promise(function (ok, fail) {
      var ta = document.createElement("textarea");
      ta.value = text; ta.style.position = "fixed"; ta.style.opacity = "0";
      document.body.appendChild(ta); ta.select();
      var done = false;
      try { done = document.execCommand("copy"); } catch (e) { done = false; }
      ta.remove();
      if (done) { ok(); } else { fail(); }
    });
  }
  document.addEventListener("click", function (e) {
    var b = e.target.closest && e.target.closest("button[data-copy]");
    if (b) {
      var label = b.textContent;
      copy(b.getAttribute("data-copy")).then(function () {
        b.classList.add("done"); b.textContent = "Copied ✓";
        setTimeout(function () { b.classList.remove("done"); b.textContent = label; }, 1200);
        track("palette_copy", { value: b.getAttribute("data-copy").slice(0, 40) });
      }, function () { window.prompt("", b.getAttribute("data-copy")); });
      return;
    }
    var a = e.target.closest && e.target.closest("[data-cta]");
    if (a) track("app_cta_click", { placement: a.getAttribute("data-cta") });
  });
})();
