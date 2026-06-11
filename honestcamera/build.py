#!/usr/bin/env python3
"""Generate Honest Camera landing pages (flat files) from one template.

Usage: python3 build.py
Output: ./index.html (en), ./ko.html, ./ja.html, ./zh-hant.html

Flat filenames are load-bearing: App Store Connect marketing/support URLs
point at /honestcamera/ko.html etc. Do not switch to subdirectories.
"""
import pathlib

ROOT = pathlib.Path(__file__).parent
BASE_URL = "https://www.kkirukstudio.com/honestcamera/"
APP_STORE_URL = "https://apps.apple.com/app/id6766827649"

APPLE_SVG = '<svg viewBox="0 0 384 512" aria-hidden="true"><path d="M318.7 268.7c-.2-36.7 16.4-64.4 50-84.8-18.8-26.9-47.2-41.7-84.7-44.6-35.5-2.8-74.3 20.7-88.5 20.7-15 0-49.4-19.7-76.4-19.7C63.3 141.2 4 184.8 4 273.5q0 39.3 14.4 81.2c12.8 36.7 59 126.7 107.2 125.2 25.2-.6 43-17.9 75.8-17.9 31.8 0 48.3 17.9 76.4 17.9 48.6-.7 90.4-82.5 102.6-119.3-65.2-30.7-61.7-90-61.7-91.9zm-56.6-164.2c27.3-32.4 24.8-61.9 24-72.5-24.1 1.4-52 16.4-67.9 34.9-17.5 19.8-27.8 44.3-25.6 71.9 26.1 2 49.9-11.4 69.5-34.3z"/></svg>'

LANG_LABELS = [("index.html", "EN"), ("ko.html", "한국어"), ("ja.html", "日本語"), ("zh-hant.html", "繁體")]

