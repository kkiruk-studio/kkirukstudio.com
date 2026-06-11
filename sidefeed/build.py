#!/usr/bin/env python3
"""Generate index.html for every locale from one template.

Usage: python3 build.py
Output: ./index.html (en), ./ko/index.html, ./ja/index.html
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).parent
BASE_URL = "https://www.kkirukstudio.com/sidefeed/"
APP_STORE_URL = "https://apps.apple.com/app/id6762836653"

APPLE_SVG = '<svg viewBox="0 0 384 512" aria-hidden="true"><path d="M318.7 268.7c-.2-36.7 16.4-64.4 50-84.8-18.8-26.9-47.2-41.7-84.7-44.6-35.5-2.8-74.3 20.7-88.5 20.7-15 0-49.4-19.7-76.4-19.7C63.3 141.2 4 184.8 4 273.5q0 39.3 14.4 81.2c12.8 36.7 59 126.7 107.2 125.2 25.2-.6 43-17.9 75.8-17.9 31.8 0 48.3 17.9 76.4 17.9 48.6-.7 90.4-82.5 102.6-119.3-65.2-30.7-61.7-90-61.7-91.9zm-56.6-164.2c27.3-32.4 24.8-61.9 24-72.5-24.1 1.4-52 16.4-67.9 34.9-17.5 19.8-27.8 44.3-25.6 71.9 26.1 2 49.9-11.4 69.5-34.3z"/></svg>'

LANG_LABELS = [("", "EN"), ("ko/", "한국어"), ("ja/", "日本語")]

LOCALES = {
    "en": {
        "dir": "", "lang": "en", "font": None, "shots": "en",
        "title": "Sidefeed — Trend research for YouTube creators",
        "desc": "Official YouTube trending from 12 countries, 14 categories, and 6-hour rank movement. See what's rising while it's rising — no Google login, no personalization.",
        "og_title": "Sidefeed — Trend Research for Creators",
        "og_desc": "12 countries, 14 categories, 6-hour rank movement. Find the next video before the algorithm does.",
        "kicker_num": "TREND RESEARCH",
        "h1": "Find the next video<br>before the <em>algorithm</em> does.",
        "demo_items": [
            ["🇺🇸", "GAMING", "#18", "#3", "▲15 · 6H", "up"],
            ["🇰🇷", "MUSIC", "#9", "#2", "▲7 · 6H", "up"],
            ["🇯🇵", "ENTERTAINMENT", "—", "#5", "NEW", "new"],
            ["🇬🇧", "SPORTS", "#21", "#6", "▲15 · 6H", "up"],
        ],
        "sub": "Sidefeed is trend research for YouTube creators and content planners. Official trending charts from 12 countries, 14 categories, and 6-hour rank movement show you what's rising while it's still rising — on a feed that never personalizes.",
        "badge_small": "Download on the", "note": "FREE DOWNLOAD · IPHONE &amp; IPAD · NO GOOGLE LOGIN",
        "badge_aria": "Download on the App Store",
        "chips": [["up", "▲9", "Top mover"], ["new", "N", "New entry"], ["", "🌍", "12 countries"], ["", "🎵", "14 categories"]],
        "hero_alt": "Sidefeed trending screen showing the US YouTube chart with rank-change badges and a category breakdown bar",
        "marquee": ["UNITED STATES", "JAPAN", "UNITED KINGDOM", "GERMANY", "AUSTRALIA", "CANADA", "FRANCE", "KOREA", "SWITZERLAND", "NETHERLANDS", "SWEDEN", "SINGAPORE"],
        "how_kicker": "HOW IT WORKS",
        "how_h2": "From <em>“what should I make next?”</em> to a data-backed idea.",
        "steps": [
            ["COUNTRY", "Pick a market", "Tap the flag to switch between 12 countries. Korea at breakfast, the US at lunch — each chart is the official YouTube trending for that market."],
            ["SIGNALS", "Read the movement", "Every video carries its 6-hour rank change — ▲ rising, ▼ falling, NEW just entered. Top Movers surfaces the fastest climbers, and Radar catches breakouts beyond the chart."],
            ["RESEARCH", "Keep the clues", "Open the insight sheet for rank history, category and view pace. Save promising videos to Watch Later — synced through your own iCloud."],
        ],
        "rank_kicker": "RANK MOVEMENT", "rank_num": "EVERY 6 HOURS",
        "rank_h2": "Trends are <em>movement</em>, not lists.",
        "rank_lede": "A chart tells you what's big right now. Movement tells you what's about to be. Sidefeed snapshots every chart through the day and pins the 6-hour delta on every video.",
        "rank_rows": [
            ["6h ago #18", "now #3", '🇺🇸 GAMING · <span class="d-up">▲15</span>'],
            ["6h ago #9", "now #2", '🇰🇷 MUSIC · <span class="d-up">▲7</span>'],
            ["6h ago —", "now #5", '🇯🇵 ENTERTAINMENT · <span class="d-new">NEW</span>'],
            ["6h ago #4", "now #11", '🇬🇧 SPORTS · <span class="d-down">▼7</span>'],
        ],
        "views_kicker": "THE TOOLKIT", "views_num": "4 VIEWS",
        "views_h2": "Four views, <em>one research flow</em>.",
        "views_lede": "Official charts, Sidefeed's own ranking, category discovery and market switching — all built on public data, so everyone sees the same screen.",
        "views": [
            ["🔥", "Trending", "The official YouTube chart with 6-hour rank badges, Top Movers and a live category breakdown bar."],
            ["📡", "Radar", "Sidefeed's own ranking — catches breakouts climbing from outside the trending chart."],
            ["✨", "Discover", "Fresh popular videos across 14 categories. Public popularity, zero personalization."],
            ["🌍", "12 Countries", "One tap on the flag to compare markets. What's #1 in Tokyo right now?"],
        ],
        "shots_kicker": "SCREENS", "shots_num": "IOS 17+",
        "shots_h2": "A research desk, <em>not another feed</em>.",
        "shots_caps": ["RADAR · BREAKOUT RANKING", "12-COUNTRY SWITCHER", "DISCOVER · 14 CATEGORIES"],
        "feat_kicker": "DETAILS", "feat_num": "06",
        "feat_h2": "Built for research. <em>Deliberate</em> choices.",
        "feats": [
            ["No login, no personalization", "No Google account, no watch history. Everyone sees the same public data — what's actually trending, not what an algorithm thinks you want."],
            ["6-hour snapshots", "Rank history is computed from chart snapshots taken through the day — movement you can't see on YouTube itself."],
            ["Insight sheet", "Tap any video to see its rank, 6-hour delta, category and view pace before you decide to watch it on YouTube."],
            ["Shorts filter", "Researching long-form? Hide Shorts from every feed with one toggle."],
            ["Watch Later + iCloud", "Save reference videos and they follow you across devices through your own iCloud."],
            ["Feed control", "Block channels and dismiss videos to keep your research signal clean."],
        ],
        "final_h2": "Plan the next video with data, not guesswork.", "final_lede": "Free download on iPhone &amp; iPad.",
        "f_contact": "Contact", "f_privacy": "Privacy", "f_terms": "Terms",
    },
    "ko": {
        "dir": "ko/", "lang": "ko", "font": '"Apple SD Gothic Neo", "Pretendard"', "shots": "ko",
        "title": "Sidefeed — 크리에이터를 위한 12개국 트렌드 리서치",
        "desc": "12개국 YouTube 공식 트렌딩, 14개 카테고리, 6시간 순위 변동. 구글 로그인 없이, 개인화 없는 피드에서 지금 뜨는 흐름을 읽으세요.",
        "og_title": "Sidefeed — 크리에이터 트렌드 리서치",
        "og_desc": "12개국 · 14카테고리 · 6시간 순위 변동. 알고리즘보다 먼저 다음 영상의 단서를.",
        "kicker_num": "트렌드 리서치",
        "h1": "다음 영상의 단서,<br>알고리즘보다 <em>먼저</em>.",
        "demo_items": [
            ["🇰🇷", "음악", "#9", "#2", "▲7 · 6시간", "up"],
            ["🇺🇸", "게임", "#18", "#3", "▲15 · 6시간", "up"],
            ["🇯🇵", "엔터", "—", "#5", "NEW", "new"],
            ["🇬🇧", "스포츠", "#21", "#6", "▲15 · 6시간", "up"],
        ],
        "sub": "Sidefeed는 YouTube 크리에이터·콘텐츠 기획자를 위한 트렌드 리서치 도구입니다. 12개국 공식 트렌딩, 14개 카테고리, 6시간 순위 변동 — 개인화 없는 피드에서 지금 올라오는 흐름을 그대로 읽으세요.",
        "badge_small": "다운로드는", "note": "무료 다운로드 · iPhone &amp; iPad · 구글 로그인 없음",
        "badge_aria": "App Store에서 다운로드",
        "chips": [["up", "▲9", "급상승"], ["new", "N", "NEW 진입"], ["", "🌍", "12개국"], ["", "🎵", "14 카테고리"]],
        "hero_alt": "Sidefeed 트렌딩 화면 — 순위 변화 뱃지와 카테고리 분포 바가 있는 한국 YouTube 차트",
        "marquee": ["미국", "일본", "영국", "독일", "호주", "캐나다", "프랑스", "한국", "스위스", "네덜란드", "스웨덴", "싱가포르"],
        "how_kicker": "사용 방법",
        "how_h2": "\"다음에 뭐 만들지?\"에서 <em>데이터가 받쳐주는 기획까지</em>.",
        "steps": [
            ["국가", "시장을 고른다", "국기 버튼 한 번으로 12개국 전환. 아침엔 한국, 점심엔 미국 — 각 시장의 YouTube 공식 트렌딩 차트를 그대로 봅니다."],
            ["시그널", "움직임을 읽는다", "모든 영상에 6시간 순위 변화가 붙습니다. ▲ 상승, ▼ 하락, NEW 진입. Top Movers가 가장 빠른 상승작을, 레이더가 트렌딩 밖 급상승을 잡아냅니다."],
            ["리서치", "단서를 남긴다", "인사이트 시트로 순위 이력·카테고리·조회 속도를 확인하고, 참고할 영상은 나중에 보기로 저장 — iCloud로 기기 간 동기화."],
        ],
        "rank_kicker": "순위 변동", "rank_num": "6시간마다",
        "rank_h2": "트렌드는 목록이 아니라 <em>움직임</em>입니다.",
        "rank_lede": "차트는 '지금 큰 것'을 보여줄 뿐입니다. 무엇이 커질지는 움직임이 말해주죠. Sidefeed는 하루 내내 차트를 스냅샷해 모든 영상에 6시간 변화량을 붙입니다.",
        "rank_rows": [
            ["6시간 전 #18", "지금 #3", '🇺🇸 게임 · <span class="d-up">▲15</span>'],
            ["6시간 전 #9", "지금 #2", '🇰🇷 음악 · <span class="d-up">▲7</span>'],
            ["6시간 전 —", "지금 #5", '🇯🇵 엔터 · <span class="d-new">NEW</span>'],
            ["6시간 전 #4", "지금 #11", '🇬🇧 스포츠 · <span class="d-down">▼7</span>'],
        ],
        "views_kicker": "구성", "views_num": "4개의 뷰",
        "views_h2": "네 개의 뷰, <em>하나의 리서치 플로우</em>.",
        "views_lede": "공식 차트, 자체 랭킹, 카테고리 발견, 시장 전환 — 전부 공개 데이터 기반이라 누가 봐도 같은 화면입니다.",
        "views": [
            ["🔥", "트렌딩", "YouTube 공식 인기 차트에 6시간 순위 뱃지, Top Movers, 카테고리 분포 바를 얹었습니다."],
            ["📡", "레이더", "Sidefeed 자체 랭킹. 트렌딩 차트 밖에서 올라오는 급상승작까지 포착합니다."],
            ["✨", "발견", "14개 카테고리별 인기 영상. 공개 인기 데이터 그대로, 개인화 없음."],
            ["🌍", "12개국", "국기 탭 한 번으로 시장 비교. 지금 도쿄의 1위는 무엇일까요?"],
        ],
        "shots_kicker": "화면", "shots_num": "IOS 17+",
        "shots_h2": "둘러보는 피드가 아니라 <em>리서치 데스크</em>.",
        "shots_caps": ["레이더 · 급상승 랭킹", "12개국 전환", "발견 · 14 카테고리"],
        "feat_kicker": "디테일", "feat_num": "06",
        "feat_h2": "리서치를 위한 <em>분명한 선택</em>.",
        "feats": [
            ["로그인·개인화 없음", "구글 계정도 시청기록도 필요 없습니다. 알고리즘이 고른 피드가 아니라, 모두에게 같은 공개 트렌드를 봅니다."],
            ["6시간 스냅샷", "하루 내내 차트를 스냅샷해 순위 이력을 계산합니다. YouTube에서는 볼 수 없는 움직임입니다."],
            ["인사이트 시트", "영상을 탭하면 현재 순위·6시간 변화·카테고리·조회 속도를 먼저 확인. YouTube 이동은 그다음."],
            ["쇼츠 필터", "롱폼만 리서치하고 싶을 때, 토글 하나로 모든 피드에서 쇼츠 제외."],
            ["나중에 보기 + iCloud", "참고 영상을 저장하면 내 iCloud로 기기 간 동기화됩니다."],
            ["피드 제어", "채널 차단·관심없음으로 리서치에 잡음이 끼지 않게."],
        ],
        "final_h2": "다음 영상, 감이 아니라 데이터로.", "final_lede": "iPhone &amp; iPad 무료 다운로드.",
        "f_contact": "문의", "f_privacy": "개인정보 처리방침", "f_terms": "이용약관",
    },
    "ja": {
        "dir": "ja/", "lang": "ja", "font": '"Hiragino Kaku Gothic ProN", "Hiragino Sans", "Yu Gothic"', "shots": "ja",
        "title": "Sidefeed — クリエイターのための12ヶ国トレンドリサーチ",
        "desc": "12ヶ国のYouTube公式トレンド、14カテゴリ、6時間の順位変動。Googleログイン不要、パーソナライズなしのフィードで、いま伸びている流れを読む。",
        "og_title": "Sidefeed — クリエイターのトレンドリサーチ",
        "og_desc": "12ヶ国 · 14カテゴリ · 6時間の順位変動。アルゴリズムより先に、次の動画のヒントを。",
        "kicker_num": "トレンドリサーチ",
        "h1": "次の動画のヒントを、<br>アルゴリズムより<em>先に</em>。",
        "demo_items": [
            ["🇯🇵", "エンタメ", "#24", "#6", "▲18 · 6時間", "up"],
            ["🇺🇸", "ゲーム", "#18", "#3", "▲15 · 6時間", "up"],
            ["🇰🇷", "音楽", "—", "#5", "NEW", "new"],
            ["🇬🇧", "スポーツ", "#21", "#6", "▲15 · 6時間", "up"],
        ],
        "sub": "SidefeedはYouTubeクリエイター・企画者のためのトレンドリサーチツール。12ヶ国の公式トレンド、14カテゴリ、6時間の順位変動 — パーソナライズのないフィードで、いま上がってきている流れをそのまま読めます。",
        "badge_small": "ダウンロードは", "note": "無料ダウンロード · iPhone &amp; iPad · Googleログイン不要",
        "badge_aria": "App Store でダウンロード",
        "chips": [["up", "▲9", "急上昇"], ["new", "N", "NEW入り"], ["", "🌍", "12ヶ国"], ["", "🎵", "14カテゴリ"]],
        "hero_alt": "Sidefeedのトレンド画面 — 順位変動バッジとカテゴリ分布バー付きの日本のYouTubeチャート",
        "marquee": ["アメリカ", "日本", "イギリス", "ドイツ", "オーストラリア", "カナダ", "フランス", "韓国", "スイス", "オランダ", "スウェーデン", "シンガポール"],
        "how_kicker": "使い方",
        "how_h2": "「次は何を作る？」から<em>データに裏付けられた企画へ</em>。",
        "steps": [
            ["国", "市場を選ぶ", "国旗ボタンひとつで12ヶ国を切り替え。朝は日本、昼はアメリカ — 各市場のYouTube公式トレンドチャートをそのまま見られます。"],
            ["シグナル", "動きを読む", "すべての動画に6時間の順位変動が付きます。▲上昇、▼下降、NEW初登場。Top Moversが最速の上昇作を、レーダーがチャート圏外の急上昇を捉えます。"],
            ["リサーチ", "ヒントを残す", "インサイトシートで順位履歴・カテゴリ・再生ペースを確認。参考動画は「後で見る」に保存 — iCloudで端末間同期。"],
        ],
        "rank_kicker": "順位変動", "rank_num": "6時間ごと",
        "rank_h2": "トレンドはリストではなく<em>動き</em>。",
        "rank_lede": "チャートは「いま大きいもの」を見せるだけ。これから伸びるものは動きが教えてくれます。Sidefeedは一日を通してチャートをスナップショットし、全動画に6時間の変化量を表示します。",
        "rank_rows": [
            ["6時間前 #18", "いま #3", '🇺🇸 ゲーム · <span class="d-up">▲15</span>'],
            ["6時間前 #24", "いま #6", '🇯🇵 エンタメ · <span class="d-up">▲18</span>'],
            ["6時間前 —", "いま #5", '🇰🇷 音楽 · <span class="d-new">NEW</span>'],
            ["6時間前 #4", "いま #11", '🇬🇧 スポーツ · <span class="d-down">▼7</span>'],
        ],
        "views_kicker": "構成", "views_num": "4つのビュー",
        "views_h2": "4つのビュー、<em>ひとつのリサーチフロー</em>。",
        "views_lede": "公式チャート、独自ランキング、カテゴリ発見、市場切り替え — すべて公開データなので、誰が見ても同じ画面です。",
        "views": [
            ["🔥", "トレンド", "YouTube公式の人気チャートに6時間の順位バッジ、Top Movers、カテゴリ分布バーを追加。"],
            ["📡", "レーダー", "Sidefeed独自のランキング。トレンドチャート圏外から上がってくる急上昇作まで捕捉。"],
            ["✨", "発見", "14カテゴリ別の人気動画。公開データそのまま、パーソナライズなし。"],
            ["🌍", "12ヶ国", "国旗をタップして市場を比較。いまソウルの1位は？"],
        ],
        "shots_kicker": "画面", "shots_num": "IOS 17+",
        "shots_h2": "眺めるフィードではなく、<em>リサーチデスク</em>。",
        "shots_caps": ["レーダー · 急上昇ランキング", "12ヶ国スイッチャー", "発見 · 14カテゴリ"],
        "feat_kicker": "こだわり", "feat_num": "06",
        "feat_h2": "リサーチのための<em>明確な選択</em>。",
        "feats": [
            ["ログイン・パーソナライズなし", "Googleアカウントも視聴履歴も不要。アルゴリズムが選んだフィードではなく、誰にとっても同じ公開トレンドを見られます。"],
            ["6時間スナップショット", "一日を通してチャートをスナップショットし、順位履歴を計算。YouTube本体では見えない動きです。"],
            ["インサイトシート", "動画をタップすると現在順位・6時間変動・カテゴリ・再生ペースを先に確認。YouTubeへはその後。"],
            ["ショートフィルター", "長尺だけをリサーチしたいときは、トグルひとつで全フィードからショートを除外。"],
            ["後で見る + iCloud", "参考動画を保存すれば、自分のiCloudで端末間に同期。"],
            ["フィード制御", "チャンネルブロック・興味なしで、リサーチからノイズを排除。"],
        ],
        "final_h2": "次の動画は、勘ではなくデータで。", "final_lede": "iPhone &amp; iPad 無料ダウンロード。",
        "f_contact": "お問い合わせ", "f_privacy": "プライバシーポリシー", "f_terms": "利用規約",
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


def badge(loc, el_id):
    return (f'<a class="store-badge" id="{el_id}" href="{APP_STORE_URL}" aria-label="{loc["badge_aria"]}">{APPLE_SVG}'
            f'<span class="txt"><small>{loc["badge_small"]}</small><strong>App Store</strong></span></a>')


def render(key):
    loc = LOCALES[key]
    rel = "../" if loc["dir"] else ""
    font_override = f'<style>body{{font-family:-apple-system,BlinkMacSystemFont,{loc["font"]},"Segoe UI",sans-serif}}</style>' if loc["font"] else ""
    chips = "".join(
        f'<div class="chip c{i+1}"><span class="g {cls}">{g}</span>{label}</div>'
        for i, (cls, g, label) in enumerate(loc["chips"])
    )
    marquee = "".join(f"<span>{m}</span>" for m in loc["marquee"] * 2)
    steps = "".join(
        f'<div class="step"><span class="n">0{i+1}</span><span class="tag">{tag}</span><h3>{h}</h3><p>{p}</p></div>'
        for i, (tag, h, p) in enumerate(loc["steps"])
    )
    rank_rows = "".join(
        f'<div class="rank-row"><span class="was">{a}</span><span class="arrow">→</span><span class="to">{b}</span><span class="cat">{c}</span></div>'
        for a, b, c in loc["rank_rows"]
    )
    views = "".join(
        f'<div class="view-card"><span class="ico">{ico}</span><h3>{h}</h3><p>{p}</p></div>'
        for ico, h, p in loc["views"]
    )
    shot_files = ["radar", "country", "discover"]
    shots = "".join(
        f'<figure><div class="phone"><img src="{rel}assets/shot-{loc["shots"]}-{f}.png" alt="{cap}" loading="lazy"><div class="island"></div></div><figcaption>{cap}</figcaption></figure>'
        for f, cap in zip(shot_files, loc["shots_caps"])
    )
    feats = "".join(f'<div class="feat"><h3>{h}</h3><p>{p}</p></div>' for h, p in loc["feats"])
    demo_json = json.dumps(loc["demo_items"], ensure_ascii=False)
    d0 = loc["demo_items"][0]

    html = f"""<!doctype html>
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
    <a class="wordmark" href="{rel if rel else './'}"><img src="{rel}assets/icon-180.png" alt=""><span>SIDEFEED</span></a>
    <div class="lang">{lang_nav(loc['dir'], rel)}</div>
  </div>
