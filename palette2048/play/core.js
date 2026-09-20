/* Palette daily (web) — pure core: 2048 engine + palette color mapping.
   Ported from the iOS app (Palette2048/GameViewModel.swift, ThemeManager.swift).
   Keep the math identical to the app so web tiles render the same colors.
   No DOM access here — node tests require() this file (see test_core.js). */
(function (root) {
  "use strict";

  /* ───────────── Lab color (ThemeManager.swift · LabColor) ───────────── */
  function clamp01(v) { return Math.min(1, Math.max(0, v)); }
  function gamma(c) { return c <= 0.0031308 ? 12.92 * c : 1.055 * Math.pow(c, 1 / 2.4) - 0.055; }
  function invGamma(c) { return c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); }
  var EPS = 0.008856, KAPPA = 903.3;

  function lab(L, a, b) { return { L: L, a: a, b: b }; }

  function fromRGB(r, g, b) { // components 0..1
    var rl = invGamma(r), gl = invGamma(g), bl = invGamma(b);
    var X = (0.4124564 * rl + 0.3575761 * gl + 0.1804375 * bl) / 0.95047;
    var Y = (0.2126729 * rl + 0.7151522 * gl + 0.0721750 * bl) / 1.0;
    var Z = (0.0193339 * rl + 0.1191920 * gl + 0.9503041 * bl) / 1.08883;
    var fx = X > EPS ? Math.cbrt(X) : (KAPPA * X + 16) / 116;
    var fy = Y > EPS ? Math.cbrt(Y) : (KAPPA * Y + 16) / 116;
    var fz = Z > EPS ? Math.cbrt(Z) : (KAPPA * Z + 16) / 116;
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

  function toBytes(c) {
    var v = toRGB(c);
    return [Math.round(clamp01(v[0]) * 255), Math.round(clamp01(v[1]) * 255), Math.round(clamp01(v[2]) * 255)];
  }
  function hex2(n) { return (n < 16 ? "0" : "") + n.toString(16).toUpperCase(); }
  function toHex(c) { var b = toBytes(c); return "#" + hex2(b[0]) + hex2(b[1]) + hex2(b[2]); }
  function fromHex(h) {
    var n = parseInt(h.replace("#", ""), 16);
    return fromRGB(((n >> 16) & 255) / 255, ((n >> 8) & 255) / 255, (n & 255) / 255);
  }
  function lerpLab(p, q, t) { return lab(p.L + (q.L - p.L) * t, p.a + (q.a - p.a) * t, p.b + (q.b - p.b) * t); }
  function deltaE(p, q) { var d1 = p.L - q.L, d2 = p.a - q.a, d3 = p.b - q.b; return Math.sqrt(d1 * d1 + d2 * d2 + d3 * d3); }

  /* ───────────── Palette (ThemeManager.swift · GeneratedPalette) ───────────── */
  function hueLockedLerp(from, to, t) {
    var cFrom = Math.sqrt(from.a * from.a + from.b * from.b);
    var cTo = Math.sqrt(to.a * to.a + to.b * to.b);
    var hFrom = Math.atan2(from.b, from.a), hTo = Math.atan2(to.b, to.a);
    if (cFrom < 3) hFrom = hTo;
    if (cTo < 3) hTo = hFrom;
    var h = t < 0.5 ? hFrom : hTo;
    var c = cFrom + (cTo - cFrom) * t;
    return lab(from.L + (to.L - from.L) * t, c * Math.cos(h), c * Math.sin(h));
  }

  // Uniform N-stop interpolator (GeneratedPalette.interpolate)
  function interpolate(stops, t) {
    if (stops.length === 1) return stops[0];
    var c = Math.min(Math.max(t, 0), 1), n = stops.length;
    var seg = Math.min(Math.floor(c * (n - 1)), n - 2);
    return hueLockedLerp(stops[seg], stops[seg + 1], c * (n - 1) - seg);
  }

  // All 6 anchors sorted dark→light (smoothPath / gameStops)
  function gameStops(anchorHex) {
    return anchorHex.map(fromHex).sort(function (p, q) { return p.L - q.L; });
  }

  function anchorLevels(stops, exposure) {
    var n = stops.length, i;
    var segs = [], total = 0;
    for (i = 0; i < n - 1; i++) { segs.push(Math.max(deltaE(stops[i], stops[i + 1]), 0.000001)); total += segs[i]; }
    var pos = [1];
    for (i = 0; i < segs.length; i++) pos.push(pos[pos.length - 1] + segs[i] / total * (exposure - 1));
    // Swift .rounded() = half away from zero (positions are positive)
    var lv = pos.map(function (p) { return Math.floor(p + 0.5); });
    lv[0] = 1;
    for (i = 1; i < n; i++) if (lv[i] <= lv[i - 1]) lv[i] = lv[i - 1] + 1;
    lv[n - 1] = exposure;
    for (i = n - 2; i >= 0; i--) if (lv[i] >= lv[i + 1]) lv[i] = lv[i + 1] - 1;
    return lv;
  }

  function gameTileLab(stops, levels, level) {
    if (!(level > levels[0])) return stops[0];
    for (var i = 0; i < levels.length - 1; i++) {
      if (level <= levels[i + 1]) {
        var span = levels[i + 1] - levels[i];
        return hueLockedLerp(stops[i], stops[i + 1], span > 0 ? (level - levels[i]) / span : 1);
      }
    }
    return stops[stops.length - 1];
  }

  var CHROMA_CAP = [[0, 78], [25, 80], [55, 90], [85, 95], [110, 88], [140, 75],
    [180, 62], [220, 55], [260, 55], [300, 65], [330, 72], [360, 78]];

  function tamedChroma(c) {
    var ch = Math.sqrt(c.a * c.a + c.b * c.b);
    if (!(ch > 0)) return c;
    var h = Math.atan2(c.b, c.a) * 180 / Math.PI;
    if (h < 0) h += 360;
    var base = CHROMA_CAP[0][1];
    for (var i = 0; i < CHROMA_CAP.length - 1; i++) {
      var h0 = CHROMA_CAP[i][0], c0 = CHROMA_CAP[i][1], h1 = CHROMA_CAP[i + 1][0], c1 = CHROMA_CAP[i + 1][1];
      if (h >= h0 && h <= h1) { base = c0 + (c1 - c0) * (h - h0) / (h1 - h0); break; }
    }
    var lightFactor = c.L <= 60 ? 1 : Math.max(0.8, 1 - (c.L - 60) * 0.005);
    var maxC = base * lightFactor;
    if (!(ch > maxC)) return c;
    var s = maxC / ch;
    return lab(c.L, c.a * s, c.b * s);
  }

  // 4×4 board constants (BoardSize.four)
  var SIZE = 4, EXPOSURE = 11, MAX_LEVEL = 16;

  /* Theme for one painting. p = { colors:[6 hex], bg: hex|null } */
  function makeTheme(p) {
    var stops = gameStops(p.colors);
    var levels = anchorLevels(stops, EXPOSURE);
    var bg = p.bg ? fromHex(p.bg) : interpolate(stops, 0);
    var cache = {};
    function tileLab(value) {
      var raw;
      if (value < 2) raw = interpolate(stops, 0);
      else {
        var level = Math.max(1, Math.floor(Math.log2(value)));
        if (level <= EXPOSURE) raw = gameTileLab(stops, levels, Math.min(level, EXPOSURE));
        else {
          var base = interpolate(stops, 1);
          var cap = lab(Math.min(98, Math.max(base.L + 18, 92)), base.a * 0.55, base.b * 0.55);
          var t = Math.min(Math.max((level - EXPOSURE) / Math.max(1, MAX_LEVEL - EXPOSURE), 0), 1);
          raw = lerpLab(base, cap, t);
        }
      }
      return tamedChroma(raw);
    }
    return {
      stops: stops,
      levels: levels,
      tileLab: tileLab,
      tileHex: function (v) { return cache[v] || (cache[v] = toHex(tileLab(v))); },
      bgLab: bg,
      bg: toHex(bg),
      panel: toHex(lab(Math.min(96, bg.L + 7), bg.a, bg.b)),
      empty: toHex(lab(Math.min(96, Math.max(0, bg.L + 3)), bg.a, bg.b)),
      ink: bg.L > 55 ? toHex(lab(20, bg.a * 0.3, bg.b * 0.3)) : toHex(lab(85, bg.a * 0.15, bg.b * 0.15)),
      isLight: bg.L > 55
    };
  }

  /* ───────────── Share emoji (nearest in Lab) ───────────── */
  var EMOJI = [["🟥", "#E0393E"], ["🟧", "#F28B24"], ["🟨", "#F7CE46"], ["🟩", "#62B34A"], ["🟦", "#2E7FE0"],
    ["🟪", "#9B5BC4"], ["🟫", "#8A5A36"], ["⬛", "#262626"], ["⬜", "#EDEDED"]].map(function (e) { return [e[0], fromHex(e[1])]; });
  function nearestEmoji(c) {
    var best = EMOJI[0], bd = Infinity;
    for (var i = 0; i < EMOJI.length; i++) { var d = deltaE(c, EMOJI[i][1]); if (d < bd) { bd = d; best = EMOJI[i]; } }
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
      default: return [SIZE - 1 - step, line]; // down
    }
  }

  /* Slide + merge. Returns null when nothing moves (→ no spawn, like the app).
     merged: [{id, into}] — the absorbed tile id and the survivor it slid into. */
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

  // 2 at 90%, 4 at 10% on a random empty cell. rng() in [0,1)
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

  /* ───────────── Daily schedule (CuratedPalettes.swift · dailyPalette) ───────────── */
  function dayKey(d) {
    return d.getFullYear() + "-" + (d.getMonth() < 9 ? "0" : "") + (d.getMonth() + 1) + "-" + (d.getDate() < 10 ? "0" : "") + d.getDate();
  }
  function keyToUTC(k) { var p = k.split("-"); return Date.UTC(+p[0], +p[1] - 1, +p[2]); }
  function daysBetween(a, b) { return Math.round((keyToUTC(b) - keyToUTC(a)) / 86400000); }

  // Puzzle number for a day (daily.json's epoch is fixed regardless of which schedule — app's or
  // web's own, see build.py — supplied that day's painting; the numbering stays one continuous count).
  function puzzleNumber(epoch, dayKey) { return daysBetween(epoch, dayKey) + 1; }

  // Fallback painting for a dayKey missing from daily.json's `days` window (device clock set past
  // daily.json's `end`): rotate through all.json's `rows` (one full schedule period, already ordered
  // to start the day right after `end` — see build.py#build_data), cycling forever via modulo.
  function pickFromAll(all, dayKey) {
    var past = daysBetween(all.end, dayKey);
    var row = past >= 1 ? all.rows[(past - 1) % all.rows.length] : all.rows[0];
    return unpack(row);
  }

  // Light XOR+base64, same scheme/key as the app's CuratedPalette.deobf
  var OBF = "palette2048-2026-curator";
  function deobf(s) {
    if (!s) return "";
    var bin = (typeof atob === "function") ? atob(s) : Buffer.from(s, "base64").toString("binary");
    var bytes = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i) ^ OBF.charCodeAt(i % OBF.length);
    return new TextDecoder().decode(bytes);
  }
  // Compact row → painting. Row: [id, nameObf, artistObf, year, "hex hex hex hex hex hex", bg|"",
  // urlObf, imageOk(0/1), [flavorEnObf, flavorKoObf, flavorJaObf, flavorZhHantObf, flavorZhHansObf]]
  // 인덱스 순서는 build.py 의 FLAVOR_LOCALES 와 짝이다. 구버전 daily.json 이 캐시돼 3개만 올 수 있어 길이를 확인한다.
  function unpack(row) {
    return { id: row[0], name: deobf(row[1]), artist: deobf(row[2]), year: row[3],
      colors: row[4].split(" ").map(function (h) { return "#" + h; }), bg: row[5] ? "#" + row[5] : null,
      url: deobf(row[6]), imageOk: !!row[7],
      flavor: { en: deobf(row[8][0]), ko: deobf(row[8][1]), ja: deobf(row[8][2]),
                "zh-Hant": row[8].length > 3 ? deobf(row[8][3]) : "",
                "zh-Hans": row[8].length > 4 ? deobf(row[8][4]) : "" } };
  }

  // Downsize a Wikimedia Commons image URL to one of the widths the thumbnail service accepts
  // (20/40/60/120/250/330/500/960/1280/1920/3840px — arbitrary widths return HTTP 400). Works for
  // both /thumb/.../NNNpx-name URLs and bare (un-thumbnailed) Commons file URLs. Anything else
  // (non-Commons url) is returned unchanged.
  function thumbURL(url, width) {
    width = width || 500;
    var clean = url.split("?")[0];
    var m = clean.match(/^(https:\/\/upload\.wikimedia\.org\/wikipedia\/commons\/thumb\/[^/]+\/[^/]+\/[^/]+)\/\d+px-([^/]+)$/);
    if (m) return m[1] + "/" + width + "px-" + m[2];
    m = clean.match(/^(https:\/\/upload\.wikimedia\.org\/wikipedia\/commons)\/([0-9a-f])\/([0-9a-f]{2})\/([^/]+)$/);
    if (m) return m[1] + "/thumb/" + m[2] + "/" + m[3] + "/" + m[4] + "/" + width + "px-" + m[4];
    return url;
  }

  var api = {
    SIZE: SIZE, fromHex: fromHex, toHex: toHex, fromRGB: fromRGB, deltaE: deltaE, makeTheme: makeTheme,
    hueLockedLerp: hueLockedLerp, anchorLevels: anchorLevels, nearestEmoji: nearestEmoji,
    move: move, spawn: spawn, canMove: canMove, toGrid: toGrid, fromGrid: fromGrid, maxValue: maxValue,
    dayKey: dayKey, daysBetween: daysBetween, deobf: deobf, unpack: unpack, thumbURL: thumbURL,
    puzzleNumber: puzzleNumber, pickFromAll: pickFromAll
  };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.PaletteCore = api;
})(this);
