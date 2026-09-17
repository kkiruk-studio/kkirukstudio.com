#!/usr/bin/env python3
"""Palette web daily — generator for the browser puzzle and the painting-palette SEO pages.

Outputs (edit this file / play.js / play.css / core.js / palettes.css, never the generated HTML):
  palette2048/play/index.html, play/ko/index.html, play/ja/index.html   — daily puzzle (en/ko/ja)
  palette2048/play/daily.json   — date → painting rows, from (build date − 2 days) to the app's
                                  SCHEDULE_CUTOFF; names lightly obfuscated like the app
  palette2048/play/all.json     — the app's `all` rotation (only fetched after the cutoff)
  palette2048/palettes/index.html, palettes/<painting-id>/index.html — English palette pages
  sitemap.xml                   — regenerated with gen/gen_sitemap.py (scans canonical URLs)

Source of truth is the app repo (read-only): ~/Palette2048/tools/paintings.json + schedule.json,
and SCHEDULE_CUTOFF from tools/generate_swift.py, so the web follows exactly the same daily
schedule and fallback rotation as CuratedPaletteStore.dailyPalette(for:).
Override the repo location with PALETTE_REPO=/path.

DAILY REBUILD: palette pages are generated only for paintings whose scheduled date is strictly
before the build date (no spoilers for upcoming puzzles). Re-running this script every day
therefore adds one new /palettes/<id>/ page per day and refreshes daily.json's window.
  python3 palette2048/play/build.py                 # build for today (local date)
  python3 palette2048/play/build.py --date 2026-09-20   # pretend the build date (testing)
"""
import argparse
import base64
import datetime as dt
import hashlib
import importlib.util
import json
import math
import os
import re
import shutil
import subprocess
import sys
from html import escape
from pathlib import Path

sys.dont_write_bytecode = True

# ─── Constants ────────────────────────────────────────────────────────────────
PT = ""                                   # App Store provider token (pt). Empty → omitted.
CT_PLAY = "palette_web_play"              # campaign token for the play page CTAs
CT_PALETTE = "palette_web_palette"        # campaign token for palette pages
APP_ID = "6767449110"
APP_NAME = "Palette: Daily Art Puzzle"
EPOCH = "2026-03-01"                      # puzzle #1 = first day of the app schedule
SITE = "https://www.kkirukstudio.com"
OG_IMAGE = SITE + "/palette2048/og.png"
OBF_KEY = b"palette2048-2026-curator"     # same light XOR as the app (CuratedPalette.deobf)
BUILD_MARK = "<!-- seo:build-owned palette2048/play/build.py -->"

HERE = Path(__file__).resolve().parent            # palette2048/play
P2048 = HERE.parent                               # palette2048
ROOT = P2048.parent                               # site root
PAL_DIR = P2048 / "palettes"
REPO = Path(os.environ.get("PALETTE_REPO", Path.home() / "Palette2048"))

APPLE_SVG = '<svg viewBox="0 0 384 512" aria-hidden="true"><path d="M318.7 268.7c-.2-36.7 16.4-64.4 50-84.8-18.8-26.9-47.2-41.7-84.7-44.6-35.5-2.8-74.3 20.7-88.5 20.7-15 0-49.4-19.7-76.4-19.7C63.3 141.2 4 184.8 4 273.5q0 39.3 14.4 81.2c12.8 36.7 59 126.7 107.2 125.2 25.2-.6 43-17.9 75.8-17.9 31.8 0 48.3 17.9 76.4 17.9 48.6-.7 90.4-82.5 102.6-119.3-65.2-30.7-61.7-90-61.7-91.9zm-56.6-164.2c27.3-32.4 24.8-61.9 24-72.5-24.1 1.4-52 16.4-67.9 34.9-17.5 19.8-27.8 44.3-25.6 71.9 26.1 2 49.9-11.4 69.5-34.3z"/></svg>'


def app_url(ct):
    q = f"?ct={ct}" + (f"&pt={PT}" if PT else "") + "&mt=8"
    return f"https://apps.apple.com/app/id{APP_ID}{q}"


