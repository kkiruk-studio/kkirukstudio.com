SVG='<svg viewBox="0 0 384 512" aria-hidden="true"><path d="M318.7 268.7c-.2-36.7 16.4-64.4 50-84.8-18.8-26.9-47.2-41.7-84.7-44.6-35.5-2.8-74.3 20.7-88.5 20.7-15 0-49.4-19.7-76.4-19.7C63.3 141.2 4 184.8 4 273.5q0 39.3 14.4 81.2c12.8 36.7 59 126.7 107.2 125.2 25.2-.6 43-17.9 75.8-17.9 31.8 0 48.3 17.9 76.4 17.9 48.6-.7 90.4-82.5 102.6-119.3-65.2-30.7-61.7-90-61.7-91.9zm-56.6-164.2c27.3-32.4 24.8-61.9 24-72.5-24.1 1.4-52 16.4-67.9 34.9-17.5 19.8-27.8 44.3-25.6 71.9 26.1 2 49.9-11.4 69.5-34.3z"/></svg>'
APP='https://apps.apple.com/app/idYOURAPPID'

LANGS=[('en','index.html','English'),('ko','ko.html','한국어'),('ja','ja.html','日本語'),
       ('zh-Hans','zh-hans.html','简体中文'),('zh-Hant','zh-hant.html','繁體中文')]

L={}
L['en']=dict(htmllang='en',brand='Palette 2048',
 title="Palette 2048 — Play a famous painting's colors, every day",
 desc="A daily color puzzle: the board is painted with a real masterpiece's palette. Merge by color — no numbers. And every Saturday, guess the painting from its colors alone.",
 ogt="Palette 2048 — Play a famous painting's colors", ogd="A new masterpiece every day. Merge by color, complete the painting. Saturdays: guess the artwork from its colors.",
 kicker="A museum in your pocket", hmsg="A new masterpiece,<br>every single day.",
 hsub="Each day the board is painted with the palette of a real masterpiece.<br>Merge tiles <strong>by color</strong> — there are no numbers. Just the painting.",
 cta="Download on the App Store", rating="Daily · Free to play", hfoot="122 masterpieces · iPhone &amp; iPad · No ads · Offline",
 wlabel="Why it's different", wtitle="No numbers.<br>Your eye is the game.",
 c1tag="Ordinary 2048", c1note="Chasing a number. Same gray tiles, every day.",
 c2tag="Palette 2048", c2note="Chasing a painting. A new palette to feel, every day.",
 punch="Merge two of the same color, and it blooms into the next.",
 mlabel="Every Saturday", mtitle="The Mystery Day.",
 msub="On Saturdays the title is hidden. Play the colors — then name the masterpiece from its palette alone. How well do you really know your art?",
 flabel="Inside", ftitle="A calm daily ritual, built from real art.",
 f=[("One masterpiece a day","122 curated paintings — Van Gogh, Monet, Hokusai, Kim Hong-do, and more. Come back tomorrow for the next."),
    ("Colors, not numbers","Tiles are pure color. Merging blends toward the next shade in the painting's palette. A quiet test of your eye."),
    ("Saturday Mystery","Guess the hidden artwork from its colors alone. A weekly event for the art lover in you."),
    ("The archive","Missed a day? Replay past paintings from a color calendar of everything you've played."),
    ("Streaks &amp; stats","Keep a daily streak, track your best run on every painting, and grow your collection."),
    ("Quiet by design","No ads. No login. Plays fully offline. Just one painting, at your own pace.")],
 ctitle="Today's painting is<br>already on the wall.", csub="Free to play · 122 masterpieces · iPhone &amp; iPad",
 fcontact="Contact", fprivacy="Privacy", fterms="Terms")

