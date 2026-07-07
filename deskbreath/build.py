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
        "title": "DeskBreath — A breathing rhythm you can feel, one tap at a time",
        "desc": "DeskBreath turns your breathing rhythm into something you can feel — tap to start, distinct haptics for inhale, hold and exhale — plus honest stretch reminders for people who sit at a desk all day.",
        "og_title": "DeskBreath — Breathing Timer for Desk Work",
        "og_desc": "A breathing rhythm built for desk work — one tap, real haptics, honest stretch tracking.",
        "kicker_num": "BREATHING TIMER",
        "h1": "One tap.<br>A rhythm you can <em>feel</em>.",
        "sub": "Between back-to-back calls and heads-down deep work, breathing is the first thing you forget. DeskBreath turns it into something physical — tap the circle once to start, and feel each phase change as a distinct pulse for inhale, hold, and exhale.",
        "badge_small": "Download on the", "note": "FREE PRESETS · IPHONE &amp; MAC · NO SUBSCRIPTION",
        "badge_aria": "Download on the App Store", "coming_soon": "Coming soon",
        "orb_in": "Breathe in", "orb_out": "Breathe out",
        "marquee": ["BREATHE", "FOCUS", "STRETCH", "POSTURE", "RHYTHM", "DEEP WORK", "DESK FATIGUE", "CALM"],
        "how_kicker": "HOW IT WORKS",
        "how_h2": "Three moments where the <em>rhythm</em> finds you.",
        "steps": [
            ["START", "Pick a rhythm and go", "Box breathing, 4-7-8, or your own inhale/exhale seconds — start free, no account, right from the menu bar or the app."],
            ["FEEL", "Feel each phase change", "Distinct haptics mark inhale, hold, and exhale, so you can keep the rhythm without watching the screen."],
            ["STAND UP", "Rise on the stretch cue", "Every 30, 60, 90 or 120 minutes, a gentle nudge tells you to stand and stretch — tap Done only when you actually did, so your stats stay honest."],
        ],
        "value_kicker": "REAL ACCOUNTABILITY", "value_num": "NOT JUST A TIMER",
        "value_h2": "A timer that <em>knows</em> if you actually moved.",
        "value_lede": "Desk fatigue doesn't care how many reminders you dismiss. DeskBreath only counts a stretch when you tap Done — and quietly ends your session after 10 hours, so you're never reminded once you've clocked out.",
        "iphone_tag": "IPHONE", "iphone_h3": "Tap to Start, Feel Every Phase",
        "iphone_p": "Tap the breathing circle once to start or pause, and feel distinct haptics as you move from inhale to hold to exhale — no need to watch the screen.",
        "mac_tag": "MAC", "mac_h3": "Menu Bar &amp; Floating Circle",
        "mac_p": "A tiny breathing circle lives in your menu bar, and an optional always-on-top floating circle sits quietly over whatever you're working on.",
        "shots_kicker": "SCREENS", "shots_num": "IOS 17+ · MACOS 14+",
        "shots_h2": "Built for the middle of a workday, <em>not a demo</em>.",
        "shots_caps": ["ACTIVE BREATHING SESSION", "RHYTHM &amp; PRESET SETTINGS", "WEEKLY STATS &amp; STREAK"],
        "feat_kicker": "DETAILS", "feat_num": "07",
        "feat_h2": "Small app. <em>Deliberate</em> choices.",
        "feats": [
            ["Box breathing &amp; presets", "4-4-4-4 box breathing, 4-7-8, and more — free, built in, ready in one tap.", False],
            ["Haptics for every phase", "Feel inhale, hold, and exhale as distinct pulses — set your own seconds, too. Free.", False],
            ["Color, image &amp; direction", "Recolor the circle, drop in your own image, and flip the countdown direction to match how you focus.", True],
            ["7 breathing themes", "Circle, Equalizer, Ring, Bloom, Box, Waveform, Pulse — pick the look that fits your focus.", True],
            ["Weekly stats &amp; streaks", "See how many sessions you actually finished this week, and keep the streak alive.", True],
            ["Honest stretch reminders", "Nudges every 30, 60, 90 or 120 minutes — tap Done only when you actually stretched.", False],
            ["Pay once. No subscription.", "Pro is a single lifetime purchase — one payment, no recurring fees, ever.", False],
        ],
        "final_h2": "Give your breath a rhythm.", "final_lede": "Free presets on iPhone and Mac. Pro unlocks once, forever.",
        "f_contact": "Contact", "f_privacy": "Privacy", "f_terms": "Terms",
    },
    "ko": {
        "dir": "ko/", "lang": "ko", "font": '"Apple SD Gothic Neo", "Pretendard"', "shots": "ko",
        "title": "데스크브레스 — 탭 한 번, 느껴지는 호흡 리듬",
        "desc": "데스크브레스는 탭 한 번으로 시작하고, 들숨·멈춤·날숨을 구분하는 확실한 햅틱으로 리듬을 느끼게 해줍니다. 스트레칭도 실제로 한 것만 기록되는 정직한 알림으로, 하루 종일 책상 앞에 있는 사람을 위해.",
        "og_title": "데스크브레스 — 업무용 호흡 타이머",
        "og_desc": "탭 한 번, 확실한 햅틱, 정직한 스트레칭 기록 — 업무를 위한 호흡 리듬.",
        "kicker_num": "호흡 타이머",
        "h1": "탭 한 번,<br><em>느껴지는</em> 호흡 리듬.",
        "sub": "화상회의와 집중 작업 사이, 호흡은 자꾸 잊혀집니다. 데스크브레스는 호흡 원을 한 번 탭하면 시작하고, 들숨·멈춤·날숨이 바뀔 때마다 확실한 햅틱으로 느껴져요.",
        "badge_small": "다운로드는", "note": "무료 프리셋 · IPHONE &amp; MAC · 구독 없음",
        "badge_aria": "App Store에서 다운로드", "coming_soon": "출시 예정",
        "orb_in": "들숨", "orb_out": "날숨",
        "marquee": ["호흡", "집중", "스트레칭", "거북목", "리듬", "재택근무", "야근", "회복"],
        "how_kicker": "사용 방법",
        "how_h2": "<em>호흡 원</em>이 당신을 찾아오는 세 순간.",
        "steps": [
            ["시작", "리듬을 고르고 시작", "박스호흡, 4-7-8, 혹은 나만의 들숨·날숨 초 — 계정 없이 메뉴바나 앱에서 바로 무료로 시작합니다."],
            ["느끼기", "단계마다 느끼기", "들숨·멈춤·날숨이 바뀔 때마다 다른 햅틱으로 느껴져서, 화면을 보지 않아도 리듬을 유지할 수 있어요."],
            ["일어나기", "스트레칭 알림에 일어나기", "30·60·90·120분마다 부드러운 알림이 자리에서 일어나 어깨를 풀고 자세를 바로잡으라고 알려줍니다. 실제로 했을 때만 \"했어요\"를 눌러 기록에 남겨요."],
        ],
        "value_kicker": "정직한 기록", "value_num": "타이머 그 이상",
        "value_h2": "실제로 <em>움직였는지</em> 아는 타이머.",
        "value_lede": "거북목과 뻐근함은 알림을 몇 번 무시했는지 신경 쓰지 않습니다. 데스크브레스는 실제로 스트레칭했을 때만 \"했어요\"로 기록하고, 세션은 10시간 뒤 자동으로 끝나 퇴근 후엔 알림이 오지 않아요.",
        "iphone_tag": "IPHONE", "iphone_h3": "탭으로 시작, 단계마다 느끼기",
        "iphone_p": "호흡 원을 한 번 탭해서 시작하거나 멈추고, 들숨에서 멈춤, 날숨으로 넘어갈 때마다 다른 햅틱을 느껴보세요 — 화면을 보지 않아도 됩니다.",
        "mac_tag": "MAC", "mac_h3": "메뉴바 &amp; 플로팅 호흡 원",
        "mac_p": "작은 호흡 원이 메뉴바에 상주하고, 원하면 항상 위에 뜨는 플로팅 호흡 원이 작업 화면 위에 조용히 자리합니다.",
        "shots_kicker": "화면", "shots_num": "IOS 17+ · MACOS 14+",
        "shots_h2": "업무 중간에 쓰는 도구, <em>데모가 아니라</em>.",
        "shots_caps": ["호흡 세션 진행 중", "리듬 · 프리셋 설정", "주간 통계 · 스트릭"],
        "feat_kicker": "디테일", "feat_num": "07",
        "feat_h2": "작은 앱, <em>분명한 선택</em>.",
        "feats": [
            ["박스호흡 · 프리셋", "4-4-4-4 박스호흡, 4-7-8 등 — 무료로 내장, 한 탭이면 바로 시작합니다.", False],
            ["단계별 햅틱", "들숨·멈춤·날숨을 각각 다른 햅틱으로 느껴보세요. 초도 직접 정할 수 있어요 — 무료.", False],
            ["색 · 이미지 꾸미기", "호흡 원 색을 바꾸고 원하는 이미지를 넣고, 카운트 방향까지 내게 맞게 뒤집습니다.", True],
            ["호흡 원 테마 7종", "원형·이퀄라이저·링·블룸·박스·파형·펄스 중 취향에 맞는 모양을 골라보세요.", True],
            ["주간 통계 · 스트릭", "이번 주 실제로 끝낸 세션이 몇 번인지 확인하고 스트릭을 이어가세요.", True],
            ["정직한 스트레칭 알림", "30·60·90·120분마다 알려드려요. 실제로 했을 때만 \"했어요\"를 눌러 기록에 남습니다.", False],
            ["평생 한 번 결제, 구독 없음", "Pro는 평생 한 번 결제입니다. 매달 빠져나가는 구독료는 없습니다.", False],
        ],
        "final_h2": "호흡에 리듬을 붙이세요.", "final_lede": "iPhone과 Mac에서 무료 프리셋으로. Pro는 평생 한 번 결제.",
        "f_contact": "문의", "f_privacy": "개인정보 처리방침", "f_terms": "이용약관",
    },
    "ja": {
        "dir": "ja/", "lang": "ja", "font": '"Hiragino Kaku Gothic ProN", "Hiragino Sans", "Yu Gothic"', "shots": "ja",
        "title": "デスクブレス — タップひとつで、感じる呼吸のリズム",
        "desc": "デスクブレスはタップひとつで始まり、吸う・止める・吐くを区別するはっきりした触覚フィードバックでリズムを感じさせます。ストレッチも実際に行った分だけ記録される正直な通知で、一日中デスクに座る人のために。",
        "og_title": "デスクブレス — デスクワーク向け呼吸タイマー",
        "og_desc": "タップひとつ、はっきりした触覚、正直なストレッチ記録 — 仕事のための呼吸リズム。",
        "kicker_num": "呼吸タイマー",
        "h1": "タップひとつで、<br><em>感じる</em>呼吸のリズム。",
        "sub": "オンライン会議と作業の合間、呼吸はつい忘れがちです。デスクブレスは呼吸オーブをタップひとつで開始でき、吸う・止める・吐くが切り替わるたびにはっきりした触覚で感じられます。",
        "badge_small": "ダウンロードは", "note": "無料プリセット · IPHONE &amp; MAC · サブスクなし",
        "badge_aria": "App Store でダウンロード", "coming_soon": "近日公開",
        "orb_in": "吸う", "orb_out": "吐く",
        "marquee": ["呼吸", "集中", "ストレッチ", "猫背", "リズム", "在宅勤務", "デスクワーク", "回復"],
        "how_kicker": "使い方",
        "how_h2": "<em>呼吸の輪</em>があなたを見つける3つの瞬間。",
        "steps": [
            ["はじめる", "リズムを選んで開始", "ボックス呼吸、4-7-8、または自分だけの秒数設定 — 登録不要でメニューバーやアプリからすぐ無料で始められます。"],
            ["感じる", "段階ごとに感じる", "吸う・止める・吐くが切り替わるたびに違う触覚で感じられるので、画面を見なくてもリズムを保てます。"],
            ["立ち上がる", "ストレッチ通知で動く", "30・60・90・120分ごとの通知が、立ち上がって肩を回し、姿勢を整えるタイミングを教えてくれます。実際に行ったときだけ「やった」を押して記録します。"],
        ],
        "value_kicker": "正直な記録", "value_num": "タイマー以上のもの",
        "value_h2": "実際に<em>動いたか</em>を知るタイマー。",
        "value_lede": "猫背やこりは、通知を何回スキップしたかなんて気にしてくれません。デスクブレスは実際にストレッチしたときだけ「やった」で記録し、セッションは10時間で自動終了 — 退勤後は通知が来ません。",
        "iphone_tag": "IPHONE", "iphone_h3": "タップで開始、段階ごとに感じる",
        "iphone_p": "呼吸の輪をタップひとつで開始・一時停止し、吸う・止める・吐くが切り替わるたびに違う触覚を感じてください — 画面を見る必要はありません。",
        "mac_tag": "MAC", "mac_h3": "メニューバー &amp; フローティングオーブ",
        "mac_p": "小さな呼吸の輪がメニューバーに常駐し、必要なら常に最前面に浮かぶフローティングオーブが作業画面の上に静かに佇みます。",
        "shots_kicker": "画面", "shots_num": "IOS 17+ · MACOS 14+",
        "shots_h2": "仕事の合間に使う道具、<em>デモではなく</em>。",
        "shots_caps": ["呼吸セッション実行中", "リズム · プリセット設定", "週間統計 · ストリーク"],
        "feat_kicker": "こだわり", "feat_num": "07",
        "feat_h2": "小さなアプリ、<em>明確な選択</em>。",
        "feats": [
            ["ボックス呼吸 · プリセット", "4-4-4-4 ボックス呼吸、4-7-8 など — 無料で内蔵、ワンタップですぐ始められます。", False],
            ["段階ごとのハプティック", "吸う・止める・吐くをそれぞれ違うハプティックで感じられます。秒数も自分で設定可能 — 無料。", False],
            ["色・画像で着せ替え", "呼吸の輪の色を変え、好きな画像を入れ、カウントの向きも自分好みに反転できます。", True],
            ["呼吸オーブのテーマ7種", "サークル・イコライザー・リング・ブルーム・ボックス・波形・パルスから好みの見た目を選べます。", True],
            ["週間統計 · ストリーク", "今週実際に終えたセッション数を確認し、ストリークをつなげましょう。", True],
            ["正直なストレッチ通知", "30・60・90・120分ごとに通知。実際に行ったときだけ「やった」を押して記録されます。", False],
            ["買い切り、サブスクなし", "Pro は一度きりの買い切り。毎月引き落とされる料金はありません。", False],
        ],
        "final_h2": "呼吸にリズムを。", "final_lede": "iPhone と Mac で無料プリセット。Pro は買い切り一回。",
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
    if APP_STORE_URL:
        return (f'<a class="store-badge" id="{el_id}" href="{APP_STORE_URL}" aria-label="{loc["badge_aria"]}">{APPLE_SVG}'
                f'<span class="txt"><small>{loc["badge_small"]}</small><strong>App Store</strong></span></a>')
    return (f'<a class="store-badge soon" id="{el_id}" href="javascript:void(0)" aria-disabled="true">{APPLE_SVG}'
            f'<span class="txt"><small>App Store</small><strong>{loc["coming_soon"]}</strong></span></a>')


def render(key):
    loc = LOCALES[key]
    rel = "../" if loc["dir"] else ""
    font_override = f'<style>body{{font-family:-apple-system,BlinkMacSystemFont,{loc["font"]},"Segoe UI",sans-serif}}</style>' if loc["font"] else ""

    marquee = "".join(f"<span>{m}</span>" for m in loc["marquee"] * 2)
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
  <div class="ghost">DB</div>
  <div class="wrap">
    <div>
      <div class="kicker"><span>DESK · BREATH</span><span class="rule"></span><span class="num">{loc['kicker_num']}</span></div>
      <h1>{loc['h1']}</h1>
      <p class="sub">{loc['sub']}</p>
      <div class="cta">
        {badge(loc, 'storeLink')}
        <span class="note">{loc['note']}</span>
      </div>
    </div>
    <div class="hero-visual">
      <div class="orb-stage">
        <div class="orb" id="orb"></div>
        <div class="orb-count" id="orbCount">4</div>
        <div class="orb-label" id="orbLabel">{loc['orb_in']}</div>
      </div>
      <div class="phone-mini">
        <div class="screen">
          <div class="island"><span class="mini-orb"></span><span class="mini-timer">25:04</span></div>
          <div class="clock">9:41</div>
          <div class="caption">DeskBreath · Box breathing</div>
        </div>
      </div>
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
    <div class="kicker"><span>{loc['value_kicker']}</span><span class="rule"></span><span class="num">{loc['value_num']}</span></div>
    <h2>{loc['value_h2']}</h2>
    <p class="lede">{loc['value_lede']}</p>
    <div class="platform-grid">
      <div class="platform-card">
        <div class="iphone-mock">
          <div class="island"><span class="mini-orb"></span><span class="mini-timer">25:04</span></div>
          <div class="lock-time">9:41</div>
        </div>
        <span class="tag">{loc['iphone_tag']}</span>
        <h3>{loc['iphone_h3']}</h3>
        <p>{loc['iphone_p']}</p>
      </div>
      <div class="platform-card">
        <div class="mac-mock">
          <div class="menubar"><span class="dot"></span><span class="dot"></span><span class="menu-orb"></span></div>
          <div class="floating"></div>
        </div>
        <span class="tag">{loc['mac_tag']}</span>
        <h3>{loc['mac_h3']}</h3>
        <p>{loc['mac_p']}</p>
      </div>
    </div>
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
        orb.style.transition = "transform 4s linear, background-color 4s linear";
        orb.style.transform = "scale(1.42)";
        orb.style.backgroundColor = "var(--tide)";
        for (let i = 4; i >= 0; i--) {{ orbCount.textContent = i; if (i > 0) await sleep(1000); }}

        // exhale: 6s, scale down, ember color, count 6 -> 0
        orbLabel.textContent = labels.out;
        orb.style.transition = "transform 6s linear, background-color 6s linear";
        orb.style.transform = "scale(1)";
        orb.style.backgroundColor = "var(--ember)";
        for (let i = 6; i >= 0; i--) {{ orbCount.textContent = i; if (i > 0) await sleep(1000); }}
      }}
    }})();
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
