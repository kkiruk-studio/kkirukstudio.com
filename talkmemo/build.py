#!/usr/bin/env python3
"""Generate index.html for every locale from one template.

Usage: python3 build.py
Output: ./index.html (en), ./ko/index.html, ./ja/index.html
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).parent
BASE_URL = "https://www.kkirukstudio.com/talkmemo/"

APPLE_SVG = '<svg viewBox="0 0 384 512" aria-hidden="true"><path d="M318.7 268.7c-.2-36.7 16.4-64.4 50-84.8-18.8-26.9-47.2-41.7-84.7-44.6-35.5-2.8-74.3 20.7-88.5 20.7-15 0-49.4-19.7-76.4-19.7C63.3 141.2 4 184.8 4 273.5q0 39.3 14.4 81.2c12.8 36.7 59 126.7 107.2 125.2 25.2-.6 43-17.9 75.8-17.9 31.8 0 48.3 17.9 76.4 17.9 48.6-.7 90.4-82.5 102.6-119.3-65.2-30.7-61.7-90-61.7-91.9zm-56.6-164.2c27.3-32.4 24.8-61.9 24-72.5-24.1 1.4-52 16.4-67.9 34.9-17.5 19.8-27.8 44.3-25.6 71.9 26.1 2 49.9-11.4 69.5-34.3z"/></svg>'

LANG_LABELS = [("", "EN"), ("ko/", "한국어"), ("ja/", "日本語")]

LOCALES = {
    "en": {
        "dir": "", "lang": "en", "font": None, "shots": "en",
        "title": "Talk Memo — Speak to your watch, read it on your iPhone",
        "desc": "Tap your Apple Watch, say what's on your mind, and it's on your iPhone as text — transcribed on your device, ready to send to Notion, Bear or Obsidian. No ads, no subscription.",
        "og_title": "Talk Memo — Voice to text, wrist to phone",
        "og_desc": "Tap your watch. Say it. Read it on your phone as text.",
        "kicker_num": "VOICE NOTES, HANDS-FREE",
        "h1": "Got an idea?<br><em>Just say it</em> to your wrist.",
        "pairs": [["MID-RUN", "Build the widget first in the next version."],
                  ["DRIVING", "Pick up milk and eggs on the way home."],
                  ["SHOWER", "Open the talk with a question, not a slide."],
                  ["3 AM", "Order Mia's birthday gift this weekend."]],
        "sub": "Your best ideas show up mid-run, mid-drive, mid-shampoo — exactly when your phone is out of reach. Tap your Apple Watch once and talk. By the time you pick up your iPhone, it's already text.",
        "badge_small": "Download on the", "note": "BUY ONCE · NO SUBSCRIPTION · IPHONE &amp; APPLE WATCH",
        "badge_aria": "Download on the App Store",
        "chips": [["N", "Notion"], ["B", "Bear"], ["O", "Obsidian"], ["S", "Siri"]],
        "hero_alt": "Talk Memo home screen on iPhone showing voice memos transcribed to text",
        "watch_alt": "Talk Memo recording on Apple Watch with a live level meter",
        "marquee": ["MID-RUN", "DRIVING", "IN THE SHOWER", "DOG WALK", "DOING DISHES", "COMMUTE", "AT THE GYM", "LIGHTS OUT"],
        "how_kicker": "HOW IT WORKS",
        "how_h2": "From <em>“oh, that's good”</em> to saved text in three seconds.",
        "steps": [
            ["TAP", "Tap your wrist", "Keep running. One tap on the big red button starts recording — the action button, a watch-face complication or Siri work too."],
            ["TALK", "Say what you're thinking", "No typing, no looking at a screen. Say it like you'd tell a friend, tap stop, and get back to your day."],
            ["READ", "It's text on your iPhone", "Open Talk Memo and it's already written down. Transcription happens on your device — your voice never leaves it."],
        ],
        "mom_kicker": "THE MOMENT", "mom_num": "3 SECONDS",
        "mom_h2": "Reach for your phone, and the idea is <em>already gone</em>.",
        "mom_lede": "Unlock, find the app, start typing — good ideas don't wait that long. Talk Memo cuts the whole dance down to one tap and one sentence.",
        "mom_rows": [
            ["Mid-run", "Build the widget first.", "NO STOPPING"],
            ["Driving", "Milk and eggs on the way home.", "HANDS ON THE WHEEL"],
            ["Shower", "Open the talk with a question.", "WET HANDS OK"],
            ["Lights out", "Order the gift this weekend.", "EYES CLOSED"],
        ],
        "dest_kicker": "EXPORT", "dest_num": "YOUR NOTES APP",
        "dest_h2": "Your words end up <em>where you work</em>.",
        "dest_lede": "Talk Memo doesn't trap your notes. Send them to Notion through a real API connection, to Bear or Obsidian directly, or anywhere else with the share sheet.",
        "provs": [
            ["N", "Notion", "A real API integration — memos land in your database as pages."],
            ["B", "Bear", "One tap creates a new Bear note, ready to edit."],
            ["O", "Obsidian", "Drops straight into your vault as a new note."],
            ["⇪", "Share sheet", "Apple Notes, Messages, anywhere iOS can share."],
        ],
        "shots_kicker": "SCREENS", "shots_num": "WATCH + IPHONE",
        "shots_h2": "Two screens, <em>one flow</em>.",
        "shots_caps": ["ONE TAP TO RECORD", "TEXT, AUTOMATICALLY", "LIGHT &amp; DARK"],
        "feat_kicker": "DETAILS", "feat_num": "06",
        "feat_h2": "Small app. <em>Deliberate</em> choices.",
        "feats": [
            ["On-device transcription", "Speech recognition runs on your iPhone. Your voice is never uploaded anywhere."],
            ["No ads, no tracking", "Zero analytics, zero accounts. The app collects nothing."],
            ["Buy once, keep forever", "One purchase. No subscription, no locked tiers, no nagging."],
            ["iCloud sync", "Memos follow you to your iPad through your own iCloud — not our servers."],
            ["Speaks 3 languages", "Korean, English and Japanese recognition — switch any time."],
            ["Starts from anywhere", "Action button, complication, dock, or “Hey Siri, start recording.”"],
        ],
        "final_h2": "Your next idea deserves better than “I'll remember it.”",
        "final_lede": "Talk Memo for iPhone &amp; Apple Watch.",
        "f_contact": "Contact", "f_privacy": "Privacy", "f_terms": "Terms",
    },
    "ko": {
        "dir": "ko/", "lang": "ko", "font": '"Apple SD Gothic Neo", "Pretendard"', "shots": "ko",
        "title": "토크 메모 — 시계에 대고 말하면, iPhone에 글자로",
        "desc": "Apple Watch 한 번 탭하고 말하면 끝. iPhone에 텍스트로 적혀 있어요. 변환은 전부 기기 안에서, Notion·Bear·Obsidian으로 바로 내보내기. 광고도 구독도 없습니다.",
        "og_title": "토크 메모 — 말하면 글이 되는 손목 메모",
        "og_desc": "시계 탭, 말하기, 끝. 폰에 글자로 적혀 있어요.",
        "kicker_num": "손이 바빠도 메모",
        "h1": "좋은 생각이 떠올랐나요?<br>시계에 대고 <em>말만 하세요</em>",
        "pairs": [["러닝 중", "다음 버전엔 위젯부터 만들자"],
                  ["운전 중", "집에 갈 때 우유랑 달걀 사기"],
                  ["샤워하다가", "발표는 질문으로 시작하자"],
                  ["새벽 3시", "유진이 선물 주말에 주문하기"]],
        "sub": "좋은 생각은 꼭 폰이 멀리 있을 때 떠오르죠. 달리는 중에, 운전 중에, 머리 감다가. Apple Watch를 한 번 탭하고 말하면 — iPhone을 집어 들 때쯤엔 이미 글자가 되어 있어요.",
        "badge_small": "다운로드는", "note": "한 번 결제 · 구독 없음 · iPhone &amp; Apple Watch",
        "badge_aria": "App Store에서 다운로드",
        "chips": [["N", "Notion"], ["B", "Bear"], ["O", "Obsidian"], ["S", "Siri"]],
        "hero_alt": "토크 메모 iPhone 홈 화면 — 음성 메모가 텍스트로 변환되어 정리된 모습",
        "watch_alt": "Apple Watch에서 토크 메모 녹음 중 — 실시간 레벨 미터",
        "marquee": ["러닝 중", "운전 중", "샤워하다가", "강아지 산책", "설거지 중", "출근길", "운동 중", "불 끄고 누워서"],
        "how_kicker": "사용 방법",
        "how_h2": "\"아, 이거 좋다\"에서 <em>저장까지 3초</em>.",
        "steps": [
            ["탭", "손목을 한 번 탭", "뛰던 걸음 그대로. 큰 빨간 버튼 하나면 녹음 시작 — 액션 버튼, 콤플리케이션, Siri로도 시작돼요."],
            ["말", "생각을 그대로 말하기", "타이핑도, 화면 볼 필요도 없어요. 친구한테 말하듯 말하고 정지를 누르면 끝."],
            ["글", "iPhone에 글자로", "토크 메모를 열면 이미 적혀 있어요. 변환은 전부 iPhone 안에서 — 목소리는 어디로도 나가지 않아요."],
        ],
        "mom_kicker": "그 순간", "mom_num": "3초",
        "mom_h2": "폰을 꺼내는 순간, 생각은 <em>벌써 도망가요</em>.",
        "mom_lede": "잠금 풀고, 앱 찾고, 타이핑하는 동안 좋은 생각은 기다려주지 않아요. 토크 메모는 그 전부를 탭 한 번과 한 문장으로 줄였어요.",
        "mom_rows": [
            ["러닝 중", "다음 버전엔 위젯부터 만들자", "멈추지 않아도"],
            ["운전 중", "우유랑 달걀 사 가기", "손은 핸들에"],
            ["샤워하다가", "발표는 질문으로 시작하자", "젖은 손 OK"],
            ["불 끄고 누워서", "선물 주말에 주문하기", "눈 감은 채로"],
        ],
        "dest_kicker": "내보내기", "dest_num": "내 노트 앱으로",
        "dest_h2": "메모는 <em>내가 쓰는 노트 앱</em>으로.",
        "dest_lede": "토크 메모에 가둬두지 않아요. Notion은 진짜 API로 데이터베이스에 바로, Bear·Obsidian은 한 탭에, 나머지는 공유 시트로 어디든.",
        "provs": [
            ["N", "Notion", "진짜 API 연동 — 내 데이터베이스에 페이지로 바로 들어가요."],
            ["B", "Bear", "한 탭이면 Bear 새 노트로."],
            ["O", "Obsidian", "내 vault에 새 노트로 쏙."],
            ["⇪", "공유 시트", "Apple 메모, 카카오톡, 메시지 — iOS가 보낼 수 있는 곳 어디든."],
        ],
        "shots_kicker": "화면", "shots_num": "WATCH + IPHONE",
        "shots_h2": "워치와 아이폰, <em>한 흐름</em>.",
        "shots_caps": ["한 탭이면 녹음", "글자는 자동으로", "라이트 &amp; 다크"],
        "feat_kicker": "디테일", "feat_num": "06",
        "feat_h2": "작은 앱, <em>분명한 선택</em>.",
        "feats": [
            ["기기 안에서 변환", "음성 인식이 iPhone 안에서 돌아가요. 목소리가 서버로 올라가지 않아요."],
            ["광고·추적 없음", "분석도 계정도 없어요. 앱이 수집하는 데이터 0."],
            ["한 번 결제, 평생", "구독 없음, 잠금 해제 등급 없음, 결제 유도 없음."],
            ["iCloud 동기화", "메모가 내 iCloud로 iPad까지 따라와요. 우리 서버가 아니라요."],
            ["3개 언어 인식", "한국어·영어·일본어 음성 인식 — 언제든 전환."],
            ["어디서든 시작", "액션 버튼, 콤플리케이션, 도크, \"시리야, 녹음 시작\"까지."],
        ],
        "final_h2": "다음 아이디어는 \"기억해야지\"에 맡기지 마세요.",
        "final_lede": "iPhone &amp; Apple Watch용 토크 메모.",
        "f_contact": "문의", "f_privacy": "개인정보 처리방침", "f_terms": "이용약관",
    },
    "ja": {
        "dir": "ja/", "lang": "ja", "font": '"Hiragino Kaku Gothic ProN", "Hiragino Sans", "Yu Gothic"', "shots": "ja",
        "title": "トークメモ — 腕時計に話すだけ、iPhone に文字で",
        "desc": "Apple Watch をタップして話すだけ。iPhone にテキストとして残ります。変換はすべて端末内、Notion・Bear・Obsidian へすぐ書き出し。広告もサブスクもありません。",
        "og_title": "トークメモ — 話せば文字になる手首のメモ",
        "og_desc": "時計をタップ、話す、おわり。iPhone に文字で残ります。",
        "kicker_num": "手がふさがっていてもメモ",
        "h1": "ひらめいた？<br>手首に<em>話すだけ</em>。",
        "pairs": [["ランニング中", "次のバージョンはウィジェットから作ろう"],
                  ["運転中", "帰りに牛乳と卵を買う"],
                  ["シャワー中", "プレゼンは質問から始めよう"],
                  ["夜中の3時", "ユイのプレゼントを週末に注文"]],
        "sub": "いいアイデアは、スマホが手元にない時に限ってやってきます。走っている時、運転中、シャンプー中。Apple Watch を一度タップして話せば — iPhone を手に取る頃には、もう文字になっています。",
        "badge_small": "ダウンロードは", "note": "買い切り · サブスクなし · iPhone &amp; Apple Watch",
        "badge_aria": "App Store でダウンロード",
        "chips": [["N", "Notion"], ["B", "Bear"], ["O", "Obsidian"], ["S", "Siri"]],
        "hero_alt": "iPhone のトークメモのホーム画面 — 音声メモがテキストに変換され整理された様子",
        "watch_alt": "Apple Watch のトークメモで録音中 — リアルタイムレベルメーター",
        "marquee": ["ランニング中", "運転中", "シャワー中", "犬の散歩", "皿洗い中", "通勤中", "ジムで", "寝る前"],
        "how_kicker": "使い方",
        "how_h2": "「あ、それいい」から<em>保存まで3秒</em>。",
        "steps": [
            ["タップ", "手首を一度タップ", "走ったまま。大きな赤いボタンひとつで録音開始 — アクションボタンやコンプリケーション、Siri からでも。"],
            ["話す", "思ったことをそのまま", "入力も、画面を見る必要もなし。友達に話すように話して、停止を押すだけ。"],
            ["文字", "iPhone に文字で", "トークメモを開けば、もう書いてあります。変換はすべて iPhone の中 — 声はどこにも送られません。"],
        ],
        "mom_kicker": "その瞬間", "mom_num": "3秒",
        "mom_h2": "スマホを取り出した瞬間、ひらめきは<em>もう逃げています</em>。",
        "mom_lede": "ロック解除、アプリ探し、入力 — いいアイデアはそんなに待ってくれません。トークメモはその全部を、タップ一回とひと言に縮めました。",
        "mom_rows": [
            ["ランニング中", "ウィジェットから作ろう", "止まらなくていい"],
            ["運転中", "牛乳と卵を買って帰る", "手はハンドルに"],
            ["シャワー中", "プレゼンは質問から", "濡れた手でもOK"],
            ["寝る前", "プレゼントを週末に注文", "目を閉じたまま"],
        ],
        "dest_kicker": "書き出し", "dest_num": "いつものノートへ",
        "dest_h2": "メモは<em>いつものノートアプリ</em>へ。",
        "dest_lede": "トークメモに閉じ込めません。Notion は本物の API でデータベースへ直接、Bear・Obsidian はワンタップ、それ以外は共有シートでどこへでも。",
        "provs": [
            ["N", "Notion", "本物の API 連携 — あなたのデータベースにページとして直接入ります。"],
            ["B", "Bear", "ワンタップで Bear の新規ノートに。"],
            ["O", "Obsidian", "あなたの vault に新しいノートとして。"],
            ["⇪", "共有シート", "Apple メモ、LINE、メッセージ — iOS が共有できる場所ならどこへでも。"],
        ],
        "shots_kicker": "画面", "shots_num": "WATCH + IPHONE",
        "shots_h2": "Watch と iPhone、<em>ひとつの流れ</em>。",
        "shots_caps": ["ワンタップで録音", "文字は自動で", "ライト &amp; ダーク"],
        "feat_kicker": "こだわり", "feat_num": "06",
        "feat_h2": "小さなアプリ、<em>明確な選択</em>。",
        "feats": [
            ["端末内で変換", "音声認識は iPhone の中で完結。声がサーバーに送られることはありません。"],
            ["広告・トラッキングなし", "分析もアカウントも不要。アプリが集めるデータはゼロ。"],
            ["買い切り、ずっと使える", "サブスクなし、機能制限なし、課金の催促なし。"],
            ["iCloud 同期", "メモはあなたの iCloud で iPad にも同期。当社サーバーは使いません。"],
            ["3言語の音声認識", "日本語・英語・韓国語 — いつでも切り替え可能。"],
            ["どこからでも開始", "アクションボタン、コンプリケーション、Dock、「Hey Siri、録音開始」。"],
        ],
        "final_h2": "次のひらめきを「覚えておこう」に任せないで。",
        "final_lede": "iPhone &amp; Apple Watch のトークメモ。",
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
    return (f'<a class="store-badge" id="{el_id}" href="#" aria-label="{loc["badge_aria"]}">{APPLE_SVG}'
            f'<span class="txt"><small>{loc["badge_small"]}</small><strong>App Store</strong></span></a>')


def render(key):
    loc = LOCALES[key]
    rel = "../" if loc["dir"] else ""
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
    moments = "".join(
        f'<div class="moment-row"><span class="who">{a}</span><span class="arrow">→</span><span class="to">“{b}”</span><span class="cat">{c}</span></div>'
        for a, b, c in loc["mom_rows"]
    )
    provs = "".join(
        f'<div class="prov"><span class="g">{g}</span><h3>{name}</h3><p>{p}</p></div>'
        for g, name, p in loc["provs"]
    )
    shots = (
        f'<figure><div class="watch"><img src="{rel}assets/watch-rec.png" alt="{loc["watch_alt"]}" loading="lazy"></div>'
        f'<figcaption>{loc["shots_caps"][0]}</figcaption></figure>'
        f'<figure><div class="phone"><img src="{rel}assets/shot-{loc["shots"]}-home-dark.png" alt="{loc["hero_alt"]}" loading="lazy"><div class="island"></div></div>'
        f'<figcaption>{loc["shots_caps"][1]}</figcaption></figure>'
        f'<figure><div class="phone"><img src="{rel}assets/shot-{loc["shots"]}-home-light.png" alt="{loc["hero_alt"]}" loading="lazy"><div class="island"></div></div>'
        f'<figcaption>{loc["shots_caps"][2]}</figcaption></figure>'
    )
    feats = "".join(f'<div class="feat"><h3>{h}</h3><p>{p}</p></div>' for h, p in loc["feats"])
    pairs_json = json.dumps(loc["pairs"], ensure_ascii=False)

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
    <a class="wordmark" href="{rel if rel else './'}"><img src="{rel}assets/icon-180.png" alt=""><span>TALK·MEMO</span></a>
    <div class="lang">{lang_nav(loc['dir'], rel)}</div>
  </div>
</nav>

<header class="hero">
  <div class="ghost">T·M</div>
  <div class="wrap">
    <div>
      <div class="kicker"><span>TALK · MEMO</span><span class="rule"></span><span class="num">{loc['kicker_num']}</span></div>
      <h1>{loc['h1']}</h1>
      <div class="demo">
        <span class="ctx" id="demoCtx">{loc['pairs'][0][0]}</span>
        <span class="rec"><span class="dot"></span><span class="bars"><i></i><i></i><i></i><i></i><i></i></span></span>
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
      <div class="phone"><img src="{rel}assets/shot-{loc['shots']}-home-dark.png" alt="{loc['hero_alt']}"><div class="island"></div></div>
      <div class="watch"><img src="{rel}assets/watch-rec.png" alt="{loc['watch_alt']}"></div>
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
    <div class="kicker"><span>{loc['mom_kicker']}</span><span class="rule"></span><span class="num">{loc['mom_num']}</span></div>
    <h2>{loc['mom_h2']}</h2>
    <p class="lede">{loc['mom_lede']}</p>
    <div class="moment-table">{moments}</div>
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap">
    <div class="kicker"><span>{loc['dest_kicker']}</span><span class="rule"></span><span class="num">{loc['dest_num']}</span></div>
    <h2>{loc['dest_h2']}</h2>
    <p class="lede">{loc['dest_lede']}</p>
    <div class="providers">{provs}</div>
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
  const APP_STORE_URL = "https://apps.apple.com/app/id6764329223";
  if (APP_STORE_URL) {{
    document.getElementById("storeLink").href = APP_STORE_URL;
    document.getElementById("storeLink2").href = APP_STORE_URL;
  }}

  const pairs = {pairs_json};
  const ctxEl = document.getElementById("demoCtx");
  const dstEl = document.getElementById("demoDst");
  if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {{
    let i = 0;
    const sleep = (ms) => new Promise(r => setTimeout(r, ms));
    (async function loop() {{
      for (;;) {{
        const [ctx, text] = pairs[i % pairs.length];
        ctxEl.textContent = ctx;
        dstEl.textContent = "";
        await sleep(500);
        for (const ch of text) {{ dstEl.textContent += ch; await sleep(45); }}
        await sleep(2400);
        i++;
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