L['ko']=dict(htmllang='ko',brand='팔레트 2048',
 title="팔레트 2048 — 매일 명화의 색으로 즐기는 퍼즐",
 desc="매일 보드가 실제 명화의 팔레트로 칠해집니다. 숫자 없이 색으로 타일을 합쳐 그림을 완성하세요. 토요일엔 색만 보고 그림을 맞히는 미스터리 데이.",
 ogt="팔레트 2048 — 매일 명화의 색으로", ogd="매일 새로운 명화. 색으로 합쳐 그림을 완성하고, 토요일엔 색만 보고 작품을 맞혀보세요.",
 kicker="포켓 속 미술관", hmsg="매일 새로운 명화,<br>한 점씩.",
 hsub="매일 보드가 실제 명화의 팔레트로 칠해집니다.<br>숫자 없이 <strong>색</strong>으로 타일을 합쳐 그림을 완성하세요.",
 cta="App Store에서 다운로드", rating="매일 · 무료 플레이", hfoot="명화 122점 · 아이폰 &amp; 아이패드 · 광고 없음 · 오프라인",
 wlabel="왜 다를까", wtitle="숫자가 없습니다.<br>당신의 눈이 게임이에요.",
 c1tag="보통의 2048", c1note="숫자만 쫓는 회색 타일. 매일 똑같죠.",
 c2tag="팔레트 2048", c2note="명화를 쫓는 게임. 매일 느낄 새로운 팔레트.",
 punch="같은 색 두 개를 합치면, 다음 색으로 피어납니다.",
 mlabel="매주 토요일", mtitle="미스터리 데이.",
 msub="토요일엔 작품명이 가려집니다. 색을 플레이한 뒤, 팔레트만 보고 명화를 맞혀보세요. 당신의 안목은 얼마나 정확할까요?",
 flabel="둘러보기", ftitle="진짜 명화로 만든, 조용한 하루 의식.",
 f=[("매일 한 점의 명화","엄선한 명화 122점 — 반 고흐, 모네, 호쿠사이, 김홍도 등. 내일은 또 다른 그림이 기다려요."),
    ("숫자가 아닌 색","타일은 순수한 색. 합치면 팔레트의 다음 색으로 섞입니다. 조용한 색각 테스트예요."),
    ("토요일 미스터리","색만 보고 가려진 작품을 맞혀보세요. 미술 애호가를 위한 주간 이벤트."),
    ("아카이브","놓친 날이 있나요? 플레이한 모든 그림을 색 캘린더에서 다시 플레이."),
    ("스트릭 &amp; 통계","매일 연속 기록을 쌓고, 그림별 최고 기록과 컬렉션을 키워보세요."),
    ("비우는 디자인","광고 없음. 로그인 없음. 완전 오프라인. 하루 한 점, 내 속도로.")],
 ctitle="오늘의 그림이<br>이미 벽에 걸렸어요.", csub="무료 플레이 · 명화 122점 · 아이폰 &amp; 아이패드",
 fcontact="문의", fprivacy="개인정보", fterms="약관")

L['ja']=dict(htmllang='ja',brand='Palette 2048',
 title="Palette 2048 — 毎日、名画の色で遊ぶパズル",
 desc="毎日、ボードが実際の名画のパレットで彩られます。数字ではなく色でタイルを合わせて絵を完成。土曜日は色だけで作品を当てるミステリーデー。",
 ogt="Palette 2048 — 名画の色で遊ぶ", ogd="毎日新しい名画。色を合わせて絵を完成、土曜日は色だけで作品を当ててみましょう。",
 kicker="ポケットの中の美術館", hmsg="毎日、新しい名画を<br>一枚ずつ。",
 hsub="毎日ボードが実際の名画のパレットで彩られます。<br>数字はありません。<strong>色</strong>でタイルを合わせて絵を完成させましょう。",
 cta="App Storeでダウンロード", rating="毎日 · 無料で遊べる", hfoot="名画122点 · iPhone &amp; iPad · 広告なし · オフライン",
 wlabel="なぜ違うのか", wtitle="数字はありません。<br>あなたの目が勝負です。",
 c1tag="ふつうの2048", c1note="数字を追うだけ。毎日同じグレーのタイル。",
 c2tag="Palette 2048", c2note="名画を追う遊び。毎日新しいパレットを。",
 punch="同じ色を二つ合わせると、次の色へと花開きます。",
 mlabel="毎週土曜日", mtitle="ミステリーデー。",
 msub="土曜日は作品名が隠れます。色をプレイし、パレットだけで名画を当ててください。あなたの審美眼はどれくらいでしょう。",
 flabel="中身", ftitle="本物のアートでつくる、静かな毎日の習慣。",
 f=[("毎日一枚の名画","厳選した名画122点 — ゴッホ、モネ、北斎、金弘道など。明日はまた別の絵。"),
    ("数字ではなく色","タイルは純粋な色。合わせるとパレットの次の色へ。静かな色覚テスト。"),
    ("土曜ミステリー","色だけで隠れた作品を当てる、アート好きのための週イベント。"),
    ("アーカイブ","見逃した日も、遊んだ全作品をカラーカレンダーから再プレイ。"),
    ("ストリーク &amp; 統計","毎日の連続記録を伸ばし、作品ごとのベストとコレクションを育てよう。"),
    ("静かなデザイン","広告なし。ログインなし。完全オフライン。一日一枚、自分のペースで。")],
 ctitle="今日の絵は<br>もう壁に掛かっています。", csub="無料で遊べる · 名画122点 · iPhone &amp; iPad",
 fcontact="お問い合わせ", fprivacy="プライバシー", fterms="規約")

