#!/usr/bin/env python3
"""
/rail/ — the hub for the rail logging family.

Three apps, one engine, a different country's network in each. The App
Store cannot say that: NYC Subway Log gave up the series naming
(鉄ログ / 레일로그 / …log) for ASO reasons, so nothing in the store
connects them. This page is where the family is stated.

Deliberately no "coming soon" for the UK or Germany editions. Landing
copy on this site is held to what actually ships, and an announcement
that slips becomes a debt.

    python3 build.py     # regenerates every locale in place
"""

import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
BASE = "https://www.kkirukstudio.com/rail/"

# file -> (html lang, store/landing paths, copy)
LOCALES = {
    "index.html": dict(
        lang="ko", label="한국어",
        title="철도 기록 앱 — 테츠로그 · 레일로그 · NYC Subway Log",
        desc="탄 노선을 지도에 채워가는 기록장. 일본, 한국, 뉴욕 — 가는 곳마다 하나씩 있습니다.",
        home="홈으로",
        kicker="Rail",
        h1="탄 노선을<br>지도에 채워갑니다",
        lead="역을 탭하면 탑승이 기록되고, 탄 노선의 색이 지도 위에 퍼집니다. "
             "일본·한국·뉴욕 — 가는 곳마다 그곳의 기록장이 있어요.",
        cards_label="일본 · 한국 · 뉴욕",
        how_label="기록되는 방식",
        how=[("지도가 기록입니다",
              "체크리스트에 표시하는 게 아니라, 실제 선로 모양 그대로 색이 칠해집니다. 어디까지 갔는지가 한눈에 보여요."),
             ("노선을 다 타면 완주카드",
              "노선 하나를 끝내면 완주카드가 발급되고, 역은 스탬프북에 쌓입니다. PDF로 내보낼 수도 있어요."),
             ("계정 없이, 기기 안에",
              "로그인도 서버도 없습니다. 기록은 기기에 저장되고, 원하면 본인 iCloud로만 동기화됩니다.")],
        note="노선·역 데이터는 각 나라의 공공 데이터를 씁니다. 출처는 앱 설정의 「데이터 출처」에 적어두었어요.",
        apps=[("테츠로그", "Tetsulog · Japan Rail Trip Log", "/tetsulog/ko/", "tetsulog",
               "일본 전국 <b>163개사·571개 노선·10,096개 역</b>. 乗りつぶし 문화 그대로의 완주 기록 앱."),
              ("레일로그", "Raillog · Korea Rail Trip Log", "/raillog/", "raillog",
               "전국 <b>17개 사업자·55개 노선·1,191개 역</b>. KTX부터 무궁화호까지, 안 타본 노선을 지워갑니다."),
              ("NYC Subway Log", "New York Subway Log", "/nyc-subway-log/ko/", "nyc-subway-log",
               "뉴욕 지하철 <b>25개 노선·475개 역</b>. 전 역을 다 타는 Subway Challenge, 그 기록장.")],
        more="자세히 보기 →",
    ),
    "en.html": dict(
        lang="en", label="English",
        title="Rail logging apps — Tetsulog, Raillog, NYC Subway Log",
        desc="A log that fills the map with the lines you've ridden. Japan, Korea, New York — "
             "one for each place you go.",
        home="Home",
        kicker="Rail",
        h1="Fill the map with<br>the lines you've ridden",
        lead="Tap a station to log the ride, and the line's color spreads across the map. "
             "Japan, Korea, New York — wherever you ride, there's a log for it.",
        cards_label="Japan · Korea · New York",
        how_label="How it works",
        how=[("The map is the record",
              "Nothing to tick off — the line fills in along its real shape, so how far you've gotten reads at a glance."),
             ("Finish a line, get the card",
              "Complete a line and a completion card is issued; stations collect in a stamp book you can export as PDF."),
             ("No account, on your device",
              "No login, no server. Records live on the device and sync only through your own iCloud if you want them to.")],
        note="Line and station data comes from each country's public datasets, credited in the app under Data Sources.",
        apps=[("Tetsulog", "Japan Rail Trip Log", "/tetsulog/en/", "tetsulog",
               "<b>163 operators, 571 lines, 10,096 stations</b> across Japan — built around the 乗りつぶし tradition."),
              ("Raillog", "Korea Rail Trip Log", "/raillog/en/", "raillog",
               "<b>17 operators, 55 lines, 1,191 stations</b> across Korea — KTX down to the slow Mugunghwa."),
              ("NYC Subway Log", "New York Subway Log", "/nyc-subway-log/", "nyc-subway-log",
               "<b>25 services, 475 stations</b> — a log for the Subway Challenge, riding every stop in the city.")],
        more="Learn more →",
    ),
    "ja.html": dict(
        lang="ja", label="日本語",
        title="鉄道記録アプリ — 鉄ログ・Raillog・NYC Subway Log",
        desc="乗った路線で地図を埋めていく記録帳。日本・韓国・ニューヨーク — 行く先ごとに一冊ずつ。",
        home="ホームへ",
        kicker="Rail",
        h1="乗った路線で<br>地図を埋めていく",
        lead="駅をタップするだけで乗車が記録され、乗った路線の色が地図に広がります。"
             "日本・韓国・ニューヨーク — 行く先ごとに、その土地の記録帳を。",
        cards_label="日本 · 韓国 · ニューヨーク",
        how_label="記録のしかた",
        how=[("地図がそのまま記録に",
              "チェックリストに印をつけるのではなく、実際の線路の形のまま色が塗られます。どこまで行ったかが一目で。"),
             ("路線を完乗すると完乗カード",
              "1路線を乗りつぶすと完乗カードが発行され、駅はスタンプ帳に貯まります。PDF 書き出しも可能。"),
             ("アカウント不要・端末の中に",
              "ログインもサーバーもありません。記録は端末に保存され、希望すればご自身の iCloud だけで同期します。")],
        note="路線・駅データは各国の公共データを使用しています。出典はアプリの「データの出典」に記載しています。",
        apps=[("鉄ログ", "Tetsulog · Japan Rail Trip Log", "/tetsulog/", "tetsulog",
               "全国<b>163社・571路線・10,096駅</b>。乗りつぶし文化そのままの記録アプリ。"),
              ("Raillog", "Korea Rail Trip Log", "/raillog/en/", "raillog",
               "韓国全土<b>17社・55路線・1,191駅</b>。KTX から ムグンファ号 まで。"),
              ("NYC Subway Log", "New York Subway Log", "/nyc-subway-log/ja/", "nyc-subway-log",
               "ニューヨーク地下鉄<b>25路線・475駅</b>。全駅を乗りつぶす Subway Challenge の記録帳。")],
        more="くわしく見る →",
    ),
    "zh-hans.html": dict(
        lang="zh-Hans", label="简体中文",
        title="铁道乘车记录应用 — Tetsulog · Raillog · NYC Subway Log",
        desc="用搭过的线路把地图填满的记录本。日本、韩国、纽约 —— 去到哪里，就有哪里的一本。",
        home="回首页",
        kicker="Rail",
        h1="用搭过的线路<br>把地图填满",
        lead="点击车站即可记录乘车，乘坐路线的颜色会在地图上扩散。"
             "日本、韩国、纽约 —— 去到哪里，就有哪里的记录本。",
        cards_label="日本 · 韩国 · 纽约",
        how_label="怎么记录",
        how=[("地图本身就是记录",
              "不是在清单上打勾，而是照实际线路的形状上色。走到哪里一目了然。"),
             ("坐完整条线就有完乘卡",
              "完成一条线路即发放完乘卡，车站累积到盖章簿中，还可导出 PDF。"),
             ("无需账号，留在设备里",
              "没有登录，也没有服务器。记录保存在设备上，需要时仅通过你自己的 iCloud 同步。")],
        note="线路与车站数据来自各国公共数据，出处记载于应用的「数据来源」中。",
        apps=[("Tetsulog", "日本铁道乘车记录", "/tetsulog/en/", "tetsulog",
               "日本全国<b>163家公司·571条线路·10,096个车站</b>。"),
              ("Raillog", "韩国铁道乘车记录", "/raillog/en/", "raillog",
               "韩国全国<b>17家公司·55条线路·1,191个车站</b>。"),
              ("NYC Subway Log", "纽约地铁乘车记录", "/nyc-subway-log/", "nyc-subway-log",
               "纽约地铁<b>25条线路·475个车站</b>。搭遍每一站的 Subway Challenge 记录本。")],
        more="了解更多 →",
    ),
    "zh-hant.html": dict(
        lang="zh-Hant", label="繁體中文",
        title="鐵道乘車記錄應用程式 — Tetsulog · Raillog · NYC Subway Log",
        desc="用搭過的路線把地圖填滿的紀錄簿。日本、韓國、紐約 —— 去到哪裡，就有哪裡的一本。",
        home="回首頁",
        kicker="Rail",
        h1="用搭過的路線<br>把地圖填滿",
        lead="點擊車站即可記錄乘車，搭乘路線的顏色會在地圖上擴散。"
             "日本、韓國、紐約 —— 去到哪裡，就有哪裡的紀錄簿。",
        cards_label="日本 · 韓國 · 紐約",
        how_label="怎麼記錄",
        how=[("地圖本身就是紀錄",
              "不是在清單上打勾，而是照實際路線的形狀上色。走到哪裡一目了然。"),
             ("搭完整條路線就有完乘卡",
              "完成一條路線即發放完乘卡，車站累積到蓋章簿中，還可匯出 PDF。"),
             ("免帳號，留在裝置裡",
              "沒有登入，也沒有伺服器。紀錄保存在裝置上，需要時僅透過你自己的 iCloud 同步。")],
        note="路線與車站資料來自各國公共資料，出處記載於應用程式的「資料來源」中。",
        apps=[("Tetsulog", "日本鐵道乘車記錄", "/tetsulog/en/", "tetsulog",
               "日本全國<b>163家公司·571條路線·10,096個車站</b>。"),
              ("Raillog", "韓國鐵道乘車記錄", "/raillog/en/", "raillog",
               "韓國全國<b>17家公司·55條路線·1,191個車站</b>。"),
              ("NYC Subway Log", "紐約地鐵乘車記錄", "/nyc-subway-log/zh-hant/", "nyc-subway-log",
               "紐約地鐵<b>25條路線·475個車站</b>。搭遍每一站的 Subway Challenge 紀錄簿。")],
        more="了解更多 →",
    ),
}

