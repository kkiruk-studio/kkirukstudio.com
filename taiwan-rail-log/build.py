#!/usr/bin/env python3
"""
Build the 鐵道誌 / Taiwan Rail Log landing page (zh-Hant root, en / ja / ko).

Same shape as the sibling rail landings (`~/kkirukstudio-site/tetsulog/`,
`~/kkirukstudio-site/nyc-subway-log/`): one `build.py` holding the template
and per-locale strings, one shared `assets/style.css`, generated
`index.html` + `<lang>/index.html`.

Never edit the generated HTML — change this file and re-run:

    python3 sync_assets.py   # icon + raw screenshots from the app repo
    python3 make_map.py      # only when the seed / county outlines change
    python3 build.py

Design note: the page is the app icon's object — the 臺鐵 站名牌 (blue frame,
white panel, adjacent-station band) — over the app's own paper / burgundy
tokens. The hero demo is the app's map: the 39 real lines in grey, then the
環島 loop, 高鐵, a branch line, 阿里山 and the metros paint in, stations ink
in, and a 完乘 stamp lands.

Copy source of truth: TwraillogApp/fastlane/metadata/<locale>/. No live /
real-time map claims (not shipped). No competitor comparisons.
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).parent
BASE_URL = "https://www.kkirukstudio.com/taiwan-rail-log/"

# Filled in after App Store approval. While empty, both CTAs render as a
# disabled "coming soon" pill and the final lede uses `final_soon`.
# (gen/check_stale.py flags an empty value on purpose — fill it on launch day,
# then register the slug in check_stale APP_DIRS and gen_jsonld APPS.)
APP_STORE_URL = "https://apps.apple.com/app/id6816993501"

APPLE_SVG = ('<svg viewBox="0 0 384 512" aria-hidden="true"><path d="M318.7 268.7c-.2-36.7 '
             '16.4-64.4 50-84.8-18.8-26.9-47.2-41.7-84.7-44.6-35.5-2.8-74.3 20.7-88.5 '
             '20.7-15 0-49.4-19.7-76.4-19.7C63.3 141.2 4 184.8 4 273.5q0 39.3 14.4 '
             '81.2c12.8 36.7 59 126.7 107.2 125.2 25.2-.6 43-17.9 75.8-17.9 31.8 0 48.3 '
             '17.9 76.4 17.9 48.6-.7 90.4-82.5 102.6-119.3-65.2-30.7-61.7-90-61.7-91.9zm'
             '-56.6-164.2c27.3-32.4 24.8-61.9 24-72.5-24.1 1.4-52 16.4-67.9 34.9-17.5 '
             '19.8-27.8 44.3-25.6 71.9 26.1 2 49.9-11.4 69.5-34.3z"/></svg>')

LANG_LABELS = [("", "繁體中文"), ("zh-hans/", "简体中文"), ("en/", "EN"), ("ja/", "日本語"), ("ko/", "한국어")]

RAILMAP_SVG = (ROOT / "_src" / "railmap.svg").read_text(encoding="utf-8").strip()
OSM_CREDIT = "© OpenStreetMap contributors"

# Real line names + colours (LineColorRegistry.swift) — shared by every locale,
# the way the Tetsulog landing keeps its marquee in Japanese. `None` colour =
# a highlighted concept word.
MARQUEE_ITEMS = [
    ("縱貫線", "#0B4EA2"), ("平溪線", "#5B96D6"), ("集集線", "#4F8BCB"), ("內灣線", "#5E8FCC"),
    ("南迴線", "#163F86"), ("台灣高鐵", "#E8722A"), ("淡水信義線", "#FF0000"), ("板南線", "#007EC7"),
    ("文湖線", "#A74C00"), ("機場捷運", "#8E7CC3"), ("高雄捷運紅線", "#FF0000"), ("阿里山線", "#B3143C"),
    ("完乘", None), ("印章簿", None), ("前面展望", None),
]

# Operator chips in the value section: (key, colour, line count). Counts are
# from Resources/seed.json (16 + 1 + 9 + 4 + 1 + 1 + 3 + 4 = 39).
OPERATORS = [("tra", "#0B4EA2", 16), ("thsr", "#E8722A", 1), ("trtc", "#E3002C", 9),
             ("ntmc", "#5FB7E5", 4), ("tymc", "#8E7CC3", 1), ("tmrt", "#7AB929", 1),
             ("krtc", "#F08A00", 3), ("afr", "#B3143C", 4)]

SHOTS = ["1-map", "2-flyover", "4-stamps"]

LOCALES = {
    "zh-hant": {
        "dir": "", "lang": "zh-Hant", "shots": "zh-hant", "font": None,
        "title": "鐵道誌 — 台灣鐵道乘車紀錄",
        "desc": ("點一下車站就記下乘車，搭過的路線會在地圖上慢慢染上顏色。收錄全臺 39 條路線、589 個車站："
                 "臺鐵、高鐵、捷運與輕軌、阿里山林業鐵路。印章簿、完乘卡片、前面展望。"),
        "og_title": "鐵道誌 — 台灣鐵道乘車紀錄",
        "og_desc": "搭過的路線，會在地圖上慢慢染上顏色。全臺 39 條路線・589 個車站。",
        "brand": "鐵道誌",
        "sign_prev": "39 條路線", "sign_next": "589 個車站",
        "h1": "搭過的路線，<br>在地圖上<em>慢慢染色</em>。",
        "sub": ("點一下車站就記下這趟乘車，路線圖會逐漸變成只屬於你的完乘地圖。臺鐵正式路線、台灣高鐵、"
                "北北桃中高的捷運與輕軌，還有阿里山林業鐵路——全臺 39 條路線、589 個車站，收進同一本紀錄。"),
        "cta_note": "iPhone・iPad ・ iOS 18+ ・ 基本功能免費",
        "badge_soon": "即將上架", "badge_live": "下載",
        "stamp": "完乘",
        "read_label": "已記錄車站",
        "how_kicker": "使用方式", "how_num": "01–03",
        "how_h2": "從點一下車站，到<em>蓋下印章</em>。",
        "steps": [
            ("記錄", "點車站，記下乘車", "點地圖上的車站即可。選好起訖站能一次登錄整段區間，過去的旅程也能選日期補登。"),
            ("上色", "路線染上顏色", "搭過的區間以路線代表色塗滿，沒搭過的保持灰色。切換成只看未搭乘路線，下一趟去哪一目瞭然。"),
            ("收集", "印章慢慢累積", "造訪過的車站化作印章，收進你的印章簿。完乘一條路線，就會出現可以分享的紀念卡片。"),
        ],
        "value_kicker": "全臺資料", "value_num": "臺鐵・高鐵・捷運・林鐵",
        "value_h2": "全臺 <em>39 條路線・589 個車站</em>，一個 App 全收錄。",
        "value_lede": ("從縱貫線、南迴線到平溪線、集集線、內灣線，臺鐵 16 條正式路線全部收錄；再加上台灣高鐵、"
                       "臺北・新北・桃園・臺中・高雄的捷運與輕軌，以及阿里山林業鐵路。"
                       "臺鐵、高鐵與捷運共用的轉乘站會整合在一起。"),
        "stats": [("39", "條路線"), ("589", "個車站"), ("22", "縣市熱度地圖"), ("29", "種車款圖鑑")],
        "ops": {"tra": "臺鐵", "thsr": "台灣高鐵", "trtc": "臺北捷運", "ntmc": "新北捷運",
                "tymc": "桃園捷運", "tmrt": "臺中捷運", "krtc": "高雄捷運", "afr": "阿里山林業鐵路"},
        "shots_kicker": "畫面", "shots_num": "iOS",
        "shots_h2": "邊旅行邊寫下的<em>乘車紀錄。</em>",
        "shots_caps": ["搭過的路線，塗在地圖上", "搭過的區間，用 3D 衛星再飛一次", "造訪過的車站，化作一枚印章"],
        "beta": "BETA",
        "feat_kicker": "細節", "feat_num": "06",
        "feat_h2": "為記錄的人準備的<em>貼心設計</em>。",
        "feats": [
            ("前面展望", "BETA", "在衛星影像與 3D 建築之上，沿著鐵軌回看搭過的路段；地下區間則飛越地面街道上方。也能匯出成影片分享。"),
            ("整段區間一次輸入", None, "選好起點與終點，區間內的車站一次標記。乘車日期可自由選擇，GPS 也能找出附近車站當場記錄。"),
            ("完乘紀念卡片", None, "完乘一條路線、車站數達標時會出現紀念卡片，可直接分享到社群。"),
            ("22 縣市熱度地圖", "PRO", "以深淺呈現各縣市走過多少，旅行的足跡一眼看懂。另有以 A4 版面輸出的 PDF 印章簿。"),
            ("車輛圖鑑 29 種", None, "從高鐵 700T、普悠瑪號、太魯閣號到各地捷運與阿里山的蒸汽機車。"),
            ("紀錄留在你手上", None, "iCloud 同步，換機也能原樣接續（免費）。隨時可匯出 JSON 備份與 Excel 可開啟的 CSV。"),
        ],
        "final_h2": "從下一站開始，畫出你的<em>完乘地圖</em>。",
        "final_live": "臺鐵全線完乘、搭火車環島，或只是週末的支線小旅行——從第一站開始記。",
        "final_soon": "即將在 App Store 上架。臺鐵全線完乘、搭火車環島，或只是週末的支線小旅行——從第一站開始記。",
        "f_contact": "聯絡我們", "f_privacy": "隱私權政策", "f_terms": "使用條款",
        "disclaimer": ("臺鐵車站資料取自政府資料開放平臺（國營臺灣鐵路股份有限公司，政府資料開放授權條款第1版）；"
                       "路線軌跡與臺鐵以外的車站資料來自 OpenStreetMap（© OpenStreetMap contributors）。"
                       "鐵道誌為獨立開發的 App，與國營臺灣鐵路股份有限公司、台灣高速鐵路股份有限公司及各捷運營運單位"
                       "均無合作或隸屬關係。"),
    },
    "zh-hans": {
        "dir": "zh-hans/", "lang": "zh-Hans", "shots": "zh-hant", "font": '"PingFang SC", "Microsoft YaHei"',
        "title": "铁道志 — 台湾铁道乘车记录",
        "desc": ("点一下车站就记下乘车，搭过的路线会在地图上慢慢染上颜色。收录全台 39 条路线、589 个车站："
                 "台铁、高铁、捷运与轻轨、阿里山林业铁路。印章簿、完乘卡片、前面展望。"),
        "og_title": "铁道志 — 台湾铁道乘车记录",
        "og_desc": "搭过的路线，会在地图上慢慢染上颜色。全台 39 条路线・589 个车站。",
        "brand": "铁道志",
        "sign_prev": "39 条路线", "sign_next": "589 个车站",
        "h1": "搭过的路线，<br>在地图上<em>慢慢染色</em>。",
        "sub": ("点一下车站就记下这趟乘车，路线图会逐渐变成只属于你的完乘地图。台铁正式路线、台湾高铁、"
                "北北桃中高的捷运与轻轨，还有阿里山林业铁路——全台 39 条路线、589 个车站，收进同一本记录。"),
        "cta_note": "iPhone・iPad ・ iOS 18+ ・ 基本功能免费",
        "badge_soon": "即将上架", "badge_live": "下载",
        "stamp": "完乘",
        "read_label": "已记录车站",
        "how_kicker": "使用方式", "how_num": "01–03",
        "how_h2": "从点一下车站，到<em>盖下印章</em>。",
        "steps": [
            ("记录", "点车站，记下乘车", "点地图上的车站即可。选好起讫站能一次登录整段区间，过去的旅程也能选日期补登。"),
            ("上色", "路线染上颜色", "搭过的区间以路线代表色涂满，没搭过的保持灰色。切换成只看未乘坐路线，下一趟去哪一目了然。"),
            ("收集", "印章慢慢累积", "造访过的车站化作印章，收进你的印章簿。完乘一条路线，就会出现可以分享的纪念卡片。"),
        ],
        "value_kicker": "全台数据", "value_num": "台铁・高铁・捷运・林铁",
        "value_h2": "全台 <em>39 条路线・589 个车站</em>，一个 App 全收录。",
        "value_lede": ("从纵贯线、南回线到平溪线、集集线、内湾线，台铁 16 条正式路线全部收录；再加上台湾高铁、"
                       "台北・新北・桃园・台中・高雄的捷运与轻轨，以及阿里山林业铁路。"
                       "台铁、高铁与捷运共用的转乘站会集成在一起。"),
        "stats": [("39", "条路线"), ("589", "个车站"), ("22", "县市热度地图"), ("29", "种车款图鉴")],
        "ops": {"tra": "台铁", "thsr": "台湾高铁", "trtc": "台北捷运", "ntmc": "新北捷运",
                "tymc": "桃园捷运", "tmrt": "台中捷运", "krtc": "高雄捷运", "afr": "阿里山林业铁路"},
        "shots_kicker": "画面", "shots_num": "iOS",
        "shots_h2": "边旅行边写下的<em>乘车记录。</em>",
        "shots_caps": ["搭过的路线，涂在地图上", "搭过的区间，用 3D 卫星再飞一次", "造访过的车站，化作一枚印章"],
        "beta": "BETA",
        "feat_kicker": "细节", "feat_num": "06",
        "feat_h2": "为记录的人准备的<em>贴心设计</em>。",
        "feats": [
            ("前面展望", "BETA", "在卫星图像与 3D 建筑之上，沿着铁轨回看搭过的路段；地下区间则飞越地面街道上方。也能导出成视频分享。"),
            ("整段区间一次输入", None, "选好起点与终点，区间内的车站一次标记。乘车日期可自由选择，GPS 也能找出附近车站当场记录。"),
            ("完乘纪念卡片", None, "完乘一条路线、车站数达标时会出现纪念卡片，可直接分享到社区。"),
            ("22 县市热度地图", "PRO", "以深浅呈现各县市走过多少，旅行的足迹一眼看懂。另有以 A4 版面输出的 PDF 印章簿。"),
            ("车辆图鉴 29 种", None, "从高铁 700T、普悠玛号、太鲁阁号到各地捷运与阿里山的蒸汽机车。"),
            ("记录留在你手上", None, "iCloud 同步，换机也能原样接续（免费）。随时可导出 JSON 备份与 Excel 可打开的 CSV。"),
        ],
        "final_h2": "从下一站开始，画出你的<em>完乘地图</em>。",
        "final_live": "台铁全线完乘、搭火车环岛，或只是周末的支线小旅行——从第一站开始记。",
        "final_soon": "即将在 App Store 上架。台铁全线完乘、搭火车环岛，或只是周末的支线小旅行——从第一站开始记。",
        "f_contact": "联系我们", "f_privacy": "隐私权政策", "f_terms": "使用条款",
        "disclaimer": ("台铁车站数据取自政府数据开放平台（国营台湾铁路股份有限公司，政府数据开放授权条款第1版）；"
                       "路线轨迹与台铁以外的车站数据来自 OpenStreetMap（© OpenStreetMap contributors）。"
                       "铁道志为独立开发的 App，与国营台湾铁路股份有限公司、台湾高速铁路股份有限公司及各捷运营运单位"
                       "均无合作或隶属关系。"),
    },
    "en": {
        "dir": "en/", "lang": "en", "shots": "en", "font": None,
        "title": "Taiwan Rail Log — Train, MRT & HSR ride log for Taiwan",
        "desc": ("Tap a station to log the ride and watch Taiwan's rail map fill in with color. 39 lines and 589 "
                 "stations: TRA, High Speed Rail, metro and light rail, and the Alishan Forest Railway."),
        "og_title": "Taiwan Rail Log (鐵道誌)",
        "og_desc": "Every line you ride fills in with color. 39 lines · 589 stations across Taiwan.",
        "brand": "Taiwan Rail Log",
        "sign_prev": "39 LINES", "sign_next": "589 STATIONS",
        "h1": "Every line you ride<br><em>fills in with color</em>.",
        "sub": ("Tap a station to log the ride, and Taiwan's rail map slowly becomes your own. The TRA network, "
                "Taiwan High Speed Rail, metro and light rail in Taipei, New Taipei, Taoyuan, Taichung and "
                "Kaohsiung, and the Alishan Forest Railway — 39 lines and 589 stations in one log."),
        "cta_note": "iPhone & iPad · iOS 18+ · Free, Pro available",
        "badge_soon": "Coming soon", "badge_live": "Download on the",
        "stamp": "完乘",
        "read_label": "STATIONS LOGGED",
        "how_kicker": "HOW IT WORKS", "how_num": "01–03",
        "how_h2": "From a tap on the map to <em>a stamp in the book</em>.",
        "steps": [
            ("LOG", "Tap a station", "Tap any station on the map, or pick a start and end to log a whole stretch at once. Backfill trips from years ago by picking the date."),
            ("COLOR", "Watch the line fill in", "Ridden stretches are painted in the line's real color; the rest stays grey. Filter to unridden lines when you plan the next trip."),
            ("COLLECT", "Stamps pile up", "Every station you visit becomes a stamp in your stamp book. Finish a line and a card appears, ready to share."),
        ],
        "value_kicker": "ALL OF TAIWAN", "value_num": "TRA · HSR · METRO · FOREST RAILWAY",
        "value_h2": "<em>39 lines · 589 stations</em> — one app for Taiwan's railways.",
        "value_lede": ("All 16 TRA lines, from the Western and South-Link trunk lines to the Pingxi, Jiji and Neiwan "
                       "branches; Taiwan High Speed Rail; metro and light rail in five cities; and the Alishan "
                       "Forest Railway. Transfer stations shared by TRA, HSR and metro are grouped as one."),
        "stats": [("39", "lines"), ("589", "stations"), ("22", "county heatmap"), ("29", "trains in the rolling stock book")],
        "ops": {"tra": "TRA", "thsr": "Taiwan High Speed Rail", "trtc": "Taipei Metro", "ntmc": "New Taipei Metro",
                "tymc": "Taoyuan Metro", "tmrt": "Taichung MRT", "krtc": "Kaohsiung MRT", "afr": "Alishan Forest Railway"},
        "shots_kicker": "SCREENS", "shots_num": "iOS",
        "shots_h2": "A notebook for <em>your Taiwan rail trips.</em>",
        "shots_caps": ["The lines you ride, painted on the map", "Fly the stretch you rode again, over 3D satellite imagery", "Every station you visit becomes a stamp"],
        "beta": "BETA",
        "feat_kicker": "DETAILS", "feat_num": "06",
        "feat_h2": "Built for <em>the record-keeper</em>.",
        "feats": [
            ("Cab View", "BETA", "Follow the stretches you rode from above, over satellite imagery and 3D buildings. Underground, you fly over the streets above. Export the flight as a video."),
            ("Log a whole stretch", None, "Pick a start and end station and every stop between is marked at once. Any date works, and GPS finds the station you're standing at."),
            ("Line-complete cards", None, "Finish a line or reach a station milestone and a celebration card appears — share it straight to social media."),
            ("22-county heatmap", "PRO", "See how much of each county and city you've covered, shaded on a map of Taiwan. Plus an A4 PDF stamp book."),
            ("29-train rolling stock book", None, "From the THSR 700T and the Puyuma and Taroko expresses to metro trains and Alishan's steam locomotives."),
            ("Your records stay yours", None, "iCloud sync carries your log to a new iPhone, free. Export a JSON backup or a spreadsheet-ready CSV any time."),
        ],
        "final_h2": "Start your map at <em>the next station</em>.",
        "final_live": "High Speed Rail between cities, the Pingxi Line on a day trip, the whole island by train — start with the first station.",
        "final_soon": "Coming soon to the App Store. High Speed Rail between cities, the Pingxi Line on a day trip, the whole island by train — start with the first station.",
        "f_contact": "Contact", "f_privacy": "Privacy", "f_terms": "Terms",
        "disclaimer": ("TRA station data comes from Taiwan's government open data (Taiwan Railway Corporation, Open "
                       "Government Data License, version 1.0). Track geometry and non-TRA stations come from "
                       "OpenStreetMap (© OpenStreetMap contributors). Taiwan Rail Log is an independent app and is not "
                       "affiliated with, endorsed by, or sponsored by Taiwan Railway Corporation, Taiwan High Speed "
                       "Rail Corporation, or any metro operator."),
    },
    "ja": {
        "dir": "ja/", "lang": "ja", "shots": "ja",
        "font": '"Hiragino Sans", "Hiragino Kaku Gothic ProN"',
        "serif": '"Hiragino Mincho ProN", "Songti TC", "Yu Mincho", serif',
        "title": "鐵道誌 — 台湾鉄道の記録｜台湾旅行の乗りつぶし・駅スタンプ帳",
        "desc": ("駅をタップして乗車を記録すると、乗った路線が台湾の地図に色づいていきます。台鉄・台湾高速鉄道・"
                 "MRT・ライトレール・阿里山森林鉄道まで、39路線・589駅を収録した乗りつぶしアプリ。"),
        "og_title": "鐵道誌 - 台湾鉄道の記録",
        "og_desc": "乗った路線が、地図の上で色づいていく。台湾の39路線・589駅。",
        "brand": "鐵道誌",
        "sign_prev": "39路線", "sign_next": "589駅",
        "h1": "乗った路線が、<br>地図の上で<br><em>色づいていく</em>。",
        "sub": ("駅をタップするだけで乗車を記録。台湾の路線図が、少しずつあなただけの乗りつぶしマップに育っていきます。"
                "台鉄の正式路線、台湾高速鉄道（台湾新幹線）、台北・新北・桃園・台中・高雄のMRTとライトレール、"
                "阿里山森林鉄道まで、39路線・589駅を一冊に。"),
        "cta_note": "iPhone・iPad ・ iOS 18+ ・ 基本無料",
        "badge_soon": "近日公開", "badge_live": "ダウンロード",
        "stamp": "完乗",
        "read_label": "記録した駅",
        "how_kicker": "使い方", "how_num": "01–03",
        "how_h2": "駅をタップしてから、<em>スタンプが押される</em>まで。",
        "steps": [
            ("記録", "駅をタップして記録", "地図の駅をタップするだけ。始点と終点を選べば区間をまとめて登録でき、昔の旅も日付を選んでさかのぼれます。"),
            ("着色", "路線が色づく", "乗った区間は路線カラーで塗られ、未乗区間はグレーのまま。未乗車の路線だけを表示して、次の旅の計画にも。"),
            ("収集", "スタンプが貯まる", "訪れた駅はスタンプになってスタンプ帳へ。路線を完乗すると、シェアできる記念カードが登場します。"),
        ],
        "value_kicker": "台湾全土", "value_num": "台鉄・高鉄・MRT・森林鉄道",
        "value_h2": "台湾の<em>39路線・589駅</em>を、これ一つで。",
        "value_lede": ("縦貫線・南廻線から平渓線・集集線・内湾線まで、台鉄の正式路線16本をすべて収録。"
                       "さらに台湾高速鉄道、5都市のMRTとライトレール、阿里山森林鉄道。"
                       "台鉄・高鉄・MRTが接続する乗換駅はひとつにまとめて表示します。"),
        "stats": [("39", "路線"), ("589", "駅"), ("22", "県市ヒートマップ"), ("29", "種の車両図鑑")],
        "ops": {"tra": "台鉄", "thsr": "台湾高速鉄道", "trtc": "台北MRT", "ntmc": "新北MRT",
                "tymc": "桃園MRT", "tmrt": "台中MRT", "krtc": "高雄MRT", "afr": "阿里山森林鉄道"},
        "shots_kicker": "画面", "shots_num": "iOS",
        "shots_h2": "旅先で書き足す<em>乗車記録。</em>",
        "shots_caps": ["乗った路線を、地図に塗る", "乗った区間を、3D衛星写真でもう一度", "訪れた駅が、スタンプになる"],
        "beta": "BETA",
        "feat_kicker": "こだわり", "feat_num": "06",
        "feat_h2": "記録する人のための、<em>心配り</em>。",
        "feats": [
            ("前面展望", "BETA", "衛星写真と3D建物の上を、乗った区間に沿って飛ぶように振り返れます。地下区間は地上の街並みの上を進みます。動画に書き出してシェアも。"),
            ("区間まとめて入力", None, "起点と終点を選ぶだけで区間内の駅をまとめて記録。乗車日は自由に選べ、GPSで近くの駅もすぐ見つかります。"),
            ("完乗記念カード", None, "路線の完乗や駅数の節目で記念カードが登場。そのままSNSでシェアできます。"),
            ("22県市ヒートマップ", "PRO", "県市ごとにどれだけ巡ったかを地図の濃淡で表示。A4で書き出せるPDFスタンプ帳も。"),
            ("車両図鑑 29種", None, "高鉄700T、プユマ号、タロコ号から各地のMRT、阿里山の蒸気機関車まで。"),
            ("記録はあなたのもの", None, "iCloud同期で機種変更後もそのまま（無料）。JSONバックアップとExcelで開けるCSVをいつでも書き出せます。"),
        ],
        "final_h2": "次の一駅から、<em>台湾の乗りつぶし</em>を。",
        "final_live": "台北のMRTから、平渓線の日帰り旅、阿里山まで。まずは最初の一駅から。",
        "final_soon": "App Storeで近日公開。台北のMRTから、平渓線の日帰り旅、阿里山まで。まずは最初の一駅から。",
        "f_contact": "お問い合わせ", "f_privacy": "プライバシーポリシー", "f_terms": "利用規約",
        "disclaimer": ("台鉄の駅データは台湾政府のオープンデータ（国営台湾鉄路股份有限公司、政府資料開放授權條款 第1版）を、"
                       "線路形状と台鉄以外の駅データはOpenStreetMap（© OpenStreetMap contributors）を元にしています。"
                       "鐵道誌は個人開発の独立したアプリであり、国営台湾鉄路股份有限公司、台湾高速鉄路股份有限公司、"
                       "各MRT運営事業者とは一切関係ありません。"),
    },
    "ko": {
        "dir": "ko/", "lang": "ko", "shots": "ko",
        "font": '"Apple SD Gothic Neo", "Pretendard"',
        "serif": '"AppleMyungjo", "Songti TC", "Noto Serif KR", serif',
        "title": "鐵道誌 — 대만 철도 승차 기록｜기차여행 완주 지도·역 스탬프북",
        "desc": ("역을 탭해 승차를 기록하면 탄 노선이 대만 지도 위에 색으로 채워집니다. 臺鐵·고속철도(高鐵)·MRT·"
                 "경전철·阿里山 삼림철도까지 39개 노선·589개 역을 담은 대만 철도 여행 기록 앱."),
        "og_title": "鐵道誌 - 대만 철도 승차 기록",
        "og_desc": "탄 노선이 지도 위에서 색으로 채워집니다. 대만 39개 노선·589개 역.",
        "brand": "鐵道誌",
        "sign_prev": "39개 노선", "sign_next": "589개 역",
        "h1": "탄 노선이,<br>지도 위에서 <em>색으로 채워집니다</em>.",
        "sub": ("역을 탭하기만 하면 기록되고, 대만 노선도가 나만의 완주 지도로 자라납니다. 臺鐵(대만철도) 정식 노선, "
                "대만 고속철도(高鐵), 타이베이·신베이·타오위안·타이중·가오슝의 MRT와 경전철, 阿里山 삼림철도까지 "
                "39개 노선·589개 역을 한 권에."),
        "cta_note": "iPhone·iPad · iOS 18+ · 기본 무료",
        "badge_soon": "곧 출시", "badge_live": "다운로드",
        "stamp": "完乘",
        "read_label": "기록한 역",
        "how_kicker": "사용 방법", "how_num": "01–03",
        "how_h2": "역을 탭한 순간부터, <em>도장이 찍히기</em>까지.",
        "steps": [
            ("기록", "역을 탭해서 기록", "지도 위 역을 탭하면 됩니다. 출발·도착역을 고르면 구간을 한 번에 넣을 수 있고, 지난 여행도 날짜를 골라 소급해서 기록해요."),
            ("채색", "노선이 색으로 채워짐", "탄 구간은 노선 고유색으로 칠해지고, 안 탄 구간은 회색 그대로. 안 탄 노선만 골라 보며 다음 여행을 계획하세요."),
            ("수집", "도장이 쌓임", "방문한 역은 도장이 되어 스탬프 수첩에 모입니다. 노선을 완주하면 공유할 수 있는 기념 카드가 나와요."),
        ],
        "value_kicker": "대만 전역", "value_num": "臺鐵·高鐵·MRT·삼림철도",
        "value_h2": "대만 <em>39개 노선·589개 역</em>을 이 앱 하나로.",
        "value_lede": ("종관선·남회선부터 핑시선·지지선·네이완선까지 臺鐵 정식 노선 16개를 모두 담았습니다. "
                       "여기에 대만 고속철도, 5개 도시의 MRT와 경전철, 阿里山 삼림철도까지. "
                       "臺鐵·高鐵·MRT가 만나는 환승역은 하나로 묶어서 표시합니다."),
        "stats": [("39", "개 노선"), ("589", "개 역"), ("22", "개 현·시 히트맵"), ("29", "종 차량 도감")],
        "ops": {"tra": "臺鐵(대만철도)", "thsr": "대만 고속철도", "trtc": "타이베이 MRT", "ntmc": "신베이 MRT",
                "tymc": "타오위안 MRT", "tmrt": "타이중 MRT", "krtc": "가오슝 MRT", "afr": "阿里山 삼림철도"},
        "shots_kicker": "화면", "shots_num": "iOS",
        "shots_h2": "여행하며 채워가는 <em>승차 기록장.</em>",
        "shots_caps": ["탄 노선을 지도에 칠하고", "탄 구간을 3D 위성으로 다시 날아보고", "방문한 역은 도장 하나로"],
        "beta": "BETA",
        "feat_kicker": "디테일", "feat_num": "06",
        "feat_h2": "기록할 때 유용한 <em>기능들.</em>",
        "feats": [
            ("전면 전망", "BETA", "위성 사진과 3D 건물 위로, 탄 구간을 따라 날아가듯 다시 돌아봅니다. 지하 구간은 지상 거리 위를 지나가요. 동영상으로 내보내 공유도."),
            ("구간 한 번에 입력", None, "출발역과 도착역만 고르면 구간 전체가 한 번에 기록됩니다. 날짜는 자유롭게, GPS로 가까운 역도 바로 찾아요."),
            ("완주 기념 카드", None, "노선을 완주하거나 역 수를 달성하면 기념 카드가 나오고, 바로 SNS에 공유할 수 있어요."),
            ("22개 현·시 히트맵", "PRO", "현·시별로 얼마나 다녔는지 지도 색의 농도로 확인. A4로 출력하는 PDF 스탬프 수첩도 있어요."),
            ("차량 도감 29종", None, "高鐵 700T, 푸유마호, 타이루거호부터 각지 MRT와 阿里山 증기기관차까지."),
            ("기록은 내 손에", None, "iCloud 동기화로 기기를 바꿔도 그대로(무료). JSON 백업과 엑셀에서 열리는 CSV를 언제든 내보내기."),
        ],
        "final_h2": "다음 한 역부터, <em>대만 완주 지도</em>를.",
        "final_live": "타이베이 MRT부터 핑시선 당일치기, 가오슝까지. 첫 역부터 기록해 보세요.",
        "final_soon": "App Store 곧 출시. 타이베이 MRT부터 핑시선 당일치기, 가오슝까지. 첫 역부터 기록해 보세요.",
        "f_contact": "문의", "f_privacy": "개인정보 처리방침", "f_terms": "이용약관",
        "disclaimer": ("臺鐵 역 데이터는 대만 정부 공개 데이터(國營臺灣鐵路股份有限公司, 政府資料開放授權條款 第1版)를, "
                       "선로 형상과 臺鐵 외 역 데이터는 OpenStreetMap(© OpenStreetMap contributors)을 바탕으로 합니다. "
                       "鐵道誌는 독립 개발 앱이며 國營臺灣鐵路股份有限公司, 台灣高速鐵路股份有限公司 및 각 MRT 운영사와 "
                       "제휴·후원 관계가 없습니다."),
    },
}


def hreflang_block():
    lines = [f'<link rel="alternate" hreflang="x-default" href="{BASE_URL}">']
    for loc in LOCALES.values():
        lines.append(f'<link rel="alternate" hreflang="{loc["lang"]}" href="{BASE_URL}{loc["dir"]}">')
    return "\n".join(lines)


def lang_nav(cur_dir, rel):
    out = []
    for d, label in LANG_LABELS:
        cls = ' class="cur"' if d == cur_dir else ""
        href = (rel + d) if d else (rel if rel else "./")
        out.append(f'<a href="{href}"{cls}>{label}</a>')
    return "".join(out)


def kicker(word, num):
    return (f'<div class="kicker"><span class="glyph">誌</span><span>· {word}</span>'
            f'<span class="rule"></span><span class="num">{num}</span></div>')


def badge(loc, el_id):
    if APP_STORE_URL:
        return (f'<a class="store-badge" id="{el_id}" href="{APP_STORE_URL}" aria-label="App Store">{APPLE_SVG}'
                f'<span class="txt"><small>{loc["badge_live"]}</small><strong>App Store</strong></span></a>')
    return (f'<span class="store-badge disabled" id="{el_id}" aria-disabled="true">'
            f'<span class="txt"><small>{loc["badge_soon"]}</small><strong>App Store</strong></span></span>')


def render(key):
    loc = LOCALES[key]
    rel = "../" if loc["dir"] else ""
    overrides = []
    if loc["font"]:
        overrides.append(f'--sans:-apple-system,BlinkMacSystemFont,{loc["font"]},"PingFang TC","Segoe UI",sans-serif')
    if loc.get("serif"):
        overrides.append(f'--serif:{loc["serif"]}')
    style_override = f'<style>:root{{{";".join(overrides)}}}</style>' if overrides else ""

    marquee = "".join(
        (f'<span><i style="--c:{c}"></i>{name}</span>' if c else f'<span class="hl">{name}</span>')
        for name, c in MARQUEE_ITEMS * 2)
    steps = "".join(
        f'<div class="step"><span class="tag">{tag}</span><span class="n">0{i+1}</span><h3>{h}</h3><p>{p}</p></div>'
        for i, (tag, h, p) in enumerate(loc["steps"]))
    stats = "".join(f'<div class="stat"><div class="n">{n}</div><div class="l">{l}</div></div>'
                    for n, l in loc["stats"])
    ops = "".join(f'<span class="op"><i style="--c:{c}"></i>{loc["ops"][k]}<b>{n}</b></span>'
                  for k, c, n in OPERATORS)
    shots = "".join(
        f'<figure><div class="phone"><img src="{rel}assets/shots/{loc["shots"]}/shot-{f}.jpg" alt="{cap}" '
        f'width="600" height="1304" loading="lazy"><div class="island"></div></div>'
        f'<figcaption>{cap}{"<span class=beta>" + loc["beta"] + "</span>" if f == "2-flyover" else ""}'
        f'</figcaption></figure>'
        for f, cap in zip(SHOTS, loc["shots_caps"]))
    feats = "".join(
        f'<div class="feat"><h3>{h}{f"<span class=tagpill>{tag}</span>" if tag else ""}</h3><p>{p}</p></div>'
        for h, tag, p in loc["feats"])
    final_lede = loc["final_live"] if APP_STORE_URL else loc["final_soon"]

    html = f"""<!doctype html>
