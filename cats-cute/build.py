#!/usr/bin/env python3
"""Cats are Cute landing page generator.

Generates index.html (en) + 12 flat <lang>.html files (paths must stay —
ASC/Play marketing URLs reference them). All cat names, dialogue lines and
rarity labels in game_data.json come from the actual game data
(StreamingAssets cat_info_* / dialogue_info_*, decrypted) — do not invent
content there, re-extract instead.

Usage: python3 build.py
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).parent
BASE_URL = "https://www.kkirukstudio.com/cats-cute/"
APPSTORE_URL = "https://apps.apple.com/app/id1395888987"
PLAY_URL = "https://play.google.com/store/apps/details?id=com.game.kkiruk.myadorablecats"
OG_IMAGE = "https://www.kkirukstudio.com/icons/cats-cute.png"

GAME = json.loads((ROOT / "game_data.json").read_text(encoding="utf-8"))

APPLE_SVG = '<svg viewBox="0 0 384 512" aria-hidden="true"><path d="M318.7 268.7c-.2-36.7 16.4-64.4 50-84.8-18.8-26.9-47.2-41.7-84.7-44.6-35.5-2.8-74.3 20.7-88.5 20.7-15 0-49.4-19.7-76.4-19.7C63.3 141.2 4 184.8 4 273.5q0 39.3 14.4 81.2c12.8 36.7 59 126.7 107.2 125.2 25.2-.6 43-17.9 75.8-17.9 31.8 0 48.3 17.9 76.4 17.9 48.6-.7 90.4-82.5 102.6-119.3-65.2-30.7-61.7-90-61.7-91.9zm-56.6-164.2c27.3-32.4 24.8-61.9 24-72.5-24.1 1.4-52 16.4-67.9 34.9-17.5 19.8-27.8 44.3-25.6 71.9 26.1 2 49.9-11.4 69.5-34.3z"/></svg>'
PLAY_SVG = '<svg viewBox="0 0 512 512" aria-hidden="true"><path d="M325.3 234.3 104.6 13l280.8 161.2-60.1 60.1zM47 0C34 6.8 25.3 19.2 25.3 35.3v441.3c0 16.1 8.7 28.5 21.7 35.3l256.6-256L47 0zm425.2 225.6-58.9-34.1-65.7 64.5 65.7 64.5 60.1-34.1c18-14.3 18-46.5-1.2-60.8zM104.6 499l280.8-161.2-60.1-60.1L104.6 499z"/></svg>'

# Cats shown face-up in the collection grid (mix of rarities), the rest of
# the 41 extracted cats form the tap-to-draw pool.
GRID_SPRITES = ["cat001", "cat021", "cat016", "cat007", "cat104", "cat113",
                "cat115", "cat118", "cat201", "cat210", "cat213", "cat302"]
UNKNOWN_SLOTS = 6
# Hero demo speakers, paired index-by-index with game_data lines[0..7]
DEMO_SPRITES = ["cat001", "cat021", "cat104", "cat115", "cat201", "cat210", "cat302", "cat016"]
CHIP_SPRITES = ["cat021", "cat104", "cat302"]
MARQUEE_SPRITES = ["cat001", "cat003", "cat007", "cat010", "cat011", "cat015",
                   "cat016", "cat021", "cat104", "cat106", "cat109", "cat113",
                   "cat114", "cat115", "cat118", "cat201", "cat206", "cat210",
                   "cat213", "cat221", "cat302", "cat020"]

SKYLINE = [("tree2_3", 120), ("bed", 56), ("piano", 62), ("__cat:cat104", 38),
           ("ball", 26), ("basket3", 46), ("cart1", 56), ("flowers", 36),
           ("chimney1", 64), ("__cat:cat302", 38), ("tree4_3", 96)]

LANG_OPTIONS = [("ko.html", "한국어"), ("index.html", "EN"), ("ja.html", "日本語"),
                ("zh-hans.html", "简体中文"), ("zh-hant.html", "繁體中文"),
                ("es.html", "Español"), ("pt.html", "Português"), ("de.html", "Deutsch"),
                ("fr.html", "Français"), ("ru.html", "Русский"), ("th.html", "ไทย"),
                ("id.html", "Bahasa Indonesia"), ("vi.html", "Tiếng Việt")]

HREFLANGS = [("ko", "ko.html"), ("en", "index.html"), ("ja", "ja.html"),
             ("zh-Hans", "zh-hans.html"), ("zh-Hant", "zh-hant.html"),
             ("es", "es.html"), ("pt", "pt.html"), ("de", "de.html"),
             ("fr", "fr.html"), ("ru", "ru.html"), ("th", "th.html"),
             ("id", "id.html"), ("vi", "vi.html")]

LOCALES = {
    "en": {
        "file": "index.html", "lang": "en", "font": None, "shots": "en",
        "name": "Cats are Cute",
        "title": "Cats are Cute — A hand-drawn village of collectible cats",
        "desc": "A calm idle game loved since 2018. Collect 60+ hand-drawn cats, feed them, and grow a cozy ink-line village. ★4.9 · 71,000+ reviews · free on iOS & Android.",
        "og_title": "Cats are Cute — Idle Cat Village",
        "og_desc": "A village drawn in ink, where only the cats are in color. ★4.9 · 71,000+ reviews.",
        "kicker_num": "IDLE CAT VILLAGE · SINCE 2018",
        "h1": "A village drawn in ink.<br><em>Only the cats are in color.</em>",
        "sub": "Collect 60+ cats — each with a name, a personality and something to say. Feed them, grow your village, and let rewards stack while you're away. Ads only when you choose to watch.",
        "demo_kicker": "LISTEN TO THE CATS",
        "ios_small": "Download on the", "play_small": "GET IT ON",
        "note": "FREE · IOS &amp; ANDROID · NO FORCED ADS",
        "hero_alt": "Cats are Cute gameplay — an ink-drawn village with a cat speaking in a word box",
        "stats": [["<em>★</em>4.9", "App Store rating"], ["71,000+", "Store reviews"], ["10M+", "Downloads"], ["2018", "Running since"]],
        "how_kicker": "HOW IT WORKS", "how_num": "01–03",
        "how_h2": "Feed. Collect. <em>Watch it grow.</em>",
        "steps": [
            ["FEED", "Serve fish, earn hearts", "Buildings produce fish on their own. Feed the cats and collect hearts to level up your village.", "catfish"],
            ["COLLECT", "Draw new cats", "Use draw tickets to meet new cats — Normal, Rare and Epic, each with its own face and habits.", "gachaticket"],
            ["GROW", "Build your village", "Upgrade buildings and fill the ink-line town with cozy spots for the cats to claim.", "building"],
        ],
        "col_kicker": "CAT COLLECTION", "col_num": "60+ CATS",
        "col_h2": "Every cat has a name.<br><em>And opinions.</em>",
        "col_lede": "These are real cats from the game — names, rarities and all. Tap a hidden card to draw one, just like the in-game gacha.",
        "col_hint": "TAP A CARD TO DRAW",
        "shots_kicker": "SCREENS", "shots_num": "IN-GAME",
        "shots_h2": "The village, <em>as it actually looks.</em>",
        "shots_caps": ["LISTEN TO THE CATS", "FEED THE CATS", "PLAY WITH THE CATS"],
        "feat_kicker": "DETAILS", "feat_num": "06",
        "feat_h2": "Calm by design. <em>For seven years.</em>",
        "feats": [
            ["True idle", "Progress keeps stacking while the app is closed. A few minutes a day is plenty.", "catgrass"],
            ["No forced ads", "Nothing interrupts you. Watch an ad only when you want the bonus.", "heart"],
            ["60+ personalities", "Each cat has a name, a personality and favorite things to do around town.", "cat"],
            ["A town to decorate", "Upgrade buildings and dress up every corner of the village.", "building"],
            ["13 languages", "Loved in Japan, the US, Korea, Vietnam, Taiwan and far beyond.", "collection"],
            ["7 years of care", "Run by a tiny indie studio since 2018 — ★4.9 across 71,000+ reviews.", "toy"],
        ],
        "final_h2": "The cats are waiting for you today, too.",
        "final_lede": "Free on iOS &amp; Android.",
        "f_contact": "Contact", "f_privacy": "Privacy", "f_terms": "Terms",
    },
    "ko": {
        "file": "ko.html", "lang": "ko", "font": '"Apple SD Gothic Neo","Pretendard"', "shots": "ko",
        "name": "고양이는 정말 귀여워",
        "title": "고양이는 정말 귀여워 — 잉크로 그린 고양이 마을 키우기",
        "desc": "2018년부터 사랑받아온 힐링 방치 게임. 손그림 고양이 60+마리를 모아 잉크 라인 마을을 키워보세요. ★4.9 · 리뷰 71,000+ · iOS & Android 무료.",
        "og_title": "고양이는 정말 귀여워 — 고양이 마을 키우기",
        "og_desc": "잉크로 그린 마을, 색은 고양이뿐. ★4.9 · 리뷰 71,000+.",
        "kicker_num": "고양이 마을 방치 게임 · SINCE 2018",
        "h1": "잉크로 그린 마을,<br><em>색은 고양이뿐.</em>",
        "sub": "이름도, 성격도, 할 말도 있는 고양이 60+마리. 밥을 주고 마을을 키우다 보면, 자리를 비운 사이에도 보상이 쌓입니다. 광고는 내가 보고 싶을 때만.",
        "demo_kicker": "고양이의 말에 귀 기울여 보세요",
        "ios_small": "다운로드는", "play_small": "다운로드는",
        "note": "무료 · iOS &amp; Android · 강제 광고 없음",
        "hero_alt": "고양이는 정말 귀여워 플레이 화면 — 잉크로 그린 마을과 말풍선 속 고양이",
        "stats": [["<em>★</em>4.9", "앱스토어 평점"], ["71,000+", "전 세계 리뷰"], ["10M+", "누적 다운로드"], ["2018", "서비스 시작"]],
        "how_kicker": "이렇게 놀아요", "how_num": "01–03",
        "how_h2": "밥 주고, 모으고, <em>마을이 자라요.</em>",
        "steps": [
            ["밥 주기", "생선 주고 하트 받기", "건물이 알아서 생선을 만들어요. 고양이에게 밥을 주고 하트를 모아 마을 레벨을 올려요.", "catfish"],
            ["뽑기", "새 고양이 만나기", "뽑기 티켓으로 새 고양이를 만나요. 일반·레어·에픽, 얼굴도 습관도 다 달라요.", "gachaticket"],
            ["꾸미기", "나만의 마을 만들기", "건물을 업그레이드하고 구석구석 꾸미면, 고양이들이 제자리처럼 찾아와 앉아요.", "building"],
        ],
        "col_kicker": "고양이 도감", "col_num": "60+ 마리",
        "col_h2": "고양이마다 이름이 있어요.<br><em>할 말도요.</em>",
        "col_lede": "전부 게임 속 진짜 고양이들이에요 — 이름도 등급도 그대로. 가려진 카드를 탭하면 게임 속 뽑기처럼 새 고양이가 나와요.",
        "col_hint": "카드를 탭해서 뽑아보세요",
        "shots_kicker": "스크린샷", "shots_num": "인게임",
        "shots_h2": "마을은 <em>실제로 이렇게 생겼어요.</em>",
        "shots_caps": ["고양이의 이야기 듣기", "고양이 밥 주기", "고양이랑 놀기"],
        "feat_kicker": "디테일", "feat_num": "06",
        "feat_h2": "7년째, <em>조용하게 다정하게.</em>",
        "feats": [
            ["진짜 방치형", "앱을 꺼도 보상은 계속 쌓여요. 하루 몇 분이면 충분해요.", "catgrass"],
            ["강제 광고 없음", "아무것도 끼어들지 않아요. 보너스가 필요할 때만 내가 선택해서 봐요.", "heart"],
            ["60+마리, 60+가지 성격", "고양이마다 이름과 성격, 마을에서 즐기는 취미가 따로 있어요.", "cat"],
            ["꾸미는 재미", "건물을 올리고 장식을 놓아 마을 구석구석을 내 취향으로.", "building"],
            ["13개 언어", "일본·미국·한국·베트남·대만… 전 세계에서 사랑받고 있어요.", "collection"],
            ["7년의 운영", "2018년부터 1인 인디 스튜디오가 꾸준히 — ★4.9, 리뷰 71,000+.", "toy"],
        ],
        "final_h2": "오늘도 고양이들이 기다리고 있어요.",
        "final_lede": "iOS &amp; Android 무료.",
        "f_contact": "문의", "f_privacy": "개인정보 처리방침", "f_terms": "이용약관",
    },
    "ja": {
        "file": "ja.html", "lang": "ja", "font": '"Hiragino Kaku Gothic ProN","Hiragino Sans","Yu Gothic"', "shots": "ja",
        "name": "ねこはほんとかわいい",
        "title": "ねこはほんとかわいい — インクで描いたねこの村を育てる",
        "desc": "2018年から愛される癒やしの放置ゲーム。手描きのねこ60匹以上を集めて、インクの線で描かれた村を育てよう。★4.9 · レビュー71,000+ · iOS & Android 無料。",
        "og_title": "ねこはほんとかわいい — ねこの村育成",
        "og_desc": "インクで描いた村。色があるのは、ねこだけ。★4.9 · レビュー71,000+。",
        "kicker_num": "ねこの村 放置ゲーム · SINCE 2018",
        "h1": "インクで描いた村。<br><em>色があるのは、ねこだけ。</em>",
        "sub": "名前も性格も、言いたいことまである60匹以上のねこたち。ごはんをあげて村を育てれば、離れている間も報酬は貯まります。広告は見たいときだけ。",
        "demo_kicker": "ねこの話を聞いてみて",
        "ios_small": "ダウンロードは", "play_small": "ダウンロードは",
        "note": "無料 · iOS &amp; Android · 強制広告なし",
        "hero_alt": "ねこはほんとかわいいのプレイ画面 — インクで描かれた村と、ふきだしで話すねこ",
        "stats": [["<em>★</em>4.9", "App Store評価"], ["71,000+", "世界のレビュー"], ["10M+", "累計ダウンロード"], ["2018", "サービス開始"]],
        "how_kicker": "あそびかた", "how_num": "01–03",
        "how_h2": "ごはんをあげて、集めて、<em>村が育つ。</em>",
        "steps": [
            ["ごはん", "お魚をあげてハートをもらう", "建物が自動でお魚を作ってくれます。ねこにごはんをあげて、ハートを集めて村をレベルアップ。", "catfish"],
            ["ガチャ", "新しいねこに出会う", "チケットでガチャを引いて新しいねこと出会おう。ノーマル・レア・エピック、顔もクセもみんな違う。", "gachaticket"],
            ["村づくり", "自分だけの村を", "建物をアップグレードして飾り付ければ、ねこたちがお気に入りの場所みたいに集まってきます。", "building"],
        ],
        "col_kicker": "ねこ図鑑", "col_num": "60+ 匹",
        "col_h2": "どのねこにも名前がある。<br><em>言い分もある。</em>",
        "col_lede": "ぜんぶゲームに本当にいるねこたち — 名前もレアリティもそのまま。隠れたカードをタップすると、ゲーム内ガチャみたいに新しいねこが出てきます。",
        "col_hint": "カードをタップしてガチャ",
        "shots_kicker": "スクリーンショット", "shots_num": "ゲーム画面",
        "shots_h2": "村は<em>実際こんな見た目です。</em>",
        "shots_caps": ["ねこの話を聞く", "ねこにごはん", "ねこと遊ぶ"],
        "feat_kicker": "こだわり", "feat_num": "06",
        "feat_h2": "7年間、<em>静かにやさしく。</em>",
        "feats": [
            ["ほんとうの放置型", "アプリを閉じても報酬は貯まり続ける。1日数分で十分。", "catgrass"],
            ["強制広告なし", "何も割り込みません。ボーナスがほしいときだけ、自分で選んで見る。", "heart"],
            ["60匹以上の個性", "ねこごとに名前と性格、村でのお気に入りの過ごし方があります。", "cat"],
            ["飾る楽しみ", "建物を育てて、村のすみずみまで自分好みに。", "building"],
            ["13言語対応", "日本・アメリカ・韓国・ベトナム・台湾…世界中で愛されています。", "collection"],
            ["7年の運営", "2018年から小さなインディースタジオがこつこつと — ★4.9、レビュー71,000+。", "toy"],
        ],
        "final_h2": "今日もねこたちが待っています。",
        "final_lede": "iOS &amp; Android 無料。",
        "f_contact": "お問い合わせ", "f_privacy": "プライバシーポリシー", "f_terms": "利用規約",
    },
    "zh-hans": {
        "file": "zh-hans.html", "lang": "zh-Hans", "font": '"PingFang SC","Heiti SC"', "shots": "zh-hans",
        "name": "猫咪真的很可爱",
        "title": "猫咪真的很可爱 — 养一座墨线画成的猫咪小村",
        "desc": "自2018年起备受喜爱的治愈系放置游戏。收集60+只手绘猫咪，养大一座墨线小村。★4.9 · 71,000+条评价 · iOS & Android 免费。",
        "og_title": "猫咪真的很可爱 — 猫咪小村放置游戏",
        "og_desc": "一座墨线画成的小村，只有猫咪是彩色的。★4.9 · 71,000+条评价。",
        "kicker_num": "猫咪小村放置游戏 · SINCE 2018",
        "h1": "一座墨线画成的小村，<br><em>只有猫咪是彩色的。</em>",
        "sub": "60+只猫咪，每只都有名字、性格，还有想说的话。喂喂猫、养养村，离开的时候奖励也会自己累积。广告只在你想看时才出现。",
        "demo_kicker": "听听猫咪在说什么",
        "ios_small": "下载于", "play_small": "下载于",
        "note": "免费 · iOS &amp; Android · 无强制广告",
        "hero_alt": "猫咪真的很可爱游戏画面 — 墨线小村和对话框里说话的猫咪",
        "stats": [["<em>★</em>4.9", "App Store 评分"], ["71,000+", "全球评价"], ["10M+", "累计下载"], ["2018", "上线至今"]],
        "how_kicker": "玩法", "how_num": "01–03",
        "how_h2": "喂猫、收集,<em>小村慢慢长大。</em>",
        "steps": [
            ["喂食", "喂小鱼、攒爱心", "建筑会自动生产小鱼。给猫咪喂食、收集爱心，提升小村等级。", "catfish"],
            ["抽猫", "认识新猫咪", "用抽奖券抽新猫咪——普通、稀有、史诗，每只的长相和习惯都不一样。", "gachaticket"],
            ["建设", "打造自己的小村", "升级建筑、添置装饰，猫咪们会把每个角落当成自己的地盘。", "building"],
        ],
        "col_kicker": "猫咪图鉴", "col_num": "60+ 只",
        "col_h2": "每只猫都有名字,<br><em>也有自己的想法。</em>",
        "col_lede": "这些都是游戏里真实存在的猫咪——名字和稀有度原封不动。点一下盖住的卡片，就像游戏里抽猫一样。",
        "col_hint": "点卡片抽一只",
        "shots_kicker": "截图", "shots_num": "游戏画面",
        "shots_h2": "小村<em>真实的样子。</em>",
        "shots_caps": ["听猫咪说话", "给猫咪喂食", "陪猫咪玩耍"],
        "feat_kicker": "细节", "feat_num": "06",
        "feat_h2": "七年如一日,<em>安静又温柔。</em>",
        "feats": [
            ["真正的放置", "关掉应用奖励也在累积，每天几分钟就够了。", "catgrass"],
            ["无强制广告", "没有任何打扰。想要奖励时，自己选择看广告。", "heart"],
            ["60+种性格", "每只猫都有名字、性格和在村里最爱做的事。", "cat"],
            ["装扮乐趣", "升级建筑、摆放装饰，把小村的每个角落变成你的风格。", "building"],
            ["13种语言", "日本、美国、韩国、越南、台湾……全球玩家都在玩。", "collection"],
            ["七年运营", "2018年至今由独立小工作室用心维护——★4.9，71,000+条评价。", "toy"],
        ],
        "final_h2": "今天，猫咪们也在等你。",
        "final_lede": "iOS &amp; Android 免费。",
        "f_contact": "联系我们", "f_privacy": "隐私政策", "f_terms": "服务条款",
    },
    "zh-hant": {
        "file": "zh-hant.html", "lang": "zh-Hant", "font": '"PingFang TC","Heiti TC"', "shots": "zh-hant",
        "name": "貓咪真的很可愛",
        "title": "貓咪真的很可愛 — 養一座墨線畫成的貓咪小村",
        "desc": "自2018年起深受喜愛的療癒系放置遊戲。收集60+隻手繪貓咪，養大一座墨線小村。★4.9 · 71,000+則評價 · iOS & Android 免費。",
        "og_title": "貓咪真的很可愛 — 貓咪小村放置遊戲",
        "og_desc": "一座墨線畫成的小村，只有貓咪是彩色的。★4.9 · 71,000+則評價。",
        "kicker_num": "貓咪小村放置遊戲 · SINCE 2018",
        "h1": "一座墨線畫成的小村，<br><em>只有貓咪是彩色的。</em>",
        "sub": "60+隻貓咪，每隻都有名字、個性，還有想說的話。餵餵貓、養養村，離開的時候獎勵也會自己累積。廣告只在你想看時才出現。",
        "demo_kicker": "聽聽貓咪在說什麼",
        "ios_small": "下載於", "play_small": "下載於",
        "note": "免費 · iOS &amp; Android · 無強制廣告",
        "hero_alt": "貓咪真的很可愛遊戲畫面 — 墨線小村和對話框裡說話的貓咪",
        "stats": [["<em>★</em>4.9", "App Store 評分"], ["71,000+", "全球評價"], ["10M+", "累計下載"], ["2018", "上線至今"]],
        "how_kicker": "玩法", "how_num": "01–03",
        "how_h2": "餵貓、收集，<em>小村慢慢長大。</em>",
        "steps": [
            ["餵食", "餵小魚、存愛心", "建築會自動生產小魚。給貓咪餵食、收集愛心，提升小村等級。", "catfish"],
            ["抽貓", "認識新貓咪", "用抽獎券抽新貓咪——普通、稀有、史詩，每隻的長相和習慣都不一樣。", "gachaticket"],
            ["建設", "打造自己的小村", "升級建築、添置裝飾，貓咪們會把每個角落當成自己的地盤。", "building"],
        ],
        "col_kicker": "貓咪圖鑑", "col_num": "60+ 隻",
        "col_h2": "每隻貓都有名字，<br><em>也有自己的想法。</em>",
        "col_lede": "這些都是遊戲裡真實存在的貓咪——名字和稀有度原封不動。點一下蓋住的卡片，就像遊戲裡抽貓一樣。",
        "col_hint": "點卡片抽一隻",
        "shots_kicker": "截圖", "shots_num": "遊戲畫面",
        "shots_h2": "小村<em>真實的樣子。</em>",
        "shots_caps": ["聽貓咪說話", "給貓咪餵食", "陪貓咪玩耍"],
        "feat_kicker": "細節", "feat_num": "06",
        "feat_h2": "七年如一日，<em>安靜又溫柔。</em>",
        "feats": [
            ["真正的放置", "關掉 App 獎勵也在累積，每天幾分鐘就夠了。", "catgrass"],
            ["無強制廣告", "沒有任何打擾。想要獎勵時，自己選擇看廣告。", "heart"],
            ["60+種個性", "每隻貓都有名字、個性和在村裡最愛做的事。", "cat"],
            ["裝扮樂趣", "升級建築、擺放裝飾，把小村的每個角落變成你的風格。", "building"],
            ["13種語言", "日本、美國、韓國、越南、台灣……全球玩家都在玩。", "collection"],
            ["七年營運", "2018年至今由獨立小工作室用心維護——★4.9，71,000+則評價。", "toy"],
        ],
        "final_h2": "今天，貓咪們也在等你。",
        "final_lede": "iOS &amp; Android 免費。",
        "f_contact": "聯絡我們", "f_privacy": "隱私權政策", "f_terms": "服務條款",
    },
    "es": {
        "file": "es.html", "lang": "es", "font": None, "shots": "es",
        "name": "Cats are Cute",
        "title": "Cats are Cute — Un pueblo de gatos dibujado a tinta",
        "desc": "Un idle game tranquilo, querido desde 2018. Colecciona más de 60 gatos dibujados a mano y haz crecer un pueblito de líneas de tinta. ★4.9 · 71.000+ reseñas · gratis en iOS y Android.",
        "og_title": "Cats are Cute — Pueblo de Gato",
        "og_desc": "Un pueblo dibujado a tinta, donde solo los gatos tienen color. ★4.9 · 71.000+ reseñas.",
        "kicker_num": "PUEBLO DE GATOS IDLE · DESDE 2018",
        "h1": "Un pueblo dibujado a tinta.<br><em>Solo los gatos tienen color.</em>",
        "sub": "Colecciona más de 60 gatos — cada uno con nombre, personalidad y algo que decir. Aliméntalos, haz crecer tu pueblo y deja que las recompensas se acumulen mientras no estás. Anuncios solo si tú quieres.",
        "demo_kicker": "ESCUCHA A LOS GATOS",
        "ios_small": "Descárgalo en", "play_small": "DISPONIBLE EN",
        "note": "GRATIS · IOS &amp; ANDROID · SIN ANUNCIOS FORZADOS",
        "hero_alt": "Juego Cats are Cute — un pueblo dibujado a tinta con un gato hablando en un bocadillo",
        "stats": [["<em>★</em>4.9", "Nota en App Store"], ["71.000+", "Reseñas"], ["10M+", "Descargas"], ["2018", "En marcha desde"]],
        "how_kicker": "CÓMO SE JUEGA", "how_num": "01–03",
        "how_h2": "Alimenta, colecciona y <em>míralo crecer.</em>",
        "steps": [
            ["ALIMENTA", "Sirve pescado, gana corazones", "Los edificios producen pescado solos. Alimenta a los gatos y junta corazones para subir de nivel tu pueblo.", "catfish"],
            ["COLECCIONA", "Saca gatos nuevos", "Usa tickets para conocer gatos nuevos — normales, raros y épicos, cada uno con su cara y sus mañas.", "gachaticket"],
            ["CONSTRUYE", "Tu propio pueblo", "Mejora los edificios y llena el pueblo de rincones acogedores que los gatos harán suyos.", "building"],
        ],
        "col_kicker": "COLECCIÓN", "col_num": "60+ GATOS",
        "col_h2": "Cada gato tiene nombre.<br><em>Y opiniones.</em>",
        "col_lede": "Son gatos reales del juego — con sus nombres y rarezas. Toca una carta oculta para sacar uno, como en el gacha del juego.",
        "col_hint": "TOCA UNA CARTA",
        "shots_kicker": "PANTALLAS", "shots_num": "DEL JUEGO",
        "shots_h2": "El pueblo, <em>tal y como se ve.</em>",
        "shots_caps": ["ESCUCHA A LOS GATOS", "ALIMENTA A LOS GATOS", "JUEGA CON LOS GATOS"],
        "feat_kicker": "DETALLES", "feat_num": "06",
        "feat_h2": "Tranquilo a propósito. <em>Desde hace 7 años.</em>",
        "feats": [
            ["Idle de verdad", "El progreso sigue aunque cierres la app. Con unos minutos al día basta.", "catgrass"],
            ["Sin anuncios forzados", "Nada te interrumpe. Ves un anuncio solo cuando quieres el bonus.", "heart"],
            ["60+ personalidades", "Cada gato tiene nombre, carácter y sus pasatiempos favoritos en el pueblo.", "cat"],
            ["Un pueblo que decorar", "Mejora edificios y decora cada rincón a tu gusto.", "building"],
            ["13 idiomas", "Querido en Japón, EE. UU., Corea, Vietnam, Taiwán y más allá.", "collection"],
            ["7 años de cariño", "Un pequeño estudio indie lo cuida desde 2018 — ★4.9 con 71.000+ reseñas.", "toy"],
        ],
        "final_h2": "Los gatos también te esperan hoy.",
        "final_lede": "Gratis en iOS y Android.",
        "f_contact": "Contacto", "f_privacy": "Privacidad", "f_terms": "Términos",
    },
    "pt": {
        "file": "pt.html", "lang": "pt", "font": None, "shots": "pt",
        "name": "Cats are Cute",
        "title": "Cats are Cute — Uma vila de gatos desenhada a nanquim",
        "desc": "Um idle game tranquilo, querido desde 2018. Colecione mais de 60 gatos desenhados à mão e faça crescer uma vilinha de traços de nanquim. ★4.9 · 71.000+ avaliações · grátis no iOS e Android.",
        "og_title": "Cats are Cute — Cidade de Gatos",
        "og_desc": "Uma vila desenhada a nanquim, onde só os gatos têm cor. ★4.9 · 71.000+ avaliações.",
        "kicker_num": "VILA DE GATOS IDLE · DESDE 2018",
        "h1": "Uma vila desenhada a nanquim.<br><em>Só os gatos têm cor.</em>",
        "sub": "Colecione mais de 60 gatos — cada um com nome, personalidade e algo a dizer. Alimente-os, faça a vila crescer e deixe as recompensas acumularem enquanto você está fora. Anúncios só quando você quiser.",
        "demo_kicker": "OUÇA OS GATOS",
        "ios_small": "Baixar na", "play_small": "DISPONÍVEL NO",
        "note": "GRÁTIS · IOS &amp; ANDROID · SEM ANÚNCIOS FORÇADOS",
        "hero_alt": "Jogo Cats are Cute — uma vila desenhada a nanquim com um gato falando em um balão",
        "stats": [["<em>★</em>4.9", "Nota na App Store"], ["71.000+", "Avaliações"], ["10M+", "Downloads"], ["2018", "No ar desde"]],
        "how_kicker": "COMO JOGAR", "how_num": "01–03",
        "how_h2": "Alimente, colecione e <em>veja crescer.</em>",
        "steps": [
            ["ALIMENTE", "Sirva peixe, ganhe corações", "Os prédios produzem peixe sozinhos. Alimente os gatos e junte corações para subir o nível da vila.", "catfish"],
            ["COLECIONE", "Tire gatos novos", "Use tickets para conhecer gatos novos — normais, raros e épicos, cada um com sua cara e suas manias.", "gachaticket"],
            ["CONSTRUA", "Sua própria vila", "Melhore os prédios e encha a vila de cantinhos aconchegantes que os gatos vão adotar.", "building"],
        ],
        "col_kicker": "COLEÇÃO", "col_num": "60+ GATOS",
        "col_h2": "Cada gato tem nome.<br><em>E opiniões.</em>",
        "col_lede": "São gatos reais do jogo — com nomes e raridades de verdade. Toque numa carta escondida para tirar um, como no gacha do jogo.",
        "col_hint": "TOQUE NUMA CARTA",
        "shots_kicker": "TELAS", "shots_num": "DO JOGO",
        "shots_h2": "A vila, <em>do jeito que ela é.</em>",
        "shots_caps": ["OUÇA OS GATOS", "ALIMENTE OS GATOS", "BRINQUE COM OS GATOS"],
        "feat_kicker": "DETALHES", "feat_num": "06",
        "feat_h2": "Calmo de propósito. <em>Há 7 anos.</em>",
        "feats": [
            ["Idle de verdade", "O progresso continua com o app fechado. Alguns minutos por dia bastam.", "catgrass"],
            ["Sem anúncios forçados", "Nada interrompe você. Veja um anúncio só quando quiser o bônus.", "heart"],
            ["60+ personalidades", "Cada gato tem nome, jeito próprio e passatempos favoritos na vila.", "cat"],
            ["Uma vila para decorar", "Melhore prédios e decore cada cantinho do seu jeito.", "building"],
            ["13 idiomas", "Querido no Japão, nos EUA, na Coreia, no Vietnã, em Taiwan e além.", "collection"],
            ["7 anos de carinho", "Um pequeno estúdio indie cuida dele desde 2018 — ★4.9 com 71.000+ avaliações.", "toy"],
        ],
        "final_h2": "Os gatos estão esperando por você hoje também.",
        "final_lede": "Grátis no iOS e Android.",
        "f_contact": "Contato", "f_privacy": "Privacidade", "f_terms": "Termos",
    },
    "de": {
        "file": "de.html", "lang": "de", "font": None, "shots": "de",
        "name": "Cats are Cute",
        "title": "Cats are Cute — Ein mit Tinte gezeichnetes Katzendorf",
        "desc": "Ein ruhiges Idle-Game, geliebt seit 2018. Sammle über 60 handgezeichnete Katzen und lass ein gemütliches Tintendorf wachsen. ★4,9 · 71.000+ Bewertungen · gratis für iOS & Android.",
        "og_title": "Cats are Cute — Idle Katzendorf",
        "og_desc": "Ein Dorf, mit Tinte gezeichnet — nur die Katzen haben Farbe. ★4,9 · 71.000+ Bewertungen.",
        "kicker_num": "IDLE-KATZENDORF · SEIT 2018",
        "h1": "Ein Dorf, mit Tinte gezeichnet.<br><em>Nur die Katzen haben Farbe.</em>",
        "sub": "Sammle über 60 Katzen — jede mit Namen, Persönlichkeit und einer eigenen Meinung. Füttere sie, lass dein Dorf wachsen, und die Belohnungen stapeln sich auch ohne dich. Werbung nur, wenn du willst.",
        "demo_kicker": "HÖR DEN KATZEN ZU",
        "ios_small": "Laden im", "play_small": "JETZT BEI",
        "note": "GRATIS · IOS &amp; ANDROID · KEINE ZWANGSWERBUNG",
        "hero_alt": "Cats are Cute Spielszene — ein mit Tinte gezeichnetes Dorf, eine Katze spricht in einer Sprechblase",
        "stats": [["<em>★</em>4,9", "App-Store-Wertung"], ["71.000+", "Bewertungen"], ["10M+", "Downloads"], ["2018", "Online seit"]],
        "how_kicker": "SO FUNKTIONIERT'S", "how_num": "01–03",
        "how_h2": "Füttern, sammeln, <em>wachsen sehen.</em>",
        "steps": [
            ["FÜTTERN", "Fisch servieren, Herzen sammeln", "Die Gebäude produzieren von selbst Fisch. Füttere die Katzen und sammle Herzen, um dein Dorf aufzuleveln.", "catfish"],
            ["SAMMELN", "Neue Katzen ziehen", "Mit Tickets ziehst du neue Katzen — Normal, Selten und Episch, jede mit eigenem Gesicht und eigenen Macken.", "gachaticket"],
            ["BAUEN", "Dein eigenes Dorf", "Verbessere Gebäude und fülle das Tintendorf mit gemütlichen Plätzen, die sich die Katzen schnappen.", "building"],
        ],
        "col_kicker": "KATZENSAMMLUNG", "col_num": "60+ KATZEN",
        "col_h2": "Jede Katze hat einen Namen.<br><em>Und eine Meinung.</em>",
        "col_lede": "Das sind echte Katzen aus dem Spiel — mit Namen und Seltenheit. Tippe auf eine verdeckte Karte und zieh eine, wie beim Gacha im Spiel.",
        "col_hint": "KARTE ANTIPPEN",
        "shots_kicker": "SCREENS", "shots_num": "IM SPIEL",
        "shots_h2": "Das Dorf, <em>wie es wirklich aussieht.</em>",
        "shots_caps": ["HÖR DEN KATZEN ZU", "FÜTTERE DIE KATZEN", "SPIEL MIT DEN KATZEN"],
        "feat_kicker": "DETAILS", "feat_num": "06",
        "feat_h2": "Bewusst ruhig. <em>Seit sieben Jahren.</em>",
        "feats": [
            ["Echtes Idle", "Der Fortschritt läuft weiter, auch wenn die App zu ist. Ein paar Minuten am Tag reichen.", "catgrass"],
            ["Keine Zwangswerbung", "Nichts unterbricht dich. Werbung nur, wenn du den Bonus willst.", "heart"],
            ["60+ Persönlichkeiten", "Jede Katze hat einen Namen, einen Charakter und Lieblingsbeschäftigungen im Dorf.", "cat"],
            ["Ein Dorf zum Gestalten", "Gebäude ausbauen, Deko platzieren — jede Ecke nach deinem Geschmack.", "building"],
            ["13 Sprachen", "Geliebt in Japan, den USA, Korea, Vietnam, Taiwan und darüber hinaus.", "collection"],
            ["7 Jahre Pflege", "Seit 2018 von einem kleinen Indie-Studio betreut — ★4,9 bei 71.000+ Bewertungen.", "toy"],
        ],
        "final_h2": "Die Katzen warten auch heute auf dich.",
        "final_lede": "Gratis für iOS &amp; Android.",
        "f_contact": "Kontakt", "f_privacy": "Datenschutz", "f_terms": "Nutzungsbedingungen",
    },
    "fr": {
        "file": "fr.html", "lang": "fr", "font": None, "shots": "fr",
        "name": "Cats are Cute",
        "title": "Cats are Cute — Un village de chats dessiné à l'encre",
        "desc": "Un idle game paisible, aimé depuis 2018. Collectionnez plus de 60 chats dessinés à la main et faites grandir un petit village à l'encre. ★4,9 · 71 000+ avis · gratuit sur iOS et Android.",
        "og_title": "Cats are Cute — Ville des Chats",
        "og_desc": "Un village dessiné à l'encre, où seuls les chats sont en couleur. ★4,9 · 71 000+ avis.",
        "kicker_num": "VILLAGE DE CHATS IDLE · DEPUIS 2018",
        "h1": "Un village dessiné à l'encre.<br><em>Seuls les chats sont en couleur.</em>",
        "sub": "Collectionnez plus de 60 chats — chacun avec un nom, un caractère et son mot à dire. Nourrissez-les, agrandissez votre village, et les récompenses s'accumulent même en votre absence. La pub, seulement si vous le choisissez.",
        "demo_kicker": "ÉCOUTEZ LES CHATS",
        "ios_small": "Télécharger sur", "play_small": "DISPONIBLE SUR",
        "note": "GRATUIT · IOS &amp; ANDROID · SANS PUB FORCÉE",
        "hero_alt": "Jeu Cats are Cute — un village dessiné à l'encre avec un chat qui parle dans une bulle",
        "stats": [["<em>★</em>4,9", "Note App Store"], ["71 000+", "Avis"], ["10M+", "Téléchargements"], ["2018", "En ligne depuis"]],
        "how_kicker": "COMMENT ÇA MARCHE", "how_num": "01–03",
        "how_h2": "Nourrir, collectionner, <em>regarder grandir.</em>",
        "steps": [
            ["NOURRIR", "Servez du poisson, gagnez des cœurs", "Les bâtiments produisent du poisson tout seuls. Nourrissez les chats et récoltez des cœurs pour faire monter votre village de niveau.", "catfish"],
            ["COLLECTIONNER", "Tirez de nouveaux chats", "Utilisez des tickets pour rencontrer de nouveaux chats — normaux, rares et épiques, chacun avec sa frimousse et ses manies.", "gachaticket"],
            ["CONSTRUIRE", "Votre propre village", "Améliorez les bâtiments et remplissez le village de coins douillets que les chats s'approprieront.", "building"],
        ],
        "col_kicker": "COLLECTION", "col_num": "60+ CHATS",
        "col_h2": "Chaque chat a un nom.<br><em>Et des opinions.</em>",
        "col_lede": "Ce sont de vrais chats du jeu — noms et raretés compris. Touchez une carte cachée pour en tirer un, comme au gacha du jeu.",
        "col_hint": "TOUCHEZ UNE CARTE",
        "shots_kicker": "ÉCRANS", "shots_num": "EN JEU",
        "shots_h2": "Le village, <em>tel qu'il est vraiment.</em>",
        "shots_caps": ["ÉCOUTEZ LES CHATS", "NOURRISSEZ LES CHATS", "JOUEZ AVEC LES CHATS"],
        "feat_kicker": "DÉTAILS", "feat_num": "06",
        "feat_h2": "Paisible par choix. <em>Depuis sept ans.</em>",
        "feats": [
            ["Vraiment idle", "La progression continue app fermée. Quelques minutes par jour suffisent.", "catgrass"],
            ["Sans pub forcée", "Rien ne vous interrompt. Une pub seulement quand vous voulez le bonus.", "heart"],
            ["60+ caractères", "Chaque chat a un nom, un caractère et ses passe-temps favoris au village.", "cat"],
            ["Un village à décorer", "Améliorez les bâtiments et décorez chaque recoin à votre goût.", "building"],
            ["13 langues", "Aimé au Japon, aux États-Unis, en Corée, au Vietnam, à Taïwan et au-delà.", "collection"],
            ["7 ans d'attention", "Entretenu par un petit studio indé depuis 2018 — ★4,9 pour 71 000+ avis.", "toy"],
        ],
        "final_h2": "Les chats vous attendent aujourd'hui aussi.",
        "final_lede": "Gratuit sur iOS et Android.",
        "f_contact": "Contact", "f_privacy": "Confidentialité", "f_terms": "Conditions",
    },
    "ru": {
        "file": "ru.html", "lang": "ru", "font": None, "shots": "ru",
        "name": "Cats are Cute",
        "title": "Cats are Cute — Кошачья деревня, нарисованная тушью",
        "desc": "Спокойная idle-игра, любимая с 2018 года. Соберите 60+ нарисованных от руки котов и вырастите уютную деревню из чернильных линий. ★4,9 · 71 000+ отзывов · бесплатно на iOS и Android.",
        "og_title": "Cats are Cute — Idle котов",
        "og_desc": "Деревня, нарисованная тушью, — цветные здесь только коты. ★4,9 · 71 000+ отзывов.",
        "kicker_num": "IDLE ГОРОД КОТОВ · С 2018",
        "h1": "Деревня, нарисованная тушью.<br><em>Цветные здесь только коты.</em>",
        "sub": "Соберите 60+ котов — у каждого есть имя, характер и что сказать. Кормите их, развивайте деревню, а награды копятся даже без вас. Реклама — только по вашему желанию.",
        "demo_kicker": "ПОСЛУШАЙТЕ КОТОВ",
        "ios_small": "Загрузите в", "play_small": "ДОСТУПНО В",
        "note": "БЕСПЛАТНО · IOS &amp; ANDROID · БЕЗ ПРИНУДИТЕЛЬНОЙ РЕКЛАМЫ",
        "hero_alt": "Игра Cats are Cute — нарисованная тушью деревня и кот, говорящий в облачке",
        "stats": [["<em>★</em>4,9", "Рейтинг App Store"], ["71 000+", "Отзывов"], ["10M+", "Загрузок"], ["2018", "Работает с"]],
        "how_kicker": "КАК ИГРАТЬ", "how_num": "01–03",
        "how_h2": "Кормите, собирайте — <em>и деревня растёт.</em>",
        "steps": [
            ["КОРМИТЕ", "Рыба котам, сердечки вам", "Здания сами производят рыбу. Кормите котов и собирайте сердечки, чтобы повышать уровень деревни.", "catfish"],
            ["СОБИРАЙТЕ", "Новые коты из гачи", "Тяните билетики и знакомьтесь с новыми котами — обычными, редкими и эпическими, у каждого своя мордочка и свои привычки.", "gachaticket"],
            ["СТРОЙТЕ", "Своя деревня", "Улучшайте здания и наполняйте чернильный городок уютными местечками — коты их быстро займут.", "building"],
        ],
        "col_kicker": "КОЛЛЕКЦИЯ", "col_num": "60+ КОТОВ",
        "col_h2": "У каждого кота есть имя.<br><em>И своё мнение.</em>",
        "col_lede": "Это настоящие коты из игры — с именами и редкостью. Нажмите на закрытую карту, чтобы вытянуть кота, как в игровой гаче.",
        "col_hint": "НАЖМИТЕ НА КАРТУ",
        "shots_kicker": "ЭКРАНЫ", "shots_num": "ИЗ ИГРЫ",
        "shots_h2": "Деревня — <em>какая она на самом деле.</em>",
        "shots_caps": ["ПОСЛУШАЙТЕ КОТОВ", "ПОКОРМИТЕ КОТОВ", "ПОИГРАЙТЕ С КОТАМИ"],
        "feat_kicker": "ДЕТАЛИ", "feat_num": "06",
        "feat_h2": "Спокойная по задумке. <em>Уже семь лет.</em>",
        "feats": [
            ["Настоящий idle", "Прогресс идёт, даже когда приложение закрыто. Пары минут в день достаточно.", "catgrass"],
            ["Без принудительной рекламы", "Ничто не прерывает игру. Реклама — только когда вам нужен бонус.", "heart"],
            ["60+ характеров", "У каждого кота есть имя, характер и любимые занятия в деревне.", "cat"],
            ["Деревня для декора", "Улучшайте здания и украшайте каждый уголок по своему вкусу.", "building"],
            ["13 языков", "Игру любят в Японии, США, Корее, Вьетнаме, на Тайване и не только.", "collection"],
            ["7 лет заботы", "Маленькая инди-студия ведёт игру с 2018 года — ★4,9 и 71 000+ отзывов.", "toy"],
        ],
        "final_h2": "Коты ждут вас и сегодня.",
        "final_lede": "Бесплатно на iOS и Android.",
        "f_contact": "Связаться", "f_privacy": "Конфиденциальность", "f_terms": "Условия",
    },
    "th": {
        "file": "th.html", "lang": "th", "font": '"Thonburi"', "shots": "th",
        "name": "Cats are Cute",
        "title": "Cats are Cute — หมู่บ้านแมวที่วาดด้วยหมึก",
        "desc": "เกม idle สุดชิลที่มีคนรักมาตั้งแต่ปี 2018 สะสมแมววาดมือกว่า 60 ตัว แล้วปลูกหมู่บ้านลายเส้นหมึกแสนอบอุ่น ★4.9 · รีวิว 71,000+ · เล่นฟรีบน iOS และ Android",
        "og_title": "Cats are Cute — หมู่บ้านแมว idle",
        "og_desc": "หมู่บ้านที่วาดด้วยหมึก มีแค่แมวเท่านั้นที่มีสี ★4.9 · รีวิว 71,000+",
        "kicker_num": "เกมหมู่บ้านแมว IDLE · ตั้งแต่ 2018",
        "h1": "หมู่บ้านที่วาดด้วยหมึก<br><em>มีแค่แมวเท่านั้นที่มีสี</em>",
        "sub": "สะสมแมวกว่า 60 ตัว แต่ละตัวมีชื่อ มีนิสัย แถมมีเรื่องอยากพูด ให้อาหาร ปลูกหมู่บ้าน แล้วรางวัลจะสะสมเองแม้ตอนคุณไม่อยู่ โฆษณาดูเฉพาะตอนที่คุณเลือกเอง",
        "demo_kicker": "ฟังเสียงแมวสิ",
        "ios_small": "ดาวน์โหลดบน", "play_small": "ดาวน์โหลดบน",
        "note": "ฟรี · IOS &amp; ANDROID · ไม่มีโฆษณาบังคับ",
        "hero_alt": "ภาพเกม Cats are Cute — หมู่บ้านลายเส้นหมึกกับแมวที่กำลังพูดในกล่องข้อความ",
        "stats": [["<em>★</em>4.9", "คะแนน App Store"], ["71,000+", "รีวิวทั่วโลก"], ["10M+", "ยอดดาวน์โหลด"], ["2018", "เปิดบริการตั้งแต่"]],
        "how_kicker": "วิธีเล่น", "how_num": "01–03",
        "how_h2": "ให้อาหาร สะสม <em>แล้วดูหมู่บ้านโต</em>",
        "steps": [
            ["ให้อาหาร", "เสิร์ฟปลา รับหัวใจ", "อาคารผลิตปลาให้เองอัตโนมัติ ให้อาหารแมวแล้วเก็บหัวใจเพื่ออัปเลเวลหมู่บ้าน", "catfish"],
            ["สุ่มแมว", "พบแมวตัวใหม่", "ใช้ตั๋วสุ่มเพื่อพบแมวใหม่ ๆ — ทั้งธรรมดา แรร์ และอีพิค หน้าตาและนิสัยไม่ซ้ำกันเลย", "gachaticket"],
            ["สร้างหมู่บ้าน", "หมู่บ้านในแบบของคุณ", "อัปเกรดอาคารและแต่งหมู่บ้านลายหมึกให้เต็มไปด้วยมุมอุ่น ๆ ที่แมวจะมาจับจอง", "building"],
        ],
        "col_kicker": "สมุดสะสมแมว", "col_num": "60+ ตัว",
        "col_h2": "แมวทุกตัวมีชื่อ<br><em>และมีความเห็นด้วยนะ</em>",
        "col_lede": "นี่คือแมวตัวจริงจากในเกม — ชื่อและความแรร์ตรงตามเกมเป๊ะ แตะการ์ดที่คว่ำอยู่เพื่อสุ่มแมว เหมือนกาชาในเกมเลย",
        "col_hint": "แตะการ์ดเพื่อสุ่ม",
        "shots_kicker": "ภาพหน้าจอ", "shots_num": "ในเกม",
        "shots_h2": "หมู่บ้าน<em>หน้าตาแบบนี้เลย</em>",
        "shots_caps": ["ฟังเสียงแมว", "ให้อาหารแมว", "เล่นกับแมว"],
        "feat_kicker": "รายละเอียด", "feat_num": "06",
        "feat_h2": "เงียบสงบโดยตั้งใจ <em>มาเจ็ดปีแล้ว</em>",
        "feats": [
            ["Idle ของแท้", "ปิดแอปไปรางวัลก็ยังสะสมต่อ วันละไม่กี่นาทีก็พอ", "catgrass"],
            ["ไม่มีโฆษณาบังคับ", "ไม่มีอะไรมาขัดจังหวะ ดูโฆษณาเฉพาะตอนอยากได้โบนัส", "heart"],
            ["60+ นิสัยไม่ซ้ำ", "แมวแต่ละตัวมีชื่อ นิสัย และงานอดิเรกประจำหมู่บ้านของตัวเอง", "cat"],
            ["แต่งหมู่บ้านสนุก", "อัปเกรดอาคาร วางของตกแต่ง จัดทุกมุมตามใจคุณ", "building"],
            ["13 ภาษา", "มีคนเล่นทั้งญี่ปุ่น อเมริกา เกาหลี เวียดนาม ไต้หวัน และอีกมากมาย", "collection"],
            ["ดูแลมา 7 ปี", "สตูดิโออินดี้เล็ก ๆ ดูแลมาตั้งแต่ 2018 — ★4.9 จากรีวิว 71,000+", "toy"],
        ],
        "final_h2": "วันนี้เหล่าแมวก็รอคุณอยู่นะ",
        "final_lede": "เล่นฟรีบน iOS และ Android",
        "f_contact": "ติดต่อเรา", "f_privacy": "นโยบายความเป็นส่วนตัว", "f_terms": "ข้อกำหนด",
    },
    "id": {
        "file": "id.html", "lang": "id", "font": None, "shots": "id",
        "name": "Cats are Cute",
        "title": "Cats are Cute — Desa kucing yang digambar dengan tinta",
        "desc": "Game idle santai yang dicintai sejak 2018. Kumpulkan 60+ kucing gambar tangan dan besarkan desa mungil bergaris tinta. ★4,9 · 71.000+ ulasan · gratis di iOS & Android.",
        "og_title": "Cats are Cute — Kucing Lucu",
        "og_desc": "Desa yang digambar dengan tinta — hanya kucingnya yang berwarna. ★4,9 · 71.000+ ulasan.",
        "kicker_num": "DESA KUCING IDLE · SEJAK 2018",
        "h1": "Desa yang digambar dengan tinta.<br><em>Hanya kucingnya yang berwarna.</em>",
        "sub": "Kumpulkan 60+ kucing — masing-masing punya nama, kepribadian, dan sesuatu untuk dikatakan. Beri makan, besarkan desamu, dan hadiah terus menumpuk saat kamu pergi. Iklan hanya kalau kamu mau.",
        "demo_kicker": "DENGARKAN PARA KUCING",
        "ios_small": "Unduh di", "play_small": "TERSEDIA DI",
        "note": "GRATIS · IOS &amp; ANDROID · TANPA IKLAN PAKSA",
        "hero_alt": "Gameplay Cats are Cute — desa bergaris tinta dengan kucing yang berbicara di kotak kata",
        "stats": [["<em>★</em>4,9", "Rating App Store"], ["71.000+", "Ulasan"], ["10M+", "Unduhan"], ["2018", "Beroperasi sejak"]],
        "how_kicker": "CARA MAIN", "how_num": "01–03",
        "how_h2": "Beri makan, kumpulkan, <em>lihat desamu tumbuh.</em>",
        "steps": [
            ["BERI MAKAN", "Sajikan ikan, dapatkan hati", "Bangunan memproduksi ikan sendiri. Beri makan kucing dan kumpulkan hati untuk menaikkan level desa.", "catfish"],
            ["KUMPULKAN", "Gacha kucing baru", "Pakai tiket untuk bertemu kucing baru — Normal, Langka, dan Epik, masing-masing dengan wajah dan kebiasaannya sendiri.", "gachaticket"],
            ["BANGUN", "Desa milikmu sendiri", "Tingkatkan bangunan dan isi desa tinta dengan sudut-sudut nyaman yang akan diklaim para kucing.", "building"],
        ],
        "col_kicker": "KOLEKSI KUCING", "col_num": "60+ KUCING",
        "col_h2": "Setiap kucing punya nama.<br><em>Dan pendapat.</em>",
        "col_lede": "Ini kucing-kucing asli dari dalam game — nama dan kelangkaannya persis. Ketuk kartu tertutup untuk menggacha, seperti di dalam game.",
        "col_hint": "KETUK KARTUNYA",
        "shots_kicker": "LAYAR", "shots_num": "DALAM GAME",
        "shots_h2": "Desanya, <em>persis seperti aslinya.</em>",
        "shots_caps": ["DENGARKAN KUCING", "BERI MAKAN KUCING", "MAIN DENGAN KUCING"],
        "feat_kicker": "DETAIL", "feat_num": "06",
        "feat_h2": "Tenang memang disengaja. <em>Sudah tujuh tahun.</em>",
        "feats": [
            ["Idle sungguhan", "Progres terus berjalan walau aplikasi ditutup. Beberapa menit sehari sudah cukup.", "catgrass"],
            ["Tanpa iklan paksa", "Tidak ada yang menyela. Tonton iklan hanya saat kamu mau bonusnya.", "heart"],
            ["60+ kepribadian", "Setiap kucing punya nama, sifat, dan kegiatan favorit di desa.", "cat"],
            ["Desa untuk didekorasi", "Tingkatkan bangunan dan hias tiap sudut sesuai seleramu.", "building"],
            ["13 bahasa", "Dicintai di Jepang, AS, Korea, Vietnam, Taiwan, dan banyak lagi.", "collection"],
            ["7 tahun dirawat", "Dikelola studio indie kecil sejak 2018 — ★4,9 dari 71.000+ ulasan.", "toy"],
        ],
        "final_h2": "Hari ini pun para kucing menunggumu.",
        "final_lede": "Gratis di iOS & Android.",
        "f_contact": "Kontak", "f_privacy": "Privasi", "f_terms": "Ketentuan",
    },
    "vi": {
        "file": "vi.html", "lang": "vi", "font": None, "shots": "vi",
        "name": "Cats are Cute",
        "title": "Cats are Cute — Ngôi làng mèo vẽ bằng mực",
        "desc": "Game idle nhẹ nhàng được yêu thích từ 2018. Sưu tầm hơn 60 chú mèo vẽ tay và nuôi lớn một ngôi làng nét mực ấm áp. ★4,9 · 71.000+ đánh giá · miễn phí trên iOS & Android.",
        "og_title": "Cats are Cute — Mèo Dễ Cưng",
        "og_desc": "Ngôi làng vẽ bằng mực — chỉ những chú mèo là có màu. ★4,9 · 71.000+ đánh giá.",
        "kicker_num": "LÀNG MÈO IDLE · TỪ 2018",
        "h1": "Ngôi làng vẽ bằng mực.<br><em>Chỉ những chú mèo là có màu.</em>",
        "sub": "Sưu tầm hơn 60 chú mèo — mỗi bé có tên riêng, tính cách riêng và cả những điều muốn nói. Cho mèo ăn, xây làng, phần thưởng vẫn tự tích lũy khi bạn vắng mặt. Quảng cáo chỉ xuất hiện khi bạn muốn xem.",
        "demo_kicker": "LẮNG NGHE LŨ MÈO",
        "ios_small": "Tải về trên", "play_small": "TẢI VỀ TRÊN",
        "note": "MIỄN PHÍ · IOS &amp; ANDROID · KHÔNG QUẢNG CÁO ÉP BUỘC",
        "hero_alt": "Cảnh chơi Cats are Cute — ngôi làng nét mực với chú mèo đang nói trong khung thoại",
        "stats": [["<em>★</em>4,9", "Điểm App Store"], ["71.000+", "Đánh giá"], ["10M+", "Lượt tải"], ["2018", "Vận hành từ"]],
        "how_kicker": "CÁCH CHƠI", "how_num": "01–03",
        "how_h2": "Cho ăn, sưu tầm, <em>nhìn làng lớn lên.</em>",
        "steps": [
            ["CHO ĂN", "Dọn cá, nhận tim", "Các tòa nhà tự sản xuất cá. Cho mèo ăn và gom tim để nâng cấp ngôi làng.", "catfish"],
            ["SƯU TẦM", "Quay mèo mới", "Dùng vé quay để gặp mèo mới — Thường, Hiếm và Sử thi, mỗi bé một gương mặt, một thói quen.", "gachaticket"],
            ["XÂY DỰNG", "Ngôi làng của riêng bạn", "Nâng cấp nhà cửa, trang trí khắp nơi — lũ mèo sẽ tự tìm chỗ yêu thích của mình.", "building"],
        ],
        "col_kicker": "BỘ SƯU TẬP", "col_num": "60+ CHÚ MÈO",
        "col_h2": "Mèo nào cũng có tên.<br><em>Và cả chính kiến.</em>",
        "col_lede": "Đây là những chú mèo thật trong game — đúng tên, đúng độ hiếm. Chạm vào thẻ úp để quay một bé, y như gacha trong game.",
        "col_hint": "CHẠM THẺ ĐỂ QUAY",
        "shots_kicker": "MÀN HÌNH", "shots_num": "TRONG GAME",
        "shots_h2": "Ngôi làng, <em>đúng như nó vốn thế.</em>",
        "shots_caps": ["NGHE MÈO NÓI", "CHO MÈO ĂN", "CHƠI VỚI MÈO"],
        "feat_kicker": "CHI TIẾT", "feat_num": "06",
        "feat_h2": "Bình yên có chủ đích. <em>Suốt bảy năm.</em>",
        "feats": [
            ["Idle đích thực", "Tiến trình vẫn chạy khi tắt app. Mỗi ngày vài phút là đủ.", "catgrass"],
            ["Không quảng cáo ép buộc", "Không gì làm phiền bạn. Chỉ xem quảng cáo khi bạn muốn nhận thưởng.", "heart"],
            ["60+ tính cách", "Mỗi chú mèo có tên, cá tính và thú vui riêng trong làng.", "cat"],
            ["Ngôi làng để trang trí", "Nâng cấp nhà cửa, bày biện từng góc nhỏ theo ý bạn.", "building"],
            ["13 ngôn ngữ", "Được yêu thích ở Nhật, Mỹ, Hàn, Việt Nam, Đài Loan và hơn thế nữa.", "collection"],
            ["7 năm chăm chút", "Một studio indie nhỏ vận hành từ 2018 — ★4,9 với 71.000+ đánh giá.", "toy"],
        ],
        "final_h2": "Hôm nay lũ mèo vẫn đang đợi bạn.",
        "final_lede": "Miễn phí trên iOS & Android.",
        "f_contact": "Liên hệ", "f_privacy": "Quyền riêng tư", "f_terms": "Điều khoản",
    },
}


def hreflang_block():
    lines = []
    for code, fname in HREFLANGS:
        lines.append(f'<link rel="alternate" hreflang="{code}" href="{BASE_URL}{fname}">')
    lines.append(f'<link rel="alternate" hreflang="x-default" href="{BASE_URL}index.html">')
    return "\n".join(lines)


def lang_select(cur_file):
    opts = "".join(
        f'<option value="{f}"{" selected" if f == cur_file else ""}>{label}</option>'
        for f, label in LANG_OPTIONS
    )
    return f'<select class="lang-select" onchange="location.href=this.value" aria-label="Language">{opts}</select>'


def badge(loc, store, el_cls):
    if store == "ios":
        return (f'<a class="store-badge {el_cls}" href="{APPSTORE_URL}">{APPLE_SVG}'
                f'<span class="txt"><small>{loc["ios_small"]}</small><strong>App Store</strong></span></a>')
    return (f'<a class="store-badge {el_cls}" href="{PLAY_URL}">{PLAY_SVG}'
            f'<span class="txt"><small>{loc["play_small"]}</small><strong>Google Play</strong></span></a>')


def render(key):
    loc = LOCALES[key]
    g = GAME[key]
    by_sprite = {c["sprite"]: c for c in g["cats"]}

    demo = [{"s": s, "n": by_sprite[s]["name"], "t": g["lines"][i]}
            for i, s in enumerate(DEMO_SPRITES)]
    pool = [{"s": c["sprite"], "n": c["name"], "r": c["rarity"], "t": c["tier"]}
            for c in g["cats"] if c["sprite"] not in GRID_SPRITES]

    chips = "".join(
        f'<div class="chip wordbox c{i+1}"><img src="assets/cats/{s}.png" alt="">'
        f'{by_sprite[s]["name"]}<span class="h">♥</span></div>'
        for i, s in enumerate(CHIP_SPRITES)
    )
    marquee = "".join(
        f'<img src="assets/cats/{s}.png" alt="" loading="lazy">'
        for s in MARQUEE_SPRITES * 2
    )
    skyline = "".join(
        f'<img class="peek" src="assets/cats/{item.split(":")[1]}.png" style="height:{h}px" alt="">'
        if item.startswith("__cat:")
        else f'<img src="assets/props/{item}.png" style="height:{h}px" alt="" loading="lazy">'
        for item, h in SKYLINE
    )
    stats = "".join(
        f'<div class="stat"><div class="v">{v}</div><div class="k">{k}</div></div>'
        for v, k in loc["stats"]
    )
    steps = "".join(
        f'<div class="step wordbox"><span class="n">0{i+1}</span>'
        f'<div class="ic"><img src="assets/ui/{ic}.png" alt=""></div>'
        f'<span class="kicker" style="margin-bottom:6px"><span>{tag}</span></span>'
        f'<h3>{h}</h3><p>{p}</p></div>'
        for i, (tag, h, p, ic) in enumerate(loc["steps"])
    )
    tiles = "".join(
        f'<div class="tile wordbox {by_sprite[s]["tier"]}">'
        f'<img src="assets/cats/{s}.png" alt="{by_sprite[s]["name"]}" loading="lazy">'
        f'<div class="nm">{by_sprite[s]["name"]}</div>'
        f'<span class="rr">{by_sprite[s]["rarity"]}</span></div>'
        for s in GRID_SPRITES
    ) + "".join(
        '<div class="tile wordbox unknown" role="button" tabindex="0">'
        '<img src="assets/cats/unknown.png" alt="?" loading="lazy">'
        '<div class="nm">?</div><span class="rr">···</span></div>'
        for _ in range(UNKNOWN_SLOTS)
    )
    shots = "".join(
        f'<figure><div class="phone"><img src="../shots/cats-cute/{loc["shots"]}-{i}.jpg" alt="{cap}" loading="lazy">'
        f'<div class="island"></div></div><figcaption>{cap}</figcaption></figure>'
        for i, cap in zip((1, 2, 3), loc["shots_caps"])
    )
    feats = "".join(
        f'<div class="feat wordbox"><div class="ic"><img src="assets/ui/{ic}.png" alt=""></div>'
        f'<h3>{h}</h3><p>{p}</p></div>'
        for h, p, ic in loc["feats"]
    )
    font_override = (f'<style>body{{font-family:{loc["font"]},ui-rounded,-apple-system,'
                     f'BlinkMacSystemFont,"Segoe UI",sans-serif}}</style>') if loc["font"] else ""
    canonical = BASE_URL if key == "en" else f'{BASE_URL}{loc["file"]}'
    demo_json = json.dumps(demo, ensure_ascii=False)
    pool_json = json.dumps(pool, ensure_ascii=False)

    html = f"""<!doctype html>