HREFLANG = {"index.html": "ko", "en.html": "en", "ja.html": "ja",
            "zh-hans.html": "zh-Hans", "zh-hant.html": "zh-Hant"}


def url(name):
    return BASE if name == "index.html" else BASE + name


PAGE = """<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — kkiruk studio</title>
<meta name="description" content="{desc}">
<link rel="icon" type="image/png" href="/icons/cats-cute.png">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:image" content="https://www.kkirukstudio.com/og-image.png?v=2">
<meta name="twitter:card" content="summary_large_image">
{alts}
<link rel="canonical" href="{url}">
<link rel="stylesheet" href="/style.css?v=20260714a">
<style>
  .rail-hero {{ padding: 54px 0 8px; }}
  .rail-hero h1 {{ font-size: clamp(30px, 5.4vw, 46px); line-height: 1.18; letter-spacing: -.02em; }}
  .rail-hero .lead {{ margin-top: 16px; max-width: 54ch; color: var(--ink2); font-size: 15px; line-height: 1.75; }}
  .rail-how {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }}
  /* Same surface as .app-card. A hardcoded white card was unreadable
     in the site's night themes (t-midnight/t-evening flip --ink light,
     so light text landed on white). */
  .rail-how .card {{ background: color-mix(in srgb, var(--ink) 5%, transparent);
                     border: 1px solid color-mix(in srgb, var(--ink) 8%, transparent);
                     border-radius: 18px; padding: 22px; }}
  .rail-how h3 {{ font-size: 15.5px; font-weight: 650; letter-spacing: -.01em; color: var(--ink); }}
  .rail-how p {{ font-size: 13.5px; color: var(--ink2); margin-top: 7px; line-height: 1.7; }}
  .rail-note {{ font-size: 12.5px; color: var(--ink2); margin-top: 18px; line-height: 1.7; }}
  @media (max-width: 760px) {{ .rail-how {{ grid-template-columns: 1fr; }} }}
</style>
<script src="/ga.js"></script>
</head>
<body>

<header>
  <div class="bar">
    <a class="wordmark" href="/">kkiruk studio</a>
    <nav class="nav-right">
      <a href="/">{home}</a>
      <select class="lang-sel" onchange="location.href=this.value" aria-label="Language">
{options}
      </select>
    </nav>
  </div>
</header>

<main>

<div class="rail-hero wrap">
  <p class="sec-label reveal">{kicker}</p>
  <h1 class="reveal">{h1}</h1>
  <p class="lead reveal">{lead}</p>
</div>

<section>
  <div class="wrap">
    <p class="sec-label reveal">{cards_label}</p>
    <div class="apps">
{cards}    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <p class="sec-label reveal">{how_label}</p>
    <div class="rail-how">
{how}    </div>
    <p class="rail-note reveal">{note}</p>
  </div>
</section>

</main>

<footer>
  <div class="wrap cols">
    <span>© 2026 kkiruk studio</span>
    <nav class="links">
      <a href="mailto:kkirukstudio.help@gmail.com">kkirukstudio.help@gmail.com</a>
      <a href="https://kkiruk-studio.github.io/privacy-policy-app/" target="_blank" rel="noopener">Privacy</a>
      <a href="https://kkiruk-studio.github.io/terms-of-service-app/" target="_blank" rel="noopener">Terms</a>
    </nav>
  </div>
</footer>

<script src="/app.js?v=20260611"></script>
</body>
</html>
"""


