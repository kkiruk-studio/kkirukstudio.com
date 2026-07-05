#!/usr/bin/env python3
"""Generate index.html for every locale from one template.

Usage: python3 build.py
Output: ./index.html (ja, root/default), ./ko/index.html, ./en/index.html
"""
import pathlib

ROOT = pathlib.Path(__file__).parent
BASE_URL = "https://www.kkirukstudio.com/tetsulog/"

# Filled in after App Store approval (e.g. https://apps.apple.com/app/id1234567890).
# While empty, the CTA renders as a disabled "coming soon" pill instead of a
# real store badge.
APP_STORE_URL = ""

LANG_LABELS = [("", "日本語"), ("ko/", "한국어"), ("en/", "EN")]

# Shared marquee content across all locales: real Japanese line names plus the
# three otaku-culture words that anchor the app's concept, regardless of UI
# language (the app's own screens stay Japanese in every locale — see spec).
MARQUEE_ITEMS = [
    ("山手線", False), ("大阪環状線", False), ("銀座線", False),
    ("ゆいレール", False), ("函館市電", False), ("東海道新幹線", False),
    ("完乗", True), ("駅スタンプ", True), ("乗りつぶし", True),
]

# 山手線30駅を実際の経緯度からWebメルカトル図法で投影（z=14, タイル原点 x0=14549 y0=6448）。
# 背景地図（assets/yamanote-map.png, 1280x2048px）と1px単位で一致するviewBox。
# 分岐路線（中央線・京浜東北線・総武線）は同じ座標系上に実在駅を起点として延伸。
# viewBox/座標はデザイン確定案（drafts/railmap.html）と完全に一致させ、変更しないこと。
OSM_CREDIT = "© OpenStreetMap contributors"
RAILMAP_SVG = """<svg viewBox="0 0 1280 2048" aria-hidden="true">
  <path class="rail-casing" d="M1012.7,937.2 966.1,1027.5 910.2,1146.6 898.6,1308.6 785.5,1446.3 702.8,1589.6 681.9,1692.8 561.9,1819.0 502.4,1725.8 412.7,1615.4 348.6,1431.9 249.6,1269.9 262.4,1095.0 255.4,908.5 235.6,816.7 231.0,653.2 275.2,486.7 303.2,361.9 358.0,244.2 563.0,212.6 686.5,191.1 777.4,143.7 940.5,120.8 1009.2,205.4 1057.0,268.6 1147.9,364.7 1130.4,465.2 1099.0,559.9 1090.8,690.5 1055.8,786.6 Z"/>
  <path class="rail-base" d="M1012.7,937.2 966.1,1027.5 910.2,1146.6 898.6,1308.6 785.5,1446.3 702.8,1589.6 681.9,1692.8 561.9,1819.0 502.4,1725.8 412.7,1615.4 348.6,1431.9 249.6,1269.9 262.4,1095.0 255.4,908.5 235.6,816.7 231.0,653.2 275.2,486.7 303.2,361.9 358.0,244.2 563.0,212.6 686.5,191.1 777.4,143.7 940.5,120.8 1009.2,205.4 1057.0,268.6 1147.9,364.7 1130.4,465.2 1099.0,559.9 1090.8,690.5 1055.8,786.6 Z"/>
  <path class="rail-color c-loop" pathLength="100" d="M1012.7,937.2 966.1,1027.5 910.2,1146.6 898.6,1308.6 785.5,1446.3 702.8,1589.6 681.9,1692.8 561.9,1819.0 502.4,1725.8 412.7,1615.4 348.6,1431.9 249.6,1269.9 262.4,1095.0 255.4,908.5 235.6,816.7 231.0,653.2 275.2,486.7 303.2,361.9 358.0,244.2 563.0,212.6 686.5,191.1 777.4,143.7 940.5,120.8 1009.2,205.4 1057.0,268.6 1147.9,364.7 1130.4,465.2 1099.0,559.9 1090.8,690.5 1055.8,786.6 Z"/>

  <path class="rail-branch-casing" d="M235.6,816.7 150,798 70,782 0,768"/>
  <path class="rail-branch-base" d="M235.6,816.7 150,798 70,782 0,768"/>
  <path class="rail-color c-chuo" pathLength="100" d="M235.6,816.7 150,798 70,782 0,768"/>

  <path class="rail-branch-casing" d="M1130.4,465.2 1155,320 1185,160 1210,20"/>
  <path class="rail-branch-base" d="M1130.4,465.2 1155,320 1185,160 1210,20"/>
  <path class="rail-color c-keihin" pathLength="100" d="M1130.4,465.2 1155,320 1185,160 1210,20"/>
  <path class="rail-branch-casing" d="M681.9,1692.8 600,1830 520,1950 430,2048"/>
  <path class="rail-branch-base" d="M681.9,1692.8 600,1830 520,1950 430,2048"/>
  <path class="rail-color c-keihin" pathLength="100" d="M681.9,1692.8 600,1830 520,1950 430,2048"/>

  <path class="rail-branch-casing" d="M1090.8,690.5 1180,705 1250,725 1280,735"/>
  <path class="rail-branch-base" d="M1090.8,690.5 1180,705 1250,725 1280,735"/>
  <path class="rail-color c-sobu" pathLength="100" d="M1090.8,690.5 1180,705 1250,725 1280,735"/>

  <circle class="dot major loop" cx="1012.7" cy="937.2" r="16"/>
  <circle class="dot loop" cx="966.1" cy="1027.5" r="11"/>
  <circle class="dot loop" cx="910.2" cy="1146.6" r="11"/>
  <circle class="dot loop" cx="898.6" cy="1308.6" r="11"/>
  <circle class="dot loop" cx="785.5" cy="1446.3" r="11"/>
  <circle class="dot loop" cx="702.8" cy="1589.6" r="11"/>
  <circle class="dot major loop" cx="681.9" cy="1692.8" r="16"/>
  <circle class="dot loop" cx="561.9" cy="1819.0" r="11"/>
  <circle class="dot loop" cx="502.4" cy="1725.8" r="11"/>
  <circle class="dot loop" cx="412.7" cy="1615.4" r="11"/>
  <circle class="dot loop" cx="348.6" cy="1431.9" r="11"/>
  <circle class="dot major loop" cx="249.6" cy="1269.9" r="16"/>
  <circle class="dot loop" cx="262.4" cy="1095.0" r="11"/>
  <circle class="dot loop" cx="255.4" cy="908.5" r="11"/>
  <circle class="dot major loop" cx="235.6" cy="816.7" r="16"/>
  <circle class="dot loop" cx="231.0" cy="653.2" r="11"/>
  <circle class="dot loop" cx="275.2" cy="486.7" r="11"/>
  <circle class="dot loop" cx="303.2" cy="361.9" r="11"/>
  <circle class="dot major loop" cx="358.0" cy="244.2" r="16"/>
  <circle class="dot loop" cx="563.0" cy="212.6" r="11"/>
  <circle class="dot loop" cx="686.5" cy="191.1" r="11"/>
  <circle class="dot loop" cx="777.4" cy="143.7" r="11"/>
  <circle class="dot loop" cx="940.5" cy="120.8" r="11"/>
  <circle class="dot loop" cx="1009.2" cy="205.4" r="11"/>
  <circle class="dot loop" cx="1057.0" cy="268.6" r="11"/>
  <circle class="dot loop" cx="1147.9" cy="364.7" r="11"/>
  <circle class="dot major loop" cx="1130.4" cy="465.2" r="16"/>
  <circle class="dot loop" cx="1099.0" cy="559.9" r="11"/>
  <circle class="dot loop" cx="1090.8" cy="690.5" r="11"/>
  <circle class="dot loop" cx="1055.8" cy="786.6" r="11"/>

  <text class="eki-label" x="1032" y="930" text-anchor="start" font-size="46">東京</text>
  <text class="eki-label" x="212" y="810" text-anchor="end" font-size="46">新宿</text>
  <text class="eki-label" x="228" y="1290" text-anchor="end" font-size="46">渋谷</text>
  <text class="eki-label" x="338" y="230" text-anchor="end" font-size="46">池袋</text>
  <text class="eki-label" x="1150" y="450" text-anchor="start" font-size="46">上野</text>
  <text class="eki-label" x="681.9" y="1740" text-anchor="middle" font-size="46">品川</text>
</svg>"""

