#!/usr/bin/env python3
"""Generate index.html for every locale from one template (everykeep).

Usage: python3 build.py
Output: ./index.html (en), ./ko/index.html, ./ja/index.html
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).parent
BASE_URL = "https://www.kkirukstudio.com/everykeep/"
OG_IMAGE = "https://www.kkirukstudio.com/everykeep/og.png"  # TODO: custom everykeep OG 1200x630
APP_STORE_URL = "https://apps.apple.com/app/id6781988992"  # live 2026-06-24

APPLE_SVG = '<svg viewBox="0 0 384 512" aria-hidden="true"><path d="M318.7 268.7c-.2-36.7 16.4-64.4 50-84.8-18.8-26.9-47.2-41.7-84.7-44.6-35.5-2.8-74.3 20.7-88.5 20.7-15 0-49.4-19.7-76.4-19.7C63.3 141.2 4 184.8 4 273.5q0 39.3 14.4 81.2c12.8 36.7 59 126.7 107.2 125.2 25.2-.6 43-17.9 75.8-17.9 31.8 0 48.3 17.9 76.4 17.9 48.6-.7 90.4-82.5 102.6-119.3-65.2-30.7-61.7-90-61.7-91.9zm-56.6-164.2c27.3-32.4 24.8-61.9 24-72.5-24.1 1.4-52 16.4-67.9 34.9-17.5 19.8-27.8 44.3-25.6 71.9 26.1 2 49.9-11.4 69.5-34.3z"/></svg>'

LANG_LABELS = [("", "EN"), ("ko/", "한국어"), ("ja/", "日本語")]

LOCALES = {
    "en": {
        "dir": "", "lang": "en", "font": None, "shots": "en-US",
        "title": "everykeep — Home maintenance reminders",
        "desc": "Filters, warranties, registrations, cleaning cycles — everykeep remembers the easy-to-forget upkeep of everything you own, and reminds you before it's due. Free, on-device.",
        "og_title": "everykeep — Remembers when you can't",
        "og_desc": "The easy-to-forget upkeep of everything you own, in one place. Free.",
        "kicker_num": "HOME MAINTENANCE",
        "h1": "Filters, warranties, the small upkeep —<br>everykeep <em>remembers</em> when you can't.",
        "pairs": [["Water filter", "Replace · 5 days"], ["Aircon filter", "Clean · 12 days"], ["Laptop warranty", "Ends · 340 days"], ["Purifier filter", "Replace · today"]],
        "sub": "Filters, warranties, registrations, cleaning cycles — the easy-to-forget upkeep of everything you own, in one place. everykeep remembers when it's due and quietly reminds you. Free, and nothing leaves your phone.",
        "note": "FREE · IPHONE &amp; IPAD",
        "badge_small": "Download on the", "badge_aria": "everykeep on the App Store",
        "chips": [["↻", "Replace"], ["✦", "Clean"], ["🛡", "Warranty"], ["✓", "Register"]],
        "hero_alt": "everykeep home screen showing upcoming upkeep and the Keepy character",
        "marquee": ["WATER FILTER", "AIRCON", "AIR PURIFIER", "TOOTHBRUSH HEAD", "CONTACT LENS", "WARRANTY", "REGISTRATION", "CLEANING"],
        "how_kicker": "HOW IT WORKS",
        "how_h2": "From <em>“when did I last…?”</em> to handled.",
        "steps": [
            ["REGISTER", "Add a thing", "Register an item and how often it needs care — a filter every 3 months, a warranty that ends next year."],
            ["REMIND", "everykeep remembers", "It tracks the date and nudges you before it's due — 30, 7, 1 days ahead, your choice."],
            ["DONE", "One tap, done", "Mark it done and the next date is set automatically. Keepy grows a little."],
        ],
        "keepy_kicker": "KEEPY", "keepy_num": "GROWS WITH YOU",
        "keepy_h2": "A keeper that <em>grows</em> as you keep up.",
        "keepy_lede": "Every time you register a thing or finish a task, Keepy earns a little care and levels up — from a seed to full bloom. No nagging, just the quiet proof you've got it handled.",
        "keepy": [["Seed", "Just planted", "START"], ["Sprout", "Starting to grow", "30 PT"], ["Leaf", "Coming along", "70 PT"], ["Bloom", "Fully grown", "150 PT"]],
        "status_kicker": "STATUS", "status_num": "AT A GLANCE",
        "status_h2": "You'll <em>see</em> it coming.",
        "status_lede": "Every item carries a simple traffic-light. Plenty of time, due soon, or overdue — no digging, no spreadsheet.",
        "status": [["Plenty of time", "Logged and on track."], ["Due soon", "Within your reminder window."], ["Overdue", "Time to take care of it."]],
        "shots_kicker": "SCREENS", "shots_num": "iOS",
        "shots_h2": "Built to be <em>glanced at</em>, not managed.",
        "shots_caps": ["TODAY'S UPKEEP", "KEEPY GROWS", "CALENDAR TIMELINE"],
        "feat_kicker": "DETAILS", "feat_num": "06",
        "feat_h2": "Free app. <em>Careful</em> choices.",
        "feats": [
            ["On-device, nothing collected", "Everything stays on your iPhone. No account, no analytics leaving the device."],
            ["Notifications that fit", "Choose 30 / 7 / 1 / day-of reminders per item. Only the nudges you want."],
            ["Keepy grows with you", "A hand-drawn keeper that levels up every time you log or finish a task."],
            ["Calendar timeline", "See what's due this week or month, laid out on a clean timeline."],
            ["Lifespan at a glance", "The inventory shows each item's remaining life as a ring — green, amber, done."],
            ["Photos &amp; warranties", "Attach a photo, store warranty and registration dates, find the receipt later."],
        ],
        "final_h2": "Stop trying to remember.", "final_lede": "Free on iPhone and iPad.",
        "f_contact": "Contact", "f_privacy": "Privacy", "f_terms": "Terms",
    },
    "ko": {
        "dir": "ko/", "lang": "ko", "font": '"Apple SD Gothic Neo", "Pretendard"', "shots": "ko",
        "title": "everykeep — 소모품 교체·관리 알림",
        "desc": "필터 교체, 보증 만료, 정품 등록, 청소 주기 — 잊기 쉬운 물건 관리를 everykeep이 대신 기억하고 갈 때가 되면 알려줘요. 무료, 온디바이스.",
        "og_title": "everykeep — 대신 기억해 주는 물건 관리",
        "og_desc": "잊기 쉬운 우리 집 물건 관리를 한곳에. 무료.",
        "kicker_num": "물건 관리",
        "h1": "필터·보증·잊기 쉬운 관리,<br>everykeep이 <em>대신 기억</em>해요.",
        "pairs": [["정수기 필터", "교체 · 5일"], ["에어컨 필터", "청소 · 12일"], ["노트북 보증", "만료 · 340일"], ["공기청정기 필터", "교체 · 오늘"]],
        "sub": "필터 교체, 보증 만료, 정품 등록, 청소 주기 — 잊어버리기 쉬운 우리 집 물건 관리를 한곳에. 갈 때가 되면 everykeep이 대신 기억하고 조용히 알려줘요. 무료, 그리고 기록은 기기 밖으로 안 나가요.",
        "note": "무료 · iPhone &amp; iPad",
        "badge_small": "다운로드는", "badge_aria": "App Store의 everykeep",
        "chips": [["↻", "교체"], ["✦", "청소"], ["🛡", "보증"], ["✓", "정품"]],
        "hero_alt": "everykeep 홈 화면 — 다가오는 관리 일정과 키프이 캐릭터",
        "marquee": ["정수기 필터", "에어컨", "공기청정기", "칫솔모", "콘택트렌즈", "보증서", "정품등록", "청소 주기"],
        "how_kicker": "사용 방법",
        "how_h2": "<em>“마지막에 언제 했더라?”</em>에서 해결까지.",
        "steps": [
            ["등록", "물건을 추가", "물건과 주기를 등록해요 — 3개월마다 필터, 내년에 끝나는 보증처럼."],
            ["알림", "키프이가 기억", "날짜를 추적하다가 때가 오기 전에 알려줘요 — 30·7·1일 전, 원하는 대로."],
            ["완료", "한 탭이면 끝", "완료를 누르면 다음 날짜가 자동으로. 키프이도 한 뼘 자라요."],
        ],
        "keepy_kicker": "키프이", "keepy_num": "함께 자라요",
        "keepy_h2": "기록할수록 <em>자라는</em> 정리 동반자.",
        "keepy_lede": "물건을 등록하거나 할 일을 끝낼 때마다 키프이가 돌봄을 얻어 한 단계씩 자라요 — 씨앗에서 활짝까지. 잔소리 없이, 잘 챙긴 마음만 차곡차곡.",
        "keepy": [["씨앗", "갓 심은", "시작"], ["새싹", "자라기 시작", "30 P"], ["잎새", "한창 크는 중", "70 P"], ["활짝", "활짝 핀", "150 P"]],
        "status_kicker": "상태", "status_num": "한눈에",
        "status_h2": "<em>미리</em> 보여요.",
        "status_lede": "모든 물건에 신호등 하나. 여유 있음·곧 임박·지남 — 뒤질 것도, 엑셀도 없이.",
        "status": [["여유 있음", "기록돼 있고 순조로워요."], ["곧 임박", "알림 범위 안에 들어왔어요."], ["지남", "이제 챙길 때예요."]],
        "shots_kicker": "화면", "shots_num": "iOS",
        "shots_h2": "관리하는 게 아니라, <em>흘끗 보는</em> 앱.",
        "shots_caps": ["오늘 챙길 일", "자라는 키프이", "캘린더 타임라인"],
        "feat_kicker": "디테일", "feat_num": "06",
        "feat_h2": "무료 앱, <em>꼼꼼한</em> 선택.",
        "feats": [
            ["데이터 미수집", "모든 기록이 내 아이폰 안에만. 계정도, 기기 밖으로 나가는 분석도 없어요."],
            ["딱 맞는 알림", "물건마다 30·7·1일·당일 알림을 골라서. 원하는 만큼만 챙겨요."],
            ["자라는 키프이", "기록하고 완료할수록 한 단계씩 자라는 손그림 정리 동반자."],
            ["캘린더 타임라인", "이번 주·이번 달 챙길 일을 깔끔한 타임라인으로."],
            ["한눈에 수명", "보관함에서 물건별 남은 수명을 링으로. 초록·앰버·완료."],
            ["사진 · 보증", "사진 첨부, 보증·정품 등록일 저장, 영수증도 나중에 바로."],
        ],
        "final_h2": "이제 기억하려 애쓰지 마세요.", "final_lede": "iPhone · iPad 무료.",
        "f_contact": "문의", "f_privacy": "개인정보 처리방침", "f_terms": "이용약관",
    },
    "ja": {
        "dir": "ja/", "lang": "ja", "font": '"Hiragino Kaku Gothic ProN", "Hiragino Sans", "Yu Gothic"', "shots": "ja",
        "title": "everykeep — モノのお手入れ通知",
        "desc": "フィルター交換、保証、正規登録、清掃の周期 — 忘れがちなモノの管理をeverykeepが覚えて、その時が来たら知らせます。無料・オンデバイス。",
        "og_title": "everykeep — 代わりに覚えておくモノ管理",
        "og_desc": "忘れがちなモノのお手入れをひとつに。無料。",
        "kicker_num": "モノの管理",
        "h1": "フィルター・保証・忘れがちなお手入れ、<br>everykeepが<em>覚えて</em>おきます。",
        "pairs": [["浄水フィルター", "交換 · 5日"], ["エアコンフィルター", "清掃 · 12日"], ["ノートPC保証", "満了 · 340日"], ["空気清浄機フィルター", "交換 · 今日"]],
        "sub": "フィルター交換、保証の満了、正規登録、清掃の周期 — 忘れがちなモノのお手入れをひとつに。その時が来たらeverykeepが覚えていて、そっと知らせます。無料、記録は端末の外に出ません。",
        "note": "無料 · iPhone &amp; iPad",
        "badge_small": "ダウンロードは", "badge_aria": "App Store の everykeep",
        "chips": [["↻", "交換"], ["✦", "清掃"], ["🛡", "保証"], ["✓", "登録"]],
        "hero_alt": "everykeepのホーム画面 — これからのお手入れとキープイ",
        "marquee": ["浄水フィルター", "エアコン", "空気清浄機", "歯ブラシ", "コンタクト", "保証書", "正規登録", "清掃周期"],
        "how_kicker": "使い方",
        "how_h2": "<em>「前にやったのいつ？」</em>から解決まで。",
        "steps": [
            ["登録", "モノを追加", "モノと周期を登録 — 3か月ごとのフィルター、来年切れる保証のように。"],
            ["通知", "キープイが記憶", "日付を追って、その時が来る前に知らせます — 30・7・1日前、お好みで。"],
            ["完了", "ワンタップで完了", "完了を押すと次の日付が自動で。キープイも少し育ちます。"],
        ],
        "keepy_kicker": "キープイ", "keepy_num": "一緒に育つ",
        "keepy_h2": "記録するほど<em>育つ</em>整理パートナー。",
        "keepy_lede": "モノを登録したり、やることを終えるたびにキープイがケアを得て育ちます — タネから満開まで。小言はなし、ちゃんとできた証だけが積もります。",
        "keepy": [["タネ", "植えたばかり", "スタート"], ["芽", "育ち始め", "30 P"], ["葉", "成長中", "70 P"], ["満開", "満開", "150 P"]],
        "status_kicker": "ステータス", "status_num": "ひと目で",
        "status_h2": "<em>前もって</em>見えます。",
        "status_lede": "すべてのモノに信号がひとつ。余裕あり・もうすぐ・期限切れ — 探す手間も、表計算もなし。",
        "status": [["余裕あり", "記録済みで順調。"], ["もうすぐ", "通知の範囲に入りました。"], ["期限切れ", "そろそろお手入れを。"]],
        "shots_kicker": "画面", "shots_num": "iOS",
        "shots_h2": "管理ではなく、<em>ちらっと見る</em>アプリ。",
        "shots_caps": ["今日のお手入れ", "育つキープイ", "カレンダー"],
        "feat_kicker": "こだわり", "feat_num": "06",
        "feat_h2": "無料アプリ、<em>ていねいな</em>選択。",
        "feats": [
            ["データ非収集", "すべての記録はあなたのiPhoneの中だけ。アカウントも、端末の外に出る分析もありません。"],
            ["ちょうどいい通知", "モノごとに30・7・1日・当日の通知を選べます。必要な分だけ。"],
            ["育つキープイ", "記録して完了するたびに一段ずつ育つ、手描きの整理パートナー。"],
            ["カレンダー", "今週・今月のやることを、すっきりしたタイムラインで。"],
            ["寿命がひと目で", "収納庫でモノごとの残り寿命をリングで。緑・アンバー・完了。"],
            ["写真 · 保証", "写真を添付、保証・正規登録日を保存、レシートも後ですぐ。"],
        ],
        "final_h2": "もう覚えようとしなくて大丈夫。", "final_lede": "iPhone · iPad 無料。",
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
    href = APP_STORE_URL or "#"
    return (f'<a class="store-badge" id="{el_id}" href="{href}" aria-label="{loc["badge_aria"]}">{APPLE_SVG}'
            f'<span class="txt"><small>{loc["badge_small"]}</small><strong>App Store</strong></span></a>')


REDIRECT_SCRIPT = """<script>
/* Auto-detect browser language on first visit (root/en only). Respects a prior manual choice. */
(function(){
  try{
    if(localStorage.getItem('ek_lang')) return;            // already chose/auto-routed before
    var n=((navigator.languages&&navigator.languages[0])||navigator.language||'').toLowerCase();
    var d=n.indexOf('ko')===0?'ko/':n.indexOf('ja')===0?'ja/':null;
    if(d){ localStorage.setItem('ek_lang', d==='ko/'?'ko':'ja'); location.replace(d); }
    else { localStorage.setItem('ek_lang','en'); }
  }catch(e){}
})();
</script>
"""

LANG_PERSIST_SCRIPT = """<script>
/* Remember the visitor's manual language choice so the root won't auto-redirect again. */
(function(){
  document.querySelectorAll('.lang a').forEach(function(a){
    a.addEventListener('click', function(){
      var h=a.getAttribute('href')||'';
      var c=h.indexOf('ko')>-1?'ko':h.indexOf('ja')>-1?'ja':'en';
      try{ localStorage.setItem('ek_lang', c); }catch(e){}
    });
  });
})();
</script>
"""


def render(key):
    loc = LOCALES[key]
    rel = "../" if loc["dir"] else ""
    redirect_script = REDIRECT_SCRIPT if loc["dir"] == "" else ""
    font_override = f'<style>body{{font-family:-apple-system,BlinkMacSystemFont,{loc["font"]},"Segoe UI",sans-serif}}</style>' if loc["font"] else ""
    chips = "".join(
        f'<div class="chip c{i+1}"><span class="g">{g}</span>{label}</div>'
        for i, (g, label) in enumerate(loc["chips"])
    )
    marquee = "".join(f"<span>{m}</span>" for m in loc["marquee"] * 2)
    steps = "".join(
        f'<div class="step"><span class="n">0{i+1}</span><span class="tag">{tag}</span><h3>{h}</h3><p>{p}</p></div>'
        for i, (tag, h, p) in enumerate(loc["steps"])
    )
    keepy_imgs = ["seed", "sprout", "leaf", "bloom"]
    keepy = "".join(
        f'<div class="keepy"><img src="{rel}assets/keepy-{img}.png" alt="{name}" loading="lazy"><h3>{name}</h3><p>{cap}</p><span class="pt">{pt}</span></div>'
        for img, (name, cap, pt) in zip(keepy_imgs, loc["keepy"])
    )
    status_cls = ["green", "amber", "red"]
    status = "".join(
        f'<div class="status {c}"><span class="dot"></span><h3>{h}</h3><p>{p}</p></div>'
        for c, (h, p) in zip(status_cls, loc["status"])
    )
    shot_files = ["home", "keepy", "calendar"]
    shots = "".join(
        f'<figure><img class="shot-flat" src="{rel}assets/shot-{loc["shots"]}-{f}.png" alt="{cap}" loading="lazy"></figure>'
        for f, cap in zip(shot_files, loc["shots_caps"])
    )
    feats = "".join(f'<div class="feat"><h3>{h}</h3><p>{p}</p></div>' for h, p in loc["feats"])
    pairs_json = json.dumps(loc["pairs"], ensure_ascii=False)
    canonical = f"{BASE_URL}{loc['dir']}"

    html = f"""<!doctype html>
