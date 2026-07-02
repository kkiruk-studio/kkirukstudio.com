#!/usr/bin/env python3
"""Cats are Cute: Pop Time! landing page generator — v2 "팡팡 진화 사다리" (2026-07-02).

Generates index.html (en) + 6 flat <lang>.html files (paths must stay —
ASC/Play marketing URLs reference them).

Authentic-data rules (cats-cute build.py 전례 준수):
- REVIEWS are verbatim 5★ App Store reviews fetched per storefront via iTunes RSS (2026-07-02).
  zh-hans reuses zh-hant(TW) quotes (CN storefront has no listing);
  es mixes ES/CO/CL storefront quotes (each tiny markets).
- Ball sprites in assets/balls/ are the game's real Ball{n}_Default assets (11종 + 표정 3종).
- Store names verified per storefront (2026-07-02 iTunes lookup / Play):
  ko 고양이는 정말 팡팡 / ja ねこはほんとはじける / zh-hant 貓咪真的很爆爆 /
  zh-hans 猫咪真的很爆爆(Play) / en·es·pt Cats are Cute: Pop Time!
- Numbers: ★4.8 = 주요 스토어프런트 최저 4.82 / "10,000+" = iOS 스토어프런트
  userRatingCount 합계 10,497 (KR 3,912 + JP 3,956 + TW 1,692 + US 822 + 기타).
- 금지 표현: スイカゲーム(상표) → スイカ風, "광고 없음" → "강제 광고 없음".
- Creds (검증 근거): GP 인디 게임 페스티벌 2021 Top 20 (developers-kr.googleblog.com/2021/08/IGF2021.html),
  App Store 스토리 소개 (apps.apple.com/story/id1578830055) + '오늘의 게임' 피처드,
  테레비아사히 드라마 「無能の鷹」 3화 등장 (일본판).

Usage: python3 build.py
"""
import pathlib

ROOT = pathlib.Path(__file__).parent
BASE_URL = "https://www.kkirukstudio.com/cats-pop/"
APPSTORE_URL = "https://apps.apple.com/app/id1556403381"
PLAY_URL = "https://play.google.com/store/apps/details?id=com.game.kkiruk.catsarepop"
OG_IMAGE = "https://www.kkirukstudio.com/cats-pop/og.png"

LANG_OPTIONS = [("ko.html", "한국어"), ("index.html", "EN"), ("ja.html", "日本語"),
                ("zh-hans.html", "简体中文"), ("zh-hant.html", "繁體中文"),
                ("es.html", "Español"), ("pt.html", "Português")]

HREFLANGS = [("ko", "ko.html"), ("en", "index.html"), ("ja", "ja.html"),
             ("zh-Hans", "zh-hans.html"), ("zh-Hant", "zh-hant.html"),
             ("es", "es.html"), ("pt", "pt.html")]

REVIEW_FACES = ["ball2_oh", "ball7_wink", "ball1_surprise"]
STAT_BALLS = ["ball4", "ball7", "ball9", "ball11"]

# 검증된 실제 5★ App Store 리뷰 (storefront별 iTunes RSS 2026-07-02, verbatim)
REVIEWS = {
    "ko": ["아니 진짜 심심할때해도 좋고 고양이들이 넘 귀엽고 고양이들 떨어질 때 나는 소리도 너무 귀엽고 계속하게됨!",
           "이게 슬슬 할만하면서 은근하게 어려운게 승부욕 자극하면서 재밌네요",
           "시간 때울 때 하기 좋은 고양이 게임! 고양이의 끝은 어딜까 궁금해서 계속 하게 돼요"],
    "en": ["It’s Suika but with cute cats! What more could you possibly ask for?",
           "It’s pop time. You pop the cats. Little cats become bigger cats. Pop cats. It’s good.",
           "Super cute, super fun. I can also get to customize the cats! This is a great puzzle!"],
    "ja": ["猫のカタチのスイカゲーム。ただ、耳の出っぱりがあるから、なかなか思ったようにくっついてくれない・・・！そこがまた楽しくて、気づけば時間が経っている。クセになります！",
           "とってもかわいいです。消える音と振動が癖になる",
           "はじめたら止められない！弾けるのは私の心！"],
    "zh-hant": ["貓咪連環爆的時候很爽，好玩👍",
                "每次焦慮一玩就能平靜下來",
                "非常療癒，無壓力，可以玩很久的遊戲👍 休閒娛樂推推推！"],
    "zh-hans": ["貓咪連環爆的時候很爽，好玩👍",
                "每次焦慮一玩就能平靜下來",
                "非常療癒，無壓力，可以玩很久的遊戲👍 休閒娛樂推推推！"],
    "es": ["Este juego es súper entretenido, siento que me parece un desafío tener que desbloquear los niveles según a la medida que juegas.",
           "Es un juego muy divertido y te ayuda a pensar en tu siguiente jugada",
           "muy lindo!!"],
    "pt": ["Muito bom! Ótimo entretenimento, não precisa de internet e é bom para viagens longas!",
           "Cats Are Cute já era um dos melhores jogos da app store, mas com esse novo jogo conseguiram desenvolver meu novo vício! ❤️",
           "Baixei esse jogo por recomendação da Kim Minjeong!! ❄️ obrigada Winter por me divertir indicando este jogo, vou bater o seu recorde. 🤍"],
}

