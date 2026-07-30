#!/usr/bin/env python3
"""Generate index.html for every locale from one template.

Usage: python3 build.py
Output: ./index.html (en), ./ko/index.html, ./ja/index.html, ./zh/index.html
"""
import json, hashlib
import pathlib

ROOT = pathlib.Path(__file__).parent
CSS_V = hashlib.md5((ROOT / "assets" / "style.css").read_bytes()).hexdigest()[:8]
BASE_URL = "https://www.kkirukstudio.com/deskbreath/"

IOS_URL = "https://apps.apple.com/app/id6786591689"
MAC_URL = "https://apps.apple.com/app/id6786591689?platform=mac"

APPLE_SVG = '<svg viewBox="0 0 384 512" aria-hidden="true"><path d="M318.7 268.7c-.2-36.7 16.4-64.4 50-84.8-18.8-26.9-47.2-41.7-84.7-44.6-35.5-2.8-74.3 20.7-88.5 20.7-15 0-49.4-19.7-76.4-19.7C63.3 141.2 4 184.8 4 273.5q0 39.3 14.4 81.2c12.8 36.7 59 126.7 107.2 125.2 25.2-.6 43-17.9 75.8-17.9 31.8 0 48.3 17.9 76.4 17.9 48.6-.7 90.4-82.5 102.6-119.3-65.2-30.7-61.7-90-61.7-91.9zm-56.6-164.2c27.3-32.4 24.8-61.9 24-72.5-24.1 1.4-52 16.4-67.9 34.9-17.5 19.8-27.8 44.3-25.6 71.9 26.1 2 49.9-11.4 69.5-34.3z"/></svg>'

LANG_LABELS = [("", "EN"), ("ko/", "한국어"), ("ja/", "日本語"), ("zh/", "繁體中文")]

