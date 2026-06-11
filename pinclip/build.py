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
CSS_VERSION = "3"  # bump whenever style.css changes — busts stale browser caches

APPLE_SVG = '<svg viewBox="0 0 384 512" aria-hidden="true"><path d="M318.7 268.7c-.2-36.7 16.4-64.4 50-84.8-18.8-26.9-47.2-41.7-84.7-44.6-35.5-2.8-74.3 20.7-88.5 20.7-15 0-49.4-19.7-76.4-19.7C63.3 141.2 4 184.8 4 273.5q0 39.3 14.4 81.2c12.8 36.7 59 126.7 107.2 125.2 25.2-.6 43-17.9 75.8-17.9 31.8 0 48.3 17.9 76.4 17.9 48.6-.7 90.4-82.5 102.6-119.3-65.2-30.7-61.7-90-61.7-91.9zm-56.6-164.2c27.3-32.4 24.8-61.9 24-72.5-24.1 1.4-52 16.4-67.9 34.9-17.5 19.8-27.8 44.3-25.6 71.9 26.1 2 49.9-11.4 69.5-34.3z"/></svg>'

LANG_LABELS = [("", "EN"), ("ko/", "한국어"), ("ja/", "日本語"), ("zh-hans/", "简体"), ("zh-hant/", "繁體")]
PLAT_GLYPH = {"yt": "▶", "tt": "♪", "ig": "✦", "any": "∞"}

