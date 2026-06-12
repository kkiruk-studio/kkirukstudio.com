#!/usr/bin/env python3
"""Cats are Cute landing page generator — design B "표준 게임 문법 + 아기자기" (확정 2026-06-13).

Generates index.html (en) + 12 flat <lang>.html files (paths must stay —
ASC/Play marketing URLs reference them).

Authentic-data rules:
- Cat names in game_data.json come from the game's StreamingAssets (decrypted) — re-extract, don't invent.
- REVIEWS are verbatim 5★ App Store reviews fetched per storefront via iTunes RSS (2026-06-13).
  zh-hans reuses zh-hant(TW) quotes because the CN storefront has no listing.
- Heading fonts are the game's real fonts where the license allows web embedding:
  ko=BM연성체(self-host), latin/th/vi/ru=Itim "Itim Cat" subset(OFL, renamed),
  zh-hans·zh-hant=小赖体 "MaoCun" subset(OFL, renamed — 간·번 모두 커버),
  ja=Yomogi CDN (substitute — あんずもじ/Senty는 웹 임베드 불가).

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

FLOAT_SPRITES = ["cat021", "cat104", "cat302", "cat210"]
CHIP_SPRITES = ["cat001", "cat115"]
PEEK_SPRITES = ["cat118", "cat016", "cat213"]
REVIEW_FACES = ["cat007", "cat109", "cat221"]
FINAL_SPRITES = ["cat021", "cat001"]
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

# 검증된 실제 5★ App Store 리뷰 (storefront별 iTunes RSS, verbatim)
REVIEWS = {
    "ko": ["너무너무 귀여워요! 기분 안좋을때 켜면 위로댕ㅁ.. 레벨업 할때마다 고양이들이 하는 말들 넘 조아요…",
           "이제2틀차인데 너무 귀엽고 재밌어요!!그리고 이 그림 특유의 느낌이 너무 깜찍하네여~^^",
           "고양이들 너무 귀엽고 광고도 적어서 좋아요!🐈❤️"],
    "en": ["Cats are cute. This game is cute. Easy to play. I have a lovely time collecting cats!",
           "I love this game it’s so fun. My favorite cat is daisy because she lives in a flower house",
           "This game is so cute and relaxing 5 stars"],
    "ja": ["タイトル通り、ねこが本当に可愛くて癒やされます。 操作も簡単で、仕事や勉強の合間に少しずつ進められるのが良いです。",
           "かわいい猫とのびのびあそべてたのしいです。",
           "本当にかわいい癒される"],
    "zh-hant": ["畫風很簡單乾淨，貓咪很可愛，沒有什麼進度壓力，還可以領養多種不同的貓貓，既滿足了貓貓癖也滿足了收集癖。",
                "家裡沒辦法養貓咪的！建議下載這個遊戲！裡面超多可愛貓貓！！❤️",
                "真的就是純粹的可愛 而且 根本是不用課金的那種 完全免費 你只需要偶爾開起來玩 就會覺得很療癒"],
    "zh-hans": ["畫風很簡單乾淨，貓咪很可愛，沒有什麼進度壓力，還可以領養多種不同的貓貓，既滿足了貓貓癖也滿足了收集癖。",
                "家裡沒辦法養貓咪的！建議下載這個遊戲！裡面超多可愛貓貓！！❤️",
                "真的就是純粹的可愛 而且 根本是不用課金的那種 完全免費 你只需要偶爾開起來玩 就會覺得很療癒"],
    "es": ["Me encanta, es un juego sencillo, divertido y los dibujos son adorables🫠",
           "no tiene anuncios pesados y es súper bonito💗💗",
           "Amo a los gatos y este juego es muy relajante ><"],
    "pt": ["É um jogo mto relaxante e fofo, com essa estética toda eu ameiii e recomendo muitooo!!!",
           "Eu achei o jogo maravilhoso!! É uma fofura",
           "O jogo é simplesmente perfeito! Meu jogo favorito❤️recomendo baixem!"],
    "de": ["Einfach nur süß, gut zum Zeitvertreib:)",
           "Das beste Katzen Spiel der Welt😻😹😽😺🐈🐱😸",
           "Ich Liebe dieses Game einfach <3"],
    "fr": ["jeu super mignon, les dessins sont très jolis <3 ça donne une vibes très japonaise :0",
           "Très sympa, mignon et facile d’avancer dans le jeu",
           "Je pense que c’est adorable, j’adore cette jeux je le joue souvent !💕"],
    "ru": ["очень милая игра... прекрасно.",
           "Игра очень классная и успокаивающая советую!🌺💐❤️",
           "Мне очень нравится.котики милашки:3"],
    "th": ["สนุกสุดๆ ต้องลองมาฮิลใจเมี้ยวดูนะ🩷🐈‍⬛",
           "น่ารักและฮีลใจมากค่าาา",
           "แมวน่ารักม๊ากกกกกก"],
    "id": ["Benar2 seperti merawat kucing",
           "Lucuuuu",
           "very very cute and easy to play. i love catssss"],
    "vi": ["Game cute điênggg 🤍 chơi sieuu chill",
           "game cực chill, siêu hay luôn",
           "Hay lắm lun, nên tải nha.Ko bt còn ai chơi ko :>"],
}

LOCALES = {
    "en": {
        "file": "index.html", "lang": "en", "head": "itim", "body_font": None, "shots": "en",
        "name": "Cats are Cute",
        "title": "Cats are Cute — A hand-drawn village of collectible cats",
        "desc": "A calm idle game loved since 2018. Collect 60+ hand-drawn cats, feed them, and grow a cozy ink-line village. ★4.9 · 71,000+ reviews · free on iOS & Android.",
        "og_title": "Cats are Cute — Idle Cat Village",
        "og_desc": "A village drawn in ink, where only the cats are in color. ★4.9 · 71,000+ reviews.",
        "tag": "A calm idle game — collect 60+ cats and grow your own village",
        "proof": "<span class=\"s\">★4.9</span> · 71,000+ reviews · 10M+ downloads · since 2018",
        "ios_alt": "Download on the App Store", "play_alt": "Get it on Google Play",
        "alts": ["Feeding a cat in the ink-drawn village", "A cat speaking in a word box in the village", "Playing with a cat by the cafe"],
        "fb": [
            ["🐱 COLLECT", "60+ cats, each with<br>a name and a personality", "Draw new cats with tickets — Normal, Rare and Epic. Every cat has its own face, its own habits and something to say. What they tell you as you level up is the best part of the game."],
            ["🐟 TRUE IDLE", "Rewards keep stacking<br>while you're away", "Buildings produce fish on their own. A few minutes a day — feed the cats, collect hearts, and the village grows. Ads only when you choose to watch; nothing is forced."],
            ["🏠 DECORATE", "A village drawn in ink —<br>only the cats are in color", "In this hand-drawn ink-line town, the only color is the cats. Upgrade buildings and dress up every corner your way."],
        ],
        "rev_h2": "Real reviews from players", "rev_sub": "Actually posted on the App Store", "rev_label": "App Store review",
        "stats": [["★4.9", "App Store rating"], ["71,000+", "Store reviews"], ["10M+", "Downloads"], ["2018", "Running since"]],
        "stats_h2": "A cat village loved for 7 years", "stats_sub": "Run by a tiny indie studio since 2018",
        "final_h2": "The cats are waiting for you today, too", "final_lede": "Free on iOS &amp; Android",
        "f_contact": "Contact", "f_privacy": "Privacy", "f_terms": "Terms",
    },
    "ko": {
        "file": "ko.html", "lang": "ko", "head": "yeonsung", "body_font": '"Apple SD Gothic Neo","Pretendard"', "shots": "ko",
        "name": "고양이는 정말 귀여워",
        "title": "고양이는 정말 귀여워 — 잉크로 그린 고양이 마을 키우기",
        "desc": "2018년부터 사랑받아온 힐링 방치 게임. 손그림 고양이 60+마리를 모아 잉크 라인 마을을 키워보세요. ★4.9 · 리뷰 71,000+ · iOS & Android 무료.",
        "og_title": "고양이는 정말 귀여워 — 고양이 마을 키우기",
        "og_desc": "잉크로 그린 마을, 색은 고양이뿐. ★4.9 · 리뷰 71,000+.",
        "tag": "고양이 60+마리를 모아 나만의 마을을 키우는 힐링 방치 게임",
        "proof": "<span class=\"s\">★4.9</span> · 리뷰 71,000+ · 다운로드 10M+ · since 2018",
        "ios_alt": "App Store에서 다운로드", "play_alt": "Google Play에서 다운로드",
        "alts": ["잉크로 그린 마을에서 고양이 밥 주기", "말풍선으로 말하는 고양이가 있는 마을", "카페 옆에서 고양이랑 놀기"],
        "fb": [
            ["🐱 고양이 수집", "이름도 성격도 다른<br>고양이 60+마리", "뽑기로 새 고양이를 만나요. 일반부터 레어·에픽까지, 고양이마다 얼굴도 취미도 할 말도 달라요. 레벨업할 때마다 들려주는 고양이들의 말이 이 게임의 백미."],
            ["🐟 힐링 방치", "자리를 비워도<br>보상은 쌓여요", "건물이 알아서 생선을 만들어요. 하루 몇 분, 밥 주고 하트만 모으면 마을이 자라요. 광고는 보고 싶을 때만 — 강제 광고가 없어요."],
            ["🏠 마을 꾸미기", "잉크로 그린 마을,<br>색은 고양이뿐", "손그림 잉크 라인의 마을에서 컬러는 오직 고양이. 건물을 올리고 장식을 놓아 구석구석 내 취향대로 꾸며보세요."],
        ],
        "rev_h2": "유저들의 진짜 리뷰", "rev_sub": "App Store에 실제로 올라온 이야기들", "rev_label": "App Store 리뷰",
        "stats": [["★4.9", "앱스토어 평점"], ["71,000+", "전 세계 리뷰"], ["10M+", "누적 다운로드"], ["2018", "서비스 시작"]],
        "stats_h2": "7년째 사랑받는 고양이 마을", "stats_sub": "2018년부터, 작은 인디 스튜디오가 꾸준히",
        "final_h2": "오늘도 고양이들이 기다리고 있어요", "final_lede": "iOS &amp; Android 무료",
        "f_contact": "문의", "f_privacy": "개인정보 처리방침", "f_terms": "이용약관",
    },
    "ja": {
        "file": "ja.html", "lang": "ja", "head": "yomogi", "body_font": '"Hiragino Kaku Gothic ProN","Hiragino Sans","Yu Gothic"', "shots": "ja",
        "name": "ねこはほんとかわいい",
        "title": "ねこはほんとかわいい — インクで描いたねこの村を育てる",
        "desc": "2018年から愛される癒やしの放置ゲーム。手描きのねこ60匹以上を集めて、インクの線で描かれた村を育てよう。★4.9 · レビュー71,000+ · iOS & Android 無料。",
        "og_title": "ねこはほんとかわいい — ねこの村育成",
        "og_desc": "インクで描いた村。色があるのは、ねこだけ。★4.9 · レビュー71,000+。",
        "tag": "ねこを60匹以上集めて、自分だけの村を育てる癒やしの放置ゲーム",
        "proof": "<span class=\"s\">★4.9</span> · レビュー71,000+ · 累計10M+ DL · since 2018",
        "ios_alt": "App Storeでダウンロード", "play_alt": "Google Playで手に入れよう",
        "alts": ["インクで描かれた村でねこにごはん", "ふきだしで話すねこのいる村", "カフェのそばでねこと遊ぶ"],
        "fb": [
            ["🐱 ねこ集め", "名前も性格もちがう<br>ねこが60匹以上", "チケットでガチャを引いて新しいねこと出会おう。ノーマル・レア・エピック、顔もクセもみんな違う。レベルアップのたびに聞ける、ねこたちのひとことがこのゲームの真骨頂。"],
            ["🐟 ほんとうの放置", "離れていても<br>報酬は貯まる", "建物が自動でお魚を作ってくれます。1日数分、ごはんをあげてハートを集めるだけで村が育つ。広告は見たいときだけ — 強制はありません。"],
            ["🏠 村づくり", "インクで描いた村。<br>色があるのは、ねこだけ", "手描きのインクの線でできた村で、色を持つのはねこだけ。建物を育てて、すみずみまで自分好みに飾ろう。"],
        ],
        "rev_h2": "プレイヤーのほんとうのレビュー", "rev_sub": "App Storeに実際に投稿された声", "rev_label": "App Store レビュー",
        "stats": [["★4.9", "App Store評価"], ["71,000+", "世界のレビュー"], ["10M+", "累計ダウンロード"], ["2018", "サービス開始"]],
        "stats_h2": "7年間愛されてきた、ねこの村", "stats_sub": "2018年から、小さなインディースタジオがこつこつと",
        "final_h2": "今日もねこたちが待っています", "final_lede": "iOS &amp; Android 無料",
        "f_contact": "お問い合わせ", "f_privacy": "プライバシーポリシー", "f_terms": "利用規約",
    },
    "zh-hans": {
        "file": "zh-hans.html", "lang": "zh-Hans", "head": "xiaolai", "body_font": '"PingFang SC","Heiti SC"', "shots": "zh-hans",
        "name": "猫咪真的很可爱",
        "title": "猫咪真的很可爱 — 养一座墨线画成的猫咪小村",
        "desc": "自2018年起备受喜爱的治愈系放置游戏。收集60+只手绘猫咪，养大一座墨线小村。★4.9 · 71,000+条评价 · iOS & Android 免费。",
        "og_title": "猫咪真的很可爱 — 猫咪小村放置游戏",
        "og_desc": "一座墨线画成的小村，只有猫咪是彩色的。★4.9 · 71,000+条评价。",
        "tag": "收集60+只猫咪、养大自己小村的治愈系放置游戏",
        "proof": "<span class=\"s\">★4.9</span> · 评价71,000+ · 下载10M+ · since 2018",
        "ios_alt": "在 App Store 下载", "play_alt": "在 Google Play 下载",
        "alts": ["在墨线小村里给猫咪喂食", "对话框里说话的猫咪", "在咖啡店旁陪猫咪玩"],
        "fb": [
            ["🐱 收集猫咪", "60+只猫咪<br>名字和性格都不一样", "用抽奖券抽新猫咪——普通、稀有、史诗，每只的长相和习惯都不同。升级时听到的猫咪碎碎念，是这游戏最棒的部分。"],
            ["🐟 真正的放置", "离开的时候<br>奖励也在累积", "建筑会自动生产小鱼。每天几分钟，喂喂猫、收收爱心，小村就会长大。广告只在你想看时出现——没有强制。"],
            ["🏠 装扮小村", "一座墨线画成的小村<br>只有猫咪是彩色的", "在这座手绘墨线小村里，唯一的色彩就是猫咪。升级建筑、摆放装饰，把每个角落变成你的风格。"],
        ],
        "rev_h2": "玩家的真实评价", "rev_sub": "真实发布在 App Store 上的声音", "rev_label": "App Store 评价",
        "stats": [["★4.9", "App Store 评分"], ["71,000+", "全球评价"], ["10M+", "累计下载"], ["2018", "上线至今"]],
        "stats_h2": "七年来备受喜爱的猫咪小村", "stats_sub": "2018年起，由小小独立工作室用心维护",
        "final_h2": "今天，猫咪们也在等你", "final_lede": "iOS &amp; Android 免费",
        "f_contact": "联系我们", "f_privacy": "隐私政策", "f_terms": "服务条款",
    },
    "zh-hant": {
        "file": "zh-hant.html", "lang": "zh-Hant", "head": "xiaolai", "body_font": '"PingFang TC","Heiti TC"', "shots": "zh-hant",
        "name": "貓咪真的很可愛",
        "title": "貓咪真的很可愛 — 養一座墨線畫成的貓咪小村",
        "desc": "自2018年起深受喜愛的療癒系放置遊戲。收集60+隻手繪貓咪，養大一座墨線小村。★4.9 · 71,000+則評價 · iOS & Android 免費。",
        "og_title": "貓咪真的很可愛 — 貓咪小村放置遊戲",
        "og_desc": "一座墨線畫成的小村，只有貓咪是彩色的。★4.9 · 71,000+則評價。",
        "tag": "收集60+隻貓咪、養大自己小村的療癒系放置遊戲",
        "proof": "<span class=\"s\">★4.9</span> · 評價71,000+ · 下載10M+ · since 2018",
        "ios_alt": "在 App Store 下載", "play_alt": "在 Google Play 下載",
        "alts": ["在墨線小村裡給貓咪餵食", "對話框裡說話的貓咪", "在咖啡店旁陪貓咪玩"],
        "fb": [
            ["🐱 收集貓咪", "60+隻貓咪<br>名字和個性都不一樣", "用抽獎券抽新貓咪——普通、稀有、史詩，每隻的長相和習慣都不同。升級時聽到的貓咪碎碎念，是這遊戲最棒的部分。"],
            ["🐟 真正的放置", "離開的時候<br>獎勵也在累積", "建築會自動生產小魚。每天幾分鐘，餵餵貓、收收愛心，小村就會長大。廣告只在你想看時出現——沒有強制。"],
            ["🏠 裝扮小村", "一座墨線畫成的小村<br>只有貓咪是彩色的", "在這座手繪墨線小村裡，唯一的色彩就是貓咪。升級建築、擺放裝飾，把每個角落變成你的風格。"],
        ],
        "rev_h2": "玩家的真實評價", "rev_sub": "真實發佈在 App Store 上的聲音", "rev_label": "App Store 評價",
        "stats": [["★4.9", "App Store 評分"], ["71,000+", "全球評價"], ["10M+", "累計下載"], ["2018", "上線至今"]],
        "stats_h2": "七年來深受喜愛的貓咪小村", "stats_sub": "2018年起，由小小獨立工作室用心維護",
        "final_h2": "今天，貓咪們也在等你", "final_lede": "iOS &amp; Android 免費",
        "f_contact": "聯絡我們", "f_privacy": "隱私權政策", "f_terms": "服務條款",
    },
    "es": {
        "file": "es.html", "lang": "es", "head": "itim", "body_font": None, "shots": "es",
        "name": "Cats are Cute",
        "title": "Cats are Cute — Un pueblo de gatos dibujado a tinta",
        "desc": "Un idle game tranquilo, querido desde 2018. Colecciona más de 60 gatos dibujados a mano y haz crecer un pueblito de líneas de tinta. ★4.9 · 71.000+ reseñas · gratis en iOS y Android.",
        "og_title": "Cats are Cute — Pueblo de Gato",
        "og_desc": "Un pueblo dibujado a tinta, donde solo los gatos tienen color. ★4.9 · 71.000+ reseñas.",
        "tag": "Un idle game tranquilo: colecciona 60+ gatos y haz crecer tu pueblo",
        "proof": "<span class=\"s\">★4.9</span> · 71.000+ reseñas · 10M+ descargas · desde 2018",
        "ios_alt": "Descárgalo en el App Store", "play_alt": "Disponible en Google Play",
        "alts": ["Alimentando a un gato en el pueblo de tinta", "Un gato hablando en un bocadillo", "Jugando con un gato junto al café"],
        "fb": [
            ["🐱 COLECCIONA", "60+ gatos, cada uno con<br>nombre y personalidad", "Saca gatos nuevos con tickets — normales, raros y épicos. Cada gato tiene su cara, sus mañas y algo que decir. Lo que te cuentan al subir de nivel es lo mejor del juego."],
            ["🐟 IDLE DE VERDAD", "Las recompensas se acumulan<br>mientras no estás", "Los edificios producen pescado solos. Unos minutos al día — alimenta a los gatos, junta corazones y el pueblo crece. Anuncios solo si tú quieres; nada forzado."],
            ["🏠 DECORA", "Un pueblo dibujado a tinta —<br>solo los gatos tienen color", "En este pueblito de líneas de tinta dibujado a mano, el único color son los gatos. Mejora edificios y decora cada rincón a tu gusto."],
        ],
        "rev_h2": "Reseñas reales de jugadores", "rev_sub": "Publicadas de verdad en el App Store", "rev_label": "Reseña del App Store",
        "stats": [["★4.9", "Nota en App Store"], ["71.000+", "Reseñas"], ["10M+", "Descargas"], ["2018", "En marcha desde"]],
        "stats_h2": "Un pueblo de gatos querido desde hace 7 años", "stats_sub": "Desde 2018, con el cariño de un pequeño estudio indie",
        "final_h2": "Los gatos también te esperan hoy", "final_lede": "Gratis en iOS y Android",
        "f_contact": "Contacto", "f_privacy": "Privacidad", "f_terms": "Términos",
    },
    "pt": {
        "file": "pt.html", "lang": "pt", "head": "itim", "body_font": None, "shots": "pt",
        "name": "Cats are Cute",
        "title": "Cats are Cute — Uma vila de gatos desenhada a nanquim",
        "desc": "Um idle game tranquilo, querido desde 2018. Colecione mais de 60 gatos desenhados à mão e faça crescer uma vilinha de traços de nanquim. ★4.9 · 71.000+ avaliações · grátis no iOS e Android.",
        "og_title": "Cats are Cute — Cidade de Gatos",
        "og_desc": "Uma vila desenhada a nanquim, onde só os gatos têm cor. ★4.9 · 71.000+ avaliações.",
        "tag": "Um idle game tranquilo: colecione 60+ gatos e faça sua vila crescer",
        "proof": "<span class=\"s\">★4.9</span> · 71.000+ avaliações · 10M+ downloads · desde 2018",
        "ios_alt": "Baixar na App Store", "play_alt": "Disponível no Google Play",
        "alts": ["Alimentando um gato na vila de nanquim", "Um gato falando em um balão", "Brincando com um gato perto do café"],
        "fb": [
            ["🐱 COLECIONE", "60+ gatos, cada um com<br>nome e personalidade", "Tire gatos novos com tickets — normais, raros e épicos. Cada gato tem sua cara, suas manias e algo a dizer. O que eles contam quando você sobe de nível é a melhor parte do jogo."],
            ["🐟 IDLE DE VERDADE", "As recompensas continuam<br>enquanto você está fora", "Os prédios produzem peixe sozinhos. Alguns minutos por dia — alimente os gatos, junte corações e a vila cresce. Anúncios só quando você quiser; nada forçado."],
            ["🏠 DECORE", "Uma vila desenhada a nanquim —<br>só os gatos têm cor", "Nesta vilinha de traços de nanquim feita à mão, a única cor são os gatos. Melhore prédios e decore cada cantinho do seu jeito."],
        ],
        "rev_h2": "Avaliações reais de jogadores", "rev_sub": "Publicadas de verdade na App Store", "rev_label": "Avaliação da App Store",
        "stats": [["★4.9", "Nota na App Store"], ["71.000+", "Avaliações"], ["10M+", "Downloads"], ["2018", "No ar desde"]],
        "stats_h2": "Uma vila de gatos amada há 7 anos", "stats_sub": "Desde 2018, no capricho de um pequeno estúdio indie",
        "final_h2": "Os gatos estão esperando por você hoje também", "final_lede": "Grátis no iOS e Android",
        "f_contact": "Contato", "f_privacy": "Privacidade", "f_terms": "Termos",
    },
    "de": {
        "file": "de.html", "lang": "de", "head": "itim", "body_font": None, "shots": "de",
        "name": "Cats are Cute",
        "title": "Cats are Cute — Ein mit Tinte gezeichnetes Katzendorf",
        "desc": "Ein ruhiges Idle-Game, geliebt seit 2018. Sammle über 60 handgezeichnete Katzen und lass ein gemütliches Tintendorf wachsen. ★4,9 · 71.000+ Bewertungen · gratis für iOS & Android.",
        "og_title": "Cats are Cute — Idle Katzendorf",
        "og_desc": "Ein Dorf, mit Tinte gezeichnet — nur die Katzen haben Farbe. ★4,9 · 71.000+ Bewertungen.",
        "tag": "Ein ruhiges Idle-Game: sammle über 60 Katzen und lass dein Dorf wachsen",
        "proof": "<span class=\"s\">★4,9</span> · 71.000+ Bewertungen · 10M+ Downloads · seit 2018",
        "ios_alt": "Laden im App Store", "play_alt": "Jetzt bei Google Play",
        "alts": ["Eine Katze im Tintendorf füttern", "Eine Katze spricht in einer Sprechblase", "Mit einer Katze am Café spielen"],
        "fb": [
            ["🐱 SAMMELN", "Über 60 Katzen, jede mit<br>Namen und Persönlichkeit", "Zieh mit Tickets neue Katzen — Normal, Selten und Episch. Jede Katze hat ihr eigenes Gesicht, ihre Macken und etwas zu sagen. Was sie dir beim Aufleveln erzählen, ist das Beste am Spiel."],
            ["🐟 ECHTES IDLE", "Belohnungen stapeln sich,<br>auch wenn du weg bist", "Die Gebäude produzieren von selbst Fisch. Ein paar Minuten am Tag — Katzen füttern, Herzen sammeln, und das Dorf wächst. Werbung nur, wenn du willst; nichts wird erzwungen."],
            ["🏠 GESTALTEN", "Ein Dorf aus Tinte —<br>nur die Katzen haben Farbe", "In diesem handgezeichneten Tintendorf sind die Katzen die einzige Farbe. Bau Gebäude aus und gestalte jede Ecke nach deinem Geschmack."],
        ],
        "rev_h2": "Echte Bewertungen von Spielern", "rev_sub": "Wirklich im App Store gepostet", "rev_label": "App-Store-Bewertung",
        "stats": [["★4,9", "App-Store-Wertung"], ["71.000+", "Bewertungen"], ["10M+", "Downloads"], ["2018", "Online seit"]],
        "stats_h2": "Ein Katzendorf, seit 7 Jahren geliebt", "stats_sub": "Seit 2018, gepflegt von einem kleinen Indie-Studio",
        "final_h2": "Die Katzen warten auch heute auf dich", "final_lede": "Gratis für iOS &amp; Android",
        "f_contact": "Kontakt", "f_privacy": "Datenschutz", "f_terms": "Nutzungsbedingungen",
    },
    "fr": {
        "file": "fr.html", "lang": "fr", "head": "itim", "body_font": None, "shots": "fr",
        "name": "Cats are Cute",
        "title": "Cats are Cute — Un village de chats dessiné à l'encre",
        "desc": "Un idle game paisible, aimé depuis 2018. Collectionnez plus de 60 chats dessinés à la main et faites grandir un petit village à l'encre. ★4,9 · 71 000+ avis · gratuit sur iOS et Android.",
        "og_title": "Cats are Cute — Ville des Chats",
        "og_desc": "Un village dessiné à l'encre, où seuls les chats sont en couleur. ★4,9 · 71 000+ avis.",
        "tag": "Un idle game paisible : collectionnez 60+ chats et faites grandir votre village",
        "proof": "<span class=\"s\">★4,9</span> · 71 000+ avis · 10M+ téléchargements · depuis 2018",
        "ios_alt": "Télécharger dans l'App Store", "play_alt": "Disponible sur Google Play",
        "alts": ["Nourrir un chat dans le village à l'encre", "Un chat qui parle dans une bulle", "Jouer avec un chat près du café"],
        "fb": [
            ["🐱 COLLECTIONNEZ", "60+ chats, chacun avec<br>un nom et un caractère", "Tirez de nouveaux chats avec des tickets — normaux, rares et épiques. Chaque chat a sa frimousse, ses manies et son mot à dire. Ce qu'ils vous racontent en montant de niveau est le meilleur du jeu."],
            ["🐟 VRAI IDLE", "Les récompenses s'accumulent<br>même en votre absence", "Les bâtiments produisent du poisson tout seuls. Quelques minutes par jour — nourrissez les chats, récoltez des cœurs, et le village grandit. La pub, seulement si vous le choisissez ; rien d'imposé."],
            ["🏠 DÉCOREZ", "Un village dessiné à l'encre —<br>seuls les chats sont en couleur", "Dans ce petit village tracé à l'encre, la seule couleur, ce sont les chats. Améliorez les bâtiments et décorez chaque recoin à votre goût."],
        ],
        "rev_h2": "De vrais avis de joueurs", "rev_sub": "Vraiment publiés sur l'App Store", "rev_label": "Avis App Store",
        "stats": [["★4,9", "Note App Store"], ["71 000+", "Avis"], ["10M+", "Téléchargements"], ["2018", "En ligne depuis"]],
        "stats_h2": "Un village de chats aimé depuis 7 ans", "stats_sub": "Depuis 2018, entretenu par un petit studio indé",
        "final_h2": "Les chats vous attendent aujourd'hui aussi", "final_lede": "Gratuit sur iOS et Android",
        "f_contact": "Contact", "f_privacy": "Confidentialité", "f_terms": "Conditions",
    },
    "ru": {
        "file": "ru.html", "lang": "ru", "head": "itim", "body_font": None, "shots": "ru",
        "name": "Cats are Cute",
        "title": "Cats are Cute — Кошачья деревня, нарисованная тушью",
        "desc": "Спокойная idle-игра, любимая с 2018 года. Соберите 60+ нарисованных от руки котов и вырастите уютную деревню из чернильных линий. ★4,9 · 71 000+ отзывов · бесплатно на iOS и Android.",
        "og_title": "Cats are Cute — Idle котов",
        "og_desc": "Деревня, нарисованная тушью, — цветные здесь только коты. ★4,9 · 71 000+ отзывов.",
        "tag": "Спокойная idle-игра: соберите 60+ котов и вырастите свою деревню",
        "proof": "<span class=\"s\">★4,9</span> · 71 000+ отзывов · 10M+ загрузок · с 2018",
        "ios_alt": "Загрузите в App Store", "play_alt": "Доступно в Google Play",
        "alts": ["Кормим кота в нарисованной тушью деревне", "Кот говорит в облачке", "Играем с котом у кафе"],
        "fb": [
            ["🐱 КОЛЛЕКЦИЯ", "60+ котов, у каждого —<br>имя и характер", "Тяните билетики и знакомьтесь с новыми котами — обычными, редкими и эпическими. У каждого своя мордочка, свои привычки и что сказать. Их реплики при повышении уровня — лучшее в игре."],
            ["🐟 НАСТОЯЩИЙ IDLE", "Награды копятся,<br>пока вас нет", "Здания сами производят рыбу. Пара минут в день — покормить котов, собрать сердечки, и деревня растёт. Реклама — только по вашему желанию; ничего принудительного."],
            ["🏠 ДЕКОР", "Деревня из туши —<br>цветные здесь только коты", "В этом нарисованном от руки чернильном городке единственный цвет — коты. Улучшайте здания и украшайте каждый уголок по своему вкусу."],
        ],
        "rev_h2": "Настоящие отзывы игроков", "rev_sub": "Реально опубликованы в App Store", "rev_label": "Отзыв в App Store",
        "stats": [["★4,9", "Рейтинг App Store"], ["71 000+", "Отзывов"], ["10M+", "Загрузок"], ["2018", "Работает с"]],
        "stats_h2": "Кошачья деревня, любимая уже 7 лет", "stats_sub": "С 2018 года — заботой маленькой инди-студии",
        "final_h2": "Коты ждут вас и сегодня", "final_lede": "Бесплатно на iOS и Android",
        "f_contact": "Связаться", "f_privacy": "Конфиденциальность", "f_terms": "Условия",
    },
    "th": {
        "file": "th.html", "lang": "th", "head": "itim", "body_font": '"Thonburi"', "shots": "th",
        "name": "Cats are Cute",
        "title": "Cats are Cute — หมู่บ้านแมวที่วาดด้วยหมึก",
        "desc": "เกม idle สุดชิลที่มีคนรักมาตั้งแต่ปี 2018 สะสมแมววาดมือกว่า 60 ตัว แล้วปลูกหมู่บ้านลายเส้นหมึกแสนอบอุ่น ★4.9 · รีวิว 71,000+ · เล่นฟรีบน iOS และ Android",
        "og_title": "Cats are Cute — หมู่บ้านแมว idle",
        "og_desc": "หมู่บ้านที่วาดด้วยหมึก มีแค่แมวเท่านั้นที่มีสี ★4.9 · รีวิว 71,000+",
        "tag": "เกม idle สุดชิล สะสมแมวกว่า 60 ตัวแล้วปลูกหมู่บ้านของคุณเอง",
        "proof": "<span class=\"s\">★4.9</span> · รีวิว 71,000+ · ดาวน์โหลด 10M+ · ตั้งแต่ 2018",
        "ios_alt": "ดาวน์โหลดบน App Store", "play_alt": "ดาวน์โหลดบน Google Play",
        "alts": ["ให้อาหารแมวในหมู่บ้านลายหมึก", "แมวกำลังพูดในกล่องข้อความ", "เล่นกับแมวข้างคาเฟ่"],
        "fb": [
            ["🐱 สะสมแมว", "แมวกว่า 60 ตัว แต่ละตัว<br>มีชื่อและนิสัยของตัวเอง", "ใช้ตั๋วสุ่มเพื่อพบแมวใหม่ ๆ — ธรรมดา แรร์ และอีพิค หน้าตาและนิสัยไม่ซ้ำกันเลย คำพูดของเหล่าแมวตอนเลเวลอัปคือเสน่ห์ที่สุดของเกมนี้"],
            ["🐟 IDLE ของแท้", "รางวัลสะสมต่อเนื่อง<br>แม้ตอนคุณไม่อยู่", "อาคารผลิตปลาให้เองอัตโนมัติ วันละไม่กี่นาที — ให้อาหารแมว เก็บหัวใจ หมู่บ้านก็โตขึ้น โฆษณาดูเฉพาะตอนที่คุณเลือกเอง ไม่มีบังคับ"],
            ["🏠 แต่งหมู่บ้าน", "หมู่บ้านที่วาดด้วยหมึก —<br>มีแค่แมวเท่านั้นที่มีสี", "ในหมู่บ้านลายเส้นหมึกวาดมือแห่งนี้ สีเดียวที่มีคือเหล่าแมว อัปเกรดอาคารและแต่งทุกมุมตามใจคุณ"],
        ],
        "rev_h2": "รีวิวจริงจากผู้เล่น", "rev_sub": "โพสต์จริงบน App Store", "rev_label": "รีวิว App Store",
        "stats": [["★4.9", "คะแนน App Store"], ["71,000+", "รีวิวทั่วโลก"], ["10M+", "ยอดดาวน์โหลด"], ["2018", "เปิดบริการตั้งแต่"]],
        "stats_h2": "หมู่บ้านแมวที่มีคนรักมา 7 ปี", "stats_sub": "ตั้งแต่ 2018 โดยสตูดิโออินดี้เล็ก ๆ",
        "final_h2": "วันนี้เหล่าแมวก็รอคุณอยู่นะ", "final_lede": "เล่นฟรีบน iOS และ Android",
        "f_contact": "ติดต่อเรา", "f_privacy": "นโยบายความเป็นส่วนตัว", "f_terms": "ข้อกำหนด",
    },
    "id": {
        "file": "id.html", "lang": "id", "head": "itim", "body_font": None, "shots": "id",
        "name": "Cats are Cute",
        "title": "Cats are Cute — Desa kucing yang digambar dengan tinta",
        "desc": "Game idle santai yang dicintai sejak 2018. Kumpulkan 60+ kucing gambar tangan dan besarkan desa mungil bergaris tinta. ★4,9 · 71.000+ ulasan · gratis di iOS & Android.",
        "og_title": "Cats are Cute — Kucing Lucu",
        "og_desc": "Desa yang digambar dengan tinta — hanya kucingnya yang berwarna. ★4,9 · 71.000+ ulasan.",
        "tag": "Game idle santai: kumpulkan 60+ kucing dan besarkan desamu sendiri",
        "proof": "<span class=\"s\">★4,9</span> · 71.000+ ulasan · 10M+ unduhan · sejak 2018",
        "ios_alt": "Unduh di App Store", "play_alt": "Tersedia di Google Play",
        "alts": ["Memberi makan kucing di desa garis tinta", "Kucing berbicara di kotak kata", "Bermain dengan kucing di dekat kafe"],
        "fb": [
            ["🐱 KUMPULKAN", "60+ kucing, masing-masing punya<br>nama dan kepribadian", "Gacha kucing baru dengan tiket — Normal, Langka, dan Epik. Setiap kucing punya wajah, kebiasaan, dan sesuatu untuk dikatakan. Celotehan mereka saat naik level adalah bagian terbaiknya."],
            ["🐟 IDLE SUNGGUHAN", "Hadiah terus menumpuk<br>saat kamu pergi", "Bangunan memproduksi ikan sendiri. Beberapa menit sehari — beri makan kucing, kumpulkan hati, dan desa pun tumbuh. Iklan hanya kalau kamu mau; tidak ada yang dipaksakan."],
            ["🏠 DEKORASI", "Desa yang digambar dengan tinta —<br>hanya kucingnya yang berwarna", "Di desa garis tinta gambar tangan ini, satu-satunya warna adalah para kucing. Tingkatkan bangunan dan hias tiap sudut sesukamu."],
        ],
        "rev_h2": "Ulasan asli dari pemain", "rev_sub": "Benar-benar diposting di App Store", "rev_label": "Ulasan App Store",
        "stats": [["★4,9", "Rating App Store"], ["71.000+", "Ulasan"], ["10M+", "Unduhan"], ["2018", "Beroperasi sejak"]],
        "stats_h2": "Desa kucing yang dicintai 7 tahun", "stats_sub": "Sejak 2018, dirawat studio indie kecil",
        "final_h2": "Hari ini pun para kucing menunggumu", "final_lede": "Gratis di iOS &amp; Android",
        "f_contact": "Kontak", "f_privacy": "Privasi", "f_terms": "Ketentuan",
    },
    "vi": {
        "file": "vi.html", "lang": "vi", "head": "itim", "body_font": None, "shots": "vi",
        "name": "Cats are Cute",
        "title": "Cats are Cute — Ngôi làng mèo vẽ bằng mực",
        "desc": "Game idle nhẹ nhàng được yêu thích từ 2018. Sưu tầm hơn 60 chú mèo vẽ tay và nuôi lớn một ngôi làng nét mực ấm áp. ★4,9 · 71.000+ đánh giá · miễn phí trên iOS & Android.",
        "og_title": "Cats are Cute — Mèo Dễ Cưng",
        "og_desc": "Ngôi làng vẽ bằng mực — chỉ những chú mèo là có màu. ★4,9 · 71.000+ đánh giá.",
        "tag": "Game idle nhẹ nhàng: sưu tầm hơn 60 chú mèo và xây ngôi làng của riêng bạn",
        "proof": "<span class=\"s\">★4,9</span> · 71.000+ đánh giá · 10M+ lượt tải · từ 2018",
        "ios_alt": "Tải về trên App Store", "play_alt": "Tải về trên Google Play",
        "alts": ["Cho mèo ăn trong ngôi làng nét mực", "Chú mèo nói trong khung thoại", "Chơi với mèo cạnh quán cà phê"],
        "fb": [
            ["🐱 SƯU TẦM", "Hơn 60 chú mèo, mỗi bé<br>một cái tên, một tính cách", "Dùng vé quay để gặp mèo mới — Thường, Hiếm và Sử thi. Mỗi bé một gương mặt, một thói quen và cả những điều muốn nói. Lời mèo nói khi bạn lên cấp chính là phần thú vị nhất."],
            ["🐟 IDLE ĐÍCH THỰC", "Phần thưởng vẫn tích lũy<br>khi bạn vắng mặt", "Các tòa nhà tự sản xuất cá. Mỗi ngày vài phút — cho mèo ăn, gom tim, ngôi làng cứ thế lớn lên. Quảng cáo chỉ khi bạn muốn; không gì ép buộc."],
            ["🏠 TRANG TRÍ", "Ngôi làng vẽ bằng mực —<br>chỉ những chú mèo là có màu", "Trong ngôi làng nét mực vẽ tay này, màu sắc duy nhất là lũ mèo. Nâng cấp nhà cửa và bày biện từng góc nhỏ theo ý bạn."],
        ],
        "rev_h2": "Đánh giá thật từ người chơi", "rev_sub": "Được đăng thật trên App Store", "rev_label": "Đánh giá App Store",
        "stats": [["★4,9", "Điểm App Store"], ["71.000+", "Đánh giá"], ["10M+", "Lượt tải"], ["2018", "Vận hành từ"]],
        "stats_h2": "Ngôi làng mèo được yêu suốt 7 năm", "stats_sub": "Từ 2018, bởi một studio indie nhỏ",
        "final_h2": "Hôm nay lũ mèo vẫn đang đợi bạn", "final_lede": "Miễn phí trên iOS &amp; Android",
        "f_contact": "Liên hệ", "f_privacy": "Quyền riêng tư", "f_terms": "Điều khoản",
    },
}

GOOGLE_FONT_LINKS = {
    "yomogi": '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link href="https://fonts.googleapis.com/css2?family=Yomogi&display=swap" rel="stylesheet">',
}
HEAD_FAMILY = {
    "yeonsung": '"BMYeonsung"',
    "itim": '"Itim Cat"',
    "yomogi": '"Yomogi"',
    "xiaolai": '"MaoCun"',
}
FONT_FACE = {
    "yeonsung": '@font-face{font-family:"BMYeonsung";src:url("assets/fonts/BMYEONSUNG-subset.woff2") format("woff2");font-display:swap}',
    "itim": '@font-face{font-family:"Itim Cat";src:url("assets/fonts/ItimCat-subset.woff2") format("woff2");font-display:swap}',
    # 小赖体(Xiaolai, OFL) 서브셋 — 예약명 회피로 "MaoCun" 리네임. zh 카피/고양이 이름/리뷰의
    # 한자만 포함하므로 zh 텍스트 변경 시 재서브셋 필요:
    #   pyftsubset Xiaolai-Regular.ttf --text-file=<zh 전체 텍스트> --flavor=woff2 + name 테이블 리네임
    "xiaolai": '@font-face{font-family:"MaoCun";src:url("assets/fonts/MaoCun-subset.woff2") format("woff2");font-display:swap}',
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


def badges(loc, key):
    return (f'<a href="{APPSTORE_URL}"><img class="apple" src="assets/badges/ios-{key}.svg" alt="{loc["ios_alt"]}"></a>\n'
            f'      <a href="{PLAY_URL}"><img src="assets/badges/play-{key}.png" alt="{loc["play_alt"]}"></a>')


def render(key):
    loc = LOCALES[key]
    by_sprite = {c["sprite"]: c for c in GAME[key]["cats"]}

    floats = "".join(
        f'<img class="float f{i+1}" src="assets/cats/{s}.png" alt="">'
        for i, s in enumerate(FLOAT_SPRITES)
    )
    chips = "".join(
        f'<div class="chip ch{i+1}"><img src="assets/cats/{s}.png" alt="">{by_sprite[s]["name"]} <span class="hh">♥</span></div>'
        for i, s in enumerate(CHIP_SPRITES)
    )
    marquee = "".join(
        f'<img src="assets/cats/{s}.png" alt="" loading="lazy">'
        for s in MARQUEE_SPRITES * 2
    )
    fblocks = "".join(
        f'<div class="fblock{" rev" if i == 1 else ""}">'
        f'<div class="phwrap"><img class="peek" src="assets/cats/{PEEK_SPRITES[i]}.png" alt="">'
        f'<div class="ph"><img src="../shots/cats-cute/{loc["shots"]}-{i+1}.jpg" alt="{loc["alts"][i] if i < len(loc["alts"]) else ""}" loading="lazy"></div></div>'
        f'<div><span class="k">{pill}</span><h2 class="hf">{h2}</h2><p>{p}</p></div></div>'
        for i, (pill, h2, p) in enumerate(loc["fb"])
    )
    rcards = "".join(
        f'<div class="rcard"><img class="face" src="assets/cats/{REVIEW_FACES[i]}.png" alt="">'
        f'<div class="st">★★★★★</div><p>"{q}"</p><div class="by">{loc["rev_label"]}</div></div>'
        for i, q in enumerate(REVIEWS[key])
    )
    stats = "".join(
        f'<div class="cell"><img src="assets/ui/{ic}.png" alt=""><div class="v">{v}</div><div class="k">{k}</div></div>'
        for (v, k), ic in zip(loc["stats"], ["toy", "heart", "catfish", "collection"])
    )
    skyline = "".join(
        f'<img src="assets/cats/{item.split(":")[1]}.png" style="height:{h}px" alt="">'
        if item.startswith("__cat:")
        else f'<img src="assets/props/{item}.png" style="height:{h}px" alt="" loading="lazy">'
        for item, h in SKYLINE
    )
    finals = "".join(
        f'<img class="float g{i+1}" src="assets/cats/{s}.png" alt="">'
        for i, s in enumerate(FINAL_SPRITES)
    )

    font_face = FONT_FACE.get(loc["head"], "")
    gf_link = GOOGLE_FONT_LINKS.get(loc["head"], "")
    body_font = (f'body{{font-family:{loc["body_font"]},-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}'
                 if loc["body_font"] else "")
    page_style = f'<style>\n{font_face}\n:root{{--head-font:{HEAD_FAMILY[loc["head"]]}}}\n{body_font}\n</style>'
    canonical = BASE_URL if key == "en" else f'{BASE_URL}{loc["file"]}'

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
{gf_link}
<link rel="stylesheet" href="style.css">
{page_style}
<script src="/ga.js"></script>
</head>
<body>

<nav>
  <div class="wrap">
    <a class="wordmark hf" href="{'index.html' if key != 'en' else './'}"><img src="../icons/cats-cute.png" alt="">{loc['name']}</a>
    {lang_select(loc['file'])}
  </div>
</nav>

<header class="hero">
  {floats}
  <img class="float fh h1" src="assets/ui/heart.png" alt="">
  <img class="float fh h2" src="assets/ui/heart.png" alt="">
  <img class="appicon" src="../icons/cats-cute.png" alt="{loc['name']}">
  <h1 class="hf">{loc['name']}</h1>
  <p class="tag">{loc['tag']}</p>
  <div class="badges">
    {badges(loc, key)}
  </div>
  <p class="proof hf">{loc['proof']}</p>
  <div class="fan">
    {chips}
    <div class="ph l"><img src="../shots/cats-cute/{loc['shots']}-2.jpg" alt="{loc['alts'][0]}"></div>
    <div class="ph c"><img src="../shots/cats-cute/{loc['shots']}-1.jpg" alt="{loc['alts'][1]}"></div>
    <div class="ph r"><img src="../shots/cats-cute/{loc['shots']}-3.jpg" alt="{loc['alts'][2]}"></div>
  </div>
</header>
<div class="scallop"></div>

<div class="marquee" aria-hidden="true"><div class="track">{marquee}</div></div>

<section>
  <div class="wrap">
    {fblocks}
  </div>
</section>

<div class="scallop cream flip"></div>
<section class="reviews">
  <div class="wrap">
    <h2 class="sec-h hf">{loc['rev_h2']}</h2>
    <p class="sec-sub">{loc['rev_sub']}</p>
    <div class="rcards">
      {rcards}
    </div>
  </div>
</section>
<div class="scallop cream"></div>

<section class="stats-sec">
  <div class="wrap">
    <h2 class="sec-h hf">{loc['stats_h2']}</h2>
    <p class="sec-sub">{loc['stats_sub']}</p>
    <div class="grid">
      {stats}
    </div>
  </div>
</section>

<div class="skyline" aria-hidden="true"><div class="row">{skyline}</div></div>

<section class="final">
  {finals}
  <div class="wrap">
    <h2 class="hf">{loc['final_h2']}</h2>
    <p>{loc['final_lede']}</p>
    <div class="badges">
      {badges(loc, key)}
    </div>
  </div>
</section>

<footer>
  <div class="wrap">
    <div>© 2026 kkiruk studio</div>
    <div class="links">
      <a href="mailto:kkirukstudio.help@gmail.com">{loc['f_contact']}</a>
      <a href="https://kkiruk-studio.github.io/privacy-policy-app/">{loc['f_privacy']}</a>
      <a href="https://kkiruk-studio.github.io/terms-of-service-app/">{loc['f_terms']}</a>
    </div>
  </div>
</footer>

</body>
</html>
"""
    out = ROOT / loc["file"]
    out.write_text(html, encoding="utf-8")
    print(f"wrote {loc['file']} ({len(html)} bytes)")


for key in LOCALES:
    render(key)
