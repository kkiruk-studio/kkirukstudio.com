#!/usr/bin/env python3
"""Generate index.html for every locale from one template.

Usage: python3 build.py
Output: ./index.html (en), ./ko/index.html, ./ja/index.html, ./zh-hant/index.html
Screenshots: ./assets/shots/<lang>-{library,sort,stats}.jpg (from fastlane/screenshots_raw)
"""
import pathlib

ROOT = pathlib.Path(__file__).parent
BASE_URL = "https://www.kkirukstudio.com/capbox/"

# Filled in after App Store approval (https://apps.apple.com/app/id6816986062).
# While empty, both CTAs render as a disabled "coming soon" pill and the final
# lede uses `final_soon`. (gen/check_stale.py in the site repo flags an empty
# value on purpose — fill it on launch day, then register the slug in
# check_stale APP_DIRS, gen_jsonld APPS and refresh_seo SUMMARIES.)
APP_STORE_URL = "https://apps.apple.com/app/id6816986062"

LANG_LABELS = [("ko/", "한국어"), ("", "EN"), ("ja/", "日本語"), ("zh-hant/", "繁體中文")]

SHOTS = ["library", "sort", "stats"]

APPLE_SVG = ('<svg viewBox="0 0 384 512" aria-hidden="true"><path d="M318.7 268.7c-.2-36.7 16.4-64.4 50-84.8-18.8-26.9-47.2-41.7-84.7-44.6-35.5-2.8-74.3 20.7-88.5 20.7-15 0-49.4-19.7-76.4-19.7C63.3 141.2 4 184.8 4 273.5q0 39.3 14.4 81.2c12.8 36.7 59 126.7 107.2 125.2 25.2-.6 43-17.9 75.8-17.9 31.8 0 48.3 17.9 76.4 17.9 48.6-.7 90.4-82.5 102.6-119.3-65.2-30.7-61.7-90-61.7-91.9zm-56.6-164.2c27.3-32.4 24.8-61.9 24-72.5-24.1 1.4-52 16.4-67.9 34.9-17.5 19.8-27.8 44.3-25.6 71.9 26.1 2 49.9-11.4 69.5-34.3z"/></svg>')