L['zh-Hans']=dict(htmllang='zh-Hans',brand='Palette 2048',
 title="Palette 2048 — 每天用名画的颜色玩的拼图",
 desc="每天，棋盘都被一幅真实名画的调色板点亮。不用数字，用颜色合并拼出画作。周六是只凭颜色猜画的谜题日。",
 ogt="Palette 2048 — 用名画的颜色游玩", ogd="每天一幅新名画。合并颜色拼出画作，周六只凭颜色猜出作品。",
 kicker="口袋里的美术馆", hmsg="每天一幅<br>全新名画。",
 hsub="每天棋盘都被一幅真实名画的调色板点亮。<br>没有数字，用<strong>颜色</strong>合并拼出完整的画作。",
 cta="在 App Store 下载", rating="每天 · 免费畅玩", hfoot="122 幅名画 · iPhone 和 iPad · 无广告 · 离线",
 wlabel="有何不同", wtitle="没有数字。<br>你的眼睛就是游戏。",
 c1tag="普通的 2048", c1note="只追数字。每天都是同样的灰色方块。",
 c2tag="Palette 2048", c2note="追逐一幅画。每天都有新的色彩。",
 punch="把两个相同的颜色合并，它便绽放成下一种。",
 mlabel="每周六", mtitle="谜题日。",
 msub="周六隐藏作品名称。先玩颜色，再仅凭调色板认出名画。你对艺术的眼力有多准？",
 flabel="内容", ftitle="用真实艺术打造的，宁静的每日仪式。",
 f=[("每天一幅名画","精选名画 122 幅 — 梵高、莫奈、北斋、金弘道等。明天又是另一幅。"),
    ("颜色，而非数字","方块是纯粹的颜色。合并后融入调色板的下一种色。一场安静的色觉测试。"),
    ("周六谜题","仅凭颜色认出隐藏的作品，为爱艺术的你准备的每周活动。"),
    ("归档","错过了某天？在色彩日历里重玩你玩过的所有画作。"),
    ("连胜 &amp; 统计","保持每日连胜，记录每幅画的最佳成绩，壮大你的收藏。"),
    ("极简设计","无广告。无需登录。完全离线。每天一幅，随你的节奏。")],
 ctitle="今天的画<br>已经挂在墙上。", csub="免费畅玩 · 122 幅名画 · iPhone 和 iPad",
 fcontact="联系", fprivacy="隐私", fterms="条款")

L['zh-Hant']=dict(htmllang='zh-Hant',brand='Palette 2048',
 title="Palette 2048 — 每天用名畫的顏色玩的拼圖",
 desc="每天，棋盤都被一幅真實名畫的調色盤點亮。不用數字，用顏色合併拼出畫作。週六是只憑顏色猜畫的謎題日。",
 ogt="Palette 2048 — 用名畫的顏色遊玩", ogd="每天一幅新名畫。合併顏色拼出畫作，週六只憑顏色猜出作品。",
 kicker="口袋裡的美術館", hmsg="每天一幅<br>全新名畫。",
 hsub="每天棋盤都被一幅真實名畫的調色盤點亮。<br>沒有數字，用<strong>顏色</strong>合併拼出完整的畫作。",
 cta="在 App Store 下載", rating="每天 · 免費暢玩", hfoot="122 幅名畫 · iPhone 和 iPad · 無廣告 · 離線",
 wlabel="有何不同", wtitle="沒有數字。<br>你的眼睛就是遊戲。",
 c1tag="普通的 2048", c1note="只追數字。每天都是同樣的灰色方塊。",
 c2tag="Palette 2048", c2note="追逐一幅畫。每天都有新的色彩。",
 punch="把兩個相同的顏色合併，它便綻放成下一種。",
 mlabel="每週六", mtitle="謎題日。",
 msub="週六隱藏作品名稱。先玩顏色，再僅憑調色盤認出名畫。你對藝術的眼力有多準？",
 flabel="內容", ftitle="用真實藝術打造的，寧靜的每日儀式。",
 f=[("每天一幅名畫","精選名畫 122 幅 — 梵谷、莫內、北齋、金弘道等。明天又是另一幅。"),
    ("顏色，而非數字","方塊是純粹的顏色。合併後融入調色盤的下一種色。一場安靜的色覺測試。"),
    ("週六謎題","僅憑顏色認出隱藏的作品，為愛藝術的你準備的每週活動。"),
    ("典藏","錯過了某天？在色彩日曆裡重玩你玩過的所有畫作。"),
    ("連勝 &amp; 統計","保持每日連勝，記錄每幅畫的最佳成績，壯大你的收藏。"),
    ("極簡設計","無廣告。無須登入。完全離線。每天一幅，隨你的節奏。")],
 ctitle="今天的畫<br>已經掛在牆上。", csub="免費暢玩 · 122 幅名畫 · iPhone 和 iPad",
 fcontact="聯絡", fprivacy="隱私", fterms="條款")

