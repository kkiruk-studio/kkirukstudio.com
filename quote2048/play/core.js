/* Quote 2048 daily (web) — pure core: 2048 engine, board color mapping, schedule, tile font fitting.
   Ported from the iOS app (Quote2048/GameViewModel.swift, ThemeManager.swift, BoardPalettes.swift,
   GameBoardView.swift · TileFontSizing). Keep the math identical to the app so web tiles match.
   No DOM access here — node tests require() this file (see test_core.js). */
(function (root) {
  "use strict";

  /* ───────────── Lab color (ThemeManager.swift · LabColor) ───────────── */
  function clamp01(v) { return Math.min(1, Math.max(0, v)); }
  function gamma(c) { return c <= 0.0031308 ? 12.92 * c : 1.055 * Math.pow(c, 1 / 2.4) - 0.055; }
  function invGamma(c) { return c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); }
  var EPS = 0.008856, KAPPA = 903.3;
  function lab(L, a, b) { return { L: L, a: a, b: b }; }

  function fromRGB(r, g, b) { // 0..1
    var rl = invGamma(r), gl = invGamma(g), bl = invGamma(b);
    var X = (0.4124564 * rl + 0.3575761 * gl + 0.1804375 * bl) / 0.95047;
    var Y = (0.2126729 * rl + 0.7151522 * gl + 0.0721750 * bl) / 1.0;
    var Z = (0.0193339 * rl + 0.1191920 * gl + 0.9503041 * bl) / 1.08883;
    var fx = X > EPS ? Math.pow(X, 1 / 3) : (KAPPA * X + 16) / 116;
    var fy = Y > EPS ? Math.pow(Y, 1 / 3) : (KAPPA * Y + 16) / 116;
    var fz = Z > EPS ? Math.pow(Z, 1 / 3) : (KAPPA * Z + 16) / 116;
    return lab(116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz));
  }
  function toRGB(c) {
    var fy = (c.L + 16) / 116, fx = c.a / 500 + fy, fz = fy - c.b / 200;
    var xr = fx * fx * fx > EPS ? fx * fx * fx : (116 * fx - 16) / KAPPA;
    var yr = c.L > KAPPA * EPS ? Math.pow((c.L + 16) / 116, 3) : c.L / KAPPA;
    var zr = fz * fz * fz > EPS ? fz * fz * fz : (116 * fz - 16) / KAPPA;
    var X = xr * 0.95047, Y = yr, Z = zr * 1.08883;
    return [
      gamma(3.2404542 * X - 1.5371385 * Y - 0.4985314 * Z),
      gamma(-0.9692660 * X + 1.8760108 * Y + 0.0415560 * Z),
      gamma(0.0556434 * X - 0.2040259 * Y + 1.0572252 * Z)
    ];
  }
  function hex2(n) { return (n < 16 ? "0" : "") + n.toString(16).toUpperCase(); }
  function toHex(c) {
    var v = toRGB(c);
    return "#" + hex2(Math.round(clamp01(v[0]) * 255)) + hex2(Math.round(clamp01(v[1]) * 255)) + hex2(Math.round(clamp01(v[2]) * 255));
  }
  function fromHex(h) {
    var n = parseInt(h.replace("#", ""), 16);
    return fromRGB(((n >> 16) & 255) / 255, ((n >> 8) & 255) / 255, (n & 255) / 255);
  }
  function lerpLab(p, q, t) { return lab(p.L + (q.L - p.L) * t, p.a + (q.a - p.a) * t, p.b + (q.b - p.b) * t); }
  function deltaE(p, q) { var d1 = p.L - q.L, d2 = p.a - q.a, d3 = p.b - q.b; return Math.sqrt(d1 * d1 + d2 * d2 + d3 * d3); }
  function chroma(c) { return Math.sqrt(c.a * c.a + c.b * c.b); }

  function hueLockedLerp(from, to, t) {
    var cFrom = chroma(from), cTo = chroma(to);
    var hFrom = Math.atan2(from.b, from.a), hTo = Math.atan2(to.b, to.a);
    if (cFrom < 3) hFrom = hTo;
    if (cTo < 3) hTo = hFrom;
    var h = t < 0.5 ? hFrom : hTo;
    var c = cFrom + (cTo - cFrom) * t;
    return lab(from.L + (to.L - from.L) * t, c * Math.cos(h), c * Math.sin(h));
  }

  // ThemeManager.tamedChroma (Quote 2048 version — L-dependent cap 50 → 44)
  function tamedChroma(c) {
    var ch = chroma(c);
    var maxC = c.L <= 55 ? 50 : Math.max(44, 50 - (c.L - 55) * 0.2);
    if (!(ch > maxC && ch > 0)) return c;
    var s = maxC / ch;
    return lab(c.L, c.a * s, c.b * s);
  }

  // ThemeManager.vividBackground
  function vividBackground(c) {
    var ch = chroma(c);
    if (!(ch > 0.05)) return c;
    var h = Math.atan2(c.b, c.a);
    var maxC = c.L <= 40 ? 34 : Math.max(18, 34 - (c.L - 40) * 0.35);
    var floorC = Math.min(maxC, 16);
    var target = Math.min(Math.max(ch, floorC) * (ch < floorC ? 1 : 1.3), maxC);
    return lab(c.L, target * Math.cos(h), target * Math.sin(h));
  }

  /* ───────────── Board palettes (BoardPalettes.swift — 6 anchors, dark → light) ───────────── */
  var BOARDS = {
    "board-dawn": ["2B2D4F", "5C4270", "96547E", "C97B6D", "E8A94F", "F2E3C4"],
    "board-forest": ["1F3327", "33553B", "557A4A", "89985A", "C3B36A", "EFE8C8"],
    "board-ocean": ["16294A", "1F4E6E", "2E7E8C", "62AFA4", "B4D4B8", "F1EFDC"],
    "board-ember": ["3D1F33", "7A2740", "B23A38", "D96B35", "EBA53F", "F5DFAE"],
    "board-lavender": ["2E2447", "55407A", "8062A6", "AB8CC4", "D0B7D8", "F1E7EC"],
    "board-desert": ["3B2A20", "6E4630", "9C6239", "BE8A4A", "D9B678", "F0E3C6"],
    "board-inkjade": ["1E2528", "3C5257", "4F7D6E", "7FA98D", "B7CDB4", "F2F1E4"],
    "board-berry": ["331B33", "6B2450", "A33564", "CD5E63", "E89A70", "F6E3C9"],
    "board-peacock": ["11333B", "145A66", "1F8480", "55AB92", "A5CFAE", "EEF0DA"],
    "board-charcoal": ["26262B", "4A4A50", "7A6A4C", "A98C43", "D0B45C", "F0E7CB"]
  };
  var BOARD_IDS = Object.keys(BOARDS);

  // 4×4 (BoardSize.four)
  var SIZE = 4, EXPOSURE = 11, MAX_LEVEL = 16;

  function makeTheme(boardId) {
    var hexes = BOARDS[boardId] || BOARDS[BOARD_IDS[0]];
    var anchors = hexes.map(function (h) { return fromHex(h); });
    // smoothPath: all six anchors sorted dark → light
    var stops = anchors.slice().sort(function (p, q) { return p.L - q.L; }).map(tamedChroma);

    // gameLevelColors(maxExposure:)
    var pal = [];
    (function () {
      var last = stops[0], anc = [last], i, k;
      for (i = 1; i < stops.length; i++) if (deltaE(last, stops[i]) >= 5) { anc.push(stops[i]); last = stops[i]; }
      var n = anc.length;
      if (n < 2) { pal = anc; return; }
      var spans = [], alloc = [];
      for (i = 0; i < n - 1; i++) {
        var dL = anc[i + 1].L - anc[i].L, dC = chroma(anc[i + 1]) - chroma(anc[i]);
        spans.push(Math.sqrt(dL * dL + dC * dC));
        alloc.push(0);
      }
      var sum = function () { return alloc.reduce(function (s, x) { return s + x; }, 0); };
      while (n + sum() < EXPOSURE) {
        var bestStep = 0, bestIdx = -1;
        for (i = 0; i < n - 1; i++) {
          var step = spans[i] / (alloc[i] + 2);
          if (step > bestStep) { bestStep = step; bestIdx = i; }
        }
        if (!(bestIdx >= 0 && bestStep >= 6.5)) break;
        alloc[bestIdx] += 1;
      }
      for (i = 0; i < n - 1; i++) {
        pal.push(anc[i]);
        for (k = 1; k <= alloc[i]; k++) pal.push(tamedChroma(hueLockedLerp(anc[i], anc[i + 1], k / (alloc[i] + 1))));
      }
      pal.push(anc[n - 1]);
    })();

    function tailLab(base, tailIndex, tailCount) {
      var cBase = chroma(base), h = Math.atan2(base.b, base.a);
      var cTarget = Math.min(44, cBase + 30);
      var gilded = tamedChroma(lab(Math.min(96, base.L + 4), cTarget * Math.cos(h), cTarget * Math.sin(h)));
      var white = tamedChroma(lab(Math.min(98, Math.max(gilded.L + 18, 92)), gilded.a * 0.55, gilded.b * 0.55));
      var len1 = deltaE(base, gilded), len2 = deltaE(gilded, white);
      var total = Math.max(len1 + len2, 0.000001);
      var u = Math.min(Math.max(tailIndex / Math.max(tailCount, 1), 0), 1);
      var ease = Math.max(1, 6 * tailCount / total);
      var arc = total * (1 - Math.pow(1 - u, ease));
      var raw;
      if (arc <= len1 && len1 > 0.000001) raw = lerpLab(base, gilded, arc / len1);
      else raw = lerpLab(gilded, white, Math.min(1, (arc - len1) / Math.max(len2, 0.000001)));
      return tamedChroma(raw);
    }

    var cache = {};
    function tileLab(value) {
      if (value < 2) return pal[0];
      var level = Math.max(1, Math.floor(Math.log2(value)));
      if (level <= pal.length) return pal[level - 1];
      var tailCount = Math.max(1, MAX_LEVEL - pal.length);
      return tailLab(pal[pal.length - 1], Math.min(level - pal.length, tailCount), tailCount);
    }
    function get(value) {
      if (!cache[value]) {
        var c = tileLab(value);
        cache[value] = { lab: c, hex: toHex(c), darkText: c.L >= 68 };
      }
      return cache[value];
    }
    // bgColorRGB = darkest anchor × 0.72 (BoardPaletteStore.make) → vividBackground
    var d = parseInt(hexes[0], 16);
    var bg = vividBackground(fromRGB(((d >> 16) & 255) / 255 * 0.72, ((d >> 8) & 255) / 255 * 0.72, (d & 255) / 255 * 0.72));
    return {
      id: boardId, levels: pal,
      tileLab: function (v) { return get(v).lab; },
      tileHex: function (v) { return get(v).hex; },
      darkText: function (v) { return get(v).darkText; },
      bgLab: bg, bg: toHex(bg),
      panel: toHex(lab(Math.min(96, bg.L + 9), bg.a, bg.b)),
      empty: toHex(lab(Math.min(96, Math.max(0, bg.L + 1)), bg.a, bg.b))
    };
  }

  /* ───────────── Share emoji (nearest in Lab) ───────────── */
  var EMOJI = [["🟥", "#E0393E"], ["🟧", "#F28B24"], ["🟨", "#F7CE46"], ["🟩", "#62B34A"], ["🟦", "#2E7FE0"],
    ["🟪", "#9B5BC4"], ["🟫", "#8A5A36"], ["⬛", "#262626"], ["⬜", "#EDEDED"]].map(function (e) { return [e[0], fromHex(e[1])]; });
  function nearestEmoji(c) {
    var best = EMOJI[0], bd = Infinity;
    for (var i = 0; i < EMOJI.length; i++) { var dd = deltaE(c, EMOJI[i][1]); if (dd < bd) { bd = dd; best = EMOJI[i]; } }
    return best[0];
  }

  /* ───────────── Engine (GameViewModel.swift) ───────────── */
  var nextId = 1;
  function tile(value, row, col, id) { return { id: id || nextId++, value: value, row: row, col: col }; }
  function toGrid(tiles) {
    var g = [], r, c;
    for (r = 0; r < SIZE; r++) { g.push([]); for (c = 0; c < SIZE; c++) g[r].push(0); }
    tiles.forEach(function (t) { g[t.row][t.col] = t.value; });
    return g;
  }
  function fromGrid(g) {
    var out = [];
    for (var r = 0; r < SIZE; r++) for (var c = 0; c < SIZE; c++) if (g[r][c]) out.push(tile(g[r][c], r, c));
    return out;
  }
  function cellFor(dir, line, step) {
    switch (dir) {
      case "left": return [line, step];
      case "right": return [line, SIZE - 1 - step];
      case "up": return [step, line];
      default: return [SIZE - 1 - step, line];
    }
  }
  /* Slide + merge. null when nothing moves (→ no spawn, like the app).
     merged: [{id, into, row, col}] — absorbed tile id and the survivor it slid into. */
  function move(tiles, dir) {
    var at = {};
    tiles.forEach(function (t) { at[t.row * SIZE + t.col] = t; });
    var out = [], merged = [], gained = 0, changed = false;
    for (var line = 0; line < SIZE; line++) {
      var lt = [];
      for (var step = 0; step < SIZE; step++) {
        var rc = cellFor(dir, line, step), t = at[rc[0] * SIZE + rc[1]];
        if (t) lt.push(t);
      }
      var o = 0, i = 0;
      while (i < lt.length) {
        var d = cellFor(dir, line, o), nt;
        if (i + 1 < lt.length && lt[i].value === lt[i + 1].value) {
          nt = tile(lt[i].value * 2, d[0], d[1], lt[i].id);
          gained += nt.value;
          merged.push({ id: lt[i + 1].id, into: lt[i].id, row: d[0], col: d[1] });
          changed = true;
          i += 2;
        } else {
          nt = tile(lt[i].value, d[0], d[1], lt[i].id);
          if (nt.row !== lt[i].row || nt.col !== lt[i].col) changed = true;
          i += 1;
        }
        out.push(nt);
        o++;
      }
    }
    if (!changed) return null;
    return { tiles: out, gained: gained, merged: merged };
  }
  function emptyCells(tiles) {
    var occ = {}, out = [];
    tiles.forEach(function (t) { occ[t.row * SIZE + t.col] = 1; });
    for (var r = 0; r < SIZE; r++) for (var c = 0; c < SIZE; c++) if (!occ[r * SIZE + c]) out.push([r, c]);
    return out;
  }
  // 2 at 90%, 4 at 10% on a random empty cell (addRandomTile)
  function spawn(tiles, rng) {
    rng = rng || Math.random;
    var e = emptyCells(tiles);
    if (!e.length) return null;
    var pos = e[Math.floor(rng() * e.length)];
    var t = tile(rng() < 0.9 ? 2 : 4, pos[0], pos[1]);
    tiles.push(t);
    return t;
  }
  function canMove(tiles) {
    var g = toGrid(tiles);
    for (var r = 0; r < SIZE; r++) for (var c = 0; c < SIZE; c++) {
      if (g[r][c] === 0) return true;
      if (c < SIZE - 1 && g[r][c] === g[r][c + 1]) return true;
      if (r < SIZE - 1 && g[r][c] === g[r + 1][c]) return true;
    }
    return false;
  }
  function maxValue(tiles) { return tiles.reduce(function (m, t) { return Math.max(m, t.value); }, 0); }
  // QuoteTheme.quote(forValue:) index — 2 → 0 … 2048 → 10, clamped to the last quote
  function quoteIndex(value, count) { return Math.min(count - 1, Math.max(0, Math.floor(Math.log2(value)) - 1)); }

  /* ───────────── Web schedule (web_schedule.json, fixed; epoch = puzzle #1) ───────────── */
  function dayKey(d) {
    return d.getFullYear() + "-" + (d.getMonth() < 9 ? "0" : "") + (d.getMonth() + 1) + "-" + (d.getDate() < 10 ? "0" : "") + d.getDate();
  }
  function keyToUTC(k) { var p = k.split("-"); return Date.UTC(+p[0], +p[1] - 1, +p[2]); }
  function daysBetween(a, b) { return Math.round((keyToUTC(b) - keyToUTC(a)) / 86400000); }
  /* sched = {epoch, days:[[themeId, boardId], …]}. Cycles forever. Days before the epoch are a
     preview (num 0 and below) that wraps backwards through the same cycle. */
  function scheduleFor(sched, key) {
    var off = daysBetween(sched.epoch, key), n = sched.days.length;
    var idx = ((off % n) + n) % n;
    return { num: off + 1, idx: idx, preview: off < 0, theme: sched.days[idx][0], board: sched.days[idx][1] };
  }

  /* ───────────── Tile font fitting (GameBoardView.swift · TileFontSizing) ─────────────
     measure(text, size) → rendered width in px of `text` in the tile font at `size`.
     lineHeight = font line height ÷ size. Returns the largest whole-px size (stepping down from
     max(9, tile × 0.185)) at which the whole quote fits the tile's content box with no ellipsis. */
  function isWrappable(seg) {
    for (var i = 0; i < seg.length; i++) {
      var s = seg.codePointAt(i);
      if ((s >= 0x1100 && s <= 0x11FF) || (s >= 0x3040 && s <= 0x30FF) || (s >= 0x3400 && s <= 0x4DBF) ||
          (s >= 0x4E00 && s <= 0x9FFF) || (s >= 0xAC00 && s <= 0xD7AF) || (s >= 0xF900 && s <= 0xFAFF)) return true;
      if (s > 0xFFFF) i++;
    }
    return false;
  }
  function fitFont(text, tileSize, measure, opts) {
    opts = opts || {};
    var ratio = opts.baseFontRatio || 0.185, lh = opts.lineHeight || 1.2, scale = opts.fontScale || 1;
    var defaultSize = Math.max(9, tileSize * ratio) * scale;
    var floor = 6;
    var cw = tileSize - 2 * (tileSize * 0.08), ch = tileSize - 2 * (tileSize * 0.02);
    if (!(cw > 0 && ch > 0)) return defaultSize;
    var words = text.split(" ");
    function lineCount(size) {
      var space = measure(" ", size), lines = 1, used = 0;
      for (var i = 0; i < words.length; i++) {
        var w = words[i];
        if (!w) continue;
        var ww = measure(w, size);
        if (ww > cw) {
          if (used > 0) lines += 1;
          lines += Math.ceil(ww / cw) - 1;
          used = ww % cw;
          continue;
        }
        var needed = used === 0 ? ww : used + space + ww;
        if (needed <= cw) used = needed;
        else { lines += 1; used = ww; }
      }
      return lines;
    }
    function heightFits(size) { return lineCount(size) * size * lh <= ch; }
    function wordsFit(size) {
      return words.every(function (w) {
        if (!w) return true;
        return w.split(/[—–-]/).every(function (seg) { return !seg || isWrappable(seg) || measure(seg, size) <= cw; });
      });
    }
    function largest(pred) {
      for (var c = defaultSize; c > floor; c -= 1) if (pred(c)) return c;
      return null;
    }
    var legibleFloor = 11 * scale;
    var best = largest(function (s) { return wordsFit(s) && heightFits(s); });
    if (best !== null && best >= legibleFloor) return best;
    var h = largest(heightFits);
    return h === null ? floor : h;
  }

  var api = {
    SIZE: SIZE, BOARDS: BOARDS, BOARD_IDS: BOARD_IDS,
    fromHex: fromHex, toHex: toHex, fromRGB: fromRGB, deltaE: deltaE, makeTheme: makeTheme, tamedChroma: tamedChroma,
    nearestEmoji: nearestEmoji, move: move, spawn: spawn, canMove: canMove, toGrid: toGrid, fromGrid: fromGrid,
    maxValue: maxValue, quoteIndex: quoteIndex, dayKey: dayKey, daysBetween: daysBetween, scheduleFor: scheduleFor,
    fitFont: fitFont, isWrappable: isWrappable
  };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.QuoteCore = api;
})(this);
