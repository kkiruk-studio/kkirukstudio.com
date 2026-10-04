#!/usr/bin/env python3
"""
Build the NYC Subway Log landing page (en / ko / ja / zh-Hant).

Same shape as the Local Link landing (`~/Find Local/LandingPage/locallink/`):
one `build.py` holding the template and per-locale strings, one shared
`assets/style.css`, generated `index.html` + `<lang>/index.html`.

Never edit the generated HTML — change this file and re-run:

    python3 build.py

Design note: the page is the app's own signage system, not a generic
product page. Black field, Helvetica, route bullets, and the nine MTA
trunk colours as a stripe — the same object that runs under the app
icon's wordmark and every in-app page header.
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).parent
BASE_URL = "https://www.kkirukstudio.com/nyc-subway-log/"

# Filled in after App Store approval.
APP_STORE_URL = "https://apps.apple.com/app/id6795853224"

APPLE_SVG = ('<svg viewBox="0 0 384 512" aria-hidden="true"><path d="M318.7 268.7c-.2-36.7 '
             '16.4-64.4 50-84.8-18.8-26.9-47.2-41.7-84.7-44.6-35.5-2.8-74.3 20.7-88.5 '
             '20.7-15 0-49.4-19.7-76.4-19.7C63.3 141.2 4 184.8 4 273.5q0 39.3 14.4 '
             '81.2c12.8 36.7 59 126.7 107.2 125.2 25.2-.6 43-17.9 75.8-17.9 31.8 0 48.3 '
             '17.9 76.4 17.9 48.6-.7 90.4-82.5 102.6-119.3-65.2-30.7-61.7-90-61.7-91.9zm'
             '-56.6-164.2c27.3-32.4 24.8-61.9 24-72.5-24.1 1.4-52 16.4-67.9 34.9-17.5 '
             '19.8-27.8 44.3-25.6 71.9 26.1 2 49.9-11.4 69.5-34.3z"/></svg>')

LANG_LABELS = [("", "EN"), ("ko/", "한국어"), ("ja/", "日本語"), ("zh-hant/", "繁體"), ("zh-hans/", "简体")]

# The ten trunks, in MTA bullet order. (bullets, colour class, name)
TRUNKS = [
    (["A", "C", "E"], "blue", "Eighth Avenue", "IND"),
    (["B", "D", "F", "M"], "orange", "Sixth Avenue", "IND"),
    (["G"], "lime", "Crosstown", "IND"),
    (["J", "Z"], "brown", "Nassau Street", "BMT"),
    (["L"], "gray", "Canarsie", "BMT"),
    (["N", "Q", "R", "W"], "yellow", "Broadway", "BMT"),
    (["S"], "gray", "Shuttles", "—"),
    (["1", "2", "3"], "red", "Broadway–Seventh Av", "IRT"),
    (["4", "5", "6"], "green", "Lexington Avenue", "IRT"),
    (["7"], "purple", "Flushing", "IRT"),
]

MARQUEE_BULLETS = [
    ("A", "blue"), ("C", "blue"), ("E", "blue"), ("B", "orange"), ("D", "orange"),
    ("F", "orange"), ("M", "orange"), ("G", "lime"), ("J", "brown"), ("Z", "brown"),
    ("L", "gray"), ("N", "yellow"), ("Q", "yellow"), ("R", "yellow"), ("W", "yellow"),
    ("S", "gray"), ("1", "red"), ("2", "red"), ("3", "red"), ("4", "green"),
    ("5", "green"), ("6", "green"), ("7", "purple"),
]

# The hero strip animates through the 7's stations — the app's anchor line.
STRIP_STATIONS = ["Flushing–Main St", "Mets–Willets Pt", "111 St", "103 St", "Junction Blvd",
                  "90 St", "82 St", "74 St", "69 St", "61 St", "52 St", "46 St"]

LOCALES = {
    "en": {
        "lang": "en", "dir": "", "font": "",
        "title": "NYC Subway Log — stamp every station you ride",
        "desc": ("A station-bagging tracker for the New York City Subway. All 25 services "
                 "and 475 stations, logged with photos and notes, drawn in MTA's own line colors."),
        "og_title": "NYC Subway Log",
        "og_desc": "All 25 services. All 475 stations. One stamp book.",
        "kicker_num": "25 SERVICES · 475 STATIONS",
        "h1": "Every station<br>you ride, stamped.",
        "sub": ("Mark a station and the line fills in — in the colors you already read off "
                "the wall. Rides from years ago count too."),
        "strip_label": "STATIONS RIDDEN",
        "note": "iPhone · iOS 18+",
        "hero_alt": "The map with ridden lines filled in",
        "chips": [("7", "purple", "Flushing"), ("A", "blue", "8 Avenue"), ("L", "gray", "Canarsie")],
        "how_kicker": "HOW IT WORKS", "how_h2": "How to log the stations you\'ve visited.",
        "steps": [
            ("RIDE", "Take the train", "No check-in, no GPS chase. Log it whenever — on the platform or a month later."),
            ("TAP", "Mark the station", "One tap per station, or set a start and end and log the whole stretch at once."),
            ("COLLECT", "Watch it fill", "The line colors in over real track. Finish one end to end and you get a card for it."),
        ],
        "trunk_kicker": "THE COLOR SYSTEM", "trunk_num": "10 TRUNKS",
        "trunk_h2": "Official MTA line colors.",
        "trunk_lede": ("Line colors, station names, and track geometry come straight from the MTA's "
                       "public GTFS feed — the same data that drives the countdown clocks. Nothing hand-picked."),
        "shots_kicker": "IN THE APP", "shots_num": "01–03", "shots_h2": "What you get.",
        "shots_caps": ["Ridden lines fill in over real track geometry.",
                       "Browse services by division, with their route symbols.",
                       "A stamp book that fills as you go."],
        "feat_kicker": "DETAILS", "feat_num": "06", "feat_h2": "What a full run needs.",
        "feats": [
            ("Two maps", "A real one, and a network view that strips everything away but the subway."),
            ("Five boroughs", "A heatmap that shows where you've actually been — and where you haven't."),
            ("Line complete", "Ride a service end to end and get a card with the route on it."),
            ("Photos and notes", "Attach either to any station visit. Photos stay on your device."),
            ("Rolling stock", "From the R32 Brightliner to the R211. Mark what you've ridden and seen."),
            ("iCloud sync", "Free for everyone. Your records survive a new phone."),
        ],
        "final_h2": "475 stations. How many have you actually seen?",
        "final_lede": "Start with one. The 7 is already in your favorites.",
        "cta_soon": "App Store", "cta_store": "Download on the App Store",
        "f_contact": "Contact", "f_privacy": "Privacy", "f_terms": "Terms",
        "disclaimer": ("NYC Subway Log is an independent app and is not affiliated with, endorsed by, "
                       "or sponsored by the Metropolitan Transportation Authority. Station and route "
                       "data from the MTA's public GTFS feed; land silhouette from NYC OpenData."),
    },
    "ko": {
        "lang": "ko", "dir": "ko/", "font": '"Apple SD Gothic Neo"',
        "title": "NYC Subway Log — 뉴욕 지하철 완주 기록",
        "desc": ("뉴욕 지하철 답사 기록 앱. 25개 노선·475개 역 전부를 사진·메모와 함께 "
                 "기록하고, MTA 공식 노선색으로 지도에 칠합니다."),
        "og_title": "NYC Subway Log",
        "og_desc": "25개 노선, 475개 역, 스탬프북 하나.",
        "kicker_num": "25개 노선 · 475개 역",
        "h1": "탄 역이<br>하나씩 채워집니다.",
        "sub": ("역을 체크하면 노선이 실제 노선색으로 칠해집니다. 예전에 탄 기록도 "
                "날짜를 골라 넣을 수 있습니다."),
        "strip_label": "방문한 역",
        "note": "iPhone · iOS 18+",
        "hero_alt": "탄 노선이 칠해진 지도",
        "chips": [("7", "purple", "플러싱"), ("A", "blue", "8번가"), ("L", "gray", "커네이시")],
        "how_kicker": "사용법", "how_h2": "탄 역을 기록하는 방법",
        "steps": [
            ("탑승", "지하철을 탄다", "체크인도 GPS 추적도 없습니다. 승강장에서든 한 달 뒤든 원할 때 기록하세요."),
            ("기록", "역을 체크한다", "역마다 한 번 누르거나, 출발·도착역을 정해 그 사이를 한 번에 넣습니다."),
            ("수집", "채워지는 걸 본다", "실제 선로 위에 노선색이 칠해집니다. 한 노선을 끝까지 타면 완주 카드가 나옵니다."),
        ],
        "trunk_kicker": "노선색 체계", "trunk_num": "10개 계통",
        "trunk_h2": "MTA 공식 노선색을 사용합니다.",
        "trunk_lede": ("노선색·역명·선로 형상 모두 MTA 가 공개하는 GTFS 피드에서 그대로 가져왔습니다. "
                       "역 전광판을 움직이는 것과 같은 데이터입니다."),
        "shots_kicker": "앱 화면", "shots_num": "01–03", "shots_h2": "앱에서는 이렇게 보여요.",
        "shots_caps": ["탄 노선이 실제 선로 위에 칠해집니다.",
                       "전 노선을 디비전별로, 노선 기호와 함께 확인합니다.",
                       "다닐수록 채워지는 스탬프북."],
        "feat_kicker": "디테일", "feat_num": "06", "feat_h2": "완주까지 필요한 것들.",
        "feats": [
            ("지도 2종", "실제 지도와, 지하철만 남기고 전부 걷어낸 노선망 뷰."),
            ("5개 자치구", "어디를 실제로 다녔고 어디를 안 갔는지 보여주는 히트맵."),
            ("전 구간 완주", "한 노선을 끝까지 타면 그 노선이 그려진 카드를 받습니다."),
            ("사진·메모", "역 방문마다 붙일 수 있습니다. 사진은 기기 안에만 남습니다."),
            ("차량 도감", "R32 브라이트라이너부터 R211 까지. 탄 것과 본 것을 기록합니다."),
            ("iCloud 동기화", "전 사용자 무료. 기기를 바꿔도 기록이 남습니다."),
        ],
        "final_h2": "475개 역. 실제로 몇 개나 가보셨나요?",
        "final_lede": "한 역부터 시작하세요. 7호선은 이미 즐겨찾기에 있습니다.",
        "cta_soon": "App Store", "cta_store": "App Store에서 받기",
        "f_contact": "문의", "f_privacy": "개인정보", "f_terms": "이용약관",
        "disclaimer": ("NYC Subway Log 는 독립 앱이며 MTA(Metropolitan Transportation Authority)와 "
                       "제휴·후원 관계가 없습니다. 역·노선 데이터는 MTA 공개 GTFS 피드, 육지 실루엣은 "
                       "NYC OpenData 를 사용합니다."),
    },
    "ja": {
        "lang": "ja", "dir": "ja/", "font": '"Hiragino Sans"',
        "title": "NYC Subway Log — ニューヨーク地下鉄 全駅記録",
        "desc": ("ニューヨーク地下鉄の乗車記録アプリ。25系統・475駅すべてを写真とメモで残し、"
                 "MTA公式の路線色で地図に塗ります。"),
        "og_title": "NYC Subway Log",
        "og_desc": "25系統、475駅、スタンプ帳ひとつ。",
        "kicker_num": "25系統 · 475駅",
        "h1": "乗った駅が、<br>ひとつずつ埋まる。",
        "sub": ("駅を記録すると路線が実際の路線色で塗られます。昔乗った記録も日付を選んで残せます。"),
        "strip_label": "記録した駅",
        "note": "iPhone · iOS 18+",
        "hero_alt": "乗った路線が塗られた地図",
        "chips": [("7", "purple", "フラッシング"), ("A", "blue", "8番街"), ("L", "gray", "カナーシー")],
        "how_kicker": "使い方", "how_h2": "訪れた駅を記録する方法。",
        "steps": [
            ("乗る", "地下鉄に乗る", "チェックインもGPS追跡もありません。ホームでも1か月後でも、好きなときに記録できます。"),
            ("記録", "駅を記録する", "駅ごとに1タップ、または始点と終点を選んでその区間をまとめて登録。"),
            ("集める", "埋まっていく", "実際の線路の上が路線色で塗られます。1系統を乗り通すと記念カードが出ます。"),
        ],
        "trunk_kicker": "路線色の体系", "trunk_num": "10系統",
        "trunk_h2": "MTA公式の路線色を使っています。",
        "trunk_lede": ("路線色・駅名・線路形状はすべてMTAが公開するGTFSフィードそのままです。"
                       "駅の発車標を動かしているのと同じデータです。"),
        "shots_kicker": "アプリ画面", "shots_num": "01–03", "shots_h2": "収録内容。",
        "shots_caps": ["乗った路線が実際の線路の上に塗られます。",
                       "各系統を区分ごとに、路線マークと一緒に確認。",
                       "乗るほど埋まるスタンプ帳。"],
        "feat_kicker": "詳細", "feat_num": "06", "feat_h2": "完乗までに必要なもの。",
        "feats": [
            ("地図2種", "実際の地図と、地下鉄だけを残して他を取り払ったネットワーク表示。"),
            ("5行政区", "どこに実際に行き、どこに行っていないかを示すヒートマップ。"),
            ("全区間走破", "1系統を乗り通すと、その路線が描かれたカードがもらえます。"),
            ("写真とメモ", "駅の記録ごとに添付できます。写真は端末内にのみ残ります。"),
            ("車両図鑑", "R32ブライトライナーからR211まで。乗った車両と見た車両を記録。"),
            ("iCloud同期", "全ユーザー無料。端末を替えても記録は残ります。"),
        ],
        "final_h2": "475駅。実際に何駅行きましたか？",
        "final_lede": "まず1駅から。7系統はすでにお気に入りに入っています。",
        "cta_soon": "App Store", "cta_store": "App Storeでダウンロード",
        "f_contact": "お問い合わせ", "f_privacy": "プライバシー", "f_terms": "利用規約",
        "disclaimer": ("NYC Subway Log は独立したアプリであり、MTA（Metropolitan Transportation "
                       "Authority）との提携・後援関係はありません。駅・路線データはMTA公開のGTFSフィード、"
                       "陸地シルエットはNYC OpenDataを使用しています。"),
    },
    "zh-hant": {
        "lang": "zh-Hant", "dir": "zh-hant/", "font": '"PingFang TC"',
        "title": "NYC Subway Log — 紐約地鐵全站紀錄",
        "desc": ("紐約地鐵搭乘紀錄應用程式。收錄全部25條路線・475個車站，可加照片與筆記，"
                 "並以 MTA 官方路線色繪製地圖。"),
        "og_title": "NYC Subway Log",
        "og_desc": "25條路線、475個車站、一本蓋章簿。",
        "kicker_num": "25條路線 · 475個車站",
        "h1": "搭過的車站，<br>一個一個填滿。",
        "sub": ("記錄車站後，路線會以實際路線色填滿。以前搭過的紀錄也能選日期補上。"),
        "strip_label": "已記錄車站",
        "note": "iPhone · iOS 18+",
        "hero_alt": "填滿搭過路線的地圖",
        "chips": [("7", "purple", "法拉盛"), ("A", "blue", "第八大道"), ("L", "gray", "卡納西")],
        "how_kicker": "使用方式", "how_h2": "這樣記錄去過的車站。",
        "steps": [
            ("搭乘", "搭上地鐵", "不需打卡，不追 GPS。在月台上或一個月後，想記錄時再記錄。"),
            ("記錄", "標記車站", "每站點一下，或選好起訖站一次登錄整段。"),
            ("收集", "看它填滿", "實際軌道上會被路線色填滿。搭完整條路線就會產生紀念卡。"),
        ],
        "trunk_kicker": "路線色體系", "trunk_num": "10 條幹線",
        "trunk_h2": "採用 MTA 官方路線配色。",
        "trunk_lede": ("路線色、站名與軌道形狀全部直接取自 MTA 公開的 GTFS 資料，"
                       "與驅動車站到站顯示器的是同一份資料。"),
        "shots_kicker": "應用畫面", "shots_num": "01–03", "shots_h2": "內容。",
        "shots_caps": ["搭過的路線會填在實際軌道上。",
                       "全部路線依分區排列，各自帶著路線標誌。",
                       "越搭越滿的蓋章簿。"],
        "feat_kicker": "細節", "feat_num": "06", "feat_h2": "跑完全程需要的東西。",
        "feats": [
            ("兩種地圖", "真實地圖，以及只留下地鐵、其餘全部拿掉的路網檢視。"),
            ("五個行政區", "顯示你實際去過哪裡、還沒去哪裡的熱點圖。"),
            ("全線完乘", "搭完一條路線，就會得到印有該路線的卡片。"),
            ("照片與筆記", "每次車站紀錄都能附加。照片只留在你的裝置上。"),
            ("車輛圖鑑", "從 R32 Brightliner 到 R211。記錄搭過與看過的車輛。"),
            ("iCloud 同步", "所有使用者免費。換手機紀錄也不會消失。"),
        ],
        "final_h2": "475 個車站。你實際去過幾個？",
        "final_lede": "從一站開始。7 號線已經在你的最愛裡。",
        "cta_soon": "App Store", "cta_store": "在 App Store 下載",
        "f_contact": "聯絡", "f_privacy": "隱私權", "f_terms": "使用條款",
        "disclaimer": ("NYC Subway Log 為獨立應用程式，與 MTA（Metropolitan Transportation "
                       "Authority）無合作或贊助關係。車站與路線資料取自 MTA 公開的 GTFS 資料，"
                       "陸地輪廓取自 NYC OpenData。"),
    },
    "zh-hans": {
        "lang": "zh-Hans", "dir": "zh-hans/", "font": '"PingFang SC"',
        "title": "NYC Subway Log — 纽约地铁全站记录",
        "desc": ("纽约地铁乘坐记录应用程序。收录全部25条路线・475个车站，可加照片与笔记，"
                 "并以 MTA 官方路线色绘制地图。"),
        "og_title": "NYC Subway Log",
        "og_desc": "25条路线、475个车站、一本盖章簿。",
        "kicker_num": "25条路线 · 475个车站",
        "h1": "搭过的车站，<br>一个一个填满。",
        "sub": ("记录车站后，路线会以实际路线色填满。以前搭过的记录也能选日期补上。"),
        "strip_label": "已记录车站",
        "note": "iPhone · iOS 18+",
        "hero_alt": "填满搭过路线的地图",
        "chips": [("7", "purple", "法拉盛"), ("A", "blue", "第八大道"), ("L", "gray", "卡纳西")],
        "how_kicker": "使用方式", "how_h2": "这样记录去过的车站。",
        "steps": [
            ("乘坐", "搭上地铁", "不需打卡，不追 GPS。在月台上或一个月后，想记录时再记录。"),
            ("记录", "标记车站", "每站点一下，或选好起讫站一次登录整段。"),
            ("收集", "看它填满", "实际轨道上会被路线色填满。搭完整条路线就会产生纪念卡。"),
        ],
        "trunk_kicker": "路线色体系", "trunk_num": "10 条干线",
        "trunk_h2": "采用 MTA 官方路线配色。",
        "trunk_lede": ("路线色、站名与轨道形状全部直接取自 MTA 公开的 GTFS 数据，"
                       "与驱动车站到站显示器的是同一份数据。"),
        "shots_kicker": "应用画面", "shots_num": "01–03", "shots_h2": "内容。",
        "shots_caps": ["搭过的路线会填在实际轨道上。",
                       "全部路线依分区排列，各自带着路线标志。",
                       "越搭越满的盖章簿。"],
        "feat_kicker": "细节", "feat_num": "06", "feat_h2": "跑完全程需要的东西。",
        "feats": [
            ("两种地图", "真实地图，以及只留下地铁、其余全部拿掉的路网查看。"),
            ("五个行政区", "显示你实际去过哪里、还没去哪里的热点图。"),
            ("全线完乘", "搭完一条路线，就会得到印有该路线的卡片。"),
            ("照片与笔记", "每次车站记录都能附加。照片只留在你的设备上。"),
            ("车辆图鉴", "从 R32 Brightliner 到 R211。记录搭过与看过的车辆。"),
            ("iCloud 同步", "所有用户免费。换手机记录也不会消失。"),
        ],
        "final_h2": "475 个车站。你实际去过几个？",
        "final_lede": "从一站开始。7 号线已经在你的最爱里。",
        "cta_soon": "App Store", "cta_store": "在 App Store 下载",
        "f_contact": "联系", "f_privacy": "隐私权", "f_terms": "使用条款",
        "disclaimer": ("NYC Subway Log 为独立应用程序，与 MTA（Metropolitan Transportation "
                       "Authority）无合作或赞助关系。车站与路线数据取自 MTA 公开的 GTFS 数据，"
                       "陆地轮廓取自 NYC OpenData。"),
    },
}


def bullet(glyph, color, cls="bullet"):
    return f'<span class="{cls} b-{color}">{glyph}</span>'


def hreflang_block():
    lines = [f'<link rel="alternate" hreflang="x-default" href="{BASE_URL}">']
    for loc in LOCALES.values():
        lines.append(f'<link rel="alternate" hreflang="{loc["lang"]}" href="{BASE_URL}{loc["dir"]}">')
    return "\n".join(lines)


def lang_nav(cur_dir, rel):
    out = []
    for d, label in LANG_LABELS:
        href = (rel + d) if d else (rel if rel else "./")
        cls = ' class="on"' if d == cur_dir else ""
        out.append(f'<a href="{href}"{cls}>{label}</a>')
    return "".join(out)


def badge(loc, el_id):
    disabled = "" if APP_STORE_URL else ' aria-disabled="true"'
    href = APP_STORE_URL or "#"
    label = loc["cta_store"] if APP_STORE_URL else loc["cta_soon"]
    return f'<a class="badge" id="{el_id}" href="{href}"{disabled}>{APPLE_SVG}<span>{label}</span></a>'


def render(key):
    loc = LOCALES[key]
    rel = "../" if loc["dir"] else ""
    font_override = (f'<style>body{{font-family:"Helvetica Neue",Helvetica,Arial,'
                     f'-apple-system,{loc["font"]},sans-serif}}</style>') if loc["font"] else ""

    chips = "".join(
        f'<div class="chip c{i+1}">{bullet(g, c)}{name}</div>'
        for i, (g, c, name) in enumerate(loc["chips"]))
    marquee = "".join(bullet(g, c) for g, c in MARQUEE_BULLETS * 2)
    steps = "".join(
        f'<div class="step"><span class="n">0{i+1}</span><span class="tag">{tag}</span>'
        f'<h3>{h}</h3><p>{p}</p></div>'
        for i, (tag, h, p) in enumerate(loc["steps"]))
    trunks = "".join(
        '<div class="trunk"><div class="bullets">%s</div><span class="name">%s</span>'
        '<span class="div">%s</span></div>'
        % ("".join(bullet(g, color) for g in glyphs), name, div)
        for glyphs, color, name, div in TRUNKS)
    shot_files = ["1-map", "2-lines", "3-stamps"]
    shots = "".join(
        f'<figure><div class="phone"><img src="{rel}assets/shot-{f}.png" alt="{cap}" '
        f'loading="lazy"><div class="island"></div></div><figcaption>{cap}</figcaption></figure>'
        for f, cap in zip(shot_files, loc["shots_caps"]))
    feats = "".join(f'<div class="feat"><h3>{h}</h3><p>{p}</p></div>' for h, p in loc["feats"])
    dots = "".join('<span class="dot"></span>' for _ in STRIP_STATIONS)

    return f"""<!doctype html>
