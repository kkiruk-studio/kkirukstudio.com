# PinClip — 숏폼 북마크. 크림+코랄, 비디오 카드 스택에 핀.
from common import build_app

APP = {
    "slug": "pinclip",
    "trackId": "6761982511",
    "rating": None,
    "theme": {"bg": "#FBF6F2", "ink": "#27201B", "ink2": "#9A8C80", "accent": "#E8584A"},
    "hero_html": """    <div class="fanx">
      <img class="shot s1" src="../shots/pinclip/{lang}-2.jpg" alt="">
      <img class="shot s2" src="../shots/pinclip/{lang}-1.jpg" alt="">
      <div class="pin"><i></i></div>
    </div>""",
    "extra_css": """
.fanx { position:relative; width:360px; height:480px; }
.fanx .s1 { position:absolute; width:215px; left:0; top:34px; transform:rotate(-7deg); }
.fanx .s2 { position:absolute; width:225px; left:128px; top:0; transform:rotate(4deg); z-index:2;
  animation:cardfloat 4.5s ease-in-out infinite; }
.pin { position:absolute; z-index:3; left:104px; bottom:54px; width:46px; height:46px; border-radius:50%;
  background:var(--accent); box-shadow:0 10px 24px -6px rgba(232,88,74,.65);
  display:flex; align-items:center; justify-content:center; animation:pindrop 3.2s ease-in-out infinite; }
.pin i { width:14px; height:14px; border-radius:50%; background:#FFF; }
.pin::after { content:""; position:absolute; bottom:-12px; left:50%; transform:translateX(-50%);
  border:8px solid transparent; border-top:13px solid var(--accent); }
@keyframes pindrop { 0%,100% { transform:translateY(0); } 50% { transform:translateY(-8px); } }
@keyframes cardfloat { 0%,100% { transform:rotate(4deg) translateY(0); } 50% { transform:rotate(4deg) translateY(-7px); } }
@media (max-width:520px) { .fanx { transform:scale(.84); margin:-34px 0; } }
""",
}