LOCALES = {
    "ko": {
        "dir": "ko/", "lang": "ko", "shot": "ko", "font": None,
        "title": "CapBox — 스크린샷 정리 · 사진 속 텍스트 검색",
        "desc": "쌓인 스크린샷과 짤을 한 장씩 넘기며 폴더로 정리하고, 필요 없는 건 휴지통에 모아 한 번에 삭제하세요. 사진 속 글자로 검색까지, 전부 기기 안에서 무료로.",
        "og_title": "CapBox — 스크린샷 정리",
        "og_desc": "쌓인 캡처, 넘기면서 폴더로. 사진 속 글자로 다시 찾기.",
        "kicker_num": "스크린샷 정리",
        "h1": "쌓인 캡처,<br><em>넘기면서</em> 정리하세요.",
        "sub": "단톡방에서 저장한 짤, 배달 주문 내역, 맛집 찾다 캡처한 네이버 지도까지 — 사진첩에 뒤섞인 스크린샷을 한 장씩 넘기며 폴더로 보내세요. 필요 없는 건 휴지통에 모았다가 한 번에 비우고, 나중엔 사진 속 글자로 찾으면 됩니다.",
        "badge_soon": "곧 출시", "badge_live": "다운로드는", "badge_aria": "App Store에서 다운로드",
        "note": "온디바이스 · 가입 없음 · 무료",
        "chips": [["짤", "짤/밈 폴더"], ["결", "결제 폴더"], ["지", "지도 폴더"]],
        "hero_alt": "CapBox 보관함 화면 — 정리 안 된 캡처 1,284장과 짤/밈·대화·결제·지도·쇼핑·문서 폴더",
        "marquee": ["한 장씩 스와이프", "여러 장씩 정리", "폴더 칩 한 탭", "휴지통 일괄 삭제", "사진 속 텍스트 검색", "사진 앱 앨범 연동", "기존 앨범 가져오기", "온디바이스"],
        "how_kicker": "사용 방법",
        "how_h2": "스캔하고, 넘기고, <em>앨범으로 남기기</em>.",
        "steps": [
            ["스캔", "사진 보관함 스캔", "카메라 롤을 훑어서 아직 정리 안 된 캡처가 몇 장인지 보여줍니다. 스크린샷만, 또는 전체 사진을 대상으로 고를 수 있어요."],
            ["정리", "넘기면서 폴더로", "한 장씩 좌우로 넘기며 아래 폴더 칩을 탭하면 끝. 여러 장을 골라 한 번에 보낼 수도 있어요. 필요 없는 건 휴지통으로."],
            ["보관", "사진 앱 앨범으로 남음", "폴더는 사진 앱 ‘CapBox’ 폴더 안의 진짜 앨범이라, CapBox를 지워도 정리한 결과는 그대로 남습니다."],
        ],
        "conv_kicker": "핵심 가치", "conv_num": "온디바이스",
        "conv_h2": "정리는 되는데, <em>사진은 안 나간다</em>.",
        "conv_lede": "사진 속 글자 인식도, 검색도 전부 iPhone 안에서 처리합니다. 서버가 없으니 보낼 곳도 없어요. 가입도, 인앱 결제도 없습니다.",
        "conv_rows": [["스크린샷 스캔", "기기 안"], ["사진 속 글자 인식 (OCR)", "기기 안"], ["정리 결과 저장", "사진 앱 앨범"]],
        "maps_kicker": "폴더 구성", "maps_num": "예시",
        "maps_h2": "폴더는 <em>내 마음대로</em>.",
        "maps_lede": "짤/밈·대화·결제·지도·쇼핑·문서 기본 폴더 세트로 시작하거나, 이미 만들어 둔 앨범을 가져오세요. 이름·색·아이콘은 언제든 바꿀 수 있어요.",
        "providers": [
            ["😂", "짤/밈", ["단톡방 짤", "반응짤 모음"]],
            ["💬", "대화", ["카톡 대화 캡처", "인스타 DM"]],
            ["🧾", "결제", ["배달 주문 내역", "계좌이체 확인"]],
            ["🗺️", "지도", ["네이버 지도 캡처", "맛집 주소"]],
        ],
        "shots_kicker": "화면", "shots_num": "iOS",
        "shots_h2": "쌓아두기용이 아니라, <em>꺼내 쓰는 도구</em>로.",
        "shots_caps": ["보관함 · 폴더", "넘기면서 정리", "스크린샷 통계"],
        "feat_kicker": "디테일", "feat_num": "06",
        "feat_h2": "작은 앱, <em>분명한 선택</em>.",
        "feats": [
            ["휴지통에 모았다가 한 번에", "정리하다 필요 없는 캡처는 휴지통으로. 모아서 확인하고 한 번에 비워요. 잘못 넣은 건 복원할 수 있어요."],
            ["사진 속 텍스트 검색", "캡처 안의 글자를 기기에서 인식해 둡니다. 폴더 안 사진은 물론 아직 정리 안 한 스크린샷도 글자로 찾아요. 한국어·영어·일본어·중국어(번체)."],
            ["기존 앨범 가져오기", "사진 앱에 이미 만들어 둔 앨범을 CapBox 폴더로 가져와 이어서 정리할 수 있어요."],
            ["한 장씩, 또는 여러 장씩", "카드를 한 장씩 넘기며 정리할 수도, 여러 장을 골라 한 번에 폴더로 보낼 수도 있습니다."],
            ["연도별 · 해상도별 통계", "스크린샷이 해마다 몇 장씩 쌓였는지, 어떤 해상도가 많은지 한눈에 봅니다."],
            ["4개 언어 지원", "한국어·English·日本語·繁體中文. 앱 화면도, 글자 검색도."],
        ],
        "wit": "엔트로피는 저절로 줄지 않습니다.",
        "final_h2": "스크린샷 폴더, 더 이상 미루지 마세요.",
        "final_soon": "App Store 곧 출시. iPhone에서 무료, 인앱 결제 없음.",
        "final_live": "iPhone에서 무료. 인앱 결제 없음.",
        "f_contact": "문의", "f_privacy": "개인정보 처리방침", "f_terms": "이용약관",
    },
    "en": {
        "dir": "", "lang": "en", "shot": "en", "font": None,
        "title": "CapBox — Screenshot Cleaner & Photo Text Search",
        "desc": "Sort screenshots into folders with a swipe, toss what you don't need into the trash and empty it in one go, and search the text inside your photos. All on device, free.",
        "og_title": "CapBox — Screenshot Cleaner",
        "og_desc": "Swipe through the pile, file it into folders, find it later by the text inside.",
        "kicker_num": "SCREENSHOT CLEANER",
        "h1": "Swipe the pile.<br><em>File it away.</em>",
        "sub": "Memes from the group chat, order confirmations, a Google Maps pin you grabbed before heading out — they all end up in one messy camera roll. Swipe through them one at a time and tap a folder, toss the rest into the trash, then find anything later by the text inside it.",
        "badge_soon": "Coming soon", "badge_live": "Download on the", "badge_aria": "Download on the App Store",
        "note": "ON-DEVICE · NO ACCOUNT · FREE",
        "chips": [["M", "Memes folder"], ["R", "Receipts folder"], ["P", "Maps folder"]],
        "hero_alt": "CapBox library screen — 1,284 unsorted captures and folders for Memes, Chats, Receipts, Maps, Shopping and Docs",
        "marquee": ["SWIPE TO SORT", "BATCH SORT", "ONE-TAP FOLDERS", "TRASH & EMPTY", "TEXT SEARCH", "REAL PHOTOS ALBUMS", "IMPORT ALBUMS", "ON-DEVICE"],
        "how_kicker": "HOW IT WORKS",
        "how_h2": "Scan, swipe, <em>keep it in Photos</em>.",
        "steps": [
            ["SCAN", "Scan your camera roll", "CapBox counts the captures you haven't sorted yet. Work through screenshots only, or all your photos."],
            ["SORT", "Swipe and tap a folder", "Swipe through one at a time and tap a folder chip. Or select a batch and send it all at once. Anything you don't need goes to the trash."],
            ["KEEP", "Stays as real Photos albums", "Folders are real albums inside a “CapBox” folder in the Photos app, so your sorting stays even if you delete CapBox."],
        ],
        "conv_kicker": "CORE VALUE", "conv_num": "ON-DEVICE",
        "conv_h2": "Sorted, but <em>never uploaded</em>.",
        "conv_lede": "Text recognition and search both run on your iPhone. There's no server, so there's nowhere to send your photos. No account, no in-app purchases.",
        "conv_rows": [["Screenshot scan", "ON DEVICE"], ["Text recognition (OCR)", "ON DEVICE"], ["Where results live", "PHOTOS ALBUMS"]],
        "maps_kicker": "FOLDERS", "maps_num": "EXAMPLES",
        "maps_h2": "Folders, <em>your way</em>.",
        "maps_lede": "Start with a starter set — Memes, Chats, Receipts, Maps, Shopping, Docs — or import the albums you already have. Rename, recolor, or change the icon any time.",
        "providers": [
            ["😂", "Memes", ["Group-chat memes", "Reaction pics"]],
            ["💬", "Chats", ["iMessage threads", "WhatsApp chats"]],
            ["🧾", "Receipts", ["Order confirmations", "Venmo payments"]],
            ["🗺️", "Maps", ["Google Maps pins", "Restaurant addresses"]],
        ],
        "shots_kicker": "SCREENS", "shots_num": "iOS",
        "shots_h2": "Built to be <em>used</em>, not just stored.",
        "shots_caps": ["LIBRARY & FOLDERS", "SWIPE TO SORT", "SCREENSHOT STATS"],
        "feat_kicker": "DETAILS", "feat_num": "06",
        "feat_h2": "Small app. <em>Deliberate</em> choices.",
        "feats": [
            ["Trash first, empty once", "Screenshots you don't need go to the trash. Review them, then delete the whole pile in one go — or restore the ones you tossed by mistake."],
            ["Search the text in your photos", "CapBox reads the text in your captures on device, so you can find a shot by what it said — in folders and in unsorted screenshots alike. Korean, English, Japanese, Traditional Chinese."],
            ["Import existing albums", "Already made albums in Photos? Bring them in as CapBox folders and keep going."],
            ["Swipe one, or select a batch", "Flip through one card at a time, or multi-select a pile and send it to a folder at once."],
            ["Year & resolution stats", "See how many screenshots piled up each year and which resolutions dominate your library."],
            ["Four languages", "Korean, English, Japanese and Traditional Chinese — in the app and in text search."],
        ],
        "wit": "Entropy does not decrease on its own.",
        "final_h2": "Stop putting off that screenshot folder.",
        "final_soon": "Coming soon to the App Store. Free on iPhone, no in-app purchases.",
        "final_live": "Free on iPhone. No in-app purchases.",
        "f_contact": "Contact", "f_privacy": "Privacy", "f_terms": "Terms",
    },
    "ja": {
        "dir": "ja/", "lang": "ja", "shot": "ja", "font": '"Hiragino Kaku Gothic ProN", "Hiragino Sans", "Yu Gothic"',
        "title": "CapBox — スクショ整理・写真内の文字検索",
        "desc": "たまったスクリーンショットを1枚ずつめくってフォルダへ。不要な写真はゴミ箱にまとめて一括削除。写真の中の文字で検索もできます。すべて端末内で、無料。",
        "og_title": "CapBox — スクショ整理",
        "og_desc": "たまったスクショ、めくりながらフォルダへ。あとから写真の中の文字で探せる。",
        "kicker_num": "スクショ整理",
        "h1": "たまったスクショ、<br><em>めくりながら</em>整理。",
        "sub": "LINEで保存したネタ画像、ネット注文の確認画面、お店を探して撮ったGoogleマップ — カメラロールにごちゃ混ぜになったスクショを、1枚ずつめくってフォルダへ。不要なものはゴミ箱にまとめて一括削除、あとから写真の中の文字で探せます。",
        "badge_soon": "近日公開", "badge_live": "ダウンロード", "badge_aria": "App Store でダウンロード",
        "note": "端末内処理 · 登録不要 · 無料",
        "chips": [["ネ", "ネタ画像フォルダ"], ["決", "決済フォルダ"], ["地", "地図フォルダ"]],
        "hero_alt": "CapBoxのライブラリ画面 — 未整理のキャプチャ1,284枚と、ネタ画像・会話・決済・地図・買い物・書類のフォルダ",
        "marquee": ["スワイプで整理", "まとめて整理", "フォルダをワンタップ", "ゴミ箱で一括削除", "写真内の文字検索", "写真アプリのアルバム", "既存アルバムの取り込み", "端末内処理"],
        "how_kicker": "使い方",
        "how_h2": "スキャン、めくる、<em>アルバムに残す</em>。",
        "steps": [
            ["スキャン", "カメラロールをスキャン", "未整理のキャプチャが何枚あるかを表示します。スクリーンショットだけ、またはすべての写真から選べます。"],
            ["整理", "めくってフォルダへ", "1枚ずつ左右にめくり、下のフォルダをタップするだけ。まとめて選んで一括で送ることも。不要なものはゴミ箱へ。"],
            ["保存", "写真アプリのアルバムに残る", "フォルダは写真アプリの「CapBox」フォルダ内の本物のアルバム。CapBoxを削除しても、整理した結果はそのまま残ります。"],
        ],
        "conv_kicker": "コア価値", "conv_num": "オンデバイス",
        "conv_h2": "整理はできても、<em>写真は外に出ない</em>。",
        "conv_lede": "文字の認識も検索も、すべてiPhoneの中で処理します。サーバーがないので送信先もありません。登録もアプリ内課金もありません。",
        "conv_rows": [["スクショのスキャン", "端末内"], ["文字認識（OCR）", "端末内"], ["整理結果の保存先", "写真アプリ"]],
        "maps_kicker": "フォルダ", "maps_num": "例",
        "maps_h2": "フォルダは<em>自由自在</em>。",
        "maps_lede": "ネタ画像・会話・決済・地図・買い物・書類の基本セットから始めるか、作ってあるアルバムを取り込めます。名前・色・アイコンはいつでも変更できます。",
        "providers": [
            ["😂", "ネタ画像", ["LINEで回ってきたネタ", "推しの名場面"]],
            ["💬", "会話", ["LINEのトーク", "XのDM"]],
            ["🧾", "決済", ["PayPayの支払い画面", "ネット注文の確認"]],
            ["🗺️", "地図", ["Googleマップのピン", "お店の住所"]],
        ],
        "shots_kicker": "画面", "shots_num": "iOS",
        "shots_h2": "しまい込むためじゃなく、<em>使うための道具</em>に。",
        "shots_caps": ["ライブラリ・フォルダ", "めくって整理", "スクショ統計"],
        "feat_kicker": "こだわり", "feat_num": "06",
        "feat_h2": "小さなアプリ、<em>明確な選択</em>。",
        "feats": [
            ["ゴミ箱にまとめて一括削除", "不要なスクショはゴミ箱へ。確認してから、まとめて一度に削除できます。間違えて入れたものは復元も可能。"],
            ["写真の中の文字で検索", "キャプチャ内の文字を端末内で認識。フォルダ内の写真も未整理のスクショも、書いてあった文字で探せます。日本語・韓国語・英語・繁体字中国語に対応。"],
            ["既存アルバムの取り込み", "写真アプリで作ってあるアルバムを、CapBoxのフォルダとして取り込んで続きから整理できます。"],
            ["1枚ずつ、またはまとめて", "カードを1枚ずつめくって整理も、複数選択して一括でフォルダへ送ることもできます。"],
            ["年別・解像度別の統計", "年ごとに何枚たまったか、どの解像度が多いかがひと目でわかります。"],
            ["4言語対応", "日本語・韓国語・英語・繁体字中国語。アプリ表示も文字検索も。"],
        ],
        "wit": "エントロピーは勝手には減りません。",
        "final_h2": "スクショフォルダ、もう後回しにしない。",
        "final_soon": "App Storeで近日公開。iPhoneで無料、アプリ内課金なし。",
        "final_live": "iPhoneで無料。アプリ内課金なし。",
        "f_contact": "お問い合わせ", "f_privacy": "プライバシーポリシー", "f_terms": "利用規約",
    },
    "zh-hant": {
        "dir": "zh-hant/", "lang": "zh-Hant", "shot": "zh-hant", "font": '"PingFang TC", "Heiti TC", "Microsoft JhengHei"',
        "title": "CapBox — 截圖整理・照片文字搜尋",
        "desc": "把堆積的截圖和梗圖一張張滑過、分進資料夾，不需要的先放進垃圾桶再一次刪除，還能用照片中的文字搜尋。全部在裝置上完成，免費使用。",
        "og_title": "CapBox — 截圖整理",
        "og_desc": "堆積的截圖，滑一滑就分進資料夾。之後用照片中的文字就能找到。",
        "kicker_num": "截圖整理",
        "h1": "堆積的截圖，<br><em>滑一滑</em>就整理好。",
        "sub": "LINE 群組存下的梗圖、電子發票和網購訂單、找店時截的 Google 地圖 — 相簿裡混在一起的截圖，一張張滑過、點一下資料夾就分好。不需要的先放進垃圾桶再一次清空，之後用照片中的文字就能找到。",
        "badge_soon": "即將上架", "badge_live": "下載", "badge_aria": "在 App Store 下載",
        "note": "裝置端處理 · 免註冊 · 免費",
        "chips": [["梗", "梗圖資料夾"], ["付", "付款資料夾"], ["地", "地圖資料夾"]],
        "hero_alt": "CapBox 收納盒畫面 — 1,284 張尚未整理的截圖，以及梗圖、對話、付款、地圖、購物、文件資料夾",
        "marquee": ["滑動整理", "批次整理", "一點進資料夾", "垃圾桶一次清空", "照片文字搜尋", "「照片」App 相簿", "匯入原有相簿", "裝置端處理"],
        "how_kicker": "使用方式",
        "how_h2": "掃描、滑動、<em>留在相簿裡</em>。",
        "steps": [
            ["掃描", "掃描相機膠卷", "顯示還有幾張截圖尚未整理。可以只整理截圖，也可以從所有照片中整理。"],
            ["整理", "滑過去、點資料夾", "一張張左右滑動，點下方的資料夾就完成。也能一次選多張批次送出。不需要的丟進垃圾桶。"],
            ["保存", "留在「照片」App 的相簿", "資料夾就是「照片」App 中「CapBox」資料夾裡的真正相簿，即使刪除 CapBox，整理好的結果也會保留。"],
        ],
        "conv_kicker": "核心價值", "conv_num": "裝置端",
        "conv_h2": "整理好了，<em>照片不會離開手機</em>。",
        "conv_lede": "文字辨識和搜尋都在 iPhone 上處理。沒有伺服器，也就沒有地方可以傳送。免註冊，也沒有 App 內購買。",
        "conv_rows": [["截圖掃描", "裝置端"], ["文字辨識（OCR）", "裝置端"], ["整理結果存放處", "「照片」相簿"]],
        "maps_kicker": "資料夾", "maps_num": "範例",
        "maps_h2": "資料夾，<em>隨你安排</em>。",
        "maps_lede": "從梗圖、對話、付款、地圖、購物、文件的基本組合開始，或匯入原有的相簿。名稱、顏色、圖示隨時都能改。",
        "providers": [
            ["😂", "梗圖", ["LINE 群組梗圖", "迷因收藏"]],
            ["💬", "對話", ["LINE 對話截圖", "IG 私訊"]],
            ["🧾", "付款", ["電子發票", "網購訂單"]],
            ["🗺️", "地圖", ["Google 地圖截圖", "餐廳地址"]],
        ],
        "shots_kicker": "畫面", "shots_num": "iOS",
        "shots_h2": "不是拿來堆的，是<em>拿來用的工具</em>。",
        "shots_caps": ["收納盒・資料夾", "滑動整理", "截圖統計"],
        "feat_kicker": "細節", "feat_num": "06",
        "feat_h2": "小小的 App，<em>明確的選擇</em>。",
        "feats": [
            ["先進垃圾桶，再一次清空", "不需要的截圖先丟進垃圾桶，確認後一次全部刪除。放錯的也能復原。"],
            ["搜尋照片中的文字", "在裝置上辨識截圖裡的文字。不論是資料夾裡的照片，還是還沒整理的截圖，都能用文字找到。支援繁體中文、英文、日文、韓文。"],
            ["匯入原有相簿", "在「照片」App 已經建好的相簿，可以匯入成 CapBox 資料夾，接著整理。"],
            ["一張張滑，或一次多張", "一張一張翻著整理，或多選一整批，一次送進資料夾。"],
            ["年度・解析度統計", "每年累積了幾張截圖、哪種解析度最多，一目了然。"],
            ["支援 4 種語言", "繁體中文、英文、日文、韓文。App 介面和文字搜尋都支援。"],
        ],
        "wit": "熵不會自己減少。",
        "final_h2": "截圖資料夾，別再拖了。",
        "final_soon": "即將在 App Store 上架。iPhone 免費使用，無 App 內購買。",
        "final_live": "iPhone 免費使用，無 App 內購買。",
        "f_contact": "聯絡我們", "f_privacy": "隱私權政策", "f_terms": "使用條款",
    },
}