<html lang="{loc['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{loc['title']}</title>
<meta name="description" content="{loc['desc']}">
<meta property="og:title" content="{loc['og_title']}">
<meta property="og:description" content="{loc['og_desc']}">
<meta property="og:image" content="{BASE_URL}assets/icon-512.png">
<meta property="og:type" content="website">
<meta name="theme-color" content="#000000">
<link rel="canonical" href="{BASE_URL}{loc['dir']}">
{hreflang_block()}
<link rel="icon" type="image/png" href="{rel}assets/icon-180.png">
<link rel="apple-touch-icon" href="{rel}assets/icon-180.png">
<link rel="stylesheet" href="{rel}assets/style.css">
{font_override}
</head>
<body>

<div class="stripe" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>

<nav>
  <div class="wrap">
    <a class="wordmark" href="{rel if rel else './'}"><img src="{rel}assets/icon-180.png" alt=""><span>NYC SUBWAY LOG</span></a>
    <div class="lang">{lang_nav(loc['dir'], rel)}</div>
  </div>
</nav>

<header class="hero">
  <div class="wrap">
    <div>
      <div class="kicker"><span>NYC SUBWAY LOG</span><span class="rule"></span><span class="num">{loc['kicker_num']}</span></div>
      <h1>{loc['h1']}</h1>
      <div class="strip">
        <div class="rail"><div class="fill" id="stripFill"></div><div class="dots" id="stripDots">{dots}</div></div>
        <div class="read"><b id="stripCount">0</b><span>{loc['strip_label']}</span></div>
      </div>
      <p class="sub">{loc['sub']}</p>
      <div class="cta">
        {badge(loc, 'storeLink')}
        <span class="note">{loc['note']}</span>
      </div>
    </div>
    <div class="phone-col">
      {chips}
      <div class="phone"><img src="{rel}assets/shot-1-map.png" alt="{loc['hero_alt']}"><div class="island"></div></div>
    </div>
  </div>