LOCALES = {
    "en": {
        "file": "index.html", "lang": "en", "font": None,
        "title": "Honest Camera — A toddler camera with one yellow button",
        "desc": "The simplest camera for kids ages 3 and up. One big yellow shutter, photos save straight to your library — no ads, no purchases, no settings, nothing to break.",
        "og_title": "Honest Camera — My First Camera",
        "og_desc": "One yellow button. That's the whole app.",
        "kicker_num": "FOR AGES 3+",
        "h1": "One yellow button.<br>That's the <em>whole app</em>.",
        "pill": ["Tap", "Click!", "Saved ✓"],
        "sub": "Honest Camera is a real camera for small hands. Your child taps the big yellow button — click! — and the photo lands safely in your Photos library. There are no other buttons. Nothing to switch, nothing to buy, nowhere to get lost.",
        "badge_small": "Download on the", "note": "PAID ONCE · NO ADS · NO SUBSCRIPTION",
        "badge_aria": "Download on the App Store",
        "chips": [["3+", "Ages 3 and up"], ["1", "One button"], ["✓", "Saved to Photos"], ["0", "No ads"]],
        "hero_alt": "Honest Camera screen: a photo preview and one big yellow shutter button",
        "how_kicker": "HOW IT WORKS", "how_num": "01–03",
        "how_h2": "So simple, a three-year-old <em>already knows how</em>.",
        "steps": [
            ["TAP", "Press the yellow button", "There is exactly one button on screen. A click sound, a little flash, a happy buzz — your child knows the photo happened."],
            ["SAVED", "The photo saves itself", "No save button, no pop-up asking questions. Every photo goes straight into the family Photos library, full size."],
            ["AGAIN", "Red X, shoot again", "The photo shows up big. Tap the red X and the camera is back. That's the entire app — we promise."],
        ],
        "cut_kicker": "THE HONEST PART", "cut_num": "EXTRAS: ZERO",
        "cut_h2": "We didn't add features.<br>We <em>removed</em> them.",
        "cut_lede": "A normal camera app has dozens of buttons — and every one of them is an accident waiting for a toddler's finger. Honest Camera works the other way around: everything risky is gone, and one yellow shutter remains.",
        "cut_rows": [
            ["Mode switching", "gone", "NO ACCIDENTAL VIDEO", ""],
            ["Settings &amp; menus", "gone", "NOTHING TO BREAK", ""],
            ["Gallery &amp; sharing", "gone", "NO WAY OUT OF THE APP", ""],
            ["Filters &amp; AI", "gone", "PHOTOS STAY HONEST", ""],
            ["Ads &amp; purchases", "gone", "NOTHING TO TAP INTO", ""],
            ["The yellow shutter", "one stays", "ALL THAT'S LEFT", "keep"],
        ],
        "shots_kicker": "SCREENS", "shots_num": "THE WHOLE APP",
        "shots_h2": "Two screens. <em>That's everything.</em>",
        "shots_caps": ["ONE YELLOW SHUTTER", "TAP X TO SHOOT AGAIN", "WHAT THEY SAW IS WHAT YOU GET"],
        "feat_kicker": "DETAILS", "feat_num": "06",
        "feat_h2": "Small app. <em>Parent-grade</em> decisions.",
        "feats": [
            ["Saves to your Photos library", "Photos don't get trapped inside the app — they land in the family library at full quality, the moment they're taken."],
            ["Paid once. That's it.", "No subscription, no coins, no “premium”. Inside the app there is nothing to buy and no ad to tap."],
            ["Lock them in, gently", "Onboarding walks you through Apple's Guided Access — triple-click the side button and your child can't leave the camera."],
            ["Volume-button shutter? Removed on purpose.", "Toddlers can't tell the volume button from the power button — and the screen goes dark. So the only shutter is on the screen."],
            ["What they see is what you get", "No filters, no AI touch-ups, no stickers. The photo is exactly what your child saw. That's why it's called Honest."],
            ["iPhone &amp; iPad · 4 languages", "English, 한국어, 日本語, 繁體中文. Landscape works too — for lining up all the stuffed animals."],
        ],
        "final_h2": "Their first camera.",
        "final_lede": "Hundreds of blurry masterpieces are coming. You'll love every one.",
        "f_contact": "Contact", "f_privacy": "Privacy", "f_terms": "Terms",
    },
    "ko": {
        "file": "ko.html", "lang": "ko", "font": '"Apple SD Gothic Neo", "Pretendard"',
        "title": "Honest Camera — 노란 버튼 하나뿐인 유아 카메라",
        "desc": "3세부터 쓰는 가장 단순한 카메라. 큰 노란 셔터 하나, 찍으면 부모님 사진 앱에 바로 저장 — 광고도, 결제도, 설정도 없어요.",
        "og_title": "Honest Camera — 첫 카메라",
        "og_desc": "노란 버튼 하나. 그게 앱의 전부예요.",
        "kicker_num": "3세부터",
        "h1": "노란 버튼 하나.<br>그게 <em>앱의 전부</em>예요.",
        "pill": ["꾹", "찰칵!", "저장 ✓"],
        "sub": "Honest Camera는 작은 손을 위한 진짜 카메라예요. 아이가 노란 버튼을 꾹 — 찰칵! — 사진은 부모님 사진 앱에 안전하게 들어가요. 다른 버튼은 없어요. 바꿀 것도, 살 것도, 헤맬 곳도 없어요.",
        "badge_small": "다운로드는", "note": "일회 구매 · 광고 없음 · 구독 없음",
        "badge_aria": "App Store에서 다운로드",
        "chips": [["3+", "3세부터"], ["1", "버튼 한 개"], ["✓", "자동 저장"], ["0", "광고 없음"]],
        "hero_alt": "Honest Camera 화면 — 사진 미리보기와 큰 노란 셔터 버튼 하나",
        "how_kicker": "사용 방법", "how_num": "01–03",
        "how_h2": "세 살이면 <em>벌써 다 아는</em> 사용법.",
        "steps": [
            ["꾹", "노란 버튼을 눌러요", "화면에 버튼은 딱 하나예요. 찰칵 소리, 반짝 불빛, 손에 오는 진동 — 찍혔다는 걸 아이도 바로 알아요."],
            ["저장", "사진은 저절로 저장돼요", "저장 버튼도, 물어보는 창도 없어요. 찍는 순간 가족 사진 보관함에 원본 그대로 들어가요."],
            ["또", "빨간 X를 누르면 다시", "찍은 사진이 크게 보여요. 빨간 X를 누르면 다시 카메라로. 이게 앱의 전부예요 — 정말로요."],
        ],
        "cut_kicker": "정직한 이유", "cut_num": "더한 것 0",
        "cut_h2": "기능을 더한 게 아니라<br><em>뺀</em> 카메라예요.",
        "cut_lede": "보통 카메라 앱엔 버튼이 수십 개 있어요. 유아 손가락에는 전부 사고의 씨앗이죠. Honest Camera는 반대로 만들었어요 — 위험한 건 다 빼고, 노란 셔터 하나만 남겼어요.",
        "cut_rows": [
            ["모드 전환", "없음", "실수로 동영상 안 찍혀요", ""],
            ["설정 · 메뉴", "없음", "눌러서 망가질 게 없어요", ""],
            ["갤러리 · 공유", "없음", "앱 밖으로 못 나가요", ""],
            ["필터 · AI 보정", "없음", "사진이 정직해요", ""],
            ["광고 · 결제 창", "없음", "잘못 누를 게 없어요", ""],
            ["노란 셔터", "한 개만 남김", "이것만 있으면 돼요", "keep"],
        ],
        "shots_kicker": "화면", "shots_num": "이게 전부",
        "shots_h2": "화면은 두 개. <em>그게 전부예요.</em>",
        "shots_caps": ["노란 셔터 하나", "빨간 X로 다시 찍기", "본 대로 찍혀요"],
        "feat_kicker": "디테일", "feat_num": "06",
        "feat_h2": "작은 앱, <em>부모 기준</em>의 결정들.",
        "feats": [
            ["부모님 사진 앱으로 바로", "사진이 앱 안에 갇히지 않아요. 찍는 순간 가족 사진 보관함에 원본 화질로 저장돼요."],
            ["한 번 구매로 끝", "구독도, 코인도, '프리미엄'도 없어요. 앱 안에는 살 것도, 누를 광고도 없어요."],
            ["앱에서 못 나가게 잠그기", "애플의 '사용법 유도' 기능(측면 버튼 3번)으로 카메라에 잠그는 법을 온보딩에서 차근차근 알려드려요."],
            ["볼륨 버튼 셔터도 일부러 뺐어요", "아이는 볼륨 버튼과 전원 버튼을 구별하지 못해요. 화면이 꺼져버리죠. 그래서 셔터는 화면에만 있어요."],
            ["본 대로 찍혀요", "필터도, AI 보정도, 스티커도 없어요. 아이 눈에 보인 그대로가 사진이 돼요. 그래서 이름이 Honest예요."],
            ["iPhone · iPad · 4개 언어", "한국어 · English · 日本語 · 繁體中文. 인형들을 줄 세워 찍을 땐 가로로 돌려도 돼요."],
        ],
        "final_h2": "아이의 첫 카메라.",
        "final_lede": "흔들린 걸작 수백 장이 찾아올 거예요. 전부 사랑하게 될걸요.",
        "f_contact": "문의", "f_privacy": "개인정보 처리방침", "f_terms": "이용약관",
    },
    "ja": {
        "file": "ja.html", "lang": "ja", "font": '"Hiragino Kaku Gothic ProN", "Hiragino Sans", "Yu Gothic"',
        "title": "Honest Camera — 黄色いボタンひとつだけの幼児カメラ",
        "desc": "3歳から使えるいちばんシンプルなカメラ。大きな黄色いシャッターひとつ、撮ったらすぐ写真ライブラリへ保存 — 広告も課金も設定もありません。",
        "og_title": "Honest Camera — はじめてのカメラ",
        "og_desc": "黄色いボタン、ひとつだけ。それがアプリのぜんぶ。",
        "kicker_num": "3さいから",
        "h1": "黄色いボタン、ひとつ。<br>それが<em>アプリのぜんぶ</em>。",
        "pill": ["ポン", "カシャ！", "保存 ✓"],
        "sub": "Honest Camera は小さな手のための本物のカメラ。お子さんが黄色いボタンをポンと押すと — カシャ！ — 写真はおうちの写真ライブラリへ安全に保存されます。ほかのボタンはありません。切り替えるものも、買うものも、迷子になる場所もありません。",
        "badge_small": "ダウンロードは", "note": "買い切り · 広告なし · サブスクなし",
        "badge_aria": "App Store でダウンロード",
        "chips": [["3+", "3さいから"], ["1", "ボタンひとつ"], ["✓", "自動保存"], ["0", "広告なし"]],
        "hero_alt": "Honest Camera の画面 — 写真プレビューと大きな黄色いシャッターボタン",
        "how_kicker": "使いかた", "how_num": "01–03",
        "how_h2": "3歳なら<em>もう知ってる</em>使いかた。",
        "steps": [
            ["ポン", "黄色いボタンを押す", "画面のボタンはひとつだけ。カシャという音、ピカッと光る画面、手に伝わる振動 — 撮れたことが子どもにもすぐ分かります。"],
            ["保存", "写真はひとりでに保存", "保存ボタンも、確認のポップアップもありません。撮った瞬間、家族の写真ライブラリへそのまま入ります。"],
            ["もう一回", "赤い×でまた撮る", "撮った写真が大きく表示されます。赤い×を押せばまたカメラに戻る。アプリはこれでぜんぶです — 本当に。"],
        ],
        "cut_kicker": "正直なわけ", "cut_num": "足したもの 0",
        "cut_h2": "機能を足したのではなく、<br><em>引いた</em>カメラ。",
        "cut_lede": "ふつうのカメラアプリにはボタンが何十個もあります。幼児の指には、そのすべてが事故のもと。Honest Camera は逆につくりました — 危ないものをぜんぶ取り除いて、黄色いシャッターだけを残しました。",
        "cut_rows": [
            ["モード切替", "なし", "まちがえて動画にならない", ""],
            ["設定・メニュー", "なし", "押して壊れるものがない", ""],
            ["ギャラリー・共有", "なし", "アプリの外に出られない", ""],
            ["フィルター・AI補正", "なし", "写真が正直なまま", ""],
            ["広告・課金画面", "なし", "押してしまうものがない", ""],
            ["黄色いシャッター", "ひとつだけ", "これさえあればいい", "keep"],
        ],
        "shots_kicker": "画面", "shots_num": "これでぜんぶ",
        "shots_h2": "画面はふたつ。<em>それでぜんぶ。</em>",
        "shots_caps": ["黄色いシャッターひとつ", "赤い×でもう一回", "見たままが撮れる"],
        "feat_kicker": "こだわり", "feat_num": "06",
        "feat_h2": "小さなアプリ、<em>親の目線</em>の決断。",
        "feats": [
            ["写真ライブラリへ直行", "写真がアプリの中に閉じ込められません。撮った瞬間、家族の写真ライブラリへ元の画質のまま保存されます。"],
            ["買い切り、それだけ", "サブスクもコインも「プレミアム」もなし。アプリの中に買うものも、押してしまう広告もありません。"],
            ["カメラから出られないように", "Apple の「アクセスガイド」(サイドボタン3回) でこのアプリにロックする方法を、オンボーディングで順番にご案内します。"],
            ["音量ボタンのシャッターも、あえて削除", "幼児は音量ボタンと電源ボタンを区別できず、画面が消えてしまいます。だからシャッターは画面の中だけ。"],
            ["見たままが写真になる", "フィルターも AI 補正もステッカーもなし。子どもの目に見えたままが写真になります。だから名前が Honest。"],
            ["iPhone · iPad · 4言語", "日本語 · English · 한국어 · 繁體中文。ぬいぐるみを並べて撮るときは横向きでもどうぞ。"],
        ],
        "final_h2": "はじめてのカメラに。",
        "final_lede": "ぶれた傑作が何百枚もやってきます。きっとぜんぶ好きになります。",
        "f_contact": "お問い合わせ", "f_privacy": "プライバシーポリシー", "f_terms": "利用規約",
    },
    "zh-hant": {
        "file": "zh-hant.html", "lang": "zh-Hant", "font": '"PingFang TC", "Heiti TC"',
        "title": "Honest Camera — 只有一顆黃色按鈕的幼兒相機",
        "desc": "3 歲就能用的最簡單相機。一顆大大的黃色快門，拍了直接存進照片圖庫 — 沒有廣告、沒有內購、沒有設定。",
        "og_title": "Honest Camera — 第一台相機",
        "og_desc": "一顆黃色按鈕，就是整個 App。",
        "kicker_num": "3 歲以上",
        "h1": "一顆黃色按鈕。<br>就是<em>整個 App</em>。",
        "pill": ["按", "喀嚓！", "已儲存 ✓"],
        "sub": "Honest Camera 是為小小手設計的真相機。孩子按下黃色按鈕 — 喀嚓！— 照片就安全地存進家裡的照片圖庫。沒有其他按鈕。沒有東西可以切換、可以買、可以迷路。",
        "badge_small": "下載於", "note": "買斷制 · 無廣告 · 無訂閱",
        "badge_aria": "在 App Store 下載",
        "chips": [["3+", "3 歲以上"], ["1", "只有一顆按鈕"], ["✓", "自動儲存"], ["0", "無廣告"]],
        "hero_alt": "Honest Camera 畫面 — 照片預覽與一顆大大的黃色快門按鈕",
        "how_kicker": "使用方式", "how_num": "01–03",
        "how_h2": "三歲的孩子<em>本來就會</em>的用法。",
        "steps": [
            ["按", "按下黃色按鈕", "畫面上只有一顆按鈕。喀嚓一聲、閃一下光、手上輕輕一震 — 孩子馬上知道拍到了。"],
            ["儲存", "照片自己存好", "沒有儲存按鈕，也沒有跳出來問東問西的視窗。按下的那一刻，照片就以原始畫質進到家人的照片圖庫。"],
            ["再來", "紅色 × 再拍一張", "拍好的照片會放大顯示。按紅色 × 就回到相機。整個 App 就這樣 — 真的。"],
        ],
        "cut_kicker": "誠實的理由", "cut_num": "加上的 0",
        "cut_h2": "不是加了功能，<br>是把功能<em>拿掉</em>的相機。",
        "cut_lede": "一般相機 App 有幾十顆按鈕，對幼兒的手指來說每一顆都是意外。Honest Camera 反著做 — 把危險的全部拿掉，只留下一顆黃色快門。",
        "cut_rows": [
            ["模式切換", "沒有", "不會誤拍成影片", ""],
            ["設定・選單", "沒有", "沒有東西可以弄壞", ""],
            ["相簿・分享", "沒有", "出不了這個 App", ""],
            ["濾鏡・AI 修圖", "沒有", "照片保持誠實", ""],
            ["廣告・付費視窗", "沒有", "沒有東西會誤按", ""],
            ["黃色快門", "只留這一顆", "有這顆就夠了", "keep"],
        ],
        "shots_kicker": "畫面", "shots_num": "就是全部",
        "shots_h2": "兩個畫面，<em>就是全部。</em>",
        "shots_caps": ["一顆黃色快門", "紅色 × 再拍一張", "看到什麼拍到什麼"],
        "feat_kicker": "細節", "feat_num": "06",
        "feat_h2": "小小的 App，<em>家長標準</em>的決定。",
        "feats": [
            ["直接存進照片圖庫", "照片不會被關在 App 裡。按下快門的那一刻，就以原始畫質存進家人的照片圖庫。"],
            ["買斷一次就好", "沒有訂閱、沒有代幣、沒有「進階版」。App 裡沒有東西可以買，也沒有廣告可以誤按。"],
            ["把孩子留在相機裡", "新手引導會一步步教你用 Apple 的「引導使用模式」(側邊按鈕按三下)，孩子就離不開相機畫面。"],
            ["音量鍵快門？故意拿掉的", "幼兒分不清音量鍵和電源鍵，一按螢幕就黑了。所以快門只在螢幕上。"],
            ["看到什麼，拍到什麼", "沒有濾鏡、沒有 AI 修圖、沒有貼紙。孩子眼裡的世界原原本本變成照片。所以才叫 Honest。"],
            ["iPhone · iPad · 4 種語言", "繁體中文 · English · 한국어 · 日本語。把娃娃排排站拍照時，橫著拿也可以。"],
        ],
        "final_h2": "孩子的第一台相機。",
        "final_lede": "幾百張晃到不行的傑作正在路上，你會每一張都捨不得刪。",
        "f_contact": "聯絡我們", "f_privacy": "隱私權政策", "f_terms": "服務條款",
    },
}

