#!/usr/bin/env python3
"""Generate index.html for every locale from one template.

Usage: python3 build.py
Output: ./index.html (en), ./ko/index.html, ./ja/index.html
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).parent
BASE_URL = "https://www.kkirukstudio.com/sidefeed/"
APP_STORE_URL = "https://apps.apple.com/app/id6762836653"

APPLE_SVG = '<svg viewBox="0 0 384 512" aria-hidden="true"><path d="M318.7 268.7c-.2-36.7 16.4-64.4 50-84.8-18.8-26.9-47.2-41.7-84.7-44.6-35.5-2.8-74.3 20.7-88.5 20.7-15 0-49.4-19.7-76.4-19.7C63.3 141.2 4 184.8 4 273.5q0 39.3 14.4 81.2c12.8 36.7 59 126.7 107.2 125.2 25.2-.6 43-17.9 75.8-17.9 31.8 0 48.3 17.9 76.4 17.9 48.6-.7 90.4-82.5 102.6-119.3-65.2-30.7-61.7-90-61.7-91.9zm-56.6-164.2c27.3-32.4 24.8-61.9 24-72.5-24.1 1.4-52 16.4-67.9 34.9-17.5 19.8-27.8 44.3-25.6 71.9 26.1 2 49.9-11.4 69.5-34.3z"/></svg>'

LANG_LABELS = [("", "EN"), ("ko/", "한국어"), ("ja/", "日本語"), ("zh/", "繁體中文")]

LOCALES = {
    "en": {
        "dir": "", "lang": "en", "font": None, "shots": "en",
        "title": "Sidefeed — See what's trending on YouTube in 12 countries",
        "desc": "Trending (the official YouTube chart), Radar (Sidefeed's own breakout ranking) and Discover (top videos in 14 categories) — across 12 countries, with 6-hour rank changes. Trend research for creators planning their next video.",
        "og_title": "Sidefeed — YouTube Trends, Country by Country",
        "og_desc": "See which videos are rising right now, with 6-hour rank changes across 12 countries.",
        "kicker_num": "TREND RESEARCH",
        "h1": "What is everyone else<br><em>watching on YouTube?</em>",
        "demo_items": [
            ["🇺🇸", "GAMING", "#18", "#3", "▲15 · 6H", "up"],
            ["🇰🇷", "MUSIC", "#9", "#2", "▲7 · 6H", "up"],
            ["🇯🇵", "ENTERTAINMENT", "—", "#5", "NEW", "new"],
            ["🇬🇧", "SPORTS", "#21", "#6", "▲15 · 6H", "up"],
        ],
        "sub": "That question is where this app started. Open YouTube and the algorithm shows you videos picked just for you — so you never really know what everyone else is watching. Sidefeed answers with three rankings: Trending, the official chart for 12 countries; Radar, a ranking Sidefeed computes itself to catch risers before the official chart does; and Discover, the most popular videos in each of 14 categories. Stop guessing your next video — check the data, then make it.",
        "badge_small": "Download on the", "note": "FREE DOWNLOAD · IPHONE &amp; IPAD · NO GOOGLE LOGIN",
        "badge_aria": "Download on the App Store",
        "chips": [["", "🔥", "Official trending chart"], ["new", "📡", "Radar — our own ranking"], ["up", "🎵", "Top videos in 14 categories"], ["", "🌍", "12 countries"]],
        "hero_alt": "Sidefeed trending screen showing the US YouTube chart with rank-change badges and a category breakdown bar",
        "marquee": ["UNITED STATES", "JAPAN", "UNITED KINGDOM", "GERMANY", "AUSTRALIA", "CANADA", "FRANCE", "KOREA", "SWITZERLAND", "NETHERLANDS", "SWEDEN", "SINGAPORE"],
        "how_kicker": "HOW IT WORKS",
        "how_h2": "Here's how you use it — <em>three simple steps</em>.",
        "steps": [
            ["COUNTRY", "Pick a country to look at", "Tap the flag button and choose one of 12 countries — the US, Japan, Korea and more. You instantly see the videos people in that country are watching the most right now."],
            ["SIGNALS", "Spot the videos that are climbing", "Every video carries a ▲ (rising), ▼ (falling) or NEW (just entered) mark. Top Movers and the Radar tab gather the fastest climbers for you."],
            ["RESEARCH", "Save the ones worth remembering", "Tap a video and Sidefeed first shows how its rank has changed and how fast its views are growing. Save the useful ones to Watch Later — they sync through your own iCloud to both iPhone and iPad."],
        ],
        "rank_kicker": "RANK MOVEMENT", "rank_num": "EVERY 6 HOURS",
        "rank_h2": "\"Rising right now\" is something <em>YouTube itself never shows you</em>.",
        "rank_lede": "Anyone can see what's #1 today. The real signal is the video that was #18 six hours ago and is #3 now — that one is blowing up as you watch. Sidefeed saves the chart through the day and marks every video with exactly how its rank changed.",
        "rank_rows": [
            ["6h ago #18", "now #3", '🇺🇸 GAMING · <span class="d-up">▲15</span>'],
            ["6h ago #9", "now #2", '🇰🇷 MUSIC · <span class="d-up">▲7</span>'],
            ["6h ago —", "now #5", '🇯🇵 ENTERTAINMENT · <span class="d-new">NEW</span>'],
            ["6h ago #4", "now #11", '🇬🇧 SPORTS · <span class="d-down">▼7</span>'],
        ],
        "rank_nums": [[18, 3], [9, 2], [None, 5], [4, 11]],
        "views_kicker": "THE TOOLKIT", "views_num": "3 RANKINGS + 12 COUNTRIES",
        "views_h2": "Three rankings — <em>Trending, Radar, Discover</em>.",
        "views_lede": "The official chart alone isn't enough. Radar — computed by Sidefeed itself — catches videos rising outside the chart, and Discover shows what's most popular in every one of 14 categories. All of it public data, so everyone sees the same screens: the actual trends, not an algorithm's guess.",
        "views": [
            ["🔥", "Trending", "The official YouTube popularity chart. Sidefeed adds 6-hour rank-change marks, a Top Movers row, and a bar showing which categories dominate right now."],
            ["📡", "Radar", "Sidefeed's own ranking. It catches videos that are rising fast but haven't reached the official chart yet."],
            ["✨", "Discover", "Popular videos sorted into 14 categories — music, gaming, comedy and more. No personalization, just what's actually popular."],
            ["🌍", "12 Countries", "Switch countries with one tap on the flag and compare. What's #1 in Tokyo right now?"],
        ],
        "who_kicker": "WHO IT'S FOR", "who_num": "CREATORS · PLANNERS · MARKETERS",
        "who_h2": "For people whose <em>job</em> is knowing what's trending.",
        "who_lede": "In July 2025, YouTube removed the Trending page from its own app. Inside YouTube, it's now even harder to see past your personal recommendations. But if you make a living from video, \"what's rising right now\" is still a number you need every single day. Sidefeed is where that number lives now.",
        "personas": [
            ["YOUTUBE CREATORS", "If running out of ideas scares you",
             "“Everyone says 'ride the trend' when your channel stalls. Okay — where exactly do I see the trend?”",
             "Your recommendations only show videos like the ones you already make. Skim Trending and Radar for one minute each morning, and you'll catch topics while the ▲ marks are still fresh — before everyone else starts copying them."],
            ["CONTENT PLANNERS · PRODUCERS", "If the pitch meeting comes every week",
             "“What do I bring on Monday? Every. Single. Week.”",
             "Flip through 12 country charts. If a format is climbing with ▲ in the US but hasn't reached your market's chart yet, that's your next pitch. Five minutes before the meeting is enough."],
            ["MARKETERS · MCNs", "If campaign timing is money",
             "“I want one screen that shows what's working in this category right now.”",
             "Check the top videos in any of 14 categories on Discover, and spot channels just taking off on Radar. The best time to propose a collab is before they hit the chart."],
        ],
        "shots_kicker": "SCREENS", "shots_num": "IOS 17+",
        "shots_h2": "Here's what it <em>actually looks like</em>.",
        "shots_caps": ["RADAR · BREAKOUT RANKING", "12-COUNTRY SWITCHER", "DISCOVER · 14 CATEGORIES"],
        "feat_kicker": "DETAILS", "feat_num": "06",
        "feat_h2": "The details that <em>make it different</em>.",
        "feats": [
            ["No login, no personalization", "You never sign in with Google, and your watch history is never used. That's the point: you see the same real ranking as everyone else, not a feed shaped around you."],
            ["6-hour snapshots", "Sidefeed's server saves the trending chart all day long. By comparing those saved copies, it can tell whether each video's rank went up or down — something the YouTube app itself never shows you."],
            ["Insight card first", "Tapping a video doesn't throw you onto YouTube. You first see a small card with its current rank, 6-hour change and view speed — then you decide whether to open it on YouTube."],
            ["Shorts filter", "Only researching long videos? Flip one switch in Settings and Shorts disappear from every screen."],
            ["Watch Later + iCloud", "Save a video for reference and it shows up on your iPhone and iPad alike, synced through your own iCloud."],
            ["Feed cleanup", "Block channels you don't want and dismiss videos you don't care about, so your research screen stays clean."],
        ],
        "final_h2": "Stop guessing your next video. Check the data first.", "final_lede": "Free to download on iPhone &amp; iPad.",
        "f_contact": "Contact", "f_privacy": "Privacy", "f_terms": "Terms",
    },
    "ko": {
        "dir": "ko/", "lang": "ko", "font": '"Apple SD Gothic Neo", "Pretendard"', "shots": "ko",
        "title": "Sidefeed — 지금 유튜브에서 뜨는 영상을 나라별로 보는 앱",
        "desc": "유튜브 공식 인기 차트 '트렌딩', 직접 계산한 급상승 순위 '레이더', 14개 분야별 인기 영상 '발견' — 12개 나라의 유튜브 트렌드를 한 앱에서 봅니다. 다음 영상을 기획하는 크리에이터를 위한 트렌드 리서치 앱.",
        "og_title": "Sidefeed — 유튜브 트렌드를 나라별로",
        "og_desc": "지금 어떤 영상이 뜨고 있는지, 12개 나라의 6시간 순위 변화로 보여드려요.",
        "kicker_num": "트렌드 리서치",
        "h1": "다른 사람들은 유튜브에서<br><em>뭘 보고 있을까?</em>",
        "demo_items": [
            ["🇰🇷", "음악", "#9", "#2", "▲7 · 6시간", "up"],
            ["🇺🇸", "게임", "#18", "#3", "▲15 · 6시간", "up"],
            ["🇯🇵", "엔터", "—", "#5", "NEW", "new"],
            ["🇬🇧", "스포츠", "#21", "#6", "▲15 · 6시간", "up"],
        ],
        "sub": "그 궁금증에서 시작한 앱입니다. 유튜브를 열면 알고리즘이 '나에게 맞춘' 영상만 보여줘서, 정작 다른 사람들이 뭘 보는지는 알 수 없으니까요. Sidefeed는 세 가지 순위로 답합니다. 12개 나라의 공식 인기 차트 '트렌딩', 직접 계산해 공식 차트에 없는 급상승까지 잡아내는 '레이더', 음악·게임 같은 14개 분야의 인기 영상을 모은 '발견'. 다음 영상, 감으로 찍지 말고 데이터로 확인하고 만드세요.",
        "badge_small": "다운로드는", "note": "무료 다운로드 · iPhone &amp; iPad · 구글 로그인 없음",
        "badge_aria": "App Store에서 다운로드",
        "chips": [["", "🔥", "공식 트렌딩 차트"], ["new", "📡", "직접 계산한 레이더 순위"], ["up", "🎵", "14개 분야별 인기 영상"], ["", "🌍", "12개 나라"]],
        "hero_alt": "Sidefeed 트렌딩 화면 — 순위 변화 뱃지와 카테고리 분포 바가 있는 한국 YouTube 차트",
        "marquee": ["미국", "일본", "영국", "독일", "호주", "캐나다", "프랑스", "한국", "스위스", "네덜란드", "스웨덴", "싱가포르"],
        "how_kicker": "사용 방법",
        "how_h2": "사용법은 <em>세 단계</em>가 전부입니다.",
        "steps": [
            ["국가", "어느 나라를 볼지 고르세요", "국기 버튼을 누르면 미국·일본·한국 같은 12개 나라 중 하나를 고를 수 있어요. 그 나라 사람들이 지금 가장 많이 보는 유튜브 영상이 바로 뜹니다."],
            ["시그널", "올라오는 영상을 찾아내세요", "모든 영상 옆에 ▲(상승)·▼(하락)·NEW(새 진입) 표시가 붙어요. 빠르게 치고 올라오는 영상은 Top Movers와 레이더 탭이 따로 모아서 보여줍니다."],
            ["리서치", "쓸 만한 영상은 저장해 두세요", "영상을 누르면 순위가 어떻게 변해왔는지, 조회수가 얼마나 빨리 늘고 있는지를 먼저 보여줘요. 참고할 영상은 '나중에 보기'에 저장하면 iCloud를 통해 아이폰·아이패드 어디서든 다시 볼 수 있습니다."],
        ],
        "rank_kicker": "순위 변동", "rank_num": "6시간마다",
        "rank_h2": "'지금 막 뜨는 중'은 <em>유튜브 어디에도 안 나옵니다</em>.",
        "rank_lede": "오늘 1위가 무엇인지는 누구나 볼 수 있어요. 진짜 신호는 '6시간 전에 18위였는데 지금 3위'인 영상입니다. 바로 지금 뜨고 있다는 뜻이니까요. Sidefeed는 하루 종일 차트를 저장해 두고, 모든 영상의 순위가 정확히 어떻게 변했는지 표시해 줍니다.",
        "rank_rows": [
            ["6시간 전 #18", "지금 #3", '🇺🇸 게임 · <span class="d-up">▲15</span>'],
            ["6시간 전 #9", "지금 #2", '🇰🇷 음악 · <span class="d-up">▲7</span>'],
            ["6시간 전 —", "지금 #5", '🇯🇵 엔터 · <span class="d-new">NEW</span>'],
            ["6시간 전 #4", "지금 #11", '🇬🇧 스포츠 · <span class="d-down">▼7</span>'],
        ],
        "rank_nums": [[18, 3], [9, 2], [None, 5], [4, 11]],
        "views_kicker": "구성", "views_num": "3개의 순위 + 12개 나라",
        "views_h2": "순위가 <em>세 종류</em>입니다 — 트렌딩, 레이더, 발견.",
        "views_lede": "유튜브 공식 차트만으로는 부족해요. Sidefeed가 직접 계산한 '레이더'가 공식 차트 밖에서 올라오는 영상을 잡아내고, '발견'이 14개 분야별 인기 영상을 보여줍니다. 전부 공개 데이터 기반이라 누가 보든 똑같은 화면 — 알고리즘 추천에 가려진 진짜 트렌드입니다.",
        "views": [
            ["🔥", "트렌딩", "유튜브 공식 인기 차트입니다. 여기에 6시간 순위 변화 표시, 급상승 모음(Top Movers), 분야별 비율 막대를 더했어요."],
            ["📡", "레이더", "Sidefeed가 직접 계산한 순위예요. 아직 공식 차트에 들어오지 못했지만 빠르게 올라오는 영상을 먼저 잡아냅니다."],
            ["✨", "발견", "음악·게임·코미디처럼 14개 분야별로 인기 영상을 모아 보여줘요. 내 취향과 상관없이, 지금 실제로 인기 있는 영상 그대로요."],
            ["🌍", "12개국", "국기 버튼 한 번으로 나라를 바꿔가며 비교할 수 있어요. 지금 도쿄의 1위는 무슨 영상일까요?"],
        ],
        "who_kicker": "누가 쓰나", "who_num": "크리에이터 · 기획자 · 마케터",
        "who_h2": "트렌드 보는 게 <em>일</em>인 사람들에게.",
        "who_lede": "유튜브는 2025년 7월, 앱에서 '인기 급상승' 페이지를 없앴습니다. 이제 유튜브 안에서는 내 추천 피드 바깥을 보기가 더 어려워졌죠. 하지만 영상으로 먹고사는 사람에게 '지금 무엇이 뜨는가'는 여전히 매일 확인해야 하는 숫자입니다. 그 숫자가 이제 Sidefeed에 있습니다.",
        "personas": [
            ["유튜브 크리에이터", "소재 고갈이 무섭다면",
             "“채널이 멈추면 다들 '트렌드를 타라'고 해요. 그래서 그 트렌드, 어디서 보나요?”",
             "추천 피드는 내가 이미 만든 것과 비슷한 영상만 보여줍니다. 아침마다 1분씩 트렌딩과 레이더를 훑으세요. ▲ 표시가 막 붙기 시작한 소재를, 남들이 따라 만들기 전에 잡을 수 있습니다."],
            ["콘텐츠 기획자 · PD", "기획 회의가 매주 돌아온다면",
             "“월요일에 뭘 가져가지? 매주, 매번요.”",
             "12개 나라 차트를 넘겨 보세요. 미국에서 ▲를 달고 올라오는 포맷이 아직 한국 차트에 없다면, 그게 다음 기획안입니다. 회의 전 5분이면 충분해요."],
            ["마케터 · MCN", "캠페인 타이밍이 곧 돈이라면",
             "“이 분야에서 요즘 뭐가 먹히는지, 한 화면으로 보고 싶어요.”",
             "발견 탭에서 14개 분야별 인기 영상을 확인하고, 레이더에서 막 올라오기 시작한 채널을 먼저 찾으세요. 협업 제안은 차트에 오르기 전이 가장 쌉니다."],
        ],
        "shots_kicker": "화면", "shots_num": "IOS 17+",
        "shots_h2": "실제 화면은 <em>이렇게 생겼어요</em>.",
        "shots_caps": ["레이더 · 급상승 랭킹", "12개국 전환", "발견 · 14 카테고리"],
        "feat_kicker": "디테일", "feat_num": "06",
        "feat_h2": "이런 점이 <em>다릅니다</em>.",
        "feats": [
            ["로그인·개인화 없음", "구글 계정으로 로그인하지 않고, 내 시청기록도 쓰지 않아요. 그래서 알고리즘이 골라준 피드가 아니라, 모두에게 똑같은 '진짜 인기 순위'를 보게 됩니다."],
            ["6시간 스냅샷", "Sidefeed 서버가 하루 종일 인기 차트를 저장해 둡니다. 저장본끼리 비교해서 각 영상의 순위가 올랐는지 내렸는지 계산해요. 유튜브 앱에서는 볼 수 없는 정보입니다."],
            ["인사이트 카드가 먼저", "영상을 눌러도 바로 유튜브로 넘어가지 않아요. 현재 순위·6시간 변화·조회수 속도를 작은 카드로 먼저 보여주고, '유튜브에서 보기'는 그다음입니다."],
            ["쇼츠 필터", "긴 영상만 보고 싶다면 설정에서 스위치 하나만 켜세요. 모든 화면에서 쇼츠가 사라집니다."],
            ["나중에 보기 + iCloud", "참고할 영상을 저장하면 내 iCloud를 통해 아이폰과 아이패드 어디서나 똑같이 보입니다."],
            ["피드 정리", "보기 싫은 채널은 차단하고, 관심 없는 영상은 치울 수 있어요. 리서치 화면이 깔끔하게 유지됩니다."],
        ],
        "final_h2": "다음 영상, 감으로 찍지 말고 데이터로 확인하고 만드세요.", "final_lede": "아이폰·아이패드에서 무료로 받을 수 있어요.",
        "f_contact": "문의", "f_privacy": "개인정보 처리방침", "f_terms": "이용약관",
    },
    "ja": {
        "dir": "ja/", "lang": "ja", "font": '"Hiragino Kaku Gothic ProN", "Hiragino Sans", "Yu Gothic"', "shots": "ja",
        "title": "Sidefeed — YouTubeでいま伸びている動画を国ごとに見られるアプリ",
        "desc": "公式人気チャート「トレンド」、独自計算の急上昇ランキング「レーダー」、14ジャンル別の人気動画「発見」— 12ヶ国のYouTubeトレンドをひとつのアプリで。次の動画を企画するクリエイターのためのトレンドリサーチアプリ。",
        "og_title": "Sidefeed — YouTubeトレンドを国ごとに",
        "og_desc": "いまどの動画が伸びているのか、12ヶ国の6時間順位変動で見えます。",
        "kicker_num": "トレンドリサーチ",
        "h1": "ほかの人はYouTubeで<br><em>何を見ているんだろう？</em>",
        "demo_items": [
            ["🇯🇵", "エンタメ", "#24", "#6", "▲18 · 6時間", "up"],
            ["🇺🇸", "ゲーム", "#18", "#3", "▲15 · 6時間", "up"],
            ["🇰🇷", "音楽", "—", "#5", "NEW", "new"],
            ["🇬🇧", "スポーツ", "#21", "#6", "▲15 · 6時間", "up"],
        ],
        "sub": "その疑問から生まれたアプリです。YouTubeを開くと、アルゴリズムが「あなた向け」の動画ばかり見せてくるので、ほかの人が何を見ているかは案外分かりません。Sidefeedは3つのランキングで答えます。12ヶ国の公式人気チャート「トレンド」、公式チャートに入る前の急上昇を独自に計算して捉える「レーダー」、音楽・ゲームなど14ジャンルの人気動画を集めた「発見」。次の動画は、勘ではなくデータを確かめてから作りましょう。",
        "badge_small": "ダウンロードは", "note": "無料ダウンロード · iPhone &amp; iPad · Googleログイン不要",
        "badge_aria": "App Store でダウンロード",
        "chips": [["", "🔥", "公式トレンドチャート"], ["new", "📡", "独自計算のレーダー順位"], ["up", "🎵", "14ジャンル別人気動画"], ["", "🌍", "12ヶ国"]],
        "hero_alt": "Sidefeedのトレンド画面 — 順位変動バッジとカテゴリ分布バー付きの日本のYouTubeチャート",
        "marquee": ["アメリカ", "日本", "イギリス", "ドイツ", "オーストラリア", "カナダ", "フランス", "韓国", "スイス", "オランダ", "スウェーデン", "シンガポール"],
        "how_kicker": "使い方",
        "how_h2": "使い方は<em>3ステップ</em>だけ。",
        "steps": [
            ["国", "どの国を見るか選ぶ", "国旗ボタンを押すと、アメリカ・日本・韓国など12ヶ国から選べます。その国の人たちがいま一番見ているYouTube動画がすぐに表示されます。"],
            ["シグナル", "伸びている動画を見つける", "すべての動画に▲（上昇）・▼（下降）・NEW（初登場）のマークが付きます。勢いよく上がってくる動画はTop Moversとレーダータブがまとめて見せてくれます。"],
            ["リサーチ", "気になる動画は保存しておく", "動画をタップすると、順位がどう変わってきたか、再生数がどれだけ速く伸びているかを先に見せてくれます。参考になる動画は「後で見る」に保存すれば、iCloud経由でiPhoneでもiPadでも見られます。"],
        ],
        "rank_kicker": "順位変動", "rank_num": "6時間ごと",
        "rank_h2": "「いままさに伸びている」は、<em>YouTube本体では見られません</em>。",
        "rank_lede": "今日の1位は誰でも見られます。本当のシグナルは「6時間前は18位だったのに、いま3位」という動画。まさにいま伸びている、という意味だからです。Sidefeedは一日中チャートを保存しておき、すべての動画の順位がどう変わったかを正確に表示します。",
        "rank_rows": [
            ["6時間前 #18", "いま #3", '🇺🇸 ゲーム · <span class="d-up">▲15</span>'],
            ["6時間前 #24", "いま #6", '🇯🇵 エンタメ · <span class="d-up">▲18</span>'],
            ["6時間前 —", "いま #5", '🇰🇷 音楽 · <span class="d-new">NEW</span>'],
            ["6時間前 #4", "いま #11", '🇬🇧 スポーツ · <span class="d-down">▼7</span>'],
        ],
        "rank_nums": [[18, 3], [24, 6], [None, 5], [4, 11]],
        "views_kicker": "構成", "views_num": "3つのランキング + 12ヶ国",
        "views_h2": "ランキングは<em>3種類</em> — トレンド、レーダー、発見。",
        "views_lede": "公式チャートだけでは足りません。Sidefeedが独自に計算する「レーダー」がチャート圏外から伸びてくる動画を捉え、「発見」が14ジャンルごとの人気動画を見せてくれます。すべて公開データなので、誰が見ても同じ画面 — アルゴリズムのおすすめに隠れた本当のトレンドです。",
        "views": [
            ["🔥", "トレンド", "YouTube公式の人気チャートです。ここに6時間の順位変動マーク、急上昇まとめ（Top Movers）、ジャンル別の割合バーを足しました。"],
            ["📡", "レーダー", "Sidefeedが独自に計算したランキング。まだ公式チャートに入っていないけれど、勢いよく伸びている動画を先に捉えます。"],
            ["✨", "発見", "音楽・ゲーム・お笑いなど14ジャンルごとに人気動画をまとめて表示。あなたの好みとは関係なく、いま本当に人気のある動画そのままです。"],
            ["🌍", "12ヶ国", "国旗ボタンひとつで国を切り替えて比較できます。いまソウルの1位はどんな動画でしょう？"],
        ],
        "who_kicker": "誰のため", "who_num": "クリエイター · 企画 · マーケター",
        "who_h2": "トレンドを見るのが<em>仕事</em>の人へ。",
        "who_lede": "YouTubeは2025年7月、アプリから「急上昇」ページをなくしました。YouTubeの中では、自分へのおすすめの外側を見るのがますます難しくなっています。それでも、動画で食べている人にとって「いま何が伸びているか」は毎日確認すべき数字のまま。その数字の置き場所が、いまはSidefeedです。",
        "personas": [
            ["YouTubeクリエイター", "ネタ切れが怖いなら",
             "「チャンネルが止まると、みんな『トレンドに乗れ』と言う。じゃあそのトレンド、どこで見るの？」",
             "おすすめは、自分がすでに作ったものと似た動画ばかり見せてきます。毎朝1分、トレンドとレーダーを眺めてください。▲マークが付き始めたばかりのネタを、みんなが真似する前に掴めます。"],
            ["コンテンツ企画 · PD", "企画会議が毎週あるなら",
             "「月曜に何を持っていこう。毎週、毎回。」",
             "12ヶ国のチャートをめくってみてください。アメリカで▲を付けて伸びているフォーマットが、まだ日本のチャートになければ、それが次の企画書です。会議前の5分で足ります。"],
            ["マーケター · MCN", "キャンペーンのタイミングがお金なら",
             "「このジャンルでいま何がウケているか、一画面で見たい。」",
             "「発見」で14ジャンル別の人気動画を確認し、「レーダー」で伸び始めたばかりのチャンネルを先に見つけてください。コラボの提案は、チャートに載る前が一番安い。"],
        ],
        "shots_kicker": "画面", "shots_num": "IOS 17+",
        "shots_h2": "実際の画面は<em>こんな感じです</em>。",
        "shots_caps": ["レーダー · 急上昇ランキング", "12ヶ国スイッチャー", "発見 · 14カテゴリ"],
        "feat_kicker": "こだわり", "feat_num": "06",
        "feat_h2": "ここが<em>違います</em>。",
        "feats": [
            ["ログイン・パーソナライズなし", "Googleアカウントでのログインは不要で、視聴履歴も使いません。だからアルゴリズムが選んだフィードではなく、誰にとっても同じ「本当の人気順位」が見られます。"],
            ["6時間スナップショット", "Sidefeedのサーバーが一日中、人気チャートを保存しています。保存したもの同士を比べて、各動画の順位が上がったか下がったかを計算します。YouTubeアプリでは見られない情報です。"],
            ["インサイトカードが先", "動画をタップしてもすぐYouTubeには飛びません。現在順位・6時間の変動・再生ペースを小さなカードで先に見せて、「YouTubeで見る」はその後です。"],
            ["ショートフィルター", "長い動画だけ見たいときは、設定でスイッチをひとつ入れるだけ。すべての画面からショート動画が消えます。"],
            ["後で見る + iCloud", "参考にしたい動画を保存すれば、自分のiCloud経由でiPhoneでもiPadでも同じように見られます。"],
            ["フィード整理", "見たくないチャンネルはブロック、興味のない動画は非表示にできます。リサーチ画面がすっきり保てます。"],
        ],
        "final_h2": "次の動画は、勘ではなくデータを確かめてから。", "final_lede": "iPhone・iPadで無料でダウンロードできます。",
        "f_contact": "お問い合わせ", "f_privacy": "プライバシーポリシー", "f_terms": "利用規約",
    },
    "zh": {
        "dir": "zh/", "lang": "zh-Hant", "font": '"PingFang TC", "Heiti TC", "Microsoft JhengHei"', "shots": "en",
        "title": "Sidefeed — 用國家排行榜看 YouTube 現在在紅什麼",
        "desc": "YouTube官方發燒榜「趨勢」、自家演算的急升榜「雷達」、14個分類的熱門影片「探索」——涵蓋14個國家的YouTube趨勢，一個App全部看到。給正在企劃下一支影片的創作者的趨勢研究工具。",
        "og_title": "Sidefeed — 用國家別看 YouTube 趨勢",
        "og_desc": "現在哪支影片正在往上衝，14個國家的6小時排名變化一次看清楚。",
        "kicker_num": "趨勢研究",
        "h1": "大家在 YouTube 上<br><em>都在看什麼？</em>",
        "demo_items": [
            ["🇹🇼", "遊戲", "#18", "#3", "▲15 · 6小時", "up"],
            ["🇭🇰", "音樂", "#9", "#2", "▲7 · 6小時", "up"],
            ["🇯🇵", "娛樂", "—", "#5", "NEW", "new"],
            ["🇬🇧", "體育", "#21", "#6", "▲15 · 6小時", "up"],
        ],
        "sub": "這個疑問，就是這個App的起點。打開YouTube，演算法只會推薦「為你量身打造」的影片，讓你根本不知道別人到底在看什麼。Sidefeed用三種排行榜回答這個問題：14個國家的官方發燒榜「趨勢」；Sidefeed自行演算、能在官方榜之前就抓到急升影片的「雷達」；以及涵蓋14個分類熱門影片的「探索」。下一支影片別再憑感覺猜，先看數據再動手拍。",
        "badge_small": "立即下載", "note": "免費下載 · iPhone &amp; iPad · 不需 Google 登入",
        "badge_aria": "在 App Store 下載",
        "chips": [["", "🔥", "官方發燒榜"], ["new", "📡", "自家演算的雷達榜"], ["up", "🎵", "14個分類熱門影片"], ["", "🌍", "14個國家"]],
        "hero_alt": "Sidefeed趨勢畫面——顯示排名變化徽章與分類佔比長條的YouTube發燒榜",
        "marquee": ["台灣", "香港", "美國", "日本", "英國", "德國", "澳洲", "加拿大", "法國", "韓國", "瑞士", "荷蘭", "瑞典", "新加坡"],
        "how_kicker": "使用方法",
        "how_h2": "只要<em>三個步驟</em>就能上手。",
        "steps": [
            ["國家", "先選一個想看的國家", "點一下國旗按鈕，就能從台灣、香港、美國、日本等14個國家中挑選。馬上就能看到該國觀眾現在最愛看的YouTube影片。"],
            ["訊號", "找出正在往上衝的影片", "每支影片旁都會標示▲（上升）、▼（下降）或NEW（新進榜）。上升最快的影片，會由Top Movers和雷達分頁幫你彙整。"],
            ["研究", "把值得參考的影片先存起來", "點一支影片，Sidefeed會先告訴你它的排名怎麼變化、觀看數成長多快。值得參考的就存進「稍後觀看」，透過你自己的iCloud，iPhone和iPad都能同步看到。"],
        ],
        "rank_kicker": "排名變動", "rank_num": "每6小時更新",
        "rank_h2": "「現在正在爆紅」，這件事<em>YouTube本身從不告訴你</em>。",
        "rank_lede": "誰都能看到今天的第1名是誰。真正有價值的訊號，是那支「6小時前還是第18名，現在衝到第3名」的影片——那才是正在爆紅的證據。Sidefeed整天保存榜單快照，精確標示每支影片的排名怎麼變化。",
        "rank_rows": [
            ["6小時前 #18", "現在 #3", '🇹🇼 遊戲 · <span class="d-up">▲15</span>'],
            ["6小時前 #9", "現在 #2", '🇭🇰 音樂 · <span class="d-up">▲7</span>'],
            ["6小時前 —", "現在 #5", '🇯🇵 娛樂 · <span class="d-new">NEW</span>'],
            ["6小時前 #4", "現在 #11", '🇬🇧 體育 · <span class="d-down">▼7</span>'],
        ],
        "rank_nums": [[18, 3], [9, 2], [None, 5], [4, 11]],
        "views_kicker": "功能組成", "views_num": "3種排行榜 + 14個國家",
        "views_h2": "三種排行榜——<em>趨勢、雷達、探索</em>。",
        "views_lede": "光靠官方榜單還不夠。Sidefeed自行演算的「雷達」能抓到還沒上官方榜就已經在急升的影片，「探索」則彙整14個分類中最熱門的影片。全部都是公開數據，不管誰打開看到的都一樣——是真正的趨勢，不是演算法猜你喜歡什麼。",
        "views": [
            ["🔥", "趨勢", "YouTube官方的發燒榜。Sidefeed加上6小時排名變化標記、Top Movers急升彙整，以及顯示目前哪個分類最強勢的長條圖。"],
            ["📡", "雷達", "Sidefeed自行演算的排行榜，能抓到還沒衝進官方榜、但正在快速上升的影片。"],
            ["✨", "探索", "把音樂、遊戲、喜劇等14個分類的熱門影片整理出來，不做個人化推薦，就是現在真正紅的影片。"],
            ["🌍", "14個國家", "點一下國旗就能切換國家、互相比較。現在東京第1名是哪支影片？"],
        ],
        "who_kicker": "適合誰用", "who_num": "創作者 · 企劃 · 行銷",
        "who_h2": "獻給把<em>看趨勢</em>當工作的人。",
        "who_lede": "2025年7月，YouTube從自家App中拿掉了發燒影片頁面。在YouTube裡，現在要看到個人推薦以外的內容變得更難了。但對靠影片吃飯的人來說，「現在什麼正在紅」仍然是每天都得確認的數字。這個數字，現在就在Sidefeed。",
        "personas": [
            ["YouTube創作者", "如果最怕靈感枯竭",
             "「頻道一停更，大家就說『去追熱門』。好，但熱門到底要去哪裡看？」",
             "你的推薦頁只會顯示跟你之前做的影片類似的內容。每天早上花1分鐘掃一下趨勢和雷達，就能在▲標記剛出現時抓住題材——搶在大家開始跟風之前。"],
            ["內容企劃 ·製作人", "如果每週都要開企劃會議",
             "「星期一要提什麼？每一週，每一次。」",
             "翻一下14個國家的榜單。如果某個形式已經在美國掛著▲上升，但還沒進到你市場的榜單，那就是你的下一個企劃案。開會前5分鐘就夠了。"],
            ["行銷 · MCN", "如果活動時機就是錢",
             "「我想要一個畫面就看到這個分類現在什麼最紅。」",
             "在探索查看14個分類的熱門影片，再到雷達找剛開始起飛的頻道。提出合作提案的最佳時機，就是在他們衝上榜單之前。"],
        ],
        "shots_kicker": "畫面", "shots_num": "IOS 17+",
        "shots_h2": "實際畫面<em>長這樣</em>。",
        "shots_caps": ["雷達 · 急升排行榜", "14國切換器", "探索 · 14個分類"],
        "feat_kicker": "細節設計", "feat_num": "06",
        "feat_h2": "這些地方<em>不一樣</em>。",
        "feats": [
            ["不需登入、不做個人化", "不用Google帳號登入，也不會用到你的觀看紀錄。所以你看到的是每個人都一樣的「真實熱門排行」，不是演算法幫你挑好的內容。"],
            ["每6小時的快照", "Sidefeed的伺服器整天都在保存發燒榜。透過比對這些存檔，就能算出每支影片的排名是上升還是下降——這是YouTube App本身完全不會顯示的資訊。"],
            ["先看洞察卡片", "點一支影片不會馬上跳到YouTube。會先用一張小卡片顯示目前排名、6小時內的變化和觀看數成長速度，然後你再決定要不要打開YouTube看。"],
            ["Shorts過濾", "只想研究長影片？在設定裡開一個開關，所有畫面裡的Shorts就會消失。"],
            ["稍後觀看 + iCloud", "把值得參考的影片存起來，透過你自己的iCloud，iPhone和iPad都會同步顯示。"],
            ["整理你的內容牆", "封鎖不想看的頻道、隱藏沒興趣的影片，讓研究畫面保持乾淨清爽。"],
        ],
        "final_h2": "下一支影片，先看數據再動手拍。", "final_lede": "iPhone、iPad免費下載。",
        "f_contact": "聯絡我們", "f_privacy": "隱私權政策", "f_terms": "使用條款",
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
    return (f'<a class="store-badge" id="{el_id}" href="{APP_STORE_URL}" aria-label="{loc["badge_aria"]}">{APPLE_SVG}'
            f'<span class="txt"><small>{loc["badge_small"]}</small><strong>App Store</strong></span></a>')


SPARK_SVG = """<svg viewBox="0 0 100 40" preserveAspectRatio="none" aria-hidden="true">
<defs><linearGradient id="sg" x1="0" y1="0" x2="1" y2="0">
<stop offset="0" stop-color="#f97316"/><stop offset="1" stop-color="#7c3aed"/>
</linearGradient></defs>
<polyline points="0,34 18,30 36,31 54,22 72,18 100,6" fill="none" stroke="url(#sg)" stroke-width="2.5" stroke-linecap="round"/>
<circle cx="100" cy="6" r="3.2" fill="#c4b5fd"/>
</svg>"""


def mover_label(item):
    """'#18→#3 ▲15'-style compact label for the live board."""
    _, _, frm, to, delta, kind = item
    return f'{to} {delta.split(" ·")[0]}', kind


def board_rows(items):
    out = []
    for item in items[:3]:
        flag, cat = item[0], item[1]
        mv, kind = mover_label(item)
        out.append(f'<div class="brow"><span class="bflag">{flag}</span>'
                   f'<span class="bcat">{cat}</span><span class="bmv {kind}">{mv}</span></div>')
    return "".join(out)


def ticker_track(loc):
    parts = []
    countries = list(loc["marquee"])
    for i, item in enumerate(loc["demo_items"]):
        flag, cat, frm, to, delta, kind = item
        parts.append(f'<span class="t-cty">{countries[i]}</span>')
        parts.append(f'<span class="t-item">{flag} <b>{cat}</b> {frm}→{to} <i class="{kind}">{delta}</i></span>')
    for name in countries[len(loc["demo_items"]):]:
        parts.append(f'<span class="t-cty">{name}</span>')
    return "".join(parts * 2)


def rank_track(was, now):
    """Slope-track HTML for a 1–25 rank scale. was=None means NEW entry."""
    pct = lambda r: (r - 1) / 24 * 100
    b = pct(now)
    if was is None:
        kind, a = "new", 100.0
    elif now < was:
        kind, a = "up", pct(was)
    else:
        kind, a = "down", pct(was)
    left, width = min(a, b), abs(a - b)
    style = f"--a:{left:.1f}%;--b:{b:.1f}%;--w:{width:.1f}%"
    pt_a = '' if was is None else f'<span class="pt a" style="left:{a:.1f}%"></span>'
    track = (f'<div class="track" style="{style}"><span class="rail"></span>'
             f'<span class="seg"></span>{pt_a}<span class="pt b" style="left:{b:.1f}%"></span></div>')
    return kind, track


def render(key):
    loc = LOCALES[key]
    rel = "../" if loc["dir"] else ""
    font_override = f'<style>body{{font-family:-apple-system,BlinkMacSystemFont,{loc["font"]},"Segoe UI",sans-serif}}</style>' if loc["font"] else ""
    stats = "".join(
        f'<span class="stat"><b class="{cls}">{g}</b>{label}</span>'
        for cls, g, label in loc["chips"]
    )
    steps = "".join(
        f'<div class="step"><div class="top"><span class="n">0{i+1}</span><span class="tag">{tag}</span></div><h3>{h}</h3><p>{p}</p></div>'
        for i, (tag, h, p) in enumerate(loc["steps"])
    )
    rank_rows = ""
    for (a, b, c), (was, now) in zip(loc["rank_rows"], loc["rank_nums"]):
        kind, track = rank_track(was, now)
        rank_rows += (f'<div class="rrow {kind}"><span class="was">{a}</span>{track}'
                      f'<span class="now">{b}</span><span class="cat">{c}</span></div>')
    views = "".join(
        f'<div class="view-card v{i+1}"><span class="ico">{ico}</span><h3>{h}</h3><p>{p}</p></div>'
        for i, (ico, h, p) in enumerate(loc["views"])
    )
    personas = "".join(
        f'<div class="persona"><span class="ptag">{tag}</span><h3>{h}</h3>'
        f'<p class="quote">{q}</p><p class="how">{body}</p></div>'
        for tag, h, q, body in loc["personas"]
    )
    shot_files = ["radar", "country", "discover"]
    shots = "".join(
        f'<figure><div class="phone"><img src="{rel}assets/shot-{loc["shots"]}-{f}.png" alt="{cap}" loading="lazy"><div class="island"></div></div><figcaption>{cap}</figcaption></figure>'
        for f, cap in zip(shot_files, loc["shots_caps"])
    )
    feats = "".join(
        f'<div class="feat"><span class="idx">0{i+1}</span><h3>{h}</h3><p>{p}</p></div>'
        for i, (h, p) in enumerate(loc["feats"])
    )
    demo_json = json.dumps(loc["demo_items"], ensure_ascii=False)
    spark = loc["demo_items"][1]
    spark_val = f'{spark[2]} → <span class="to">{spark[3]}</span><span class="d">{spark[4].split(" ·")[0]}</span>'

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
    <a class="wordmark" href="{rel if rel else './'}"><img src="{rel}assets/icon-180.png" alt=""><span>SIDEFEED</span></a>
    <div class="nav-right">
      <div class="lang">{lang_nav(loc['dir'], rel)}</div>
      <a class="nav-get" href="{APP_STORE_URL}">App Store</a>
    </div>
  </div>
</nav>

<div class="ticker" aria-hidden="true"><div class="track">{ticker_track(loc)}</div></div>

<header class="hero">
  <div class="wrap">
    <div>
      <div class="prod-pill"><span class="yt">▶</span>YouTube · {loc['kicker_num']}</div>
      <h1>{loc['h1']}</h1>
      <div class="stats">{stats}</div>
      <p class="sub">{loc['sub']}</p>
      <div class="cta">
        {badge(loc, 'storeLink')}
        <span class="note">{loc['note']}</span>
      </div>
    </div>
    <div class="phone-col">
      <div class="phone"><img src="{rel}assets/shot-{loc['shots']}-trending.png" alt="{loc['hero_alt']}"><div class="island"></div></div>
      <div class="panel panel-board">
        <div class="ph"><span>TOP MOVERS</span><span class="live-dot"></span></div>
        <div id="board">{board_rows(loc['demo_items'])}</div>
      </div>
      <div class="panel panel-spark">
        <div class="ph"><span>RANK · 6H</span><span>{spark[1]}</span></div>
        {SPARK_SVG}
        <div class="spark-val">{spark_val}</div>
      </div>
    </div>
  </div>
</header>

<section>
  <div class="wrap">
    <div class="mod"><span class="dot"></span>{loc['who_kicker']}<span class="num">{loc['who_num']}</span></div>
    <h2>{loc['who_h2']}</h2>
    <p class="lede">{loc['who_lede']}</p>
    <div class="personas">{personas}</div>
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap">
    <div class="mod"><span class="dot"></span>{loc['how_kicker']}<span class="num">01–03</span></div>
    <h2>{loc['how_h2']}</h2>
    <div class="steps">{steps}</div>
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap">
    <div class="mod"><span class="dot"></span>{loc['rank_kicker']}<span class="num">{loc['rank_num']}</span></div>
    <h2>{loc['rank_h2']}</h2>
    <p class="lede">{loc['rank_lede']}</p>
    <div class="rank-board">{rank_rows}</div>
    <div class="rank-scale"><span>#1</span><span>#13</span><span>#25</span></div>
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap">
    <div class="mod"><span class="dot"></span>{loc['views_kicker']}<span class="num">{loc['views_num']}</span></div>
    <h2>{loc['views_h2']}</h2>
    <p class="lede">{loc['views_lede']}</p>
    <div class="views">{views}</div>
  </div>
</section>

<section class="shots">
  <div class="wrap">
    <div class="mod"><span class="dot"></span>{loc['shots_kicker']}<span class="num">{loc['shots_num']}</span></div>
    <h2>{loc['shots_h2']}</h2>
    <div class="row">{shots}</div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="mod"><span class="dot"></span>{loc['feat_kicker']}<span class="num">{loc['feat_num']}</span></div>
    <h2>{loc['feat_h2']}</h2>
    <div class="grid6">{feats}</div>
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap">
    <div class="final-panel">
      <h2>{loc['final_h2']}</h2>
      <p class="lede">{loc['final_lede']}</p>
      <div class="cta">{badge(loc, 'storeLink2')}</div>
    </div>
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
    <div class="yt-note">YouTube is a trademark of Google LLC. Sidefeed is an independent app and is not endorsed by or affiliated with YouTube.</div>
  </div>
</footer>

<script>
  const items = {demo_json};
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Live "Top Movers" board — a new entry slides in every few seconds.
  const board = document.getElementById("board");
  const rowHTML = (item, enter) => {{
    const [flag, cat, , to, delta, kind] = item;
    const mv = to + " " + delta.split(" ·")[0];
    return '<div class="brow' + (enter ? ' enter' : '') + '"><span class="bflag">' + flag +
      '</span><span class="bcat">' + cat + '</span><span class="bmv ' + kind + '">' + mv + '</span></div>';
  }};
  if (!reduced && board) {{
    let head = 0;
    setInterval(() => {{
      head = (head + 1) % items.length;
      const visible = [0, 1, 2].map(o => items[(head + o) % items.length]);
      board.innerHTML = visible.map((it, idx) => rowHTML(it, idx === 0)).join("");
    }}, 3000);
  }}

  // Rank slope board — animate segments when scrolled into view.
  const rows = document.querySelectorAll(".rrow");
  if (reduced || !("IntersectionObserver" in window)) {{
    rows.forEach(r => r.classList.add("in"));
  }} else {{
    const io = new IntersectionObserver(entries => {{
      entries.forEach((e, i) => {{
        if (e.isIntersecting) {{ e.target.classList.add("in"); io.unobserve(e.target); }}
      }});
    }}, {{ threshold: 0.4 }});
    rows.forEach((r, i) => {{
      const seg = r.querySelector(".seg");
      if (seg) seg.style.transitionDelay = (i * 110) + "ms";
      io.observe(r);
    }});
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