<html lang="{loc['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{loc['title']}</title>
<meta name="description" content="{loc['desc']}">
<meta property="og:title" content="{loc['og_title']}">
<meta property="og:description" content="{loc['og_desc']}">
<meta property="og:image" content="{BASE_URL}assets/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:type" content="website">
<meta property="og:url" content="{BASE_URL}{loc['dir']}">
<meta property="og:site_name" content="kkiruk studio">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#1961B8">
<link rel="canonical" href="{BASE_URL}{loc['dir']}">
{hreflang_block()}
<link rel="icon" type="image/png" href="{rel}assets/icon-180.png">
<link rel="apple-touch-icon" href="{rel}assets/icon-180.png">
<link rel="stylesheet" href="{rel}assets/style.css">
{style_override}
</head>
<body>

<nav>
  <div class="wrap">
    <a class="wordmark" href="{rel if rel else './'}"><img src="{rel}assets/icon-180.png" alt=""><span>{loc['brand']}</span></a>
    <div class="lang">{lang_nav(loc['dir'], rel)}</div>
  </div>
</nav>

<header class="hero">
  <div class="wrap">
    <div>
      <div class="sign" role="img" aria-label="鐵道誌 · Taiwan Rail Log">
        <div class="panel">
          <div class="top"></div>
          <div class="name"><span class="zh">鐵道誌</span><span class="en">TAIWAN RAIL LOG</span></div>
          <div class="adj"><span class="l"><i></i>{loc['sign_prev']}</span><span class="r">{loc['sign_next']}<i></i></span></div>
        </div>
      </div>
      <h1>{loc['h1']}</h1>
      <p class="sub">{loc['sub']}</p>
      <div class="cta">
        {badge(loc, 'storeLink')}
        <span class="note">{loc['cta_note']}</span>
      </div>
    </div>
    <div>
      <div class="railmap">
        {RAILMAP_SVG}
        <div class="stamp"><span>{loc['stamp']}</span></div>
        <div class="read"><span>{loc['read_label']}</span><span><b id="readCount">0</b>/ 589</span></div>
      </div>
      <div class="railmap-credit">{OSM_CREDIT}</div>
    </div>
  </div>