def hreflang_block():
    lines = [f'<link rel="alternate" hreflang="x-default" href="{BASE_URL}">']
    for loc in LOCALES.values():
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
                f'<span class="txt"><small>{loc["badge_live"]}</small><strong>App Store</strong></span></a>')
    return (f'<span class="store-badge disabled" id="{el_id}" aria-disabled="true">{APPLE_SVG}'
            f'<span class="txt"><small>{loc["badge_soon"]}</small><strong>App Store</strong></span></span>')


def shot_img(rel, loc, name, alt, lazy=True):
    loading = ' loading="lazy"' if lazy else ""
    return (f'<img src="{rel}assets/shots/{loc["shot"]}-{name}.jpg" alt="{alt}" '
            f'width="552" height="1200"{loading} decoding="async">')


def render(key):
    loc = LOCALES[key]
    rel = "../" if loc["dir"] else ""
    font_override = (f'<style>body{{font-family:-apple-system,BlinkMacSystemFont,{loc["font"]},"Segoe UI",sans-serif}}</style>'
                     if loc["font"] else "")
    chips = "".join(
        f'<div class="chip c{i+1}"><span class="g">{g}</span>{label}</div>'
        for i, (g, label) in enumerate(loc["chips"])
    )
    marquee = "".join(f"<span>{m}</span>" for m in loc["marquee"] * 2)
    steps = "".join(
        f'<div class="step"><span class="n">0{i+1}</span><span class="tag">{tag}</span><h3>{h}</h3><p>{p}</p></div>'
        for i, (tag, h, p) in enumerate(loc["steps"])
    )
    conv = "".join(
        f'<div class="convert-row"><span class="g">{i+1}</span><span class="label">{label}</span><span class="cat">{c}</span></div>'
        for i, (label, c) in enumerate(loc["conv_rows"])
    )
    provs = "".join(
        '<div class="prov"><span class="flag">%s</span><h3>%s</h3><ul>%s</ul></div>'
        % (flag, name, "".join(f'<li><span class="g">✓</span>{n}</li>' for n in items))
        for flag, name, items in loc["providers"]
    )
    shots = "".join(
        f'<figure><div class="phone">{shot_img(rel, loc, name, cap)}</div><figcaption>{cap}</figcaption></figure>'
        for name, cap in zip(SHOTS, loc["shots_caps"])
    )
    feats = "".join(f'<div class="feat"><h3>{h}</h3><p>{p}</p></div>' for h, p in loc["feats"])
    final_lede = loc["final_live"] if APP_STORE_URL else loc["final_soon"]

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
<meta property="og:url" content="{BASE_URL}{loc['dir']}">
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
    <a class="wordmark" href="{rel if rel else './'}"><img src="{rel}assets/icon-180.png" alt=""><span>CAPBOX</span></a>
    <div class="lang">{lang_nav(loc['dir'], rel)}</div>
  </div>
