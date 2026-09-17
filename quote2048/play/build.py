#!/usr/bin/env python3
"""Quote 2048 web daily — generator for the browser puzzle and the quote-theme SEO pages.

Outputs (edit this file / play.js / play.css / core.js / ../quotes/quotes.css|js, never the generated HTML):
  quote2048/play/index.html, play/{ko,ja,zh-hans,zh-hant}/index.html   — daily puzzle (5 locales)
  quote2048/play/data/<locale>/<theme-id>.json   — one theme's 17 quotes in one locale (~1–2 KB)
  quote2048/quotes/index.html (+ <locale>/)      — theme index (topics / author packs)
  quote2048/quotes/<theme-id>/index.html (+ <locale>/) — 60 themes × 5 locales
  sitemap.xml                                     — regenerated with gen/gen_sitemap.py

Source of truth is the app repo (read-only): ~/Quote2048/tools/quotes.json (60 themes × 17 quotes × 5
languages). Override the location with QUOTE_REPO=/path.

WEB SCHEDULE: the app has no daily puzzle (it is a theme list), so the web runs its own fixed cycle in
`quote2048/play/web_schedule.json` — every one of the 60 themes once per 60-day cycle, each day paired
with one of the app's 10 board palettes (BoardPalettes.swift). 2026-09-18 = puzzle #1; the cycle then
repeats forever (play.js computes the day from the epoch). The file is created once with
  python3 quote2048/play/build.py --make-web-schedule          # refuses if the file exists
  python3 quote2048/play/build.py --make-web-schedule --force  # reshuffle (changes every future day!)
and every normal build only reads it and embeds it into the play pages.

NO DAILY REBUILD NEEDED: the schedule is embedded in full and every quote page is public from day one
(quotes are not spoilers), so nothing in the output depends on the build date. Re-run only when
quotes.json, the templates or the assets change:
  python3 quote2048/play/build.py
"""
import argparse
import hashlib
import json
import os
import random
import subprocess
import sys
from html import escape
from pathlib import Path

sys.dont_write_bytecode = True

# ─── Constants ────────────────────────────────────────────────────────────────
PT = "118060110"
CT_PLAY = "quote_web_play"
CT_QUOTES = "quote_web_quotes"
APP_ID = "6788598686"
APP_NAME = "Quote 2048"
EPOCH = "2026-09-18"
SITE = "https://www.kkirukstudio.com"
OG_IMAGE = SITE + "/quote2048/assets/icon-512.png"
BUILD_MARK = "<!-- seo:build-owned quote2048/play/build.py -->"
SCHEDULE_SEED = 20260918
BOARD_IDS = ["board-dawn", "board-forest", "board-ocean", "board-ember", "board-lavender",
             "board-desert", "board-inkjade", "board-berry", "board-peacock", "board-charcoal"]

HERE = Path(__file__).resolve().parent            # quote2048/play
Q2048 = HERE.parent                               # quote2048
ROOT = Q2048.parent                               # site root
QDIR = Q2048 / "quotes"
SCHEDULE_FILE = HERE / "web_schedule.json"
REPO = Path(os.environ.get("QUOTE_REPO", Path.home() / "Quote2048"))

# (code, url sub-path, data key in quotes.json, hreflang, og locale, label)
LOCALES = [("en", "", "en", "en", "en_US", "English"),
           ("ko", "ko/", "ko", "ko", "ko_KR", "한국어"),
           ("ja", "ja/", "ja", "ja", "ja_JP", "日本語"),
           ("zh-hans", "zh-hans/", "zh_hans", "zh-Hans", "zh_CN", "简体中文"),
           ("zh-hant", "zh-hant/", "zh_hant", "zh-Hant", "zh_TW", "繁體中文")]
LOC = {c: dict(sub=s, key=k, hl=h, og=o, label=l) for c, s, k, h, o, l in LOCALES}

APPLE_SVG = '<svg viewBox="0 0 384 512" aria-hidden="true"><path d="M318.7 268.7c-.2-36.7 16.4-64.4 50-84.8-18.8-26.9-47.2-41.7-84.7-44.6-35.5-2.8-74.3 20.7-88.5 20.7-15 0-49.4-19.7-76.4-19.7C63.3 141.2 4 184.8 4 273.5q0 39.3 14.4 81.2c12.8 36.7 59 126.7 107.2 125.2 25.2-.6 43-17.9 75.8-17.9 31.8 0 48.3 17.9 76.4 17.9 48.6-.7 90.4-82.5 102.6-119.3-65.2-30.7-61.7-90-61.7-91.9zm-56.6-164.2c27.3-32.4 24.8-61.9 24-72.5-24.1 1.4-52 16.4-67.9 34.9-17.5 19.8-27.8 44.3-25.6 71.9 26.1 2 49.9-11.4 69.5-34.3z"/></svg>'

# Author values that are not a person (no schema.org creator for these).
NOT_PERSON = {"Proverb", "Traditional", "Spartan saying", "German proverb", "Japanese proverb", "Latin proverb",
              "Roman proverb"}
WORKS = {"Huainanzi", "I Ching", "Records of the Three Kingdoms", "The Book of Songs", "The Great Learning",
         "Zengguang Xianwen", "Zuo Zhuan"}


def app_url(ct):
    return f"https://apps.apple.com/app/id{APP_ID}?ct={ct}" + (f"&pt={PT}" if PT else "") + "&mt=8"