LOCALES = {
    "ja": {
        "dir": "", "lang": "ja", "font": None,
        "title": "鉄ログ — 乗った駅が、そのまま地図になる",
        "desc": "駅をタップするだけで乗車を記録。乗った路線の色が地図に広がり、完乗すると朱色のスタンプが押されます。全国163社・571路線・10,096駅対応の乗りつぶしアプリ。",
        "og_title": "鉄ログ — 乗りつぶし記録アプリ",
        "og_desc": "乗った駅が、そのまま地図になる。全国163社・571路線・10,096駅。",
        "brand": "鉄ログ",
        "kicker_word": "STAMP BOOK",
        "kicker_num": "全国 10,096 駅",
        "h1": "乗った駅が、<br>そのまま<em>地図になる</em>。",
        "sub": "地図の駅をタップするだけで乗車を記録。乗った路線の色がそのまま地図に広がります。全国163社・571路線・10,096駅の乗りつぶしを、鉄ログでスタンプ帳のように記録しましょう。",
        "cta_note": "iPhone・iPad・一部無料",
        "badge_small": "近日公開",
        "railmap_caption": "路線をタップで記録、色が広がり、スタンプが押される。",
        "how_kicker": "使い方", "how_num": "01–03",
        "how_h2": "駅をタップしてから、<em>スタンプが押される</em>まで。",
        "steps": [
            ["記録", "駅をタップして記録", "地図の駅をタップするだけ。乗った日付と区間を鉄ログが記録します。"],
            ["着色", "地図が色づく", "乗った路線の色が地図に広がります。未乗の区間はグレーのまま、乗った実感が一目でわかります。"],
            ["収集", "スタンプが貯まる", "路線を完乗すると、朱色の「完乗」スタンプが押されます。帳面のページが少しずつ埋まっていきます。"],
        ],
        "value_kicker": "全国データ", "value_num": "JR・私鉄・第三セクター",
        "value_h2": "全国<em>163社・571路線・10,096駅</em>を、これ一つで。",
        "value_lede": "JRグループ・大手私鉄・地方私鉄・第三セクターの路線データをあらかじめ収録。山手線一周でも、全国完乗でも、鉄ログが記録を引き継ぎます。",
        "stats": [["163", "鉄道会社"], ["571", "路線"], ["10,096", "駅"]],
        "shots_kicker": "画面", "shots_num": "IOS",
        "shots_h2": "飾りより、<em>手元で使う帳面</em>として。",
        "shots_caps": ["地図がそのまま乗車記録に", "駅スタンプ帳で会社別に管理", "完乗の瞬間に届く記念カード"],
        "feat_kicker": "こだわり", "feat_num": "06",
        "feat_h2": "記録する人のための、<em>心配り</em>。",
        "feats": [
            ["過去の乗車もOK", "昔の乗車履歴もあとから登録できます。今日から始めても、過去の完乗記録はそのまま有効です。", False],
            ["区間まとめて入力", "起点と終点を選ぶだけで、区間内の駅をまとめて乗車済みにできます。", False],
            ["完乗祝いカード", "路線を完乗すると、朱印風の記念カードが自動で作られます。SNSでのシェアにも使えます。", False],
            ["47都道府県ヒートマップ", "都道府県ごとの乗車率を地図の濃淡で可視化。旅の足跡が色でわかります。", True],
            ["PDF御朱印帳", "スタンプ帳をPDFで書き出して、印刷したり手元に保存したりできます。", True],
            ["iCloud同期", "記録はiCloudで同期。iPhoneでもiPadでも同じ帳面が開けます。無料でご利用いただけます。", False],
        ],
        "final_h2": "次の一駅から、<em>乗りつぶし</em>を記録しよう。",
        "final_lede": "近日 App Store 公開予定。",
        "f_contact": "お問い合わせ", "f_privacy": "プライバシーポリシー", "f_terms": "利用規約",
    },
    "ko": {
        "dir": "ko/", "lang": "ko", "font": '"Apple SD Gothic Neo", "Pretendard"',
        "title": "테츠로그 — 탄 역이, 그대로 지도가 됩니다",
        "desc": "역을 탭하면 탑승이 기록됩니다. 탄 노선의 색이 지도 위에 퍼지고, 완주하면 붉은 인장 스탬프가 찍힙니다. 일본 전국 163개사·571개 노선·10,096개 역을 담은 철도 여행 기록 앱.",
        "og_title": "테츠로그 — 일본 철도 여행 기록",
        "og_desc": "탄 역이, 그대로 지도가 됩니다. 전국 163개사·571개 노선·10,096개 역.",
        "brand": "테츠로그",
        "kicker_word": "스탬프북",
        "kicker_num": "전국 10,096개 역",
        "h1": "탄 역이,<br>그대로 <em>지도가 됩니다</em>.",
        "sub": "지도 위 역을 탭하기만 하면 탑승이 기록됩니다. 탄 노선의 색이 그대로 지도에 퍼져요. 일본 여행에서 탄 노선을, 전국 163개사·571개 노선·10,096개 역 규모로 테츠로그의 스탬프북에 기록하세요.",
        "cta_note": "iPhone·iPad · 일부 무료",
        "badge_small": "곧 출시",
        "railmap_caption": "노선을 탭해 기록하면 색이 채워지고, 스탬프가 찍힙니다.",
        "how_kicker": "사용 방법", "how_num": "01–03",
        "how_h2": "역을 탭한 순간부터, <em>스탬프가 찍히기</em>까지.",
        "steps": [
            ["기록", "지나온 역을 탭해서 기록", "지도 위 역을 탭하기만 하면 됩니다. 탄 날짜와 구간을 테츠로그가 기록해요."],
            ["채색", "지도가 색으로 채워짐", "탄 노선의 색이 지도 위에 퍼집니다. 안 탄 구간은 회색 그대로라 탄 흔적이 한눈에 보여요."],
            ["수집", "스탬프가 쌓임", "노선을 완주하면 붉은 인장 느낌의 '완승' 스탬프가 찍힙니다. 페이지가 한 장씩 채워지는 재미가 있어요."],
        ],
        "value_kicker": "전국 데이터", "value_num": "JR·사철·제3섹터",
        "value_h2": "전국 <em>163개사·571개 노선·10,096개 역</em>을 이 앱 하나로.",
        "value_lede": "JR그룹·대형 사철·지방 사철·제3섹터 노선 데이터를 미리 담아뒀어요. 야마노테선 한 바퀴든, 전국 완주든 테츠로그가 기록을 이어줍니다.",
        "stats": [["163", "철도회사"], ["571", "노선"], ["10,096", "역"]],
        "shots_kicker": "화면", "shots_num": "IOS",
        "shots_h2": "꾸미기보다 <em>손에 쥐는 기록장</em>으로.",
        "shots_caps": ["지도가 곧 탑승 기록이 됩니다", "회사별 역 스탬프북으로 정리", "완주 순간, 기념 카드가 도착"],
        "feat_kicker": "디테일", "feat_num": "06",
        "feat_h2": "기록하는 사람을 위한, <em>배려</em>.",
        "feats": [
            ["과거 탑승도 OK", "예전에 탄 기록도 나중에 등록할 수 있어요. 오늘 시작해도 과거 완주 기록은 그대로 인정됩니다.", False],
            ["구간 한 번에 입력", "출발역과 도착역만 고르면 구간 전체가 한 번에 탑승 처리됩니다.", False],
            ["완승 기념 카드", "노선을 완주하면 인장 느낌의 기념 카드가 자동으로 만들어져요. SNS 공유도 가능합니다.", False],
            ["47개 도도부현 히트맵", "도도부현별 탑승률을 지도 색의 농도로 확인. 여행한 흔적이 그대로 드러나요.", True],
            ["PDF 고슈인초", "스탬프북을 PDF로 내보내 인쇄하거나 보관할 수 있어요.", True],
            ["iCloud 동기화", "기록은 iCloud로 동기화됩니다. 아이폰에서도 아이패드에서도 같은 기록을 볼 수 있어요. 무료로 제공됩니다.", False],
        ],
        "final_h2": "다음 한 정거장부터, <em>완주 기록</em>을 시작하세요.",
        "final_lede": "App Store 출시 예정.",
        "f_contact": "문의", "f_privacy": "개인정보 처리방침", "f_terms": "이용약관",
    },
    "en": {
        "dir": "en/", "lang": "en", "font": None,
        "title": "Tetsulog — Every station you ride becomes a map",
        "desc": "Tap a station to log the ride. The line's color spreads across the map, and completing a line presses a vermilion stamp. A Japan rail trip log covering 163 operators, 571 lines, 10,096 stations.",
        "og_title": "Tetsulog — Japan Rail Trip Log",
        "og_desc": "Every station you ride becomes a map. 163 operators · 571 lines · 10,096 stations.",
        "brand": "Tetsulog",
        "kicker_word": "STAMP BOOK",
        "kicker_num": "10,096 STATIONS",
        "h1": "Every station you ride<br>becomes <em>a map</em>.",
        "sub": "Tap a station on the map and the ride is logged. The line's color spreads right across the map. Log your Japan rail trips — 163 operators, 571 lines, 10,096 stations — the way a stamp book fills, one page at a time.",
        "cta_note": "iPhone & iPad · Free, Pro available",
        "badge_small": "Coming soon",
        "railmap_caption": "Tap a line to log it — color spreads, a stamp is pressed.",
        "how_kicker": "HOW IT WORKS", "how_num": "01–03",
        "how_h2": "From a tap on the map to <em>a stamp in the book</em>.",
        "steps": [
            ["LOG", "Tap a station to log it", "Tap any station on the map. Tetsulog records the date and the segment you rode."],
            ["COLOR", "The map fills in color", "Ridden lines spread across the map in color. Unridden stretches stay gray, so your progress is obvious at a glance."],
            ["STAMP", "Stamps fill the book", "Complete a line and a vermilion “line complete” stamp is pressed. Page by page, the book fills up."],
        ],
        "value_kicker": "NATIONWIDE DATA", "value_num": "JR · PRIVATE · THIRD-SECTOR",
        "value_h2": "163 operators · 571 lines · <em>10,096 stations</em> — one app for all of Japan.",
        "value_lede": "Every JR group, major private railway, regional line and third-sector railway is preloaded. Whether it's one loop around the Yamanote Line or a lifelong completion run, Tetsulog keeps the log.",
        "stats": [["163", "operators"], ["571", "lines"], ["10,096", "stations"]],
        "shots_kicker": "SCREENS", "shots_num": "IOS",
        "shots_h2": "Built like a field notebook, <em>not a brochure</em>.",
        "shots_caps": ["The map is the ride log", "A stamp book organized by operator", "A keepsake card the moment you finish a line"],
        "feat_kicker": "DETAILS", "feat_num": "06",
        "feat_h2": "Built for <em>the record-keeper</em>.",
        "feats": [
            ["Backfill past rides", "Log rides you took years ago. Starting today doesn't erase the lines you'd already completed.", False],
            ["Log a whole segment at once", "Pick a start and end station — every stop between gets marked ridden in one step.", False],
            ["Line-complete keepsake card", "Finish a line and a stamp-style keepsake card is generated automatically. Shareable, too.", False],
            ["47-prefecture heatmap", "See your ridden ratio by prefecture on a shaded map of Japan.", True],
            ["PDF stamp book", "Export your stamp book as a PDF to print or archive.", True],
            ["iCloud sync, free", "Your log syncs via iCloud across iPhone and iPad — free, no subscription required.", False],
        ],
        "final_h2": "Start logging your <em>next line</em> today.",
        "final_lede": "Coming soon to the App Store.",
        "f_contact": "Contact", "f_privacy": "Privacy", "f_terms": "Terms",
    },
}