</nav>

<header class="hero">
  <div class="ghost">S·F</div>
  <div class="wrap">
    <div>
      <div class="kicker"><span>SIDEFEED</span><span class="rule"></span><span class="num">{loc['kicker_num']}</span></div>
      <h1>{loc['h1']}</h1>
      <div class="demo" id="demo">
        <span class="flag" id="demoFlag">{d0[0]}</span>
        <span class="cat" id="demoCat">{d0[1]}</span>
        <span class="from" id="demoFrom">{d0[2]}</span>
        <span class="arrow">→</span>
        <span class="to" id="demoTo">{d0[3]}</span>
        <span class="delta {('new' if d0[5] == 'new' else '')}" id="demoDelta">{d0[4]}</span>
      </div>
      <p class="sub">{loc['sub']}</p>
      <div class="cta">
        {badge(loc, 'storeLink')}
        <span class="note">{loc['note']}</span>
      </div>
    </div>
    <div class="phone-col">
      {chips}
      <div class="phone"><img src="{rel}assets/shot-{loc['shots']}-trending.png" alt="{loc['hero_alt']}"><div class="island"></div></div>
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
    <div class="kicker"><span>{loc['rank_kicker']}</span><span class="rule"></span><span class="num">{loc['rank_num']}</span></div>
    <h2>{loc['rank_h2']}</h2>
    <p class="lede">{loc['rank_lede']}</p>
    <div class="rank-table">{rank_rows}</div>
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap">
    <div class="kicker"><span>{loc['views_kicker']}</span><span class="rule"></span><span class="num">{loc['views_num']}</span></div>
    <h2>{loc['views_h2']}</h2>
    <p class="lede">{loc['views_lede']}</p>
    <div class="views">{views}</div>
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
      <a href="https://kkiruk-studio.github.io/privacy-policy-app/">{loc['f_privacy']}</a>
      <a href="https://kkiruk-studio.github.io/terms-of-service-app/">{loc['f_terms']}</a>
    </div>
    <div>© 2026 kkiruk studio</div>
    <div class="yt-note">YouTube is a trademark of Google LLC. Sidefeed is an independent app and is not endorsed by or affiliated with YouTube.</div>
  </div>
</footer>

<script>
  const items = {demo_json};
  const el = {{
    demo: document.getElementById("demo"),
    flag: document.getElementById("demoFlag"),
    cat: document.getElementById("demoCat"),
    from: document.getElementById("demoFrom"),
    to: document.getElementById("demoTo"),
    delta: document.getElementById("demoDelta"),
  }};
  if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {{
    let i = 0;
    setInterval(() => {{
      i = (i + 1) % items.length;
      const [flag, cat, from, to, delta, kind] = items[i];
      el.flag.textContent = flag;
      el.cat.textContent = cat;
      el.from.textContent = from;
      el.to.textContent = to;
      el.delta.textContent = delta;
      el.delta.classList.toggle("new", kind === "new");
      el.demo.classList.remove("tick");
      void el.demo.offsetWidth;
      el.demo.classList.add("tick");
    }}, 2800);
  }}
</script>
</body>
</html>
"""
    out = ROOT / loc["dir"] / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)} ({len(html)} bytes)")


for key in LOCALES:
    render(key)