def save(path, text):
    """Write only when content changed (keeps sitemap lastmod stable)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists() or path.read_text(encoding="utf-8") != text:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def ver(path):
    return hashlib.sha1(path.read_bytes()).hexdigest()[:8]


def obf(s):
    raw = s.encode("utf-8")
    return base64.b64encode(bytes(b ^ OBF_KEY[i % len(OBF_KEY)] for i, b in enumerate(raw))).decode("ascii")


def ld(obj):
    return ('<script type="application/ld+json">'
            + json.dumps(obj, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
            + "</script>")


# ─── Color math (Python mirror of core.js / ThemeManager.swift) ───────────────
def _inv(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _gam(c):
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


def rgb_to_lab(rgb):
    r, g, b = (_inv(v / 255) for v in rgb)
    X = (0.4124564 * r + 0.3575761 * g + 0.1804375 * b) / 0.95047
    Y = 0.2126729 * r + 0.7151522 * g + 0.0721750 * b
    Z = (0.0193339 * r + 0.1191920 * g + 0.9503041 * b) / 1.08883
    f = lambda t: t ** (1 / 3) if t > 0.008856 else (903.3 * t + 16) / 116
    fx, fy, fz = f(X), f(Y), f(Z)
    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))


def lab_to_hex(c):
    L, a, b = c
    fy = (L + 16) / 116
    fx, fz = a / 500 + fy, fy - b / 200
    xr = fx ** 3 if fx ** 3 > 0.008856 else (116 * fx - 16) / 903.3
    yr = ((L + 16) / 116) ** 3 if L > 903.3 * 0.008856 else L / 903.3
    zr = fz ** 3 if fz ** 3 > 0.008856 else (116 * fz - 16) / 903.3
    X, Y, Z = xr * 0.95047, yr, zr * 1.08883
    rgb = (3.2404542 * X - 1.5371385 * Y - 0.4985314 * Z,
           -0.9692660 * X + 1.8760108 * Y + 0.0415560 * Z,
           0.0556434 * X - 0.2040259 * Y + 1.0572252 * Z)
    return "#" + "".join(f"{int(math.floor(min(1, max(0, _gam(v))) * 255 + 0.5)):02X}" for v in rgb)


def de(p, q):
    return math.dist(p, q)


def hue_locked(fr, to, t):
    cf, ct = math.hypot(fr[1], fr[2]), math.hypot(to[1], to[2])
    hf, ht = math.atan2(fr[2], fr[1]), math.atan2(to[2], to[1])
    if cf < 3:
        hf = ht
    if ct < 3:
        ht = hf
    h = hf if t < 0.5 else ht
    c = cf + (ct - cf) * t
    return (fr[0] + (to[0] - fr[0]) * t, c * math.cos(h), c * math.sin(h))


def anchor_levels(stops, exposure=11):
    n = len(stops)
    segs = [max(de(stops[i], stops[i + 1]), 1e-6) for i in range(n - 1)]
    total = sum(segs)
    pos = [1.0]
    for s in segs:
        pos.append(pos[-1] + s / total * (exposure - 1))
    lv = [int(math.floor(p + 0.5)) for p in pos]
    lv[0] = 1
    for i in range(1, n):
        if lv[i] <= lv[i - 1]:
            lv[i] = lv[i - 1] + 1
    lv[-1] = exposure
    for i in range(n - 2, -1, -1):
        if lv[i] >= lv[i + 1]:
            lv[i] = lv[i + 1] - 1
    return lv


CAPS = [(0, 78), (25, 80), (55, 90), (85, 95), (110, 88), (140, 75),
        (180, 62), (220, 55), (260, 55), (300, 65), (330, 72), (360, 78)]


def tame(c):
    L, a, b = c
    ch = math.hypot(a, b)
    if ch <= 0:
        return c
    h = math.degrees(math.atan2(b, a)) % 360
    base = CAPS[0][1]
    for (h0, c0), (h1, c1) in zip(CAPS, CAPS[1:]):
        if h0 <= h <= h1:
            base = c0 + (c1 - c0) * (h - h0) / (h1 - h0)
            break
    mx = base * (1.0 if L <= 60 else max(0.8, 1 - (L - 60) * 0.005))
    if ch <= mx:
        return c
    return (L, a * mx / ch, b * mx / ch)


def tile_ramp(stops):
    """Hex colors of the 2 … 2048 tiles (levels 1–11) on the 4×4 board."""
    lv = anchor_levels(stops)
    out = []
    for level in range(1, 12):
        if level <= lv[0]:
            c = stops[0]
        else:
            for i in range(len(lv) - 1):
                if level <= lv[i + 1]:
                    span = lv[i + 1] - lv[i]
                    c = hue_locked(stops[i], stops[i + 1], (level - lv[i]) / span if span else 1)
                    break
        out.append(lab_to_hex(tame(c)))
    return out, lv


COLOR_NAMES = {
    "black": "#141414", "charcoal": "#36454F", "slate gray": "#708090", "gray": "#8A8A8A",
    "silver gray": "#BFC1C2", "ivory": "#F6F1DE", "cream": "#EEE3C0", "off-white": "#F4F4EF",
    "navy": "#1B2A4A", "midnight blue": "#191A4A", "cobalt blue": "#0047AB", "ultramarine": "#3F4FA0",
    "sky blue": "#87BEDF", "powder blue": "#B0D5E0", "teal": "#1F7A78", "turquoise": "#40C0B0",
    "sea green": "#2E8B57", "forest green": "#2A6B2F", "olive": "#6B6B2A", "sage": "#9CAF88",
    "moss green": "#8A9A5B", "emerald": "#3AA870", "dark green": "#1E3B25", "yellow": "#F2D22E",
    "pale yellow": "#F5E9A0", "gold": "#C9A227", "ochre": "#C4822E", "mustard": "#D8A93A",
    "orange": "#EE8A2A", "burnt orange": "#C0561A", "terracotta": "#C66B4B", "rust": "#8B3A1F",
    "brown": "#6B4226", "dark umber": "#3E2A1E", "sienna": "#A0522D", "tan": "#D2B48C",
    "beige": "#E3D5B8", "sand": "#CDB78E", "peach": "#F4C0A0", "salmon": "#E9967A",
    "coral": "#EF6F5C", "red": "#C62828", "crimson": "#9E1B32", "vermilion": "#E34234",
    "burgundy": "#6D1A2A", "maroon": "#4A1520", "pink": "#E8A0B4", "dusty rose": "#C08081",
    "magenta": "#B03A7A", "plum": "#6E3B5E", "purple": "#6A3D9A", "lavender": "#B7A6D6",
    "violet": "#7F4FA0", "indigo": "#302A66", "dusty blue": "#6C8BA8", "steel blue": "#4682B4",
    "blue gray": "#5E7384", "khaki": "#B4A56E", "skin tone": "#DDB08E", "deep blue": "#16306E",
}
_NAME_LABS = [(n, rgb_to_lab(tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)))) for n, h in COLOR_NAMES.items()]


def color_name(lab):
    return min(_NAME_LABS, key=lambda nl: de(lab, nl[1]))[0]


ERA = {"1850-1900": "the second half of the 19th century", "1900-1945": "the early 20th century",
       "1700-1850": "the 18th and early 19th centuries", "1500-1700": "the 16th and 17th centuries",
       "1945-2000": "the postwar decades", "pre-1500": "the centuries before 1500", "modern": "the modern era"}
REGION = {"europe-west": "Western European", "europe-north": "Northern European", "europe-south": "Southern European",
          "americas-north": "North American", "japan": "Japanese", "europe-east": "Eastern European",
          "china": "Chinese", "americas-latin": "Latin American", "korea": "Korean", "south-asia": "South Asian",
          "middle-east": "Middle Eastern", "africa": "African", "oceania": "Oceanian",
          "southeast-asia": "Southeast Asian", "france": "French"}


# ─── Data ─────────────────────────────────────────────────────────────────────
def load_app_data():
    spec = importlib.util.spec_from_file_location("generate_swift", REPO / "tools" / "generate_swift.py")
    gs = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gs)                      # only defines constants/functions
    paintings = json.loads((REPO / "tools" / "paintings.json").read_text())["paintings"]
    schedule = json.loads((REPO / "tools" / "schedule.json").read_text())["schedule"]
    emitted = gs.load_emitted_schedule()             # dates ≤ SCHEDULE_CUTOFF (what the app ships)
    ids = set(emitted.values())
    app_all = [p for p in paintings if p["id"] in ids]   # == CuratedPaletteStore.all
    return paintings, schedule, emitted, app_all, gs.SCHEDULE_CUTOFF


def hexs(rgb):
    return "".join(f"{v:02X}" for v in rgb)


ANCHORS = ("startRGB", "midRGB", "endRGB", "highlightRGB", "accent1RGB", "accent2RGB")


def row(p):
    return [p["id"], obf(p["name"]), obf(p["artist"]), p["year"],
            " ".join(hexs(p[k]) for k in ANCHORS), hexs(p["bgColorRGB"]) if p.get("bgColorRGB") else ""]


def build_data(emitted, app_all, cutoff, today):
    by_id = {p["id"]: p for p in app_all}
    start = (today - dt.timedelta(days=2)).isoformat()
    days = {k: row(by_id[v]) for k, v in sorted(emitted.items()) if k >= start}
    daily = {"v": 1, "epoch": EPOCH, "end": max(emitted), "count": len(app_all), "days": days}
    allj = {"v": 1, "end": max(emitted), "rows": [row(p) for p in app_all]}
    dump = lambda o: json.dumps(o, ensure_ascii=False, separators=(",", ":")) + "\n"
    save(HERE / "daily.json", dump(daily))
    save(HERE / "all.json", dump(allj))
    return len(days)


# ─── Play page (en / ko / ja) ────────────────────────────────────────────────
PLAY_LOCALES = [("en", "", "English"), ("ko", "ko/", "한국어"), ("ja", "ja/", "日本語")]
LANDING = {"en": "/palette2048/", "ko": "/palette2048/ko.html", "ja": "/palette2048/ja.html"}

T = {
"en": dict(
 title="Palette Daily — Free Art Color Puzzle (2048 with Colors)",
 desc="Play today's daily color puzzle in your browser: a 2048 color game painted with a famous painting's color palette. Free, no sign-up, one art puzzle a day.",
 ogt="Palette Daily — today's art color puzzle",
 h1="Daily art color puzzle", loading="Loading today's painting…",
 noscript="Palette needs JavaScript to play. You can still read how it works below.",
 badge="Get the app",
 ui=dict(today="Today's painting", mystery="Mystery Saturday", mysteryNote="The title is revealed when you finish.",
   score="Score", best="Best tile", hint="Swipe or use the arrow keys — merge matching colors",
   won="You reached the 2048 color!", finish="Finish & share", keep="Keep going", over="No more moves",
   result="Today's result", share="Share result", copied="Copied — paste it anywhere",
   shareFail="Couldn't copy. Select the text and copy it.", appLine="Past masterpieces archive · 3×3 & 5×5 boards · unlimited play — in the app",
   appBtn="Download on the App Store", next="Next painting in", loadErr="Couldn't load today's puzzle. Please reload.",
   boardLabel="Puzzle board. Use arrow keys or swipe to move tiles.", shareScore="Score", done="Played today"),
 how_t="How to play", how=[
   "Swipe on the board — or press the arrow keys or W A S D — to slide every tile.",
   "Two tiles of the same color merge into the next color of today's painting palette.",
   "Every move adds a new tile. Tiles have no numbers: read the board by color alone.",
   "When no move is left, the game ends. Share your board and come back tomorrow for a new masterpiece."],
 faq_t="FAQ", faq=[
   ("What is Palette?", "Palette is a daily art puzzle: a 2048-style color game where the board is painted with the palette of a real masterpiece. Instead of numbers, tiles show colors — merge two tiles of the same color and they turn into the next color of the painting's palette."),
   ("Is it free?", "Yes. Today's puzzle is free to play in your browser with no sign-up and no ads. The Palette app for iPhone and iPad is also free to download."),
   ("How is it different from 2048?", "The rules are the same as 2048 — slide the tiles, merge equal pairs, aim for the 2048 tile — but there are no numbers. You follow the painting's color palette from its darkest shade to its lightest, so every day's board looks and plays differently."),
   ("When is there a new puzzle?", "A new painting and color palette arrive every day at midnight in your time zone. The web version has one game per day. On Saturdays the painting's title stays hidden until you finish."),
   ("What does the app add?", "The app adds the archive of past masterpieces, 3×3 and 5×5 boards, unlimited replays, one-step undo and the Saturday mystery quiz, where you guess the painting from its colors."),
 ],
 more_t="Explore", more_pal="Browse painting color palettes", more_land="About the Palette app",
 foot_c="Contact", foot_p="Privacy", foot_t="Terms"),
"ko": dict(
 title="Palette 데일리 — 명화 색으로 푸는 무료 컬러 퍼즐 (색깔 2048)",
 desc="브라우저에서 바로 하는 오늘의 명화 컬러 퍼즐. 숫자 대신 명화 팔레트의 색으로 합치는 2048 색깔 게임을 하루 한 판 무료로, 가입 없이 즐기세요.",
 ogt="Palette 데일리 — 오늘의 명화 컬러 퍼즐",
 h1="매일 한 판, 명화 컬러 퍼즐", loading="오늘의 명화를 불러오는 중…",
 noscript="Palette를 플레이하려면 JavaScript가 필요합니다. 아래에서 방법은 읽어볼 수 있어요.",
 badge="앱 받기",
 ui=dict(today="오늘의 명화", mystery="미스터리 토요일", mysteryNote="작품명은 게임이 끝나면 공개돼요.",
   score="점수", best="최고 타일", hint="스와이프나 방향키로 밀어 같은 색을 합치세요",
   won="2048 색에 도달했어요!", finish="여기서 끝내고 공유", keep="계속하기", over="더 이상 움직일 수 없어요",
   result="오늘의 결과", share="결과 공유", copied="복사했어요 — 원하는 곳에 붙여넣기",
   shareFail="복사하지 못했어요. 텍스트를 직접 복사해 주세요.", appLine="지난 명화 아카이브 · 3×3/5×5 · 무제한 플레이는 앱에서",
   appBtn="App Store에서 다운로드", next="다음 명화까지", loadErr="오늘의 퍼즐을 불러오지 못했어요. 새로고침해 주세요.",
   boardLabel="퍼즐 보드. 방향키나 스와이프로 타일을 움직이세요.", shareScore="점수", done="오늘 완료"),
 how_t="플레이 방법", how=[
   "보드를 스와이프하거나 방향키·W A S D 로 모든 타일을 한쪽으로 밉니다.",
   "같은 색 타일 두 개가 만나면 오늘 명화 팔레트의 다음 색으로 합쳐집니다.",
   "움직일 때마다 새 타일이 하나 생깁니다. 숫자는 없어요 — 색만 보고 판단하세요.",
   "더 움직일 수 없으면 게임이 끝납니다. 결과를 공유하고 내일 새 명화로 다시 만나요."],
 faq_t="자주 묻는 질문", faq=[
   ("Palette는 어떤 게임인가요?", "Palette는 매일 한 점의 실제 명화 팔레트로 보드를 칠하는 2048 방식의 컬러 퍼즐입니다. 타일에는 숫자 대신 색이 있고, 같은 색 두 개를 합치면 그 그림 팔레트의 다음 색이 됩니다."),
   ("무료인가요?", "네. 오늘의 퍼즐은 가입이나 광고 없이 브라우저에서 무료로 플레이할 수 있습니다. 아이폰·아이패드용 Palette 앱도 무료로 받을 수 있어요."),
   ("2048과 무엇이 다른가요?", "규칙은 2048과 같습니다 — 타일을 밀고, 같은 것끼리 합쳐 2048 타일을 노립니다. 다만 숫자가 없고, 그림의 가장 어두운 색에서 가장 밝은 색으로 이어지는 팔레트를 따라가기 때문에 매일 보드의 색과 감각이 달라집니다."),
   ("새 퍼즐은 언제 나오나요?", "매일 사용자 시간대의 자정에 새 명화와 팔레트가 열립니다. 웹에서는 하루 한 판이며, 토요일에는 게임이 끝날 때까지 작품명이 숨겨집니다."),
   ("앱에서는 무엇을 더 할 수 있나요?", "앱에서는 지난 명화 아카이브, 3×3·5×5 보드, 무제한 플레이, 한 수 되돌리기, 색만 보고 작품을 맞히는 토요일 미스터리 퀴즈를 즐길 수 있습니다."),
 ],
 more_t="더 둘러보기", more_pal="명화 컬러 팔레트 모음 (영문)", more_land="Palette 앱 소개",
 foot_c="문의", foot_p="개인정보", foot_t="약관"),
"ja": dict(
 title="Palette デイリー — 名画の色で遊ぶ無料カラーパズル（色の2048）",
 desc="ブラウザですぐ遊べる今日の名画カラーパズル。数字の代わりに名画パレットの色を合わせる2048系の色パズルを、1日1回・無料・登録なしで。",
 ogt="Palette デイリー — 今日の名画カラーパズル",
 h1="毎日1回、名画のカラーパズル", loading="今日の名画を読み込み中…",
 noscript="Palette をプレイするには JavaScript が必要です。遊び方は下で読めます。",
 badge="アプリ",
 ui=dict(today="今日の名画", mystery="ミステリー土曜日", mysteryNote="作品名はゲーム終了後に公開されます。",
   score="スコア", best="最高タイル", hint="スワイプか矢印キーで、同じ色を合わせよう",
   won="2048の色に到達！", finish="ここで終えてシェア", keep="続ける", over="もう動かせません",
   result="今日の結果", share="結果をシェア", copied="コピーしました — 好きな場所に貼り付けて",
   shareFail="コピーできませんでした。テキストを手動でコピーしてください。", appLine="過去の名画アーカイブ · 3×3/5×5 · 無制限プレイはアプリで",
   appBtn="App Storeでダウンロード", next="次の名画まで", loadErr="今日のパズルを読み込めませんでした。再読み込みしてください。",
   boardLabel="パズルボード。矢印キーかスワイプでタイルを動かします。", shareScore="スコア", done="今日はプレイ済み"),
 how_t="遊び方", how=[
   "ボードをスワイプ、または矢印キー・W A S D で、すべてのタイルを滑らせます。",
   "同じ色のタイルが2つぶつかると、今日の名画パレットの次の色になります。",
   "動かすたびに新しいタイルが1つ出ます。数字はありません — 色だけで判断します。",
   "動かせなくなったら終了。結果をシェアして、明日の新しい名画でまた会いましょう。"],
 faq_t="よくある質問", faq=[
   ("Palette とは？", "Palette は、実在の名画のパレットでボードを彩る 2048 風のカラーパズルです。タイルには数字の代わりに色があり、同じ色を2つ合わせると、その絵のパレットの次の色に変わります。"),
   ("無料ですか？", "はい。今日のパズルは登録も広告もなく、ブラウザで無料で遊べます。iPhone・iPad 用の Palette アプリも無料でダウンロードできます。"),
   ("2048 と何が違いますか？", "ルールは 2048 と同じです — タイルを滑らせ、同じもの同士を合わせて 2048 を目指します。ただし数字はなく、絵の最も暗い色から最も明るい色へと続くパレットをたどるので、毎日ボードの色と感覚が変わります。"),
   ("新しいパズルはいつ？", "毎日、お使いのタイムゾーンの午前0時に新しい名画とパレットが公開されます。Web 版は1日1回。土曜日はゲームが終わるまで作品名が隠されます。"),
   ("アプリでは何ができますか？", "アプリでは過去の名画アーカイブ、3×3・5×5 ボード、無制限プレイ、1手戻し、色だけで作品を当てる土曜日のミステリークイズが楽しめます。"),
 ],
 more_t="もっと見る", more_pal="名画のカラーパレット集（英語）", more_land="Palette アプリについて",
 foot_c="お問い合わせ", foot_p="プライバシー", foot_t="規約"),
}


def play_url(code):
    return f"{SITE}/palette2048/play/" + dict((c, p) for c, p, _ in PLAY_LOCALES)[code]


def play_jsonld(code, d):
    url = play_url(code)
    org = {"@type": "Organization", "@id": SITE + "/#organization", "name": "kkiruk studio", "url": SITE + "/"}
    app_node = {"@type": "MobileApplication", "@id": SITE + f"/#app-{APP_ID}", "name": APP_NAME,
                "operatingSystem": "iOS", "applicationCategory": "GameApplication",
                "installUrl": f"https://apps.apple.com/app/id{APP_ID}", "url": SITE + "/palette2048/",
                "publisher": {"@id": org["@id"]}}
    game = {"@type": ["VideoGame", "WebApplication"], "@id": url + "#game", "name": "Palette Daily",
            "alternateName": "Palette — daily art color puzzle", "url": url, "description": d["desc"],
            "inLanguage": code, "applicationCategory": "Game", "operatingSystem": "Any",
            "browserRequirements": "Requires JavaScript", "gamePlatform": "Web browser",
            "genre": ["Puzzle", "Color puzzle"], "playMode": "SinglePlayer", "isAccessibleForFree": True,
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
            "image": OG_IMAGE, "publisher": {"@id": org["@id"]}, "author": {"@id": org["@id"]},
            "isBasedOn": {"@id": app_node["@id"]},
            "keywords": "daily color puzzle, art puzzle game, 2048 color game, painting color palette"}
    page = {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": d["title"], "description": d["desc"],
            "inLanguage": code, "isPartOf": {"@id": SITE + "/#website"}, "mainEntity": {"@id": game["@id"]},
            "publisher": {"@id": org["@id"]}}
    faq = {"@type": "FAQPage", "@id": url + "#faq", "inLanguage": code,
           "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                          for q, a in d["faq"]]}
    site = {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "kkiruk studio",
            "publisher": {"@id": org["@id"]}}
    return ld({"@context": "https://schema.org", "@graph": [org, site, page, game, app_node, faq]})


PLAY_TMPL = """<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{mark}
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
{hreflang}
<meta name="apple-itunes-app" content="app-id={app_id}">
<meta name="theme-color" content="#1b1a1f">
<meta name="color-scheme" content="light dark">
<meta property="og:type" content="website">
<meta property="og:site_name" content="kkiruk studio">
<meta property="og:title" content="{ogt}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og_image}">
<meta property="og:locale" content="{og_locale}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{ogt}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{og_image}">
<link rel="icon" type="image/png" href="/palette2048/icon.png">
<link rel="apple-touch-icon" href="/palette2048/icon-180.png">
<link rel="preload" href="/palette2048/play/daily.json?v={v_data}" as="fetch" crossorigin>
<link rel="stylesheet" href="/palette2048/play/play.css?v={v_css}">
<script src="/ga.js"></script>
{jsonld}
</head>
<body>
<div class="stage" id="stage">
  <header class="top">
    <a class="brand" href="{landing}"><img src="/palette2048/icon.png" alt="" width="24" height="24">Palette</a>
    <span class="daylabel" id="dayLabel"></span>
    <span class="top-end"><a class="badge" href="{app_url}" data-cta="badge" target="_blank" rel="noopener">{apple}{badge}</a></span>
  </header>
  <div class="head">
    <h1 class="kicker" id="kicker">{h1}</h1>
    <p class="pname" id="pname">{loading}</p>
    <p class="pmeta" id="pmeta">&nbsp;</p>
  </div>
  <div class="scorebar" id="scorebar">
    <div class="stat"><span class="lbl" id="scoreLbl">{score}</span><b id="score">0</b></div>
    <div class="stat"><span class="lbl">{best}</span><i class="swatch" id="bestSwatch"></i></div>
  </div>
  <div class="board" id="board" role="application" aria-label="{board_label}" tabindex="0">
    <div class="cells">{cells}</div>
    <div class="tiles" id="tiles"></div>
    <div class="overlay" id="winOverlay" hidden>
      <p id="winText"></p>
      <button type="button" class="btn primary" id="finishBtn"></button>
      <button type="button" class="btn ghost" id="keepBtn"></button>
    </div>
  </div>
  <p class="hint" id="hint">{hint}</p>
  <section class="result" id="result" hidden aria-live="polite">
    <div class="r-row">
      <div class="stat"><span class="lbl">{score}</span><b id="rScore">0</b></div>
      <div class="stat"><span class="lbl">{best}</span><i class="swatch" id="rBest"></i></div>
    </div>
    <button type="button" class="btn primary share" id="shareBtn">{share}</button>
    <p class="toast" id="toast" role="status"></p>
    <div class="r-app">
      <p>{app_line}</p>
      <a class="btn store" href="{app_url}" data-cta="result" target="_blank" rel="noopener">{apple}{app_btn}</a>
    </div>
    <p class="r-next">{next} <b id="countdown">--:--:--</b></p>
  </section>
  <noscript><p class="hint">{noscript}</p></noscript>
