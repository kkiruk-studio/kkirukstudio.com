#!/usr/bin/env python3
"""Generate index.html for every locale from one template.

Usage: python3 build.py
Output: ./index.html (en), ./ko/index.html, ./ja/index.html,
        ./zh-hans/index.html, ./zh-hant/index.html
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).parent
BASE_URL = "https://www.kkirukstudio.com/locallink/"
OG_IMAGE = "https://www.kkirukstudio.com/locallink/og.png"
APP_STORE_URL = "https://apps.apple.com/app/id6767477190"

APPLE_SVG = '<svg viewBox="0 0 384 512" aria-hidden="true"><path d="M318.7 268.7c-.2-36.7 16.4-64.4 50-84.8-18.8-26.9-47.2-41.7-84.7-44.6-35.5-2.8-74.3 20.7-88.5 20.7-15 0-49.4-19.7-76.4-19.7C63.3 141.2 4 184.8 4 273.5q0 39.3 14.4 81.2c12.8 36.7 59 126.7 107.2 125.2 25.2-.6 43-17.9 75.8-17.9 31.8 0 48.3 17.9 76.4 17.9 48.6-.7 90.4-82.5 102.6-119.3-65.2-30.7-61.7-90-61.7-91.9zm-56.6-164.2c27.3-32.4 24.8-61.9 24-72.5-24.1 1.4-52 16.4-67.9 34.9-17.5 19.8-27.8 44.3-25.6 71.9 26.1 2 49.9-11.4 69.5-34.3z"/></svg>'

LANG_LABELS = [("", "EN"), ("ko/", "한국어"), ("ja/", "日本語"), ("zh-hans/", "简体"), ("zh-hant/", "繁體")]

LOCALES = {
    "en": {
        "dir": "", "lang": "en", "font": None, "shots": "en",
        "title": "Local Link — Open overseas places in local maps",
        "desc": "Type the place name you know. Local Link converts it into local-script search text and opens it in the map app that actually works there — Naver Map, KakaoMap, Amap, Google or Apple Maps.",
        "og_title": "Local Link — Travel Map Search",
        "og_desc": "Type the name you know. Open it in the map that actually works there.",
        "kicker_num": "TRAVEL MAP SEARCH",
        "h1": "Type the name you know.<br>Open it in the map that <em>actually works</em> there.",
        "pairs": [["Myeongdong", "명동"], ["Wukang Road", "武康路"], ["Ichiran Shibuya", "一蘭 渋谷"], ["Din Tai Fung", "鼎泰豐"]],
        "sub": "Google Maps barely works in Korea and not at all in China. Local Link converts the place names you know into local-script search text, then opens them in the map app locals actually use.",
        "badge_small": "Download on the", "note": "FREE · IPHONE &amp; IPAD · NO ACCOUNT",
        "badge_aria": "Download on the App Store",
        "chips": [["N", "Naver Map"], ["K", "KakaoMap"], ["高", "Amap"], ["G", "Google Maps"]],
        "hero_alt": "Local Link map selection screen showing Naver Map, KakaoMap, Apple Maps and Google Maps options for 명동",
        "marquee": ["KOREA", "CHINA", "JAPAN", "TAIWAN", "THAILAND", "VIETNAM", "HONG KONG", "MACAU"],
        "how_kicker": "HOW IT WORKS",
        "how_h2": "Three taps from <em>“how do I even spell that?”</em> to a pin on the map.",
        "steps": [
            ["DESTINATION", "Pick where you're going", "Choose the country and city. Local Link prepares searches that match how places are written there."],
            ["SEARCH", "Type the name you know", "English, romanized, or local spelling — the app generates the local-script candidates that map services actually match."],
            ["MAP", "Open in the right map", "One tap hands the converted search to Naver, Kakao, Amap, Google or Apple Maps. No app installed? It opens on the web."],
        ],
        "conv_kicker": "CONVERSION", "conv_num": "LOCAL SCRIPT",
        "conv_h2": "Names that finally <em>match</em>.",
        "conv_lede": "Local map services index places in their own script. Searching “Myeongdong Kyoja” in English gets you nothing on Naver — 명동교자 gets you lunch.",
        "conv_rows": [
            ["Myeongdong", "명동", "KOREA · HANGUL"],
            ["Wukang Road", "武康路", "CHINA · HANZI"],
            ["Ichiran Shibuya", "一蘭 渋谷", "JAPAN · KANJI"],
            ["Din Tai Fung", "鼎泰豐", "TAIWAN · HANZI"],
        ],
        "maps_kicker": "MAP APPS", "maps_num": "PER COUNTRY",
        "maps_h2": "The right map, <em>per country</em>.",
        "maps_lede": "Each destination gets the map apps that actually work there, in the right priority — with automatic web fallback when an app isn't installed.",
        "providers": [
            ["🇰🇷", "Korea", [["N", "Naver Map"], ["K", "KakaoMap"]]],
            ["🇨🇳", "China", [["高", "Amap (Gaode)"]]],
            ["🇯🇵", "Japan · Taiwan · SEA", [["G", "Google Maps"]]],
            ["🌍", "Everywhere", [["A", "Apple Maps"]]],
        ],
        "shots_kicker": "SCREENS", "shots_num": "IOS 26",
        "shots_h2": "Built like a field tool, <em>not a brochure</em>.",
        "shots_caps": ["LOCAL-SCRIPT CANDIDATES", "ONE-TAP MAP LAUNCH", "SAVED · ICLOUD SYNC"],
        "feat_kicker": "DETAILS", "feat_num": "06",
        "feat_h2": "Down to <em>the details</em>.",
        "feats": [
            ["Works offline", "The conversion data ships inside the app. Airport basement? Still converts."],
            ["No account, no tracking", "Nothing to sign up for. No analytics leave your device."],
            ["iCloud sync", "Saved places follow you to your iPad — through your own iCloud, not our servers."],
            ["Country shortcuts", "Curated searches per destination: coffee chains in Shanghai, beauty stores in Seoul."],
            ["5 languages", "English, 한국어, 日本語, 简体中文, 繁體中文 — UI and conversion both."],
            ["Copy &amp; large text", "Show the local script full-screen to a taxi driver, or copy it anywhere."],
        ],
        "final_h2": "Stop guessing spellings.", "final_lede": "Free on iPhone and iPad.",
        "f_contact": "Contact", "f_privacy": "Privacy", "f_terms": "Terms",
    },
    "ko": {
        "dir": "ko/", "lang": "ko", "font": '"Apple SD Gothic Neo", "Pretendard"', "shots": "ko",
        "title": "로컬링크 — 해외 장소, 현지 지도앱에서 바로 열기",
        "desc": "아는 이름 그대로 검색하면 로컬링크가 현지 문자 검색어로 바꿔서, 그 나라에서 진짜 쓰는 지도앱(고덕지도·구글·네이버·카카오·애플)으로 바로 열어줍니다.",
        "og_title": "로컬링크 — 여행 지도 검색",
        "og_desc": "아는 이름 그대로 검색하고, 현지에서 진짜 통하는 지도로 여세요.",
        "kicker_num": "여행 지도 검색",
        "h1": "아는 이름 그대로,<br>현지에서 <em>진짜 통하는</em> 지도로",
        "pairs": [["Wukang Road", "武康路"], ["이치란 시부야", "一蘭 渋谷"], ["딘타이펑 타이베이", "鼎泰豐 台北"], ["와이탄", "外滩"]],
        "sub": "중국에선 구글지도가 안 되고, 일본·대만에선 한국어 검색이 안 먹히죠. 로컬링크가 발음·로마자·한국어 표기를 현지 문자 검색어로 바꿔서, 그 나라에서 실제로 쓰는 지도앱으로 바로 열어줍니다.",
        "badge_small": "다운로드는", "note": "무료 · iPhone &amp; iPad · 가입 없음",
        "badge_aria": "App Store에서 다운로드",
        "chips": [["高", "고덕지도"], ["G", "구글 지도"], ["N", "네이버 지도"], ["A", "애플 지도"]],
        "hero_alt": "로컬링크 지도 선택 화면 — 武康路를 고덕지도·애플 지도로 여는 버튼",
        "marquee": ["중국", "일본", "대만", "태국", "베트남", "홍콩", "마카오", "한국"],
        "how_kicker": "사용 방법",
        "how_h2": "\"이거 어떻게 검색하지?\"에서 <em>지도 핀까지 세 번의 탭</em>.",
        "steps": [
            ["목적지", "여행 국가 선택", "나라와 도시를 고르면, 그 지역 표기에 맞는 검색을 준비합니다."],
            ["검색", "아는 이름으로 입력", "한국어 표기든 영문이든 발음대로든 — 현지 지도가 실제로 인식하는 현지 문자 후보를 만들어줍니다."],
            ["지도", "맞는 지도앱으로 열기", "변환된 검색어를 고덕지도·구글·네이버·카카오·애플 지도로 한 탭에 전달. 앱이 없으면 웹으로 열립니다."],
        ],
        "conv_kicker": "변환", "conv_num": "현지 문자",
        "conv_h2": "드디어 <em>검색이 되는</em> 이름.",
        "conv_lede": "현지 지도는 현지 문자로 장소를 찾습니다. 고덕지도에 \"Wukang Road\"를 쳐봐야 안 나오지만, 武康路는 바로 나옵니다.",
        "conv_rows": [
            ["Wukang Road", "武康路", "중국 · 한자"],
            ["이치란 시부야", "一蘭 渋谷", "일본 · 간지"],
            ["딘타이펑 타이베이", "鼎泰豐 台北", "대만 · 한자"],
            ["와이탄", "外滩", "중국 · 한자"],
        ],
        "maps_kicker": "지도앱", "maps_num": "나라별 분기",
        "maps_h2": "나라마다 <em>되는 지도가 다르니까</em>.",
        "maps_lede": "목적지마다 실제로 동작하는 지도앱을 우선순위대로 보여줍니다. 앱이 설치돼 있지 않으면 자동으로 웹 지도로 열립니다.",
        "providers": [
            ["🇨🇳", "중국", [["高", "고덕지도 (Amap)"]]],
            ["🇯🇵", "일본 · 대만 · 동남아", [["G", "구글 지도"]]],
            ["🇰🇷", "한국", [["N", "네이버 지도"], ["K", "카카오맵"]]],
            ["🌍", "어디서나", [["A", "애플 지도"]]],
        ],
        "shots_kicker": "화면", "shots_num": "IOS 26",
        "shots_h2": "실제 화면은 <em>이렇게 생겼어요</em>.",
        "shots_caps": ["현지 문자 후보", "한 탭 지도 열기", "저장 · iCloud 동기화"],
        "feat_kicker": "디테일", "feat_num": "06",
        "feat_h2": "<em>이런 것까지</em> 챙겼어요.",
        "feats": [
            ["오프라인 동작", "변환 데이터가 앱 안에 들어 있어요. 로밍이 안 터져도 변환은 됩니다."],
            ["가입·추적 없음", "계정도, 기기 밖으로 나가는 분석 데이터도 없습니다."],
            ["iCloud 동기화", "저장한 장소는 내 iCloud로 iPad까지 따라옵니다. 우리 서버가 아니라요."],
            ["나라별 추천 검색", "상하이 커피 체인, 도쿄 라멘 — 목적지별 자주 찾는 장소를 큐레이션."],
            ["5개 언어", "한국어 · English · 日本語 · 简体中文 · 繁體中文, UI와 변환 모두."],
            ["복사 · 크게 보기", "택시 기사님께 현지 문자를 전체 화면으로 보여주거나 어디든 붙여넣기."],
        ],
        "final_h2": "철자 고민은 이제 그만.", "final_lede": "iPhone · iPad 무료.",
        "f_contact": "문의", "f_privacy": "개인정보 처리방침", "f_terms": "이용약관",
    },
    "ja": {
        "dir": "ja/", "lang": "ja", "font": '"Hiragino Kaku Gothic ProN", "Hiragino Sans", "Yu Gothic"', "shots": "ja",
        "title": "ロコリンク — 海外の場所を現地の地図ですぐ開く",
        "desc": "知っている名前で検索すると、ロコリンクが現地の文字の検索語に変換し、その国で本当に使われている地図アプリ（Naver・Kakao・高徳・Google・Apple）で開きます。",
        "og_title": "ロコリンク — 旅行地図検索",
        "og_desc": "知っている名前のまま、現地で本当に使える地図へ。",
        "kicker_num": "旅行地図検索",
        "h1": "知っている名前のまま、<br>現地で<em>本当に使える</em>地図へ",
        "pairs": [["Myeongdong", "명동"], ["Hongdae", "홍대"], ["Wukang Road", "武康路"], ["Din Tai Fung", "鼎泰豐"]],
        "sub": "韓国では Google マップが弱く、中国では使えません。ロコリンクが英語名やローマ字を現地の文字の検索語に変換し、その国で実際に使われている地図アプリへつなぎます。",
        "badge_small": "ダウンロードは", "note": "無料 · iPhone &amp; iPad · 登録不要",
        "badge_aria": "App Store でダウンロード",
        "chips": [["N", "Naver Map"], ["K", "KakaoMap"], ["G", "Google マップ"], ["A", "Apple マップ"]],
        "hero_alt": "ロコリンクの地図選択画面 — 명동を Naver Map や KakaoMap で開くボタン",
        "marquee": ["韓国", "中国", "台湾", "タイ", "ベトナム", "香港", "マカオ", "日本"],
        "how_kicker": "使い方",
        "how_h2": "「どう綴るの？」から<em>地図のピンまで3タップ</em>。",
        "steps": [
            ["目的地", "行き先を選ぶ", "国と都市を選ぶと、その地域の表記に合った検索を用意します。"],
            ["検索", "知っている名前で入力", "英語名でもローマ字でも — 現地の地図が実際に認識する現地文字の候補を生成します。"],
            ["地図", "合う地図アプリで開く", "変換した検索語を Naver・Kakao・高徳・Google・Apple マップへワンタップで送信。アプリがなければウェブで開きます。"],
        ],
        "conv_kicker": "変換", "conv_num": "現地の文字",
        "conv_h2": "やっと<em>見つかる</em>名前。",
        "conv_lede": "現地の地図サービスは現地の文字で場所を探します。Naver に「Myeongdong Kyoja」と打っても出ませんが、명동교자なら一発です。",
        "conv_rows": [
            ["Myeongdong", "명동", "韓国 · ハングル"],
            ["Gyeongbokgung", "경복궁", "韓国 · ハングル"],
            ["Wukang Road", "武康路", "中国 · 漢字"],
            ["Din Tai Fung", "鼎泰豐", "台湾 · 漢字"],
        ],
        "maps_kicker": "地図アプリ", "maps_num": "国ごとに",
        "maps_h2": "国ごとに<em>使える地図が違う</em>から。",
        "maps_lede": "目的地ごとに、実際に使える地図アプリを優先順で表示。アプリが入っていなければ自動でウェブ地図が開きます。",
        "providers": [
            ["🇰🇷", "韓国", [["N", "Naver Map"], ["K", "KakaoMap"]]],
            ["🇨🇳", "中国", [["高", "高徳地図 (Amap)"]]],
            ["🇹🇼", "台湾 · 東南アジア", [["G", "Google マップ"]]],
            ["🌍", "どこでも", [["A", "Apple マップ"]]],
        ],
        "shots_kicker": "画面", "shots_num": "IOS 26",
        "shots_h2": "飾りより、<em>旅先で使う道具</em>。",
        "shots_caps": ["現地文字の候補", "ワンタップで地図起動", "保存 · iCloud 同期"],
        "feat_kicker": "こだわり", "feat_num": "06",
        "feat_h2": "<em>細部まで</em>気を配りました。",
        "feats": [
            ["オフラインで動く", "変換データはアプリに内蔵。電波がなくても変換できます。"],
            ["登録・トラッキングなし", "アカウント不要。分析データが端末の外に出ることはありません。"],
            ["iCloud 同期", "保存した場所はあなたの iCloud で iPad にも同期。当社サーバーは使いません。"],
            ["国別おすすめ検索", "ソウルのコスメ、上海のカフェ — 目的地ごとの定番をキュレーション。"],
            ["5言語対応", "日本語 · English · 한국어 · 简体中文 · 繁體中文、UI も変換も。"],
            ["コピー・拡大表示", "現地の文字を全画面でタクシー運転手に見せたり、どこへでもコピー。"],
        ],
        "final_h2": "綴りの悩みは、もう終わり。", "final_lede": "iPhone · iPad 無料。",
        "f_contact": "お問い合わせ", "f_privacy": "プライバシーポリシー", "f_terms": "利用規約",
    },
    "zh-hans": {
        "dir": "zh-hans/", "lang": "zh-Hans", "font": '"PingFang SC", "Heiti SC"', "shots": "zh-Hans",
        "title": "当地链接 — 海外地点直接用当地地图打开",
        "desc": "用你知道的名字搜索，当地链接把它转换成当地文字的搜索词，再用那个国家真正常用的地图应用（Naver、Kakao、Google、Apple）打开。",
        "og_title": "当地链接 — 旅行地图搜索",
        "og_desc": "用你知道的名字搜索，打开当地真正能用的地图。",
        "kicker_num": "旅行地图搜索",
        "h1": "用你知道的名字搜索，<br>打开<em>当地真正能用</em>的地图",
        "pairs": [["Myeongdong", "명동"], ["Hongdae", "홍대"], ["Gyeongbokgung", "경복궁"], ["Ichiran Shibuya", "一蘭 渋谷"]],
        "sub": "在韩国，谷歌地图很不好用 — 本地人都用 Naver 和 Kakao。当地链接把你知道的名字转换成当地文字的搜索词，再跳转到那个国家真正常用的地图应用。",
        "badge_small": "下载于", "note": "免费 · iPhone &amp; iPad · 无需注册",
        "badge_aria": "在 App Store 下载",
        "chips": [["N", "Naver 地图"], ["K", "Kakao 地图"], ["G", "谷歌地图"], ["A", "苹果地图"]],
        "hero_alt": "当地链接的地图选择界面 — 用 Naver Map 或 KakaoMap 打开 명동",
        "marquee": ["韩国", "日本", "泰国", "越南", "中国香港", "中国澳门", "中国台湾"],
        "how_kicker": "使用方法",
        "how_h2": "从“这个怎么拼？”到<em>地图大头针，只要三步</em>。",
        "steps": [
            ["目的地", "选择旅行国家", "选好国家和城市，应用会按当地的写法准备搜索。"],
            ["搜索", "输入你知道的名字", "英文或罗马字都可以 — 自动生成当地地图真正能识别的当地文字候选。"],
            ["地图", "用合适的地图打开", "一键把转换后的搜索词发给 Naver、Kakao、Google 或 Apple 地图。没装应用就用网页打开。"],
        ],
        "conv_kicker": "转换", "conv_num": "当地文字",
        "conv_h2": "终于<em>搜得到</em>的名字。",
        "conv_lede": "当地地图服务用当地文字收录地点。在 Naver 输入“Myeongdong Kyoja”什么都没有，输入 명동교자 马上找到。",
        "conv_rows": [
            ["Myeongdong", "명동", "韩国 · 韩文"],
            ["Hongdae", "홍대", "韩国 · 韩文"],
            ["Gyeongbokgung", "경복궁", "韩国 · 韩文"],
            ["Ichiran Shibuya", "一蘭 渋谷", "日本 · 日文"],
        ],
        "maps_kicker": "地图应用", "maps_num": "按国家",
        "maps_h2": "每个国家，<em>能用的地图都不一样</em>。",
        "maps_lede": "按目的地优先显示真正能用的地图应用。没有安装时自动改用网页地图打开。",
        "providers": [
            ["🇰🇷", "韩国", [["N", "Naver 地图"], ["K", "Kakao 地图"]]],
            ["🇯🇵", "日本 · 东南亚", [["G", "谷歌地图"]]],
            ["🇨🇳", "中国大陆", [["高", "高德地图"]]],
            ["🌍", "任何地方", [["A", "苹果地图"]]],
        ],
        "shots_kicker": "界面", "shots_num": "IOS 26",
        "shots_h2": "不是宣传册，是<em>旅途中的工具</em>。",
        "shots_caps": ["当地文字候选", "一键打开地图", "收藏 · iCloud 同步"],
        "feat_kicker": "细节", "feat_num": "06",
        "feat_h2": "<em>连细节</em>都照顾到了。",
        "feats": [
            ["离线可用", "转换数据内置在应用里，没有网络也能转换。"],
            ["无注册、无追踪", "不需要账号，分析数据不会离开你的设备。"],
            ["iCloud 同步", "收藏的地点通过你自己的 iCloud 同步到 iPad，不经过我们的服务器。"],
            ["按国家推荐", "首尔美妆、东京拉面 — 按目的地精选常用搜索。"],
            ["5 种语言", "简体中文 · English · 한국어 · 日本語 · 繁體中文，界面和转换都支持。"],
            ["复制 · 放大显示", "把当地文字全屏给出租车司机看，或复制到任何地方。"],
        ],
        "final_h2": "别再纠结怎么拼了。", "final_lede": "iPhone · iPad 免费。",
        "f_contact": "联系我们", "f_privacy": "隐私政策", "f_terms": "服务条款",
    },
    "zh-hant": {
        "dir": "zh-hant/", "lang": "zh-Hant", "font": '"PingFang TC", "Heiti TC"', "shots": "zh-Hant",
        "title": "在地連結 — 海外地點直接用在地地圖開啟",
        "desc": "用你知道的名稱搜尋，在地連結把它轉成在地文字的搜尋詞，再用那個國家真正常用的地圖 App（Naver、Kakao、Google、Apple）開啟。",
        "og_title": "在地連結 — 旅遊地圖搜尋",
        "og_desc": "用你知道的名稱搜尋，開啟在地真正能用的地圖。",
        "kicker_num": "旅遊地圖搜尋",
        "h1": "用你知道的名稱搜尋，<br>開啟<em>在地真正能用</em>的地圖",
        "pairs": [["Myeongdong", "명동"], ["Hongdae", "홍대"], ["Gyeongbokgung", "경복궁"], ["Ichiran Shibuya", "一蘭 渋谷"]],
        "sub": "在韓國，Google 地圖很難用 — 當地人都用 Naver 和 Kakao。在地連結把你知道的名稱轉成在地文字的搜尋詞，再連到那個國家真正常用的地圖 App。",
        "badge_small": "下載於", "note": "免費 · iPhone &amp; iPad · 免註冊",
        "badge_aria": "在 App Store 下載",
        "chips": [["N", "Naver 地圖"], ["K", "Kakao 地圖"], ["G", "Google 地圖"], ["A", "Apple 地圖"]],
        "hero_alt": "在地連結的地圖選擇畫面 — 用 Naver Map 或 KakaoMap 開啟 명동",
        "marquee": ["韓國", "日本", "泰國", "越南", "香港", "澳門", "台灣"],
        "how_kicker": "使用方式",
        "how_h2": "從「這要怎麼拼？」到<em>地圖大頭針，只要三步</em>。",
        "steps": [
            ["目的地", "選擇旅遊國家", "選好國家和城市，App 會依當地的寫法準備搜尋。"],
            ["搜尋", "輸入你知道的名稱", "英文或羅馬拼音都可以 — 自動產生在地地圖真正能辨識的在地文字候選。"],
            ["地圖", "用合適的地圖開啟", "一鍵把轉換後的搜尋詞傳給 Naver、Kakao、Google 或 Apple 地圖。沒裝 App 就用網頁開啟。"],
        ],
        "conv_kicker": "轉換", "conv_num": "在地文字",
        "conv_h2": "終於<em>搜得到</em>的名稱。",
        "conv_lede": "在地地圖服務用在地文字收錄地點。在 Naver 輸入「Myeongdong Kyoja」什麼都沒有，輸入 명동교자 馬上找到。",
        "conv_rows": [
            ["Myeongdong", "명동", "韓國 · 韓文"],
            ["Hongdae", "홍대", "韓國 · 韓文"],
            ["Gyeongbokgung", "경복궁", "韓國 · 韓文"],
            ["Ichiran Shibuya", "一蘭 渋谷", "日本 · 日文"],
        ],
        "maps_kicker": "地圖 App", "maps_num": "依國家",
        "maps_h2": "每個國家，<em>能用的地圖都不一樣</em>。",
        "maps_lede": "依目的地優先顯示真正能用的地圖 App。沒有安裝時自動改用網頁地圖開啟。",
        "providers": [
            ["🇰🇷", "韓國", [["N", "Naver 地圖"], ["K", "Kakao 地圖"]]],
            ["🇯🇵", "日本 · 東南亞", [["G", "Google 地圖"]]],
            ["🇨🇳", "中國大陸", [["高", "高德地圖"]]],
            ["🌍", "任何地方", [["A", "Apple 地圖"]]],
        ],
        "shots_kicker": "畫面", "shots_num": "IOS 26",
        "shots_h2": "不是型錄，是<em>旅途中的工具</em>。",
        "shots_caps": ["在地文字候選", "一鍵開啟地圖", "收藏 · iCloud 同步"],
        "feat_kicker": "細節", "feat_num": "06",
        "feat_h2": "<em>連細節</em>都照顧到了。",
        "feats": [
            ["離線可用", "轉換資料內建在 App 裡，沒有網路也能轉換。"],
            ["免註冊、無追蹤", "不需要帳號，分析資料不會離開你的裝置。"],
            ["iCloud 同步", "收藏的地點透過你自己的 iCloud 同步到 iPad，不經過我們的伺服器。"],
            ["依國家推薦", "首爾美妝、東京拉麵 — 依目的地精選常用搜尋。"],
            ["5 種語言", "繁體中文 · English · 한국어 · 日本語 · 简体中文，介面和轉換都支援。"],
            ["複製 · 放大顯示", "把在地文字全螢幕給計程車司機看，或複製到任何地方。"],
        ],
        "final_h2": "別再煩惱怎麼拼了。", "final_lede": "iPhone · iPad 免費。",
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
    return (f'<a class="store-badge" id="{el_id}" href="{APP_STORE_URL}" aria-label="{loc["badge_aria"]}">{APPLE_SVG}'
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
    conv = "".join(
        f'<div class="convert-row"><span>{a}</span><span class="arrow">→</span><span class="to">{b}</span><span class="cat">{c}</span></div>'
        for a, b, c in loc["conv_rows"]
    )
    provs = "".join(
        '<div class="prov"><span class="flag">%s</span><h3>%s</h3><ul>%s</ul></div>'
        % (flag, name, "".join(f'<li><span class="g">{g}</span>{n}</li>' for g, n in items))
        for flag, name, items in loc["providers"]
    )
    shot_files = ["03-candidates", "05-launch", "04-saved"]
    shots = "".join(
        f'<figure><div class="phone"><img src="{rel}assets/shot-{loc["shots"]}-{f}.png" alt="{cap}" loading="lazy"><div class="island"></div></div><figcaption>{cap}</figcaption></figure>'
        for f, cap in zip(shot_files, loc["shots_caps"])
    )
    feats = "".join(f'<div class="feat"><h3>{h}</h3><p>{p}</p></div>' for h, p in loc["feats"])
    pairs_json = json.dumps(loc["pairs"], ensure_ascii=False)
    canonical = f"{BASE_URL}{loc['dir']}"

    html = f"""<!doctype html>
<html lang="{loc['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{loc['title']}</title>
<meta name="description" content="{loc['desc']}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{loc['og_title']}">
<meta property="og:description" content="{loc['og_desc']}">
<meta property="og:image" content="{OG_IMAGE}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="kkiruk studio">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{OG_IMAGE}">
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
    <a class="wordmark" href="{rel if rel else './'}"><img src="{rel}assets/icon-180.png" alt=""><span>LOCAL·LINK</span></a>
    <div class="lang">{lang_nav(loc['dir'], rel)}</div>
  </div>
</nav>

<header class="hero">
  <div class="ghost">L·L</div>
  <div class="wrap">
    <div>
      <div class="kicker"><span>LOCAL · LINK</span><span class="rule"></span><span class="num">{loc['kicker_num']}</span></div>
      <h1>{loc['h1']}</h1>
      <div class="demo">
        <span class="src" id="demoSrc">{loc['pairs'][0][0]}</span>
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
      <div class="phone"><img src="{rel}assets/shot-{loc['shots']}-05-launch.png" alt="{loc['hero_alt']}"><div class="island"></div></div>
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
  const APP_STORE_URL = "https://apps.apple.com/app/id6767477190";
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
