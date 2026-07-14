#!/usr/bin/env python3
"""Generate index.html for every locale from one template.

Usage: python3 build.py
Output: ./index.html (en), ./ko/index.html
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).parent
BASE_URL = "https://www.kkirukstudio.com/newsmaker/"

APPLE_SVG = '<svg viewBox="0 0 384 512" aria-hidden="true"><path d="M318.7 268.7c-.2-36.7 16.4-64.4 50-84.8-18.8-26.9-47.2-41.7-84.7-44.6-35.5-2.8-74.3 20.7-88.5 20.7-15 0-49.4-19.7-76.4-19.7C63.3 141.2 4 184.8 4 273.5q0 39.3 14.4 81.2c12.8 36.7 59 126.7 107.2 125.2 25.2-.6 43-17.9 75.8-17.9 31.8 0 48.3 17.9 76.4 17.9 48.6-.7 90.4-82.5 102.6-119.3-65.2-30.7-61.7-90-61.7-91.9zm-56.6-164.2c27.3-32.4 24.8-61.9 24-72.5-24.1 1.4-52 16.4-67.9 34.9-17.5 19.8-27.8 44.3-25.6 71.9 26.1 2 49.9-11.4 69.5-34.3z"/></svg>'

LANG_LABELS = [("", "EN"), ("ko/", "한국어"), ("ja/", "日本語"), ("zh-hant/", "繁體中文")]

LOCALES = {
    "en": {
        "dir": "", "lang": "en", "font": None,
        "title": "Newsmaker — Turn your day into breaking-news memes",
        "desc": "Type one headline, pick a theme and font, and Newsmaker turns your ordinary day into a shareable breaking-news meme. No account, no ads, all on-device. Free for iPhone.",
        "og_title": "Newsmaker — Breaking Meme Maker",
        "og_desc": "Turn your ordinary day into a breaking-news meme in seconds.",
        "kicker_num": "BREAKING MEME MAKER",
        "h1": "Your ordinary day.<br>One <em>breaking-news</em> headline.",
        "pairs": [
            ["Meeting canceled", "BREAKING: Meeting canceled"],
            ["Package arrived", "BREAKING: Package arrived early"],
            ["PR maxed", "BREAKING: New PR — 500 total"],
            ["Got the job", "BREAKING: Final offer received"],
        ],
        "sub": "Type one line about your day. Newsmaker turns it into a red-alert headline card — pick a theme, pick a font, drop in a cut-out photo of yourself, and save it as a shareable image.",
        "badge_small": "Download on the", "note": "FREE · IPHONE · NO ACCOUNT",
        "badge_aria": "Download on the App Store",
        "chips": [["!", "Meeting canceled"], ["!", "Package"], ["!", "Concert tix"], ["!", "PR day"]],
        "hero_alt": "Newsmaker headline maker screen showing a breaking-news style card being created",
        "marquee": ["MEETING CANCELED", "PACKAGE ARRIVED", "CONCERT TICKETS", "NEW PR", "FINAL OFFER", "LUNCH DECIDED", "STOCK UP", "VACATION APPROVED"],
        "how_kicker": "HOW IT WORKS",
        "how_h2": "From a normal sentence to a <em>front page</em> in three taps.",
        "steps": [
            ["HEADLINE", "Type one line", "Whatever happened today — big or small. That's your headline."],
            ["STYLE", "Pick a theme and font", "14 card themes from breaking-news red to newspaper broadsheet, 12 display fonts to match the mood."],
            ["SHARE", "Save and share", "Export as an image in the ratio you need and send it to the group chat."],
        ],
        "conv_kicker": "CONVERSION", "conv_num": "MUNDANE → BREAKING",
        "conv_h2": "Nothing happened. <em>Everything happened.</em>",
        "conv_lede": "Newsmaker takes the smallest events of your day and gives them the full breaking-news treatment — red banner, bold type, all caps.",
        "conv_rows": [
            ["Meeting canceled", "BREAKING: Meeting canceled", "OFFICE · RELIEF"],
            ["Package arrived", "BREAKING: Package arrived early", "DELIVERY · WIN"],
            ["PR maxed", "BREAKING: New PR — 500 total", "GYM · MILESTONE"],
            ["Got the job", "BREAKING: Final offer received", "CAREER · GOOD NEWS"],
        ],
        "styles_kicker": "STYLE", "styles_num": "YOURS TO MIX",
        "styles_h2": "14 themes. 12 fonts. <em>Endless front pages.</em>",
        "styles_lede": "Mix and match a look for every kind of news, and drop yourself into the story with a one-tap cut-out sticker.",
        "providers": [
            ["📰", "14 Card Themes", [["속", "Breaking News"], ["자", "Caption / Yellow"]]],
            ["🔤", "12 Display Fonts", [["Aa", "Impact / Serif"], ["가", "Handwriting / Round"]]],
            ["✂️", "Cut-out Sticker", [["👤", "Auto background removal"]]],
            ["🎯", "Interest Presets", [["🎮", "Student · Work · Gym · Gaming…"]]],
        ],
        "shots_kicker": "SCREENS", "shots_num": "IOS 26",
        "shots_h2": "Built for <em>fast, funny front pages</em>.",
        "shots_caps": ["14 THEMES", "12 FONTS", "MY LIBRARY"],
        "feat_kicker": "DETAILS", "feat_num": "06",
        "feat_h2": "One tap. <em>Every</em> tool.",
        "feats": [
            ["14 card themes", "Breaking news, broadcast caption, tabloid, newspaper, magazine, emergency alert and more."],
            ["12 display fonts", "Impact, handwriting, serif, bold rounded — every headline has a voice."],
            ["Cut-out photo sticker", "Auto background removal turns any photo into a sticker you can drop into the story."],
            ["Interest-based examples", "Student, office worker, fandom, gym, dating, pets, job hunting, gaming, stocks — ready-made lines to remix."],
            ["4 aspect ratios", "Square, feed 4:5, story 9:16, or widescreen 16:9 — export for wherever you're posting."],
            ["No account, no ads", "Everything happens on your device. Free, iPhone only, nothing to sign up for."],
        ],
        "final_h2": "Make today's breaking news.", "final_lede": "Free on iPhone.",
        "f_contact": "Contact", "f_privacy": "Privacy", "f_terms": "Terms",
        "flag_word": "BREAKING", "live_label": "LIVE · BROADCAST",
        "theme_lede": "Preview all 14 card themes like real news screens, then pick the font that matches your mood.",
        "theme_cards": [
            ["BREAKING", "BREAKING", "BREAKING: Meeting canceled"],
            ["CAPTION", "FUNNY CAPTION", "Package arrived early lol"],
            ["FRONT PAGE", "NEWS·MAKER GAZETTE", "Final offer received"],
            ["ALERT", "EMERGENCY ALERT", "New PR — 500 total"],
        ],
        "font_labels": ["Impact · Caps", "Serif · Italic", "Handwriting", "Bold Round"],
    },
    "ko": {
        "dir": "ko/", "lang": "ko", "font": '"Apple SD Gothic Neo", "Pretendard"',
        "title": "속보메이커 — 평범한 하루를 속보 짤로",
        "desc": "헤드라인 한 줄만 입력하면 속보메이커가 테마와 폰트를 입혀 공유용 짤로 만들어줍니다. 계정도 광고도 없이, 모든 처리는 기기 안에서. 아이폰 무료 앱.",
        "og_title": "속보메이커 — 속보 짤 제조기",
        "og_desc": "평범한 하루를 웃긴 속보 짤로, 몇 초 만에.",
        "kicker_num": "속보 짤 제조기",
        "h1": "평범한 하루도,<br>한 줄이면 <em>속보</em>가 된다",
        "pairs": [
            ["회의 취소", "속보: 회의 전격 취소"],
            ["택배 도착", "속보: 택배 하루 만에 도착"],
            ["오운완", "속보: 오운완 3대 500 달성"],
            ["최종 합격", "속보: 최종 합격 통보"],
        ],
        "sub": "오늘 있었던 일, 한 줄이면 충분해요. 속보메이커가 빨간 속보 배너 스타일로 바꿔줍니다. 테마 고르고, 폰트 고르고, 내 사진으로 누끼 스티커까지 붙여서 짤로 저장하세요.",
        "badge_small": "다운로드는", "note": "무료 · 아이폰 · 계정 불필요",
        "badge_aria": "App Store에서 다운로드",
        "chips": [["속", "회의취소"], ["속", "택배"], ["속", "티켓팅"], ["속", "오운완"]],
        "hero_alt": "속보메이커 헤드라인 제작 화면 — 속보 스타일 카드를 만드는 모습",
        "marquee": ["회의취소", "택배", "티켓팅", "오운완", "최종합격", "점심결정", "주식떡상", "휴가확정"],
        "how_kicker": "사용 방법",
        "how_h2": "평범한 한 줄이 <em>1면 속보</em>가 되기까지 세 번의 탭.",
        "steps": [
            ["헤드라인", "한 줄 입력", "오늘 있었던 일, 크든 작든 한 줄이면 헤드라인 완성."],
            ["스타일", "테마·폰트 고르기", "속보부터 신문 지면까지 14가지 테마, 분위기에 맞는 폰트 12종."],
            ["공유", "저장하고 공유", "필요한 비율로 이미지 저장해서 단톡방에 바로 투척."],
        ],
        "conv_kicker": "변환", "conv_num": "평범한 하루 → 속보",
        "conv_h2": "아무 일도 없었는데, <em>다 속보였다</em>.",
        "conv_lede": "속보메이커는 하루의 사소한 순간을 빨간 속보 배너, 굵은 글씨, 전체 대문자로 격상시켜줍니다.",
        "conv_rows": [
            ["회의 취소", "속보: 회의 전격 취소", "회사 · 안도"],
            ["택배 도착", "속보: 택배 하루 만에 도착", "택배 · 승리"],
            ["오운완", "속보: 오운완 3대 500 달성", "헬스 · 신기록"],
            ["최종 합격", "속보: 최종 합격 통보", "커리어 · 경사"],
        ],
        "styles_kicker": "스타일", "styles_num": "자유롭게 조합",
        "styles_h2": "테마 14종, 폰트 12종. <em>매번 다른 1면.</em>",
        "styles_lede": "뉴스 종류마다 다른 룩을 조합하고, 누끼 스티커로 내 얼굴을 뉴스 주인공으로 만드세요.",
        "providers": [
            ["📰", "카드 테마 14종", [["속", "속보 · 방송자막"], ["옐", "옐로 · 재난문자"]]],
            ["🔤", "폰트 12종", [["가", "임팩트 · 명조"], ["손", "손글씨 · 통통 라운드"]]],
            ["✂️", "누끼 스티커", [["👤", "배경 자동 제거"]]],
            ["🎯", "관심사별 예시", [["🎮", "학생 · 직장인 · 헬스 · 게임…"]]],
        ],
        "shots_kicker": "화면", "shots_num": "IOS 26",
        "shots_h2": "빠르고 웃긴 <em>1면 제작소</em>.",
        "shots_caps": ["테마 14종", "폰트 12종", "내 보관함"],
        "feat_kicker": "디테일", "feat_num": "06",
        "feat_h2": "탭 한 번에, <em>도구는 전부</em>.",
        "feats": [
            ["카드 테마 14종", "속보, 방송자막, 예능자막, 신문, 매거진, 재난문자 등 상황별 스타일."],
            ["디스플레이 폰트 12종", "임팩트, 손글씨, 명조, 통통 라운드 — 헤드라인마다 다른 목소리."],
            ["누끼 포토 스티커", "배경을 자동으로 제거해서 어떤 사진이든 뉴스 속 등장인물로 만들어줘요."],
            ["관심사별 예시", "학생·직장인·덕질·헬스·연애·반려동물·취준·게임·주식까지, 바로 쓰는 예시 문구."],
            ["4가지 비율", "정사각형, 피드 4:5, 스토리 9:16, 가로 16:9 — 올릴 곳에 맞춰 내보내기."],
            ["계정·광고 없음", "모든 처리는 내 기기 안에서. 무료, 아이폰 전용, 가입할 필요 없음."],
        ],
        "final_h2": "오늘의 속보를 만들어보세요.", "final_lede": "아이폰 무료.",
        "f_contact": "문의", "f_privacy": "개인정보 처리방침", "f_terms": "이용약관",
        "flag_word": "속보", "live_label": "LIVE · 생중계",
        "theme_lede": "14가지 카드 테마를 실제 뉴스 화면처럼 미리 보고, 나에게 맞는 폰트를 골라보세요.",
        "theme_cards": [
            ["속보", "BREAKING", "속보: 회의 전격 취소"],
            ["방송자막", "예능자막", "택배 하루 만에 도착 ㅋㅋ"],
            ["신문 · 1면", "NEWS·MAKER GAZETTE", "최종 합격 통보"],
            ["재난문자", "긴급재난문자", "오운완 3대 500 달성"],
        ],
        "font_labels": ["임팩트 · 대문자", "명조 · 이탤릭", "손글씨", "통통 라운드"],
    },
    "ja": {
        "dir": "ja/", "lang": "ja", "font": '"Hiragino Sans", "Hiragino Kaku Gothic ProN"',
        "title": "速報メーカー — 平凡な一日を速報ミームに",
        "desc": "見出しを一言入力するだけで、速報メーカーがテーマとフォントを添えてシェア用ミームに変換。アカウントも広告もなし、すべて端末内で処理。iPhone無料アプリ。",
        "og_title": "速報メーカー — 速報ミーム製造機",
        "og_desc": "平凡な一日を面白い速報ミームに、数秒で。",
        "kicker_num": "速報ミーム製造機",
        "h1": "平凡な一日も、<br>一言で<em>速報</em>になる",
        "pairs": [
            ["会議が急遽中止", "速報：会議が電撃中止"],
            ["荷物が1日早く到着", "速報：荷物が1日早く到着"],
            ["推しのカムバ確定", "速報：推しのカムバック決定"],
            ["内定獲得", "速報：内定を正式獲得"],
        ],
        "sub": "今日あったこと、一言で十分。速報メーカーが赤い速報バナー風に変換します。テーマを選び、フォントを選び、自分の切り抜き写真を貼り付けてミームとして保存しましょう。",
        "badge_small": "ダウンロードは", "note": "無料 · iPhone · アカウント不要",
        "badge_aria": "App Storeでダウンロード",
        "chips": [["速", "会議中止"], ["速", "推し活"], ["速", "バイト"], ["速", "筋トレ"]],
        "hero_alt": "速報メーカーの見出し作成画面 — 速報スタイルのカードを作成している様子",
        "marquee": ["会議中止", "推しのカムバ", "バイト時給アップ", "内定獲得", "ベンチプレス自己ベスト", "ランチ即決", "株爆益", "有給承認"],
        "how_kicker": "使い方",
        "how_h2": "普通の一文が<em>一面速報</em>になるまで、たった3タップ。",
        "steps": [
            ["見出し", "一言入力", "今日あったこと、大きくても小さくても一言でOK。それが見出しに。"],
            ["スタイル", "テーマとフォントを選ぶ", "速報レッドから新聞紙面風まで14種のカードテーマ、雰囲気に合わせた12種のフォント。"],
            ["共有", "保存してシェア", "必要な比率で画像として書き出し、グループLINEにそのまま投稿。"],
        ],
        "conv_kicker": "変換", "conv_num": "日常 → 速報",
        "conv_h2": "何もなかったのに、<em>全部速報だった</em>。",
        "conv_lede": "速報メーカーは一日の小さな出来事を、赤い速報バナー・太字・全角キャップスで格上げします。",
        "conv_rows": [
            ["会議が急遽中止", "速報：会議が電撃中止", "会社 · 安堵"],
            ["荷物が1日早く到着", "速報：荷物が1日早く到着", "宅配 · 勝利"],
            ["推しのカムバ確定", "速報：推しのカムバック決定", "推し活 · 歓喜"],
            ["内定獲得", "速報：内定を正式獲得", "就活 · 吉報"],
        ],
        "styles_kicker": "スタイル", "styles_num": "自由に組み合わせ",
        "styles_h2": "テーマ14種、フォント12種。<em>毎回ちがう一面。</em>",
        "styles_lede": "ニュースの種類ごとに違うルックを組み合わせ、切り抜きステッカーで自分を主役にしよう。",
        "providers": [
            ["📰", "カードテーマ14種", [["速", "速報 · 放送字幕"], ["緊", "緊急速報 · 号外"]]],
            ["🔤", "フォント12種", [["Aa", "インパクト · 明朝"], ["手", "手書き · 丸ゴシック"]]],
            ["✂️", "切り抜きステッカー", [["👤", "背景自動除去"]]],
            ["🎯", "関心事別の例文", [["🎮", "学生 · 会社員 · 推し活 · ゲーム…"]]],
        ],
        "shots_kicker": "画面", "shots_num": "IOS 26",
        "shots_h2": "速くて面白い<em>一面制作所</em>。",
        "shots_caps": ["テーマ14種", "フォント12種", "マイライブラリ"],
        "feat_kicker": "詳細", "feat_num": "06",
        "feat_h2": "タップひとつ、<em>全部そろう</em>。",
        "feats": [
            ["カードテーマ14種", "速報、放送字幕、バラエティ字幕、新聞、雑誌、緊急速報など状況別スタイル。"],
            ["ディスプレイフォント12種", "インパクト、手書き、明朝、丸ゴシック — 見出しごとに違う声。"],
            ["切り抜きフォトステッカー", "背景を自動で除去して、どんな写真もニュースの登場人物に。"],
            ["関心事別の例文", "学生・会社員・推し活・筋トレ・恋愛・ペット・就活・ゲーム・株まで、すぐ使える例文。"],
            ["4種のアスペクト比", "正方形、フィード4:5、ストーリー9:16、横長16:9 — 投稿先に合わせて書き出し。"],
            ["アカウント・広告なし", "すべて端末内で処理。無料、iPhone専用、登録不要。"],
        ],
        "final_h2": "今日の速報を作ろう。", "final_lede": "iPhone無料。",
        "f_contact": "お問い合わせ", "f_privacy": "プライバシーポリシー", "f_terms": "利用規約",
        "flag_word": "速報", "live_label": "LIVE · 生中継",
        "theme_lede": "14種のカードテーマを実際のニュース画面のようにプレビューし、気分に合うフォントを選んでみて。",
        "theme_cards": [
            ["速報", "BREAKING", "速報：会議が電撃中止"],
            ["放送字幕", "バラエティ字幕", "荷物が1日早く到着 www"],
            ["新聞 · 一面", "NEWS·MAKER GAZETTE", "内定を正式獲得"],
            ["緊急速報", "緊急速報", "推しのカムバック決定"],
        ],
        "font_labels": ["インパクト · 大文字", "明朝 · イタリック", "手書き", "丸ゴシック"],
    },
    "zh-Hant": {
        "dir": "zh-hant/", "lang": "zh-Hant", "font": '"PingFang TC", "Microsoft JhengHei"',
        "title": "快訊製造機 — 把平凡的一天變成快訊迷因",
        "desc": "只要輸入一句標題，快訊製造機就會套上主題和字型，做成可以分享的迷因。不需帳號、沒有廣告，全程在裝置端處理。iPhone 免費下載。",
        "og_title": "快訊製造機 — 快訊迷因製造機",
        "og_desc": "把平凡的一天變成爆笑快訊，只要幾秒鐘。",
        "kicker_num": "快訊迷因製造機",
        "h1": "平凡的一天，<br>一句話就是<em>快訊</em>",
        "pairs": [
            ["會議臨時取消", "快訊：會議臨時取消"],
            ["包裹提早一天到", "快訊：包裹提早一天送達"],
            ["搶票成功", "快訊：演唱會門票搶票成功"],
            ["最終錄取", "快訊：正式收到錄取通知"],
        ],
        "sub": "今天發生的事，一句話就夠了。快訊製造機會把它變成紅色快訊橫幅風格 — 選主題、選字型、貼上自己的去背照片，存成迷因就完成。",
        "badge_small": "下載請至", "note": "免費 · iPhone · 免帳號",
        "badge_aria": "在 App Store 下載",
        "chips": [["快", "會議取消"], ["快", "追星"], ["快", "打工"], ["快", "健身"]],
        "hero_alt": "快訊製造機標題製作畫面 — 正在製作快訊風格卡片",
        "marquee": ["會議取消", "搶票成功", "打工時薪調漲", "最終錄取", "臥推破紀錄", "午餐秒決定", "股票大賺", "特休核准"],
        "how_kicker": "使用方式",
        "how_h2": "一句平凡的話變成<em>頭版快訊</em>，只要三個步驟。",
        "steps": [
            ["標題", "輸入一句話", "今天發生的事，不論大小，一句話就是標題。"],
            ["風格", "選主題和字型", "從快訊紅到報紙版面，14 種卡片主題，12 種字型任你搭配心情。"],
            ["分享", "儲存並分享", "依需求比例輸出成圖片，直接丟進群組聊天室。"],
        ],
        "conv_kicker": "轉換", "conv_num": "日常 → 快訊",
        "conv_h2": "什麼都沒發生，<em>卻都是快訊</em>。",
        "conv_lede": "快訊製造機把一天中最微不足道的瞬間，升級成紅色橫幅、粗體大字、全大寫的正式快訊。",
        "conv_rows": [
            ["會議臨時取消", "快訊：會議臨時取消", "上班 · 鬆一口氣"],
            ["包裹提早一天到", "快訊：包裹提早一天送達", "宅配 · 小確幸"],
            ["搶票成功", "快訊：演唱會門票搶票成功", "追星 · 狂喜"],
            ["最終錄取", "快訊：正式收到錄取通知", "求職 · 喜訊"],
        ],
        "styles_kicker": "風格", "styles_num": "自由混搭",
        "styles_h2": "14 種主題、12 種字型。<em>每次都是不同頭版。</em>",
        "styles_lede": "為每一種新聞混搭不同的風格，再用一鍵去背貼圖把自己變成新聞主角。",
        "providers": [
            ["📰", "14 種卡片主題", [["快", "快訊 · 跑馬燈字幕"], ["急", "緊急快訊 · 號外"]]],
            ["🔤", "12 種字型", [["Aa", "粗黑體 · 明體"], ["手", "手寫 · 圓體"]]],
            ["✂️", "去背貼圖", [["👤", "自動去背"]]],
            ["🎯", "興趣主題範例", [["🎮", "學生 · 上班族 · 追星 · 遊戲…"]]],
        ],
        "shots_kicker": "畫面", "shots_num": "IOS 26",
        "shots_h2": "又快又好笑的<em>頭版製造機</em>。",
        "shots_caps": ["14 種主題", "12 種字型", "我的收藏"],
        "feat_kicker": "細節", "feat_num": "06",
        "feat_h2": "點一下，<em>工具全都有</em>。",
        "feats": [
            ["14 種卡片主題", "快訊、跑馬燈字幕、綜藝字幕、報紙、雜誌、緊急快訊等情境風格。"],
            ["12 種顯示字型", "粗黑體、手寫、明體、圓體 — 每則標題都有自己的語氣。"],
            ["去背照片貼圖", "自動去背，讓任何照片都能變成新聞裡的主角。"],
            ["興趣主題範例", "學生、上班族、追星、健身、戀愛、寵物、求職、遊戲、股票，現成句子直接套用。"],
            ["4 種長寬比", "正方形、動態消息 4:5、限時動態 9:16、橫式 16:9 — 依發佈平台輸出。"],
            ["免帳號、無廣告", "所有處理都在裝置端完成。免費、僅限 iPhone，不需註冊。"],
        ],
        "final_h2": "來製作今天的快訊吧。", "final_lede": "iPhone 免費。",
        "f_contact": "聯絡我們", "f_privacy": "隱私權政策", "f_terms": "使用條款",
        "flag_word": "快訊", "live_label": "LIVE · 現場直擊",
        "theme_lede": "像真實新聞畫面一樣預覽全部 14 種卡片主題，再選出符合心情的字型。",
        "theme_cards": [
            ["快訊", "BREAKING", "快訊：會議臨時取消"],
            ["跑馬燈字幕", "綜藝字幕", "包裹提早一天到 XD"],
            ["報紙 · 頭版", "NEWS·MAKER GAZETTE", "正式收到錄取通知"],
            ["緊急快訊", "緊急快訊", "演唱會門票搶票成功"],
        ],
        "font_labels": ["粗黑體 · 大寫", "明體 · 斜體", "手寫", "圓體"],
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
    chip_stack = "".join(
        f'<div class="chip"><span class="g">{g}</span>{label}</div>'
        for g, label in loc["chips"]
    )
    ticker_track = "".join(f"<span>{m}</span>" for m in loc["marquee"] * 2)
    steps = "".join(
        f'<div class="step"><span class="n">0{i+1}</span><span class="tag">{tag}</span><h3>{h}</h3><p>{p}</p></div>'
        for i, (tag, h, p) in enumerate(loc["steps"])
    )
    conv = "".join(
        f'<div class="convert-row"><span>{a}</span><span class="arrow">→</span><span class="to">{b}</span><span class="cat">{c}</span></div>'
        for a, b, c in loc["conv_rows"]
    )
    np_articles = "".join(
        f'<div class="np-article"><span class="cat">{cat}</span><h3>{b}</h3><p>{loc["steps"][i][2]}</p></div>'
        for i, (a, b, cat) in enumerate(loc["conv_rows"][:3])
    )
    theme_classes = ["tc-breaking", "tc-chyron", "tc-paper", "tc-alert"]
    theme_cards = "".join(
        f'<div class="theme-card {cls}"><span class="tc-label">{label}</span>'
        f'<div class="tc-content"><span class="bar">{bar}</span><div class="headline">{headline}</div></div></div>'
        for cls, (label, bar, headline) in zip(theme_classes, loc["theme_cards"])
    )
    font_classes = ["", "f2", "f3", "f4"]
    glyph_sample = {"ko": "가나다", "ja": "あア速報", "zh-Hant": "快訊繁"}.get(loc["lang"], "Aa Bb")
    font_cards = "".join(
        f'<div class="font-card {cls}"><div class="glyph">{glyph_sample}</div><div class="lbl">{lbl}</div></div>'
        for cls, lbl in zip(font_classes, loc["font_labels"])
    )
    provs = "".join(
        '<div><span class="flag">%s</span><h3>%s</h3><ul>%s</ul></div>'
        % (flag, name, "".join(f'<li><span class="g">{g}</span>{n}</li>' for g, n in items))
        for flag, name, items in loc["providers"]
    )
    shot_files = ["2-theme", "3-font", "4-gallery"]
    shots = "".join(
        f'<figure><div class="phone"><img src="{rel}assets/shot-{f}.png" alt="{cap}" loading="lazy"><div class="island"></div></div><figcaption>{cap}</figcaption></figure>'
        for f, cap in zip(shot_files, loc["shots_caps"])
    )
    feats = "".join(f'<div class="feat"><h3>{h}</h3><p>{p}</p></div>' for h, p in loc["feats"])
    feat_h2 = loc["feat_h2"].replace("<em>", '<em style="color:var(--red); font-style:normal;">')
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

<div class="ticker-bar">
  <div class="ticker-flag"><span class="dot"></span>{loc['flag_word']}</div>
  <div class="ticker-viewport">
    <div class="ticker-track">{ticker_track}</div>
  </div>
</div>

<nav>
  <div class="wrap">
    <a class="wordmark" href="{rel if rel else './'}"><img src="{rel}assets/icon-180.png" alt=""><span>NEWS·MAKER</span></a>
    <div class="lang">{lang_nav(loc['dir'], rel)}</div>
  </div>
</nav>

<header class="hero">
  <div class="breaking-strip">
    <span class="badge"><span>{loc['flag_word']}</span></span>
    <span class="kicker-txt">{loc['kicker_num']} &nbsp;·&nbsp; NEWS · MAKER</span>
  </div>
  <div class="wrap">
    <div class="hero-grid">
      <div>
        <h1>{loc['h1']}</h1>

        <div class="chyron">
          <div class="chyron-top"><span>{loc['live_label']}</span><span>NEWS·MAKER</span></div>
          <div class="chyron-body">
            <span class="src" id="demoSrc">{loc['pairs'][0][0]}</span>
            <span class="dst" id="demoDst" data-flag="{loc['flag_word']}">{loc['pairs'][0][1]}</span>
          </div>
        </div>

        <p class="sub">{loc['sub']}</p>
        <div class="cta">
          {badge(loc, 'storeLink')}
          <span class="note">{loc['note']}</span>
        </div>
      </div>
      <div class="phone-col">
        <div class="chip-stack">{chip_stack}</div>
        <div class="phone"><img src="{rel}assets/shot-1-hero.png" alt="{loc['hero_alt']}"><div class="island"></div></div>
      </div>
    </div>
  </div>
</header>

<div class="chyron-divider">
  <div class="wrap inner">
    <span class="num">01–03</span>
    <div><h2>{loc['how_h2']}</h2></div>
  </div>
</div>

<section>
  <div class="wrap">
    <div class="steps">{steps}</div>
  </div>
</section>

<div class="chyron-divider">
  <div class="wrap inner">
    <span class="num">{loc['conv_num']}</span>
    <div>
      <h2>{loc['conv_h2']}</h2>
      <p class="sub-lede">{loc['conv_lede']}</p>
    </div>
  </div>
</div>

<section>
  <div class="wrap">
    <div class="convert-table">{conv}</div>
  </div>
</section>

<div class="newspaper-wrap">
  <div class="wrap">
    <div class="newspaper">
      <div class="np-masthead">
        <div class="kicker-row"><span>{loc['styles_kicker']} · {loc['styles_num']}</span><span>NEWS·MAKER GAZETTE</span></div>
        <h2>{loc['styles_h2']}</h2>
        <div class="dateline">{loc['styles_lede']}</div>
      </div>
    </div>
  </div>
</div>

<section>
  <div class="wrap">
    <p class="style-lede">{loc['theme_lede']}</p>
    <div class="theme-grid">{theme_cards}</div>
    <div class="font-grid">{font_cards}</div>
    <div class="prov">{provs}</div>
  </div>
</section>

<div class="chyron-divider">
  <div class="wrap inner">
    <span class="num">{loc['shots_num']}</span>
    <div><h2>{loc['shots_h2']}</h2></div>
  </div>
</div>

<section class="shots">
  <div class="wrap">
    <div class="row">{shots}</div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="kicker-num" style="color:#333; opacity:1;"><span>{loc['feat_kicker']}</span><span class="rule" style="background:#999;"></span><span>{loc['feat_num']}</span></div>
    <h2 style="color:var(--ink); font-weight:900; font-size:clamp(24px,3.6vw,36px); margin-bottom:20px;">{feat_h2}</h2>
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
      <a href="https://www.kkirukstudio.com/legal/privacy/">{loc['f_privacy']}</a>
      <a href="https://www.kkirukstudio.com/legal/terms/">{loc['f_terms']}</a>
    </div>
    <div>© 2026 kkiruk studio</div>
  </div>
</footer>

<script src="/ga.js"></script>
<script>
  // After App Store approval, set the real URL here (e.g. https://apps.apple.com/app/id1234567890)
  const APP_STORE_URL = "https://apps.apple.com/app/id6787015246";
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
</body>
</html>
"""
    out = ROOT / loc["dir"] / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)} ({len(html)} bytes)")


for key in LOCALES:
    render(key)