</nav>

<header class="hero">
  <div class="ghost">C·B</div>
  <div class="wrap">
    <div>
      <div class="kicker"><span>CAPBOX</span><span class="rule"></span><span class="num">{loc['kicker_num']}</span></div>
      <h1>{loc['h1']}</h1>
      <div class="demo" aria-hidden="true">
        <div class="shot"><div class="bar w80"></div><div class="bar w60"></div><div class="bar w40"></div></div>
        <div class="folder"><span class="g">📁</span><span class="label">{loc['chips'][0][1]}</span></div>
      </div>
      <p class="sub">{loc['sub']}</p>
      <div class="cta">
        {badge(loc, 'storeLink')}
        <span class="note">{loc['note']}</span>
      </div>
    </div>
    <div class="phone-col">
      {chips}
      <div class="phone">{shot_img(rel, loc, 'library', loc['hero_alt'], lazy=False)}</div>
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
    <div class="kicker"><span>{loc['conv_kicker']}</span><span class="rule"></span><span class="num">{loc['conv_num']}</span></div>
    <h2>{loc['conv_h2']}</h2>
    <p class="lede">{loc['conv_lede']}</p>
    <div class="convert-table">{conv}</div>
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap">
    <div class="kicker"><span>{loc['maps_kicker']}</span><span class="rule"></span><span class="num">{loc['maps_num']}</span></div>
    <h2>{loc['maps_h2']}</h2>
    <p class="lede">{loc['maps_lede']}</p>
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
    <p class="wit">{loc['wit']}</p>
    <h2>{loc['final_h2']}</h2>
    <p class="lede">{final_lede}</p>
    <div class="cta">{badge(loc, 'storeLink2')}</div>
  </div>
