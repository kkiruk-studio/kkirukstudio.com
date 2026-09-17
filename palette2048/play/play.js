/* Palette daily (web) — UI controller. One 4×4 game per local day.
   Engine/colors live in core.js (PaletteCore). No undo on web (kept as an app feature). */
(function () {
  "use strict";
  var C = window.PaletteCore;
  var $ = function (id) { return document.getElementById(id); };
  var S;
  try { S = JSON.parse($("i18n").textContent); } catch (e) { S = {}; }
  var LANG = document.documentElement.lang || "en";
  var STORE_KEY = "palette.web.v1";
  var DATA = "/palette2048/play/";
  var reduceMotion = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var SLIDE_MS = reduceMotion ? 0 : 90;

  var stage = $("stage"), board = $("board"), tilesEl = $("tiles");
  var game = null;          // {day, id, num, tiles, score, won, state, started}
  var painting = null, theme = null;
  var busy = false, endTimer = 0, tickTimer = 0;
  var els = {};             // tile id → element

  /* ── utils ── */
  function track(name, params) {
    try { if (typeof window.gtag === "function") window.gtag("event", name, params || {}); } catch (e) { /* ignore */ }
  }
  function load() {
    try { return JSON.parse(localStorage.getItem(STORE_KEY) || "null"); } catch (e) { return null; }
  }
  function persist() {
    if (!game) return;
    var rec = { day: game.day, id: game.id, score: game.score, won: game.won, state: game.state,
      started: game.started, tiles: game.tiles.map(function (t) { return [t.value, t.row, t.col]; }) };
    try { localStorage.setItem(STORE_KEY, JSON.stringify(rec)); } catch (e) { /* private mode etc. */ }
  }
  function fmtNum(n) { try { return n.toLocaleString(LANG); } catch (e) { return String(n); } }
  function rgba(hex, a) {
    var n = parseInt(hex.slice(1), 16);
    return "rgba(" + ((n >> 16) & 255) + "," + ((n >> 8) & 255) + "," + (n & 255) + "," + a + ")";
  }
  function isSaturday(dayKey) { var p = dayKey.split("-"); return new Date(+p[0], +p[1] - 1, +p[2]).getDay() === 6; }
  function mysteryActive() { return game && isSaturday(game.day) && game.state !== "done"; }

  /* ── data (same lookup as CuratedPaletteStore.dailyPalette) ── */
  function getJSON(name) {
    return fetch(DATA + name, { credentials: "same-origin" }).then(function (r) {
      if (!r.ok) throw new Error(name + " " + r.status);
      return r.json();
    });
  }
  function resolveToday(dayKey) {
    return getJSON("daily.json").then(function (d) {
      var num = C.puzzleNumber(d.epoch, dayKey);
      if (d.days[dayKey]) return { p: C.unpack(d.days[dayKey]), num: num };
      return getJSON("all.json").then(function (a) { return { p: C.pickFromAll(a, dayKey), num: num }; });
    });
  }

  /* ── rendering ── */
  function applyTheme() {
    // Page is always black — only the tiles (paintTile) follow the painting's palette.
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute("content", "#000000");
  }

  function renderHead() {
    var p = game.day.split("-");
    var dateStr;
    try { dateStr = new Date(+p[0], +p[1] - 1, +p[2]).toLocaleDateString(LANG, { month: "short", day: "numeric" }); }
    catch (e) { dateStr = game.day; }
    $("dayLabel").textContent = "#" + game.num + " · " + dateStr;
    var pname = $("pname");
    if (mysteryActive()) {
      $("kicker").textContent = S.mystery;
      pname.textContent = "? ? ?"; // no link while hidden — the href itself would spoil the answer
      $("pmeta").textContent = S.mysteryNote;
    } else {
      $("kicker").textContent = game.state === "done" ? S.result : S.today;
      pname.textContent = "";
      var a = document.createElement("a");
      a.href = painting.url;
      a.target = "_blank";
      a.rel = "noopener";
      a.appendChild(document.createTextNode(painting.name));
      var ext = document.createElement("span");
      ext.className = "ext";
      ext.setAttribute("aria-hidden", "true");
      ext.textContent = " ↗";
      a.appendChild(ext);
      a.addEventListener("click", function () { track("painting_link_click", { target: "original", placement: "header" }); });
      pname.appendChild(a);
      $("pmeta").textContent = painting.year ? painting.artist + ", " + painting.year : painting.artist;
    }
  }

  /* ── today's painting card (result screen) ── */
  function renderPaintingCard() {
    var card = $("paintingCard"), img = $("pImg"), sw = $("pSwatches"), media = $("pMedia"),
        credit = $("pCredit"), note = $("pCopyNote");
    card.hidden = false;
    $("pCardName").textContent = painting.name;
    $("pCardMeta").textContent = painting.year ? painting.artist + ", " + painting.year : painting.artist;
    var flavor = painting.flavor && (painting.flavor[LANG] || painting.flavor.en);
    var flavorEl = $("pFlavor");
    if (flavor) { flavorEl.textContent = flavor; flavorEl.hidden = false; } else { flavorEl.hidden = true; }

    media.hidden = false;
    if (painting.imageOk) {
      sw.hidden = true; sw.textContent = "";
      note.hidden = true;
      img.alt = painting.name + ", " + painting.artist;
      // img must stay un-hidden (laid out) for loading="lazy" to ever fire its network request —
      // a display:none image never loads. The aspect-ratio box + empty-tile background double as
      // the loading placeholder, so there's nothing to see until the bytes arrive.
      img.hidden = false; credit.hidden = false;
      var viewed = false;
      img.onload = function () { if (!viewed) { viewed = true; track("painting_image_view", { id: painting.id }); } };
      img.onerror = function () { media.hidden = true; credit.hidden = true; };
      img.src = C.thumbURL(painting.url, 500);
    } else {
      img.hidden = true; credit.hidden = true;
      sw.hidden = false; sw.textContent = "";
      theme.stops.forEach(function (st) {
        var i = document.createElement("i");
        i.style.background = C.toHex(st);
        sw.appendChild(i);
      });
      note.hidden = false; note.textContent = S.pCopyNote || "";
    }

    var orig = $("pOriginal"), pal = $("pPalette");
    orig.href = painting.url;
    orig.textContent = S.pOriginal || "";
    pal.href = "/palette2048/palettes/" + painting.id + "/";
    pal.textContent = S.pPalette || "";
  }
  $("pOriginal").addEventListener("click", function () { track("painting_link_click", { target: "original", placement: "result" }); });
  $("pPalette").addEventListener("click", function () { track("painting_link_click", { target: "palette", placement: "result" }); });

  function paintTile(el, value) {
    var hex = theme.tileHex(value);
    el.style.setProperty("--t1", hex);
    el.style.setProperty("--t2", rgba(hex, 0.88));
    el.dataset.v = value;
  }
  function placeTile(el, t) {
    el.style.setProperty("--r", t.row);
    el.style.setProperty("--c", t.col);
  }
  function makeTile(t, isNew) {
    var el = document.createElement("div");
    el.className = "tile" + (isNew && !reduceMotion ? " new" : "");
    el.appendChild(document.createElement("i"));
    placeTile(el, t);
    paintTile(el, t.value);
    tilesEl.appendChild(el);
    els[t.id] = el;
    return el;
  }
  function renderAll() {
    tilesEl.textContent = "";
    els = {};
    game.tiles.forEach(function (t) { makeTile(t, false); });
    renderScore();
  }
  function renderScore() {
    $("score").textContent = fmtNum(game.score);
    var m = C.maxValue(game.tiles);
    var sw = $("bestSwatch");
    if (m) { sw.style.background = theme.tileHex(m); sw.title = String(m); }
  }

  /* ── game flow ── */
  function newGame(day, id, num) {
    game = { day: day, id: id, num: num, tiles: [], score: 0, won: false, state: "playing", started: false };
    C.spawn(game.tiles);
    C.spawn(game.tiles);
    persist();
  }

  function doMove(dir) {
    if (!game || game.state !== "playing" || busy) return;
    var res = C.move(game.tiles, dir);
    if (!res) return; // nothing moved → no spawn (same as app)
    if (!game.started) { game.started = true; track("play_start", { puzzle: game.num }); }
    busy = true;
    game.score += res.gained;
    // slide survivors + absorbed tiles to their destinations
    res.tiles.forEach(function (t) { var el = els[t.id]; if (el) placeTile(el, t); });
    res.merged.forEach(function (m) { var el = els[m.id]; if (el) { el.style.zIndex = 0; placeTile(el, m); } });
    game.tiles = res.tiles;
    var reachedGoal = !game.won && game.tiles.some(function (t) { return t.value === 2048; });

    setTimeout(function () {
      res.merged.forEach(function (m) {
        var gone = els[m.id];
        if (gone) { gone.remove(); delete els[m.id]; }
        var el = els[m.into];
        if (el) {
          var t = game.tiles.filter(function (x) { return x.id === m.into; })[0];
          paintTile(el, t.value);
          if (!reduceMotion) { el.classList.remove("pop"); void el.offsetWidth; el.classList.add("pop"); }
        }
      });
      renderScore();
      if (reachedGoal) {
        game.won = true;
        game.state = "won";
        busy = false;
        persist();
        showWin();
        return;
      }
      var nt = C.spawn(game.tiles);
      if (nt) makeTile(nt, true);
      busy = false;
      persist();
      checkEnd();
    }, SLIDE_MS);
  }

  function checkEnd() {
    if (C.canMove(game.tiles)) return;
    // linger on the final board before closing, like the app (0.9s)
    clearTimeout(endTimer);
    endTimer = setTimeout(function () {
      if (game.state === "playing" && !C.canMove(game.tiles)) finish("over");
    }, reduceMotion ? 300 : 900);
  }

  function showWin() {
    $("winText").textContent = S.won;
    $("finishBtn").textContent = S.finish;
    $("keepBtn").textContent = S.keep;
    $("winOverlay").hidden = false;
    $("finishBtn").focus({ preventScroll: true });
  }
  function hideWin() { $("winOverlay").hidden = true; }

  function finish(reason) {
    hideWin();
    game.state = "done";
    persist();
    track("game_over", { score: game.score, max_level: Math.log2(C.maxValue(game.tiles) || 1), reason: reason, puzzle: game.num });
    showResult(false);
  }

  function showResult(revisit) {
    stage.classList.add("done");
    board.classList.add("ended");
    renderHead();
    $("rScore").textContent = fmtNum(game.score);
    var m = C.maxValue(game.tiles);
    if (m) $("rBest").style.background = theme.tileHex(m);
    $("hint").textContent = S.done;
    $("result").hidden = false;
    renderPaintingCard();
    startCountdown();
    if (revisit) track("already_played_view", { puzzle: game.num });
  }

  function startCountdown() {
    clearInterval(tickTimer);
    function tick() {
      var now = new Date();
      var next = new Date(now.getFullYear(), now.getMonth(), now.getDate() + 1);
      var s = Math.max(0, Math.round((next - now) / 1000));
      if (C.dayKey(now) !== game.day) { location.reload(); return; }
      var h = Math.floor(s / 3600), mi = Math.floor(s % 3600 / 60), se = s % 60;
      $("countdown").textContent = h + ":" + (mi < 10 ? "0" : "") + mi + ":" + (se < 10 ? "0" : "") + se;
    }
    tick();
    tickTimer = setInterval(tick, 1000);
  }

  /* ── share ── */
  function shareText() {
    var g = C.toGrid(game.tiles);
    var lines = g.map(function (r) {
      return r.map(function (v) { return v ? C.nearestEmoji(theme.tileLab(v)) : "▫️"; }).join("");
    });
    return "Palette 2048 #" + game.num + " " + game.day + "\n" + lines.join("\n") + "\n" +
      (S.shareScore || "Score") + " " + game.score + "\n" + "kkirukstudio.com/palette2048/play/";
  }
  function toast(msg) { $("toast").textContent = msg; }
  function legacyCopy(text) {
    var ta = document.createElement("textarea");
    ta.value = text; ta.setAttribute("readonly", ""); ta.style.position = "fixed"; ta.style.opacity = "0";
    document.body.appendChild(ta); ta.select();
    var ok = false;
    try { ok = document.execCommand("copy"); } catch (e) { ok = false; }
    ta.remove();
    return ok;
  }
  function onShare() {
    var text = shareText();
    var coarse = window.matchMedia && matchMedia("(pointer: coarse)").matches;
    if (navigator.share && coarse) {
      navigator.share({ text: text }).then(function () { track("share", { method: "web_share" }); })
        .catch(function (e) { if (e && e.name !== "AbortError") copyFallback(text); });
      return;
    }
    copyFallback(text);
  }
  function copyFallback(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(function () { toast(S.copied); track("share", { method: "clipboard" }); },
        function () { legacy(); });
    } else legacy();
    function legacy() {
      if (legacyCopy(text)) { toast(S.copied); track("share", { method: "clipboard_legacy" }); }
      else { toast(S.shareFail); window.prompt("", text); }
    }
  }

  /* ── input ── */
  var KEYS = { ArrowLeft: "left", ArrowRight: "right", ArrowUp: "up", ArrowDown: "down",
    a: "left", d: "right", w: "up", s: "down", A: "left", D: "right", W: "up", S: "down" };
  document.addEventListener("keydown", function (e) {
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    var t = e.target;
    if (t && (t.tagName === "INPUT" || t.tagName === "TEXTAREA" || t.isContentEditable)) return;
    var dir = KEYS[e.key];
    if (!dir || !game || game.state !== "playing") return;
    e.preventDefault();
    doMove(dir);
  });

  var start = null;
  board.addEventListener("pointerdown", function (e) {
    if (e.pointerType === "mouse" && e.button !== 0) return;
    if (e.target.closest && e.target.closest(".overlay")) return;
    start = { x: e.clientX, y: e.clientY, id: e.pointerId };
  });
  function endSwipe(e) {
    if (!start || e.pointerId !== start.id) return;
    var dx = e.clientX - start.x, dy = e.clientY - start.y;
    start = null;
    var ax = Math.abs(dx), ay = Math.abs(dy);
    if (Math.max(ax, ay) < 24) return;
    doMove(ax > ay ? (dx > 0 ? "right" : "left") : (dy > 0 ? "down" : "up"));
  }
  window.addEventListener("pointerup", endSwipe);
  window.addEventListener("pointercancel", function () { start = null; });
  // iOS: stop the page from rubber-banding while swiping on the board
  board.addEventListener("touchmove", function (e) { e.preventDefault(); }, { passive: false });

  $("keepBtn").addEventListener("click", function () {
    hideWin();
    game.state = "playing";
    var nt = C.spawn(game.tiles); // continueAfterWin
    if (nt) makeTile(nt, true);
    persist();
    checkEnd();
    board.focus({ preventScroll: true });
  });
  $("finishBtn").addEventListener("click", function () { finish("won"); });
  $("shareBtn").addEventListener("click", onShare);
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("[data-cta]");
    if (a) track("app_cta_click", { placement: a.getAttribute("data-cta") });
  });

  /* ── boot ── */
  var today = C.dayKey(new Date());
  resolveToday(today).then(function (r) {
    painting = r.p;
    theme = C.makeTheme(painting);
    applyTheme();
    var saved = load();
    if (saved && saved.day === today && saved.id === painting.id && saved.tiles && saved.tiles.length) {
      game = { day: today, id: painting.id, num: r.num, score: saved.score || 0, won: !!saved.won,
        state: saved.state || "playing", started: !!saved.started,
        tiles: C.fromGrid(C.toGrid(saved.tiles.map(function (a) { return { value: a[0], row: a[1], col: a[2] }; }))) };
    } else {
      newGame(today, painting.id, r.num);
    }
    renderHead();
    renderAll();
    if (game.state === "done") showResult(true);
    else if (game.state === "won") showWin();
    else checkEnd();
  }).catch(function (err) {
    $("pname").textContent = S.loadErr || "Error";
    if (window.console) console.warn(err);
  });

})();