</header>

<div class="marquee" aria-hidden="true"><div class="track">{marquee}</div></div>

<section>
  <div class="wrap">
    <div class="kicker"><span>{loc['how_kicker']}</span><span class="rule"></span><span class="num">01–03</span></div>
    <h2>{loc['how_h2']}</h2>
    <div class="steps">{steps}</div>
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap">
    <div class="kicker"><span>{loc['trunk_kicker']}</span><span class="rule"></span><span class="num">{loc['trunk_num']}</span></div>
    <h2>{loc['trunk_h2']}</h2>
    <p class="lede">{loc['trunk_lede']}</p>
    <div class="trunks">{trunks}</div>
  </div>
</section>

<section class="shots">
  <div class="wrap">
    <div class="kicker"><span>{loc['shots_kicker']}</span><span class="rule"></span><span class="num">{loc['shots_num']}</span></div>
    <h2>{loc['shots_h2']}</h2>
    <div class="row">{shots}</div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="kicker"><span>{loc['feat_kicker']}</span><span class="rule"></span><span class="num">{loc['feat_num']}</span></div>
    <h2>{loc['feat_h2']}</h2>
    <div class="grid6">{feats}</div>
  </div>
</section>

<section class="final">
  <div class="wrap">
    <h2>{loc['final_h2']}</h2>
    <p class="lede">{loc['final_lede']}</p>
    <div class="cta">{badge(loc, 'storeLink2')}</div>
  </div>