S = {
"ko": {
    "name": "PinClip", "title": "PinClip — 스쳐 지나간 영상, 3초 만에 다시 찾기",
    "meta_desc": "공유 버튼 한 번으로 영상 링크를 저장하고 폴더로 정리하는 숏폼 북마크 앱. 제목·썸네일 자동, 위젯, iCloud 동기화.",
    "kicker": "Bookmark Reels & Shorts",
    "h1": "그 영상, 어디서 봤더라?<br><em>이제 3초면 찾아요.</em>",
    "sub": "보다가 공유 버튼 한 번 — PinClip이 제목과 썸네일까지 챙겨 폴더에 정리해 둡니다. 유튜브·릴스·쇼츠·틱톡 어디서든.",
    "cta": "App Store에서 받기", "foot": "무료 다운로드 · iPhone & iPad",
    "feat_label": "기능", "feat_title": "저장은 1초, 정리는 자동.",
    "features": [
        ("공유 한 번으로 저장", "어떤 앱에서든 공유 버튼 → PinClip. 그게 끝이에요."),
        ("제목·썸네일 자동", "링크만 던지면 메타데이터는 알아서 채워집니다."),
        ("폴더 + 메모", "주제별 폴더로 분류하고, 영상마다 짧은 메모를."),
        ("위젯 & iCloud", "자주 보는 폴더는 홈 화면에서 한 탭. 모든 기기에서 동기화."),
    ],
    "cta_title": "스쳐 보내지 말고,<br>핀 해두세요.", "cta_sub": "무료로 시작 · iPhone & iPad",
    "f_contact": "문의", "f_privacy": "개인정보 처리방침", "f_terms": "이용약관",
},
"en": {
    "name": "PinClip", "title": "PinClip — Find that video again in 3 seconds",
    "meta_desc": "Bookmark Reels, Shorts, and any video link with one share-sheet tap. Auto titles & thumbnails, folders, widgets, iCloud sync.",
    "kicker": "Bookmark Reels & Shorts",
    "h1": "Where did I see that video?<br><em>Now it takes 3 seconds.</em>",
    "sub": "Tap share while watching — PinClip saves the link with its title and thumbnail, neatly filed in folders. Works with YouTube, Reels, Shorts, TikTok and more.",
    "cta": "Download on the App Store", "foot": "Free download · iPhone & iPad",
    "feat_label": "Features", "feat_title": "Saving takes a second. Filing is automatic.",
    "features": [
        ("One tap to save", "Share button → PinClip, from any app. That's it."),
        ("Auto title & thumbnail", "Drop a link; the metadata fills itself in."),
        ("Folders + notes", "Organize by topic, leave a short note on any clip."),
        ("Widgets & iCloud", "Favorite folders one tap from your Home Screen. Synced everywhere."),
    ],
    "cta_title": "Don't let it scroll away.<br>Pin it.", "cta_sub": "Free to start · iPhone & iPad",
    "f_contact": "Contact", "f_privacy": "Privacy", "f_terms": "Terms",
},
"ja": {
    "name": "PinClip", "title": "PinClip — あの動画、3秒で見つかる",
    "meta_desc": "共有ボタン一回で動画リンクを保存、フォルダで整理するブックマークアプリ。タイトル・サムネ自動、ウィジェット、iCloud同期。",
    "kicker": "Bookmark Reels & Shorts",
    "h1": "あの動画、どこだっけ?<br><em>もう3秒で見つかる。</em>",
    "sub": "見ながら共有ボタンを一回 — PinClipがタイトルとサムネイル付きでフォルダに整理。YouTube・リール・ショート・TikTok、どこからでも。",
    "cta": "App Storeでダウンロード", "foot": "無料ダウンロード · iPhone & iPad",
    "feat_label": "機能", "feat_title": "保存は1秒、整理は自動。",
    "features": [
        ("共有一回で保存", "どのアプリでも共有ボタン → PinClip。それだけ。"),
        ("タイトル・サムネ自動", "リンクを渡せばメタデータは勝手に埋まります。"),
        ("フォルダ + メモ", "テーマ別に分類して、動画ごとに短いメモを。"),
        ("ウィジェット & iCloud", "よく見るフォルダはホーム画面から1タップ。全デバイスで同期。"),
    ],
    "cta_title": "流して忘れる前に、<br>ピンしておこう。", "cta_sub": "無料で始める · iPhone & iPad",
    "f_contact": "お問い合わせ", "f_privacy": "プライバシー", "f_terms": "利用規約",
},
"zh-hans": {
    "name": "PinClip", "title": "PinClip — 那条视频，3秒找回来",
    "meta_desc": "分享按钮一下就能保存视频链接，按文件夹整理的短视频书签应用。自动标题缩略图、小组件、iCloud同步。",
    "kicker": "Bookmark Reels & Shorts",
    "h1": "那条视频在哪看的?<br><em>现在3秒就能找到。</em>",
    "sub": "看到喜欢的就点分享 — PinClip 会带着标题和缩略图，整齐地存进文件夹。YouTube、Reels、Shorts、TikTok 都可以。",
    "cta": "在 App Store 下载", "foot": "免费下载 · iPhone & iPad",
    "feat_label": "功能", "feat_title": "保存只要1秒，整理全自动。",
    "features": [
        ("分享一下就保存", "任何应用里点分享 → PinClip，就这么简单。"),
        ("自动标题缩略图", "丢个链接进来，元数据自动补全。"),
        ("文件夹 + 备注", "按主题分类，每条视频都能留个短备注。"),
        ("小组件 & iCloud", "常看的文件夹放主屏幕一点即达，多设备同步。"),
    ],
    "cta_title": "别让它刷过去，<br>钉住它。", "cta_sub": "免费开始 · iPhone & iPad",
    "f_contact": "联系我们", "f_privacy": "隐私政策", "f_terms": "服务条款",
},
"zh-hant": {
    "name": "PinClip", "title": "PinClip — 那部影片，3秒找回來",
    "meta_desc": "分享按鈕一下就能儲存影片連結、用資料夾整理的短影音書籤 App。自動標題縮圖、小工具、iCloud 同步。",
    "kicker": "Bookmark Reels & Shorts",
    "h1": "那部影片在哪看的?<br><em>現在3秒就找得到。</em>",
    "sub": "看到喜歡的就按分享 — PinClip 會帶著標題和縮圖，整齊地存進資料夾。YouTube、Reels、Shorts、TikTok 都可以。",
    "cta": "在 App Store 下載", "foot": "免費下載 · iPhone & iPad",
    "feat_label": "功能", "feat_title": "儲存只要1秒，整理全自動。",
    "features": [
        ("分享一下就儲存", "任何 App 裡按分享 → PinClip，就這麼簡單。"),
        ("自動標題縮圖", "丟個連結進來，中繼資料自動補齊。"),
        ("資料夾 + 筆記", "按主題分類，每部影片都能留個短筆記。"),
        ("小工具 & iCloud", "常看的資料夾放主畫面一點即達，多裝置同步。"),
    ],
    "cta_title": "別讓它滑過去，<br>釘住它。", "cta_sub": "免費開始 · iPhone & iPad",
    "f_contact": "聯絡我們", "f_privacy": "隱私權政策", "f_terms": "服務條款",
},
}

build_app(APP, S)