LOCALES = {
    "en": {
        "file": "index.html", "lang": "en", "head": "itim", "body_font": None, "shots": "en", "store_cc": "us",
        "name": "Cats are Cute: Pop Time!",
        "title": "Cats are Cute: Pop Time! — The suika-style cat merge puzzle",
        "desc": "Drop matching cats and they merge into bigger ones — a suika-style puzzle with 11 evolutions, 4 modes and 90+ cosmetics. ★4.8 · 10,000+ ratings · free on iOS & Android.",
        "og_title": "Cats are Cute: Pop Time! — Cat Merge Puzzle",
        "og_desc": "Merge them and they grow. Pop! ★4.8 · 10,000+ ratings.",
        "tag": "Drop matching cats to merge them bigger — and that little pop! sound pops your stress too",
        "proof": "<span class=\"s\">★4.8</span> · 10,000+ ratings worldwide · Free",
        "creds": ["🏆 Google Play Indie Games Festival TOP 20", "⭐ Featured on the App Store", "📺 Seen in a TV Asahi drama (Japan)"],
        "ios_alt": "Download on the App Store", "play_alt": "Get it on Google Play",
        "alts": ["Cat balls stacking up in the play field", "Merging two cats into a bigger one", "Decorating cats with accessories"],
        "merge_eq": "=", "rank_v": "★4.8", "rank_k": "10,000+ ratings",
        "ladder_h2": "From tiny to titanic — 11 cats to evolve", "ladder_sub": "When two matching cats meet, the next one is born. These are the real 11 from the game.",
        "tease": "And when two of the biggest cats finally meet…? Go see for yourself 🎆",
        "fb": [
            ["🐱 POP MERGE", "Cute on the surface,<br>sneaky-competitive underneath", "One rule: matching cats merge into a bigger cat. But those little cat ears make every drop roll and tumble unpredictably — that's what keeps you saying \"one more try\". The pop! sound and haptics when they burst? Pure serotonin."],
            ["🎮 4 MODES + RANKINGS", "Four ways to play,<br>one leaderboard to climb", "From laid-back Classic to finger-busting Speed, a 5-minute time attack and the Race to 1000. Every mode has its own global leaderboard — chase today's best score.", ["Classic", "Speed", "5-Minute", "Race to 1000"]],
            ["🎀 MAKE IT YOURS", "90+ cosmetics,<br>zero forced ads", "Dress your cats in glasses, hats and ribbons, and swap the board theme to match. Ads only when you choose to watch — and it works offline, anywhere."],
        ],
        "rev_h2": "Real reviews from players", "rev_sub": "Actually posted on the App Store", "rev_label": "App Store review",
        "stats": [["★4.8", "App Store rating"], ["10,000+", "Ratings worldwide"], ["11", "Cat evolutions"], ["4", "Game modes"]],
        "stats_h2": "Small game, loudly loved", "stats_sub": "By the studio behind Cats are Cute (★4.9 · 71,000+ reviews)",
        "final_h2": "Think you can reach<br>the biggest cat?", "final_lede": "Free on iOS &amp; Android",
        "f_contact": "Contact", "f_privacy": "Privacy", "f_terms": "Terms",
    },
    "ko": {
        "file": "ko.html", "lang": "ko", "head": "yeonsung", "body_font": '"Apple SD Gothic Neo","Pretendard"', "shots": "ko", "store_cc": "kr",
        "name": "고양이는 정말 팡팡",
        "title": "고양이는 정말 팡팡 — 수박게임 스타일 고양이 머지 퍼즐",
        "desc": "같은 고양이를 떨어뜨려 합치면 더 큰 고양이로 — 11종 진화, 4가지 모드, 90+ 꾸미기의 수박게임 스타일 퍼즐. ★4.8 · 전 세계 평가 10,000+ · iOS & Android 무료.",
        "og_title": "고양이는 정말 팡팡 — 고양이 머지 퍼즐",
        "og_desc": "합칠수록 커지는 고양이, 팡! ★4.8 · 평가 10,000+.",
        "tag": "같은 고양이를 합치면 더 큰 고양이로 — 팡! 터지는 소리가 스트레스까지 날려줘요",
        "proof": "<span class=\"s\">★4.8</span> · 전 세계 평가 10,000+ · 무료",
        "creds": ["🏆 구글플레이 인디 게임 페스티벌 TOP 20", "⭐ App Store 오늘의 게임 · 스토리 소개", "📺 日 드라마 「무능의 매」 등장"],
        "ios_alt": "App Store에서 다운로드", "play_alt": "Google Play에서 다운로드",
        "alts": ["고양이 볼이 쌓여가는 플레이 화면", "고양이 두 마리가 합쳐지는 순간", "액세서리로 고양이 꾸미기"],
        "merge_eq": "=", "rank_v": "★4.8", "rank_k": "평가 10,000+",
        "ladder_h2": "1번부터 11번까지, 고양이 진화 사다리", "ladder_sub": "같은 고양이 둘이 만나면 다음 고양이가 태어나요 — 게임 속 11종을 그대로 데려왔어요.",
        "tease": "그리고, 가장 큰 11번 고양이 둘이 드디어 만나면…? 직접 확인해보세요 🎆",
        "fb": [
            ["🐱 팡팡 머지", "귀여운데,<br>은근히 승부욕을 자극해요", "규칙은 하나 — 같은 고양이를 붙이면 더 큰 고양이. 그런데 뾰족한 고양이 귀 때문에 데굴데굴 구르는 물리가 마음대로 안 돼서, 자꾸 \"한 판 더\"를 외치게 되죠. 팡! 터질 때의 소리와 진동은 덤."],
            ["🎮 4가지 모드 + 랭킹", "기분 따라 골라 노는<br>네 가지 방법", "느긋한 클래식부터 손이 바빠지는 스피드, 5분 타임어택, 1000점 도전까지. 모드마다 글로벌 랭킹이 따로 있어서 오늘의 기록을 겨뤄요.", ["클래식", "스피드", "5분 도전", "1000점 도전"]],
            ["🎀 내 맘대로 꾸미기", "90+ 꾸미기,<br>강제 광고는 없어요", "안경·모자·리본으로 고양이를 꾸미고, 배경 테마도 취향대로. 광고는 보고 싶을 때만 — 인터넷 없이 오프라인에서도 언제든 한 판."],
        ],
        "rev_h2": "유저들의 진짜 리뷰", "rev_sub": "App Store에 실제로 올라온 이야기들", "rev_label": "App Store 리뷰",
        "stats": [["★4.8", "앱스토어 평점"], ["10,000+", "전 세계 평가"], ["11종", "고양이 진화"], ["4가지", "게임 모드"]],
        "stats_h2": "작지만 요란하게 사랑받는 중", "stats_sub": "「고양이는 정말 귀여워」(★4.9 · 리뷰 71,000+)를 만든 그 스튜디오",
        "final_h2": "가장 큰 고양이까지,<br>가보실래요?", "final_lede": "iOS &amp; Android 무료",
        "f_contact": "문의", "f_privacy": "개인정보 처리방침", "f_terms": "이용약관",
    },
    "ja": {
        "file": "ja.html", "lang": "ja", "head": "yomogi", "body_font": '"Hiragino Kaku Gothic ProN","Hiragino Sans","Yu Gothic"', "shots": "ja", "store_cc": "jp",
        "name": "ねこはほんとはじける",
        "title": "ねこはほんとはじける — スイカ風のねこマージパズル",
        "desc": "同じねこを落として合体させると、もっと大きなねこに — 11種の進化、4モード、90+の着せ替えのスイカ風パズル。★4.8 · 世界の評価10,000+ · iOS & Android 無料。",
        "og_title": "ねこはほんとはじける — ねこマージパズル",
        "og_desc": "合体するほど大きくなるねこ、パァン! ★4.8 · 評価10,000+。",
        "tag": "同じねこを合体させると、もっと大きなねこに — パァン!とはじける音でストレスもはじけます",
        "proof": "<span class=\"s\">★4.8</span> · 世界の評価10,000+ · 無料",
        "creds": ["📺 テレ朝ドラマ「無能の鷹」に登場", "🏆 Google Play インディーゲームフェスティバル TOP 20", "⭐ App Store フィーチャー"],
        "ios_alt": "App Storeでダウンロード", "play_alt": "Google Playで手に入れよう",
        "alts": ["ねこボールが積み上がるプレイ画面", "ねこ2匹が合体する瞬間", "アクセサリーでねこを着せ替え"],
        "merge_eq": "=", "rank_v": "★4.8", "rank_k": "評価10,000+",
        "ladder_h2": "1番から11番まで、ねこ進化のはしご", "ladder_sub": "同じねこが出会うと、次のねこが生まれます — ゲーム内の11種をそのまま連れてきました。",
        "tease": "そして、いちばん大きな11番のねこ同士がついに出会ったら…？ ぜひ自分の目で 🎆",
        "fb": [
            ["🐱 ポンポンマージ", "かわいいのに、<br>じわじわ負けず嫌いを刺激", "ルールはひとつ — 同じねこをくっつけると、もっと大きなねこに。でも、ねこ耳の出っぱりのせいでコロコロ転がる物理が思いどおりにならなくて、つい「もう一局」。パァン!とはじける音と振動はごほうびです。"],
            ["🎮 4モード + ランキング", "気分で選べる、<br>4つの遊びかた", "のんびりクラシックから、手が忙しくなるスピード、5分タイムアタック、1000点チャレンジまで。モードごとにグローバルランキングがあって、今日のハイスコアを競えます。", ["クラシック", "スピード", "5分チャレンジ", "1000点チャレンジ"]],
            ["🎀 じぶん好みに", "90+の着せ替え、<br>強制広告はありません", "メガネ・ぼうし・リボンでねこを着せ替えて、背景テーマもお好みで。広告は見たいときだけ — ネットなしのオフラインでも、いつでも一局。"],
        ],
        "rev_h2": "プレイヤーのほんとうのレビュー", "rev_sub": "App Storeに実際に投稿された声", "rev_label": "App Store レビュー",
        "stats": [["★4.8", "App Store評価"], ["10,000+", "世界の評価数"], ["11種", "ねこの進化"], ["4つ", "ゲームモード"]],
        "stats_h2": "小さいけれど、にぎやかに愛されています", "stats_sub": "「ねこはほんとかわいい」(★4.9 · レビュー71,000+)を作ったスタジオから",
        "final_h2": "いちばん大きなねこまで、<br>行けますか?", "final_lede": "iOS &amp; Android 無料",
        "f_contact": "お問い合わせ", "f_privacy": "プライバシーポリシー", "f_terms": "利用規約",
    },
    "zh-hans": {
        "file": "zh-hans.html", "lang": "zh-Hans", "head": "system-zh", "body_font": '"PingFang SC","Heiti SC"', "shots": "zh-hans", "store_cc": None,
        "name": "猫咪真的很爆爆",
        "title": "猫咪真的很爆爆 — 西瓜游戏风格的猫咪合成拼图",
        "desc": "把相同的猫咪落下合体，变成更大的猫 — 11种进化、4种模式、90+装扮的西瓜风拼图。★4.8 · 全球评分10,000+ · iOS & Android 免费。",
        "og_title": "猫咪真的很爆爆 — 猫咪合成拼图",
        "og_desc": "越合越大的猫咪，砰! ★4.8 · 评分10,000+。",
        "tag": "相同的猫咪合在一起，变成更大的猫 — 砰!的一声，压力也跟着爆掉",
        "proof": "<span class=\"s\">★4.8</span> · 全球评分10,000+ · 免费",
        "creds": ["🏆 Google Play 独立游戏节 TOP 20", "⭐ App Store 编辑推荐", "📺 登上日本朝日电视台电视剧"],
        "ios_alt": "在 App Store 下载", "play_alt": "在 Google Play 下载",
        "alts": ["猫咪球堆起来的游戏画面", "两只猫咪合体的瞬间", "用配饰装扮猫咪"],
        "merge_eq": "=", "rank_v": "★4.8", "rank_k": "评分10,000+",
        "ladder_h2": "从1号到11号，猫咪进化的阶梯", "ladder_sub": "两只相同的猫咪相遇，就会诞生下一只 — 游戏里的11种原样搬来了。",
        "tease": "那么，最大的11号猫咪终于相遇时…？亲自去看看吧 🎆",
        "fb": [
            ["🐱 砰砰合成", "看着可爱，<br>玩着悄悄激起胜负欲", "规则只有一条 — 相同的猫咪碰在一起就变大。可是尖尖的猫耳朵让物理滚动总不听话，让你忍不住喊\"再来一局\"。砰!爆开时的音效和震动是额外奖励。"],
            ["🎮 4种模式 + 排行", "看心情选择的<br>四种玩法", "从悠闲的经典模式，到手忙脚乱的极速、5分钟计时赛、1000分挑战。每个模式都有自己的全球排行榜，挑战今日最高分。", ["经典", "极速", "5分钟挑战", "1000分挑战"]],
            ["🎀 随心装扮", "90+种装扮，<br>没有强制广告", "用眼镜、帽子、蝴蝶结装扮猫咪，背景主题也随你换。广告只在你想看时出现 — 没网也能离线随时来一局。"],
        ],
        "rev_h2": "玩家的真实评价", "rev_sub": "真实发布在 App Store 上的声音", "rev_label": "App Store 评价",
        "stats": [["★4.8", "App Store 评分"], ["10,000+", "全球评分数"], ["11种", "猫咪进化"], ["4种", "游戏模式"]],
        "stats_h2": "小小的游戏，大大的喜爱", "stats_sub": "出自「猫咪真的很可爱」(★4.9 · 71,000+评价)的工作室",
        "final_h2": "敢挑战<br>最大的猫咪吗?", "final_lede": "iOS &amp; Android 免费",
        "f_contact": "联系我们", "f_privacy": "隐私政策", "f_terms": "服务条款",
    },
    "zh-hant": {
        "file": "zh-hant.html", "lang": "zh-Hant", "head": "system-zh", "body_font": '"PingFang TC","Heiti TC"', "shots": "zh-hant", "store_cc": "tw",
        "name": "貓咪真的很爆爆",
        "title": "貓咪真的很爆爆 — 西瓜遊戲風格的貓咪合成拼圖",
        "desc": "把相同的貓咪落下合體，變成更大的貓 — 11種進化、4種模式、90+裝扮的西瓜風拼圖。★4.8 · 全球評分10,000+ · iOS & Android 免費。",
        "og_title": "貓咪真的很爆爆 — 貓咪合成拼圖",
        "og_desc": "越合越大的貓咪，砰! ★4.8 · 評分10,000+。",
        "tag": "相同的貓咪合在一起，變成更大的貓 — 砰!的一聲，壓力也跟著爆掉",
        "proof": "<span class=\"s\">★4.8</span> · 全球評分10,000+ · 免費",
        "creds": ["🏆 Google Play 獨立遊戲節 TOP 20", "⭐ App Store 編輯推薦", "📺 登上日本朝日電視台電視劇"],
        "ios_alt": "在 App Store 下載", "play_alt": "在 Google Play 下載",
        "alts": ["貓咪球堆起來的遊戲畫面", "兩隻貓咪合體的瞬間", "用配飾裝扮貓咪"],
        "merge_eq": "=", "rank_v": "★4.9", "rank_k": "台灣評分 1,600+",
        "ladder_h2": "從1號到11號，貓咪進化的階梯", "ladder_sub": "兩隻相同的貓咪相遇，就會誕生下一隻 — 遊戲裡的11種原樣搬來了。",
        "tease": "那麼，最大的11號貓咪終於相遇時…？親自去看看吧 🎆",
        "fb": [
            ["🐱 爆爆合成", "看著可愛，<br>玩著悄悄激起勝負欲", "規則只有一條 — 相同的貓咪碰在一起就變大。可是尖尖的貓耳朵讓物理滾動總不聽話，讓你忍不住喊「再來一局」。砰!爆開時的音效和震動是額外獎勵。"],
            ["🎮 4種模式 + 排行", "看心情選擇的<br>四種玩法", "從悠閒的經典模式，到手忙腳亂的極速、5分鐘計時賽、1000分挑戰。每個模式都有自己的全球排行榜，挑戰今日最高分。", ["經典", "極速", "5分鐘挑戰", "1000分挑戰"]],
            ["🎀 隨心裝扮", "90+種裝扮，<br>沒有強制廣告", "用眼鏡、帽子、蝴蝶結裝扮貓咪，背景主題也隨你換。廣告只在你想看時出現 — 沒網路也能離線隨時來一局。"],
        ],
        "rev_h2": "玩家的真實評價", "rev_sub": "真實發佈在 App Store 上的聲音", "rev_label": "App Store 評價",
        "stats": [["★4.9", "台灣 App Store 評分"], ["10,000+", "全球評分數"], ["11種", "貓咪進化"], ["4種", "遊戲模式"]],
        "stats_h2": "小小的遊戲，大大的喜愛", "stats_sub": "出自「貓咪真的很可愛」(★4.9 · 71,000+則評價)的工作室",
        "final_h2": "敢挑戰<br>最大的貓咪嗎?", "final_lede": "iOS &amp; Android 免費",
        "f_contact": "聯絡我們", "f_privacy": "隱私權政策", "f_terms": "服務條款",
    },
    "es": {
        "file": "es.html", "lang": "es", "head": "itim", "body_font": None, "shots": "es", "store_cc": None,
        "name": "Cats are Cute: Pop Time!",
        "title": "Cats are Cute: Pop Time! — El puzzle de gatos estilo suika",
        "desc": "Deja caer gatos iguales y se fusionan en otros más grandes — un puzzle estilo suika con 11 evoluciones, 4 modos y 90+ cosméticos. ★4.8 · 10.000+ valoraciones · gratis en iOS y Android.",
        "og_title": "Cats are Cute: Pop Time! — Puzzle de fusión de gatos",
        "og_desc": "Fusiónalos y crecen. ¡Pop! ★4.8 · 10.000+ valoraciones.",
        "tag": "Deja caer gatos iguales para fusionarlos en más grandes — y ese ¡pop! también hace estallar tu estrés",
        "proof": "<span class=\"s\">★4.8</span> · 10.000+ valoraciones en el mundo · Gratis",
        "creds": ["🏆 TOP 20 del Indie Games Festival de Google Play", "⭐ Destacado en el App Store", "📺 Visto en una serie de TV Asahi (Japón)"],
        "ios_alt": "Descárgalo en el App Store", "play_alt": "Disponible en Google Play",
        "alts": ["Bolas de gato apilándose en el tablero", "Dos gatos fusionándose en uno más grande", "Decorando gatos con accesorios"],
        "merge_eq": "=", "rank_v": "★4.8", "rank_k": "10.000+ valoraciones",
        "ladder_h2": "De diminuto a gigante — 11 gatos por evolucionar", "ladder_sub": "Cuando dos gatos iguales se encuentran, nace el siguiente. Estos son los 11 reales del juego.",
        "tease": "¿Y cuando por fin se encuentran dos de los gatos más grandes…? Compruébalo tú mismo 🎆",
        "fb": [
            ["🐱 FUSIÓN POP", "Adorable por fuera,<br>competitivo por dentro", "Una sola regla: los gatos iguales se fusionan en uno más grande. Pero esas orejitas hacen que cada caída ruede de forma impredecible — por eso siempre dices «una más». ¿El ¡pop! y la vibración al estallar? Pura serotonina."],
            ["🎮 4 MODOS + RANKING", "Cuatro formas de jugar,<br>un ranking que escalar", "Del Clásico relajado al Speed frenético, la contrarreloj de 5 minutos y la Carrera a 1000. Cada modo tiene su propio ranking global — persigue el récord de hoy.", ["Clásico", "Speed", "5 minutos", "Carrera a 1000"]],
            ["🎀 HAZLO TUYO", "90+ cosméticos,<br>cero anuncios forzados", "Ponles gafas, sombreros y lazos a tus gatos, y cambia el tema del tablero a tu gusto. Anuncios solo si tú quieres — y funciona sin conexión, donde sea."],
        ],
        "rev_h2": "Reseñas reales de jugadores", "rev_sub": "Publicadas de verdad en el App Store", "rev_label": "Reseña del App Store",
        "stats": [["★4.8", "Nota en App Store"], ["10.000+", "Valoraciones"], ["11", "Evoluciones de gato"], ["4", "Modos de juego"]],
        "stats_h2": "Pequeño juego, querido a lo grande", "stats_sub": "Del estudio detrás de Cats are Cute (★4.9 · 71.000+ reseñas)",
        "final_h2": "¿Llegarás hasta<br>el gato más grande?", "final_lede": "Gratis en iOS y Android",
        "f_contact": "Contacto", "f_privacy": "Privacidad", "f_terms": "Términos",
    },
    "pt": {
        "file": "pt.html", "lang": "pt", "head": "itim", "body_font": None, "shots": "pt", "store_cc": "br",
        "name": "Cats are Cute: Pop Time!",
        "title": "Cats are Cute: Pop Time! — O puzzle de gatos estilo suika",
        "desc": "Solte gatos iguais e eles se fundem em gatos maiores — um puzzle estilo suika com 11 evoluções, 4 modos e 90+ cosméticos. ★4.8 · 10.000+ avaliações · grátis no iOS e Android.",
        "og_title": "Cats are Cute: Pop Time! — Puzzle de fusão de gatos",
        "og_desc": "Funda e eles crescem. Pop! ★4.8 · 10.000+ avaliações.",
        "tag": "Solte gatos iguais para fundi-los em maiores — e aquele pop! estoura o seu estresse junto",
        "proof": "<span class=\"s\">★4.8</span> · 10.000+ avaliações no mundo · Grátis",
        "creds": ["🏆 TOP 20 do Indie Games Festival do Google Play", "⭐ Destaque na App Store", "📺 Apareceu em série da TV Asahi (Japão)"],
        "ios_alt": "Baixar na App Store", "play_alt": "Disponível no Google Play",
        "alts": ["Bolas de gato se empilhando no tabuleiro", "Dois gatos se fundindo em um maior", "Decorando gatos com acessórios"],
        "merge_eq": "=", "rank_v": "★4.8", "rank_k": "10.000+ avaliações",
        "ladder_h2": "De pequenino a gigante — 11 gatos para evoluir", "ladder_sub": "Quando dois gatos iguais se encontram, nasce o próximo. Estes são os 11 reais do jogo.",
        "tease": "E quando dois dos maiores gatos finalmente se encontram…? Vá conferir você mesmo 🎆",
        "fb": [
            ["🐱 FUSÃO POP", "Fofo por fora,<br>competitivo por dentro", "Uma regra só: gatos iguais se fundem em um gato maior. Mas aquelas orelhinhas fazem cada queda rolar de um jeito imprevisível — e é por isso que você sempre diz \"só mais uma\". O pop! e a vibração quando estouram? Serotonina pura."],
            ["🎮 4 MODOS + RANKING", "Quatro jeitos de jogar,<br>um ranking para escalar", "Do Clássico tranquilo ao Speed frenético, o contra-relógio de 5 minutos e a Corrida até 1000. Cada modo tem seu próprio ranking global — persiga o recorde de hoje.", ["Clássico", "Speed", "5 minutos", "Corrida até 1000"]],
            ["🎀 DO SEU JEITO", "90+ cosméticos,<br>zero anúncios forçados", "Coloque óculos, chapéus e lacinhos nos seus gatos, e troque o tema do tabuleiro como quiser. Anúncios só quando você escolher — e funciona offline, em qualquer lugar."],
        ],
        "rev_h2": "Avaliações reais de jogadores", "rev_sub": "Publicadas de verdade na App Store", "rev_label": "Avaliação da App Store",
        "stats": [["★4.8", "Nota na App Store"], ["10.000+", "Avaliações"], ["11", "Evoluções de gato"], ["4", "Modos de jogo"]],
        "stats_h2": "Jogo pequeno, amado em grande", "stats_sub": "Do estúdio por trás de Cats are Cute (★4.9 · 71.000+ avaliações)",
        "final_h2": "Consegue chegar<br>ao maior gato?", "final_lede": "Grátis no iOS e Android",
        "f_contact": "Contato", "f_privacy": "Privacidade", "f_terms": "Termos",
    },
}