def save(path, text):
    """Write only when content changed (keeps sitemap lastmod stable)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists() or path.read_text(encoding="utf-8") != text:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def ver(path):
    return hashlib.sha1(path.read_bytes()).hexdigest()[:8]


def ld(obj):
    return ('<script type="application/ld+json">'
            + json.dumps(obj, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
            + "</script>")


def jdump(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


# ─── Data ─────────────────────────────────────────────────────────────────────
def load_themes():
    themes = json.loads((REPO / "tools" / "quotes.json").read_text(encoding="utf-8"))["themes"]
    themes.sort(key=lambda t: t["order"])
    for t in themes:
        assert len(t["quotes"]) == 17, t["id"]
    return themes


def qtext(q, code):
    return q.get(LOC[code]["key"]) or q["en"]


def qauthor(q, code):
    return q.get("author_" + LOC[code]["key"]) or q["author_en"]


def tname(t, code):
    return t["name"].get(LOC[code]["key"]) or t["name"]["en"]


def make_schedule(themes, force):
    if SCHEDULE_FILE.exists() and not force:
        sys.exit(f"{SCHEDULE_FILE} already exists — refusing to reshuffle (use --force).")
    rng = random.Random(SCHEDULE_SEED)
    topics = [t["id"] for t in themes if t["kind"] == "topic"]
    authors = [t["id"] for t in themes if t["kind"] == "author"]
    rng.shuffle(topics)
    rng.shuffle(authors)
    # Build the cycle as blocks [topic, 1–2 authors]: day #1 is a free topic, topics and author packs
    # alternate, and no kind ever runs three days in a row — also across the cycle wrap.
    extra = len(authors) - len(topics)                  # blocks that carry two authors
    assert 0 <= extra <= len(topics)
    doubles = set(rng.sample(range(len(topics)), extra))
    order, ai = [], 0
    for i, tid in enumerate(topics):
        order.append(tid)
        take = 2 if i in doubles else 1
        order.extend(authors[ai:ai + take])
        ai += take
    assert ai == len(authors) and len(order) == len(themes)
    kind = {t["id"]: t["kind"] for t in themes}
    n = len(order)
    assert not any(kind[order[i]] == kind[order[(i + 1) % n]] == kind[order[(i + 2) % n]] for i in range(n))
    boards = BOARD_IDS[:]
    rng.shuffle(boards)
    days = [[tid, boards[i % len(boards)]] for i, tid in enumerate(order)]
    doc = {"v": 1, "epoch": EPOCH, "cycle": len(days), "seed": SCHEDULE_SEED,
           "note": "Fixed web-only cycle. Day i (0-based from epoch) = days[i % cycle]. Generated once by build.py --make-web-schedule.",
           "days": days}
    SCHEDULE_FILE.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"web_schedule.json: {len(days)} days")


def load_schedule(themes):
    if not SCHEDULE_FILE.exists():
        sys.exit("web_schedule.json missing — run: build.py --make-web-schedule")
    doc = json.loads(SCHEDULE_FILE.read_text(encoding="utf-8"))
    ids = {t["id"] for t in themes}
    got = [d[0] for d in doc["days"]]
    assert sorted(got) == sorted(ids), "web_schedule.json no longer matches quotes.json themes"
    assert all(d[1] in BOARD_IDS for d in doc["days"])
    return {"epoch": doc["epoch"], "days": doc["days"]}


def build_data(themes):
    n = 0
    for t in themes:
        for code in LOC:
            obj = {"id": t["id"], "kind": t["kind"], "pro": 1 if t["premium"] else 0, "name": tname(t, code),
                   "q": [[qtext(q, code), qauthor(q, code)] for q in t["quotes"]]}
            save(HERE / "data" / code / f"{t['id']}.json", json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "\n")
            n += 1
    return n


# ─── Copy ─────────────────────────────────────────────────────────────────────
T = {
"en": dict(
 brand="Quote 2048",
 title="Quote 2048 Daily — Free Quote Puzzle Game (2048 with Quotes)",
 desc="Play today's daily quote puzzle in your browser: classic 2048 where every tile is a famous quote. Merge matching lines to climb to the theme's crown quote. Free, no sign-up, one puzzle a day.",
 ogt="Quote 2048 Daily — today's quote puzzle",
 h1="Daily quote puzzle", loading="Loading today's theme…",
 noscript="Quote 2048 needs JavaScript to play. You can still read how it works below.",
 badge="Get the app",
 ui=dict(today="Today's theme", todayAuthor="Today's author pack", result="Today's result",
   kindTopic="Theme · 17 quotes", kindAuthor="Author pack · 17 quotes", kindPro="Author pack · Pro in the app",
   preview="Preview", score="Score", best="Best tile",
   hint="Swipe or use the arrow keys · tap a tile to read it",
   won="Theme complete!", wonSub="You reached the crown quote.", finish="Finish & share", keep="Keep going",
   share="Share result", saveImg="Save image", copied="Copied — paste it anywhere",
   shareFail="Couldn't copy. Select the text and copy it.",
   appLine="In the app: 60 themes · 36 author packs · 17 levels up to 131072 · make your own quote pack",
   appLinePro="Today's author pack is a Pro pack in the app — keep collecting its quotes there.",
   appBtn="Download on the App Store", next="Next theme in", loadErr="Couldn't load today's puzzle. Please reload.",
   boardLabel="Puzzle board. Use arrow keys or swipe to move tiles. Tap a tile to read its quote.",
   done="Played today", bestQuote="Your best quote", collected="Quotes you collected",
   moreInApp="{n} more quotes up to 131072 continue in the app",
   themePage="All 17 quotes of this theme →", close="Close", tile="Tile", crown="Crown quote",
   cardScore="Score", locked="?"),
 how_t="How to play", how=[
   "Swipe on the board — or press the arrow keys or W A S D — to slide every tile.",
   "Two tiles with the same quote merge into the next, deeper quote of today's theme.",
   "Every move adds a new tile. Tap any tile to read the whole quote and who said it.",
   "Reach the 2048 tile to complete the theme with its crown quote. When no move is left, share your best quote and come back tomorrow."],
 faq_t="FAQ", faq=[
   ("What is Quote 2048?", "Quote 2048 is the classic 2048 puzzle where every tile is a quotation. Each game has one theme — like Courage, Time or Shakespeare — and its 11 tiles from 2 to 2048 climb from a short proverb to the theme's crown quote."),
   ("Is it free?", "Yes. Today's puzzle is free to play in your browser with no sign-up and no ads. The Quote 2048 app for iPhone and iPad is also free to download."),
   ("Where do the quotes come from?", "Every line comes from public-domain writing or traditional proverbs — philosophers, poets and novelists such as Seneca, Laozi, Shakespeare and Emily Dickinson — and each attribution was checked against its source."),
   ("When is there a new puzzle?", "A new theme arrives every day at midnight in your time zone. The web version has one game per day and cycles through all 60 themes and author packs."),
   ("What does the app add?", "The app lets you play any of the 60 themes whenever you like, including 36 author packs, and continue past 2048 up to 131072 — 17 quotes per theme. It also keeps a collection of the quotes you reach and lets you build your own quote pack."),
 ],
 more_t="Explore quotes", more_idx="All quote themes & author packs", more_land="About the Quote 2048 app",
 foot_c="Contact", foot_p="Privacy", foot_t="Terms",
 # quote pages
 q_idx_title="Quotes by Theme and Author — 60 Collections | Quote 2048",
 q_idx_h1="Quotes by theme and author",
 q_idx_desc="60 quote collections — 24 themes such as courage, time and love, and 36 author packs from Shakespeare to Seneca — each with 17 public-domain quotes, authors and original languages.",
 q_idx_lede="Each collection holds 17 quotes, ordered from a short proverb to the crown quote. They are the tiles of Quote 2048, a 2048 puzzle where every tile is a quote.",
 q_topics="Themes", q_authors="Author packs", q_crumb="Quotes",
 q_h1_topic="Quotes about {name} — 17 Timeless Lines", q_h1_author="{name} Quotes — 17 Timeless Lines",
 q_title_topic="{n} Quotes about {name} — Proverbs to Classics | Quote 2048",
 q_title_author="{name} Quotes — 17 Lines from the Original Works | Quote 2048",
 q_desc_topic="17 quotes about {lname} by {who}, from a short proverb to the crown quote — with authors and original languages.",
 q_desc_author="17 quotes by {who}, with original-language text where it exists — the {name} pack in Quote 2048.",
 q_lede_topic="17 quotes about {lname}, arranged the way they appear in Quote 2048: from the lightest line on the 2 tile to the crown quote on the 2048 tile, and on to 131072 in the app.",
 q_lede_author="17 quotes from {name}, arranged the way they appear in Quote 2048: from the lightest line on the 2 tile to the crown quote on the 2048 tile, and on to 131072 in the app.",
 q_pd="All quotes come from public-domain works or traditional proverbs; attributions were checked against their sources.",
 q_orig="Original", q_copy="Copy", q_copied="Copied", q_crown="Crown quote", q_app_only="Levels 4096–131072 continue in the app.",
 q_play_h="Play these quotes as a 2048 puzzle", q_play_p="Merge matching quotes to climb this theme to its crown quote.",
 q_play_app="Play this pack in the app", q_play_web="Play today's free puzzle →",
 q_pro=" (Pro pack in the app)", q_rel="More {kind}", q_rel_topic="themes", q_rel_author="author packs",
 q_all="All quote collections", q_proverb_and="and",
 langs=dict(en="English", zh="Classical Chinese", lzh="Classical Chinese", la="Latin", de="German", fr="French",
            ja="Japanese", grc="Ancient Greek", el="Greek", it="Italian", es="Spanish", ru="Russian")),
"ko": dict(
 brand="명언 2048",
 title="명언 2048 데일리 — 명언으로 푸는 무료 2048 퍼즐",
 desc="브라우저에서 바로 하는 오늘의 명언 퍼즐. 타일마다 명언이 적힌 2048을 하루 한 판, 무료로, 가입 없이. 같은 문장을 합쳐 오늘 테마의 왕관 명언까지 올라가 보세요.",
 ogt="명언 2048 데일리 — 오늘의 명언 퍼즐",
 h1="매일 한 판, 명언 퍼즐", loading="오늘의 테마를 불러오는 중…",
 noscript="명언 2048을 플레이하려면 JavaScript가 필요합니다. 아래에서 방법은 읽어볼 수 있어요.",
 badge="앱 받기",
 ui=dict(today="오늘의 테마", todayAuthor="오늘의 작가 팩", result="오늘의 결과",
   kindTopic="주제 · 명언 17개", kindAuthor="작가 팩 · 명언 17개", kindPro="작가 팩 · 앱에선 Pro",
   preview="미리보기", score="점수", best="최고 타일",
   hint="스와이프나 방향키로 밀기 · 타일을 탭하면 전문",
   won="테마 완성!", wonSub="왕관 명언에 도달했어요.", finish="여기서 끝내고 공유", keep="계속하기",
   share="결과 공유", saveImg="이미지 저장", copied="복사했어요 — 원하는 곳에 붙여넣기",
   shareFail="복사하지 못했어요. 텍스트를 직접 복사해 주세요.",
   appLine="앱에서는 테마 60개 · 작가 팩 36개 · 131072까지 17단계 · 나만의 명언 팩",
   appLinePro="오늘의 작가 팩은 앱의 Pro 팩이에요 — 앱에서 이 작가의 명언을 이어서 모아보세요.",
   appBtn="App Store에서 다운로드", next="다음 테마까지", loadErr="오늘의 퍼즐을 불러오지 못했어요. 새로고침해 주세요.",
   boardLabel="퍼즐 보드. 방향키나 스와이프로 타일을 움직이고, 타일을 탭하면 명언 전문을 볼 수 있어요.",
   done="오늘 완료", bestQuote="오늘 도달한 최고 명언", collected="모은 명언",
   moreInApp="131072까지 {n}개의 명언이 앱에서 이어져요",
   themePage="이 테마의 명언 17개 전체 보기 →", close="닫기", tile="타일", crown="왕관 명언",
   cardScore="점수", locked="?"),
 how_t="플레이 방법", how=[
   "보드를 스와이프하거나 방향키·W A S D 로 모든 타일을 한쪽으로 밉니다.",
   "같은 명언 타일 두 개가 만나면 오늘 테마의 한 단계 위 명언으로 합쳐집니다.",
   "움직일 때마다 새 타일이 하나 생깁니다. 타일을 탭하면 명언 전문과 말한 사람을 볼 수 있어요.",
   "2048 타일을 만들면 왕관 명언으로 테마 완성. 더 움직일 수 없으면 최고 명언을 공유하고 내일 다시 만나요."],
 faq_t="자주 묻는 질문", faq=[
   ("명언 2048은 어떤 게임인가요?", "명언 2048은 타일마다 명언이 적힌 2048 퍼즐입니다. 한 판에 용기·시간·셰익스피어 같은 테마 하나가 정해지고, 2부터 2048까지 11개의 타일이 짧은 속담에서 그 테마의 왕관 명언으로 올라갑니다."),
   ("무료인가요?", "네. 오늘의 퍼즐은 가입이나 광고 없이 브라우저에서 무료로 플레이할 수 있습니다. 아이폰·아이패드용 명언 2048 앱도 무료로 받을 수 있어요."),
   ("명언은 어디에서 가져왔나요?", "모든 문장은 퍼블릭 도메인 저작물이나 전해 내려오는 속담에서 가져왔습니다. 세네카, 노자, 셰익스피어, 에밀리 디킨슨 같은 철학자·시인·작가의 문장이며, 출처와 저자 표기를 원전과 대조해 확인했습니다."),
   ("새 퍼즐은 언제 나오나요?", "매일 사용자 시간대의 자정에 새 테마가 열립니다. 웹에서는 하루 한 판이며, 60개의 테마와 작가 팩을 차례로 돌아갑니다."),
   ("앱에서는 무엇을 더 할 수 있나요?", "앱에서는 작가 팩 36개를 포함한 60개 테마를 언제든 골라 플레이하고, 2048 이후 131072까지 테마마다 17개의 명언을 모을 수 있습니다. 도달한 명언은 도감에 남고, 나만의 명언 팩도 만들 수 있어요."),
 ],
 more_t="명언 둘러보기", more_idx="주제별·작가별 명언 모음 전체", more_land="명언 2048 앱 소개",
 foot_c="문의", foot_p="개인정보", foot_t="약관",
 q_idx_title="주제별·작가별 명언 모음 60선 | 명언 2048",
 q_idx_h1="주제별·작가별 명언 모음",
 q_idx_desc="용기·시간·사랑 같은 주제 24개와 셰익스피어부터 세네카까지 작가 팩 36개, 모두 60개의 명언 모음. 모음마다 퍼블릭 도메인 명언 17개와 저자·원문을 함께 실었습니다.",
 q_idx_lede="모음마다 명언 17개를 짧은 속담부터 왕관 명언 순으로 담았습니다. 타일마다 명언이 적힌 2048 퍼즐, 명언 2048의 타일 그대로입니다.",
 q_topics="주제", q_authors="작가 팩", q_crumb="명언 모음",
 q_h1_topic="{name}에 관한 명언 17선", q_h1_author="{name} 명언 17선",
 q_title_topic="{name}에 관한 명언 17선 — 속담부터 고전까지 | 명언 2048",
 q_title_author="{name} 명언 17선 — 원전에서 가려 뽑은 문장 | 명언 2048",
 q_desc_topic="{who}의 {name}에 관한 명언 17개. 짧은 속담부터 왕관 명언까지 저자와 원문을 함께 소개합니다.",
 q_desc_author="{who}의 명언 17개를 원문과 함께 모았습니다. 명언 2048의 「{name}」 팩 수록 문장.",
 q_lede_topic="{name}에 관한 명언 17개를 명언 2048에 나오는 순서대로 모았습니다. 2 타일의 가벼운 문장에서 2048 타일의 왕관 명언까지, 그리고 앱에서는 131072까지 이어집니다.",
 q_lede_author="{name}의 명언 17개를 명언 2048에 나오는 순서대로 모았습니다. 2 타일의 가벼운 문장에서 2048 타일의 왕관 명언까지, 그리고 앱에서는 131072까지 이어집니다.",
 q_pd="모든 명언은 퍼블릭 도메인 저작물이나 전해 내려오는 속담에서 가져왔고, 저자 표기는 원전과 대조해 확인했습니다.",
 q_orig="원문", q_copy="복사", q_copied="복사됨", q_crown="왕관 명언", q_app_only="4096~131072 단계는 앱에서 이어집니다.",
 q_play_h="이 명언들로 2048 하기", q_play_p="같은 명언을 합쳐 이 테마의 왕관 명언까지 올라가 보세요.",
 q_play_app="앱에서 이 팩 플레이", q_play_web="오늘의 무료 퍼즐 하기 →",
 q_pro=" (앱에선 Pro 팩)", q_rel="다른 {kind}", q_rel_topic="주제", q_rel_author="작가 팩",
 q_all="명언 모음 전체 보기", q_proverb_and="외",
 langs=dict(en="영어", zh="한문", lzh="한문", la="라틴어", de="독일어", fr="프랑스어", ja="일본어",
            grc="고대 그리스어", el="그리스어", it="이탈리아어", es="스페인어", ru="러시아어")),
"ja": dict(
 brand="名言2048",
 title="名言2048デイリー — 名言で遊ぶ無料2048パズル",
 desc="ブラウザですぐ遊べる今日の名言パズル。タイルがすべて名言の2048を、1日1回・無料・登録なしで。同じ言葉を合わせて、今日のテーマの王冠の名言を目指そう。",
 ogt="名言2048デイリー — 今日の名言パズル",
 h1="毎日1回、名言パズル", loading="今日のテーマを読み込み中…",
 noscript="名言2048をプレイするには JavaScript が必要です。遊び方は下で読めます。",
 badge="アプリ",
 ui=dict(today="今日のテーマ", todayAuthor="今日の作家パック", result="今日の結果",
   kindTopic="テーマ · 名言17", kindAuthor="作家パック · 名言17", kindPro="作家パック · アプリではPro",
   preview="プレビュー", score="スコア", best="最高タイル",
   hint="スワイプか矢印キーで移動 · タイルをタップで全文",
   won="テーマ達成！", wonSub="王冠の名言にたどり着きました。", finish="ここで終えてシェア", keep="続ける",
   share="結果をシェア", saveImg="画像を保存", copied="コピーしました — 好きな場所に貼り付けて",
   shareFail="コピーできませんでした。テキストを手動でコピーしてください。",
   appLine="アプリなら テーマ60 · 作家パック36 · 131072まで17段階 · 自分だけの名言パック",
   appLinePro="今日の作家パックはアプリのPro限定 — この作家の名言の続きはアプリで集めよう。",
   appBtn="App Storeでダウンロード", next="次のテーマまで", loadErr="今日のパズルを読み込めませんでした。再読み込みしてください。",
   boardLabel="パズルボード。矢印キーかスワイプでタイルを動かします。タイルをタップすると名言の全文が見られます。",
   done="今日はプレイ済み", bestQuote="今日たどり着いた最高の名言", collected="集めた名言",
   moreInApp="131072まであと{n}の名言がアプリで続きます",
   themePage="このテーマの名言17を見る →", close="閉じる", tile="タイル", crown="王冠の名言",
   cardScore="スコア", locked="?"),
 how_t="遊び方", how=[
   "ボードをスワイプ、または矢印キー・W A S D で、すべてのタイルを滑らせます。",
   "同じ名言のタイルが2つぶつかると、今日のテーマのひとつ上の名言になります。",
   "動かすたびに新しいタイルが1つ出ます。タイルをタップすると名言の全文と発言者が見られます。",
   "2048のタイルを作れば王冠の名言でテーマ達成。動かせなくなったら最高の名言をシェアして、また明日。"],
 faq_t="よくある質問", faq=[
   ("名言2048とは？", "名言2048は、タイルがすべて名言になった2048パズルです。1ゲームに「勇気」「時間」「シェイクスピア」などのテーマがひとつあり、2から2048までの11枚のタイルが短いことわざからテーマの王冠の名言へと上がっていきます。"),
   ("無料ですか？", "はい。今日のパズルは登録も広告もなく、ブラウザで無料で遊べます。iPhone・iPad用の名言2048アプリも無料でダウンロードできます。"),
   ("名言の出典は？", "すべての言葉はパブリックドメインの著作や伝承のことわざから採っています。セネカ、老子、シェイクスピア、エミリー・ディキンソンなど哲学者・詩人・作家の言葉で、出典と発言者は原典と照合して確認しています。"),
   ("新しいパズルはいつ？", "毎日、お使いのタイムゾーンの午前0時に新しいテーマが公開されます。Web版は1日1回で、60のテーマと作家パックを順にめぐります。"),
   ("アプリでは何ができますか？", "アプリでは作家パック36を含む60テーマをいつでも選んで遊べ、2048の先の131072まで、テーマごとに17の名言を集められます。たどり着いた名言はコレクションに残り、自分だけの名言パックも作れます。"),
 ],
 more_t="名言を探す", more_idx="テーマ別・作家別の名言集", more_land="名言2048アプリについて",
 foot_c="お問い合わせ", foot_p="プライバシー", foot_t="規約",
 q_idx_title="テーマ別・作家別 名言集60 | 名言2048",
 q_idx_h1="テーマ別・作家別の名言集",
 q_idx_desc="勇気・時間・愛など24のテーマと、シェイクスピアからセネカまで36の作家パック、計60の名言集。それぞれにパブリックドメインの名言17と発言者・原文を収録。",
 q_idx_lede="どの名言集も、短いことわざから王冠の名言まで17の言葉を順に並べています。タイルがすべて名言の2048パズル「名言2048」のタイルそのままです。",
 q_topics="テーマ", q_authors="作家パック", q_crumb="名言集",
 q_h1_topic="「{name}」の名言17選", q_h1_author="{name}の名言17選",
 q_title_topic="「{name}」の名言17選 — ことわざから古典まで | 名言2048",
 q_title_author="{name}の名言17選 — 原典から選んだ言葉 | 名言2048",
 q_desc_topic="{who}による「{name}」の名言17。短いことわざから王冠の名言まで、発言者と原文を添えて紹介します。",
 q_desc_author="{who}の名言17を原文とともに。名言2048の「{name}」パック収録。",
 q_lede_topic="「{name}」の名言17を、名言2048に登場する順に並べました。2のタイルの軽い言葉から2048のタイルの王冠の名言まで。アプリでは131072まで続きます。",
 q_lede_author="{name}の名言17を、名言2048に登場する順に並べました。2のタイルの軽い言葉から2048のタイルの王冠の名言まで。アプリでは131072まで続きます。",
 q_pd="すべての名言はパブリックドメインの著作または伝承のことわざから採り、発言者は原典と照合して確認しています。",
 q_orig="原文", q_copy="コピー", q_copied="コピー済み", q_crown="王冠の名言", q_app_only="4096〜131072の段階はアプリで続きます。",
 q_play_h="この名言で2048を遊ぶ", q_play_p="同じ名言を合わせて、このテーマの王冠の名言を目指そう。",
 q_play_app="アプリでこのパックを遊ぶ", q_play_web="今日の無料パズルへ →",
 q_pro="（アプリではPro）", q_rel="ほかの{kind}", q_rel_topic="テーマ", q_rel_author="作家パック",
 q_all="名言集の一覧", q_proverb_and="ほか",
 langs=dict(en="英語", zh="漢文", lzh="漢文", la="ラテン語", de="ドイツ語", fr="フランス語", ja="日本語",
            grc="古代ギリシャ語", el="ギリシャ語", it="イタリア語", es="スペイン語", ru="ロシア語")),
"zh-hans": dict(
 brand="名言2048",
 title="名言2048 每日挑战 — 免费名言版2048益智游戏",
 desc="在浏览器里玩今天的名言谜题：每个方块都是一句名言的2048。合并相同的句子，登上今日主题的王冠名言。免费、免注册，每天一局。",
 ogt="名言2048 每日挑战 — 今天的名言谜题",
 h1="每天一局名言谜题", loading="正在载入今日主题…",
 noscript="名言2048 需要 JavaScript 才能游玩。你仍可在下方阅读玩法。",
 badge="下载应用",
 ui=dict(today="今日主题", todayAuthor="今日作家合集", result="今日结果",
   kindTopic="主题 · 17句名言", kindAuthor="作家合集 · 17句名言", kindPro="作家合集 · 应用内为 Pro",
   preview="预览", score="分数", best="最高方块",
   hint="滑动或方向键移动 · 点按方块看全文",
   won="主题完成！", wonSub="你已抵达王冠名言。", finish="结束并分享", keep="继续",
   share="分享结果", saveImg="保存图片", copied="已复制 — 可粘贴到任何地方",
   shareFail="无法复制，请手动选择文字复制。",
   appLine="应用内：60个主题 · 36个作家合集 · 17级直到131072 · 自制名言合集",
   appLinePro="今日作家合集是应用中的 Pro 内容 — 到应用里继续收集这位作家的名言。",
   appBtn="在 App Store 下载", next="距下一个主题", loadErr="无法载入今天的谜题，请刷新页面。",
   boardLabel="谜题棋盘。使用方向键或滑动移动方块，点按方块可查看名言全文。",
   done="今日已完成", bestQuote="今天抵达的最高名言", collected="收集到的名言",
   moreInApp="还有{n}句名言在应用中延续到131072",
   themePage="查看本主题全部17句名言 →", close="关闭", tile="方块", crown="王冠名言",
   cardScore="分数", locked="?"),
 how_t="玩法", how=[
   "在棋盘上滑动，或按方向键、W A S D，让所有方块朝一个方向移动。",
   "两个相同名言的方块相遇，会合并成今日主题中更高一级的名言。",
   "每移动一次会出现一个新方块。点按任意方块可查看名言全文与出处。",
   "合成2048方块即以王冠名言完成主题。无法再移动时，分享你的最高名言，明天再来。"],
 faq_t="常见问题", faq=[
   ("名言2048是什么？", "名言2048是每个方块都是一句名言的2048益智游戏。每局有一个主题，例如勇气、时间或莎士比亚；从2到2048的11个方块，由一句简短的谚语逐级升到该主题的王冠名言。"),
   ("免费吗？", "是的。今天的谜题可在浏览器中免费游玩，无需注册，也没有广告。适用于 iPhone 和 iPad 的名言2048应用同样可免费下载。"),
   ("名言出自哪里？", "所有句子均出自公有领域作品或流传的谚语，包括塞涅卡、老子、莎士比亚、艾米莉·狄金森等哲学家、诗人与作家，出处和作者均已对照原典核实。"),
   ("什么时候有新谜题？", "每天在你所在时区的午夜开放新主题。网页版每天一局，依次轮换全部60个主题与作家合集。"),
   ("应用里还能做什么？", "在应用中可以随时选择包括36个作家合集在内的60个主题，并在2048之后继续到131072，每个主题收集17句名言。抵达的名言会留在图鉴里，还能制作自己的名言合集。"),
 ],
 more_t="浏览名言", more_idx="按主题与作家分类的名言合集", more_land="关于名言2048应用",
 foot_c="联系", foot_p="隐私政策", foot_t="服务条款",
 q_idx_title="按主题与作家分类的名言合集60组 | 名言2048",
 q_idx_h1="按主题与作家分类的名言合集",
 q_idx_desc="60组名言合集：勇气、时间、爱等24个主题，以及从莎士比亚到塞涅卡的36个作家合集，每组收录17句公有领域名言，附作者与原文。",
 q_idx_lede="每组合集收录17句名言，从简短的谚语排到王冠名言，正是名言2048——每个方块都是一句名言的2048游戏——中的方块。",
 q_topics="主题", q_authors="作家合集", q_crumb="名言合集",
 q_h1_topic="关于{name}的名言17句", q_h1_author="{name}名言17句",
 q_title_topic="关于{name}的名言17句 — 从谚语到经典 | 名言2048",
 q_title_author="{name}名言17句 — 选自原典 | 名言2048",
 q_desc_topic="{who}等人关于{name}的名言17句，从简短谚语到王冠名言，附作者与原文。",
 q_desc_author="{who}的名言17句，附原文。收录于名言2048的「{name}」合集。",
 q_lede_topic="按名言2048中出现的顺序，收录关于{name}的名言17句：从2方块的轻巧句子，到2048方块的王冠名言，应用中还会延续到131072。",
 q_lede_author="按名言2048中出现的顺序，收录{name}的名言17句：从2方块的轻巧句子，到2048方块的王冠名言，应用中还会延续到131072。",
 q_pd="所有名言均出自公有领域作品或流传的谚语，作者署名已对照原典核实。",
 q_orig="原文", q_copy="复制", q_copied="已复制", q_crown="王冠名言", q_app_only="4096至131072级在应用中延续。",
 q_play_h="用这些名言玩2048", q_play_p="合并相同的名言，登上这个主题的王冠名言。",
 q_play_app="在应用中玩这个合集", q_play_web="玩今天的免费谜题 →",
 q_pro="（应用内为 Pro）", q_rel="更多{kind}", q_rel_topic="主题", q_rel_author="作家合集",
 q_all="全部名言合集", q_proverb_and="等",
 langs=dict(en="英文", zh="文言", lzh="文言", la="拉丁文", de="德文", fr="法文", ja="日文",
            grc="古希腊文", el="希腊文", it="意大利文", es="西班牙文", ru="俄文")),
"zh-hant": dict(
 brand="名言2048",
 title="名言2048 每日挑戰 — 免費名言版2048益智遊戲",
 desc="在瀏覽器裡玩今天的名言謎題：每個方塊都是一句名言的2048。合併相同的句子，登上今日主題的王冠名言。免費、免註冊，每天一局。",
 ogt="名言2048 每日挑戰 — 今天的名言謎題",
 h1="每天一局名言謎題", loading="正在載入今日主題…",
 noscript="名言2048 需要 JavaScript 才能遊玩。你仍可在下方閱讀玩法。",
 badge="下載 App",
 ui=dict(today="今日主題", todayAuthor="今日作家合集", result="今日結果",
   kindTopic="主題 · 17句名言", kindAuthor="作家合集 · 17句名言", kindPro="作家合集 · App 內為 Pro",
   preview="預覽", score="分數", best="最高方塊",
   hint="滑動或方向鍵移動 · 點按方塊看全文",
   won="主題完成！", wonSub="你已抵達王冠名言。", finish="結束並分享", keep="繼續",
   share="分享結果", saveImg="儲存圖片", copied="已複製 — 可貼到任何地方",
   shareFail="無法複製，請手動選取文字複製。",
   appLine="App 內：60 個主題 · 36 個作家合集 · 17 級直到 131072 · 自製名言合集",
   appLinePro="今日作家合集是 App 中的 Pro 內容 — 到 App 裡繼續收集這位作家的名言。",
   appBtn="在 App Store 下載", next="距下一個主題", loadErr="無法載入今天的謎題，請重新整理頁面。",
   boardLabel="謎題棋盤。使用方向鍵或滑動移動方塊，點按方塊可查看名言全文。",
   done="今日已完成", bestQuote="今天抵達的最高名言", collected="收集到的名言",
   moreInApp="還有{n}句名言在 App 中延續到 131072",
   themePage="查看本主題全部17句名言 →", close="關閉", tile="方塊", crown="王冠名言",
   cardScore="分數", locked="?"),
 how_t="玩法", how=[
   "在棋盤上滑動，或按方向鍵、W A S D，讓所有方塊朝一個方向移動。",
   "兩個相同名言的方塊相遇，會合併成今日主題中更高一級的名言。",
   "每移動一次會出現一個新方塊。點按任意方塊可查看名言全文與出處。",
   "合成2048方塊即以王冠名言完成主題。無法再移動時，分享你的最高名言，明天再來。"],
 faq_t="常見問題", faq=[
   ("名言2048是什麼？", "名言2048是每個方塊都是一句名言的2048益智遊戲。每局有一個主題，例如勇氣、時間或莎士比亞；從2到2048的11個方塊，由一句簡短的諺語逐級升到該主題的王冠名言。"),
   ("免費嗎？", "是的。今天的謎題可在瀏覽器中免費遊玩，無需註冊，也沒有廣告。適用於 iPhone 和 iPad 的名言2048 App 同樣可免費下載。"),
   ("名言出自哪裡？", "所有句子均出自公有領域作品或流傳的諺語，包括塞內卡、老子、莎士比亞、艾蜜莉·狄更生等哲學家、詩人與作家，出處和作者均已對照原典核實。"),
   ("什麼時候有新謎題？", "每天在你所在時區的午夜開放新主題。網頁版每天一局，依次輪換全部60個主題與作家合集。"),
   ("App 裡還能做什麼？", "在 App 中可以隨時選擇包括36個作家合集在內的60個主題，並在2048之後繼續到131072，每個主題收集17句名言。抵達的名言會留在圖鑑裡，還能製作自己的名言合集。"),
 ],
 more_t="瀏覽名言", more_idx="依主題與作家分類的名言合集", more_land="關於名言2048 App",
 foot_c="聯絡", foot_p="隱私權政策", foot_t="服務條款",
 q_idx_title="依主題與作家分類的名言合集60組 | 名言2048",
 q_idx_h1="依主題與作家分類的名言合集",
 q_idx_desc="60組名言合集：勇氣、時間、愛等24個主題，以及從莎士比亞到塞內卡的36個作家合集，每組收錄17句公有領域名言，附作者與原文。",
 q_idx_lede="每組合集收錄17句名言，從簡短的諺語排到王冠名言，正是名言2048——每個方塊都是一句名言的2048遊戲——中的方塊。",
 q_topics="主題", q_authors="作家合集", q_crumb="名言合集",
 q_h1_topic="關於{name}的名言17句", q_h1_author="{name}名言17句",
 q_title_topic="關於{name}的名言17句 — 從諺語到經典 | 名言2048",
 q_title_author="{name}名言17句 — 選自原典 | 名言2048",
 q_desc_topic="{who}等人關於{name}的名言17句，從簡短諺語到王冠名言，附作者與原文。",
 q_desc_author="{who}的名言17句，附原文。收錄於名言2048的「{name}」合集。",
 q_lede_topic="按名言2048中出現的順序，收錄關於{name}的名言17句：從2方塊的輕巧句子，到2048方塊的王冠名言，App 中還會延續到131072。",
 q_lede_author="按名言2048中出現的順序，收錄{name}的名言17句：從2方塊的輕巧句子，到2048方塊的王冠名言，App 中還會延續到131072。",
 q_pd="所有名言均出自公有領域作品或流傳的諺語，作者署名已對照原典核實。",
 q_orig="原文", q_copy="複製", q_copied="已複製", q_crown="王冠名言", q_app_only="4096至131072級在 App 中延續。",
 q_play_h="用這些名言玩2048", q_play_p="合併相同的名言，登上這個主題的王冠名言。",
 q_play_app="在 App 中玩這個合集", q_play_web="玩今天的免費謎題 →",
 q_pro="（App 內為 Pro）", q_rel="更多{kind}", q_rel_topic="主題", q_rel_author="作家合集",
 q_all="全部名言合集", q_proverb_and="等",
 langs=dict(en="英文", zh="文言", lzh="文言", la="拉丁文", de="德文", fr="法文", ja="日文",
            grc="古希臘文", el="希臘文", it="義大利文", es="西班牙文", ru="俄文")),
}
LANDING = {c: f"/quote2048/{LOC[c]['sub']}" for c in LOC}


def play_url(code):
    return f"{SITE}/quote2048/play/{LOC[code]['sub']}"


def idx_url(code):
    return f"{SITE}/quote2048/quotes/{LOC[code]['sub']}"


def theme_url(tid, code):
    return f"{SITE}/quote2048/quotes/{tid}/{LOC[code]['sub']}"


def rel(url):
    return url[len(SITE):]


def hreflangs(fn):
    out = [f'<link rel="alternate" hreflang="{LOC[c]["hl"]}" href="{fn(c)}">' for c in LOC]
    out.append(f'<link rel="alternate" hreflang="x-default" href="{fn("en")}">')
    return "\n".join(out)


ORG = {"@type": "Organization", "@id": SITE + "/#organization", "name": "kkiruk studio", "url": SITE + "/"}
WEBSITE = {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "kkiruk studio",
           "publisher": {"@id": ORG["@id"]}}
APP_NODE = {"@type": "MobileApplication", "@id": SITE + f"/#app-{APP_ID}", "name": APP_NAME,
            "operatingSystem": "iOS", "applicationCategory": "GameApplication",
            "installUrl": f"https://apps.apple.com/app/id{APP_ID}", "url": SITE + "/quote2048/",
            "publisher": {"@id": ORG["@id"]}}


def crumbs(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}


# ─── Play page ────────────────────────────────────────────────────────────────
def play_jsonld(code, d):
    url = play_url(code)
    game = {"@type": ["VideoGame", "WebApplication"], "@id": url + "#game", "name": "Quote 2048 Daily",
            "alternateName": d["brand"] + " — daily quote puzzle", "url": url, "description": d["desc"],
            "inLanguage": LOC[code]["hl"], "applicationCategory": "Game", "operatingSystem": "Any",
            "browserRequirements": "Requires JavaScript", "gamePlatform": "Web browser",
            "genre": ["Puzzle", "Word puzzle"], "playMode": "SinglePlayer", "isAccessibleForFree": True,
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
            "image": OG_IMAGE, "publisher": {"@id": ORG["@id"]}, "author": {"@id": ORG["@id"]},
            "isBasedOn": {"@id": APP_NODE["@id"]},
            "keywords": "daily quote puzzle, 2048 quotes game, famous quotes game, quote puzzle"}
    page = {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": d["title"], "description": d["desc"],
            "inLanguage": LOC[code]["hl"], "isPartOf": {"@id": WEBSITE["@id"]}, "mainEntity": {"@id": game["@id"]},
            "publisher": {"@id": ORG["@id"]}}
    faq = {"@type": "FAQPage", "@id": url + "#faq", "inLanguage": LOC[code]["hl"],
           "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                          for q, a in d["faq"]]}
    return ld({"@context": "https://schema.org", "@graph": [ORG, WEBSITE, page, game, APP_NODE, faq]})


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
<meta name="theme-color" content="#000000">
<meta name="color-scheme" content="dark">
<meta property="og:type" content="website">
<meta property="og:site_name" content="kkiruk studio">
<meta property="og:title" content="{ogt}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og_image}">
<meta property="og:locale" content="{og_locale}">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{ogt}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{og_image}">
<link rel="icon" type="image/png" href="/quote2048/assets/icon-180.png">
<link rel="apple-touch-icon" href="/quote2048/assets/icon-180.png">
<link rel="stylesheet" href="/quote2048/play/play.css?v={v_css}">
<script src="/ga.js"></script>
{jsonld}
</head>
<body>
<div class="stage" id="stage">
  <header class="top">
    <a class="brand" href="{landing}"><img src="/quote2048/assets/icon-180.png" alt="" width="24" height="24">{brand}</a>
    <span class="daylabel" id="dayLabel"></span>
    <span class="top-end"><a class="badge" href="{app_url}" data-cta="badge" target="_blank" rel="noopener">{apple}{badge}</a></span>
  </header>
  <div class="head">
    <h1 class="kicker" id="kicker">{h1}</h1>
    <p class="tname" id="tname">{loading}</p>
    <p class="tmeta" id="tmeta">&nbsp;</p>
  </div>
  <div class="scorebar" id="scorebar">
    <div class="stat"><span class="lbl">{score}</span><b id="score">0</b></div>
    <div class="stat"><span class="lbl">{best}</span><i class="swatch" id="bestSwatch"></i></div>
  </div>
  <div class="board" id="board" role="application" aria-label="{board_label}" tabindex="0">
    <div class="cells">{cells}</div>
    <div class="tiles" id="tiles"></div>
    <div class="overlay" id="winOverlay" hidden>
      <p class="w-title" id="winText"></p>
      <p class="w-quote" id="winQuote"></p>
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
    <div class="share-row">
      <button type="button" class="btn primary share" id="shareBtn">{share}</button>
      <button type="button" class="btn ghost save" id="saveBtn" hidden>{save_img}</button>
    </div>
    <p class="toast" id="toast" role="status"></p>
    <figure class="q-card" id="bestCard">
      <figcaption class="q-kicker" id="bestKicker"></figcaption>
      <blockquote id="bestText"></blockquote>
      <p class="q-by" id="bestBy"></p>
    </figure>
    <div class="ladder-box">
      <h2 class="l-title" id="ladderTitle"></h2>
      <ol class="ladder" id="ladder"></ol>
      <p class="l-more" id="ladderMore"></p>
      <a class="l-link" id="themeLink" href="{quotes_idx}"></a>
    </div>
    <div class="r-app" id="rApp">
      <p id="appLine">{app_line}</p>
      <a class="btn store" href="{app_url}" data-cta="result" target="_blank" rel="noopener">{apple}{app_btn}</a>
    </div>
    <p class="r-next">{next} <b id="countdown">--:--:--</b></p>
  </section>
  <noscript><p class="hint">{noscript}</p></noscript>
</div>
<div class="sheet" id="sheet" hidden>
  <div class="sheet-card" role="dialog" aria-modal="true" aria-labelledby="sheetText">
    <p class="s-level" id="sheetLevel"></p>
    <blockquote id="sheetText"></blockquote>
    <p class="s-by" id="sheetBy"></p>
    <button type="button" class="btn ghost" id="sheetClose">{close}</button>
  </div>
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
      <li><a href="{quotes_idx}">{more_idx}</a></li>
{theme_links}
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
<script src="/quote2048/play/core.js?v={v_core}"></script>
<script src="/quote2048/play/play.js?v={v_js}"></script>
</body>
</html>
"""


