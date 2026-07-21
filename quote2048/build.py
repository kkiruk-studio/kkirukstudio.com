#!/usr/bin/env python3
"""Generate index.html for every locale from one template.

Usage: python3 build.py
Output: ./index.html (en), ./ko/index.html, ./ja/index.html,
        ./zh-hans/index.html, ./zh-hant/index.html
Edit this file only — never hand-edit generated HTML.
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).parent
BASE_URL = "https://www.kkirukstudio.com/quote2048/"

APPLE_SVG = '<svg viewBox="0 0 384 512" aria-hidden="true"><path d="M318.7 268.7c-.2-36.7 16.4-64.4 50-84.8-18.8-26.9-47.2-41.7-84.7-44.6-35.5-2.8-74.3 20.7-88.5 20.7-15 0-49.4-19.7-76.4-19.7C63.3 141.2 4 184.8 4 273.5q0 39.3 14.4 81.2c12.8 36.7 59 126.7 107.2 125.2 25.2-.6 43-17.9 75.8-17.9 31.8 0 48.3 17.9 76.4 17.9 48.6-.7 90.4-82.5 102.6-119.3-65.2-30.7-61.7-90-61.7-91.9zm-56.6-164.2c27.3-32.4 24.8-61.9 24-72.5-24.1 1.4-52 16.4-67.9 34.9-17.5 19.8-27.8 44.3-25.6 71.9 26.1 2 49.9-11.4 69.5-34.3z"/></svg>'

LANG_LABELS = [("", "EN"), ("ko/", "한국어"), ("ja/", "日本語"), ("zh-hans/", "简体"), ("zh-hant/", "繁體")]

LOCALES = {
    "en": {
        "dir": "", "lang": "en", "font": None,
        "title": "Quote 2048 — Merge tiles into famous quotes",
        "desc": "The 2048 you know, but sentences grow instead of numbers. Merge matching quote tiles up 56 themes and 952 verified quotes — from a humble proverb to a crown quote — set against public-domain masterpieces.",
        "og_title": "Quote 2048 — A quiet text-merge puzzle",
        "og_desc": "Merge matching quotes and watch wisdom grow, from a proverb to a crown quote.",
        "kicker_num": "TEXT MERGE PUZZLE",
        "h1": "The 2048 you know — but <em>sentences grow</em> instead of numbers.",
        "sub": "Merge two matching quote tiles and the words grow into a greater one. Climb from a humble proverb all the way to the crown quote at 2048.",
        "note": "FREE · IPHONE &amp; IPAD · NO ACCOUNT",
        "badge_small": "Download on the", "badge_aria": "Download on the App Store",
        "chips": [["S", "Shakespeare"], ["N", "Nietzsche"], ["孔", "Confucius"], ["夏", "Sōseki"]],
        "hero_alt": "Quote 2048 theme browser — a grid of masterpiece paintings, one per theme",
        "marquee": ["Shakespeare", "Nietzsche", "Confucius", "Tolstoy", "Virginia Woolf", "Laozi", "Rumi", "Kafka", "Marcus Aurelius", "Jane Austen"],
        "how_kicker": "HOW IT PLAYS",
        "how_h2": "Merge. Grow. <em>Complete the quote.</em>",
        "steps": [
            ["MERGE", "Swipe to merge", "Two tiles with the same quote merge into one — pure 2048 rules you already know."],
            ["GROW", "Watch it grow", "Each merge lifts the words to a greater quote, one tier up the ladder."],
            ["COMPLETE", "Reach the crown", "Hit the 2048 tile to complete the theme's crown quote and collect it."],
        ],
        "lad_kicker": "THE LADDER", "lad_num": "2 → 2048",
        "lad_h2": "One theme, <em>eleven quotes</em>, climbing.",
        "lad_lede": "Every theme is a ladder — a light proverb at the bottom, the icon quote at the crown. This is the Beginnings theme.",
        "ladder": [
            ["2", "Well begun is half done", "Proverb"],
            ["8", "It's never too late", "—"],
            ["128", "Knock, and it will be opened", "Scripture"],
            ["512", "Let there be light", "Genesis"],
            ["2048", "A great tree grows from a small sprout", "Laozi"],
        ],
        "cnt_kicker": "WHAT'S INSIDE", "cnt_num": "56 · 952",
        "cnt_h2": "Real quotes. <em>Real paintings.</em>",
        "cnt_lede": "Nothing fabricated — every line is checked against its source, every backdrop is a public-domain masterpiece.",
        "provs": [
            ["24", "Topic themes", "Beginnings, Calm, Courage, Happiness and more — all free."],
            ["32", "Author collections", "Shakespeare, Nietzsche, Tolstoy, Confucius, Woolf — a Pro shelf."],
            ["952", "Verified quotes", "From real works, in five languages, with originals in Latin, German, Classical Chinese."],
            ["56", "Masterpieces", "Monet, van Gogh, Klimt, Hokusai — one painting behind every theme."],
        ],
        "shots_kicker": "SCREENS", "shots_num": "IOS",
        "shots_h2": "A gallery you play <em>one tile at a time</em>.",
        "shots_caps": ["A quiet board", "56 painted themes", "Sentences, not numbers"],
        "feat_kicker": "DETAILS", "feat_num": "07",
        "feat_h2": "Small game, <em>deliberate choices</em>.",
        "feats": [
            ["No fake quotes", "Every line verified against its source. Internet misattributions were left out on purpose."],
            ["Original languages", "See the crown quote in its own tongue — Latin, German, Russian, Classical Chinese."],
            ["Your own theme pack", "Write 11 lines of your own — resolutions, mottos, cheers — and play them. Your name goes on the card."],
            ["A quote ladder to collect", "Every theme keeps a ladder of what you've reached — a quiet dogam of wisdom."],
            ["Offline, no login", "Everything is bundled. No account, no server. No ads, ever."],
            ["Quiet by design", "Calm pace, soft palettes, a “who said this?” quiz after each clear. Play at your own tempo."],
            ["Beyond the crown", "Keep going past 2048, all the way to 131072 — every new record reveals a fresh quote."],
        ],
        "final_h2": "Grow a quote today.", "final_lede": "Free on iPhone &amp; iPad.",
        "f_contact": "Contact", "f_privacy": "Privacy Policy", "f_terms": "Terms of Service",
    },
    "ko": {
        "dir": "ko/", "lang": "ko", "font": None,
        "title": "명언 2048 — 문장을 합쳐 명언을 키우는 퍼즐",
        "desc": "알던 2048, 그런데 숫자가 아니라 문장이 자랍니다. 같은 명언 타일을 합쳐 56개 테마·952개의 검증된 명언을 속담에서 왕관 명언까지 키우세요. 배경은 퍼블릭 도메인 명화.",
        "og_title": "명언 2048 — 조용한 텍스트 2048",
        "og_desc": "같은 문장을 합치면 명언이 자라납니다. 속담에서 왕관 명언까지.",
        "kicker_num": "텍스트 머지 퍼즐",
        "h1": "알던 2048, 그런데 숫자가 아니라 <em>문장이 자랍니다.</em>",
        "sub": "같은 명언 타일 두 개를 합치면 더 큰 명언이 됩니다. 가벼운 속담에서 시작해 2048의 왕관 명언까지 키워 보세요.",
        "note": "무료 · iPhone &amp; iPad · 계정 없음",
        "badge_small": "다운로드", "badge_aria": "App Store에서 다운로드",
        "chips": [["S", "셰익스피어"], ["N", "니체"], ["孔", "공자"], ["夏", "소세키"]],
        "hero_alt": "명언 2048 테마 브라우저 — 테마마다 명화가 깔린 그리드",
        "marquee": ["셰익스피어", "니체", "공자", "톨스토이", "버지니아 울프", "노자", "루미", "카프카", "마르쿠스 아우렐리우스", "제인 오스틴"],
        "how_kicker": "플레이 방법",
        "how_h2": "합치고. 키우고. <em>명언을 완성하세요.</em>",
        "steps": [
            ["합치기", "밀어서 합치기", "같은 명언 타일 두 개가 하나로 — 이미 아는 순정 2048 규칙 그대로."],
            ["키우기", "자라나는 문장", "합칠 때마다 문장이 한 단계 위 명언으로 격상됩니다."],
            ["완성", "왕관에 도달", "2048 타일을 만들면 그 테마의 왕관 명언이 완성되고 소장됩니다."],
        ],
        "lad_kicker": "명언 사다리", "lad_num": "2 → 2048",
        "lad_h2": "한 테마, <em>열한 개의 명언</em>이 오릅니다.",
        "lad_lede": "모든 테마는 사다리입니다 — 밑엔 가벼운 속담, 왕관엔 누구나 아는 명언. 아래는 「시작」 테마.",
        "ladder": [
            ["2", "시작이 반이다", "속담"],
            ["8", "늦은 때는 없다", "—"],
            ["128", "두드리라 그리하면 열릴 것이다", "성경"],
            ["512", "태초에 빛이 있으라 하셨다", "성경"],
            ["2048", "큰 나무도 작은 싹에서 자란다", "노자"],
        ],
        "cnt_kicker": "무엇이 담겼나", "cnt_num": "56 · 952",
        "cnt_h2": "진짜 명언. <em>진짜 그림.</em>",
        "cnt_lede": "지어낸 것 없이 — 모든 문장은 출처를 대조했고, 모든 배경은 퍼블릭 도메인 명화입니다.",
        "provs": [
            ["24", "주제 테마", "시작·평온·용기·행복 등 — 전부 무료."],
            ["32", "작가 컬렉션", "셰익스피어·니체·톨스토이·공자·울프 — Pro의 소장 서가."],
            ["952", "검증된 명언", "실제 저작에서, 5개 언어로, 라틴어·독일어·한문 원어까지."],
            ["56", "명화 배경", "모네·고흐·클림트·호쿠사이 — 테마마다 그림 한 점."],
        ],
        "shots_kicker": "화면", "shots_num": "IOS",
        "shots_h2": "한 타일씩 플레이하는 <em>작은 갤러리</em>.",
        "shots_caps": ["조용한 보드", "명화로 채운 56 테마", "숫자가 아니라 문장"],
        "feat_kicker": "디테일", "feat_num": "07",
        "feat_h2": "작은 게임, <em>분명한 선택</em>.",
        "feats": [
            ["가짜 명언 없음", "모든 문장을 출처와 대조했습니다. 인터넷 오귀속 문구는 일부러 뺐어요."],
            ["원어 표기", "왕관 명언을 원래의 언어로 — 라틴어·독일어·러시아어·한문."],
            ["내 테마 팩", "내 문장 11개(다짐·가훈·응원)로 나만의 팩을 만들어 플레이. 완성 카드에 내 이름이 새겨집니다."],
            ["모으는 명언 사다리", "테마마다 도달한 명언이 사다리로 쌓입니다 — 조용한 명언 도감."],
            ["오프라인·로그인 없음", "모든 콘텐츠 내장. 계정도 서버도 없습니다. 광고는 없습니다."],
            ["조용한 설계", "차분한 속도, 은은한 색, 클리어 후 “누가 한 말?” 퀴즈. 내 페이스로 즐기세요."],
            ["왕관 너머", "2048 너머 131072까지 이어가면, 신기록마다 새로운 명언이 공개됩니다."],
        ],
        "final_h2": "오늘 명언 하나를 키워 보세요.", "final_lede": "iPhone · iPad 무료.",
        "f_contact": "문의", "f_privacy": "개인정보 처리방침", "f_terms": "이용약관",
    },
    "ja": {
        "dir": "ja/", "lang": "ja", "font": '"Hiragino Sans"',
        "title": "名言2048 — ことばを合わせて名言を育てるパズル",
        "desc": "知っている2048、でも数字ではなくことばが育ちます。同じ名言タイルを合わせ、56テーマ・952の検証済み名言を、ことわざから頂点の名言まで育てましょう。背景はパブリックドメインの名画。",
        "og_title": "名言2048 — 静かなことばの2048",
        "og_desc": "同じ文を合わせると名言が育ちます。ことわざから頂点の名言まで。",
        "kicker_num": "テキストマージパズル",
        "h1": "知っている2048、でも数字ではなく<em>ことばが育つ。</em>",
        "sub": "同じ名言タイルを2つ合わせると、より大きな名言に。軽いことわざから始めて、2048の頂点の名言まで育てましょう。",
        "note": "無料 · iPhone &amp; iPad · アカウント不要",
        "badge_small": "ダウンロード", "badge_aria": "App Storeでダウンロード",
        "chips": [["S", "シェイクスピア"], ["N", "ニーチェ"], ["孔", "孔子"], ["夏", "漱石"]],
        "hero_alt": "名言2048のテーマ一覧 — テーマごとに名画が敷かれたグリッド",
        "marquee": ["シェイクスピア", "ニーチェ", "孔子", "トルストイ", "ヴァージニア・ウルフ", "老子", "ルーミー", "カフカ", "マルクス・アウレリウス", "夏目漱石"],
        "how_kicker": "遊び方",
        "how_h2": "合わせて。育てて。<em>名言を完成。</em>",
        "steps": [
            ["合成", "スワイプで合成", "同じ名言タイル2つが1つに — おなじみの2048ルールそのまま。"],
            ["成長", "育つことば", "合わせるたびに、ことばが一段上の名言へ格上げされます。"],
            ["完成", "頂点へ", "2048タイルを作ると、そのテーマの頂点の名言が完成し、集まります。"],
        ],
        "lad_kicker": "名言のはしご", "lad_num": "2 → 2048",
        "lad_h2": "ひとつのテーマ、<em>11の名言</em>が昇る。",
        "lad_lede": "どのテーマもはしご — 下には軽いことわざ、頂点には誰もが知る名言。これは「はじまり」テーマ。",
        "ladder": [
            ["2", "始めは半ばなり", "ことわざ"],
            ["8", "遅すぎることはない", "—"],
            ["128", "たたけよ、さらば開かれん", "聖書"],
            ["512", "光あれ", "創世記"],
            ["2048", "大木も小さな芽から育つ", "老子"],
        ],
        "cnt_kicker": "中身", "cnt_num": "56 · 952",
        "cnt_h2": "本物の名言。<em>本物の絵画。</em>",
        "cnt_lede": "捏造なし — すべての文は出典を照合し、すべての背景はパブリックドメインの名画です。",
        "provs": [
            ["24", "主題テーマ", "はじまり・平穏・勇気・幸福など — すべて無料。"],
            ["32", "作家コレクション", "シェイクスピア・ニーチェ・トルストイ・孔子・ウルフ — Proの書架。"],
            ["952", "検証済み名言", "実際の著作から、5言語で、ラテン語・ドイツ語・漢文の原文も。"],
            ["56", "名画の背景", "モネ・ゴッホ・クリムト・北斎 — テーマごとに一枚。"],
        ],
        "shots_kicker": "画面", "shots_num": "IOS",
        "shots_h2": "一タイルずつ遊ぶ<em>小さな美術館</em>。",
        "shots_caps": ["静かな盤面", "名画の56テーマ", "数字ではなく、ことば"],
        "feat_kicker": "細部", "feat_num": "07",
        "feat_h2": "小さなゲーム、<em>明確な選択</em>。",
        "feats": [
            ["偽の名言なし", "すべての文を出典と照合。ネット上の誤帰属はあえて外しました。"],
            ["原語表記", "頂点の名言を元の言語で — ラテン語・ドイツ語・ロシア語・漢文。"],
            ["マイテーマパック", "自分の言葉11個で自分だけのパックを作って遊べます。完成カードに名前が刻まれます。"],
            ["集める名言のはしご", "テーマごとに到達した名言がはしごに積まれる — 静かな名言図鑑。"],
            ["オフライン・ログイン不要", "すべて内蔵。アカウントもサーバーもなし。広告はありません。"],
            ["静かな設計", "穏やかなテンポ、柔らかな色、クリア後の“誰の言葉?”クイズ。自分のペースで。"],
            ["王冠を超えて", "2048を超えて131072まで — 新記録のたびに新しい名言が現れます。"],
        ],
        "final_h2": "今日、名言をひとつ育てよう。", "final_lede": "iPhone · iPad 無料。",
        "f_contact": "お問い合わせ", "f_privacy": "プライバシーポリシー", "f_terms": "利用規約",
    },
    "zh-hans": {
        "dir": "zh-hans/", "lang": "zh-Hans", "font": '"PingFang SC"',
        "title": "名言2048 — 合并方块，收集名人名言",
        "desc": "你熟悉的2048，只是数字换成会成长的句子。合并相同的名言方块，把56个主题·952句经核实的名言从谚语一路养到巅峰名言，背景是公共领域名画。",
        "og_title": "名言2048 — 安静的文字2048",
        "og_desc": "合并相同的句子，让智慧慢慢生长——从谚语到巅峰名言。",
        "kicker_num": "文字合并解谜",
        "h1": "你熟悉的2048，只是数字换成<em>会成长的句子。</em>",
        "sub": "合并两个相同的名言方块，文字就成长为更高的名言。从一句谚语开始，养到2048的巅峰名言。",
        "note": "免费 · iPhone &amp; iPad · 无需账号",
        "badge_small": "下载于", "badge_aria": "在 App Store 下载",
        "chips": [["S", "莎士比亚"], ["N", "尼采"], ["孔", "孔子"], ["夏", "漱石"]],
        "hero_alt": "名言2048主题一览 — 每个主题配一幅名画的网格",
        "marquee": ["莎士比亚", "尼采", "孔子", "托尔斯泰", "伍尔夫", "老子", "鲁米", "卡夫卡", "马可·奥勒留", "简·奥斯汀"],
        "how_kicker": "怎么玩",
        "how_h2": "合并。成长。<em>完成名言。</em>",
        "steps": [
            ["合并", "滑动合并", "两个相同的名言方块合成一个 — 还是你熟悉的2048规则。"],
            ["成长", "看它长大", "每次合并都把文字提升到更高一级的名言。"],
            ["完成", "抵达巅峰", "合出2048方块，完成该主题的巅峰名言并收藏。"],
        ],
        "lad_kicker": "名言阶梯", "lad_num": "2 → 2048",
        "lad_h2": "一个主题，<em>十一句名言</em>，拾级而上。",
        "lad_lede": "每个主题都是一架阶梯 — 底部是轻巧的谚语，顶端是人人皆知的名言。这是「开始」主题。",
        "ladder": [
            ["2", "好的开始是成功的一半", "谚语"],
            ["8", "永远都不算晚", "—"],
            ["128", "叩门，就给你们开门", "圣经"],
            ["512", "要有光", "创世记"],
            ["2048", "大树也从小芽长成", "老子"],
        ],
        "cnt_kicker": "内含", "cnt_num": "56 · 952",
        "cnt_h2": "真实的名言。<em>真实的画作。</em>",
        "cnt_lede": "绝不杜撰 — 每句都核对出处，每幅背景都是公共领域名画。",
        "provs": [
            ["24", "主题合集", "开始·平静·勇气·幸福等 — 全部免费。"],
            ["32", "作家合集", "莎士比亚·尼采·托尔斯泰·孔子·伍尔夫 — Pro 藏书架。"],
            ["952", "核实的名言", "取自原著，五种语言，附拉丁语·德语·文言文原文。"],
            ["56", "名画背景", "莫奈·梵高·克里姆特·葛饰北斋 — 每个主题一幅。"],
        ],
        "shots_kicker": "界面", "shots_num": "IOS",
        "shots_h2": "一格一格玩的<em>小美术馆</em>。",
        "shots_caps": ["安静的棋盘", "56幅名画主题", "不是数字，是句子"],
        "feat_kicker": "细节", "feat_num": "07",
        "feat_h2": "小游戏，<em>清晰的取舍</em>。",
        "feats": [
            ["拒绝伪名言", "每句都核对出处。网络上的误传一律排除。"],
            ["原文对照", "用原本的语言看巅峰名言 — 拉丁语·德语·俄语·文言文。"],
            ["我的主题包", "写下11句自己的话（座右铭·家训·祝福）做成专属主题包，完成卡刻着你的名字。"],
            ["可收集的名言阶梯", "每个主题都记录你抵达的名言 — 一部安静的名言图鉴。"],
            ["离线·无需登录", "内容全部内置，没有账号也没有服务器。没有任何广告。"],
            ["安静的设计", "从容的节奏、柔和的色彩、通关后的“这是谁说的?”小测验。"],
            ["超越王冠", "超过2048一路到131072 — 每破一次纪录，解锁一句新名言。"],
        ],
        "final_h2": "今天，养大一句名言。", "final_lede": "iPhone · iPad 免费。",
        "f_contact": "联系我们", "f_privacy": "隐私政策", "f_terms": "服务条款",
    },
    "zh-hant": {
        "dir": "zh-hant/", "lang": "zh-Hant", "font": '"PingFang TC"',
        "title": "名言2048 — 收集名句的療癒益智遊戲",
        "desc": "你熟悉的2048，只是數字換成會成長的句子。合併相同的名言方塊，把56個主題·952句經核實的名言從諺語一路養到巔峰名言，背景是公有領域名畫。",
        "og_title": "名言2048 — 安靜的文字2048",
        "og_desc": "合併相同的句子，讓智慧慢慢生長——從諺語到巔峰名言。",
        "kicker_num": "文字合併解謎",
        "h1": "你熟悉的2048，只是數字換成<em>會成長的句子。</em>",
        "sub": "合併兩個相同的名言方塊，文字就成長為更高的名言。從一句諺語開始，養到2048的巔峰名言。",
        "note": "免費 · iPhone &amp; iPad · 免註冊",
        "badge_small": "下載於", "badge_aria": "在 App Store 下載",
        "chips": [["S", "莎士比亞"], ["N", "尼采"], ["孔", "孔子"], ["夏", "漱石"]],
        "hero_alt": "名言2048主題一覽 — 每個主題配一幅名畫的網格",
        "marquee": ["莎士比亞", "尼采", "孔子", "托爾斯泰", "吳爾芙", "老子", "魯米", "卡夫卡", "馬可·奧理略", "珍·奧斯汀"],
        "how_kicker": "怎麼玩",
        "how_h2": "合併。成長。<em>完成名言。</em>",
        "steps": [
            ["合併", "滑動合併", "兩個相同的名言方塊合成一個 — 還是你熟悉的2048規則。"],
            ["成長", "看它長大", "每次合併都把文字提升到更高一級的名言。"],
            ["完成", "抵達巔峰", "合出2048方塊，完成該主題的巔峰名言並收藏。"],
        ],
        "lad_kicker": "名言階梯", "lad_num": "2 → 2048",
        "lad_h2": "一個主題，<em>十一句名言</em>，拾級而上。",
        "lad_lede": "每個主題都是一架階梯 — 底部是輕巧的諺語，頂端是人人皆知的名言。這是「開始」主題。",
        "ladder": [
            ["2", "好的開始是成功的一半", "諺語"],
            ["8", "永遠都不算晚", "—"],
            ["128", "叩門，就給你們開門", "聖經"],
            ["512", "要有光", "創世記"],
            ["2048", "大樹也從小芽長成", "老子"],
        ],
        "cnt_kicker": "內含", "cnt_num": "56 · 952",
        "cnt_h2": "真實的名言。<em>真實的畫作。</em>",
        "cnt_lede": "絕不杜撰 — 每句都核對出處，每幅背景都是公有領域名畫。",
        "provs": [
            ["24", "主題合集", "開始·平靜·勇氣·幸福等 — 全部免費。"],
            ["32", "作家合集", "莎士比亞·尼采·托爾斯泰·孔子·吳爾芙 — Pro 藏書架。"],
            ["952", "核實的名言", "取自原著，五種語言，附拉丁語·德語·文言文原文。"],
            ["56", "名畫背景", "莫內·梵谷·克林姆·葛飾北齋 — 每個主題一幅。"],
        ],
        "shots_kicker": "介面", "shots_num": "IOS",
        "shots_h2": "一格一格玩的<em>小美術館</em>。",
        "shots_caps": ["安靜的棋盤", "56幅名畫主題", "不是數字，是句子"],
        "feat_kicker": "細節", "feat_num": "07",
        "feat_h2": "小遊戲，<em>清晰的取捨</em>。",
        "feats": [
            ["拒絕偽名言", "每句都核對出處。網路上的誤傳一律排除。"],
            ["原文對照", "用原本的語言看巔峰名言 — 拉丁語·德語·俄語·文言文。"],
            ["我的主題包", "寫下11句自己的話（座右銘·家訓·祝福）做成專屬主題包，完成卡刻著你的名字。"],
            ["可收集的名言階梯", "每個主題都記錄你抵達的名言 — 一部安靜的名言圖鑑。"],
            ["離線·免登入", "內容全部內建，沒有帳號也沒有伺服器。沒有任何廣告。"],
            ["安靜的設計", "從容的節奏、柔和的色彩、通關後的“這是誰說的?”小測驗。"],
            ["超越王冠", "超過2048一路到131072 — 每破一次紀錄，解鎖一句新名言。"],
        ],
        "final_h2": "今天，養大一句名言。", "final_lede": "iPhone · iPad 免費。",
        "f_contact": "聯絡我們", "f_privacy": "隱私權政策", "f_terms": "服務條款",
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
    ladder = "".join(
        f'<div class="ladder-row{" crown" if tier=="2048" else ""}"><span class="tier">{tier}</span><span class="quote">{q}</span><span class="who">{w}</span></div>'
        for tier, q, w in loc["ladder"]
    )
    provs = "".join(
        f'<div class="prov"><span class="big">{big}</span><h3>{h}</h3><p>{p}</p></div>'
        for big, h, p in loc["provs"]
    )
    shot_files = ["board", "hero", "board2"]
    shots = "".join(
        f'<figure><div class="phone"><img src="{rel}assets/shot-{f}.png" alt="{cap}" loading="lazy"><div class="island"></div></div><figcaption>{cap}</figcaption></figure>'
        for f, cap in zip(shot_files, loc["shots_caps"])
    )
    feats = "".join(f'<div class="feat"><h3>{h}</h3><p>{p}</p></div>' for h, p in loc["feats"])
    ladder_json = json.dumps(loc["ladder"], ensure_ascii=False)

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
    <a class="wordmark" href="{rel if rel else './'}"><img src="{rel}assets/icon-180.png" alt=""><span>QUOTE·2048</span></a>
    <div class="lang">{lang_nav(loc['dir'], rel)}</div>
  </div>
</nav>

<header class="hero">
  <div class="ghost">&#8220;</div>
  <div class="wrap">
    <div>
      <div class="kicker"><span>QUOTE · 2048</span><span class="rule"></span><span class="num">{loc['kicker_num']}</span></div>
      <h1>{loc['h1']}</h1>
      <div class="demo">
        <div class="tile"><span class="badge" id="demoBadge">2</span><span class="q" id="demoQuote">{loc['ladder'][0][1]}</span></div>
        <div class="meta"><span class="step" id="demoStep">TIER 2 / 2048</span><span class="author" id="demoAuthor">— {loc['ladder'][0][2]}</span></div>
      </div>
      <p class="sub">{loc['sub']}</p>
      <div class="cta">
        {badge(loc, 'storeLink')}
        <span class="note">{loc['note']}</span>
      </div>
    </div>
    <div class="phone-col">
      {chips}
      <div class="phone"><img src="{rel}assets/shot-hero.png" alt="{loc['hero_alt']}"><div class="island"></div></div>
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
    <div class="kicker"><span>{loc['lad_kicker']}</span><span class="rule"></span><span class="num">{loc['lad_num']}</span></div>
    <h2>{loc['lad_h2']}</h2>
    <p class="lede">{loc['lad_lede']}</p>
    <div class="ladder">{ladder}</div>
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap">
    <div class="kicker"><span>{loc['cnt_kicker']}</span><span class="rule"></span><span class="num">{loc['cnt_num']}</span></div>
    <h2>{loc['cnt_h2']}</h2>
    <p class="lede">{loc['cnt_lede']}</p>
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
  // After App Store approval, set the real URL here (e.g. https://apps.apple.com/app/id1234567890)
  const APP_STORE_URL = "";
  if (APP_STORE_URL) {{
    document.getElementById("storeLink").href = APP_STORE_URL;
    document.getElementById("storeLink2").href = APP_STORE_URL;
  }}

  const ladder = {ladder_json};
  const bEl = document.getElementById("demoBadge");
  const qEl = document.getElementById("demoQuote");
  const sEl = document.getElementById("demoStep");
  const aEl = document.getElementById("demoAuthor");
  if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {{
    let i = 0;
    const sleep = (ms) => new Promise(r => setTimeout(r, ms));
    (async function loop() {{
      for (;;) {{
        const [tier, q, w] = ladder[i % ladder.length];
        qEl.style.opacity = 0;
        await sleep(360);
        bEl.textContent = tier;
        qEl.textContent = q;
        sEl.textContent = "TIER " + tier + " / 2048";
        aEl.textContent = "— " + w;
        qEl.style.opacity = 1;
        await sleep(2100);
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
