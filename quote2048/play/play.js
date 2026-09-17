/* Quote 2048 daily (web) — UI controller. One 4×4 game per local day, theme from the fixed web
   schedule. Engine/colors/font fitting live in core.js (QuoteCore). No undo on web (an app feature). */
(function () {
  "use strict";
  var C = window.QuoteCore;
  var $ = function (id) { return document.getElementById(id); };
  var S;
  try { S = JSON.parse($("i18n").textContent); } catch (e) { S = {}; }
  var LANG = document.documentElement.lang || "en";
  var LOC = S.loc || "en";
  var STORE_KEY = "quote.web.v1";
  var DATA = "/quote2048/play/d/";
  var reduceMotion = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var SLIDE_MS = reduceMotion ? 0 : 90;
  var CJK_QUOTES = LOC === "ja" || LOC === "zh-hant";

  var stage = $("stage"), board = $("board"), tilesEl = $("tiles");
  var game = null;          // {day, id, num, preview, tiles, score, won, state, started}
  var qt = null, theme = null, pick = null;
  var busy = false, endTimer = 0, tickTimer = 0;
  var els = {};             // tile id → element
  var shareFile = null, shareBlob = null;

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
  function quoteFor(value) { return qt.q[C.quoteIndex(value, qt.q.length)]; }
  function wrapQuote(s) { return CJK_QUOTES ? "「" + s + "」" : "“" + s + "”"; }
  function levelOf(v) { return Math.round(Math.log2(v || 1)); }
  function puzzleLabel() { return game.preview ? S.preview : "#" + game.num; }

  /* ── data ── */
  // S.sched's day entries hold an opaque per-locale filename (build.py hashes locale+theme id), not
  // the theme id itself — pick.theme is that filename token; the real theme id only appears once the
  // fetched body is decrypted below. The body itself is XOR+base64 obfuscated (see core.js#deobf).
  function resolveToday(dayKey) {
    pick = C.scheduleFor(S.sched, dayKey);
    return fetch(DATA + pick.theme, { credentials: "same-origin" }).then(function (r) {
      if (!r.ok) throw new Error(pick.theme + " " + r.status);
      return r.text();
    }).then(function (body) {
      return JSON.parse(C.deobf(body.trim()));
    });
  }

  /* ── tile font fitting (TileFontSizing port + DOM check) ── */
  var FONT = (getComputedStyle(document.documentElement).getPropertyValue("--rounded") || "sans-serif").trim();
  var mctx = document.createElement("canvas").getContext("2d");
  function measure(text, size) { mctx.font = "600 " + size + "px " + FONT; return mctx.measureText(text).width; }
  var fitCache = {}, cellPx = 0;
  var fitter = document.createElement("div");
  fitter.className = "qfit";
  fitter.setAttribute("aria-hidden", "true");
  document.body.appendChild(fitter);
  function currentCell() {
    var c = board.querySelector(".cells i");
    return c ? c.getBoundingClientRect().width : 0;
  }
  function fitSize(text) {
    var key = text + "#" + cellPx;
    if (fitCache[key]) return fitCache[key];
    var size = C.fitFont(text, cellPx, measure, { lineHeight: 1.2 });
    // Safety net like the app's minimumScaleFactor: browsers break CJK lines with kinsoku rules the
    // greedy estimate can't see, so confirm in real layout and shrink until nothing overflows.
    var cw = cellPx * 0.84, ch = cellPx * 0.96;
    fitter.style.width = cw + "px";
    fitter.textContent = text;
    for (var i = 0; i < 40 && size > 6; i++) {
      fitter.style.fontSize = size + "px";
      if (fitter.scrollHeight <= ch + 0.5 && fitter.scrollWidth <= cw + 0.5) break;
      size = Math.max(6, size - 0.5);
    }
    fitCache[key] = size;
    return size;
  }

  /* ── rendering ── */
  function renderHead() {
    var p = game.day.split("-");
    var dateStr;
    try { dateStr = new Date(+p[0], +p[1] - 1, +p[2]).toLocaleDateString(LANG, { month: "short", day: "numeric" }); }
    catch (e) { dateStr = game.day; }
    $("dayLabel").textContent = puzzleLabel() + " · " + dateStr;
    $("kicker").textContent = game.state === "done" ? S.result : (qt.kind === "author" ? S.todayAuthor : S.today);
    $("tname").textContent = qt.name;
    $("tmeta").textContent = qt.kind === "topic" ? S.kindTopic : (qt.pro ? S.kindPro : S.kindAuthor);
    renderSide();
  }

  /* ── desktop side panel (≥1024px; display:none below) ── */
  function renderSide() {
    $("sKicker").textContent = qt.kind === "author" ? S.todayAuthor : S.today;
    $("sName").textContent = qt.name;
    $("sMeta").textContent = $("tmeta").textContent;
    var ramp = $("sRamp");
    if (!ramp.childNodes.length) {
      for (var v = 2; v <= 2048; v *= 2) {
        var i = document.createElement("i");
        i.style.background = theme.tileHex(v);
        ramp.appendChild(i);
      }
    }
  }

  /* ── desktop "scan to install" QR: never on iOS (it would point the phone at itself) ── */
  var IOS = /iP(hone|od|ad)/.test(navigator.userAgent) ||
    (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1);
  if (!IOS) document.documentElement.classList.add("qr-ok");
  // started from boot, once the play/result layout is final (no stray "side" view on a revisit)
  function watchQR() {
    if (IOS || !("IntersectionObserver" in window)) return;
    var qrSeen = {};
    var qrIO = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        var pl = en.target.getAttribute("data-qr-placement");
        if (!en.isIntersecting || qrSeen[pl]) return;
        qrSeen[pl] = true;
        qrIO.unobserve(en.target);
        track("app_qr_view", { placement: pl });
      });
    }, { threshold: 0.6 });
    Array.prototype.forEach.call(document.querySelectorAll(".qr[data-qr-placement]"), function (el) { qrIO.observe(el); });
  }

  function paintTile(el, value) {
    var hex = theme.tileHex(value);
    el.style.setProperty("--t1", hex);
    el.style.setProperty("--t2", rgba(hex, 0.88));
    el.classList.toggle("ink", theme.darkText(value));
    el.dataset.v = value;
    var q = quoteFor(value), b = el.querySelector("b");
    b.textContent = q[0];
    if (cellPx && !stage.classList.contains("done")) b.style.fontSize = fitSize(q[0]) + "px";
  }
  function placeTile(el, t) {
    el.style.setProperty("--r", t.row);
    el.style.setProperty("--c", t.col);
  }
  function makeTile(t, isNew) {
    var el = document.createElement("div");
    el.className = "tile" + (isNew && !reduceMotion ? " new" : "");
    el.appendChild(document.createElement("i"));
    el.appendChild(document.createElement("b"));
    placeTile(el, t);
    paintTile(el, t.value);
    tilesEl.appendChild(el);
    els[t.id] = el;
    return el;
  }
  function renderAll() {
    cellPx = currentCell();
    tilesEl.textContent = "";
    els = {};
    game.tiles.forEach(function (t) { makeTile(t, false); });
    renderScore();
  }
  function refit() {
    var c = currentCell();
    if (!game || !c || Math.abs(c - cellPx) < 0.5) return;
    cellPx = c;
    game.tiles.forEach(function (t) { var el = els[t.id]; if (el) paintTile(el, t.value); });
  }
  window.addEventListener("resize", function () { clearTimeout(refit.t); refit.t = setTimeout(refit, 120); });

  function renderScore() {
    $("score").textContent = fmtNum(game.score);
    var m = C.maxValue(game.tiles);
    var sw = $("bestSwatch");
    if (m) { sw.style.background = theme.tileHex(m); sw.title = String(m); }
  }

  /* ── quote sheet (tap a tile) ── */
  var sheetOpen = false, lastFocus = null, sheetStamp = 0;
  function openSheet(value) {
    var q = quoteFor(value);
    $("sheetLevel").textContent = S.tile + " " + value + (value >= 2048 && levelOf(value) === 11 ? " · 👑 " + S.crown : "");
    $("sheetText").textContent = wrapQuote(q[0]);
    $("sheetBy").textContent = "— " + q[1];
    lastFocus = document.activeElement;
    $("sheet").hidden = false;
    sheetOpen = true;
    sheetStamp = performance.now();
    $("sheetClose").focus({ preventScroll: true });
    track("quote_tile_open", { level: levelOf(value) });
  }
  function closeSheet() {
    if (!sheetOpen) return;
    $("sheet").hidden = true;
    sheetOpen = false;
    if (lastFocus && lastFocus.focus) lastFocus.focus({ preventScroll: true });
  }
  $("sheetClose").addEventListener("click", closeSheet);
  // The compatibility click that follows the opening tap lands on the fresh backdrop — ignore it.
  $("sheet").addEventListener("click", function (e) {
    if (e.target === $("sheet") && performance.now() - sheetStamp > 400) closeSheet();
  });
  function tileAt(x, y) {
    var r = tilesEl.getBoundingClientRect();
    var gap = parseFloat(getComputedStyle(board).paddingLeft) || 0;
    var step = cellPx + gap;
    var col = Math.floor((x - r.left) / step), row = Math.floor((y - r.top) / step);
    if (col < 0 || row < 0 || col > 3 || row > 3) return null;
    if (x - r.left - col * step > cellPx || y - r.top - row * step > cellPx) return null; // in a gap
    for (var i = 0; i < game.tiles.length; i++) if (game.tiles[i].row === row && game.tiles[i].col === col) return game.tiles[i];
    return null;
  }

  /* ── game flow ── */
  function newGame(day, id) {
    game = { day: day, id: id, num: pick.num, preview: pick.preview, tiles: [], score: 0, won: false, state: "playing", started: false };
    C.spawn(game.tiles);
    C.spawn(game.tiles);
    persist();
  }

  function doMove(dir) {
    if (!game || game.state !== "playing" || busy) return;
    closeSheet();
    var res = C.move(game.tiles, dir);
    if (!res) return; // nothing moved → no spawn (same as app)
    if (!game.started) { game.started = true; track("play_start", { puzzle: game.num, theme: qt.id }); }
    busy = true;
    game.score += res.gained;
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
        track("theme_complete", { theme: qt.id });
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
    clearTimeout(endTimer);
    endTimer = setTimeout(function () {
      if (game.state === "playing" && !C.canMove(game.tiles)) finish("over");
    }, reduceMotion ? 300 : 900);
  }

  function showWin() {
    $("winText").textContent = "👑 " + S.won;
    $("winQuote").textContent = wrapQuote(quoteFor(2048)[0]) + " — " + quoteFor(2048)[1];
    $("finishBtn").textContent = S.finish;
    $("keepBtn").textContent = S.keep;
    $("winOverlay").hidden = false;
    $("finishBtn").focus({ preventScroll: true });
  }
  function hideWin() { $("winOverlay").hidden = true; }

  function finish(reason) {
    hideWin();
    closeSheet();
    game.state = "done";
    persist();
    track("game_over", { score: game.score, max_level: levelOf(C.maxValue(game.tiles)), reason: reason,
      puzzle: game.num, theme: qt.id });
    showResult(false);
  }

  function showResult(revisit) {
    stage.classList.add("done");
    board.classList.add("ended");
    renderHead();
    $("rScore").textContent = fmtNum(game.score);
    var m = C.maxValue(game.tiles) || 2;
    $("rBest").style.background = theme.tileHex(m);
    $("hint").textContent = S.done;
    $("result").hidden = false;
    $("resultSide").hidden = false;

    var best = quoteFor(m), lv = levelOf(m);
    $("bestKicker").textContent = S.bestQuote + " · " + m + (lv >= 11 ? " 👑" : "");
    $("bestText").textContent = wrapQuote(best[0]);
    $("bestBy").textContent = "— " + best[1];
    var card = $("bestCard");
    card.style.setProperty("--t1", theme.tileHex(m));
    card.classList.toggle("ink", theme.darkText(m));

    var shown = Math.max(11, Math.min(qt.q.length, lv));
    var ol = $("ladder");
    ol.textContent = "";
    for (var i = 0; i < shown; i++) {
      var v = Math.pow(2, i + 1), got = i + 1 <= lv;
      var li = document.createElement("li");
      li.className = (got ? "got" : "no") + (i === 10 ? " crown" : "");
      var sw = document.createElement("i");
      sw.style.background = got ? theme.tileHex(v) : "";
      var num = document.createElement("span");
      num.className = "n";
      num.textContent = v;
      var tx = document.createElement("span");
      tx.className = "t";
      tx.textContent = got ? qt.q[i][0] + " — " + qt.q[i][1] : S.locked;
      li.appendChild(sw); li.appendChild(num); li.appendChild(tx);
      ol.appendChild(li);
    }
    $("ladderTitle").textContent = S.collected + " " + Math.min(lv, qt.q.length) + "/" + qt.q.length;
    $("ladderMore").textContent = S.moreInApp.replace("{n}", qt.q.length - shown);
    var link = $("themeLink");
    link.href = "/quote2048/quotes/" + qt.id + "/" + (S.sub || "");
    link.textContent = S.themePage;
    if (qt.pro) { $("appLine").textContent = S.appLinePro; $("rApp").classList.add("pro"); }

    startCountdown();
    buildShareImage();
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
  var SITE_LINK = "kkirukstudio.com/quote2048/play/" + (S.sub || "");
  function shareText() {
    var g = C.toGrid(game.tiles);
    var lines = g.map(function (r) {
      return r.map(function (v) { return v ? C.nearestEmoji(theme.tileLab(v)) : "▫️"; }).join("");
    });
    var best = quoteFor(C.maxValue(game.tiles) || 2);
    return "Quote 2048 " + (game.preview ? "" : "#" + game.num + " ") + qt.name + "\n" + lines.join("\n") + "\n" +
      wrapQuote(best[0]) + " — " + best[1] + "\n" + SITE_LINK;
  }

  var SERIF = LOC === "ko" ? 'Georgia,"Apple SD Gothic Neo","Noto Sans KR","Malgun Gothic",sans-serif' : 'Georgia,"Times New Roman","Noto Serif KR","AppleMyungjo","Hiragino Mincho ProN","Songti SC","Songti TC",serif';
  var SANS = '-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue","Apple SD Gothic Neo","Hiragino Sans","PingFang SC","Noto Sans KR",Arial,sans-serif';
  function wrapLines(ctx, text, maxW) {
    // words by spaces (Korean/Latin keep words whole); Chinese/Japanese break between characters
    var units = [];
    text.split(" ").forEach(function (w, wi) {
      if (/[぀-ヿ㐀-䶿一-鿿豈-﫿]/.test(w)) {
        Array.from(w).forEach(function (ch, ci) { units.push({ s: ch, sp: ci === 0 && wi > 0 }); });
      } else units.push({ s: w, sp: wi > 0 });
    });
    var lines = [], cur = "";
    units.forEach(function (u) {
      var cand = cur ? cur + (u.sp ? " " : "") + u.s : u.s;
      if (cur && ctx.measureText(cand).width > maxW) {
        if (/^[、。，．,.!?！？」』）)]$/.test(u.s)) { cur = cand; return; } // keep closing punctuation on the line
        lines.push(cur);
        cur = u.s;
      } else cur = cand;
    });
    if (cur) lines.push(cur);
    return lines;
  }
  function roundRect(ctx, x, y, w, h, r) {
    ctx.beginPath();
    ctx.moveTo(x + r, y); ctx.arcTo(x + w, y, x + w, y + h, r); ctx.arcTo(x + w, y + h, x, y + h, r);
    ctx.arcTo(x, y + h, x, y, r); ctx.arcTo(x, y, x + w, y, r); ctx.closePath();
  }
  function drawCard() {
    var W = 1080, H = 1350, cv = document.createElement("canvas");
    cv.width = W; cv.height = H;
    var ctx = cv.getContext("2d");
    var m = C.maxValue(game.tiles) || 2, best = quoteFor(m), accent = theme.tileHex(m);
    ctx.fillStyle = theme.bg; ctx.fillRect(0, 0, W, H);
    var grd = ctx.createRadialGradient(W / 2, 420, 60, W / 2, 420, 760);
    grd.addColorStop(0, rgba(accent, 0.22)); grd.addColorStop(1, rgba(accent, 0));
    ctx.fillStyle = grd; ctx.fillRect(0, 0, W, H);
    var ink = "#ECE8E0";
    ctx.textAlign = "center"; ctx.textBaseline = "alphabetic";
    ctx.fillStyle = rgba(ink, 0.7);
    ctx.font = "600 26px " + SANS;
    ctx.fillText(("QUOTE 2048  ·  " + (game.preview ? S.preview : "#" + game.num)).split("").join(String.fromCharCode(8202)), W / 2, 104);
    ctx.fillStyle = ink;
    ctx.font = "700 46px " + SANS;
    ctx.fillText(qt.name, W / 2, 170, W - 160);
    // tile level pill
    var pill = m + (levelOf(m) >= 11 ? "  👑" : "");
    ctx.font = "700 28px " + SANS;
    var pw = ctx.measureText(pill).width + 44;
    ctx.fillStyle = accent; roundRect(ctx, (W - pw) / 2, 204, pw, 50, 25); ctx.fill();
    ctx.fillStyle = theme.darkText(m) ? "rgba(0,0,0,.82)" : "#F4F1EA";
    ctx.fillText(pill, W / 2, 239);
    // the quote, auto-sized
    var qtext = wrapQuote(best[0]), size = 72, lines;
    for (; size >= 34; size -= 2) {
      ctx.font = "400 " + size + "px " + SERIF;
      lines = wrapLines(ctx, qtext, 880);
      if (lines.length * size * 1.3 <= 440) break;
    }
    var lh = size * 1.3, block = lines.length * lh + 70, top = 300 + (500 - block) / 2;
    ctx.fillStyle = ink;
    lines.forEach(function (l, i) { ctx.fillText(l, W / 2, top + (i + 0.8) * lh); });
    ctx.font = (LOC === "en" ? "italic " : "") + "400 36px " + SERIF;
    ctx.fillStyle = rgba(ink, 0.82);
    ctx.fillText("— " + best[1], W / 2, top + lines.length * lh + 60, W - 160);
    // board colors
    var bs = 300, gap = 10, cs = (bs - 5 * gap) / 4, bx = (W - bs) / 2, by = 870;
    ctx.fillStyle = theme.panel; roundRect(ctx, bx, by, bs, bs, 20); ctx.fill();
    var g = C.toGrid(game.tiles);
    for (var r = 0; r < 4; r++) for (var c = 0; c < 4; c++) {
      ctx.fillStyle = g[r][c] ? theme.tileHex(g[r][c]) : theme.empty;
      roundRect(ctx, bx + gap + c * (cs + gap), by + gap + r * (cs + gap), cs, cs, 10); ctx.fill();
    }
    ctx.fillStyle = ink;
    ctx.font = "600 32px " + SANS;
    ctx.fillText(S.cardScore + " " + fmtNum(game.score), W / 2, 1236);
    ctx.fillStyle = rgba(ink, 0.6);
    ctx.font = "500 26px " + SANS;
    ctx.fillText("kkirukstudio.com/quote2048/play/", W / 2, 1296);
    return cv;
  }
  function buildShareImage() {
    shareFile = null; shareBlob = null;
    try {
      var cv = drawCard();
      cv.toBlob(function (blob) {
        if (!blob) return;
        shareBlob = blob;
        try { shareFile = new File([blob], "quote2048-" + game.day + ".png", { type: "image/png" }); } catch (e) { shareFile = null; }
        var canFiles = false;
        try { canFiles = !!(shareFile && navigator.canShare && navigator.canShare({ files: [shareFile] })); } catch (e) { canFiles = false; }
        $("saveBtn").hidden = canFiles && isCoarse();
        api.imageReady = true;
      }, "image/png");
    } catch (e) { if (window.console) console.warn(e); }
  }
  function isCoarse() { return !!(window.matchMedia && matchMedia("(pointer: coarse)").matches); }
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
    if (navigator.share && isCoarse()) {
      var canFiles = false;
      try { canFiles = !!(shareFile && navigator.canShare && navigator.canShare({ files: [shareFile] })); } catch (e) { canFiles = false; }
      var data = canFiles ? { files: [shareFile], text: text } : { text: text };
      navigator.share(data).then(function () { track("share", { method: canFiles ? "image" : "text" }); })
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
  function onSave() {
    if (!shareBlob) return;
    var url = URL.createObjectURL(shareBlob), a = document.createElement("a");
    a.href = url; a.download = "quote2048-" + game.day + ".png";
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(function () { URL.revokeObjectURL(url); }, 4000);
    track("share", { method: "download" });
  }

  /* ── input ── */
  var KEYS = { ArrowLeft: "left", ArrowRight: "right", ArrowUp: "up", ArrowDown: "down",
    a: "left", d: "right", w: "up", s: "down", A: "left", D: "right", W: "up", S: "down" };
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && sheetOpen) { closeSheet(); return; }
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
    start = { x: e.clientX, y: e.clientY, id: e.pointerId, t: Date.now() };
  });
  function endSwipe(e) {
    if (!start || e.pointerId !== start.id) return;
    var dx = e.clientX - start.x, dy = e.clientY - start.y, dt = Date.now() - start.t;
    var sx = start.x, sy = start.y;
    start = null;
    var ax = Math.abs(dx), ay = Math.abs(dy);
    if (Math.max(ax, ay) < 24) {
      // a tap (not a swipe) on a tile opens its full quote
      if (Math.max(ax, ay) < 10 && dt < 600 && game && game.state === "playing" && !busy) {
        var t = tileAt(sx, sy);
        if (t) openSheet(t.value);
      }
      return;
    }
    doMove(ax > ay ? (dx > 0 ? "right" : "left") : (dy > 0 ? "down" : "up"));
  }
  window.addEventListener("pointerup", endSwipe);
  window.addEventListener("pointercancel", function () { start = null; });
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
  $("saveBtn").addEventListener("click", onSave);
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("[data-cta]");
    if (a) track("app_cta_click", { placement: a.getAttribute("data-cta") });
    var x = e.target.closest && e.target.closest("[data-xpromo]");
    if (x) track("cross_promo_click", { placement: x.getAttribute("data-xpromo"), target: x.getAttribute("data-xtarget") });
  });

  var api = window.QuotePlay = { shareText: function () { return shareText(); }, imageReady: false,
    cardDataURL: function () { return drawCard().toDataURL("image/png"); } };

  /* ── boot ── */
  var today = C.dayKey(new Date());
  resolveToday(today).then(function (data) {
    qt = data;
    theme = C.makeTheme(pick.board);
    var saved = load();
    if (saved && saved.day === today && saved.id === qt.id && saved.tiles && saved.tiles.length) {
      game = { day: today, id: qt.id, num: pick.num, preview: pick.preview, score: saved.score || 0, won: !!saved.won,
        state: saved.state || "playing", started: !!saved.started,
        tiles: C.fromGrid(C.toGrid(saved.tiles.map(function (a) { return { value: a[0], row: a[1], col: a[2] }; }))) };
    } else {
      newGame(today, qt.id);
    }
    renderHead();
    if (game.state === "done") stage.classList.add("done");
    renderAll();
    if (game.state === "done") showResult(true);
    else if (game.state === "won") showWin();
    else checkEnd();
    watchQR();
  }).catch(function (err) {
    $("tname").textContent = S.loadErr || "Error";
    if (window.console) console.warn(err);
  });
})();