def hreflang():
    out=[f'<link rel="alternate" hreflang="{c}" href="{f}">' for c,f,_ in LANGS]
    out.append('<link rel="alternate" hreflang="x-default" href="index.html">')
    return "\n".join(out)

def langselect(cur):
    opts=[]
    short={'en':'EN','ko':'한국어','ja':'日本語','zh-Hans':'简体中文','zh-Hant':'繁體中文'}
    for c,f,_ in LANGS:
        sel=' selected' if c==cur else ''
        opts.append(f'        <option value="{f}"{sel}>{short[c]}</option>')
    return "\n".join(opts)

def footlangs(cur):
    return "\n".join(f'      <a href="{f}">{name}</a>' for c,f,name in LANGS if c!=cur)

def feat(d):
    s=['s1','s2','s3','s4','s5','s6']
    out=[]
    for i,(h,p) in enumerate(d['f']):
        out.append(f'''      <div class="feature">
        <div class="f-swatch {s[i]}"></div>
        <h3>{h}</h3>
        <p>{p}</p>
      </div>''')
    return "\n".join(out)

TMPL='''<!DOCTYPE html>
<html lang="{htmllang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{hreflang}
<meta property="og:title" content="{ogt}">
<meta property="og:description" content="{ogd}">
<link rel="icon" type="image/png" href="icon.png">
<link rel="apple-touch-icon" href="icon-180.png">
<meta property="og:image" content="icon.png">
<meta property="og:type" content="website">
<link rel="stylesheet" href="style.css">
</head>
<body>

<header>
  <div class="bar">
    <a class="wordmark" href="{selfurl}"><img class="brand-icon" src="icon.png" alt="" width="26" height="26">{brand}</a>
    <nav class="nav-right">
      <select class="lang-select" onchange="location.href=this.value" aria-label="Language">
{langselect}
      </select>
      <a class="nav-cta" href="{app}" target="_blank" rel="noopener">App Store</a>
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
      <a class="appstore-btn" href="{app}" target="_blank" rel="noopener">{svg}{cta}</a>
      <span class="rating"><span class="stars">★★★★★</span>{rating}</span>
    </div>
    <p class="hero-foot">{hfoot}</p>
  </div>
  <div class="board-col">
    <div class="frame">
      <div class="board" id="board" aria-hidden="true">
        <span></span><span></span><span></span>
        <span></span><span></span><span></span>
        <span></span><span></span><span></span>
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
      <div class="choices">
        <span>The Starry Night</span>
        <span class="pick">The Great Wave</span>
        <span>Water Lilies</span>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <p class="sec-label">{flabel}</p>
    <h2 class="sec-title">{ftitle}</h2>
    <div class="features">
{features}
    </div>
  </div>
</section>

<section class="cta">
  <div class="wrap">
    <h2 class="cta-title">{ctitle}</h2>
    <p class="cta-sub">{csub}</p>
    <a class="appstore-btn" href="{app}" target="_blank" rel="noopener">{svg}{cta}</a>
  </div>
</section>
</main>

<footer>
  <div class="wrap cols">
    <a class="home-link" href="https://www.kkirukstudio.com/">© kkiruk studio</a>
    <nav class="links">
      <a href="mailto:kkirukstudio.help@gmail.com">{fcontact}</a>
      <a href="https://kkiruk-studio.github.io/privacy-policy-app/" target="_blank" rel="noopener">{fprivacy}</a>
      <a href="https://kkiruk-studio.github.io/terms-of-service-app/" target="_blank" rel="noopener">{fterms}</a>
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
    html=TMPL.format(svg=SVG, app=APP, selfurl=fname,
        hreflang=hreflang(), langselect=langselect(code), footlangs=footlangs(code),
        features=feat(d), **d)
    open(fname,'w').write(html)
    print("wrote", fname, len(html), "bytes")
