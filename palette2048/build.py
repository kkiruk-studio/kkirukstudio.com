#!/usr/bin/env python3
"""Generate the Palette landing for every locale from one template.
Output: index.html (en), ko.html, ja.html, zh-hans.html, zh-hant.html (flat,
to keep the live URLs). Edit this file, not the generated HTML; run `python3 build.py`.
"""
import pathlib
ROOT = pathlib.Path(__file__).parent
APP = "https://apps.apple.com/app/id6767449110"   # Palette: Daily Art Puzzle — live 2026-07-08
SVG = '<svg viewBox="0 0 384 512" aria-hidden="true"><path d="M318.7 268.7c-.2-36.7 16.4-64.4 50-84.8-18.8-26.9-47.2-41.7-84.7-44.6-35.5-2.8-74.3 20.7-88.5 20.7-15 0-49.4-19.7-76.4-19.7C63.3 141.2 4 184.8 4 273.5q0 39.3 14.4 81.2c12.8 36.7 59 126.7 107.2 125.2 25.2-.6 43-17.9 75.8-17.9 31.8 0 48.3 17.9 76.4 17.9 48.6-.7 90.4-82.5 102.6-119.3-65.2-30.7-61.7-90-61.7-91.9zm-56.6-164.2c27.3-32.4 24.8-61.9 24-72.5-24.1 1.4-52 16.4-67.9 34.9-17.5 19.8-27.8 44.3-25.6 71.9 26.1 2 49.9-11.4 69.5-34.3z"/></svg>'
LANGS = [("en","index.html","English"),("ko","ko.html","한국어"),("ja","ja.html","日本語"),
         ("zh-Hans","zh-hans.html","简体中文"),("zh-Hant","zh-hant.html","繁體中文")]
MARQUEE = ["VAN GOGH","MONET","HOKUSAI","KLIMT","VERMEER","WARHOL","DA VINCI","MUNCH","KIM HONG-DO","RENOIR"]
SHOTS = [("assets/shot3.png","s_cap1"),("assets/shot1.png","s_cap2"),("assets/shot2.png","s_cap3")]