def build_play(themes, sched):
    versions = dict(v_css=ver(HERE / "play.css"), v_js=ver(HERE / "play.js"), v_core=ver(HERE / "core.js"))
    picks = [t for t in themes if t["kind"] == "topic"][:4] + [t for t in themes if t["kind"] == "author"][:4]
    for code in LOC:
        d = T[code]
        ui = dict(d["ui"], appUrl=app_url(CT_PLAY), sched=sched, sub=LOC[code]["sub"], loc=code)
        langs = "\n".join(f'    <a href="/quote2048/play/{LOC[c]["sub"]}" hreflang="{LOC[c]["hl"]}" lang="{LOC[c]["hl"]}">{LOC[c]["label"]}</a>'
                          for c in LOC if c != code)
        theme_links = "\n".join(f'      <li><a href="{rel(theme_url(t["id"], code))}">{escape(h1_for(t, code))}</a></li>'
                                for t in picks)
        html = PLAY_TMPL.format(
            lang=LOC[code]["hl"], mark=BUILD_MARK, title=escape(d["title"]), desc=escape(d["desc"]), url=play_url(code),
            hreflang=hreflangs(play_url), app_id=APP_ID, ogt=escape(d["ogt"]), og_image=OG_IMAGE,
            og_locale=LOC[code]["og"], jsonld=play_jsonld(code, d), landing=LANDING[code],
            app_url=escape(app_url(CT_PLAY)), brand=escape(d["brand"]), apple=APPLE_SVG, badge=d["badge"],
            h1=escape(d["h1"]), loading=escape(d["loading"]), score=d["ui"]["score"], best=d["ui"]["best"],
            board_label=escape(d["ui"]["boardLabel"]), cells="<i></i>" * 16, hint=escape(d["ui"]["hint"]),
            share=d["ui"]["share"], save_img=d["ui"]["saveImg"], close=d["ui"]["close"],
            app_line=escape(d["ui"]["appLine"]), app_btn=d["ui"]["appBtn"], next=d["ui"]["next"],
            noscript=escape(d["noscript"]), how_t=d["how_t"], faq_t=d["faq_t"], more_t=d["more_t"],
            how="".join(f"<li>{escape(s)}</li>" for s in d["how"]),
            faq="".join(f"<details><summary><h3>{escape(q)}</h3></summary><p>{escape(a)}</p></details>"
                        for q, a in d["faq"]),
            quotes_idx=rel(idx_url(code)), more_idx=d["more_idx"], theme_links=theme_links,
            more_land=d["more_land"], app_name=APP_NAME,
            foot_c=d["foot_c"], foot_p=d["foot_p"], foot_t=d["foot_t"], langs=langs,
            ui=jdump(ui), **versions)
        save(HERE / LOC[code]["sub"] / "index.html", html)