def hreflang_block():
    lines = [f'<link rel="alternate" hreflang="x-default" href="{BASE_URL}">']
    for key, loc in LOCALES.items():
        lines.append(f'<link rel="alternate" hreflang="{loc["lang"]}" href="{BASE_URL}{loc["dir"]}">')
    return "\n".join(lines)


def lang_nav(cur_dir, rel):
    out = []
    for d, label in LANG_LABELS:
        cls = ' class="cur"' if d == cur_dir else ""
        href = (rel + d) if d else (rel if rel else "./")
        out.append(f'<a href="{href}"{cls}>{label}</a>')
    return "".join(out)


def kicker(word_glyph_text, num_text, extra_class=""):
    return (f'<div class="kicker {extra_class}"><span class="glyph">帳</span>'
            f'<span>· {word_glyph_text}</span><span class="rule"></span><span class="num">{num_text}</span></div>')


def badge(loc, el_id):
    if APP_STORE_URL:
        apple_svg = '<svg viewBox="0 0 384 512" aria-hidden="true"><path d="M318.7 268.7c-.2-36.7 16.4-64.4 50-84.8-18.8-26.9-47.2-41.7-84.7-44.6-35.5-2.8-74.3 20.7-88.5 20.7-15 0-49.4-19.7-76.4-19.7C63.3 141.2 4 184.8 4 273.5q0 39.3 14.4 81.2c12.8 36.7 59 126.7 107.2 125.2 25.2-.6 43-17.9 75.8-17.9 31.8 0 48.3 17.9 76.4 17.9 48.6-.7 90.4-82.5 102.6-119.3-65.2-30.7-61.7-90-61.7-91.9zm-56.6-164.2c27.3-32.4 24.8-61.9 24-72.5-24.1 1.4-52 16.4-67.9 34.9-17.5 19.8-27.8 44.3-25.6 71.9 26.1 2 49.9-11.4 69.5-34.3z"/></svg>'
        return (f'<a class="store-badge" id="{el_id}" href="{APP_STORE_URL}" aria-label="App Store">{apple_svg}'
                f'<span class="txt"><small>Download on the</small><strong>App Store</strong></span></a>')
    return (f'<span class="store-badge disabled" id="{el_id}" aria-disabled="true">'
            f'<span class="txt"><small>{loc["badge_small"]}</small><strong>App Store</strong></span></span>')