<html lang="{loc['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{loc['title']}</title>
<meta name="description" content="{loc['desc']}">
<meta property="og:title" content="{loc['og_title']}">
<meta property="og:description" content="{loc['og_desc']}">
<meta property="og:image" content="{OG_IMAGE}">
<meta property="og:type" content="website">
<link rel="canonical" href="{canonical}">
{hreflang_block()}
<link rel="icon" type="image/png" href="../icons/cats-cute.png">
<link rel="apple-touch-icon" href="../icons/cats-cute.png">
<link rel="stylesheet" href="style.css">
{font_override}
</head>
<body>

<nav>
  <div class="wrap">
    <a class="wordmark" href="{'index.html' if key != 'en' else './'}"><img src="../icons/cats-cute.png" alt="">{loc['name']}</a>
    {lang_select(loc['file'])}
  </div>
</nav>

<header class="hero">
  <div class="ghost" aria-hidden="true">CAT</div>
  <div class="wrap">
    <div>
      <div class="kicker"><span>CATS ARE CUTE</span><span class="rule"></span><span class="num">{loc['kicker_num']}</span></div>
      <h1>{loc['h1']}</h1>
      <div class="demo-kicker">{loc['demo_kicker']}</div>
      <div class="demo wordbox">
        <div class="who"><img id="demoFace" src="assets/cats/{demo[0]['s']}.png" alt=""><span class="nm" id="demoName">{demo[0]['n']}</span></div>
        <div class="line" id="demoLine">{demo[0]['t']}</div>
      </div>
      <p class="sub">{loc['sub']}</p>
      <div class="cta">
        {badge(loc, 'ios', 'b-ios')}
        {badge(loc, 'play', 'b-play')}
        <span class="note">{loc['note']}</span>
      </div>
    </div>
    <div class="phone-col">
      {chips}
      <div class="phone"><img src="../shots/cats-cute/{loc['shots']}-1.jpg" alt="{loc['hero_alt']}"><div class="island"></div></div>
    </div>
  </div>