</header>

<div class="marquee" aria-hidden="true"><div class="track">{marquee}</div></div>

<section>
  <div class="wrap">
    {kicker(loc['how_kicker'], loc['how_num'])}
    <h2>{loc['how_h2']}</h2>
    <div class="steps">{steps}</div>
  </div>
</section>

<section class="value">
  <div class="ghost" aria-hidden="true">589</div>
  <div class="wrap">
    {kicker(loc['value_kicker'], loc['value_num'])}
    <h2>{loc['value_h2']}</h2>
    <p class="lede">{loc['value_lede']}</p>
    <div class="stats">{stats}</div>
    <div class="ops">{ops}</div>
  </div>
</section>

<section class="shots">
  <div class="wrap">
    {kicker(loc['shots_kicker'], loc['shots_num'])}
    <h2>{loc['shots_h2']}</h2>
    <div class="row">{shots}</div>
  </div>
</section>

<section>
  <div class="wrap">
    {kicker(loc['feat_kicker'], loc['feat_num'])}
    <h2>{loc['feat_h2']}</h2>
    <div class="grid6">{feats}</div>
  </div>
</section>

<section class="final">
  <div class="wrap">
    <h2>{loc['final_h2']}</h2>
    <p class="lede">{final_lede}</p>
    <div class="cta">{badge(loc, 'storeLink2')}</div>
  </div>