def render(name, c):
    alts = "\n".join(
        f'<link rel="alternate" hreflang="{HREFLANG[n]}" href="{url(n)}">' for n in LOCALES
    ) + f'\n<link rel="alternate" hreflang="x-default" href="{url("en.html")}">'

    options = "\n".join(
        f'        <option value="{url(n).replace(BASE, "/rail/")}"'
        f'{" selected" if n == name else ""}>{LOCALES[n]["label"]}</option>'
        for n in LOCALES)

    cards = "".join(f'''      <a class="app-card reveal" href="{href}">
        <img src="/icons/{icon}.png" alt="{title}">
        <div>
          <h3>{title}</h3>
          <p class="en">{sub}<span class="plat"> · iOS</span></p>
          <p>{body}</p>
          <div class="links"><span>{c['more']}</span></div>
        </div>
      </a>
''' for title, sub, href, icon, body in c["apps"])

    how = "".join(f'''      <div class="card reveal">
        <h3>{h}</h3>
        <p>{p}</p>
      </div>
''' for h, p in c["how"])

    return PAGE.format(url=url(name), alts=alts, options=options,
                       cards=cards, how=how, **{k: v for k, v in c.items()
                                                if k not in ("apps", "how", "label")})


for name, conf in LOCALES.items():
    (ROOT / name).write_text(render(name, conf), encoding="utf-8")
    print(f"rail/{name}")