# ─── Quote pages ──────────────────────────────────────────────────────────────
def h1_for(t, code):
    d = T[code]
    return (d["q_h1_topic"] if t["kind"] == "topic" else d["q_h1_author"]).format(name=tname(t, code))


def lname(t, code):
    n = tname(t, code)
    return n.lower() if code == "en" else n


def who_for(t, code):
    """Distinct real authors in the theme (proverbs/works excluded), most-quoted first."""
    seen = {}
    for q in t["quotes"]:
        if q["author_en"] in NOT_PERSON or q["author_en"] in WORKS:
            continue
        a = qauthor(q, code)
        seen[a] = seen.get(a, 0) + 1
    names = sorted(seen, key=lambda a: -seen[a])
    sep = ", " if code == "en" else ("、" if code in ("ja", "zh-hans", "zh-hant") else ", ")
    if code == "en":
        top = names[:3]
        return (", ".join(top[:-1]) + " and " + top[-1]) if len(top) > 1 else (top[0] if top else "")
    return sep.join(names[:3])


def original_for(q, code):
    """Mirror of QuoteEntry.displayOriginal for the page's language."""
    text = qtext(q, code)
    cand = q.get("original") or {"en": q["en"], "zh": q["zh_hant"], "ja": q["ja"]}.get(q.get("original_lang"))
    if not cand or cand == text:
        return None
    return cand