</div>

<main class="info">
  <section>
    <h2>{how_t}</h2>
    <ol class="how">{how}</ol>
  </section>
  <section>
    <h2>{faq_t}</h2>
    <div class="faq">{faq}</div>
  </section>
  <section>
    <h2>{more_t}</h2>
    <ul class="more">
      <li><a href="/palette2048/palettes/">{more_pal}</a></li>
      <li><a href="{landing}">{more_land}</a></li>
      <li><a href="{app_url}" data-cta="info" target="_blank" rel="noopener">{app_name} — App Store</a></li>
    </ul>
  </section>
</main>
<footer class="foot">
  <a href="/">© kkiruk studio</a>
  <nav>
    <a href="mailto:kkirukstudio.help@gmail.com">{foot_c}</a>
    <a href="/legal/privacy/">{foot_p}</a>
    <a href="/legal/terms/">{foot_t}</a>
{langs}
  </nav>
</footer>
<script id="i18n" type="application/json">{ui}</script>
<script src="/palette2048/play/core.js?v={v_core}"></script>
<script src="/palette2048/play/play.js?v={v_js}"></script>
</body>
</html>
"""


def build_play():
    hreflang = "\n".join(f'<link rel="alternate" hreflang="{c}" href="{play_url(c)}">' for c, _, _ in PLAY_LOCALES)
    hreflang += f'\n<link rel="alternate" hreflang="x-default" href="{play_url("en")}">'
    versions = dict(v_css=ver(HERE / "play.css"), v_js=ver(HERE / "play.js"),
                    v_core=ver(HERE / "core.js"), v_data=ver(HERE / "daily.json"))
    for code, sub, _ in PLAY_LOCALES:
        d = T[code]
        ui = dict(d["ui"], appUrl=app_url(CT_PLAY))
        langs = "\n".join(f'    <a href="/palette2048/play/{p}" hreflang="{c}" lang="{c}">{n}</a>'
                          for c, p, n in PLAY_LOCALES if c != code)
        html = PLAY_TMPL.format(
            lang=code, mark=BUILD_MARK, title=escape(d["title"]), desc=escape(d["desc"]), url=play_url(code),
            hreflang=hreflang, app_id=APP_ID, ogt=escape(d["ogt"]), og_image=OG_IMAGE,
            og_locale={"en": "en_US", "ko": "ko_KR", "ja": "ja_JP"}[code],
            jsonld=play_jsonld(code, d), landing=LANDING[code], app_url=escape(app_url(CT_PLAY)),
            apple=APPLE_SVG, badge=d["badge"], h1=escape(d["h1"]), loading=escape(d["loading"]),
            score=d["ui"]["score"], best=d["ui"]["best"], board_label=escape(d["ui"]["boardLabel"]),
            cells="<i></i>" * 16, hint=escape(d["ui"]["hint"]), share=d["ui"]["share"],
            app_line=escape(d["ui"]["appLine"]), app_btn=d["ui"]["appBtn"], next=d["ui"]["next"],
            noscript=escape(d["noscript"]), how_t=d["how_t"], faq_t=d["faq_t"], more_t=d["more_t"],
            how="".join(f"<li>{escape(s)}</li>" for s in d["how"]),
            faq="".join(f"<details><summary><h3>{escape(q)}</h3></summary><p>{escape(a)}</p></details>"
                        for q, a in d["faq"]),
            more_pal=d["more_pal"], more_land=d["more_land"], app_name=APP_NAME,
            foot_c=d["foot_c"], foot_p=d["foot_p"], foot_t=d["foot_t"], langs=langs,
            ui=json.dumps(ui, ensure_ascii=False).replace("</", "<\\/"), **versions)
        save(HERE / sub / "index.html", html)


# ─── Palette pages (English) ─────────────────────────────────────────────────
def fmt_date(iso):
    d = dt.date.fromisoformat(iso)
    return f"{d.strftime('%B')} {d.day}, {d.year}"


def palette_info(p):
    anchors = [(tuple(p[k]), rgb_to_lab(p[k])) for k in ANCHORS]
    anchors.sort(key=lambda x: x[1][0])                  # dark → light, like the game
    stops = [lab for _, lab in anchors]
    ramp, levels = tile_ramp(stops)
    return anchors, stops, ramp, levels


def describe(p, date, anchors, stops, levels):
    names = [color_name(lab) for _, lab in anchors]
    uniq = list(dict.fromkeys(names))
    hexes = ["#" + hexs(rgb) for rgb, _ in anchors]
    tags = p.get("tags", {})
    era, region = ERA.get(tags.get("era")), REGION.get(tags.get("region"))
    by = f"{p['name']} is a painting by {p['artist']}" + (f", dated {p['year']}" if p["year"] else "") + "."
    ctx = ""
    if era and region:
        ctx = f" It comes from {region} art of {era}."
    elif era:
        ctx = f" It dates from {era}."
    span = stops[-1][0] - stops[0][0]
    chroma = sum(math.hypot(l[1], l[2]) for l in stops) / len(stops)
    warm = sum(1 for l in stops if math.hypot(l[1], l[2]) > 8 and (-60 < math.degrees(math.atan2(l[2], l[1])) < 100))
    cool = sum(1 for l in stops if math.hypot(l[1], l[2]) > 8 and not (-60 < math.degrees(math.atan2(l[2], l[1])) < 100))
    contrast = ("a high-contrast palette" if span > 65 else "a palette with moderate contrast" if span > 40
                else "a close-valued, low-contrast palette")
    sat = "rich, saturated" if chroma > 40 else "muted" if chroma < 20 else "balanced"
    temp = ("mostly warm" if warm >= cool + 2 else "mostly cool" if cool >= warm + 2 else "a mix of warm and cool")
    middle = ", ".join(uniq[1:-1]) if len(uniq) > 2 else ""
    pal = (f"Its six colors run from {names[0]} ({hexes[0]}) up to {names[-1]} ({hexes[-1]})"
           + (f", passing through {middle}" if middle else "") + f". It is {contrast} with {sat} tones, {temp}"
           + f" (lightness {stops[0][0]:.0f} to {stops[-1][0]:.0f} in CIE Lab).")
    tiles = [2 ** lv for lv in levels]
    game = (f"Palette used this painting for the daily puzzle of {fmt_date(date)}. The tiles show no numbers: "
            f"the smallest tile is {names[0]}, and each merge steps along the palette. The six colors land exactly on "
            f"the {', '.join(str(t) for t in tiles[:-1])} and {tiles[-1]} tiles, with blended shades in between, "
            f"so the {tiles[-1]} tile is {names[-1]}.")
    return by + ctx, pal, game


PAL_HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{mark}
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="apple-itunes-app" content="app-id={app_id}">
<meta name="color-scheme" content="light dark">
<meta property="og:type" content="article">
<meta property="og:site_name" content="kkiruk studio">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{og_image}">
<link rel="icon" type="image/png" href="/palette2048/icon.png">
<link rel="apple-touch-icon" href="/palette2048/icon-180.png">
<link rel="stylesheet" href="/palette2048/palettes/palettes.css?v={v_css}">
<script src="/ga.js"></script>
{jsonld}
</head>
<body>
<header class="bar">
  <a class="brand" href="/palette2048/"><img src="/palette2048/icon.png" alt="" width="24" height="24">Palette</a>
  <nav><a href="/palette2048/palettes/">Palettes</a><a class="play" href="/palette2048/play/">Play today</a></nav>
</header>
<main class="wrap">
"""