</header>

<div class="skyline" aria-hidden="true"><div class="row">{skyline}</div></div>

<div class="marquee" aria-hidden="true"><div class="track">{marquee}</div></div>

<div class="stats">
  <div class="wrap">{stats}</div>
</div>

<section>
  <div class="wrap">
    <div class="kicker"><span>{loc['how_kicker']}</span><span class="rule"></span><span class="num">{loc['how_num']}</span></div>
    <h2>{loc['how_h2']}</h2>
    <div class="steps">{steps}</div>
  </div>
</section>

<section class="collection">
  <div class="wrap">
    <div class="kicker"><span>{loc['col_kicker']}</span><span class="rule"></span><span class="num">{loc['col_num']}</span></div>
    <h2>{loc['col_h2']}</h2>
    <p class="lede">{loc['col_lede']}</p>
    <div class="tiles" id="tiles">{tiles}</div>
    <span class="col-hint">{loc['col_hint']}</span>
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
  <div class="band">
    <div class="wrap">
      <h2>{loc['final_h2']}</h2>
      <p class="lede">{loc['final_lede']}</p>
      <div class="cta">
        {badge(loc, 'ios', 'b-ios2')}
        {badge(loc, 'play', 'b-play2')}
      </div>
    </div>
  </div>
</section>

