// node palette2048/play/test_core.js — engine + color sanity tests for core.js
"use strict";
const assert = require("assert");
const C = require("./core.js");

const row = (vals, dir = "left") => {
  const res = C.move(C.fromGrid([vals, [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]), dir);
  return res ? { line: C.toGrid(res.tiles)[0], gained: res.gained } : null;
};
let n = 0;
const test = (name, fn) => { fn(); n++; console.log("ok -", name); };

test("[2,2,2,2] → [4,4,0,0]", () => {
  const r = row([2, 2, 2, 2]);
  assert.deepStrictEqual(r.line, [4, 4, 0, 0]);
  assert.strictEqual(r.gained, 8);
});
test("[2,2,4,0] → [4,4,0,0] (no chain merge)", () => assert.deepStrictEqual(row([2, 2, 4, 0]).line, [4, 4, 0, 0]));
test("[4,4,8,8] → [8,16,0,0]", () => assert.deepStrictEqual(row([4, 4, 8, 8]).line, [8, 16, 0, 0]));
test("[2,0,0,2] → [4,0,0,0]", () => assert.deepStrictEqual(row([2, 0, 0, 2]).line, [4, 0, 0, 0]));
test("[2,2,2,0] right → [0,0,2,4] (merge from the leading edge)", () =>
  assert.deepStrictEqual(row([2, 2, 2, 0], "right").line, [0, 0, 2, 4]));
test("[2,4,8,16] left → no move (null)", () => assert.strictEqual(row([2, 4, 8, 16]), null));
test("column up/down", () => {
  const g = [[2, 0, 0, 0], [2, 0, 0, 0], [4, 0, 0, 0], [4, 0, 0, 0]];
  assert.deepStrictEqual(C.toGrid(C.move(C.fromGrid(g), "up").tiles).map((r) => r[0]), [4, 8, 0, 0]);
  assert.deepStrictEqual(C.toGrid(C.move(C.fromGrid(g), "down").tiles).map((r) => r[0]), [0, 0, 4, 8]);
});
test("no move → no spawn (caller spawns only on a real move)", () => {
  const tiles = C.fromGrid([[2, 4, 8, 16], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]);
  const before = tiles.length;
  const res = C.move(tiles, "left");
  if (res) C.spawn(tiles);
  assert.strictEqual(res, null);
  assert.strictEqual(tiles.length, before);
});
test("merge keeps the leading tile id, reports absorbed id", () => {
  const tiles = C.fromGrid([[2, 2, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]);
  const res = C.move(tiles, "left");
  assert.strictEqual(res.tiles[0].id, tiles[0].id);
  assert.strictEqual(res.merged[0].id, tiles[1].id);
  assert.strictEqual(res.merged[0].into, tiles[0].id);
});
test("canMove", () => {
  assert.strictEqual(C.canMove(C.fromGrid([[2, 4, 2, 4], [4, 2, 4, 2], [2, 4, 2, 4], [4, 2, 4, 8]])), false);
  assert.strictEqual(C.canMove(C.fromGrid([[2, 4, 2, 4], [4, 2, 4, 2], [2, 4, 2, 4], [4, 2, 8, 8]])), true);
  assert.strictEqual(C.canMove(C.fromGrid([[2, 4, 2, 4], [4, 2, 4, 2], [2, 4, 2, 4], [4, 2, 4, 0]])), true);
  assert.strictEqual(C.canMove(C.fromGrid([[2, 4, 2, 4], [4, 2, 4, 2], [2, 4, 2, 8], [4, 2, 4, 8]])), true);
});
test("spawn: 2 at 90%, 4 at 10%, only on empty cells", () => {
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
test("Lab round trip", () => {
  for (const h of ["#000000", "#FFFFFF", "#16377A", "#D8D391", "#B9000C"]) assert.strictEqual(C.toHex(C.fromHex(h)), h);
});
test("deobf matches the app key", () => {
  const b64 = Buffer.from([..."Mona Lisa"].map((ch, i) => ch.charCodeAt(0) ^ "palette2048-2026-curator".charCodeAt(i))).toString("base64");
  assert.strictEqual(C.deobf(b64), "Mona Lisa");
});
test("daysBetween / puzzle number", () => {
  assert.strictEqual(C.daysBetween("2026-03-01", "2026-09-17") + 1, 201);
  assert.strictEqual(C.daysBetween("2027-02-28", "2027-03-01"), 1);
});
test("puzzleNumber matches daysBetween+1 and stays continuous across the web/app schedule split", () => {
  assert.strictEqual(C.puzzleNumber("2026-03-01", "2026-09-17"), 201);
  assert.strictEqual(C.puzzleNumber("2026-03-01", "2026-09-18"), 202); // first web-scheduled day
});
test("pickFromAll rotates through all.json's rows, wrapping forever from the day after `end`", () => {
  const mkRow = (id) => [id, "", "", "", "000000 000000 000000 000000 000000 000000", "", "", 0, ["", "", ""]];
  const all = { end: "2027-09-04", rows: ["a", "b", "c"].map(mkRow) };
  assert.strictEqual(C.pickFromAll(all, "2027-09-05").id, "a"); // end+1 → rows[0]
  assert.strictEqual(C.pickFromAll(all, "2027-09-06").id, "b"); // end+2 → rows[1]
  assert.strictEqual(C.pickFromAll(all, "2027-09-07").id, "c"); // end+3 → rows[2]
  assert.strictEqual(C.pickFromAll(all, "2027-09-08").id, "a"); // end+4 → wraps back to rows[0]
  assert.strictEqual(C.pickFromAll(all, "2028-09-08").id, C.pickFromAll(all, "2027-09-08").id); // wraps forever
  assert.strictEqual(C.pickFromAll(all, "2027-09-04").id, "a"); // dayKey === end (edge case): rows[0]
});
test("unpack decodes url, imageOk and per-locale flavor", () => {
  const KEY = "palette2048-2026-curator";
  const obf = (s) => Buffer.from([...Buffer.from(s, "utf8")].map((b, i) => b ^ KEY.charCodeAt(i % KEY.length))).toString("base64");
  const row = ["mona-lisa", obf("Mona Lisa"), obf("Leonardo da Vinci"), "1503",
    "000000 111111 222222 333333 444444 555555", "",
    obf("https://upload.wikimedia.org/wikipedia/commons/0/00/x.jpg"), 1,
    [obf("She smiles."), obf("그녀가 웃는다."), obf("彼女は微笑む。")]];
  const p = C.unpack(row);
  assert.strictEqual(p.name, "Mona Lisa");
  assert.strictEqual(p.url, "https://upload.wikimedia.org/wikipedia/commons/0/00/x.jpg");
  assert.strictEqual(p.imageOk, true);
  assert.deepStrictEqual(p.flavor, { en: "She smiles.", ko: "그녀가 웃는다.", ja: "彼女は微笑む。" });
  const row2 = row.slice(); row2[7] = 0;
  assert.strictEqual(C.unpack(row2).imageOk, false);
});
test("thumbURL downsizes Commons images, leaves others untouched", () => {
  assert.strictEqual(
    C.thumbURL("https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Water_Lilies.jpg/960px-Water_Lilies.jpg", 500),
    "https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Water_Lilies.jpg/500px-Water_Lilies.jpg");
  assert.strictEqual(
    C.thumbURL("https://upload.wikimedia.org/wikipedia/commons/b/bb/Venere_di_Urbino.jpg", 500),
    "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bb/Venere_di_Urbino.jpg/500px-Venere_di_Urbino.jpg");
  assert.strictEqual(
    C.thumbURL("https://upload.wikimedia.org/wikipedia/commons/4/46/Last_Supper.jpg?utm_source=en.wikipedia.org", 500),
    "https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Last_Supper.jpg/500px-Last_Supper.jpg");
  assert.strictEqual(
    C.thumbURL("https://www.moma.org/collection/works/79802", 500),
    "https://www.moma.org/collection/works/79802");
});
test("nearest emoji", () => {
  assert.strictEqual(C.nearestEmoji(C.fromHex("#D02030")), "🟥");
  assert.strictEqual(C.nearestEmoji(C.fromHex("#1E5FC0")), "🟦");
  assert.strictEqual(C.nearestEmoji(C.fromHex("#FAFAFA")), "⬜");
  assert.strictEqual(C.nearestEmoji(C.fromHex("#101010")), "⬛");
});
console.log(`\n${n} tests passed`);