def related(t, themes):
    """6 same-kind themes nearest in app order (cyclic)."""
    ids = [x["id"] for x in themes if x["kind"] == t["kind"]]
    by = {x["id"]: x for x in themes}
    i, n = ids.index(t["id"]), len(ids)
    others = [j for j in range(n) if j != i]
    others.sort(key=lambda j: (min(abs(j - i), n - abs(j - i)), j))
    return [by[ids[j]] for j in others[:6]]


QHEAD = """<!DOCTYPE html>
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
<meta name="theme-color" content="#000000">
<meta name="color-scheme" content="dark">
<meta property="og:type" content="article">
<meta property="og:site_name" content="kkiruk studio">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og_image}">
<meta property="og:locale" content="{og_locale}">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{og_image}">
<link rel="icon" type="image/png" href="/quote2048/assets/icon-180.png">
<link rel="apple-touch-icon" href="/quote2048/assets/icon-180.png">
<link rel="stylesheet" href="/quote2048/quotes/quotes.css?v={v_css}">
<script src="/ga.js"></script>
{jsonld}
</head>
<body>
<header class="bar">
  <a class="brand" href="{landing}"><img src="/quote2048/assets/icon-180.png" alt="" width="24" height="24">{brand}</a>
  <nav><a href="{idx}">{crumb}</a><a class="play" href="{play}">{play_lbl}</a></nav>
</header>
<main class="wrap">
"""

