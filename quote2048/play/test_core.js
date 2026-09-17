// node quote2048/play/test_core.js — engine, schedule, color and tile-font sanity tests for core.js
"use strict";
const assert = require("assert");
const fs = require("fs");
const path = require("path");
const C = require("./core.js");

const row = (vals, dir = "left") => {
  const res = C.move(C.fromGrid([vals, [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]), dir);
  return res ? { line: C.toGrid(res.tiles)[0], gained: res.gained } : null;
};
let n = 0;
const test = (name, fn) => { fn(); n++; console.log("ok -", name); };

/* ── merge rules ── */
test("[2,2,2,2] → [4,4,0,0], +8", () => {
  const r = row([2, 2, 2, 2]);
  assert.deepStrictEqual(r.line, [4, 4, 0, 0]);
  assert.strictEqual(r.gained, 8);
});
test("[2,2,4,0] → [4,4,0,0] (no chain merge)", () => assert.deepStrictEqual(row([2, 2, 4, 0]).line, [4, 4, 0, 0]));
test("[4,4,8,8] → [8,16,0,0]", () => assert.deepStrictEqual(row([4, 4, 8, 8]).line, [8, 16, 0, 0]));
test("[2,0,0,2] → [4,0,0,0]", () => assert.deepStrictEqual(row([2, 0, 0, 2]).line, [4, 0, 0, 0]));
test("[2,2,2,0] right → [0,0,2,4] (merge from the leading edge)", () =>
  assert.deepStrictEqual(row([2, 2, 2, 0], "right").line, [0, 0, 2, 4]));
test("[1024,1024,0,0] → 2048, +2048", () => {
  const r = row([1024, 1024, 0, 0]);
  assert.deepStrictEqual(r.line, [2048, 0, 0, 0]);
  assert.strictEqual(r.gained, 2048);
});
test("[2,4,8,16] left → no move (null)", () => assert.strictEqual(row([2, 4, 8, 16]), null));
test("column up/down", () => {
  const g = [[2, 0, 0, 0], [2, 0, 0, 0], [4, 0, 0, 0], [4, 0, 0, 0]];
  assert.deepStrictEqual(C.toGrid(C.move(C.fromGrid(g), "up").tiles).map((r) => r[0]), [4, 8, 0, 0]);
  assert.deepStrictEqual(C.toGrid(C.move(C.fromGrid(g), "down").tiles).map((r) => r[0]), [0, 0, 4, 8]);
});
test("merge keeps the leading tile id, reports absorbed id", () => {
  const tiles = C.fromGrid([[2, 2, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]);
  const res = C.move(tiles, "left");
  assert.strictEqual(res.tiles[0].id, tiles[0].id);
  assert.strictEqual(res.merged[0].id, tiles[1].id);
  assert.strictEqual(res.merged[0].into, tiles[0].id);
});

/* ── canMove / spawn ── */
test("canMove", () => {
  assert.strictEqual(C.canMove(C.fromGrid([[2, 4, 2, 4], [4, 2, 4, 2], [2, 4, 2, 4], [4, 2, 4, 8]])), false);
  assert.strictEqual(C.canMove(C.fromGrid([[2, 4, 2, 4], [4, 2, 4, 2], [2, 4, 2, 4], [4, 2, 8, 8]])), true);
  assert.strictEqual(C.canMove(C.fromGrid([[2, 4, 2, 4], [4, 2, 4, 2], [2, 4, 2, 4], [4, 2, 4, 0]])), true);
  assert.strictEqual(C.canMove(C.fromGrid([[2, 4, 2, 4], [4, 2, 4, 2], [2, 4, 2, 8], [4, 2, 4, 8]])), true);
});
test("spawn: 2 at 90%, 4 at 10%, only on empty cells; full board → null", () => {
  let fours = 0;
  const N = 20000;
  for (let i = 0; i < N; i++) {
    const tiles = C.fromGrid([[2, 2, 2, 2], [2, 2, 2, 2], [2, 2, 2, 2], [2, 2, 2, 0]]);
    const t = C.spawn(tiles);
    assert.deepStrictEqual([t.row, t.col], [3, 3]);
    if (t.value === 4) fours++;
  }
  assert.ok(Math.abs(fours / N - 0.1) < 0.012, `4-rate ${fours / N}`);
  assert.strictEqual(C.spawn(C.fromGrid([[2, 4, 2, 4], [4, 2, 4, 2], [2, 4, 2, 4], [4, 2, 4, 8]])), null);
});
test("quoteIndex: 2→0 … 2048→10, 131072→16, clamps past the last quote", () => {
  assert.strictEqual(C.quoteIndex(2, 17), 0);
  assert.strictEqual(C.quoteIndex(2048, 17), 10);
  assert.strictEqual(C.quoteIndex(131072, 17), 16);
  assert.strictEqual(C.quoteIndex(262144, 17), 16);
});

/* ── schedule ── */
const sched = JSON.parse(fs.readFileSync(path.join(__dirname, "web_schedule.json"), "utf8"));
test("schedule: 2026-09-18 = #1 = days[0]; cycles every 60 days", () => {
  assert.strictEqual(sched.days.length, 60);
  const a = C.scheduleFor(sched, "2026-09-18");
  assert.deepStrictEqual([a.num, a.idx, a.preview, a.theme, a.board], [1, 0, false, sched.days[0][0], sched.days[0][1]]);
  const b = C.scheduleFor(sched, "2026-11-16"); // +59
  assert.deepStrictEqual([b.num, b.idx], [60, 59]);
  const c = C.scheduleFor(sched, "2026-11-17"); // +60 → wraps
  assert.deepStrictEqual([c.num, c.idx, c.theme], [61, 0, sched.days[0][0]]);
  const d = C.scheduleFor(sched, "2027-03-01"); // DST/month/year boundaries
  assert.strictEqual(d.num, 165);
  assert.strictEqual(d.idx, 164 % 60);
});
test("schedule: days before the epoch are a preview, wrapping backwards", () => {
  const p = C.scheduleFor(sched, "2026-09-17");
  assert.deepStrictEqual([p.num, p.idx, p.preview], [0, 59, true]);
});
test("schedule: 60 distinct themes, day 1 topic, no kind 3 days in a row (cyclic)", () => {
  const qj = JSON.parse(fs.readFileSync(require("os").homedir() + "/Quote2048/tools/quotes.json", "utf8"));
  const kind = Object.fromEntries(qj.themes.map((t) => [t.id, t.kind]));
  const ids = sched.days.map((d) => d[0]);
  assert.strictEqual(new Set(ids).size, 60);
  assert.strictEqual(kind[ids[0]], "topic");
  for (let i = 0; i < 60; i++) {
    const k = [0, 1, 2].map((j) => kind[ids[(i + j) % 60]]);
    assert.ok(!(k[0] === k[1] && k[1] === k[2]), `run of 3 at ${i}`);
  }
  for (let i = 0; i < 60; i++) assert.notStrictEqual(sched.days[i][1], sched.days[(i + 1) % 60][1], "same board two days in a row");
});
test("daysBetween", () => {
  assert.strictEqual(C.daysBetween("2026-09-18", "2026-09-18"), 0);
  assert.strictEqual(C.daysBetween("2027-02-28", "2027-03-01"), 1);
  assert.strictEqual(C.daysBetween("2026-10-31", "2026-11-02"), 2);
});

/* ── data obfuscation (build.py's play/d/<opaque>.json) ── */
test("deobf: round-trips a built data file against quotes.json (filename hides locale+theme id)", () => {
  // Mirrors build.py's opaque_name() — sha256(FILE_SALT|locale|id) → first 16 hex chars + ".json".
  // A visitor's browser never computes this itself (each locale's play page already embeds its own
  // opaque filenames in S.sched); this replica exists only so the test can find the right file.
  const crypto = require("crypto");
  const FILE_SALT = "quote2048-2026-files"; // must match build.py's FILE_SALT
  const opaqueName = (locale, tid) =>
    crypto.createHash("sha256").update(`${FILE_SALT}|${locale}|${tid}`, "utf8").digest("hex").slice(0, 16) + ".json";

  const qj = JSON.parse(fs.readFileSync(require("os").homedir() + "/Quote2048/tools/quotes.json", "utf8"));
  const theme = qj.themes.find((t) => t.id === "courage");
  const fname = opaqueName("en", "courage");
  const body = fs.readFileSync(path.join(__dirname, "d", fname), "utf8").trim();
  const obj = JSON.parse(C.deobf(body));
  assert.strictEqual(obj.id, "courage");
  assert.strictEqual(obj.kind, "topic");
  assert.strictEqual(obj.q.length, 17, "all 17 levels ship (continue-past-2048 stays unobfuscated)");
  theme.quotes.forEach((q, i) => {
    assert.strictEqual(obj.q[i][0], q.en, `quote ${i} text`);
    assert.strictEqual(obj.q[i][1], q.author_en, `quote ${i} author`);
  });
  // opaque filenames differ per locale for the same theme (locale folded into the hash)
  assert.notStrictEqual(opaqueName("ko", "courage"), fname);
});

/* ── colors ── */
test("Lab round trip", () => {
  for (const h of ["#000000", "#FFFFFF", "#16294A", "#F2E3C4", "#B23A38"]) assert.strictEqual(C.toHex(C.fromHex(h)), h);
});
test("board palettes: 10 boards, first tile = darkest anchor, ramp gets lighter to 2048", () => {
  assert.strictEqual(C.BOARD_IDS.length, 10);
  for (const id of C.BOARD_IDS) {
    const th = C.makeTheme(id);
    assert.strictEqual(th.tileHex(2), "#" + C.BOARDS[id][0]);
    let prev = -1;
    for (let v = 2; v <= 2048; v *= 2) { const L = th.tileLab(v).L; assert.ok(L >= prev - 0.001, `${id} ${v}`); prev = L; }
  }
});
test("tile text color: dark ink on light tiles (L ≥ 68)", () => {
  const th = C.makeTheme("board-dawn");
  assert.strictEqual(th.darkText(2), false);
  assert.strictEqual(th.darkText(2048), true);
});

/* ── tile font fitting ── */
const mono = (ratio) => (text, size) => [...text].length * size * ratio; // fixed-advance fake font
test("fitFont: short text keeps the default size max(9, tile × 0.185)", () => {
  assert.strictEqual(C.fitFont("Hi", 80, mono(0.5)), 80 * 0.185);
  assert.strictEqual(C.fitFont("Hi", 40, mono(0.5)), 9);
});
test("fitFont: result actually fits the content box (greedy word wrap)", () => {
  const text = "A journey of a thousand miles starts with one step";
  const tile = 78, m = mono(0.55), s = C.fitFont(text, tile, m, { lineHeight: 1.2 });
  assert.ok(s < tile * 0.185 && s >= 6, `size ${s}`);
  const cw = tile * 0.84, words = text.split(" ");
  const fits = (z) => {
    let lines = 1, used = 0;
    for (const w of words) { const ww = m(w, z); const need = used ? used + m(" ", z) + ww : ww; if (need <= cw) used = need; else { lines++; used = ww; } }
    return lines * z * 1.2 <= tile * 0.96;
  };
  assert.ok(fits(s), `size ${s} must fit`);
  assert.ok(!fits(s + 1), `size ${s + 1} fits too — not the largest`);
});
test("fitFont: longer text never gets a bigger font", () => {
  const m = mono(0.55);
  const a = C.fitFont("Well begun is half done", 78, m), b = C.fitFont("Well begun is half done and the rest takes care of itself in time", 78, m);
  assert.ok(b <= a);
});
test("fitFont: CJK text wraps between characters (no word-break penalty)", () => {
  assert.strictEqual(C.isWrappable("天下"), true);
  assert.strictEqual(C.isWrappable("시작이"), true);
  assert.strictEqual(C.isWrappable("Knowledge"), false);
  const s = C.fitFont("千里之行始于足下千里之行始于足下千里之行始于足下", 78, (t, z) => [...t].length * z);
  assert.ok(s >= 6 && s < 78 * 0.185);
});
test("fitFont: one very long Latin word gives up word-keeping below 11px", () => {
  const s = C.fitFont("Incomprehensibilities", 50, mono(0.6));
  assert.ok(s > 6 && s <= 11, `size ${s}`);
});
test("fitFont: zero-size tile falls back to the default", () => assert.strictEqual(C.fitFont("x", 0, mono(0.5)), 9));

console.log(`\n${n} tests passed`);