PHOTOS = ["photo-duplo.jpg", "photo-zebra.jpg", "photo-chick.jpg", "photo-lamb.jpg"]


def hreflang_block():
    lines = [f'<link rel="alternate" hreflang="x-default" href="{BASE_URL}">']
    for loc in LOCALES.values():
        href = BASE_URL if loc["file"] == "index.html" else BASE_URL + loc["file"]
        lines.append(f'<link rel="alternate" hreflang="{loc["lang"]}" href="{href}">')
    return "\n".join(lines)


def lang_nav(cur_file):
    out = []
    for f, label in LANG_LABELS:
        cls = ' class="cur"' if f == cur_file else ""
        out.append(f'<a href="{f}"{cls}>{label}</a>')
    return "".join(out)


def badge(loc, el_id):
    return (f'<a class="store-badge" id="{el_id}" href="{APP_STORE_URL}" aria-label="{loc["badge_aria"]}">{APPLE_SVG}'
            f'<span class="txt"><small>{loc["badge_small"]}</small><strong>App Store</strong></span></a>')


def appscreen(photo, preview=False, ids=False):
    """Composed Honest Camera app screen (the real UI is this simple)."""
    cls = "appscreen is-preview" if preview else "appscreen"
    sid = ' id="demoScreen"' if ids else ""
    img_id = ' id="demoPhoto"' if ids else ""
    shut_id = ' id="demoShut"' if ids else ""
    xb_id = ' id="demoXb"' if ids else ""
    flash = '<div class="flashov" id="demoFlash"></div>' if ids else ""
    return (f'<div class="{cls}"{sid}><div class="band"></div>'
            f'<div class="pa"><img{img_id} src="assets/{photo}" alt="" loading="lazy"></div>'
            f'<div class="ctrl"><span class="shut"{shut_id}></span><span class="xb"{xb_id}>✕</span></div>'
            f'{flash}</div>')