L = {
"en": dict(htmllang="en", soon="Coming soon", cta_soon="Coming soon to the App Store", brand="Palette", self="index.html",
 title="Palette: Daily Art Puzzle — Play a famous painting's colors",
 desc="A daily color puzzle: the board is painted with a real masterpiece's palette. Merge by color — no numbers. And every Saturday, guess the painting from its colors alone.",
 ogt="Palette — Play a famous painting's colors", ogd="A new masterpiece every day. Merge by color, complete the painting. Saturdays: guess the artwork from its colors.",
 kicker="A MUSEUM IN YOUR POCKET", knum="DAILY",
 hmsg="A new masterpiece,<br>every single day.",
 hsub="Each day the board is painted with the palette of a real masterpiece.<br>Merge tiles <strong>by color</strong> — there are no numbers. Just the painting.",
 cta="Download on the App Store", rating="Daily · Free to play", hfoot="122 masterpieces · iPhone &amp; iPad · No ads · Offline",
 how_k="HOW IT WORKS", how_t="From a blank board to a finished painting —<br>in a few swipes.",
 steps=[("TODAY","Open today's painting","A new masterpiece's palette is waiting — no setup, no levels."),
        ("PLAY","Merge by color","Swipe to combine same-colored tiles; they bloom into the next shade."),
        ("SATURDAY","Guess the mystery","On Saturdays the title hides — name the artwork from its colors.")],
 wlabel="WHY IT'S DIFFERENT", wtitle="No numbers.<br>Your eye is the game.",
 c1tag="NUMBER PUZZLES", c1note="Chasing a number. Same gray tiles, every day.",
 c2tag="PALETTE", c2note="Chasing a painting. A new palette to feel, every day.",
 punch="Merge two of the same color, and it blooms into the next.",
 mlabel="EVERY SATURDAY", mtitle="The Mystery Day.",
 msub="On Saturdays the title is hidden. Play the colors — then name the masterpiece from its palette alone. How well do you really know your art?",
 s_label="SCREENS", s_title="The same game, a different painting every day.",
 s_cap1="3×3 · everyday", s_cap2="4×4 · deeper palette", s_cap3="5×5 · the whole painting",
 flabel="DETAILS", ftitle="A calm daily ritual, built from real art.",
 f=[("One masterpiece a day","122 curated paintings — Van Gogh, Monet, Hokusai, Kim Hong-do, and more."),
    ("Colors, not numbers","Tiles are pure color, blending toward the next palette shade. A quiet test of your eye."),
    ("Saturday Mystery","Guess the hidden artwork from its colors alone — a weekly event for art lovers."),
    ("The archive","Missed a day? Replay past paintings from a color calendar of everything you've played."),
    ("Streaks &amp; stats","Keep a daily streak, track your best on every painting, and grow your collection."),
    ("Quiet by design","No ads. No login. Fully offline. Just one painting, at your own pace.")],
 ctitle="Today's painting is<br>already on the wall.", csub="Free to play · 122 masterpieces · iPhone &amp; iPad",
 fc="Contact", fp="Privacy", ft="Terms"),

"ko": dict(htmllang="ko", soon="곧 출시", cta_soon="App Store 곧 출시", brand="Palette", self="ko.html",
 title="Palette: 매일 명화 퍼즐 — 명화의 색으로 즐기는 퍼즐",
 desc="매일 보드가 실제 명화의 팔레트로 칠해집니다. 숫자 없이 색으로 타일을 합쳐 그림을 완성하세요. 토요일엔 색만 보고 그림을 맞히는 미스터리 데이.",
 ogt="Palette — 매일 명화의 색으로", ogd="매일 새로운 명화. 색으로 합쳐 그림을 완성하고, 토요일엔 색만 보고 작품을 맞혀보세요.",
 kicker="포켓 속 미술관", knum="DAILY",
 hmsg="매일 새로운 명화,<br>한 점씩.",
 hsub="매일 보드가 실제 명화의 팔레트로 칠해집니다.<br>숫자 없이 <strong>색</strong>으로 타일을 합쳐 그림을 완성하세요.",
 cta="App Store에서 다운로드", rating="매일 · 무료 플레이", hfoot="명화 122점 · 아이폰 &amp; 아이패드 · 광고 없음 · 오프라인",
 how_k="사용 방법", how_t="빈 보드에서 완성된 그림까지 —<br>몇 번의 스와이프로.",
 steps=[("오늘","오늘의 그림 열기","새 명화의 팔레트가 기다려요 — 설정도 레벨도 없이."),
        ("플레이","색으로 합치기","같은 색 타일을 밀어 합치면 다음 색으로 피어나요."),
        ("토요일","미스터리 맞히기","토요일엔 제목이 숨겨져요 — 색만 보고 작품을 맞혀보세요.")],
 wlabel="왜 다를까", wtitle="숫자가 없습니다.<br>당신의 눈이 게임이에요.",
 c1tag="보통의 숫자 퍼즐", c1note="숫자만 쫓는 회색 타일. 매일 똑같죠.",
 c2tag="PALETTE", c2note="명화를 쫓는 게임. 매일 느낄 새로운 팔레트.",
 punch="같은 색 두 개를 합치면, 다음 색으로 피어납니다.",
 mlabel="매주 토요일", mtitle="미스터리 데이.",
 msub="토요일엔 작품명이 가려집니다. 색을 플레이한 뒤, 팔레트만 보고 명화를 맞혀보세요. 당신의 안목은 얼마나 정확할까요?",
 s_label="스크린", s_title="같은 게임, 매일 다른 그림.",
 s_cap1="3×3 · 매일", s_cap2="4×4 · 깊어진 팔레트", s_cap3="5×5 · 그림 전체",
 flabel="디테일", ftitle="진짜 명화로 만든, 조용한 하루 의식.",
 f=[("매일 한 점의 명화","엄선한 명화 122점 — 반 고흐, 모네, 호쿠사이, 김홍도 등."),
    ("숫자가 아닌 색","타일은 순수한 색, 합치면 팔레트의 다음 색으로. 조용한 색각 테스트예요."),
    ("토요일 미스터리","색만 보고 가려진 작품을 맞혀보세요 — 미술 애호가를 위한 주간 이벤트."),
    ("아카이브","놓친 날이 있나요? 플레이한 모든 그림을 색 캘린더에서 다시 플레이."),
    ("스트릭 &amp; 통계","매일 연속 기록을 쌓고, 그림별 최고 기록과 컬렉션을 키워보세요."),
    ("비우는 디자인","광고 없음. 로그인 없음. 완전 오프라인. 하루 한 점, 내 속도로.")],
 ctitle="오늘의 그림이<br>이미 벽에 걸렸어요.", csub="무료 플레이 · 명화 122점 · 아이폰 &amp; 아이패드",
 fc="문의", fp="개인정보", ft="약관"),

"ja": dict(htmllang="ja", soon="近日公開", cta_soon="App Storeで近日公開", brand="Palette", self="ja.html",
 title="Palette: 名画の色パズル — 毎日、名画の色で遊ぶ",
 desc="毎日、ボードが実際の名画のパレットで彩られます。数字ではなく色でタイルを合わせて絵を完成。土曜日は色だけで作品を当てるミステリーデー。",
 ogt="Palette — 名画の色で遊ぶ", ogd="毎日新しい名画。色を合わせて絵を完成、土曜日は色だけで作品を当ててみましょう。",
 kicker="ポケットの中の美術館", knum="DAILY",
 hmsg="毎日、新しい名画を<br>一枚ずつ。",
 hsub="毎日ボードが実際の名画のパレットで彩られます。<br>数字はありません。<strong>色</strong>でタイルを合わせて絵を完成させましょう。",
 cta="App Storeでダウンロード", rating="毎日 · 無料で遊べる", hfoot="名画122点 · iPhone &amp; iPad · 広告なし · オフライン",
 how_k="使い方", how_t="空のボードから完成した絵まで —<br>数回のスワイプで。",
 steps=[("今日","今日の名画を開く","新しい名画のパレットが待っています — 設定もレベルもなし。"),
        ("プレイ","色で合わせる","同じ色のタイルを滑らせて合わせると、次の色へ。"),
        ("土曜日","ミステリーを当てる","土曜日は作品名が隠れます — 色だけで作品を当てて。")],
 wlabel="なぜ違うのか", wtitle="数字はありません。<br>あなたの目が勝負です。",
 c1tag="ふつうの数字パズル", c1note="数字を追うだけ。毎日同じグレーのタイル。",
 c2tag="PALETTE", c2note="名画を追う遊び。毎日新しいパレットを。",
 punch="同じ色を二つ合わせると、次の色へと花開きます。",
 mlabel="毎週土曜日", mtitle="ミステリーデー。",
 msub="土曜日は作品名が隠れます。色をプレイし、パレットだけで名画を当ててください。あなたの審美眼はどれくらいでしょう。",
 s_label="スクリーン", s_title="同じゲーム、毎日違う絵。",
 s_cap1="3×3 · 毎日", s_cap2="4×4 · 深いパレット", s_cap3="5×5 · 絵の全体",
 flabel="ディテール", ftitle="本物のアートでつくる、静かな毎日の習慣。",
 f=[("毎日一枚の名画","厳選した名画122点 — ゴッホ、モネ、北斎、金弘道など。"),
    ("数字ではなく色","タイルは純粋な色、合わせるとパレットの次の色へ。静かな色覚テスト。"),
    ("土曜ミステリー","色だけで隠れた作品を当てる — アート好きのための週イベント。"),
    ("アーカイブ","見逃した日も、遊んだ全作品をカラーカレンダーから再プレイ。"),
    ("ストリーク &amp; 統計","毎日の連続記録を伸ばし、作品ごとのベストとコレクションを育てよう。"),
    ("静かなデザイン","広告なし。ログインなし。完全オフライン。一日一枚、自分のペースで。")],
 ctitle="今日の絵は<br>もう壁に掛かっています。", csub="無料で遊べる · 名画122点 · iPhone &amp; iPad",
 fc="お問い合わせ", fp="プライバシー", ft="規約"),

"zh-Hans": dict(htmllang="zh-Hans", soon="即将推出", cta_soon="即将登陆 App Store", brand="Palette", self="zh-hans.html",
 title="Palette：每日名画拼图 — 每天用名画的颜色玩的拼图",
 desc="每天，棋盘都被一幅真实名画的调色板点亮。不用数字，用颜色合并拼出画作。周六是只凭颜色猜画的谜题日。",
 ogt="Palette — 用名画的颜色游玩", ogd="每天一幅新名画。合并颜色拼出画作，周六只凭颜色猜出作品。",
 kicker="口袋里的美术馆", knum="DAILY",
 hmsg="每天一幅<br>全新名画。",
 hsub="每天棋盘都被一幅真实名画的调色板点亮。<br>没有数字，用<strong>颜色</strong>合并拼出完整的画作。",
 cta="在 App Store 下载", rating="每天 · 免费畅玩", hfoot="122 幅名画 · iPhone 和 iPad · 无广告 · 离线",
 how_k="玩法", how_t="从空棋盘到完成的画作 —<br>只需几次滑动。",
 steps=[("今天","打开今天的名画","一幅新名画的调色板在等你 — 无需设置，没有关卡。"),
        ("游玩","用颜色合并","滑动合并相同颜色的方块，它便绽放成下一种色。"),
        ("周六","猜出谜题","周六隐藏标题 — 只凭颜色认出作品。")],
 wlabel="有何不同", wtitle="没有数字。<br>你的眼睛就是游戏。",
 c1tag="普通的数字拼图", c1note="只追数字。每天都是同样的灰色方块。",
 c2tag="PALETTE", c2note="追逐一幅画。每天都有新的色彩。",
 punch="把两个相同的颜色合并，它便绽放成下一种。",
 mlabel="每周六", mtitle="谜题日。",
 msub="周六隐藏作品名称。先玩颜色，再仅凭调色板认出名画。你对艺术的眼力有多准？",
 s_label="截图", s_title="同样的游戏，每天不同的画。",
 s_cap1="3×3 · 日常", s_cap2="4×4 · 更深的调色板", s_cap3="5×5 · 完整画作",
 flabel="细节", ftitle="用真实艺术打造的，宁静的每日仪式。",
 f=[("每天一幅名画","精选名画 122 幅 — 梵高、莫奈、北斋、金弘道等。"),
    ("颜色，而非数字","方块是纯粹的颜色，合并后融入调色板的下一种色。一场安静的色觉测试。"),
    ("周六谜题","仅凭颜色认出隐藏的作品 — 为爱艺术的你准备的每周活动。"),
    ("归档","错过了某天？在色彩日历里重玩你玩过的所有画作。"),
    ("连胜 &amp; 统计","保持每日连胜，记录每幅画的最佳成绩，壮大你的收藏。"),
    ("极简设计","无广告。无需登录。完全离线。每天一幅，随你的节奏。")],
 ctitle="今天的画<br>已经挂在墙上。", csub="免费畅玩 · 122 幅名画 · iPhone 和 iPad",
 fc="联系", fp="隐私", ft="条款"),

"zh-Hant": dict(htmllang="zh-Hant", soon="即將推出", cta_soon="即將登陸 App Store", brand="Palette", self="zh-hant.html",
 title="Palette：每日名畫拼圖 — 每天用名畫的顏色玩的拼圖",
 desc="每天，棋盤都被一幅真實名畫的調色盤點亮。不用數字，用顏色合併拼出畫作。週六是只憑顏色猜畫的謎題日。",
 ogt="Palette — 用名畫的顏色遊玩", ogd="每天一幅新名畫。合併顏色拼出畫作，週六只憑顏色猜出作品。",
 kicker="口袋裡的美術館", knum="DAILY",
 hmsg="每天一幅<br>全新名畫。",
 hsub="每天棋盤都被一幅真實名畫的調色盤點亮。<br>沒有數字，用<strong>顏色</strong>合併拼出完整的畫作。",
 cta="在 App Store 下載", rating="每天 · 免費暢玩", hfoot="122 幅名畫 · iPhone 和 iPad · 無廣告 · 離線",
 how_k="玩法", how_t="從空棋盤到完成的畫作 —<br>只需幾次滑動。",
 steps=[("今天","打開今天的名畫","一幅新名畫的調色盤在等你 — 無需設定，沒有關卡。"),
        ("遊玩","用顏色合併","滑動合併相同顏色的方塊，它便綻放成下一種色。"),
        ("週六","猜出謎題","週六隱藏標題 — 只憑顏色認出作品。")],
 wlabel="有何不同", wtitle="沒有數字。<br>你的眼睛就是遊戲。",
 c1tag="普通的數字拼圖", c1note="只追數字。每天都是同樣的灰色方塊。",
 c2tag="PALETTE", c2note="追逐一幅畫。每天都有新的色彩。",
 punch="把兩個相同的顏色合併，它便綻放成下一種。",
 mlabel="每週六", mtitle="謎題日。",
 msub="週六隱藏作品名稱。先玩顏色，再僅憑調色盤認出名畫。你對藝術的眼力有多準？",
 s_label="截圖", s_title="同樣的遊戲，每天不同的畫。",
 s_cap1="3×3 · 日常", s_cap2="4×4 · 更深的調色盤", s_cap3="5×5 · 完整畫作",
 flabel="細節", ftitle="用真實藝術打造的，寧靜的每日儀式。",
 f=[("每天一幅名畫","精選名畫 122 幅 — 梵谷、莫內、北齋、金弘道等。"),
    ("顏色，而非數字","方塊是純粹的顏色，合併後融入調色盤的下一種色。一場安靜的色覺測試。"),
    ("週六謎題","僅憑顏色認出隱藏的作品 — 為愛藝術的你準備的每週活動。"),
    ("典藏","錯過了某天？在色彩日曆裡重玩你玩過的所有畫作。"),
    ("連勝 &amp; 統計","保持每日連勝，記錄每幅畫的最佳成績，壯大你的收藏。"),
    ("極簡設計","無廣告。無須登入。完全離線。每天一幅，隨你的節奏。")],
 ctitle="今天的畫<br>已經掛在牆上。", csub="免費暢玩 · 122 幅名畫 · iPhone 和 iPad",
 fc="聯絡", fp="隱私", ft="條款"),
}

