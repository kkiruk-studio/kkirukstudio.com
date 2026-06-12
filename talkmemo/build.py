#!/usr/bin/env python3
"""Generate index.html for every locale from one template.

Usage: python3 build.py
Output: ./index.html (en), ./ko/index.html, ./ja/index.html
"""
import json
import math
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
        "rec_label": "REC", "rec_text": "VOICE NOTES, <em>HANDS-FREE</em>",
        "h1": "Got an idea?<br><em>Just say it</em> to your wrist.",
        "demo_time": "09:41",
        "pairs": [["MID-RUN", "Build the widget first in the next version."],
                  ["DRIVING", "Pick up milk and eggs on the way home."],
                  ["SHOWER", "Open the talk with a question, not a slide."],
                  ["3 AM", "Order Mia's birthday gift this weekend."]],
        "sub": "Your best ideas show up mid-run, mid-drive, mid-shampoo — exactly when your phone is out of reach. Tap your Apple Watch once and talk. By the time you pick up your iPhone, it's already text.",
        "badge_small": "Download on the", "note": "BUY ONCE · NO SUBSCRIPTION · IPHONE &amp; APPLE WATCH",
        "badge_aria": "Download on the App Store",
        "chips": ["Notion", "Bear", "Obsidian", "Siri"],
        "hero_alt": "Talk Memo home screen on iPhone showing voice memos transcribed to text",
        "watch_alt": "Talk Memo recording on Apple Watch with a live level meter",
        "how_label": "HOW IT WORKS",
        "how_h2": "From a thought in your head to saved text, in <em>three seconds</em>.",
        "steps": [
            ["0:00", "Tap your wrist", "Keep running. One tap on the big red button starts recording — the action button, a watch-face complication or Siri work too."],
            ["0:03", "Say what you're thinking", "No typing, no looking at a screen. Say it like you'd tell a friend, then tap stop."],
            ["0:04", "It's text on your iPhone", "Open Talk Memo and it's already written down. Transcription happens on your device — your voice never leaves it."],
        ],
        "mom_label": "ONE DAY WITH TALK MEMO",
        "mom_h2": "Reach for your phone, and the idea is <em>already gone</em>.",
        "mom_lede": "Unlock, find the app, start typing — good ideas don't wait that long. Talk Memo cuts the whole dance down to one tap and one sentence. A day's worth of passing thoughts, all kept:",
        "mom_day": "TODAY",
        "mom_rows": [
            ["07:12", "Build the widget first in the next version.", "MID-RUN", None],
            ["08:45", "Milk and eggs on the way home.", "DRIVING", None],
            ["21:03", "Open the talk with a question, not a slide.", "SHOWER", "Notion"],
            ["23:58", "Order Mia's birthday gift this weekend.", "LIGHTS OUT", None],
        ],
        "dest_label": "EXPORT",
        "dest_h2": "Your words end up <em>where you work</em>.",
        "dest_lede": "Talk Memo doesn't trap your notes. One tap on a memo opens the export sheet — exactly like this one:",
        "sheet_title": "Export memo",
        "provs": [
            ["N", "Notion", "A real API integration — memos land in your database as pages."],
            ["B", "Bear", "One tap creates a new Bear note, ready to edit."],
            ["O", "Obsidian", "Drops straight into your vault as a new note."],
            ["⇪", "Share sheet", "Apple Notes, Messages, anywhere iOS can share."],
        ],
        "shots_label": "SCREENS",
        "shots_h2": "Two screens, <em>one flow</em>.",
        "shots_caps": ["ONE TAP TO RECORD", "TEXT, AUTOMATICALLY", "LIGHT &amp; DARK"],
        "feat_label": "DETAILS",
        "feat_h2": "Small app. <em>Deliberate</em> choices.",
        "feat_groups": [
            ["PRIVACY", [
                ["On-device transcription", "Speech recognition runs on your iPhone. Your voice is never uploaded anywhere."],
                ["No ads, no tracking", "Zero analytics, zero accounts. The app collects nothing."],
                ["Buy once, keep forever", "One purchase. No subscription, no locked tiers, no nagging."],
            ]],
            ["EVERYDAY", [
                ["iCloud sync", "Memos follow you to your iPad through your own iCloud — not our servers."],
                ["Speaks 3 languages", "Korean, English and Japanese recognition — switch any time."],
                ["Starts from anywhere", "Action button, complication, dock, or “Hey Siri, start recording.”"],
            ]],
        ],
        "final_cap": "TAP TO START",
        "final_h2": "Your next idea deserves better than “I'll remember it.”",
        "final_lede": "Talk Memo for iPhone &amp; Apple Watch.",
        "final_aria": "Download Talk Memo on the App Store",
        "f_contact": "Contact", "f_privacy": "Privacy", "f_terms": "Terms",
    },
    "ko": {
        "dir": "ko/", "lang": "ko", "font": '"Apple SD Gothic Neo", "Pretendard"', "shots": "ko",
        "title": "토크 메모 — 시계에 대고 말하면, iPhone에 글자로",
        "desc": "Apple Watch 한 번 탭하고 말하면 끝. iPhone에 텍스트로 적혀 있어요. 변환은 전부 기기 안에서, Notion·Bear·Obsidian으로 바로 내보내기. 광고도 구독도 없습니다.",
        "og_title": "토크 메모 — 말하면 글이 되는 손목 메모",
        "og_desc": "시계 탭, 말하기, 끝. 폰에 글자로 적혀 있어요.",
        "rec_label": "REC", "rec_text": "손이 바빠도 <em>메모</em>",
        "h1": "좋은 생각이 떠올랐나요?<br>시계에 대고 <em>말만 하세요</em>",
        "demo_time": "09:41",
        "pairs": [["러닝 중", "다음 버전엔 위젯부터 만들자"],
                  ["운전 중", "집에 갈 때 우유랑 달걀 사기"],
                  ["샤워하다가", "발표는 질문으로 시작하자"],
                  ["새벽 3시", "경은이 선물 주말에 주문하기"]],
        "sub": "좋은 생각은 꼭 폰이 멀리 있을 때 떠오르죠. 달리는 중에, 운전 중에, 머리 감다가. Apple Watch를 한 번 탭하고 말하면 — iPhone을 집어 들 때쯤엔 이미 글자가 되어 있어요.",
        "badge_small": "다운로드는", "note": "한 번 결제 · 구독 없음 · iPhone &amp; Apple Watch",
        "badge_aria": "App Store에서 다운로드",
        "chips": ["Notion", "Bear", "Obsidian", "Siri"],
        "hero_alt": "토크 메모 iPhone 홈 화면 — 음성 메모가 텍스트로 변환되어 정리된 모습",
        "watch_alt": "Apple Watch에서 토크 메모 녹음 중 — 실시간 레벨 미터",
        "how_label": "사용 방법",
        "how_h2": "떠오른 생각이 글이 되기까지, <em>딱 3초</em>.",
        "steps": [
            ["0:00", "손목을 한 번 탭", "뛰던 걸음 그대로. 큰 빨간 버튼 하나면 녹음 시작 — 액션 버튼, 콤플리케이션, Siri로도 시작돼요."],
            ["0:03", "생각을 그대로 말하기", "타이핑도, 화면 볼 필요도 없어요. 친구한테 말하듯 말하고 정지를 누르면 끝."],
            ["0:04", "iPhone에 글자로", "토크 메모를 열면 이미 적혀 있어요. 변환은 전부 iPhone 안에서 — 목소리는 어디로도 나가지 않아요."],
        ],
        "mom_label": "토크 메모와 하루",
        "mom_h2": "폰을 꺼내는 순간, 생각은 <em>벌써 도망가요</em>.",
        "mom_lede": "잠금 풀고, 앱 찾고, 타이핑하는 동안 좋은 생각은 기다려주지 않아요. 토크 메모는 그 전부를 탭 한 번과 한 문장으로 줄였어요. 하루 동안 스쳐 간 생각들이 이렇게 남아요:",
        "mom_day": "오늘",
        "mom_rows": [
            ["07:12", "다음 버전엔 위젯부터 만들자", "러닝 중", None],
            ["08:45", "집에 갈 때 우유랑 달걀 사기", "운전 중", None],
            ["21:03", "발표는 질문으로 시작하자", "샤워하다가", "Notion"],
            ["23:58", "경은이 선물 주말에 주문하기", "불 끄고 누워서", None],
        ],
        "dest_label": "내보내기",
        "dest_h2": "메모는 <em>내가 쓰는 노트 앱</em>으로.",
        "dest_lede": "토크 메모에 가둬두지 않아요. 메모를 한 번 탭하면 내보내기 시트가 열려요 — 바로 이렇게:",
        "sheet_title": "메모 내보내기",
        "provs": [
            ["N", "Notion", "진짜 API 연동 — 내 데이터베이스에 페이지로 바로 들어가요."],
            ["B", "Bear", "한 탭이면 Bear 새 노트로."],
            ["O", "Obsidian", "내 vault에 새 노트로 쏙."],
            ["⇪", "공유 시트", "Apple 메모, 카카오톡, 메시지 — iOS가 보낼 수 있는 곳 어디든."],
        ],
        "shots_label": "화면",
        "shots_h2": "워치와 아이폰, <em>한 흐름</em>.",
        "shots_caps": ["한 탭이면 녹음", "글자는 자동으로", "라이트 &amp; 다크"],
        "feat_label": "디테일",
        "feat_h2": "작은 앱, <em>분명한 선택</em>.",
        "feat_groups": [
            ["프라이버시", [
                ["기기 안에서 변환", "음성 인식이 iPhone 안에서 돌아가요. 목소리가 서버로 올라가지 않아요."],
                ["광고·추적 없음", "분석도 계정도 없어요. 앱이 수집하는 데이터 0."],
                ["한 번 결제, 평생", "구독 없음, 잠금 해제 등급 없음, 결제 유도 없음."],
            ]],
            ["일상", [
                ["iCloud 동기화", "메모가 내 iCloud로 iPad까지 따라와요. 우리 서버가 아니라요."],
                ["3개 언어 인식", "한국어·영어·일본어 음성 인식 — 언제든 전환."],
                ["어디서든 시작", "액션 버튼, 콤플리케이션, 도크, \"시리야, 녹음 시작\"까지."],
            ]],
        ],
        "final_cap": "탭해서 시작",
        "final_h2": "다음 아이디어는 \"기억해야지\"에 맡기지 마세요.",
        "final_lede": "iPhone &amp; Apple Watch용 토크 메모.",
        "final_aria": "App Store에서 토크 메모 다운로드",
        "f_contact": "문의", "f_privacy": "개인정보 처리방침", "f_terms": "이용약관",
    },
    "ja": {
        "dir": "ja/", "lang": "ja", "font": '"Hiragino Kaku Gothic ProN", "Hiragino Sans", "Yu Gothic"', "shots": "ja",
        "title": "トークメモ — 腕時計に話すだけ、iPhone に文字で",
        "desc": "Apple Watch をタップして話すだけ。iPhone にテキストとして残ります。変換はすべて端末内、Notion・Bear・Obsidian へすぐ書き出し。広告もサブスクもありません。",
        "og_title": "トークメモ — 話せば文字になる手首のメモ",
        "og_desc": "時計をタップ、話す、おわり。iPhone に文字で残ります。",
        "rec_label": "REC", "rec_text": "手がふさがっていても<em>メモ</em>",
        "h1": "ひらめいた？<br>手首に<em>話すだけ</em>。",
        "demo_time": "09:41",
        "pairs": [["ランニング中", "次のバージョンはウィジェットから作ろう"],
                  ["運転中", "帰りに牛乳と卵を買う"],
                  ["シャワー中", "プレゼンは質問から始めよう"],
                  ["夜中の3時", "ユイのプレゼントを週末に注文"]],
        "sub": "いいアイデアは、スマホが手元にない時に限ってやってきます。走っている時、運転中、シャンプー中。Apple Watch を一度タップして話せば — iPhone を手に取る頃には、もう文字になっています。",
        "badge_small": "ダウンロードは", "note": "買い切り · サブスクなし · iPhone &amp; Apple Watch",
        "badge_aria": "App Store でダウンロード",
        "chips": ["Notion", "Bear", "Obsidian", "Siri"],
        "hero_alt": "iPhone のトークメモのホーム画面 — 音声メモがテキストに変換され整理された様子",
        "watch_alt": "Apple Watch のトークメモで録音中 — リアルタイムレベルメーター",
        "how_label": "使い方",
        "how_h2": "頭に浮かんでから保存まで、<em>たった3秒</em>。",
        "steps": [
            ["0:00", "手首を一度タップ", "走ったまま。大きな赤いボタンひとつで録音開始 — アクションボタンやコンプリケーション、Siri からでも。"],
            ["0:03", "思ったことをそのまま", "入力も、画面を見る必要もなし。友達に話すように話して、停止を押すだけ。"],
            ["0:04", "iPhone に文字で", "トークメモを開けば、もう書いてあります。変換はすべて iPhone の中 — 声はどこにも送られません。"],
        ],
        "mom_label": "トークメモのある一日",
        "mom_h2": "スマホを取り出した瞬間、ひらめきは<em>もう逃げています</em>。",
        "mom_lede": "ロック解除、アプリ探し、入力 — いいアイデアはそんなに待ってくれません。トークメモはその全部を、タップ一回とひと言に縮めました。一日の思いつきが、こんなふうに残ります:",
        "mom_day": "今日",
        "mom_rows": [
            ["07:12", "次のバージョンはウィジェットから作ろう", "ランニング中", None],
            ["08:45", "帰りに牛乳と卵を買う", "運転中", None],
            ["21:03", "プレゼンは質問から始めよう", "シャワー中", "Notion"],
            ["23:58", "ユイのプレゼントを週末に注文", "寝る前", None],
        ],
        "dest_label": "書き出し",
        "dest_h2": "メモは<em>いつものノートアプリ</em>へ。",
        "dest_lede": "トークメモに閉じ込めません。メモを一度タップすると書き出しシートが開きます — まさにこんなふうに:",
        "sheet_title": "メモを書き出す",
        "provs": [
            ["N", "Notion", "本物の API 連携 — あなたのデータベースにページとして直接入ります。"],
            ["B", "Bear", "ワンタップで Bear の新規ノートに。"],
            ["O", "Obsidian", "あなたの vault に新しいノートとして。"],
            ["⇪", "共有シート", "Apple メモ、LINE、メッセージ — iOS が共有できる場所ならどこへでも。"],
        ],
        "shots_label": "画面",
        "shots_h2": "Watch と iPhone、<em>ひとつの流れ</em>。",
        "shots_caps": ["ワンタップで録音", "文字は自動で", "ライト &amp; ダーク"],
        "feat_label": "こだわり",
        "feat_h2": "小さなアプリ、<em>明確な選択</em>。",
        "feat_groups": [
            ["プライバシー", [
                ["端末内で変換", "音声認識は iPhone の中で完結。声がサーバーに送られることはありません。"],
                ["広告・トラッキングなし", "分析もアカウントも不要。アプリが集めるデータはゼロ。"],
                ["買い切り、ずっと使える", "サブスクなし、機能制限なし、課金の催促なし。"],
            ]],
            ["毎日のために", [
                ["iCloud 同期", "メモはあなたの iCloud で iPad にも同期。当社サーバーは使いません。"],
                ["3言語の音声認識", "日本語・英語・韓国語 — いつでも切り替え可能。"],
                ["どこからでも開始", "アクションボタン、コンプリケーション、Dock、「Hey Siri、録音開始」。"],
            ]],
        ],
        "final_cap": "タップして開始",
        "final_h2": "次のひらめきを「覚えておこう」に任せないで。",
        "final_lede": "iPhone &amp; Apple Watch のトークメモ。",
        "final_aria": "App Store でトークメモをダウンロード",
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


def sec_head(stamp, label):
    return (f'<div class="sec-head"><span class="stamp"><span class="rdot"></span>{stamp}</span>'
            f'<span class="label">{label}</span><span class="line"></span></div>')


def wave_strip(n=56):
    bars = []
    for i in range(n):
        h = round(abs(math.sin(i * 0.55)) * 26 + abs(math.sin(i * 1.7)) * 10 + 6)
        d = round((i % 7) * 0.13, 2)
        bars.append(f'<i style="height:{h}px;animation-delay:{d}s"></i>')
    return f'<div class="wave-strip" aria-hidden="true">{"".join(bars)}</div>'


def render(key):
    loc = LOCALES[key]
    rel = "../" if loc["dir"] else ""
    font_override = f'<style>body{{font-family:-apple-system,BlinkMacSystemFont,{loc["font"]},"Segoe UI",sans-serif}}</style>' if loc["font"] else ""
    chips = "".join(
        f'<div class="chip c{i+1}"><span class="pt"></span>{label}</div>'
        for i, label in enumerate(loc["chips"])
    )
    talk_bars = "".join(f'<i style="height:{h}px;animation-delay:{d}s"></i>'
                        for h, d in [(18, 0), (34, .12), (52, .24), (40, .36), (60, .48),
                                     (30, .6), (46, .72), (22, .84), (38, .96), (54, .3), (28, .54), (14, .18)])
    steps_html = []
    vizzes = [
        '<div class="mini-watch"><span class="rbtn"></span></div>',
        f'<div class="talk-wave">{talk_bars}</div>',
        f'<div class="text-mini"><span class="tm-time">{loc["demo_time"]}</span><span class="tm-line w1"></span><span class="tm-line w2"></span><span class="tm-line w3"></span></div>',
    ]
    for i, (stamp, h, p) in enumerate(loc["steps"]):
        steps_html.append(f'<div class="stage"><span class="stamp-sm">{stamp}</span>'
                          f'<div class="viz">{vizzes[i]}</div><h3>{h}</h3><p>{p}</p></div>')
        if i < 2:
            steps_html.append('<div class="flow">→</div>')
    pipeline = "".join(steps_html)

    mrows = []
    for time, text, tag, exp in loc["mom_rows"]:
        expc = f'<br><span class="exp">{exp}</span>' if exp else ""
        mrows.append(f'<div class="mrow"><span class="time">{time}</span>'
                     f'<span class="txt">{text}{expc}</span><span class="tag">{tag}</span></div>')
    applist = f'<div class="applist"><div class="day">{loc["mom_day"]}</div>{"".join(mrows)}</div>'

    srows = "".join(
        f'<div class="srow s{i+1}"><span class="sicon">{g}</span>'
        f'<div class="body"><h3>{name}</h3><p>{p}</p></div><span class="chev">→</span></div>'
        for i, (g, name, p) in enumerate(loc["provs"])
    )
    sheet = f'<div class="sheet"><div class="grab"></div><div class="sheet-title">{loc["sheet_title"]}</div>{srows}</div>'

    shots = (
        f'<figure><div class="watch"><img src="{rel}assets/watch-rec.png" alt="{loc["watch_alt"]}" loading="lazy"></div>'
        f'<figcaption>{loc["shots_caps"][0]}</figcaption></figure>'
        f'<figure><div class="phone"><img src="{rel}assets/shot-{loc["shots"]}-home-dark.png" alt="{loc["hero_alt"]}" loading="lazy"><div class="island"></div></div>'
        f'<figcaption>{loc["shots_caps"][1]}</figcaption></figure>'
        f'<figure><div class="phone"><img src="{rel}assets/shot-{loc["shots"]}-home-light.png" alt="{loc["hero_alt"]}" loading="lazy"><div class="island"></div></div>'
        f'<figcaption>{loc["shots_caps"][2]}</figcaption></figure>'
    )

    set_cards = "".join(
        '<div class="set-card"><div class="set-title">%s</div>%s</div>'
        % (title, "".join(f'<div class="frow"><span class="check">✓</span><div><h3>{h}</h3><p>{p}</p></div></div>'
                          for h, p in rows))
        for title, rows in loc["feat_groups"]
    )

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
<script src="/ga.js"></script>
</head>
<body>

<nav>
  <div class="wrap">
    <a class="wordmark" href="{rel if rel else './'}"><img src="{rel}assets/icon-180.png" alt=""><span>TALK·MEMO</span></a>
    <div class="lang">{lang_nav(loc['dir'], rel)}</div>
  </div>
</nav>

<header class="hero">
  <div class="wrap">
    <div>
      <div class="rec-pill"><span class="rdot"></span><span class="rec">{loc['rec_label']}</span><span>{loc['rec_text']}</span></div>
      <h1>{loc['h1']}</h1>
      <div class="demo-card">
        <div class="dhead"><span class="dtime">{loc['demo_time']}</span><span class="ctx" id="demoCtx">{loc['pairs'][0][0]}</span></div>
        <div class="dtext"><span id="demoDst">{loc['pairs'][0][1]}</span></div>
        <div class="dfoot"><span class="rdot"></span><span class="bars"><i></i><i></i><i></i><i></i><i></i></span><span class="dstamp">TALK MEMO</span></div>
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

{wave_strip()}

<section>
  <div class="wrap">
    {sec_head("00:01", loc['how_label'])}
    <h2>{loc['how_h2']}</h2>
    <div class="pipeline">{pipeline}</div>
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap">
    {sec_head("00:02", loc['mom_label'])}
    <h2>{loc['mom_h2']}</h2>
    <p class="lede">{loc['mom_lede']}</p>
    {applist}
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap">
    {sec_head("00:03", loc['dest_label'])}
    <h2>{loc['dest_h2']}</h2>
    <p class="lede">{loc['dest_lede']}</p>
    {sheet}
  </div>
</section>

<section class="shots">
  <div class="wrap">
    {sec_head("00:04", loc['shots_label'])}
    <h2>{loc['shots_h2']}</h2>
    <div class="row">{shots}</div>
  </div>
</section>

<section>
  <div class="wrap">
    {sec_head("00:05", loc['feat_label'])}
    <h2>{loc['feat_h2']}</h2>
    <div class="set-grid">{set_cards}</div>
  </div>
</section>

<section class="final">
  <div class="wrap">
    <a class="record-btn" id="storeLink2" href="#" aria-label="{loc['final_aria']}"><span></span></a>
    <div class="cap">{loc['final_cap']}</div>
    <h2>{loc['final_h2']}</h2>
    <p class="lede">{loc['final_lede']}</p>
    <div class="cta">{badge(loc, 'storeLink3')}</div>
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
    for (const id of ["storeLink", "storeLink2", "storeLink3"]) {{
      const el = document.getElementById(id);
      if (el) el.href = APP_STORE_URL;
    }}
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