def render(key):
    loc = LOCALES[key]
    font_override = f'<style>body{{font-family:-apple-system,BlinkMacSystemFont,{loc["font"]},"Segoe UI",sans-serif}}</style>' if loc["font"] else ""
    canonical = BASE_URL if loc["file"] == "index.html" else BASE_URL + loc["file"]

    pill = f'<span class="d d1 on">{loc["pill"][0]}</span><span class="sep">→</span><span class="d d2">{loc["pill"][1]}</span><span class="sep">→</span><span class="d d3">{loc["pill"][2]}</span>'
    chips = "".join(
        f'<div class="chip c{i+1}"{" id=\"savedChip\"" if i == 2 else ""}><span class="g">{g}</span>{label}</div>'
        for i, (g, label) in enumerate(loc["chips"])
    )
    steps = "".join(
        f'<div class="step"><span class="n">0{i+1}</span><span class="tag">{tag}</span><h3>{h}</h3><p>{p}</p></div>'
        for i, (tag, h, p) in enumerate(loc["steps"])
    )
    cut = "".join(
        f'<div class="cut-row {cls}"><span>{a}</span><span class="arrow">→</span><span class="to">{b}</span><span class="cat">{c}</span></div>'
        for a, b, c, cls in loc["cut_rows"]
    )
    shot_states = [("photo-duplo.jpg", False), ("photo-zebra.jpg", True), ("photo-lamb.jpg", True)]
    shots = "".join(
        f'<figure><div class="phone">{appscreen(p, prev)}<div class="island"></div></div><figcaption>{cap}</figcaption></figure>'
        for (p, prev), cap in zip(shot_states, loc["shots_caps"])
    )
    feats = "".join(f'<div class="feat"><h3>{h}</h3><p>{p}</p></div>' for h, p in loc["feats"])

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
<link rel="canonical" href="{canonical}">
{hreflang_block()}
<link rel="icon" type="image/png" href="assets/icon-180.png">
<link rel="apple-touch-icon" href="assets/icon-180.png">
<link rel="stylesheet" href="assets/style.css">
{font_override}
</head>
<body>