PAL_FOOT = """</main>
<footer class="foot">
  <a href="/">© kkiruk studio</a>
  <nav><a href="/palette2048/">Palette app</a><a href="/palette2048/play/">Daily puzzle</a><a href="/legal/privacy/">Privacy</a><a href="/legal/terms/">Terms</a></nav>
</footer>
{script}</body>
</html>
"""


def crumbs(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}


def related_for(p, published):
    tags = p.get("tags", {})
    others = [q for q in published if q["id"] != p["id"]]
    tiers = [
        lambda q: q["artist"] == p["artist"],
        lambda q: q["tags"].get("era") == tags.get("era") and q["tags"].get("region") == tags.get("region"),
        lambda q: q["tags"].get("era") == tags.get("era"),
        lambda q: q["tags"].get("region") == tags.get("region"),
        lambda q: True,
    ]
    out = []
    for tier in tiers:
        # deterministic order: nearest schedule date first
        for q in sorted((q for q in others if tier(q) and q not in out),
                        key=lambda q: (abs(dt.date.fromisoformat(q["_date"]).toordinal()
                                           - dt.date.fromisoformat(p["_date"]).toordinal()), q["id"])):
            out.append(q)
            if len(out) == 6:
                return out
    return out


def strip(p, cls="strip"):
    return f'<span class="{cls}" aria-hidden="true">' + "".join(
        f'<i style="background:#{hexs(rgb)}"></i>' for rgb, _ in palette_info(p)[0]) + "</span>"