<footer>
  <div class="wrap">
    <div class="brand"><img src="../icons/cats-cute.png" alt=""><strong>kkiruk studio</strong></div>
    <div class="links">
      <a href="mailto:kkirukstudio.help@gmail.com">{loc['f_contact']}</a>
      <a href="https://kkiruk-studio.github.io/privacy-policy-app/">{loc['f_privacy']}</a>
      <a href="https://kkiruk-studio.github.io/terms-of-service-app/">{loc['f_terms']}</a>
    </div>
    <div>© 2026 kkiruk studio</div>
  </div>
</footer>

<script>
  // Word-box demo: real in-game cats speaking real in-game lines.
  const DEMO = {demo_json};
  const faceEl = document.getElementById("demoFace");
  const nameEl = document.getElementById("demoName");
  const lineEl = document.getElementById("demoLine");
  if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {{
    const sleep = (ms) => new Promise(r => setTimeout(r, ms));
    (async function loop() {{
      let i = 0;
      for (;;) {{
        const d = DEMO[i % DEMO.length];
        faceEl.src = "assets/cats/" + d.s + ".png";
        nameEl.textContent = d.n;
        lineEl.textContent = "";
        for (const ch of d.t) {{ lineEl.textContent += ch; await sleep(55); }}
        await sleep(2400);
        i++;
      }}
    }})();
  }}

  // Collection gacha: tap a hidden card to draw a real cat from the pool.
  const POOL = {pool_json};
  for (let i = POOL.length - 1; i > 0; i--) {{
    const j = Math.floor(Math.random() * (i + 1));
    [POOL[i], POOL[j]] = [POOL[j], POOL[i]];
  }}
  document.querySelectorAll(".tile.unknown").forEach(tile => {{
    const draw = () => {{
      const c = POOL.pop();
      if (!c) return;
      tile.classList.remove("unknown");
      tile.classList.add(c.t, "pop");
      tile.removeAttribute("role");
      tile.removeAttribute("tabindex");
      tile.querySelector("img").src = "assets/cats/" + c.s + ".png";
      tile.querySelector("img").alt = c.n;
      tile.querySelector(".nm").textContent = c.n;
      tile.querySelector(".rr").textContent = c.r;
    }};
    tile.addEventListener("click", draw);
    tile.addEventListener("keydown", e => {{
      if (e.key === "Enter" || e.key === " ") {{ e.preventDefault(); draw(); }}
    }});
  }});
</script>
</body>
</html>
"""
    out = ROOT / loc["file"]
    out.write_text(html, encoding="utf-8")
    print(f"wrote {loc['file']} ({len(html)} bytes)")


for key in LOCALES:
    render(key)
