#!/usr/bin/env python3
"""
Lift the rail apps out of the flat Apps grid into their own section.

The three of them are one product with three datasets, but the App
Store cannot say so: NYC Subway Log dropped the series naming
(鉄ログ / 레일로그 / …log) for ASO reasons, so nothing in the store
tells a Tetsulog user that a New York edition exists. The site is now
the only place the family reads as a family, which is what this
section is for — and the cross-sell it enables is real, because the
audience is people who like trains *and travel*.

Idempotent: running it twice leaves one section. Re-run after editing
copy, then `git -C ~/kkirukstudio-site diff` before pushing.
"""

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

# Per locale: the home file, the nav label, the section intro, and the
# NYC card (the other two cards are moved verbatim from the Apps grid,
# so their copy stays whatever it already was).
LOCALES = {
    "index.html": dict(
        nav="Rail",
        shared='역을 탭하면 탑승이 기록되고, 탄 노선의 색이 지도 위에 퍼져요. ',
        label="Rail",
        intro="탄 노선을 지도에 채워가는 기록장 — 같은 엔진에, 나라마다 다른 노선 데이터를 넣었어요.",
        more="철도 앱 세 가지 한눈에 보기 →",
        hub="/rail/",
        nyc_href="/nyc-subway-log/ko/",
        nyc_alt="NYC Subway Log 아이콘",
        nyc_sub="New York Subway Log",
        nyc_body="뉴욕 지하철 "
                 "<b>25개 노선·475개 역</b> 완주 기록 앱.",
        nyc_link="자세히 보기 →",
    ),
    "en.html": dict(
        nav="Rail",
        shared="Tap a station to log the ride — the line's color spreads across the map. ",
        label="Rail",
        intro="A log that fills the map with the lines you've ridden — one engine, "
              "a different country's network in each.",
        more="See all three rail apps →",
        hub="/rail/en.html",
        nyc_href="/nyc-subway-log/",
        nyc_alt="NYC Subway Log icon",
        nyc_sub="New York Subway Log",
        nyc_body="A New York City subway log covering <b>25 services and 475 stations</b>.",
        nyc_link="Learn more →",
    ),
    "ja.html": dict(
        nav="Rail",
        shared='駅をタップするだけで乗車を記録。乗った路線の色が地図に広がります。',
        label="Rail",
        intro="乗った路線で地図を埋めていく記録帳 — 同じエンジンに、国ごとの路線データを載せています。",
        more="鉄道アプリ3本をまとめて見る →",
        hub="/rail/ja.html",
        nyc_href="/nyc-subway-log/ja/",
        nyc_alt="NYC Subway Log アイコン",
        nyc_sub="New York Subway Log",
        nyc_body="ニューヨーク地下鉄<b>25路線・475駅</b>の完乗記録アプリ。",
        nyc_link="くわしく見る →",
    ),
    "zh-hans.html": dict(
        nav="Rail",
        shared='点击车站即可记录乘车，乘坐路线的颜色会在地图上扩散。',
        label="Rail",
        intro="用搭过的线路把地图填满的记录本 —— 同一套引擎，装进各国的路网数据。",
        more="一次看完三款铁道应用 →",
        hub="/rail/zh-hans.html",
        nyc_href="/nyc-subway-log/",
        nyc_alt="NYC Subway Log 图标",
        nyc_sub="纽约地铁乘车记录",
        nyc_body="涵盖纽约地铁"
                 "<b>25条线路·475个车站</b>的乘车记录应用。",
        nyc_link="了解更多 →",
    ),
    "zh-hant.html": dict(
        nav="Rail",
        shared='點擊車站即可記錄乘車，搭乘路線的顏色會在地圖上擴散。',
        label="Rail",
        intro="用搭過的路線把地圖填滿的紀錄簿 —— 同一套引擎，裝進各國的路網資料。",
        more="一次看完三款鐵道應用程式 →",
        hub="/rail/zh-hant.html",
        nyc_href="/nyc-subway-log/zh-hant/",
        nyc_alt="NYC Subway Log 圖示",
        nyc_sub="紐約地鐵乘車記錄",
        nyc_body="涵蓋紐約地鐵"
                 "<b>25條路線·475個車站</b>的乘車記錄應用程式。",
        nyc_link="了解更多 →",
    ),
}

# Leading indent only, not a preceding newline: on a re-run the cards
# sit at a different indent inside the section, and requiring the
# newline made the match miss one of them.
CARD_RE = re.compile(
    r'[ \t]*<a class="app-card reveal" href="(?:raillog|tetsulog)[^"]*">.*?</a>\n',
    re.S)


def nyc_card(c):
    return f'''
      <a class="app-card reveal" href="{c['nyc_href']}">
        <img src="/icons/nyc-subway-log.png" alt="{c['nyc_alt']}">
        <div>
          <h3>NYC Subway Log</h3>
          <p class="en">{c['nyc_sub']}<span class="plat"> · iOS</span></p>
          <p>{c['nyc_body']}</p>
          <div class="links"><span>{c['nyc_link']}</span></div>
        </div>
      </a>
'''


def build(name, c):
    path = ROOT / name
    s = path.read_text(encoding="utf-8")

    # Collect the cards first: on a re-run they live inside the section
    # this is about to delete, so reading them afterwards finds nothing.
    cards = CARD_RE.findall(s)
    if len(cards) != 2:
        sys.exit(f"{name}: 철도 카드 2개를 찾지 못함 ({len(cards)}개)")

    s = re.sub(r'\n<!-- ── 철도 ── -->\n<section id="rail">.*?</section>\n',
               "\n", s, flags=re.S)
    s = CARD_RE.sub("\n", s)

    # Japan first, then Korea, then New York: the order they were built,
    # which is also the order the family grew.
    # Side by side the shared opening sentence read three times over.
    # The section intro says it once; the cards keep only what differs.
    cards = [x.replace(c["shared"], "") for x in cards]
    tetsu = next(x for x in cards if "tetsulog" in x)
    rail = next(x for x in cards if "raillog" in x)
    ordered = "".join(x.strip("\n") + "\n" for x in (tetsu, rail)) + nyc_card(c)

    section = f'''
<!-- ── 철도 ── -->
<section id="rail">
  <div class="wrap">
    <p class="sec-label reveal">{c['label']}</p>
    <p class="sec-intro reveal">{c['intro']}</p>
    <div class="apps">
{ordered}    </div>
    <p class="sec-more reveal"><a href="{c['hub']}">{c['more']}</a></p>
  </div>
</section>
'''

    # After the Apps grid — the rail apps are apps, just a set of them.
    # Locales don't share a section list (only ko has #fun), so anchor on
    # whatever section follows #apps rather than naming one.
    after_apps = s.index('<section id="apps">') + 1
    anchor = s.index('<section id=', after_apps)
    anchor = s.rindex('\n', 0, anchor) + 1
    s = s[:anchor] + section.lstrip("\n") + "\n" + s[anchor:]

    # Nav entry, once.
    head = s.split("</header>")[0]
    if 'href="#rail"' not in head:
        i = s.index('href="#apps"')
        j = s.index("</a>", i) + 4
        s = s[:j] + f'\n      <a href="#rail">{c["nav"]}</a>' + s[j:]

    path.write_text(s, encoding="utf-8")
    print(f"{name}: 카드 3장 · 섹션 삽입")


for name, conf in LOCALES.items():
    build(name, conf)