</section>

<footer>
  <div class="wrap">
    <div class="brand"><img src="{rel}assets/icon-180.png" alt=""><strong>kkiruk studio</strong></div>
    <div class="links">
      <a href="mailto:kkirukstudio.help@gmail.com">{loc['f_contact']}</a>
      <a href="https://www.kkirukstudio.com/legal/privacy/">{loc['f_privacy']}</a>
      <a href="https://www.kkirukstudio.com/legal/terms/">{loc['f_terms']}</a>
    </div>
    <div>© 2026 kkiruk studio</div>
  </div>
</footer>

<script src="/ga.js"></script>
</body>
</html>
"""
    out = ROOT / loc["dir"] / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)} ({len(html) // 1024} KB)")


for key in LOCALES:
    render(key)

# Inside the site repo (~/kkirukstudio-site/capbox/) keep discovery metadata in
# sync after regeneration: refresh_seo re-injects page JSON-LD and the sitemap.
# In the standalone CapBox repo the gen/ folder does not exist, so this is a no-op.
if __name__ == "__main__":
    import runpy as _seo_runpy
    from pathlib import Path as _SeoPath
    _seo = _SeoPath(__file__).resolve().parent.parent / "gen" / "refresh_seo.py"
    if _seo.exists():
        _seo_runpy.run_path(str(_seo), run_name="__main__")