</section>

<footer>
  <div class="wrap">
    <div class="brand"><img src="{rel}assets/icon-180.png" alt=""><strong>kkiruk studio</strong></div>
    <div class="links">
      <a href="mailto:kkirukstudio.help@gmail.com">{loc['f_contact']}</a>
      <a href="/legal/privacy/">{loc['f_privacy']}</a>
      <a href="/legal/terms/">{loc['f_terms']}</a>
    </div>
  </div>
  <div class="wrap"><p class="disclaimer">{loc['disclaimer']}</p></div>
  <div class="wrap" style="margin-top:14px">© 2026 kkiruk studio</div>
</footer>

<script>
  // Set this after App Store approval (e.g. https://apps.apple.com/app/id1234567890).
  const APP_STORE_URL = {json.dumps(APP_STORE_URL)};
  if (APP_STORE_URL) {{
    for (const id of ["storeLink", "storeLink2"]) {{
      const el = document.getElementById(id);
      if (el) {{ el.href = APP_STORE_URL; el.removeAttribute("aria-disabled"); }}
    }}
  }}

  // Hero strip: stations fill in one by one, the way the line does in
  // the app. Pauses for readers who asked for reduced motion.
  (function () {{
    const dots = Array.from(document.querySelectorAll("#stripDots .dot"));
    const fill = document.getElementById("stripFill");
    const count = document.getElementById("stripCount");
    if (!dots.length || !fill || !count) return;
    const TOTAL = 475;
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduce) {{
      dots.forEach(d => d.classList.add("on"));
      fill.style.width = "100%";
      count.textContent = TOTAL;
      return;
    }}
    let i = 0;
    setInterval(function () {{
      if (i >= dots.length) {{
        i = 0;
        dots.forEach(d => d.classList.remove("on"));
        fill.style.width = "0%";
        count.textContent = "0";
        return;
      }}
      dots[i].classList.add("on");
      fill.style.width = (i / (dots.length - 1) * 100) + "%";
      count.textContent = Math.round((i + 1) / dots.length * TOTAL);
      i++;
    }}, 520);
  }})();
</script>
</body>
</html>
"""


for key, loc in LOCALES.items():
    out_dir = ROOT / loc["dir"] if loc["dir"] else ROOT
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "index.html").write_text(render(key), encoding="utf-8")
    print(f"wrote {(out_dir / 'index.html').relative_to(ROOT)}")

# Preserve discovery metadata and visible product facts after regeneration.
if __name__ == "__main__":
    import runpy as _seo_runpy
    from pathlib import Path as _SeoPath
    _seo_runpy.run_path(str(_SeoPath(__file__).resolve().parent.parent / "gen" / "refresh_seo.py"), run_name="__main__")