def render(key):
    loc = LOCALES[key]
    rel = "../" if loc["dir"] else ""
    font_override = (f'<style>body{{font-family:-apple-system,BlinkMacSystemFont,{loc["font"]},'
                      f'"Segoe UI",sans-serif}}</style>') if loc["font"] else ""

    marquee = "".join(
        f'<span class="{"hl" if hl else ""}">{m}</span>'
        for m, hl in MARQUEE_ITEMS * 2
    )
    steps = "".join(
        f'<div class="step"><span class="tag">{tag}</span><span class="n">0{i+1}</span><h3>{h}</h3><p>{p}</p></div>'
        for i, (tag, h, p) in enumerate(loc["steps"])
    )
    stats = "".join(
        f'<div class="stat"><div class="n">{n}</div><div class="l">{l}</div></div>'
        for n, l in loc["stats"]
    )
    shot_files = ["1-map", "2-stamps", "3-completion"]
    shots = "".join(
        f'<figure><div class="phone"><img src="{rel}assets/shot-{f}.png" alt="{cap}" loading="lazy"><div class="island"></div></div><figcaption>{cap}</figcaption></figure>'
        for f, cap in zip(shot_files, loc["shots_caps"])
    )
    feats = "".join(
        f'<div class="feat"><h3>{h}{"<span class=\'pro\'>PRO</span>" if pro else ""}</h3><p>{p}</p></div>'
        for h, p, pro in loc["feats"]
    )

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
<meta property="og:type" content="website">
<meta property="og:url" content="{BASE_URL}{loc['dir']}">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="{BASE_URL}{loc['dir']}">
{hreflang_block()}
<link rel="icon" type="image/png" href="{rel}assets/icon-180.png">
<link rel="apple-touch-icon" href="{rel}assets/icon-180.png">
<link rel="stylesheet" href="{rel}assets/style.css">
{font_override}
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
      <div class="ekimeihyo">
        <div class="bar"></div>
        <div class="body">
          <div class="adj adj-prev"><span class="roundel">鉄</span><span class="arrow">← {loc['kicker_word']}</span></div>
          <div class="name"><span class="jp">{loc['brand']}</span><span class="en">TETSULOG</span></div>
          <div class="adj adj-next"><span class="arrow">{loc['kicker_num']} →</span></div>
        </div>
      </div>
      <h1>{loc['h1']}</h1>
      <p class="sub">{loc['sub']}</p>
      <div class="cta">
        {badge(loc, 'storeLink')}
        <span class="note">{loc['cta_note']}</span>
      </div>
    </div>
    <div class="railmap-col">
      <div class="railmap">
        <div class="railmap-underlay" aria-hidden="true" style="background-image:url('{rel}assets/yamanote-map.png')"></div>
        {RAILMAP_SVG}
        <div class="stamp"><span>完乗</span></div>
      </div>
      <div class="railmap-caption">
        <span>{loc['railmap_caption']}</span>
        <span class="railmap-legend"><span><i class="g"></i></span></span>
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
  <div class="ghost">10,096</div>
  <div class="wrap">
    {kicker(loc['value_kicker'], loc['value_num'])}
    <h2>{loc['value_h2']}</h2>
    <p class="lede">{loc['value_lede']}</p>
    <div class="stats">{stats}</div>
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
    <p class="lede">{loc['final_lede']}</p>
    <div class="cta">{badge(loc, 'storeLink2')}</div>
  </div>
</section>

<footer>
  <div class="wrap">
    <div class="brand"><img src="{rel}assets/icon-180.png" alt=""><strong>kkiruk studio</strong></div>
    <div class="links">
      <a href="mailto:kkirukstudio.help@gmail.com">{loc['f_contact']}</a>
      <a href="https://kkiruk-studio.github.io/privacy-policy-app/">{loc['f_privacy']}</a>
      <a href="https://kkiruk-studio.github.io/terms-of-service-app/">{loc['f_terms']}</a>
    </div>
    <div>© 2026 kkiruk studio</div>
  </div>
</footer>

<script src="/ga.js"></script>
</body>
</html>
"""
    out = ROOT / loc["dir"] / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)} ({len(html)} bytes)")


for key in LOCALES:
    render(key)