GOOGLE_FONT_LINKS = {
    "yomogi": '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link href="https://fonts.googleapis.com/css2?family=Yomogi&display=swap" rel="stylesheet">',
}
HEAD_FAMILY = {
    "yeonsung": '"BMYeonsung"',
    "itim": '"Itim Cat"',
    "yomogi": '"Yomogi"',
    "system-zh": None,  # 시스템 스택 + .hf 볼드 보정 (팡팡 카피 전용 zh 서브셋 없음)
}
FONT_FACE = {
    "yeonsung": '@font-face{font-family:"BMYeonsung";src:url("assets/fonts/BMYEONSUNG-subset.woff2") format("woff2");font-display:swap}',
    "itim": '@font-face{font-family:"Itim Cat";src:url("assets/fonts/ItimCat-subset.woff2") format("woff2");font-display:swap}',
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

    floats = "".join(
        f'<img class="float f{i+1}" src="assets/balls/{s}.png" alt="">'
        for i, s in enumerate(["ball5", "ball2", "ball8", "ball3"])
    )
    creds = "".join(f"<span>{c}</span>" for c in loc["creds"])
    ladder = ""
    for n in range(1, 12):
        if n > 1:
            ladder += '<span class="a">→</span>'
        if n == 11:
            ladder += f'<span class="last"><img class="b11" src="assets/balls/ball11.png" alt=""><span class="spark">✨</span></span>'
        else:
            ladder += f'<img class="b{n}" src="assets/balls/ball{n}.png" alt="">'
    fblocks = ""
    for i, fb in enumerate(loc["fb"]):
        pill, h2, p = fb[0], fb[1], fb[2]
        chips = ("".join(f"<span>{m}</span>" for m in fb[3])) if len(fb) > 3 else ""
        chips_html = f'<div class="modechips">{chips}</div>' if chips else ""
        fblocks += (
            f'<div class="fblock{" rev" if i == 1 else ""}">'
            f'<div class="phwrap"><img class="peek" src="assets/balls/{["ball6", "ball4", "ball10"][i]}.png" alt="">'
            f'<div class="ph"><img src="../shots/cats-pop/{loc["shots"]}-{i+1}.jpg" alt="{loc["alts"][i]}" loading="lazy"></div></div>'
            f'<div><span class="k">{pill}</span><h2 class="hf">{h2}</h2><p>{p}</p>{chips_html}</div></div>'
        )
    rcards = "".join(
        f'<div class="rcard"><img class="face" src="assets/balls/{REVIEW_FACES[i]}.png" alt="">'
        f'<div class="st">★★★★★</div><p>"{q}"</p><div class="by">{loc["rev_label"]}</div></div>'
        for i, q in enumerate(REVIEWS[key])
    )
    stats = "".join(
        f'<div class="cell"><img src="assets/balls/{b}.png" alt=""><div class="v">{v}</div><div class="k">{k}</div></div>'
        for (v, k), b in zip(loc["stats"], STAT_BALLS)
    )
    finals = "".join(
        f'<img class="float g{i+1}" src="assets/balls/{s}.png" alt="">'
        for i, s in enumerate(["ball11_wink", "ball7"])
    )

    font_face = FONT_FACE.get(loc["head"], "")
    gf_link = GOOGLE_FONT_LINKS.get(loc["head"], "")
    head_family = HEAD_FAMILY[loc["head"]]
    if head_family:
        head_css = f':root{{--head-font:{head_family}}}'
    else:
        head_css = f':root{{--head-font:{loc["body_font"]}}}\n.hf{{font-weight:800}}'
    body_font = (f'body{{font-family:{loc["body_font"]},-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}'
                 if loc["body_font"] else "")
    page_style = f'<style>\n{font_face}\n{head_css}\n{body_font}\n</style>'
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
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="kkiruk studio">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{loc['og_title']}">
<meta name="twitter:description" content="{loc['og_desc']}">
<meta name="twitter:image" content="{OG_IMAGE}">
<link rel="canonical" href="{canonical}">
{hreflang_block()}
<link rel="icon" type="image/png" href="../icons/cats-pop.png">
<link rel="apple-touch-icon" href="../icons/cats-pop.png">
{gf_link}
<link rel="stylesheet" href="style.css">
{page_style}
<script src="/ga.js"></script>
</head>
<body>

<nav>
  <div class="wrap">
    <a class="wordmark hf" href="{'index.html' if key != 'en' else './'}"><img src="../icons/cats-pop.png" alt="">{loc['name']}</a>
    {lang_select(loc['file'])}
  </div>
</nav>

<header class="hero">
  {floats}
  <img class="appicon" src="../icons/cats-pop.png" alt="{loc['name']}">
  <h1 class="hf">{loc['name']}</h1>
  <p class="tag">{loc['tag']}</p>
  <div class="badges">
    {badges(loc, key)}
  </div>
  <p class="proof hf">{loc['proof']}</p>
  <div class="creds">{creds}</div>
  <div class="fan">
    <div class="mergechip"><img src="assets/balls/ball3.png" alt=""><b>+</b><img src="assets/balls/ball3.png" alt=""><b>{loc['merge_eq']}</b><img class="big" src="assets/balls/ball4.png" alt=""></div>
    <div class="rankchip">{loc['rank_v']}<small>{loc['rank_k']}</small></div>
    <div class="ph l"><img src="../shots/cats-pop/{loc['shots']}-2.jpg" alt="{loc['alts'][0]}"></div>
    <div class="ph c"><img src="../shots/cats-pop/{loc['shots']}-1.jpg" alt="{loc['alts'][1]}"></div>
    <div class="ph r"><img src="../shots/cats-pop/{loc['shots']}-3.jpg" alt="{loc['alts'][2]}"></div>
  </div>
</header>
<div class="scallop"></div>

<section class="ladder-sec">
  <div class="wrap">
    <h2 class="sec-h hf">{loc['ladder_h2']}</h2>
    <p class="sec-sub">{loc['ladder_sub']}</p>
  </div>
  <div class="ladder" aria-hidden="true">{ladder}</div>
  <p class="tease hf">{loc['tease']}</p>
</section>

<div class="scallop cream flip"></div>
<section class="why">
  <div class="wrap">
    {fblocks}
  </div>
</section>
<div class="scallop cream"></div>

<section class="reviews">
  <div class="wrap">
    <h2 class="sec-h hf">{loc['rev_h2']}</h2>
    <p class="sec-sub">{loc['rev_sub']}</p>
    <div class="rcards">
      {rcards}
    </div>
  </div>
</section>

<div class="scallop cream flip"></div>
<section class="stats-sec">
  <div class="wrap">
    <h2 class="sec-h hf">{loc['stats_h2']}</h2>
    <p class="sec-sub">{loc['stats_sub']}</p>
    <div class="grid">
      {stats}
    </div>
  </div>
</section>
<div class="scallop cream"></div>

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
      <a href="/">kkiruk studio</a>
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