def build_palette_pages(paintings, schedule, today):
    first = {}
    for k, v in sorted(schedule.items()):
        first.setdefault(v, k)
    published = []
    for p in paintings:
        date = first.get(p["id"])
        if date and date < today.isoformat():
            published.append(dict(p, _date=date))
    v_css = ver(PAL_DIR / "palettes.css")
    v_js = ver(PAL_DIR / "palettes.js")
    idx_url = f"{SITE}/palette2048/palettes/"
    for p in published:
        anchors, stops, ramp, levels = palette_info(p)
        url = f"{idx_url}{p['id']}/"
        who = f"{p['artist']}" + (f" ({p['year']})" if p["year"] else "")
        h1 = f"{p['name']} Color Palette — {who}"
        title = f"{p['name']} Color Palette — {p['artist']} | HEX & RGB codes"
        names = list(dict.fromkeys(color_name(lab) for _, lab in anchors))
        desc = (f"The {p['name']} color palette by {p['artist']}: 6 colors with HEX and RGB codes "
                f"({', '.join(names[:4])}), and how the painting plays as a daily color puzzle.")
        s_by, s_pal, s_game = describe(p, p["_date"], anchors, stops, levels)
        painting = {"@type": "Painting", "name": p["name"], "creator": {"@type": "Person", "name": p["artist"]},
                    "url": p["url"]}
        if p["year"]:
            painting["dateCreated"] = p["year"]
        work = {"@type": "CreativeWork", "@id": url + "#palette", "name": f"{p['name']} color palette",
                "url": url, "description": desc, "inLanguage": "en", "about": painting,
                "keywords": "painting color palette, " + ", ".join(names),
                "publisher": {"@type": "Organization", "name": "kkiruk studio", "url": SITE + "/"},
                "isPartOf": {"@type": "CollectionPage", "@id": idx_url, "name": "Painting color palettes"}}
        bc = crumbs([("kkiruk studio", SITE + "/"), ("Palette", SITE + "/palette2048/"),
                     ("Painting color palettes", idx_url), (p["name"], url)])
        swatches = "".join(
            f'<li class="sw"><span class="chip" style="background:#{hexs(rgb)}"></span>'
            f'<span class="nm">{escape(color_name(lab))}</span>'
            f'<button type="button" class="copy" data-copy="#{hexs(rgb)}">#{hexs(rgb)}</button>'
            f'<button type="button" class="copy" data-copy="rgb({rgb[0]}, {rgb[1]}, {rgb[2]})">rgb({rgb[0]}, {rgb[1]}, {rgb[2]})</button></li>'
            for rgb, lab in anchors)
        all_hex = " ".join("#" + hexs(rgb) for rgb, _ in anchors)
        ramp_html = "".join(f'<li style="background:{h}"><span>{2 ** (i + 1)}</span></li>' for i, h in enumerate(ramp))
        rel = "".join(f'<li><a href="../{q["id"]}/">{strip(q)}<span>{escape(q["name"])}</span>'
                      f'<small>{escape(q["artist"])}</small></a></li>' for q in related_for(p, published))
        body = f"""<nav class="crumbs" aria-label="Breadcrumb"><a href="/palette2048/">Palette</a> › <a href="/palette2048/palettes/">Painting color palettes</a> › <span>{escape(p['name'])}</span></nav>
<h1>{escape(h1)}</h1>
<ul class="swatches">{swatches}</ul>
<p class="copyall"><button type="button" class="copy" data-copy="{all_hex}">Copy all HEX codes</button></p>
<section class="about">
<h2>About this palette</h2>
<p>{escape(s_by)}</p>
<p>{escape(s_pal)}</p>
<p><a href="{escape(p['url'])}" target="_blank" rel="noopener">See the original painting ↗</a></p>
</section>
<section>
<h2>How it plays in the puzzle</h2>
<p>{escape(s_game)}</p>
<ol class="ramp" aria-label="Tile colors from 2 to 2048">{ramp_html}</ol>
<div class="cta">
<a class="btn store" href="{escape(app_url(CT_PALETTE))}" data-cta="palette" target="_blank" rel="noopener">{APPLE_SVG}Play this palette in the app</a>
<a class="btn ghost" href="/palette2048/play/">Play today's free puzzle →</a>
</div>
</section>
<section>
<h2>Related painting palettes</h2>
<ul class="related">{rel}</ul>
<p><a href="/palette2048/palettes/">All painting color palettes</a></p>
</section>
"""
        html = (PAL_HEAD.format(mark=BUILD_MARK, title=escape(title), desc=escape(desc), url=url, app_id=APP_ID,
                                og_image=OG_IMAGE, v_css=v_css, jsonld=ld({"@context": "https://schema.org",
                                                                           "@graph": [work, bc]}))
                + body + PAL_FOOT.format(script=f'<script src="/palette2048/palettes/palettes.js?v={v_js}"></script>\n'))
        save(PAL_DIR / p["id"] / "index.html", html)

    # remove generated pages that are no longer published (e.g. schedule edits)
    keep = {p["id"] for p in published}
    for d in PAL_DIR.iterdir():
        f = d / "index.html"
        if d.is_dir() and d.name not in keep and f.exists() and BUILD_MARK in f.read_text(encoding="utf-8"):
            shutil.rmtree(d)

    # index — grouped by artist
    groups = {}
    for p in published:
        groups.setdefault(p["artist"], []).append(p)
    order = sorted(groups, key=lambda a: a.lower())
    blocks = []
    for a in order:
        items = "".join(f'<li><a href="{q["id"]}/">{strip(q)}<span>{escape(q["name"])}</span>'
                        + (f'<small>{escape(q["year"])}</small>' if q["year"] else "") + "</a></li>"
                        for q in sorted(groups[a], key=lambda q: q["name"]))
        blocks.append(f'<section class="artist"><h2>{escape(a)}</h2><ul class="related">{items}</ul></section>')
    title = "Painting Color Palettes — HEX Codes from Famous Artworks | Palette"
    desc = (f"{len(published)} color palettes taken from famous paintings, grouped by artist, each with HEX and RGB "
            "codes. Every palette was a daily color puzzle in the Palette art puzzle game.")
    coll = {"@type": "CollectionPage", "@id": idx_url, "url": idx_url, "name": "Painting color palettes",
            "description": desc, "inLanguage": "en",
            "publisher": {"@type": "Organization", "name": "kkiruk studio", "url": SITE + "/"},
            "mainEntity": {"@type": "ItemList", "numberOfItems": len(published)}}
    bc = crumbs([("kkiruk studio", SITE + "/"), ("Palette", SITE + "/palette2048/"),
                 ("Painting color palettes", idx_url)])
    body = f"""<nav class="crumbs" aria-label="Breadcrumb"><a href="/palette2048/">Palette</a> › <span>Painting color palettes</span></nav>
<h1>Painting Color Palettes</h1>
<p class="lede">Six-color palettes taken from {len(published)} famous paintings, with HEX and RGB codes. Each one was the board of a daily color puzzle in Palette — a 2048-style art puzzle game where tiles show colors instead of numbers. A new palette is added here the day after its puzzle.</p>
<div class="cta"><a class="btn ghost" href="/palette2048/play/">Play today's free puzzle →</a>
<a class="btn store" href="{escape(app_url(CT_PALETTE))}" data-cta="palette_index" target="_blank" rel="noopener">{APPLE_SVG}Get the app</a></div>
<p class="artists">{len(order)} artists · {" · ".join(f'<a href="#a{i}">{escape(a)}</a>' for i, a in enumerate(order))}</p>
{"".join(b.replace('<section class="artist">', f'<section class="artist" id="a{i}">', 1) for i, b in enumerate(blocks))}
"""
    html = (PAL_HEAD.format(mark=BUILD_MARK, title=escape(title), desc=escape(desc), url=idx_url, app_id=APP_ID,
                            og_image=OG_IMAGE, v_css=v_css,
                            jsonld=ld({"@context": "https://schema.org", "@graph": [coll, bc]}))
            + body + PAL_FOOT.format(script=f'<script src="/palette2048/palettes/palettes.js?v={v_js}"></script>\n'))
    save(PAL_DIR / "index.html", html)
    return published


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", help="build date YYYY-MM-DD (default: today)")
    ap.add_argument("--no-sitemap", action="store_true")
    args = ap.parse_args()
    today = dt.date.fromisoformat(args.date) if args.date else dt.date.today()
    paintings, schedule, emitted, app_all, cutoff = load_app_data()
    n_days = build_data(emitted, app_all, cutoff, today)
    build_play()
    published = build_palette_pages(paintings, schedule, today)
    print(f"daily.json: {n_days} days (cutoff {cutoff}) · all.json: {len(app_all)} rows")
    print(f"play pages: {len(PLAY_LOCALES)} · palette pages: {len(published)} (+ index)")
    if not args.no_sitemap:
        subprocess.run([sys.executable, str(ROOT / "gen" / "gen_sitemap.py")], check=True)


if __name__ == "__main__":
    main()