</section>

<footer>
  <div class="wrap">
    <div class="row">
      <div class="brand"><img src="{rel}assets/icon-180.png" alt=""><strong>kkiruk studio</strong></div>
      <div class="links">
        <a href="mailto:kkirukstudio.help@gmail.com">{loc['f_contact']}</a>
        <a href="/legal/privacy/">{loc['f_privacy']}</a>
        <a href="/legal/terms/">{loc['f_terms']}</a>
      </div>
      <div>© 2026 kkiruk studio</div>
    </div>
    <p class="disclaimer">{loc['disclaimer']}</p>
  </div>
</footer>

<script>
  // Hero counter: follows the lines as they paint in (CSS draws them over
  // ~7s), then rests on the demo total. Reduced motion shows the total.
  (function () {{
    const el = document.getElementById("readCount");
    const svg = document.querySelector(".railmap svg");
    if (!el || !svg) return;
    const total = +svg.dataset.ridden || 0;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {{ el.textContent = total; return; }}
    const start = performance.now() + 400, dur = 6800;
    (function tick(now) {{
      const t = Math.min(1, Math.max(0, (now - start) / dur));
      el.textContent = Math.round(total * t);
      if (t < 1) requestAnimationFrame(tick);
    }})(performance.now());
  }})();
</script>
<script src="/ga.js"></script>
</body>
</html>
"""
    out = ROOT / loc["dir"] / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)} ({len(html) // 1024} KB)")


for key in LOCALES:
    render(key)

# Preserve discovery metadata and visible product facts after regeneration —
# only when running inside the site repo (the sibling-landing convention).
# Pre-launch the slug is not in gen_jsonld APPS, so this touches only the
# home pages' metadata and the sitemap.
if __name__ == "__main__":
    import runpy as _seo_runpy
    from pathlib import Path as _SeoPath
    _seo = _SeoPath(__file__).resolve().parent.parent / "gen" / "refresh_seo.py"
    if _seo.exists():
        _seo_runpy.run_path(str(_seo), run_name="__main__")