def langsel(cur):
    short={'en':'EN','ko':'한국어','ja':'日本語','zh-Hans':'简体中文','zh-Hant':'繁體中文'}
    return "\n".join(f'        <option value="{f}"{" selected" if c==cur else ""}>{short[c]}</option>' for c,f,_ in LANGS)
def hreflang():
    out=[f'<link rel="alternate" hreflang="{c}" href="https://www.kkirukstudio.com/palette2048/{f}">' for c,f,_ in LANGS]
    out.append('<link rel="alternate" hreflang="x-default" href="https://www.kkirukstudio.com/palette2048/index.html">')
    return "\n".join(out)
def footlangs(cur):
    return "\n".join(f'      <a href="{f}">{name}</a>' for c,f,name in LANGS if c!=cur)
def steps_html(d):
    return "".join(f'<div class="step"><span class="n">0{i+1}</span><span class="tag">{t}</span><h3>{h}</h3><p>{p}</p></div>'
                   for i,(t,h,p) in enumerate(d["steps"]))
def feats_html(d):
    sw=['s1','s2','s3','s4','s5','s6']
    return "".join(f'<div class="feature"><div class="f-swatch {sw[i]}"></div><h3>{h}</h3><p>{p}</p></div>'
                   for i,(h,p) in enumerate(d["f"]))