LOCALES = {
    "en": {
        "dir": "", "lang": "en", "font": None, "shots": "en",
        "title": "DeskBreath — A breathing circle in the corner of your screen",
        "desc": "One circle in your menu bar, counting four seconds in and six seconds out while you keep working. Stretch reminders you can skip, and a session that ends itself after ten hours. iPhone and Mac, free to start, no subscription.",
        "og_title": "DeskBreath — Breathing timer for desk work",
        "og_desc": "A breathing circle that lives in the corner of your screen. iPhone and Mac, free to start, no subscription.",
        "brand2": "Breathing timer",
        "h1": "It breathes in the<br>corner of your <em>screen</em>.",
        "sub": "One circle in the menu bar, counting four seconds in and six seconds out. You keep working; it keeps the rhythm.",
        "note": "Free to start · iPhone and Mac · No subscription",
        "ios_cta": "App Store", "mac_cta": "Mac App Store",
        "orb_in": "Breathe in", "orb_out": "Breathe out",
        "rhythm_h2": "Four seconds in, <em>six seconds out</em>.",
        "rhythm_in": "<b>4s</b> in", "rhythm_out": "<b>6s</b> out",
        "rhythm_lede": "A longer exhale is what settles you, so that's the default. Switch to box breathing or 4-7-8, or set the seconds yourself. Each phase change arrives as its own haptic, so you never have to watch the screen.",
        "mac_h2": "On a Mac it just <em>stays on your screen</em>.",
        "mac_caps": [
            ["Or floating on top", "Track it out of the corner of your eye. It follows you across desktops."],
            ["Always up there", "Glance up mid-task and you can see whether you're on the in-breath or the out-breath."],
            ["Today's count", "Breaths and stretches for the day, without leaving what you were doing."],
        ],
        "phone_h2": "On iPhone you feel it <em>instead of watching it</em>.",
        "phone_caps": [
            ["One tap to start", "Tap the circle to begin or pause. Distinct haptics mark inhale, hold and exhale."],
            ["Your rhythm", "Presets, or your own seconds. Reminder intervals in five-minute steps."],
            ["What you actually did", "Skipped reminders don't count. Only the ones you marked as done."],
        ],
        "plans_h2": "Free is enough. <em>Pro is once.</em>",
        "plan_free_h": "Free", "plan_free_price": "Everything you need to start",
        "plan_free": [
            "The breathing circle, 4 in / 6 out",
            "Box breathing, 4-7-8, or your own seconds",
            "A different haptic for each phase",
            "Stretch reminders, any interval in 5-minute steps",
            "Skip a reminder when you can't stop",
            "The session ends itself after 10 hours",
            "Today's breaths and stretches",
        ],
        "plan_pro_h": "Pro", "plan_pro_price": "One purchase, no subscription",
        "plan_pro": [
            "7 shapes for the circle",
            "Your own colors, image and count direction",
            "Weekly stats and streaks",
            "Reminders only during your work hours",
            "iPhone and Mac in sync over iCloud",
        ],
        "final_h2": "Start with this afternoon.",
        "f_contact": "Contact", "f_privacy": "Privacy", "f_terms": "Terms",
        "req": "iOS 17+ · macOS 14+",
    },
    "ko": {
        "dir": "ko/", "lang": "ko", "font": '"Apple SD Gothic Neo", "Pretendard"', "shots": "ko",
        "title": "데스크브레스 — 화면 한쪽에서 같이 숨 쉬는 호흡 원",
        "desc": "메뉴바 한 칸에 호흡 원 하나. 4초 들이쉬고 6초 내쉬는 리듬을 곁에서 세어줘요. 못 할 땐 건너뛰어도 되고, 세션은 10시간 뒤 알아서 끝나요. iPhone과 Mac, 무료로 시작하고 구독은 없어요.",
        "og_title": "데스크브레스 — 업무용 호흡 타이머",
        "og_desc": "화면 한쪽에서 같이 숨 쉬는 호흡 원. iPhone과 Mac, 무료로 시작하고 구독은 없어요.",
        "brand2": "호흡 타이머",
        "h1": "화면 한쪽에서<br>같이 <em>숨 쉬어요</em>.",
        "sub": "메뉴바 한 칸에 호흡 원 하나. 4초 들이쉬고 6초 내쉬는 리듬을 곁에서 세어줘요. 하던 일은 그대로 두면 돼요.",
        "note": "무료로 시작 · iPhone과 Mac · 구독 없음",
        "ios_cta": "App Store", "mac_cta": "Mac App Store",
        "orb_in": "들숨", "orb_out": "날숨",
        "rhythm_h2": "4초 들이쉬고, <em>6초 내쉬고</em>.",
        "rhythm_in": "들숨 <b>4초</b>", "rhythm_out": "날숨 <b>6초</b>",
        "rhythm_lede": "내쉬는 숨이 길어야 몸이 풀려서 기본을 이렇게 잡았어요. 박스 호흡이나 4-7-8로 바꿔도 되고, 초를 직접 정해도 돼요. 단계가 바뀔 때마다 햅틱이 달라서 화면은 안 봐도 돼요.",
        "mac_h2": "맥에선 <em>하던 화면 위에</em> 그냥 둬요.",
        "mac_caps": [
            ["문서 위에 띄워도 돼요", "곁눈으로 리듬만 따라가면 돼요. 데스크톱을 옮겨 다녀도 따라와요."],
            ["늘 거기 있어요", "일하다 한 번 올려다보면 지금 들숨인지 날숨인지 바로 보여요."],
            ["오늘 얼마나 했는지", "숨 고른 횟수랑 스트레칭 기록을 하던 자리에서 바로 봐요."],
        ],
        "phone_h2": "iPhone에선 보지 않고 <em>손끝으로</em> 따라가요.",
        "phone_caps": [
            ["탭 한 번으로", "호흡 원을 탭하면 시작하고 멈춰요. 들숨·멈춤·날숨이 각각 다른 햅틱으로 와요."],
            ["내 리듬대로", "프리셋을 쓰거나 초를 직접 정하고, 알림 주기는 5분 단위로 맞춰요."],
            ["진짜 한 것만", "건너뛴 건 안 세요. \"했어요\"를 누른 것만 오늘 기록에 남아요."],
        ],
        "plans_h2": "무료로 충분하고, <em>Pro는 한 번</em>이에요.",
        "plan_free_h": "무료", "plan_free_price": "시작하는 데 필요한 건 다 있어요",
        "plan_free": [
            "호흡 원과 4초 들숨 · 6초 날숨",
            "박스 호흡, 4-7-8, 직접 정한 초",
            "단계마다 다른 햅틱",
            "스트레칭 알림, 5분 단위로 주기 설정",
            "지금 못 하면 알림에서 바로 건너뛰기",
            "세션은 10시간 뒤 알아서 종료",
            "오늘의 호흡 · 스트레칭 횟수",
        ],
        "plan_pro_h": "Pro", "plan_pro_price": "평생 한 번 결제, 구독 없음",
        "plan_pro": [
            "호흡 원 모양 7종",
            "색과 이미지, 카운트 방향 바꾸기",
            "주간 통계와 스트릭",
            "정해둔 업무 시간에만 알림",
            "iPhone과 Mac을 iCloud로 하나로",
        ],
        "final_h2": "오늘 오후부터 한번 해보세요.",
        "f_contact": "문의", "f_privacy": "개인정보 처리방침", "f_terms": "이용약관",
        "req": "iOS 17+ · macOS 14+",
    },
    "ja": {
        "dir": "ja/", "lang": "ja", "font": '"Hiragino Maru Gothic ProN", "Hiragino Kaku Gothic ProN", "Yu Gothic"', "shots": "ja",
        "title": "デスクブレス — 画面のすみで一緒に呼吸するオーブ",
        "desc": "メニューバーにオーブがひとつ。4秒吸って6秒吐くリズムをそばで数えます。できないときは飛ばせて、セッションは10時間で自動終了。iPhone と Mac、無料で始められてサブスクはありません。",
        "og_title": "デスクブレス — デスクワーク向け呼吸タイマー",
        "og_desc": "画面のすみで一緒に呼吸するオーブ。iPhone と Mac、無料で始められてサブスクなし。",
        "brand2": "呼吸タイマー",
        "h1": "画面のすみで<br>一緒に<em>呼吸します</em>。",
        "sub": "メニューバーにオーブがひとつ。4秒吸って6秒吐くリズムをそばで数えます。手を止めなくて大丈夫です。",
        "note": "無料で開始 · iPhone と Mac · サブスクなし",
        "ios_cta": "App Store", "mac_cta": "Mac App Store",
        "orb_in": "吸う", "orb_out": "吐く",
        "rhythm_h2": "4秒吸って、<em>6秒吐く</em>。",
        "rhythm_in": "吸う <b>4秒</b>", "rhythm_out": "吐く <b>6秒</b>",
        "rhythm_lede": "吐く息が長いほど体はゆるむので、これを基本にしました。ボックス呼吸や4-7-8に変えても、秒数を自分で決めても大丈夫です。切り替わるたびに触覚が変わるので、画面を見る必要はありません。",
        "mac_h2": "Mac では<em>作業画面の上に</em>そのまま。",
        "mac_caps": [
            ["書類の上に浮かせても", "視界の端でリズムを追うだけ。デスクトップを移動しても最前面のままです。"],
            ["いつもそこに", "作業中にふと目を上げれば、いま吸うところか吐くところかがすぐ分かります。"],
            ["今日の回数", "呼吸とストレッチの記録を、作業していた場所でそのまま確認できます。"],
        ],
        "phone_h2": "iPhone では見ずに<em>指先で</em>追えます。",
        "phone_caps": [
            ["タップひとつで", "オーブをタップすれば開始と一時停止。吸う・止める・吐くが違う触覚で届きます。"],
            ["自分のリズムで", "プリセットでも、秒数の自由設定でも。通知の間隔は5分刻みです。"],
            ["やった分だけ", "飛ばした分は数えません。「やった」を押した分だけ今日の記録に残ります。"],
        ],
        "plans_h2": "無料で十分、<em>Pro は一度きり</em>。",
        "plan_free_h": "無料", "plan_free_price": "始めるのに必要なものは全部",
        "plan_free": [
            "呼吸オーブと 吸う4秒・吐く6秒",
            "ボックス呼吸、4-7-8、秒数の自由設定",
            "段階ごとに違う触覚",
            "ストレッチ通知、5分刻みの間隔設定",
            "できないときは通知からそのままスキップ",
            "セッションは10時間で自動終了",
            "今日の呼吸とストレッチの回数",
        ],
        "plan_pro_h": "Pro", "plan_pro_price": "買い切り一回、サブスクなし",
        "plan_pro": [
            "オーブの形 7種類",
            "色と画像、カウントの向きの変更",
            "週間統計とストリーク",
            "決めた勤務時間だけ通知",
            "iPhone と Mac を iCloud でひとつに",
        ],
        "final_h2": "今日の午後から始めてみませんか。",
        "f_contact": "お問い合わせ", "f_privacy": "プライバシーポリシー", "f_terms": "利用規約",
        "req": "iOS 17+ · macOS 14+",
    },
    "zh": {
        "dir": "zh/", "lang": "zh-Hant", "font": '"PingFang TC", "Heiti TC"', "shots": "en",
        "title": "DeskBreath — 在螢幕角落陪你呼吸的圓",
        "desc": "選單列上一顆呼吸圓，替你數著吸氣 4 秒、吐氣 6 秒。忙的時候可以跳過，工作時段滿 10 小時會自動結束。iPhone 與 Mac，免費開始，沒有訂閱。",
        "og_title": "DeskBreath — 專為辦公設計的呼吸計時器",
        "og_desc": "在螢幕角落陪你呼吸的圓。iPhone 與 Mac，免費開始，沒有訂閱。",
        "brand2": "呼吸計時器",
        "h1": "在螢幕角落，<br>陪你<em>一起呼吸</em>。",
        "sub": "選單列上一顆呼吸圓，替你數著吸氣 4 秒、吐氣 6 秒。手邊的事照做就好。",
        "note": "免費開始 · iPhone 與 Mac · 沒有訂閱",
        "ios_cta": "App Store", "mac_cta": "Mac App Store",
        "orb_in": "吸氣", "orb_out": "吐氣",
        "rhythm_h2": "吸氣 4 秒，<em>吐氣 6 秒</em>。",
        "rhythm_in": "吸氣 <b>4 秒</b>", "rhythm_out": "吐氣 <b>6 秒</b>",
        "rhythm_lede": "吐氣拉長身體才鬆得下來，所以預設是這個比例。你也可以改成箱式呼吸、4-7-8，或自己設定秒數。每次切換的震動都不一樣，不用一直盯著螢幕。",
        "mac_h2": "在 Mac 上，就<em>留在你的畫面上</em>。",
        "mac_caps": [
            ["也可以浮在文件上", "用眼角餘光跟著節奏就好，換到別的桌面也依然在最上層。"],
            ["一直都在那裡", "工作到一半抬頭看一眼，就知道現在該吸還是該吐。"],
            ["今天做了多少", "呼吸與伸展的紀錄，就在你工作的地方直接看。"],
        ],
        "phone_h2": "在 iPhone 上用<em>指尖</em>跟著走。",
        "phone_caps": [
            ["輕點一下開始", "點一下呼吸圓就開始或暫停，吸氣、停頓、吐氣各有不同的震動。"],
            ["照你的節奏", "用預設或自訂秒數，提醒間隔以 5 分鐘為單位調整。"],
            ["只算真的做到的", "跳過的不計入，只有按下「完成」的才會留在今天的紀錄裡。"],
        ],
        "plans_h2": "免費就夠用，<em>Pro 只付一次</em>。",
        "plan_free_h": "免費", "plan_free_price": "開始需要的都在這裡",
        "plan_free": [
            "呼吸圓與 吸氣 4 秒、吐氣 6 秒",
            "箱式呼吸、4-7-8、自訂秒數",
            "每個階段不同的震動",
            "伸展提醒，間隔以 5 分鐘為單位",
            "忙的時候可以直接從通知跳過",
            "工作時段滿 10 小時自動結束",
            "今天的呼吸與伸展次數",
        ],
        "plan_pro_h": "Pro", "plan_pro_price": "一次付費，沒有訂閱",
        "plan_pro": [
            "7 種呼吸圓造型",
            "自訂顏色、圖片與倒數方向",
            "週統計與連續紀錄",
            "只在設定好的工作時段提醒",
            "iPhone 與 Mac 透過 iCloud 同步",
        ],
        "final_h2": "就從今天下午開始吧。",
        "f_contact": "聯絡我們", "f_privacy": "隱私權政策", "f_terms": "使用條款",
        "req": "iOS 17+ · macOS 14+",
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


def badges(loc, suffix):
    ios = (f'<a class="store-badge" id="storeLink{suffix}" href="{IOS_URL}" target="_blank" rel="noopener">'
           f'{APPLE_SVG}<span>{loc["ios_cta"]}</span></a>')
    mac = (f'<a class="store-badge" id="storeLink{suffix}-mac" href="{MAC_URL}" target="_blank" rel="noopener">'
           f'{APPLE_SVG}<span>{loc["mac_cta"]}</span></a>')
    return ios + mac


def render(key):
    loc = LOCALES[key]
    rel = "../" if loc["dir"] else ""
    font_override = (f'<style>body{{font-family:ui-rounded,"SF Pro Rounded",-apple-system,{loc["font"]},system-ui,sans-serif}}</style>'
                     if loc["font"] else "")

    mac_shots = "".join(
        f'<figure class="shot{cls}"><img src="{rel}assets/macreal-{name}-{loc["shots"]}.png" alt="" width="{w}" height="{ht}" loading="lazy">'
        f'<figcaption><b>{h}</b>{p}</figcaption></figure>'
        for (name, w, ht, cls), (h, p) in zip(
            [("orb", 750, 440, " wide"), ("menubar", 528, 932, ""), ("stats", 840, 1000, "")], loc["mac_caps"]
        )
    )
    phone_files = ["01-main-active", "02-settings", "03-stats"]
    phone_shots = "".join(
        f'<figure><img src="{rel}assets/shot-{loc["shots"]}-{f}.png" alt="" width="396" height="860" loading="lazy">'
        f'<figcaption><b>{h}</b>{p}</figcaption></figure>'
        for f, (h, p) in zip(phone_files, loc["phone_caps"])
    )
    free_items = "".join(f"<li>{t}</li>" for t in loc["plan_free"])
    pro_items = "".join(f"<li>{t}</li>" for t in loc["plan_pro"])
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
<meta name="theme-color" media="(prefers-color-scheme: light)" content="#E8EAEE">
<meta name="theme-color" media="(prefers-color-scheme: dark)" content="#16181D">
<link rel="canonical" href="{BASE_URL}{loc['dir']}">
{hreflang_block()}
<link rel="icon" type="image/png" href="{rel}assets/icon-180.png">
<link rel="apple-touch-icon" href="{rel}assets/icon-180.png">
<link rel="stylesheet" href="{rel}assets/style.css?v={CSS_V}">
{font_override}
</head>
<body>

<nav>
  <div class="wrap">
    <a class="wordmark" href="{rel if rel else './'}">
      <img src="{rel}assets/icon-180.png" alt="">
      <span>DeskBreath</span><span class="l2">{loc['brand2']}</span>
    </a>
    <div class="lang">{lang_nav(loc['dir'], rel)}</div>
  </div>
</nav>

<header class="hero">
  <div class="wrap">
    <div>
      <h1>{loc['h1']}</h1>
      <p class="sub">{loc['sub']}</p>
      <div class="cta">{badges(loc, '1')}</div>
      <p class="note">{loc['note']}</p>
    </div>
    <div class="orb-stage">
      <div class="orb-wrap">
        <div class="orb" id="orb"></div>
        <div class="orb-count" id="orbCount">4</div>
      </div>
      <div class="orb-label" id="orbLabel">{loc['orb_in']}</div>
    </div>
  </div>
</header>

<section class="rhythm">
  <div class="wrap">
    <h2>{loc['rhythm_h2']}</h2>
    <div class="bar"><span class="in"></span><span class="out"></span></div>
    <div class="bar-keys"><span>{loc['rhythm_in']}</span><span>{loc['rhythm_out']}</span></div>
    <p class="lede">{loc['rhythm_lede']}</p>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>{loc['mac_h2']}</h2>
    <div class="shelf mac">{mac_shots}</div>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>{loc['phone_h2']}</h2>
    <div class="shelf phone">{phone_shots}</div>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>{loc['plans_h2']}</h2>
    <div class="plans">
      <div class="plan">
        <h3>{loc['plan_free_h']}</h3>
        <p class="price">{loc['plan_free_price']}</p>
        <ul>{free_items}</ul>
      </div>
      <div class="plan pro">
        <h3>{loc['plan_pro_h']}</h3>
        <p class="price">{loc['plan_pro_price']}</p>
        <ul>{pro_items}</ul>
      </div>
    </div>
  </div>
</section>

<section class="final">
  <div class="wrap">
    <h2>{loc['final_h2']}</h2>
    <div class="cta">{badges(loc, '2')}</div>
    <p class="note">{loc['req']}</p>
  </div>
</section>

<footer>
  <div class="wrap">
    <div>© 2026 kkiruk studio</div>
    <div class="f-links">
      <a href="mailto:kkirukstudio.help@gmail.com">{loc['f_contact']}</a>
      <a href="https://kkiruk-studio.github.io/privacy-policy-app/">{loc['f_privacy']}</a>
      <a href="https://kkiruk-studio.github.io/terms-of-service-app/">{loc['f_terms']}</a>
    </div>
  </div>
</footer>

<button class="dock" id="dock" aria-label="{loc['orb_in']} / {loc['orb_out']}" aria-pressed="false">
  <span class="dock-orb" id="dockOrb"></span><span class="dock-count" id="dockCount">4</span>
</button>

<script>
  // 앱과 같은 리듬: 들숨 4초에 커지고, 날숨 6초에 작아진다.
  const labels = {orb_labels_json};
  const orb = document.getElementById("orb");
  const orbCount = document.getElementById("orbCount");
  const orbLabel = document.getElementById("orbLabel");
  const dock = document.getElementById("dock");
  const dockOrb = document.getElementById("dockOrb");
  const dockCount = document.getElementById("dockCount");
  const css = getComputedStyle(document.documentElement);
  const IN = css.getPropertyValue("--inhale").trim();
  const OUT = css.getPropertyValue("--exhale").trim();

  let paused = false;
  dock.addEventListener("click", () => {{
    paused = !paused;
    dock.classList.toggle("paused", paused);
    dock.setAttribute("aria-pressed", String(paused));
  }});

  // 히어로를 지나가면 화면 구석에 도킹해 계속 호흡한다 (맥 플로팅 호흡 원과 같은 동작)
  const hero = document.querySelector(".hero");
  if ("IntersectionObserver" in window) {{
    new IntersectionObserver(
      ([e]) => dock.classList.toggle("on", !e.isIntersecting),
      {{ threshold: 0 }}
    ).observe(hero);
  }}

  if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {{
    const sleep = (ms) => new Promise(r => setTimeout(r, ms));
    const phase = async (n, seconds, scale, color, label) => {{
      orbLabel.textContent = label;
      for (const el of [orb, dockOrb]) {{
        el.style.transition = "transform " + seconds + "s linear, background-color " + seconds + "s linear";
        el.style.transform = "scale(" + scale + ")";
        el.style.backgroundColor = color;
      }}
      const step = seconds * 1000 / (n + 1);
      for (let i = n; i >= 0; i--) {{
        orbCount.textContent = i;
        dockCount.textContent = i;
        await sleep(step);
      }}
    }};
    (async function loop() {{
      for (;;) {{
        while (paused) await sleep(200);
        await phase(4, 4, 1, IN, labels.in);
        while (paused) await sleep(200);
        await phase(6, 6, 0.62, OUT, labels.out);
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
