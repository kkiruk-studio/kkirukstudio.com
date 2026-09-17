/* Quote 2048 quote pages — copy buttons + App Store CTA tracking. */
(function () {
  "use strict";
  var S = {};
  try { S = JSON.parse(document.getElementById("qi18n").textContent); } catch (e) { S = {}; }
  function track(name, params) {
    try { if (typeof window.gtag === "function") window.gtag("event", name, params || {}); } catch (e) { /* ignore */ }
  }
  function legacyCopy(text) {
    var ta = document.createElement("textarea");
    ta.value = text; ta.setAttribute("readonly", ""); ta.style.position = "fixed"; ta.style.opacity = "0";
    document.body.appendChild(ta); ta.select();
    var ok = false;
    try { ok = document.execCommand("copy"); } catch (e) { ok = false; }
    ta.remove();
    return ok;
  }
  document.addEventListener("click", function (e) {
    var cta = e.target.closest && e.target.closest("[data-cta]");
    if (cta) track("app_cta_click", { placement: cta.getAttribute("data-cta") });
    var x = e.target.closest && e.target.closest("[data-xpromo]");
    if (x) track("cross_promo_click", { placement: x.getAttribute("data-xpromo"), target: x.getAttribute("data-xtarget") });
    var b = e.target.closest && e.target.closest("button.copy");
    if (!b) return;
    var text = b.getAttribute("data-copy"), label = b.textContent;
    function done() {
      b.textContent = S.copied || "Copied"; b.classList.add("done");
      setTimeout(function () { b.textContent = label; b.classList.remove("done"); }, 1400);
      track("quote_copy", { id: (location.pathname.split("/")[3] || "") });
    }
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(done, function () { if (legacyCopy(text)) done(); });
    else if (legacyCopy(text)) done();
  });
})();
