#!/usr/bin/env python3
"""Generate index.html for every locale from one template.

Usage: python3 build.py
Output: ./index.html (en), ./ko/index.html, ./ja/index.html,
        ./zh-hans/index.html, ./zh-hant/index.html
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).parent
BASE_URL = "https://www.kkirukstudio.com/pinclip/"
APP_STORE_URL = "https://apps.apple.com/app/id6761982511"

APPLE_SVG = '<svg viewBox="0 0 384 512" aria-hidden="true"><path d="M318.7 268.7c-.2-36.7 16.4-64.4 50-84.8-18.8-26.9-47.2-41.7-84.7-44.6-35.5-2.8-74.3 20.7-88.5 20.7-15 0-49.4-19.7-76.4-19.7C63.3 141.2 4 184.8 4 273.5q0 39.3 14.4 81.2c12.8 36.7 59 126.7 107.2 125.2 25.2-.6 43-17.9 75.8-17.9 31.8 0 48.3 17.9 76.4 17.9 48.6-.7 90.4-82.5 102.6-119.3-65.2-30.7-61.7-90-61.7-91.9zm-56.6-164.2c27.3-32.4 24.8-61.9 24-72.5-24.1 1.4-52 16.4-67.9 34.9-17.5 19.8-27.8 44.3-25.6 71.9 26.1 2 49.9-11.4 69.5-34.3z"/></svg>'

LANG_LABELS = [("", "EN"), ("ko/", "한국어"), ("ja/", "日本語"), ("zh-hans/", "简体"), ("zh-hant/", "繁體")]

LOCALES = {
    "en": {
        "dir": "", "lang": "en", "font": None, "shots": "en",
        "title": "Pinclip — Save Shorts, Reels & TikToks. Find them in 3 seconds.",
        "desc": "One share-sheet tap saves any short-form video with its title and thumbnail filled in automatically. Folders, tags, widgets and iCloud sync — your videos, organized.",
        "og_title": "Pinclip — Short-form Video Bookmarks",
        "og_desc": "Saved in one tap. Found in three seconds.",
        "kicker_num": "SHORT-FORM VIDEO BOOKMARKS",
        "h1": "Saved in one tap.<br>Found in <em>three seconds</em>.",
        "pairs": [["youtube.com/shorts/xK4q2…", "📌 5-Minute Pasta Recipe"], ["instagram.com/reel/Cq8w1…", "📌 Fall Daily Look Outfits"], ["tiktok.com/@fit/video/7284…", "📌 5-Min Plank Challenge"], ["youtube.com/shorts/m3Vt8…", "📌 Best 7 Cafes in Brooklyn"]],
        "sub": "That recipe Short you'd swear you saved? Pinclip keeps every Shorts, Reels and TikTok link in one place — title and thumbnail filled in automatically, sorted into folders you'll actually open again.",
        "badge_small": "Download on the", "note": "FREE DOWNLOAD · IPHONE &amp; IPAD",
        "badge_aria": "Download on the App Store",
        "chips": [["▶", "YouTube Shorts"], ["✦", "Instagram Reels"], ["♪", "TikTok"], ["#", "Tags &amp; Notes"]],
        "hero_alt": "Pinclip home screen with recently saved videos and folders like Recipes, Home Workout and NYC Cafes",
        "marquee": ["SHORTS", "REELS", "TIKTOK", "FOLDERS", "TAGS", "NOTES", "WIDGETS", "ICLOUD SYNC"],
        "how_kicker": "HOW IT WORKS",
        "how_h2": "From <em>“I'll watch this later”</em> to actually finding it later.",
        "steps": [
            ["SHARE", "Tap Pinclip in the share sheet", "Watching a video you want to keep? Hit share, tap Pinclip — done. No app switching."],
            ["AUTO", "Title &amp; thumbnail, filled in", "Pinclip pulls the title and thumbnail automatically, so your library looks like a library — not a wall of links."],
            ["ORGANIZE", "Folders, tags, notes", "Drop it in a folder, add a #tag or a note about why you saved it. Future you says thanks."],
        ],
        "conv_kicker": "RETRIEVAL", "conv_num": "3 SECONDS",
        "conv_h2": "A vague memory becomes <em>an exact place</em>.",
        "conv_lede": "Saved links you never open are just guilt. Pinclip turns “that workout video from last week” into a folder and a tag you can jump to.",
        "conv_rows": [
            ["that pasta Short from Tuesday", "Recipes · #pasta", "YOUTUBE · SHORTS"],
            ["the outfit Reel I liked", "Fashion · #ootd", "INSTAGRAM · REELS"],
            ["that plank challenge", "Home Workout · #core", "TIKTOK"],
            ["cafes for the weekend", "NYC Cafes · #brooklyn", "YOUTUBE"],
        ],
        "maps_kicker": "PLATFORMS", "maps_num": "ONE LIBRARY",
        "maps_h2": "Every platform, <em>one library</em>.",
        "maps_lede": "Share from any app that has a link. YouTube and TikTok fill in titles and thumbnails automatically; everything lands in the same searchable library.",
        "providers": [
            ["▶", "YouTube Shorts", [["✓", "Auto title"], ["✓", "Auto thumbnail"]]],
            ["♪", "TikTok", [["✓", "Auto title"], ["✓", "Auto thumbnail"]]],
            ["✦", "Instagram Reels", [["✓", "One-tap save"], ["✓", "Smart folders"]]],
            ["∞", "Any video link", [["✓", "Same library"], ["✓", "Tag search"]]],
        ],
        "shots_kicker": "SCREENS", "shots_num": "IPHONE &amp; IPAD",
        "shots_h2": "Built for finding, <em>not just hoarding</em>.",
        "shots_caps": ["FOLDERS THAT STAY TIDY", "TAGS · NOTES · ONE TAP BACK", "YOUR WHOLE FEED, SEARCHABLE"],
        "feat_kicker": "DETAILS", "feat_num": "06",
        "feat_h2": "Small app. <em>Sharp</em> details.",
        "feats": [
            ["Share-sheet native", "Save from YouTube, Instagram or TikTok without leaving them. Two taps, back to scrolling."],
            ["Home Screen widgets", "Pin folders or favorite clips to your Home Screen — one tap from unlock to video."],
            ["iCloud sync", "Pro syncs your library to iPad through your own iCloud — not our servers."],
            ["Share a folder", "Send a folder as a link. Friends see the list in their browser — and can import it into their Pinclip."],
            ["Smart folders", "Auto-grouped by platform: every Short, Reel and TikTok files itself."],
            ["Tags &amp; notes", "Add #tags and a why-I-saved-this note. Tap a tag to pull up everything related."],
        ],
        "final_h2": "Stop losing videos to the scroll.", "final_lede": "Free on iPhone and iPad.",
        "f_contact": "Contact", "f_privacy": "Privacy", "f_terms": "Terms",
    },
    "ko": {
        "dir": "ko/", "lang": "ko", "font": '"Apple SD Gothic Neo", "Pretendard"', "shots": "ko",
        "title": "Pinclip — 쇼츠·릴스 저장, 3초 만에 다시 찾기",
        "desc": "공유 시트에서 한 번 탭하면 제목·썸네일까지 자동 저장. 폴더·태그·위젯·iCloud 동기화로 숏폼 영상을 깔끔하게 정리하세요.",
        "og_title": "Pinclip — 숏폼 영상 북마크",
        "og_desc": "저장은 한 탭, 다시 찾기는 3초.",
        "kicker_num": "숏폼 영상 북마크",
        "h1": "저장은 한 탭,<br>다시 찾기는 <em>3초</em>.",
        "pairs": [["youtube.com/shorts/xK4q2…", "📌 5분 완성 파스타 레시피"], ["instagram.com/reel/Cq8w1…", "📌 가을 데일리룩 코디"], ["tiktok.com/@fit/video/7284…", "📌 5분 플랭크 챌린지"], ["youtube.com/shorts/m3Vt8…", "📌 성수동 카페 추천 BEST 7"]],
        "sub": "분명히 저장했는데 못 찾는 그 레시피 쇼츠. Pinclip은 쇼츠·릴스·틱톡 링크를 제목·썸네일과 함께 한곳에 모으고, 다시 열어보게 되는 폴더로 정리해 줍니다.",
        "badge_small": "다운로드는", "note": "무료 다운로드 · iPHONE &amp; iPAD",
        "badge_aria": "App Store에서 다운로드",
        "chips": [["▶", "유튜브 쇼츠"], ["✦", "인스타 릴스"], ["♪", "틱톡"], ["#", "태그·메모"]],
        "hero_alt": "Pinclip 홈 화면 — 최근 저장한 영상과 레시피·홈트 루틴·서울 카페 폴더",
        "marquee": ["쇼츠", "릴스", "틱톡", "폴더", "태그", "메모", "위젯", "iCLOUD 동기화"],
        "how_kicker": "사용 방법",
        "how_h2": "\"나중에 봐야지\"가 <em>진짜 나중에 보게</em> 되기까지.",
        "steps": [
            ["공유", "공유 시트에서 Pinclip 탭", "보다가 저장하고 싶은 영상이 생기면 공유 버튼 → Pinclip. 앱 전환 없이 끝."],
            ["자동", "제목·썸네일 자동 입력", "링크만 던지면 제목과 썸네일을 알아서 채웁니다. 링크 무더기가 아니라 한눈에 보이는 라이브러리로."],
            ["정리", "폴더·태그·메모", "폴더에 넣고 #태그와 저장한 이유를 메모로. 미래의 내가 고마워합니다."],
        ],
        "conv_kicker": "다시 찾기", "conv_num": "3초",
        "conv_h2": "흐릿한 기억이 <em>정확한 위치</em>가 됩니다.",
        "conv_lede": "열어보지 않는 저장은 마음의 짐일 뿐. Pinclip은 \"지난주에 본 그 운동 영상\"을 바로 점프할 수 있는 폴더와 태그로 바꿔줍니다.",
        "conv_rows": [
            ["화요일에 본 그 파스타 쇼츠", "레시피 · #파스타", "유튜브 · 쇼츠"],
            ["좋아요 누른 코디 릴스", "패션 · #코디", "인스타그램 · 릴스"],
            ["그 플랭크 챌린지", "홈트 루틴 · #코어", "틱톡"],
            ["주말에 갈 카페", "서울 카페 · #성수동", "유튜브"],
        ],
        "maps_kicker": "플랫폼", "maps_num": "라이브러리 하나",
        "maps_h2": "어느 플랫폼이든, <em>라이브러리는 하나</em>.",
        "maps_lede": "링크가 있는 앱이면 어디서든 공유로 저장. 유튜브·틱톡은 제목·썸네일까지 자동으로 채워지고, 전부 한곳에서 검색됩니다.",
        "providers": [
            ["▶", "유튜브 쇼츠", [["✓", "제목 자동"], ["✓", "썸네일 자동"]]],
            ["♪", "틱톡", [["✓", "제목 자동"], ["✓", "썸네일 자동"]]],
            ["✦", "인스타 릴스", [["✓", "한 탭 저장"], ["✓", "스마트 폴더"]]],
            ["∞", "그 외 영상 링크", [["✓", "같은 라이브러리"], ["✓", "태그 검색"]]],
        ],
        "shots_kicker": "화면", "shots_num": "iPHONE &amp; iPAD",
        "shots_h2": "쌓아두기가 아니라 <em>다시 찾기</em>를 위한 화면.",
        "shots_caps": ["폴더로 깔끔하게", "태그 · 메모 · 원본 열기", "전체 피드 검색"],
        "feat_kicker": "디테일", "feat_num": "06",
        "feat_h2": "작은 앱, <em>분명한</em> 디테일.",
        "feats": [
            ["공유 시트 저장", "유튜브·인스타·틱톡을 벗어나지 않고 저장. 두 번 탭하고 다시 스크롤."],
            ["홈 화면 위젯", "폴더와 즐겨 보는 핀을 홈 화면에. 잠금 해제에서 영상까지 한 탭."],
            ["iCloud 동기화", "Pro는 내 iCloud로 iPad까지 동기화 — 우리 서버가 아니라요."],
            ["폴더 공유 링크", "폴더를 링크 하나로 공유. 받은 사람은 브라우저로 보고, 자기 Pinclip으로 가져갈 수도 있어요."],
            ["스마트 폴더", "쇼츠·릴스·틱톡이 플랫폼별로 알아서 분류됩니다."],
            ["태그와 메모", "#태그와 저장한 이유 메모. 태그 한 번 탭이면 관련 영상이 모두."],
        ],
        "final_h2": "스크롤에 영상 그만 잃어버리세요.", "final_lede": "iPhone · iPad 무료.",
        "f_contact": "문의", "f_privacy": "개인정보 처리방침", "f_terms": "이용약관",
    },
    "ja": {
        "dir": "ja/", "lang": "ja", "font": '"Hiragino Kaku Gothic ProN", "Hiragino Sans", "Yu Gothic"', "shots": "ja",
        "title": "Pinclip — ショート・リールを保存、3秒で見つかる",
        "desc": "共有シートでワンタップ保存。タイトルとサムネイルは自動入力。フォルダ・タグ・ウィジェット・iCloud同期でショート動画をすっきり整理。",
        "og_title": "Pinclip — ショート動画ブックマーク",
        "og_desc": "保存はワンタップ、見つけるのは3秒。",
        "kicker_num": "ショート動画ブックマーク",
        "h1": "保存はワンタップ、<br>見つけるのは<em>3秒</em>。",
        "pairs": [["youtube.com/shorts/xK4q2…", "📌 5分で作れるパスタレシピ"], ["instagram.com/reel/Cq8w1…", "📌 秋のデイリーコーデ"], ["tiktok.com/@fit/video/7284…", "📌 5分プランクチャレンジ"], ["youtube.com/shorts/m3Vt8…", "📌 京都おすすめカフェ7選"]],
        "sub": "確かに保存したはずのあのレシピ動画、どこへ？ Pinclip はショート・リール・TikTok のリンクをタイトルとサムネイル付きで一か所に集め、また開きたくなるフォルダに整理します。",
        "badge_small": "ダウンロードは", "note": "無料ダウンロード · iPHONE &amp; iPAD",
        "badge_aria": "App Store でダウンロード",
        "chips": [["▶", "YouTube ショート"], ["✦", "インスタ リール"], ["♪", "TikTok"], ["#", "タグ・メモ"]],
        "hero_alt": "Pinclip のホーム画面 — 最近保存した動画とレシピ・ホームトレーニング・京都カフェのフォルダ",
        "marquee": ["ショート", "リール", "TIKTOK", "フォルダ", "タグ", "メモ", "ウィジェット", "iCLOUD同期"],
        "how_kicker": "使い方",
        "how_h2": "「あとで見る」が<em>本当にあとで見られる</em>まで。",
        "steps": [
            ["共有", "共有シートで Pinclip をタップ", "残したい動画に出会ったら共有ボタン → Pinclip。アプリを切り替えずに完了。"],
            ["自動", "タイトルとサムネイルを自動入力", "リンクを渡すだけで、タイトルとサムネイルが自動で埋まります。リンクの山ではなく、見えるライブラリに。"],
            ["整理", "フォルダ・タグ・メモ", "フォルダに入れて #タグ と保存した理由のメモを。未来の自分が感謝します。"],
        ],
        "conv_kicker": "見つける", "conv_num": "3秒",
        "conv_h2": "あいまいな記憶が<em>正確な場所</em>になる。",
        "conv_lede": "開かない保存はただの罪悪感。Pinclip は「先週見たあのトレーニング動画」を、すぐ飛べるフォルダとタグに変えます。",
        "conv_rows": [
            ["火曜に見たあのパスタ動画", "レシピ · #パスタ", "YOUTUBE · ショート"],
            ["いいねしたコーデのリール", "ファッション · #コーデ", "INSTAGRAM · リール"],
            ["あのプランクチャレンジ", "ホームトレーニング · #体幹", "TIKTOK"],
            ["週末に行くカフェ", "京都カフェ · #嵐山", "YOUTUBE"],
        ],
        "maps_kicker": "プラットフォーム", "maps_num": "ライブラリはひとつ",
        "maps_h2": "どのプラットフォームも、<em>ライブラリはひとつ</em>。",
        "maps_lede": "リンクのあるアプリならどこからでも共有で保存。YouTube・TikTok はタイトルとサムネイルまで自動。すべて一か所で検索できます。",
        "providers": [
            ["▶", "YouTube ショート", [["✓", "タイトル自動"], ["✓", "サムネイル自動"]]],
            ["♪", "TikTok", [["✓", "タイトル自動"], ["✓", "サムネイル自動"]]],
            ["✦", "インスタ リール", [["✓", "ワンタップ保存"], ["✓", "スマートフォルダ"]]],
            ["∞", "その他の動画リンク", [["✓", "同じライブラリ"], ["✓", "タグ検索"]]],
        ],
        "shots_kicker": "画面", "shots_num": "iPHONE &amp; iPAD",
        "shots_h2": "ためるためではなく、<em>見つけるため</em>の画面。",
        "shots_caps": ["フォルダですっきり", "タグ · メモ · 元リンク", "フィード全体を検索"],
        "feat_kicker": "こだわり", "feat_num": "06",
        "feat_h2": "小さなアプリ、<em>確かな</em>ディテール。",
        "feats": [
            ["共有シートで保存", "YouTube・Instagram・TikTok を離れずに保存。2タップでスクロールに戻る。"],
            ["ホーム画面ウィジェット", "フォルダやお気に入りのピンをホーム画面に。ロック解除から動画までワンタップ。"],
            ["iCloud 同期", "Pro は自分の iCloud で iPad にも同期 — 当社サーバーは使いません。"],
            ["フォルダ共有リンク", "フォルダをリンクひとつで共有。受け取った人はブラウザで見られて、自分の Pinclip に取り込むことも。"],
            ["スマートフォルダ", "ショート・リール・TikTok がプラットフォーム別に自動分類。"],
            ["タグとメモ", "#タグ と保存した理由のメモ。タグをタップすれば関連動画がすべて。"],
        ],
        "final_h2": "スクロールに動画を失うのは、もう終わり。", "final_lede": "iPhone · iPad 無料。",
        "f_contact": "お問い合わせ", "f_privacy": "プライバシーポリシー", "f_terms": "利用規約",
    },
    "zh-hans": {
        "dir": "zh-hans/", "lang": "zh-Hans", "font": '"PingFang SC", "Heiti SC"', "shots": "zh-Hans",
        "title": "Pinclip — 收藏 Shorts、Reels 和 TikTok，3 秒找回",
        "desc": "在分享面板轻点一下即可保存短视频链接，标题和封面自动抓取。文件夹、标签、小组件和 iCloud 同步，让收藏井井有条。",
        "og_title": "Pinclip — 短视频书签",
        "og_desc": "保存只要一下，找回只要 3 秒。",
        "kicker_num": "短视频书签",
        "h1": "保存只要一下，<br>找回只要<em> 3 秒</em>。",
        "pairs": [["youtube.com/shorts/xK4q2…", "📌 5分钟意面食谱"], ["instagram.com/reel/Cq8w1…", "📌 秋季日常穿搭"], ["tiktok.com/@fit/video/7284…", "📌 5分钟平板支撑挑战"], ["youtube.com/shorts/m3Vt8…", "📌 巴黎7家推荐咖啡馆"]],
        "sub": "明明收藏过的那条食谱视频，怎么找不到了？Pinclip 把 Shorts、Reels 和 TikTok 链接连同标题、封面一起收进一个地方，整理成你真的会再打开的文件夹。",
        "badge_small": "下载于", "note": "免费下载 · iPHONE &amp; iPAD",
        "badge_aria": "在 App Store 下载",
        "chips": [["▶", "YouTube Shorts"], ["✦", "Instagram Reels"], ["♪", "TikTok"], ["#", "标签·备注"]],
        "hero_alt": "Pinclip 主页 — 最近保存的视频和食谱、居家健身、巴黎咖啡馆等文件夹",
        "marquee": ["SHORTS", "REELS", "TIKTOK", "文件夹", "标签", "备注", "小组件", "iCLOUD 同步"],
        "how_kicker": "使用方法",
        "how_h2": "从“以后再看”，到<em>真的能再看到</em>。",
        "steps": [
            ["分享", "在分享面板点 Pinclip", "刷到想留下的视频？点分享 → Pinclip，不用切换应用就完成。"],
            ["自动", "标题封面自动抓取", "只要给它链接，标题和封面自动填好。不是一堆链接，而是一眼能认出的收藏库。"],
            ["整理", "文件夹·标签·备注", "放进文件夹，加上 #标签 和收藏理由。未来的你会感谢现在的你。"],
        ],
        "conv_kicker": "找回", "conv_num": "3 秒",
        "conv_h2": "模糊的印象，变成<em>准确的位置</em>。",
        "conv_lede": "从不打开的收藏只是心理负担。Pinclip 把“上周看过的那条健身视频”变成一点就到的文件夹和标签。",
        "conv_rows": [
            ["周二刷到的意面视频", "食谱 · #意面", "YOUTUBE · SHORTS"],
            ["点过赞的穿搭 Reels", "时尚 · #穿搭", "INSTAGRAM · REELS"],
            ["那个平板支撑挑战", "居家健身 · #核心", "TIKTOK"],
            ["周末想去的咖啡馆", "巴黎咖啡馆 · #咖啡", "YOUTUBE"],
        ],
        "maps_kicker": "平台", "maps_num": "一个收藏库",
        "maps_h2": "平台再多，<em>收藏库只有一个</em>。",
        "maps_lede": "任何能分享链接的应用都可以保存。YouTube 和 TikTok 连标题封面都自动抓取，全部汇入同一个可搜索的收藏库。",
        "providers": [
            ["▶", "YouTube Shorts", [["✓", "自动标题"], ["✓", "自动封面"]]],
            ["♪", "TikTok", [["✓", "自动标题"], ["✓", "自动封面"]]],
            ["✦", "Instagram Reels", [["✓", "一键保存"], ["✓", "智能文件夹"]]],
            ["∞", "其他视频链接", [["✓", "同一个收藏库"], ["✓", "标签搜索"]]],
        ],
        "shots_kicker": "界面", "shots_num": "iPHONE &amp; iPAD",
        "shots_h2": "不是为了囤积，是<em>为了找回</em>。",
        "shots_caps": ["文件夹井井有条", "标签 · 备注 · 一键回看", "整个收藏随手搜"],
        "feat_kicker": "细节", "feat_num": "06",
        "feat_h2": "小应用，<em>讲究的</em>细节。",
        "feats": [
            ["分享面板直接保存", "不离开 YouTube、Instagram 或 TikTok，两下点击，继续刷。"],
            ["主屏幕小组件", "把文件夹或常看的视频钉在主屏幕，解锁到播放只要一步。"],
            ["iCloud 同步", "Pro 通过你自己的 iCloud 同步到 iPad——不经过我们的服务器。"],
            ["文件夹分享链接", "把文件夹变成一条链接分享。对方在浏览器查看，还能导入自己的 Pinclip。"],
            ["智能文件夹", "Shorts、Reels、TikTok 按平台自动归类。"],
            ["标签和备注", "加 #标签 和收藏理由。点一下标签，相关视频全部出现。"],
        ],
        "final_h2": "别再让视频消失在信息流里。", "final_lede": "iPhone · iPad 免费。",
        "f_contact": "联系我们", "f_privacy": "隐私政策", "f_terms": "服务条款",
    },
    "zh-hant": {
        "dir": "zh-hant/", "lang": "zh-Hant", "font": '"PingFang TC", "Heiti TC"', "shots": "zh-Hant",
        "title": "Pinclip — 收藏 Shorts、Reels 和 TikTok，3 秒找回",
        "desc": "在分享面板輕點一下就能儲存短影音連結，標題與封面自動抓取。資料夾、標籤、小工具與 iCloud 同步，收藏井然有序。",
        "og_title": "Pinclip — 短影音書籤",
        "og_desc": "儲存只要一下，找回只要 3 秒。",
        "kicker_num": "短影音書籤",
        "h1": "儲存只要一下，<br>找回只要<em> 3 秒</em>。",
        "pairs": [["youtube.com/shorts/xK4q2…", "📌 5分鐘義大利麵食譜"], ["instagram.com/reel/Cq8w1…", "📌 秋季日常穿搭"], ["tiktok.com/@fit/video/7284…", "📌 5分鐘棒式挑戰"], ["youtube.com/shorts/m3Vt8…", "📌 羅馬7家推薦咖啡廳"]],
        "sub": "明明收藏過的那支食譜影片，怎麼找不到了？Pinclip 把 Shorts、Reels 和 TikTok 連結連同標題、封面收進同一個地方，整理成你真的會再打開的資料夾。",
        "badge_small": "下載於", "note": "免費下載 · iPHONE &amp; iPAD",
        "badge_aria": "在 App Store 下載",
        "chips": [["▶", "YouTube Shorts"], ["✦", "IG Reels"], ["♪", "TikTok"], ["#", "標籤·備註"]],
        "hero_alt": "Pinclip 主畫面 — 最近儲存的影片和食譜、居家健身、羅馬咖啡廳等資料夾",
        "marquee": ["SHORTS", "REELS", "TIKTOK", "資料夾", "標籤", "備註", "小工具", "iCLOUD 同步"],
        "how_kicker": "使用方式",
        "how_h2": "從「之後再看」，到<em>真的看得到</em>。",
        "steps": [
            ["分享", "在分享面板點 Pinclip", "滑到想留下的影片？點分享 → Pinclip，不用切換 App 就完成。"],
            ["自動", "標題封面自動抓取", "只要給它連結，標題與封面自動填好。不是一堆連結，而是一眼認得的收藏庫。"],
            ["整理", "資料夾·標籤·備註", "放進資料夾，加上 #標籤 和收藏原因。未來的你會感謝現在的你。"],
        ],
        "conv_kicker": "找回", "conv_num": "3 秒",
        "conv_h2": "模糊的印象，變成<em>精準的位置</em>。",
        "conv_lede": "從不打開的收藏只是心理負擔。Pinclip 把「上週看過的那支健身影片」變成一點就到的資料夾和標籤。",
        "conv_rows": [
            ["週二滑到的義大利麵影片", "食譜 · #義大利麵", "YOUTUBE · SHORTS"],
            ["按過讚的穿搭 Reels", "時尚 · #穿搭", "INSTAGRAM · REELS"],
            ["那個棒式挑戰", "居家健身 · #核心", "TIKTOK"],
            ["週末想去的咖啡廳", "羅馬咖啡廳 · #咖啡", "YOUTUBE"],
        ],
        "maps_kicker": "平台", "maps_num": "一個收藏庫",
        "maps_h2": "平台再多，<em>收藏庫只有一個</em>。",
        "maps_lede": "任何能分享連結的 App 都能儲存。YouTube 和 TikTok 連標題封面都自動抓取，全部進到同一個可搜尋的收藏庫。",
        "providers": [
            ["▶", "YouTube Shorts", [["✓", "自動標題"], ["✓", "自動封面"]]],
            ["♪", "TikTok", [["✓", "自動標題"], ["✓", "自動封面"]]],
            ["✦", "IG Reels", [["✓", "一鍵儲存"], ["✓", "智慧資料夾"]]],
            ["∞", "其他影片連結", [["✓", "同一個收藏庫"], ["✓", "標籤搜尋"]]],
        ],
        "shots_kicker": "畫面", "shots_num": "iPHONE &amp; iPAD",
        "shots_h2": "不是為了囤積，是<em>為了找回</em>。",
        "shots_caps": ["資料夾井然有序", "標籤 · 備註 · 一鍵回看", "整個收藏隨手搜"],
        "feat_kicker": "細節", "feat_num": "06",
        "feat_h2": "小 App，<em>講究的</em>細節。",
        "feats": [
            ["分享面板直接儲存", "不離開 YouTube、Instagram 或 TikTok，點兩下，繼續滑。"],
            ["主畫面小工具", "把資料夾或常看的影片釘在主畫面，解鎖到播放只要一步。"],
            ["iCloud 同步", "Pro 透過你自己的 iCloud 同步到 iPad——不經過我們的伺服器。"],
            ["資料夾分享連結", "把資料夾變成一條連結分享。對方在瀏覽器查看，還能匯入自己的 Pinclip。"],
            ["智慧資料夾", "Shorts、Reels、TikTok 依平台自動歸類。"],
            ["標籤與備註", "加上 #標籤 和收藏原因。點一下標籤，相關影片全部出現。"],
        ],
        "final_h2": "別再讓影片消失在動態裡。", "final_lede": "iPhone · iPad 免費。",
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


def badge(loc):
    return (f'<a class="store-badge" href="{APP_STORE_URL}" aria-label="{loc["badge_aria"]}">{APPLE_SVG}'
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
        f'<div class="convert-row"><span>{a}</span><span class="arrow">→</span><span class="to">📁 {b}</span><span class="cat">{c}</span></div>'
        for a, b, c in loc["conv_rows"]
    )
    provs = "".join(
        '<div class="prov"><span class="flag">%s</span><h3>%s</h3><ul>%s</ul></div>'
        % (flag, name, "".join(f'<li><span class="g">{g}</span>{n}</li>' for g, n in items))
        for flag, name, items in loc["providers"]
    )
    shot_files = ["folder", "detail", "feed"]
    shots = "".join(
        f'<figure><div class="phone"><img src="{rel}assets/shot-{loc["shots"]}-{f}.png" alt="{cap}" loading="lazy"><div class="island"></div></div><figcaption>{cap}</figcaption></figure>'
        for f, cap in zip(shot_files, loc["shots_caps"])
    )
    feats = "".join(f'<div class="feat"><h3>{h}</h3><p>{p}</p></div>' for h, p in loc["feats"])
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

<nav>
  <div class="wrap">
    <a class="wordmark" href="{rel if rel else './'}"><img src="{rel}assets/icon-180.png" alt=""><span>PINCLIP</span></a>
    <div class="lang">{lang_nav(loc['dir'], rel)}</div>
  </div>
</nav>

<header class="hero">
  <div class="ghost">P.</div>
  <div class="wrap">
    <div>
      <div class="kicker"><span>PINCLIP</span><span class="rule"></span><span class="num">{loc['kicker_num']}</span></div>
      <h1>{loc['h1']}</h1>
      <div class="demo">
        <span class="src" id="demoSrc">{loc['pairs'][0][0]}</span>
        <span class="arrow">→</span>
        <span class="dst" id="demoDst">{loc['pairs'][0][1]}</span>
      </div>
      <p class="sub">{loc['sub']}</p>
      <div class="cta">
        {badge(loc)}
        <span class="note">{loc['note']}</span>
      </div>
    </div>
    <div class="phone-col">
      {chips}
      <div class="phone"><img src="{rel}assets/shot-{loc['shots']}-home.png" alt="{loc['hero_alt']}"><div class="island"></div></div>
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
    <div class="cta">{badge(loc)}</div>
  </div>
</section>

<footer>
  <div class="wrap">
    <div class="brand"><img src="{rel}assets/icon-180.png" alt=""><a href="/"><strong>kkiruk studio</strong></a></div>
    <div class="links">
      <a href="mailto:kkirukstudio.help@gmail.com">{loc['f_contact']}</a>
      <a href="https://kkiruk-studio.github.io/privacy-policy-app/">{loc['f_privacy']}</a>
      <a href="https://kkiruk-studio.github.io/terms-of-service-app/">{loc['f_terms']}</a>
    </div>
    <div>© 2026 kkiruk studio</div>
  </div>
</footer>

<script>
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
        for (const ch of src) {{ srcEl.textContent += ch; await sleep(55); }}
        await sleep(350);
        dstEl.textContent = dst;
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