LOCALES = {
    "en": {
        "dir": "", "lang": "en", "font": None, "shots": "en",
        "title": "Pinclip — Save Shorts, Reels & TikToks. Find them in 3 seconds.",
        "desc": "Tap share on any short-form video and Pinclip saves it with the title and thumbnail filled in automatically. Folders, tags, widgets and iCloud sync keep your videos organized.",
        "og_title": "Pinclip — Short-form Video Bookmarks",
        "og_desc": "Save the videos you love, so you can find them again.",
        "kicker_num": "📌 The easy way to save short videos",
        "h1": "That video you loved?<br>Save it so you can <em>find it again</em>.",
        "demo_cards": [
            ["yt", "🍝", "5-Minute Pasta Recipe", "Recipes"],
            ["ig", "👗", "Fall Daily Look Outfits", "Fashion"],
            ["tt", "🏋️", "5-Min Plank Challenge", "Home Workout"],
            ["yt", "☕", "Best 7 Cafes in Brooklyn", "NYC Cafes"],
        ],
        "sub": "You watch a Short or a Reel, think “I'll come back to this” — and then it's gone. Pinclip is a place to keep those videos. Tap the share button on any video, choose Pinclip, and that's it: the title and preview picture are added automatically, and everything is sorted into folders.",
        "badge_small": "Download on the", "note": "FREE DOWNLOAD · IPHONE &amp; IPAD",
        "badge_aria": "Download on the App Store",
        "hero_alt": "Pinclip home screen with recently saved videos and folders like Recipes, Home Workout and NYC Cafes",
        "how_kicker": "How it works",
        "how_h2": "It only takes <em>three steps</em>.",
        "steps": [
            ["📤", "Tap the share button on a video", "Watching something on YouTube, Instagram or TikTok that you want to keep? Tap the share (arrow) button below it and choose Pinclip. You never have to leave the app you're in."],
            ["🪄", "Pinclip does the rest for you", "It grabs the video's title and preview picture automatically. You don't have to type anything — your collection ends up looking like a photo album, easy to scan."],
            ["🗂️", "Put it in a folder", "Make folders like “Cooking” or “Workout” and drop videos in. Add tags and a little note, and you'll never forget why you saved something."],
        ],
        "conv_kicker": "Finding it again",
        "conv_h2": "Can't remember the title? <em>Found in 3 seconds</em> anyway.",
        "conv_lede": "“That pasta video from last week…” — you often can't remember the title or the channel. In Pinclip, you just open the folder or tap a tag, and there it is. Like this:",
        "conv_rows": [
            ["yt", "that pasta Short from Tuesday…", "Recipes · #pasta"],
            ["ig", "the outfit Reel I liked…", "Fashion · #ootd"],
            ["tt", "that plank challenge…", "Home Workout · #core"],
            ["yt", "cafes for the weekend…", "NYC Cafes · #brooklyn"],
        ],
        "maps_kicker": "Platforms",
        "maps_h2": "YouTube, TikTok, Instagram — <em>all in one place</em>.",
        "maps_lede": "It doesn't matter which app the video came from — you save them all the same way. YouTube and TikTok videos even fill in their own title and preview picture, and everything you save can be searched in one library.",
        "share_kicker": "Share a folder",
        "share_h2": "Send a whole folder <em>as a single link</em>.",
        "share_lede": "That “NYC Cafes” folder you put together? Too good to keep to yourself. Turn the folder into a link and send it — your friend can see it right in their browser, no app needed. And if they use Pinclip too, they can import the whole folder into their own collection.",
        "share_folder": "NYC Cafes", "share_count": "2 videos",
        "share_friend": "Your friend can:",
        "share_view": "View it right in the browser", "share_import": "Import it into their Pinclip",
        "providers": [
            ["yt", "YouTube Shorts", [["✓", "Auto title"], ["✓", "Auto thumbnail"]]],
            ["tt", "TikTok", [["✓", "Auto title"], ["✓", "Auto thumbnail"]]],
            ["ig", "Instagram Reels", [["✓", "One-tap save"], ["✓", "Smart folders"]]],
            ["any", "Any video link", [["✓", "Same library"], ["✓", "Tag search"]]],
        ],
        "shots_kicker": "Screens",
        "shots_h2": "Here's what it <em>actually looks like</em>.",
        "shots_caps": ["📁 Folders that stay tidy", "🏷️ Tags · notes · one tap back", "🔍 Your whole feed, searchable"],
        "feat_kicker": "More",
        "feat_h2": "It does <em>more</em>, too.",
        "feats": [
            ["📤", "Save without switching apps", "You don't have to close YouTube, Instagram or TikTok. Share button → Pinclip — two taps and you're back to watching."],
            ["📲", "Home Screen widgets", "Put your favorite folders or videos right on your phone's Home Screen. Unlock, tap once, and the video is playing."],
            ["☁️", "iCloud sync", "With Pro, videos you save on your iPhone show up on your iPad too. It syncs through your own iCloud, so it stays private."],
            ["▶️", "Jump back to the original", "Tap a saved video and it opens right where it came from — YouTube, Instagram or TikTok. Watching it again takes one tap."],
            ["🗂️", "Smart folders", "Pinclip automatically groups videos by where they came from — YouTube, Instagram or TikTok. No effort needed."],
            ["#️⃣", "Tags and notes", "Add a tag like #cooking, or a note about why you saved it. Later, tap the tag and every related video shows up."],
        ],
        "final_h2": "Never lose a video again.", "final_lede": "Pinclip is free to start, on iPhone and iPad.",
        "f_contact": "Contact", "f_privacy": "Privacy", "f_terms": "Terms",
    },
    "ko": {
        "dir": "ko/", "lang": "ko", "font": '"Apple SD Gothic Neo", "Pretendard"', "shots": "ko",
        "title": "Pinclip — 쇼츠·릴스 저장, 3초 만에 다시 찾기",
        "desc": "영상의 공유 버튼만 누르면 제목·썸네일까지 자동 저장. 폴더·태그·위젯·iCloud 동기화로 숏폼 영상을 깔끔하게 정리하세요.",
        "og_title": "Pinclip — 숏폼 영상 저장 앱",
        "og_desc": "재밌게 본 영상, 다시 찾을 수 있게 저장하세요.",
        "kicker_num": "📌 숏폼 영상 저장 앱",
        "h1": "재밌게 본 그 영상,<br><em>다시 찾을 수 있게</em> 저장하세요.",
        "demo_cards": [
            ["yt", "🍝", "5분 완성 파스타 레시피", "레시피"],
            ["ig", "👗", "가을 데일리룩 코디", "패션"],
            ["tt", "🏋️", "5분 플랭크 챌린지", "홈트 루틴"],
            ["yt", "☕", "성수동 카페 추천 BEST 7", "서울 카페"],
        ],
        "sub": "쇼츠나 릴스를 보다가 \"이건 나중에 또 봐야지\" 했던 영상, 막상 찾으려면 안 보이죠. Pinclip은 그런 영상을 모아 두는 저장함이에요. 영상의 공유 버튼을 누르고 Pinclip을 선택하면 끝 — 제목과 미리보기 사진이 자동으로 붙고, 폴더에 차곡차곡 정리됩니다.",
        "badge_small": "다운로드는", "note": "무료 다운로드 · iPHONE &amp; iPAD",
        "badge_aria": "App Store에서 다운로드",
        "hero_alt": "Pinclip 홈 화면 — 최근 저장한 영상과 레시피·홈트 루틴·서울 카페 폴더",
        "how_kicker": "사용 방법",
        "how_h2": "사용법은 딱 <em>세 단계</em>예요.",
        "steps": [
            ["📤", "영상에서 공유 버튼을 눌러요", "유튜브·인스타·틱톡에서 영상을 보다가 마음에 들면, 밑에 있는 공유(화살표) 버튼을 누르고 Pinclip을 선택하세요. 보던 앱을 떠날 필요가 없어요."],
            ["🪄", "나머지는 Pinclip이 알아서 해요", "영상의 제목과 미리보기 사진을 자동으로 가져와요. 내가 따로 적지 않아도, 저장함이 사진첩처럼 한눈에 보여요."],
            ["🗂️", "폴더에 넣어서 정리해요", "'요리', '운동'처럼 폴더를 만들어 영상을 넣어 두세요. 태그와 메모까지 달아 두면, 왜 저장했는지도 까먹지 않아요."],
        ],
        "conv_kicker": "다시 찾을 때",
        "conv_h2": "제목이 기억 안 나도 <em>3초면 찾아요</em>.",
        "conv_lede": "\"지난주에 봤던 그 파스타 영상…\" 제목도 채널도 기억나지 않을 때가 많죠. Pinclip에서는 폴더를 열거나 태그 하나만 누르면 바로 나와요. 이렇게요:",
        "conv_rows": [
            ["yt", "화요일에 본 그 파스타 쇼츠…", "레시피 · #파스타"],
            ["ig", "좋아요 누른 코디 릴스…", "패션 · #코디"],
            ["tt", "그 플랭크 챌린지…", "홈트 루틴 · #코어"],
            ["yt", "주말에 갈 카페…", "서울 카페 · #성수동"],
        ],
        "maps_kicker": "플랫폼",
        "maps_h2": "유튜브, 틱톡, 인스타그램 — <em>전부 한곳에</em> 모여요.",
        "maps_lede": "어느 앱에서 보던 영상이든 똑같은 방법으로 저장할 수 있어요. 유튜브와 틱톡 영상은 제목과 미리보기 사진까지 알아서 채워지고, 저장한 영상은 전부 한 저장함에서 검색돼요.",
        "share_kicker": "폴더 공유",
        "share_h2": "모아 둔 폴더, <em>링크 하나로</em> 친구에게 보낼 수 있어요.",
        "share_lede": "열심히 모은 '서울 카페' 폴더, 나만 보기 아깝잖아요. 폴더를 링크로 만들어 보내면, 친구는 앱이 없어도 브라우저에서 바로 볼 수 있어요. 친구도 Pinclip을 쓰고 있다면, 그 폴더를 통째로 자기 저장함에 가져갈 수도 있고요.",
        "share_folder": "서울 카페", "share_count": "영상 2개",
        "share_friend": "받은 친구는:",
        "share_view": "브라우저에서 바로 보기", "share_import": "자기 Pinclip으로 가져가기",
        "providers": [
            ["yt", "유튜브 쇼츠", [["✓", "제목 자동"], ["✓", "썸네일 자동"]]],
            ["tt", "틱톡", [["✓", "제목 자동"], ["✓", "썸네일 자동"]]],
            ["ig", "인스타 릴스", [["✓", "한 탭 저장"], ["✓", "스마트 폴더"]]],
            ["any", "그 외 영상 링크", [["✓", "같은 라이브러리"], ["✓", "태그 검색"]]],
        ],
        "shots_kicker": "화면",
        "shots_h2": "실제 화면은 <em>이렇게 생겼어요</em>.",
        "shots_caps": ["📁 폴더로 깔끔하게", "🏷️ 태그 · 메모 · 원본 열기", "🔍 전체 피드 검색"],
        "feat_kicker": "더 있어요",
        "feat_h2": "이런 것도 <em>돼요</em>.",
        "feats": [
            ["📤", "앱 전환 없이 저장", "유튜브·인스타·틱톡을 끄지 않아도 돼요. 공유 버튼 → Pinclip, 두 번만 누르면 다시 영상으로 돌아가요."],
            ["📲", "홈 화면 위젯", "자주 보는 폴더나 영상을 휴대폰 홈 화면에 붙여 둘 수 있어요. 잠금 풀고 한 번만 누르면 바로 영상이에요."],
            ["☁️", "iCloud 동기화", "Pro를 쓰면 iPhone에서 저장한 영상이 iPad에도 똑같이 나타나요. 내 iCloud로 동기화되니까 안심이에요."],
            ["▶️", "원본 바로 열기", "저장한 영상을 누르면 유튜브·인스타·틱톡의 원본으로 바로 이동해요. 다시 보는 건 탭 한 번이면 돼요."],
            ["🗂️", "스마트 폴더", "유튜브에서 온 영상, 틱톡에서 온 영상을 Pinclip이 알아서 나눠 줘요. 따로 정리하지 않아도 플랫폼별로 모여요."],
            ["#️⃣", "태그와 메모", "영상에 #요리 같은 태그를 붙이고, 저장한 이유를 메모로 남겨 보세요. 나중에 태그만 눌러도 관련 영상이 전부 나와요."],
        ],
        "final_h2": "그 영상, 이제 잃어버리지 마세요.", "final_lede": "Pinclip은 무료로 시작할 수 있어요. iPhone과 iPad에서 쓸 수 있습니다.",
        "f_contact": "문의", "f_privacy": "개인정보 처리방침", "f_terms": "이용약관",
    },
    "ja": {
        "dir": "ja/", "lang": "ja", "font": '"Hiragino Kaku Gothic ProN", "Hiragino Sans", "Yu Gothic"', "shots": "ja",
        "title": "Pinclip — ショート・リールを保存、3秒で見つかる",
        "desc": "動画の共有ボタンを押すだけで、タイトルとサムネイル付きで自動保存。フォルダ・タグ・ウィジェット・iCloud同期でショート動画をすっきり整理。",
        "og_title": "Pinclip — ショート動画の保存アプリ",
        "og_desc": "気に入った動画を、また見つけられるように保存しよう。",
        "kicker_num": "📌 ショート動画をかんたん保存",
        "h1": "気に入ったあの動画、<br><em>また見つけられるように</em>保存しよう。",
        "demo_cards": [
            ["yt", "🍝", "5分で作れるパスタレシピ", "レシピ"],
            ["ig", "👗", "秋のデイリーコーデ", "ファッション"],
            ["tt", "🏋️", "5分プランクチャレンジ", "ホームトレーニング"],
            ["yt", "☕", "京都おすすめカフェ7選", "京都カフェ"],
        ],
        "sub": "ショートやリールを見ていて「あとでまた見よう」と思った動画、いざ探すと見つからないですよね。Pinclip はそんな動画をしまっておく保存箱です。動画の共有ボタンを押して Pinclip を選ぶだけ — タイトルとプレビュー画像は自動でついて、フォルダにきちんと整理されます。",
        "badge_small": "ダウンロードは", "note": "無料ダウンロード · iPHONE &amp; iPAD",
        "badge_aria": "App Store でダウンロード",
        "hero_alt": "Pinclip のホーム画面 — 最近保存した動画とレシピ・ホームトレーニング・京都カフェのフォルダ",
        "how_kicker": "使い方",
        "how_h2": "使い方は、たったの<em>3ステップ</em>。",
        "steps": [
            ["📤", "動画の共有ボタンを押す", "YouTube・Instagram・TikTok で気に入った動画を見つけたら、下にある共有（矢印）ボタンを押して Pinclip を選びます。見ていたアプリを離れる必要はありません。"],
            ["🪄", "あとは Pinclip におまかせ", "動画のタイトルとプレビュー画像を自動で取ってきます。自分で入力しなくても、保存箱はアルバムみたいにひと目で分かります。"],
            ["🗂️", "フォルダに入れて整理する", "「料理」「運動」のようにフォルダを作って動画を入れておきましょう。タグやメモを付けておけば、なぜ保存したかも忘れません。"],
        ],
        "conv_kicker": "見つけるとき",
        "conv_h2": "タイトルを忘れても、<em>3秒で見つかる</em>。",
        "conv_lede": "「先週見たあのパスタの動画…」タイトルもチャンネルも思い出せないこと、ありますよね。Pinclip ならフォルダを開くか、タグをひとつ押すだけ。こんなふうに：",
        "conv_rows": [
            ["yt", "火曜に見たあのパスタ動画…", "レシピ · #パスタ"],
            ["ig", "いいねしたコーデのリール…", "ファッション · #コーデ"],
            ["tt", "あのプランクチャレンジ…", "ホームトレーニング · #体幹"],
            ["yt", "週末に行くカフェ…", "京都カフェ · #嵐山"],
        ],
        "maps_kicker": "プラットフォーム",
        "maps_h2": "YouTube も TikTok も Instagram も、<em>ぜんぶ一か所に</em>。",
        "maps_lede": "どのアプリで見ていた動画でも、同じやり方で保存できます。YouTube と TikTok はタイトルとプレビュー画像まで自動で入って、保存した動画はぜんぶ同じ保存箱から検索できます。",
        "share_kicker": "フォルダを共有",
        "share_h2": "集めたフォルダは、<em>リンクひとつで</em>友だちに送れます。",
        "share_lede": "がんばって集めた「京都カフェ」フォルダ、自分だけで見るのはもったいないですよね。フォルダをリンクにして送れば、友だちはアプリがなくてもブラウザでそのまま見られます。友だちも Pinclip を使っていれば、フォルダごと自分の保存箱に取り込むこともできます。",
        "share_folder": "京都カフェ", "share_count": "動画2本",
        "share_friend": "受け取った友だちは:",
        "share_view": "ブラウザでそのまま見る", "share_import": "自分の Pinclip に取り込む",
        "providers": [
            ["yt", "YouTube ショート", [["✓", "タイトル自動"], ["✓", "サムネイル自動"]]],
            ["tt", "TikTok", [["✓", "タイトル自動"], ["✓", "サムネイル自動"]]],
            ["ig", "インスタ リール", [["✓", "ワンタップ保存"], ["✓", "スマートフォルダ"]]],
            ["any", "その他の動画リンク", [["✓", "同じライブラリ"], ["✓", "タグ検索"]]],
        ],
        "shots_kicker": "画面",
        "shots_h2": "実際の画面は<em>こんな感じ</em>。",
        "shots_caps": ["📁 フォルダですっきり", "🏷️ タグ · メモ · 元リンク", "🔍 フィード全体を検索"],
        "feat_kicker": "ほかにも",
        "feat_h2": "こんなことも<em>できます</em>。",
        "feats": [
            ["📤", "アプリを切り替えずに保存", "YouTube・Instagram・TikTok を閉じなくても保存できます。共有ボタン → Pinclip、2タップで視聴に戻れます。"],
            ["📲", "ホーム画面ウィジェット", "よく見るフォルダや動画をスマホのホーム画面に置いておけます。ロックを解除してワンタップで動画へ。"],
            ["☁️", "iCloud 同期", "Pro なら iPhone で保存した動画が iPad にも同じように表示されます。自分の iCloud 経由だから安心です。"],
            ["▶️", "元の動画へすぐ戻る", "保存した動画をタップすると、YouTube・Instagram・TikTok の元の動画がすぐ開きます。もう一度見るのはワンタップです。"],
            ["🗂️", "スマートフォルダ", "YouTube から来た動画、TikTok から来た動画を Pinclip が自動で仕分けます。何もしなくてもプラットフォーム別にまとまります。"],
            ["#️⃣", "タグとメモ", "#料理 のようなタグや、保存した理由のメモを付けられます。あとでタグを押せば、関連する動画がぜんぶ出てきます。"],
        ],
        "final_h2": "もう動画をなくさない。", "final_lede": "Pinclip は無料で始められます。iPhone と iPad で使えます。",
        "f_contact": "お問い合わせ", "f_privacy": "プライバシーポリシー", "f_terms": "利用規約",
    },
    "zh-hans": {
        "dir": "zh-hans/", "lang": "zh-Hans", "font": '"PingFang SC", "Heiti SC"', "shots": "zh-Hans",
        "title": "Pinclip — 收藏 Shorts、Reels 和 TikTok，3 秒找回",
        "desc": "在视频上点分享按钮就能保存，标题和封面自动抓取。文件夹、标签、小组件和 iCloud 同步，让收藏井井有条。",
        "og_title": "Pinclip — 短视频收藏 App",
        "og_desc": "喜欢的视频存起来，随时找得到。",
        "kicker_num": "📌 最简单的短视频收藏方法",
        "h1": "喜欢的那条视频，<br>存起来，<em>随时找得到</em>。",
        "demo_cards": [
            ["yt", "🍝", "5分钟意面食谱", "食谱"],
            ["ig", "👗", "秋季日常穿搭", "时尚"],
            ["tt", "🏋️", "5分钟平板支撑挑战", "居家健身"],
            ["yt", "☕", "巴黎7家推荐咖啡馆", "巴黎咖啡馆"],
        ],
        "sub": "刷 Shorts 或 Reels 时想着“以后再看”的视频，真要找的时候就不见了。Pinclip 就是放这些视频的收藏箱。在视频上点分享按钮，选 Pinclip，就这么简单 — 标题和预览图自动加上，所有视频整整齐齐地放进文件夹。",
        "badge_small": "下载于", "note": "免费下载 · iPHONE &amp; iPAD",
        "badge_aria": "在 App Store 下载",
        "hero_alt": "Pinclip 主页 — 最近保存的视频和食谱、居家健身、巴黎咖啡馆等文件夹",
        "how_kicker": "使用方法",
        "how_h2": "用法只有<em>三步</em>。",
        "steps": [
            ["📤", "在视频上点分享按钮", "在 YouTube、Instagram 或 TikTok 看到喜欢的视频，点下面的分享（箭头）按钮，选 Pinclip。完全不用离开正在看的应用。"],
            ["🪄", "剩下的交给 Pinclip", "它会自动抓取视频的标题和预览图。你什么都不用打字，收藏箱看起来就像相册一样，一眼就能认出来。"],
            ["🗂️", "放进文件夹整理", "建几个像“做饭”“健身”这样的文件夹，把视频放进去。再加上标签和备注，连当初为什么收藏都不会忘。"],
        ],
        "conv_kicker": "找回的时候",
        "conv_h2": "想不起标题？<em>3 秒也能找到</em>。",
        "conv_lede": "“上周看的那条意面视频……”标题和频道都想不起来，太常见了。在 Pinclip 里，打开文件夹或点一下标签就出来了。像这样：",
        "conv_rows": [
            ["yt", "周二刷到的意面视频…", "食谱 · #意面"],
            ["ig", "点过赞的穿搭 Reels…", "时尚 · #穿搭"],
            ["tt", "那个平板支撑挑战…", "居家健身 · #核心"],
            ["yt", "周末想去的咖啡馆…", "巴黎咖啡馆 · #咖啡"],
        ],
        "maps_kicker": "平台",
        "maps_h2": "YouTube、TikTok、Instagram——<em>全都收在一个地方</em>。",
        "maps_lede": "不管视频来自哪个应用，保存方法都一样。YouTube 和 TikTok 的视频连标题和预览图都自动填好，所有收藏都能在同一个收藏箱里搜索。",
        "share_kicker": "分享文件夹",
        "share_h2": "整理好的文件夹，<em>一条链接</em>就能分享。",
        "share_lede": "辛苦整理的“巴黎咖啡馆”文件夹，只有自己看太可惜了。把文件夹变成链接发出去，朋友不用装应用，在浏览器里就能直接看。如果朋友也在用 Pinclip，还能把整个文件夹导入自己的收藏箱。",
        "share_folder": "巴黎咖啡馆", "share_count": "2 个视频",
        "share_friend": "收到的朋友可以:",
        "share_view": "在浏览器里直接看", "share_import": "导入自己的 Pinclip",
        "providers": [
            ["yt", "YouTube Shorts", [["✓", "自动标题"], ["✓", "自动封面"]]],
            ["tt", "TikTok", [["✓", "自动标题"], ["✓", "自动封面"]]],
            ["ig", "Instagram Reels", [["✓", "一键保存"], ["✓", "智能文件夹"]]],
            ["any", "其他视频链接", [["✓", "同一个收藏库"], ["✓", "标签搜索"]]],
        ],
        "shots_kicker": "界面",
        "shots_h2": "实际界面<em>长这样</em>。",
        "shots_caps": ["📁 文件夹井井有条", "🏷️ 标签 · 备注 · 一键回看", "🔍 整个收藏随手搜"],
        "feat_kicker": "还有更多",
        "feat_h2": "它还能<em>做这些</em>。",
        "feats": [
            ["📤", "不用切换应用就能保存", "不用关掉 YouTube、Instagram 或 TikTok。分享按钮 → Pinclip，点两下就回去继续看。"],
            ["📲", "主屏幕小组件", "把常看的文件夹或视频放到手机主屏幕上。解锁后点一下，视频就开始播了。"],
            ["☁️", "iCloud 同步", "用 Pro 的话，iPhone 上存的视频也会出现在 iPad 上。通过你自己的 iCloud 同步，更放心。"],
            ["▶️", "一键回到原视频", "点一下保存的视频，就会直接打开 YouTube、Instagram 或 TikTok 上的原视频。再看一遍只要一下。"],
            ["🗂️", "智能文件夹", "来自 YouTube 的、来自 TikTok 的，Pinclip 自动帮你分好类。什么都不用做，就按平台整理好了。"],
            ["#️⃣", "标签和备注", "给视频加上 #做饭 这样的标签，写一句为什么收藏。以后点一下标签，相关视频全都出来。"],
        ],
        "final_h2": "别再弄丢视频了。", "final_lede": "Pinclip 免费就能开始用，支持 iPhone 和 iPad。",
        "f_contact": "联系我们", "f_privacy": "隐私政策", "f_terms": "服务条款",
    },
    "zh-hant": {
        "dir": "zh-hant/", "lang": "zh-Hant", "font": '"PingFang TC", "Heiti TC"', "shots": "zh-Hant",
        "title": "Pinclip — 收藏 Shorts、Reels 和 TikTok，3 秒找回",
        "desc": "在影片上點分享按鈕就能儲存，標題與封面自動抓取。資料夾、標籤、小工具與 iCloud 同步，收藏井然有序。",
        "og_title": "Pinclip — 短影音收藏 App",
        "og_desc": "喜歡的影片存起來，隨時找得到。",
        "kicker_num": "📌 最簡單的短影音收藏方法",
        "h1": "喜歡的那支影片，<br>存起來，<em>隨時找得到</em>。",
        "demo_cards": [
            ["yt", "🍝", "5分鐘義大利麵食譜", "食譜"],
            ["ig", "👗", "秋季日常穿搭", "時尚"],
            ["tt", "🏋️", "5分鐘棒式挑戰", "居家健身"],
            ["yt", "☕", "羅馬7家推薦咖啡廳", "羅馬咖啡廳"],
        ],
        "sub": "滑 Shorts 或 Reels 時想著「之後再看」的影片，真要找的時候就不見了。Pinclip 就是放這些影片的收藏箱。在影片上點分享按鈕，選 Pinclip，就這麼簡單 — 標題和預覽圖自動加上，所有影片整整齊齊地放進資料夾。",
        "badge_small": "下載於", "note": "免費下載 · iPHONE &amp; iPAD",
        "badge_aria": "在 App Store 下載",
        "hero_alt": "Pinclip 主畫面 — 最近儲存的影片和食譜、居家健身、羅馬咖啡廳等資料夾",
        "how_kicker": "使用方式",
        "how_h2": "用法只有<em>三步</em>。",
        "steps": [
            ["📤", "在影片上點分享按鈕", "在 YouTube、Instagram 或 TikTok 看到喜歡的影片，點下面的分享（箭頭）按鈕，選 Pinclip。完全不用離開正在看的 App。"],
            ["🪄", "剩下的交給 Pinclip", "它會自動抓取影片的標題和預覽圖。你什麼都不用打字，收藏箱看起來就像相簿一樣，一眼就能認出來。"],
            ["🗂️", "放進資料夾整理", "建幾個像「做菜」「健身」這樣的資料夾，把影片放進去。再加上標籤和備註，連當初為什麼收藏都不會忘。"],
        ],
        "conv_kicker": "找回的時候",
        "conv_h2": "想不起標題？<em>3 秒也找得到</em>。",
        "conv_lede": "「上週看的那支義大利麵影片……」標題和頻道都想不起來，太常見了。在 Pinclip 裡，打開資料夾或點一下標籤就出來了。像這樣：",
        "conv_rows": [
            ["yt", "週二滑到的義大利麵影片…", "食譜 · #義大利麵"],
            ["ig", "按過讚的穿搭 Reels…", "時尚 · #穿搭"],
            ["tt", "那個棒式挑戰…", "居家健身 · #核心"],
            ["yt", "週末想去的咖啡廳…", "羅馬咖啡廳 · #咖啡"],
        ],
        "maps_kicker": "平台",
        "maps_h2": "YouTube、TikTok、Instagram——<em>全都收在同一個地方</em>。",
        "maps_lede": "不管影片來自哪個 App，儲存方法都一樣。YouTube 和 TikTok 的影片連標題和預覽圖都自動填好，所有收藏都能在同一個收藏箱裡搜尋。",
        "share_kicker": "分享資料夾",
        "share_h2": "整理好的資料夾，<em>一條連結</em>就能分享。",
        "share_lede": "辛苦整理的「羅馬咖啡廳」資料夾，只有自己看太可惜了。把資料夾變成連結送出去，朋友不用裝 App，在瀏覽器裡就能直接看。如果朋友也在用 Pinclip，還能把整個資料夾匯入自己的收藏箱。",
        "share_folder": "羅馬咖啡廳", "share_count": "2 支影片",
        "share_friend": "收到的朋友可以:",
        "share_view": "在瀏覽器裡直接看", "share_import": "匯入自己的 Pinclip",
        "providers": [
            ["yt", "YouTube Shorts", [["✓", "自動標題"], ["✓", "自動封面"]]],
            ["tt", "TikTok", [["✓", "自動標題"], ["✓", "自動封面"]]],
            ["ig", "IG Reels", [["✓", "一鍵儲存"], ["✓", "智慧資料夾"]]],
            ["any", "其他影片連結", [["✓", "同一個收藏庫"], ["✓", "標籤搜尋"]]],
        ],
        "shots_kicker": "畫面",
        "shots_h2": "實際畫面<em>長這樣</em>。",
        "shots_caps": ["📁 資料夾井然有序", "🏷️ 標籤 · 備註 · 一鍵回看", "🔍 整個收藏隨手搜"],
        "feat_kicker": "還有更多",
        "feat_h2": "它還能<em>做這些</em>。",
        "feats": [
            ["📤", "不用切換 App 就能儲存", "不用關掉 YouTube、Instagram 或 TikTok。分享按鈕 → Pinclip，點兩下就回去繼續看。"],
            ["📲", "主畫面小工具", "把常看的資料夾或影片放到手機主畫面上。解鎖後點一下，影片就開始播了。"],
            ["☁️", "iCloud 同步", "用 Pro 的話，iPhone 上存的影片也會出現在 iPad 上。透過你自己的 iCloud 同步，更安心。"],
            ["▶️", "一鍵回到原影片", "點一下儲存的影片，就會直接打開 YouTube、Instagram 或 TikTok 上的原影片。再看一遍只要一下。"],
            ["🗂️", "智慧資料夾", "來自 YouTube 的、來自 TikTok 的，Pinclip 自動幫你分好類。什麼都不用做，就依平台整理好了。"],
            ["#️⃣", "標籤與備註", "給影片加上 #做菜 這樣的標籤，寫一句為什麼收藏。之後點一下標籤，相關影片全都出來。"],
        ],
        "final_h2": "別再弄丟影片了。", "final_lede": "Pinclip 免費就能開始用，支援 iPhone 和 iPad。",
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

    first = loc["demo_cards"][0]
    flow = (
        f'<div class="flow" aria-hidden="true">'
        f'<span class="pin" id="flowPin">📌</span>'
        f'<div class="vcard" id="flowCard">'
        f'<span class="thumb t1" id="flowThumb">{first[1]}<span class="pb {first[0]}" id="flowPb">{PLAT_GLYPH[first[0]]}</span></span>'
        f'<span class="t" id="flowTitle">{first[2]}</span>'
        f'</div>'
        f'<span class="arr">→</span>'
        f'<div class="fold" id="flowFold"><span class="ic">📁</span><span id="flowFoldName">{first[3]}</span><span class="cnt" id="flowCnt">4</span></div>'
        f'</div>'
    )

    floats = "".join(
        f'<div class="float-card f{i+1}"><span class="thumb t{i+2} ">{emoji}<span class="pb {plat}">{PLAT_GLYPH[plat]}</span></span><span>{title}</span></div>'
        for i, (plat, emoji, title, _f) in enumerate(loc["demo_cards"][1:4])
    )
    floats += f'<div class="float-chip">📁 {first[3]}</div>'

    steps = "".join(
        f'<div class="step"><span class="n">{i+1}</span><span class="ico">{ico}</span><h3>{h}</h3><p>{p}</p></div>'
        for i, (ico, h, p) in enumerate(loc["steps"])
    )
    mems = "".join(
        f'<div class="mem"><span class="q">“{q}”</span><span class="arr">→</span>'
        f'<span class="dest"><span class="chipf">📁 {dest}</span><span class="pb {plat}">{PLAT_GLYPH[plat]}</span></span></div>'
        for plat, q, dest in loc["conv_rows"]
    )
    provs = "".join(
        '<div class="prov"><span class="pic %s">%s</span><h3>%s</h3><ul>%s</ul></div>'
        % (plat, PLAT_GLYPH[plat], name, "".join(f'<li><span class="g">{g}</span>{n}</li>' for g, n in items))
        for plat, name, items in loc["providers"]
    )
    shot_files = ["folder", "detail", "feed"]
    shots = "".join(
        f'<figure><div class="phone"><img src="{rel}assets/shot-{loc["shots"]}-{f}.png" alt="{cap}" loading="lazy"><div class="island"></div></div><figcaption><span>{cap}</span></figcaption></figure>'
        for f, cap in zip(shot_files, loc["shots_caps"])
    )
    feats = "".join(f'<div class="feat"><span class="ico">{ico}</span><h3>{h}</h3><p>{p}</p></div>' for ico, h, p in loc["feats"])
    share_flow = (
        f'<div class="share-flow" aria-hidden="true">'
        f'<div class="scard sfolder"><span class="ic">📁</span><span><strong>{loc["share_folder"]}</strong><small>{loc["share_count"]}</small></span></div>'
        f'<span class="sarr">→</span>'
        f'<div class="scard slink">🔗 pinclip.link/f/3kx9q2</div>'
        f'<span class="sarr">→</span>'
        f'<div class="scard sfriend"><strong>{loc["share_friend"]}</strong>'
        f'<span>🌐 {loc["share_view"]}</span>'
        f'<span>📲 {loc["share_import"]}</span></div>'
        f'</div>'
    )
    cards_json = json.dumps(loc["demo_cards"], ensure_ascii=False)

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
<link rel="stylesheet" href="{rel}assets/style.css?v={CSS_VERSION}">
{font_override}
</head>
<body>

<nav>
  <div class="wrap">
    <a class="wordmark" href="{rel if rel else './'}"><img src="{rel}assets/icon-180.png" alt="">Pinclip</a>
    <div class="nav-right">
      <div class="lang">{lang_nav(loc['dir'], rel)}</div>
      <a class="nav-cta" href="{APP_STORE_URL}">App Store</a>
    </div>
  </div>
</nav>

<header class="hero">
  <div class="wrap">
    <div>
      <span class="badge-pill">{loc['kicker_num']}</span>
      <h1>{loc['h1']}</h1>
      <p class="sub">{loc['sub']}</p>
      <div class="cta">
        {badge(loc)}
        <span class="note">{loc['note']}</span>
      </div>
      {flow}
    </div>
    <div class="phone-col">
      {floats}
      <div class="phone"><img src="{rel}assets/shot-{loc['shots']}-home.png" alt="{loc['hero_alt']}"><div class="island"></div></div>
    </div>
  </div>
</header>

<section>
  <div class="wrap">
    <span class="badge-pill">{loc['how_kicker']}</span>
    <h2>{loc['how_h2']}</h2>
    <div class="steps">{steps}</div>
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap">
    <span class="badge-pill">{loc['conv_kicker']}</span>
    <h2>{loc['conv_h2']}</h2>
    <p class="lede">{loc['conv_lede']}</p>
    <div class="mems">{mems}</div>
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap">
    <span class="badge-pill">{loc['maps_kicker']}</span>
    <h2>{loc['maps_h2']}</h2>
    <p class="lede">{loc['maps_lede']}</p>
    <div class="providers">{provs}</div>
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap">
    <span class="badge-pill">{loc['share_kicker']}</span>
    <h2>{loc['share_h2']}</h2>
    <p class="lede">{loc['share_lede']}</p>
    {share_flow}
  </div>
</section>

<section class="shots">
  <div class="wrap">
    <span class="badge-pill">{loc['shots_kicker']}</span>
    <h2>{loc['shots_h2']}</h2>
    <div class="row">{shots}</div>
  </div>
</section>

<section>
  <div class="wrap">
    <span class="badge-pill">{loc['feat_kicker']}</span>
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
  const GLYPH = {{ yt: "▶", tt: "♪", ig: "✦" }};
  const cards = {cards_json};
  const card = document.getElementById("flowCard");
  const thumb = document.getElementById("flowThumb");
  const pb = document.getElementById("flowPb");
  const title = document.getElementById("flowTitle");
  const pin = document.getElementById("flowPin");
  const fold = document.getElementById("flowFold");
  const foldName = document.getElementById("flowFoldName");
  const cnt = document.getElementById("flowCnt");
  if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {{
    const sleep = (ms) => new Promise(r => setTimeout(r, ms));
    let i = 0, count = 4;
    (async function loop() {{
      for (;;) {{
        const [plat, emoji, t, folder] = cards[i % cards.length];
        card.classList.add("hidden");
        card.classList.remove("fly");
        card.style.removeProperty("--fly-x");
        pin.classList.remove("stamp");
        thumb.className = "thumb t" + (i % 4 + 1);
        thumb.childNodes[0].nodeValue = emoji;
        pb.className = "pb " + plat;
        pb.textContent = GLYPH[plat];
        title.textContent = t;
        foldName.textContent = folder;
        await sleep(60);
        card.classList.remove("hidden");
        await sleep(950);
        pin.classList.add("stamp");
        await sleep(700);
        const dx = fold.getBoundingClientRect().left - card.getBoundingClientRect().left;
        card.style.setProperty("--fly-x", dx + "px");
        pin.classList.remove("stamp");
        card.classList.add("fly");
        await sleep(600);
        fold.classList.add("bump");
        cnt.textContent = ++count;
        await sleep(420);
        fold.classList.remove("bump");
        await sleep(750);
        i++;
      }}
    }})();
  }} else {{
    pin.classList.add("stamp");
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
