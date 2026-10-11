/* Local Link place pages — copy, full-screen "show to driver", and app-first map links with web fallback. */
(function () {
  document.querySelectorAll("[data-copy]").forEach(function (b) {
    b.addEventListener("click", function () {
      var text = b.getAttribute("data-copy"), label = b.textContent;
      function done() { b.textContent = b.getAttribute("data-done"); setTimeout(function () { b.textContent = label; }, 1600); }
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done, fallback);
      } else { fallback(); }
      function fallback() {
        var ta = document.createElement("textarea");
        ta.value = text; ta.setAttribute("readonly", ""); ta.style.position = "fixed"; ta.style.opacity = "0";
        document.body.appendChild(ta); ta.select();
        try { document.execCommand("copy"); done(); } catch (e) {}
        document.body.removeChild(ta);
      }
    });
  });

  var show = document.getElementById("showcase");
  var opener = document.querySelector("[data-show]");
  if (show && opener) {
    opener.addEventListener("click", function () {
      show.hidden = false;
      var el = show;
      if (el.requestFullscreen) { el.requestFullscreen().catch(function () {}); }
      else if (el.webkitRequestFullscreen) { try { el.webkitRequestFullscreen(); } catch (e) {} }
    });
    function close() {
      show.hidden = true;
      if (document.fullscreenElement && document.exitFullscreen) { document.exitFullscreen().catch(function () {}); }
      opener.focus();
    }
    show.addEventListener("click", close);
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !show.hidden) close(); });
    document.addEventListener("fullscreenchange", function () { if (!document.fullscreenElement && !show.hidden) { show.hidden = true; } });
  }

  // Try the map app's URL scheme first; if the page is still visible shortly after, open the web map.
  document.querySelectorAll("a.mapbtn[data-app]").forEach(function (a) {
    a.addEventListener("click", function (e) {
      if (!/iPhone|iPad|iPod|Android/i.test(navigator.userAgent) && !(navigator.maxTouchPoints > 1 && /Mac/.test(navigator.platform))) return;
      e.preventDefault();
      var web = a.href, left = false;
      function hide() { left = true; }
      document.addEventListener("visibilitychange", hide, { once: true });
      window.addEventListener("pagehide", hide, { once: true });
      window.location.href = a.getAttribute("data-app");
      setTimeout(function () { if (!left && !document.hidden) window.location.href = web; }, 1400);
    });
  });
})();