QFOOT = """</main>
<footer class="foot">
  <a href="/">© kkiruk studio</a>
  <nav><a href="{landing}">{brand}</a><a href="{play}">{play_lbl}</a><a href="/legal/privacy/">{foot_p}</a><a href="/legal/terms/">{foot_t}</a>
{langs}
  </nav>
</footer>
<script id="qi18n" type="application/json">{qi18n}</script>
<script src="/quote2048/quotes/quotes.js?v={v_js}"></script>
</body>
</html>
"""


def head_foot(code, title, desc, url, fn, jsonld, v):
    d = T[code]
    play_lbl = T[code]["q_play_web"].rstrip(" →")
    langs = "\n".join(f'    <a href="{rel(fn(c))}" hreflang="{LOC[c]["hl"]}" lang="{LOC[c]["hl"]}">{LOC[c]["label"]}</a>'
                      for c in LOC if c != code)
    head = QHEAD.format(lang=LOC[code]["hl"], mark=BUILD_MARK, title=escape(title), desc=escape(desc), url=url,
                        hreflang=hreflangs(fn), app_id=APP_ID, og_image=OG_IMAGE, og_locale=LOC[code]["og"],
                        v_css=v["css"], jsonld=jsonld, landing=LANDING[code], brand=escape(d["brand"]),
                        idx=rel(idx_url(code)), crumb=escape(d["q_crumb"]), play=rel(play_url(code)),
                        play_lbl=escape(play_lbl))
    foot = QFOOT.format(landing=LANDING[code], brand=escape(d["brand"]), play=rel(play_url(code)),
                        play_lbl=escape(play_lbl), foot_p=d["foot_p"], foot_t=d["foot_t"], langs=langs,
                        qi18n=jdump({"copied": d["q_copied"]}), v_js=v["js"])
    return head, foot