<nav>
  <div class="wrap">
    <a class="wordmark" href="./"><img src="assets/icon-180.png" alt=""><span>HONEST·CAMERA</span></a>
    <div class="lang">{lang_nav(loc['file'])}</div>
  </div>
</nav>

<header class="hero">
  <div class="ghost">1</div>
  <div class="wrap">
    <div>
      <div class="kicker"><span>HONEST · CAMERA</span><span class="rule"></span><span class="num">{loc['kicker_num']}</span></div>
      <h1>{loc['h1']}</h1>
      <div class="demo" aria-hidden="true">{pill}</div>
      <p class="sub">{loc['sub']}</p>
      <div class="cta">
        {badge(loc, 'storeLink')}
        <span class="note">{loc['note']}</span>
      </div>
    </div>
    <div class="phone-col" role="img" aria-label="{loc['hero_alt']}">
      {chips}
      <div class="phone">{appscreen(PHOTOS[0], ids=True)}<div class="island"></div></div>
    </div>
  </div>
</header>

<section>
  <div class="wrap">
    <div class="kicker"><span>{loc['how_kicker']}</span><span class="rule"></span><span class="num">{loc['how_num']}</span></div>
    <h2>{loc['how_h2']}</h2>
    <div class="steps">{steps}</div>
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap">
    <div class="kicker"><span>{loc['cut_kicker']}</span><span class="rule"></span><span class="num">{loc['cut_num']}</span></div>
    <h2>{loc['cut_h2']}</h2>
    <p class="lede">{loc['cut_lede']}</p>
    <div class="cut-table">{cut}</div>
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
    <div class="brand"><img src="assets/icon-180.png" alt=""><strong>kkiruk studio</strong></div>
    <div class="links">
      <a href="mailto:kkirukstudio.help@gmail.com">{loc['f_contact']}</a>
      <a href="https://kkiruk-studio.github.io/privacy-policy-app/">{loc['f_privacy']}</a>
      <a href="https://kkiruk-studio.github.io/terms-of-service-app/">{loc['f_terms']}</a>
    </div>
    <div>© 2026 kkiruk studio</div>
  </div>