def shots_html(d):
    return "".join(f'<figure><div class="shot-phone"><div class="island"></div><img src="{src}" alt="{d[cap]}" loading="lazy"></div><figcaption>{d[cap]}</figcaption></figure>'
                   for src,cap in SHOTS)
def marquee_html():
    return "".join(f"<span>{m}</span>" for m in MARQUEE*2)

TMPL='''<!DOCTYPE html>
<html lang="{htmllang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{hreflang}
<link rel="canonical" href="https://www.kkirukstudio.com/palette2048/{self}">
<meta property="og:title" content="{ogt}">
<meta property="og:description" content="{ogd}">
<link rel="icon" type="image/png" href="icon.png">
<link rel="apple-touch-icon" href="icon-180.png">
<meta property="og:image" content="icon.png">
<meta property="og:type" content="website">
<link rel="stylesheet" href="style.css">
<script src="/ga.js"></script>
</head>
<body>

<header>
  <div class="bar">
    <a class="wordmark" href="{self}"><img class="brand-icon" src="icon.png" alt="" width="26" height="26">{brand}</a>
    <nav class="nav-right">
      <select class="lang-select" onchange="location.href=this.value" aria-label="Language">
{langsel}
      </select>
      {nav_cta}
    </nav>
  </div>
</header>

<main>
<div class="hero">
  <div class="hero-copy">
    <p class="kicker">{kicker}</p>
    <h1 class="hero-msg">{hmsg}</h1>
    <p class="hero-sub">{hsub}</p>
    <div class="hero-cta-row">
      {store_btn}
      <span class="rating"><span class="stars">★★★★★</span>{rating}</span>
    </div>
    <p class="hero-foot">{hfoot}</p>
  </div>
  <div class="board-col">
    <div class="diptych">
      <img id="paintImg" class="paint-img" src="assets/paintings/starry-night.jpg" alt="" aria-hidden="true">
      <span class="diptych-arrow" aria-hidden="true">&rarr;</span>
      <div class="frame">
        <div class="board" id="board" aria-hidden="true">
          <span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span>
        </div>
      </div>
    </div>
    <p class="board-caption"><span id="paintName">The Starry Night</span><br><em id="paintArtist">Vincent van Gogh</em></p>
  </div>
</div>

<section>
  <div class="wrap">
    <p class="sec-label">{wlabel}</p>
    <h2 class="sec-title">{wtitle}</h2>
    <div class="idea-cards">
      <div class="idea-card">
        <p class="tag">{c1tag}</p>
        <div class="mini-grid nums"><i>2</i><i>4</i><i>8</i><i>16</i></div>
        <p class="note">{c1note}</p>
      </div>
      <div class="idea-card today">
        <p class="tag">{c2tag}</p>
        <div class="mini-grid swatches"><i></i><i></i><i></i><i></i></div>
        <p class="note">{c2note}</p>
      </div>
    </div>
    <p class="idea-punch">{punch}</p>
  </div>
</section>

<section class="mystery">
  <div class="wrap">
    <p class="sec-label">{mlabel}</p>
    <h2 class="sec-title">{mtitle}</h2>
    <p class="sec-sub">{msub}</p>
    <div class="mystery-card">
      <div class="q">? ? ?</div>
      <div class="choices"><span>The Starry Night</span><span class="pick">The Great Wave</span><span>Water Lilies</span></div>
    </div>
  </div>
</section>

<section class="shots">
  <div class="wrap">
    <p class="sec-label">{s_label}</p>
    <h2 class="sec-title">{s_title}</h2>
    <div class="shot-row">{shots}</div>
  </div>
</section>

<section>
  <div class="wrap">
    <p class="sec-label">{flabel}</p>
    <h2 class="sec-title">{ftitle}</h2>
    <div class="features">{feats}</div>
  </div>
</section>

<section class="cta">
  <div class="wrap">
    <h2 class="cta-title">{ctitle}</h2>
    <p class="cta-sub">{csub}</p>
    {store_btn}
  </div>
</section>
</main>

<footer>
  <div class="wrap cols">
    <a class="home-link" href="https://www.kkirukstudio.com/">© kkiruk studio</a>
    <nav class="links">
      <a href="mailto:kkirukstudio.help@gmail.com">{fc}</a>
      <a href="https://kkiruk-studio.github.io/privacy-policy-app/" target="_blank" rel="noopener">{fp}</a>
      <a href="https://kkiruk-studio.github.io/terms-of-service-app/" target="_blank" rel="noopener">{ft}</a>
{footlangs}
    </nav>
  </div>
</footer>

<script src="app.js"></script>
</body>
</html>
'''

for code,fname,_ in LANGS:
    d=L[code]
    params=dict(d)
    # 미출시 상태(APP 플레이스홀더)면 CTA를 비활성 '곧 출시' 스팬으로. 출시 후 APP만 채우고 재실행.
    if "YOURAPPID" in APP:
        nav_cta = f'<span class="nav-cta soon">{d["soon"]}</span>'
        store_btn = f'<span class="appstore-btn soon">{SVG}{d["cta_soon"]}</span>'
    else:
        nav_cta = f'<a class="nav-cta" href="{APP}" target="_blank" rel="noopener">App Store</a>'
        store_btn = f'<a class="appstore-btn" href="{APP}" target="_blank" rel="noopener">{SVG}{d["cta"]}</a>'
    params.update(nav_cta=nav_cta, store_btn=store_btn)
    params.update(svg=SVG, app=APP, hreflang=hreflang(), langsel=langsel(code),
        footlangs=footlangs(code), steps=steps_html(d), feats=feats_html(d),
        shots=shots_html(d), marquee=marquee_html())
    html=TMPL.format(**params)
    (ROOT/fname).write_text(html, encoding="utf-8")
    print("wrote", fname, len(html), "bytes")