def quotation_node(q, code):
    node = {"@type": "Quotation", "text": qtext(q, code), "inLanguage": LOC[code]["hl"]}
    a = q["author_en"]
    if a in WORKS:
        node["isBasedOn"] = {"@type": "CreativeWork", "name": qauthor(q, code)}
    elif a not in NOT_PERSON:
        node["creator"] = {"@type": "Person", "name": qauthor(q, code)}
    return node


def build_quote_pages(themes):
    v = dict(css=ver(QDIR / "quotes.css"), js=ver(QDIR / "quotes.js"))
    n = 0
    for code in LOC:
        d = T[code]
        for t in themes:
            url = theme_url(t["id"], code)
            name = tname(t, code)
            h1 = h1_for(t, code)
            topic = t["kind"] == "topic"
            who = who_for(t, code)
            title = (d["q_title_topic"] if topic else d["q_title_author"]).format(name=name, n=17)
            desc = (d["q_desc_topic"] if topic else d["q_desc_author"]).format(name=name, lname=lname(t, code), who=who)
            lede = (d["q_lede_topic"] if topic else d["q_lede_author"]).format(name=name, lname=lname(t, code))
            items = []
            for i, q in enumerate(t["quotes"]):
                lv = 2 ** (i + 1)
                text, author = qtext(q, code), qauthor(q, code)
                orig = original_for(q, code)
                lang = q.get("original_lang")
                orig_html = ""
                if orig:
                    label = d["langs"].get(lang, d["q_orig"]) if lang else d["q_orig"]
                    orig_html = (f'<p class="orig"><span>{escape(d["q_orig"])} · {escape(label)}</span>'
                                 f'<q lang="{escape(lang or "")}">{escape(orig)}</q></p>')
                cls = "crown" if lv == 2048 else ("app" if lv > 2048 else "")
                badge = f'<span class="lv">{lv}</span>' + (f'<span class="crown-tag">👑 {escape(d["q_crown"])}</span>' if lv == 2048 else "")
                copy = (f"「{text}」 — {author}" if code in ("ja", "zh-hant") else f"“{text}” — {author}")
                items.append(
                    f'<li class="{cls}" id="q{lv}"><div class="meta">{badge}</div>'
                    f'<blockquote><p>{escape(text)}</p></blockquote>'
                    f'<p class="by">— {escape(author)}</p>{orig_html}'
                    f'<button type="button" class="copy" data-copy="{escape(copy)}">{escape(d["q_copy"])}</button></li>')
                if lv == 2048:
                    items.append(f'<li class="note">{escape(d["q_app_only"])}</li>')
            rel_items = "".join(
                f'<li><a href="{rel(theme_url(x["id"], code))}">{escape(tname(x, code))}'
                f'<small>{escape(qauthor(x["quotes"][10], code))}</small></a></li>' for x in related(t, themes))
            rel_kind = d["q_rel_topic"] if topic else d["q_rel_author"]
            pro = d["q_pro"] if t["premium"] else ""
            coll = {"@type": "CollectionPage", "@id": url + "#page", "url": url, "name": h1, "description": desc,
                    "inLanguage": LOC[code]["hl"], "isPartOf": {"@id": WEBSITE["@id"]},
                    "publisher": {"@id": ORG["@id"]}, "about": {"@id": APP_NODE["@id"]},
                    "mainEntity": {"@type": "ItemList", "numberOfItems": 17, "itemListOrder": "https://schema.org/ItemListOrderAscending",
                                   "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": quotation_node(q, code)}
                                                       for i, q in enumerate(t["quotes"])]}}
            bc = crumbs([("kkiruk studio", SITE + "/"), (d["brand"], SITE + LANDING[code]),
                         (d["q_crumb"], idx_url(code)), (name, url)])
            jsonld = ld({"@context": "https://schema.org", "@graph": [ORG, WEBSITE, APP_NODE, coll, bc]})
            head, foot = head_foot(code, title, desc, url, lambda c, tid=t["id"]: theme_url(tid, c), jsonld, v)
            body = f"""<nav class="crumbs" aria-label="Breadcrumb"><a href="{LANDING[code]}">{escape(d['brand'])}</a> › <a href="{rel(idx_url(code))}">{escape(d['q_crumb'])}</a> › <span>{escape(name)}</span></nav>
<p class="kind">{escape(d['q_topics'] if topic else d['q_authors'])}{escape(pro)}</p>
<h1>{escape(h1)}</h1>
<p class="lede">{escape(lede)}</p>
<p class="pd">{escape(d['q_pd'])}</p>
<ol class="quotes">{''.join(items)}</ol>
<section class="cta">
<h2>{escape(d['q_play_h'])}</h2>
<p>{escape(d['q_play_p'])}</p>
<div class="btns">
<a class="btn store" href="{escape(app_url(CT_QUOTES))}" data-cta="quotes" target="_blank" rel="noopener">{APPLE_SVG}{escape(d['q_play_app'])}</a>
<a class="btn ghost" href="{rel(play_url(code))}">{escape(d['q_play_web'])}</a>
</div>
</section>
<section>
<h2>{escape(d['q_rel'].format(kind=rel_kind))}</h2>
<ul class="grid">{rel_items}</ul>
<p class="all"><a href="{rel(idx_url(code))}">{escape(d['q_all'])} →</a></p>
</section>
"""
            save(QDIR / t["id"] / LOC[code]["sub"] / "index.html", head + body + foot)
            n += 1

        # index
        def block(kind, label):
            li = "".join(
                f'<li><a href="{rel(theme_url(x["id"], code))}">{escape(tname(x, code))}'
                f'<small>{escape(qtext(x["quotes"][10], code))}</small></a></li>'
                for x in themes if x["kind"] == kind)
            return f'<section><h2 id="{kind}">{escape(label)}</h2><ul class="grid idx">{li}</ul></section>'
        url = idx_url(code)
        coll = {"@type": "CollectionPage", "@id": url + "#page", "url": url, "name": d["q_idx_h1"],
                "description": d["q_idx_desc"], "inLanguage": LOC[code]["hl"], "isPartOf": {"@id": WEBSITE["@id"]},
                "publisher": {"@id": ORG["@id"]},
                "mainEntity": {"@type": "ItemList", "numberOfItems": len(themes),
                               "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": tname(x, code),
                                                    "url": theme_url(x["id"], code)} for i, x in enumerate(themes)]}}
        bc = crumbs([("kkiruk studio", SITE + "/"), (d["brand"], SITE + LANDING[code]), (d["q_crumb"], url)])
        head, foot = head_foot(code, d["q_idx_title"], d["q_idx_desc"], url, idx_url,
                               ld({"@context": "https://schema.org", "@graph": [ORG, WEBSITE, coll, bc]}), v)
        body = f"""<nav class="crumbs" aria-label="Breadcrumb"><a href="{LANDING[code]}">{escape(d['brand'])}</a> › <span>{escape(d['q_crumb'])}</span></nav>
<h1>{escape(d['q_idx_h1'])}</h1>
<p class="lede">{escape(d['q_idx_lede'])}</p>
<div class="btns"><a class="btn ghost" href="{rel(play_url(code))}">{escape(d['q_play_web'])}</a>
<a class="btn store" href="{escape(app_url(CT_QUOTES))}" data-cta="quotes_index" target="_blank" rel="noopener">{APPLE_SVG}{escape(T[code]['badge'])}</a></div>
<p class="jump"><a href="#topic">{escape(d['q_topics'])} · 24</a> <a href="#author">{escape(d['q_authors'])} · 36</a></p>
{block('topic', d['q_topics'])}
{block('author', d['q_authors'])}
"""
        save(QDIR / LOC[code]["sub"] / "index.html", head + body + foot)
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--make-web-schedule", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--no-sitemap", action="store_true")
    args = ap.parse_args()
    themes = load_themes()
    if args.make_web_schedule:
        make_schedule(themes, args.force)
        return
    sched = load_schedule(themes)
    n_data = build_data(themes)
    build_play(themes, sched)
    n_pages = build_quote_pages(themes)
    print(f"data files: {n_data} · play pages: {len(LOC)} · quote pages: {n_pages} (+ {len(LOC)} indexes)")
    if not args.no_sitemap:
        subprocess.run([sys.executable, str(ROOT / "gen" / "gen_sitemap.py")], check=True)


if __name__ == "__main__":
    main()
