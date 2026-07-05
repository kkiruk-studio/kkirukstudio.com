#!/usr/bin/env python3
"""Generate index.html for every locale from one template.

Usage: python3 build.py
Output: ./index.html (en), ./ko/index.html, ./ja/index.html
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).parent
BASE_URL = "https://www.kkirukstudio.com/deskbreath/"

# Fill in after App Store approval (e.g. https://apps.apple.com/app/id1234567890),
# then re-run `python3 build.py`. Empty renders a disabled "Coming soon" badge.
APP_STORE_URL = ""

APPLE_SVG = '<svg viewBox="0 0 384 512" aria-hidden="true"><path d="M318.7 268.7c-.2-36.7 16.4-64.4 50-84.8-18.8-26.9-47.2-41.7-84.7-44.6-35.5-2.8-74.3 20.7-88.5 20.7-15 0-49.4-19.7-76.4-19.7C63.3 141.2 4 184.8 4 273.5q0 39.3 14.4 81.2c12.8 36.7 59 126.7 107.2 125.2 25.2-.6 43-17.9 75.8-17.9 31.8 0 48.3 17.9 76.4 17.9 48.6-.7 90.4-82.5 102.6-119.3-65.2-30.7-61.7-90-61.7-91.9zm-56.6-164.2c27.3-32.4 24.8-61.9 24-72.5-24.1 1.4-52 16.4-67.9 34.9-17.5 19.8-27.8 44.3-25.6 71.9 26.1 2 49.9-11.4 69.5-34.3z"/></svg>'

LANG_LABELS = [("", "EN"), ("ko/", "한국어"), ("ja/", "日本語")]

LOCALES = {
    "en": {
        "dir": "", "lang": "en", "font": None, "shots": "en",
        "title": "DeskBreath — A breathing rhythm that keeps going, even with the app closed",
        "desc": "DeskBreath keeps a quiet breathing circle alive in your iPhone's Dynamic Island or your Mac's menu bar — 4 seconds in, 6 seconds out — with stretch reminders to break up desk fatigue.",
        "og_title": "DeskBreath — Breathing Timer for Desk Work",
        "og_desc": "A breathing rhythm that survives closing the app. Built for WFH deep work.",
        "kicker_num": "BREATHING TIMER",
        "h1": "Close the app.<br>The <em>rhythm</em> keeps breathing.",
        "sub": "Between back-to-back calls and heads-down deep work, breathing is the first thing you forget. DeskBreath keeps a quiet breathing circle alive in your Dynamic Island or menu bar — 4 seconds in, 6 seconds out — so you can catch the rhythm out of the corner of your eye, without opening the app.",
        "badge_small": "Download on the", "note": "FREE PRESETS · IPHONE &amp; MAC · NO SUBSCRIPTION",
        "badge_aria": "Download on the App Store", "coming_soon": "Coming soon",
        "orb_in": "Breathe in", "orb_out": "Breathe out",
        "marquee": ["BREATHE", "FOCUS", "STRETCH", "POSTURE", "RHYTHM", "DEEP WORK", "DESK FATIGUE", "CALM"],
        "how_kicker": "HOW IT WORKS",
        "how_h2": "Three moments where the <em>rhythm</em> finds you.",
        "steps": [
            ["START", "Pick a rhythm and go", "Box breathing, 4-7-8, or your own inhale/exhale seconds — start free, no account, right from the menu bar or the app."],
            ["GLANCE", "Catch it mid deep-work", "The circle keeps breathing in your Dynamic Island or menu bar. A glance mid-scroll is enough to slow your breath back down."],
            ["STAND UP", "Rise on the stretch cue", "Every 30, 60, 90 or 120 minutes, a gentle nudge tells you to stand, roll your shoulders, and reset your posture."],
        ],
        "value_kicker": "STILL RUNNING", "value_num": "APP CLOSED",
        "value_h2": "Close the app.<br>The <em>rhythm</em> doesn't close with it.",
        "value_lede": "Desk fatigue doesn't wait for you to reopen an app. DeskBreath keeps the circle breathing wherever you actually are — locked screen or menu bar.",
        "iphone_tag": "IPHONE", "iphone_h3": "Dynamic Island &amp; Lock Screen",
        "iphone_p": "A Live Activity keeps the breathing circle and a countdown running in your Dynamic Island — visible without unlocking, even mid video call.",
        "mac_tag": "MAC", "mac_h3": "Menu Bar &amp; Floating Circle",
        "mac_p": "A tiny breathing circle lives in your menu bar, and an optional always-on-top floating circle sits quietly over whatever you're working on.",
        "shots_kicker": "SCREENS", "shots_num": "IOS 17+ · MACOS 14+",
        "shots_h2": "Built for the middle of a workday, <em>not a demo</em>.",
        "shots_caps": ["ACTIVE BREATHING SESSION", "RHYTHM &amp; PRESET SETTINGS", "WEEKLY STATS &amp; STREAK"],
        "feat_kicker": "DETAILS", "feat_num": "06",
        "feat_h2": "Quiet, but <em>thorough</em>.",
        "feats": [
            ["Box breathing &amp; presets", "4-4-4-4 box breathing, 4-7-8, and more — free, built in, ready in one tap.", False],
            ["Custom rhythm &amp; haptics", "Set your own inhale/exhale seconds and feel each phase change as a haptic pulse — free.", False],
            ["Color, image &amp; direction", "Recolor the circle, drop in your own image, and flip the countdown direction to match how you focus.", True],
            ["Weekly stats &amp; streaks", "See how many sessions you actually finished this week, and keep the streak alive.", True],
            ["Stretch reminders", "Nudges every 30, 60, 90 or 120 minutes to stand, stretch, and reset your posture.", False],
            ["Pay once. No subscription.", "Pro is a single lifetime purchase — one payment, no recurring fees, ever.", False],
        ],
        "final_h2": "Give your breath a rhythm.", "final_lede": "Free presets on iPhone and Mac. Pro unlocks once, forever.",
        "f_contact": "Contact", "f_privacy": "Privacy", "f_terms": "Terms",
        "mac_hi_kicker": "STAYS AT YOUR DESK",
        "mac_hi_h2": "On Mac, DeskBreath isn't an app you open. <em>It's an app that stays.</em>",
        "mac_hi_lede": "Pin the orb to your menu bar, or let it float above whatever you're working on — DeskBreath stays on screen for the whole shift, not just the moment you open it.",
        "mac_hi_caps": ["MENU BAR ORB", "FLOATING ORB", "WEEKLY STATS"],
    },
    "ko": {
        "dir": "ko/", "lang": "ko", "font": '"Apple SD Gothic Neo", "Pretendard"', "shots": "ko",
        "title": "데스크브레스 — 앱을 닫아도 계속되는 호흡 리듬",
        "desc": "데스크브레스는 다이나믹 아일랜드와 메뉴바에 조용한 호흡 원을 띄워 둡니다. 들숨 4초, 날숨 6초 리듬을 재택근무 중에도, 야근 중에도 곁눈질로 확인하고, 스트레칭 알림으로 거북목을 풀어보세요.",
        "og_title": "데스크브레스 — 업무용 호흡 타이머",
        "og_desc": "앱을 닫아도 계속되는 호흡 리듬. 재택근무와 야근을 위한 타이머.",
        "kicker_num": "호흡 타이머",
        "h1": "앱을 닫아도,<br><em>호흡 리듬</em>은 계속됩니다.",
        "sub": "화상회의와 집중 작업 사이, 호흡은 자꾸 잊혀집니다. 데스크브레스는 앱을 닫아도 다이나믹 아일랜드와 메뉴바에 조용한 호흡 원을 띄워 둡니다 — 들숨 4초, 날숨 6초. 거북목이 굳어지기 전에, 야근이 길어지기 전에 곁눈질로 리듬을 확인하세요.",
        "badge_small": "다운로드는", "note": "무료 프리셋 · IPHONE &amp; MAC · 구독 없음",
        "badge_aria": "App Store에서 다운로드", "coming_soon": "출시 예정",
        "orb_in": "들숨", "orb_out": "날숨",
        "marquee": ["호흡", "집중", "스트레칭", "거북목", "리듬", "재택근무", "야근", "회복"],
        "how_kicker": "사용 방법",
        "how_h2": "<em>호흡 원</em>이 당신을 찾아오는 세 순간.",
        "steps": [
            ["시작", "리듬을 고르고 시작", "박스호흡, 4-7-8, 혹은 나만의 들숨·날숨 초 — 계정 없이 메뉴바나 앱에서 바로 무료로 시작합니다."],
            ["곁눈질", "일하며 리듬 확인", "다이나믹 아일랜드나 메뉴바에서 호흡 원이 계속 움직입니다. 화면을 스크롤하다 한 번 곁눈질하는 것만으로 호흡이 다시 느려집니다."],
            ["일어나기", "스트레칭 알림에 일어나기", "30·60·90·120분마다 부드러운 알림이 자리에서 일어나 어깨를 풀고 자세를 바로잡으라고 알려줍니다."],
        ],
        "value_kicker": "계속 실행 중", "value_num": "앱을 닫아도",
        "value_h2": "앱을 닫아도,<br><em>리듬</em>은 꺼지지 않습니다.",
        "value_lede": "거북목과 뻐근함은 앱을 다시 열 때까지 기다려주지 않습니다. 데스크브레스는 잠금화면에서도, 메뉴바에서도 호흡 원을 켜 둡니다.",
        "iphone_tag": "IPHONE", "iphone_h3": "다이나믹 아일랜드 &amp; 잠금화면",
        "iphone_p": "라이브 액티비티가 다이나믹 아일랜드에 호흡 원과 카운트다운을 띄워 둡니다. 화상회의 중에도, 잠금을 풀지 않아도 보입니다.",
        "mac_tag": "MAC", "mac_h3": "메뉴바 &amp; 플로팅 호흡 원",
        "mac_p": "작은 호흡 원이 메뉴바에 상주하고, 원하면 항상 위에 뜨는 플로팅 호흡 원이 작업 화면 위에 조용히 자리합니다.",
        "shots_kicker": "화면", "shots_num": "IOS 17+ · MACOS 14+",
        "shots_h2": "업무 중간에 쓰는 도구, <em>데모가 아니라</em>.",
        "shots_caps": ["호흡 세션 진행 중", "리듬 · 프리셋 설정", "주간 통계 · 스트릭"],
        "feat_kicker": "디테일", "feat_num": "06",
        "feat_h2": "조용하지만, <em>빈틈은 없이</em>.",
        "feats": [
            ["박스호흡 · 프리셋", "4-4-4-4 박스호흡, 4-7-8 등 — 무료로 내장, 한 탭이면 바로 시작합니다.", False],
            ["리듬 커스텀 · 햅틱", "들숨·날숨 초를 직접 정하고, 단계가 바뀔 때마다 햅틱으로 느껴보세요 — 무료.", False],
            ["색 · 이미지 꾸미기", "호흡 원 색을 바꾸고 원하는 이미지를 넣고, 카운트 방향까지 내게 맞게 뒤집습니다.", True],
            ["주간 통계 · 스트릭", "이번 주 실제로 끝낸 세션이 몇 번인지 확인하고 스트릭을 이어가세요.", True],
            ["스트레칭 알림", "30·60·90·120분마다 일어나서 스트레칭하고 자세를 바로잡으라는 알림.", False],
            ["평생 한 번 결제, 구독 없음", "Pro는 평생 한 번 결제입니다. 매달 빠져나가는 구독료는 없습니다.", False],
        ],
        "final_h2": "호흡에 리듬을 붙이세요.", "final_lede": "iPhone과 Mac에서 무료 프리셋으로. Pro는 평생 한 번 결제.",
        "f_contact": "문의", "f_privacy": "개인정보 처리방침", "f_terms": "이용약관",
        "mac_hi_kicker": "메뉴바에 상주",
        "mac_hi_h2": "Mac에서 데스크브레스는 잠깐 켜는 앱이 아니라, <em>계속 화면에 머무는 존재</em>입니다.",
        "mac_hi_lede": "메뉴바에 호흡 원을 고정하거나, 작업 화면 위에 플로팅 오브로 띄워두세요. 하루 종일 화면 어딘가에서 조용히 리듬을 지킵니다.",
        "mac_hi_caps": ["메뉴바 오브", "플로팅 오브", "주간 통계"],
    },
    "ja": {
        "dir": "ja/", "lang": "ja", "font": '"Hiragino Kaku Gothic ProN", "Hiragino Sans", "Yu Gothic"', "shots": "ja",
        "title": "デスクブレス — アプリを閉じても続く呼吸のリズム",
        "desc": "デスクブレスはダイナミックアイランドやメニューバーに静かな呼吸の輪を灯し続けます。吸う4秒・吐く6秒のリズムを在宅勤務中も、デスクワーク中も視界の端で確認し、ストレッチ通知で猫背をほぐしましょう。",
        "og_title": "デスクブレス — デスクワーク向け呼吸タイマー",
        "og_desc": "アプリを閉じても続く呼吸のリズム。在宅勤務とデスクワークのためのタイマー。",
        "kicker_num": "呼吸タイマー",
        "h1": "アプリを閉じても、<br><em>呼吸のリズム</em>は続く。",
        "sub": "オンライン会議と作業の合間、呼吸はつい忘れがちです。デスクブレスはアプリを閉じても、ダイナミックアイランドとメニューバーに静かな呼吸の輪を灯し続けます — 吸う4秒、吐く6秒。猫背が固まる前に、デスクワークが長引く前に、視界の端でリズムを確かめて。",
        "badge_small": "ダウンロードは", "note": "無料プリセット · IPHONE &amp; MAC · サブスクなし",
        "badge_aria": "App Store でダウンロード", "coming_soon": "近日公開",
        "orb_in": "吸う", "orb_out": "吐く",
        "marquee": ["呼吸", "集中", "ストレッチ", "猫背", "リズム", "在宅勤務", "デスクワーク", "回復"],
        "how_kicker": "使い方",
        "how_h2": "<em>呼吸の輪</em>があなたを見つける3つの瞬間。",
        "steps": [
            ["はじめる", "リズムを選んで開始", "ボックス呼吸、4-7-8、または自分だけの秒数設定 — 登録不要でメニューバーやアプリからすぐ無料で始められます。"],
            ["見る", "作業しながら確かめる", "ダイナミックアイランドやメニューバーで呼吸の輪が動き続けます。スクロールの合間に一度見るだけで呼吸が整います。"],
            ["立ち上がる", "ストレッチ通知で動く", "30・60・90・120分ごとの通知が、立ち上がって肩を回し、姿勢を整えるタイミングを教えてくれます。"],
        ],
        "value_kicker": "起動し続ける", "value_num": "アプリを閉じても",
        "value_h2": "アプリを閉じても、<br><em>リズム</em>は止まらない。",
        "value_lede": "猫背やこりは、アプリを開き直すまで待ってくれません。デスクブレスはロック画面でも、メニューバーでも呼吸の輪を灯し続けます。",
        "iphone_tag": "IPHONE", "iphone_h3": "ダイナミックアイランド &amp; ロック画面",
        "iphone_p": "ライブアクティビティがダイナミックアイランドに呼吸の輪とカウントダウンを表示し続けます。オンライン会議中でも、ロックを解除しなくても見えます。",
        "mac_tag": "MAC", "mac_h3": "メニューバー &amp; フローティングオーブ",
        "mac_p": "小さな呼吸の輪がメニューバーに常駐し、必要なら常に最前面に浮かぶフローティングオーブが作業画面の上に静かに佇みます。",
        "shots_kicker": "画面", "shots_num": "IOS 17+ · MACOS 14+",
        "shots_h2": "仕事の合間に使う道具、<em>デモではなく</em>。",
        "shots_caps": ["呼吸セッション実行中", "リズム · プリセット設定", "週間統計 · ストリーク"],
        "feat_kicker": "こだわり", "feat_num": "06",
        "feat_h2": "静かに、でも<em>抜かりなく</em>。",
        "feats": [
            ["ボックス呼吸 · プリセット", "4-4-4-4 ボックス呼吸、4-7-8 など — 無料で内蔵、ワンタップですぐ始められます。", False],
            ["リズムのカスタム · ハプティック", "吸う・吐く秒数を自分で設定し、切り替わるたびにハプティックで感じられます — 無料。", False],
            ["色・画像で着せ替え", "呼吸の輪の色を変え、好きな画像を入れ、カウントの向きも自分好みに反転できます。", True],
            ["週間統計 · ストリーク", "今週実際に終えたセッション数を確認し、ストリークをつなげましょう。", True],
            ["ストレッチ通知", "30・60・90・120分ごとに、立ち上がってストレッチし、姿勢を整える通知。", False],
            ["買い切り、サブスクなし", "Pro は一度きりの買い切り。毎月引き落とされる料金はありません。", False],
        ],
        "final_h2": "呼吸にリズムを。", "final_lede": "iPhone と Mac で無料プリセット。Pro は買い切り一回。",
        "f_contact": "お問い合わせ", "f_privacy": "プライバシーポリシー", "f_terms": "利用規約",
        "mac_hi_kicker": "メニューバーに常駐",
        "mac_hi_h2": "Macでは、デスクブレスは「たまに開くアプリ」ではなく<em>ずっと画面にいる存在</em>です。",
        "mac_hi_lede": "呼吸の輪をメニューバーに固定するか、作業画面の上にフローティングオーブとして浮かべておきましょう。仕事中ずっと、画面のどこかで静かにリズムを刻み続けます。",
        "mac_hi_caps": ["メニューバーオーブ", "フローティングオーブ", "週間統計"],
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
    if APP_STORE_URL:
        return (f'<a class="store-badge" id="{el_id}" href="{APP_STORE_URL}" aria-label="{loc["badge_aria"]}">{APPLE_SVG}'
                f'<span class="txt"><small>{loc["badge_small"]}</small><strong>App Store</strong></span></a>')
    return (f'<a class="store-badge soon" id="{el_id}" href="javascript:void(0)" aria-disabled="true">{APPLE_SVG}'
            f'<span class="txt"><small>App Store</small><strong>{loc["coming_soon"]}</strong></span></a>')


def render(key):
    loc = LOCALES[key]
    rel = "../" if loc["dir"] else ""
    font_override = f'<style>body{{font-family:-apple-system,BlinkMacSystemFont,{loc["font"]},"Segoe UI",sans-serif}}</style>' if loc["font"] else ""

    steps = "".join(
        f'<div class="step"><span class="n">0{i+1}</span><span class="tag">{tag}</span><h3>{h}</h3><p>{p}</p></div>'
        for i, (tag, h, p) in enumerate(loc["steps"])
    )
    shot_files = ["01-main-active", "02-settings", "03-stats"]
    shots = "".join(
        f'<figure><div class="phone-frame"><img src="{rel}assets/shot-{loc["shots"]}-{f}.png" alt="{cap}" loading="lazy"><div class="island"></div></div><figcaption>{cap}</figcaption></figure>'
        for f, cap in zip(shot_files, loc["shots_caps"])
    )
    feats = "".join(
        f'<div class="feat"><h3>{h}{" <span class=\'pro-chip\'>PRO</span>" if pro else ""}</h3><p>{p}</p></div>'
        for h, p, pro in loc["feats"]
    )
    orb_labels_json = json.dumps({"in": loc["orb_in"], "out": loc["orb_out"]}, ensure_ascii=False)
    mac_hi_files = ["macreal-menubar", "macreal-orb", "macreal-stats"]
    mac_hi_shots = "".join(
        f'<figure><div class="frame"><img src="{rel}assets/{f}-{loc["shots"]}.png" alt="{cap}" loading="lazy"></div><figcaption>{cap}</figcaption></figure>'
        for f, cap in zip(mac_hi_files, loc["mac_hi_caps"])
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
<meta property="og:image" content="{BASE_URL}assets/icon-180.png">
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
    <a class="wordmark" href="{rel if rel else './'}"><img src="{rel}assets/icon-180.png" alt=""><span>DESK·BREATH</span></a>
    <div class="lang">{lang_nav(loc['dir'], rel)}</div>
  </div>
</nav>

<header class="hero">
  <div class="wrap">
    <div class="kicker">{loc['kicker_num']}</div>
    <h1>{loc['h1']}</h1>

    <div class="orb-stage">
      <div class="orb" id="orb"></div>
      <div class="orb-count" id="orbCount">4</div>
    </div>
    <div class="orb-label" id="orbLabel">{loc['orb_in']}</div>

    <p class="sub">{loc['sub']}</p>

    <div class="cta">
      {badge(loc, 'storeLink')}
      <span class="note">{loc['note']}</span>
    </div>
  </div>
</header>

<div class="rule"></div>

<section>
  <div class="wrap">
    <div class="section-head">
      <div class="kicker">{loc['how_kicker']}</div>
      <h2>{loc['how_h2']}</h2>
    </div>
    <div class="steps">{steps}</div>
  </div>
</section>

<div class="rule"></div>

<section>
  <div class="wrap">
    <div class="section-head">
      <div class="kicker">{loc['value_kicker']} · {loc['value_num']}</div>
      <h2>{loc['value_h2']}</h2>
      <p class="lede">{loc['value_lede']}</p>
    </div>
    <div class="platform-grid">
      <div class="platform-card">
        <div class="device-shot iphone">
          <img src="{rel}assets/island-{loc["shots"]}.png" alt="{loc['iphone_h3']}" loading="lazy">
        </div>
        <span class="tag">{loc['iphone_tag']}</span>
        <h3>{loc['iphone_h3']}</h3>
        <p>{loc['iphone_p']}</p>
      </div>
      <div class="platform-card">
        <div class="device-shot mac">
          <img src="{rel}assets/macreal-menubar-{loc["shots"]}.png" alt="{loc['mac_h3']}" loading="lazy">
        </div>
        <span class="tag">{loc['mac_tag']}</span>
        <h3>{loc['mac_h3']}</h3>
        <p>{loc['mac_p']}</p>
      </div>
    </div>
  </div>
</section>

<div class="rule"></div>

<section class="mac-highlight">
  <div class="wrap">
    <div class="section-head">
      <div class="kicker">{loc['mac_hi_kicker']}</div>
      <h2>{loc['mac_hi_h2']}</h2>
      <p class="lede">{loc['mac_hi_lede']}</p>
    </div>
    <div class="row">{mac_hi_shots}</div>
  </div>
</section>

<div class="rule"></div>

<section class="shots">
  <div class="wrap">
    <div class="section-head">
      <div class="kicker">{loc['shots_kicker']} · {loc['shots_num']}</div>
      <h2>{loc['shots_h2']}</h2>
    </div>
    <div class="row">{shots}</div>
  </div>
</section>

<div class="rule"></div>

<section>
  <div class="wrap">
    <div class="section-head">
      <div class="kicker">{loc['feat_kicker']} · {loc['feat_num']}</div>
      <h2>{loc['feat_h2']}</h2>
    </div>
    <div class="grid6">{feats}</div>
  </div>
</section>

<div class="rule"></div>

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
  const orb = document.getElementById("orb");
  const orbCount = document.getElementById("orbCount");
  const orbLabel = document.getElementById("orbLabel");
  const labels = {orb_labels_json};

  if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {{
    const sleep = (ms) => new Promise(r => setTimeout(r, ms));
    (async function loop() {{
      for (;;) {{
        // inhale: 4s, scale up, tide color, count 4 -> 0
        orbLabel.textContent = labels.in;
        orb.style.transition = "transform 4s linear, background-color 4s linear, box-shadow 4s linear";
        orb.style.transform = "scale(1.32)";
        orb.style.backgroundColor = "var(--tide)";
        orb.style.boxShadow = "0 0 120px 20px color-mix(in srgb, var(--tide) 45%, transparent)";
        for (let i = 4; i >= 0; i--) {{ orbCount.textContent = i; if (i > 0) await sleep(1000); }}

        // exhale: 6s, scale down, ember color, count 6 -> 0
        orbLabel.textContent = labels.out;
        orb.style.transition = "transform 6s linear, background-color 6s linear, box-shadow 6s linear";
        orb.style.transform = "scale(1)";
        orb.style.backgroundColor = "var(--ember)";
        orb.style.boxShadow = "0 0 60px 6px color-mix(in srgb, var(--ember) 30%, transparent)";
        for (let i = 6; i >= 0; i--) {{ orbCount.textContent = i; if (i > 0) await sleep(1000); }}
      }}
    }})();
  }}
</script>
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