</footer>

<script>
  const PHOTOS = {PHOTOS!r};
  const scr = document.getElementById("demoScreen");
  const img = document.getElementById("demoPhoto");
  const shut = document.getElementById("demoShut");
  const xb = document.getElementById("demoXb");
  const flash = document.getElementById("demoFlash");
  const saved = document.getElementById("savedChip");
  const dots = [document.querySelector(".demo .d1"), document.querySelector(".demo .d2"), document.querySelector(".demo .d3")];
  PHOTOS.forEach(p => {{ const i = new Image(); i.src = "assets/" + p; }});

  if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches && scr) {{
    const sleep = (ms) => new Promise(r => setTimeout(r, ms));
    const setOn = (k) => dots.forEach((d, j) => d && d.classList.toggle("on", j === k));
    let i = 0;
    (async function loop() {{
      for (;;) {{
        scr.classList.remove("is-preview");
        img.src = "assets/" + PHOTOS[i % PHOTOS.length];
        setOn(0);
        await sleep(1500);
        shut.classList.add("press"); setOn(1);
        await sleep(150);
        shut.classList.remove("press");
        flash.classList.add("on");
        await sleep(110);
        scr.classList.add("is-preview");
        flash.classList.remove("on");
        setOn(2);
        saved.classList.add("pop");
        await sleep(2100);
        saved.classList.remove("pop");
        xb.classList.add("press");
        await sleep(160);
        xb.classList.remove("press");
        i++;
      }}
    }})();
  }}
</script>
</body>
</html>
"""
    out = ROOT / loc["file"]
    out.write_text(html, encoding="utf-8")
    print(f"wrote {out.name} ({len(html)} bytes)")


for key in LOCALES:
    render(key)