<html lang="{loc['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{redirect_script}<title>{loc['title']}</title>
<meta name="description" content="{loc['desc']}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{loc['og_title']}">
<meta property="og:description" content="{loc['og_desc']}">
<meta property="og:image" content="{OG_IMAGE}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="kkiruk studio">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{OG_IMAGE}">
{hreflang_block()}
<link rel="icon" type="image/png" href="{rel}assets/icon-180.png">
<link rel="apple-touch-icon" href="{rel}assets/icon-180.png">
<link rel="stylesheet" href="{rel}assets/style.css">
{font_override}
<script src="/ga.js"></script>
</head>
<body>

<nav>
  <div class="wrap">
    <a class="wordmark" href="{rel if rel else './'}"><img src="{rel}assets/icon-180.png" alt=""><span>everykeep</span></a>
    <div class="lang">{lang_nav(loc['dir'], rel)}</div>
  </div>
</nav>

<header class="hero">
  <div class="ghost">e·k</div>
  <div class="wrap">
    <div>
      <div class="kicker"><span>everykeep</span><span class="rule"></span><span class="num">{loc['kicker_num']}</span></div>
      <h1>{loc['h1']}</h1>
      <div class="demo">
        <span class="src" id="demoSrc">{loc['pairs'][0][0]}</span>
        <span class="arrow">→</span>
        <span class="dst" id="demoDst">{loc['pairs'][0][1]}</span>
      </div>
      <p class="sub">{loc['sub']}</p>
      <div class="cta">
        {badge(loc, 'storeLink')}
        <span class="note">{loc['note']}</span>
      </div>
    </div>
    <div class="phone-col">
      {chips}
      <img class="shot-flat hero-shot" src="{rel}assets/shot-{loc['shots']}-home.png" alt="{loc['hero_alt']}">
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
    <div class="kicker"><span>{loc['keepy_kicker']}</span><span class="rule"></span><span class="num">{loc['keepy_num']}</span></div>
    <h2>{loc['keepy_h2']}</h2>
    <p class="lede">{loc['keepy_lede']}</p>
    <div class="keepy-row">{keepy}</div>
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap">
    <div class="kicker"><span>{loc['status_kicker']}</span><span class="rule"></span><span class="num">{loc['status_num']}</span></div>
    <h2>{loc['status_h2']}</h2>
    <p class="lede">{loc['status_lede']}</p>
    <div class="status-grid">{status}</div>
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
  </div>
</footer>

<script>
  // After App Store approval, set the real URL here (e.g. https://apps.apple.com/app/id1234567890)
  const APP_STORE_URL = "https://apps.apple.com/app/id6781988992";
  if (APP_STORE_URL) {{
    document.getElementById("storeLink").href = APP_STORE_URL;
    document.getElementById("storeLink2").href = APP_STORE_URL;
  }}

  const pairs = {pairs_json};
  const srcEl = document.getElementById("demoSrc");
  const dstEl = document.getElementById("demoDst");
  if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {{
    let i = 0;
    const sleep = (ms) => new Promise(r => setTimeout(r, ms));
    (async function loop() {{
      for (;;) {{
        const [src, dst] = pairs[i % pairs.length];
        dstEl.textContent = "";
        srcEl.textContent = "";
        for (const ch of src) {{ srcEl.textContent += ch; await sleep(70); }}
        await sleep(350);
        dstEl.textContent = dst;
        await sleep(2200);
        i++;
      }}
    }})();
  }}
</script>
{LANG_PERSIST_SCRIPT}</body>
</html>
"""
    out = ROOT / loc["dir"] / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)} ({len(html)} bytes)")


for key in LOCALES:
    render(key)
