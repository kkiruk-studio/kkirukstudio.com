# Honest Camera — 토들러 카메라. 선샤인 옐로 풀배경, 거대 셔터, "의도적으로 뺀 것" 섹션.
from common import build_app

APP = {
    "slug": "honestcamera",
    "trackId": "6766827649",
    "rating": None,
    "theme": {"bg": "#FFD23F", "ink": "#211B0E", "ink2": "#7A6A3A", "accent": "#E84545",
              "card": "rgba(255,253,246,.55)", "border": "rgba(33,27,14,.14)"},
    "hero_html": """    <div class="hchero">
      <img class="shot" src="../shots/honestcamera/{lang}-1.jpg" alt="">
      <div class="cam">
        <span class="shutter"></span>
        <div class="lens"><i></i><b></b></div>
        <span class="dotled"></span>
      </div>
    </div>""",
    "extra_css": """
.hchero { position:relative; width:380px; height:520px; }
.hchero > .shot { position:absolute; width:250px; right:10px; top:0;
  box-shadow:10px 12px 0 rgba(33,27,14,.16); border:3px solid var(--ink); border-radius:30px; }
.cam { position:absolute; left:0; bottom:44px; width:196px; height:136px; background:#FFFDF6;
  border-radius:26px; border:3.5px solid var(--ink);
  box-shadow:8px 10px 0 rgba(33,27,14,.18); animation:camfloat 4.5s ease-in-out infinite; }
.lens { width:62px; height:62px; border-radius:50%; background:var(--ink);
  position:absolute; left:50%; top:50%; transform:translate(-50%,-50%);
  display:flex; align-items:center; justify-content:center; }
.lens i { width:36px; height:36px; border-radius:50%; background:#3A4754; display:block; }
.lens b { position:absolute; width:11px; height:11px; border-radius:50%; background:rgba(255,255,255,.7);
  top:11px; right:12px; }
.shutter { position:absolute; top:-22px; right:26px; width:50px; height:34px; border-radius:14px 14px 4px 4px;
  background:var(--bg); border:3.5px solid var(--ink); animation:press 2.4s ease-in-out infinite; }
.dotled { position:absolute; top:14px; left:18px; width:10px; height:10px; border-radius:50%;
  background:var(--accent); animation:led 2.4s ease-in-out infinite; }
@keyframes press { 0%,100% { transform:translateY(0); } 8%,14% { transform:translateY(6px); } 22% { transform:translateY(0); } }
@keyframes led { 0%,100% { opacity:.35; } 10%,16% { opacity:1; } }
@keyframes camfloat { 0%,100% { transform:translateY(0); } 50% { transform:translateY(-8px); } }
@media (max-width:520px) { .hchero { transform:scale(.82); margin:-44px 0; } }
""",
}

S = {
"ko": {
    "name": "Honest Camera", "title": "Honest Camera — 셔터 하나뿐인, 아이의 첫 카메라",
    "meta_desc": "3세부터 혼자 쓰는 가장 단순한 카메라. 큰 노란 버튼 하나, 자동 저장, 모드 전환·인앱결제·광고 없음.",
    "kicker": "My First Camera",
    "h1": "버튼 하나.<br><em>그게 전부.</em>",
    "sub": "3세 아이가 혼자 다룰 수 있는 가장 단순한 카메라. 누르면 찍히고, 찍으면 바로 사진 보관함으로. 실수로 빠져나갈 화면 자체가 없습니다.",
    "cta": "App Store에서 받기", "foot": "iPhone & iPad · 만 3세부터",
    "feat_label": "기능", "feat_title": "아이 손에 맞춰 만들었습니다.",
    "features": [
        ("큰 노란 셔터 하나", "작은 손가락과 부정확한 터치에 맞춘 크기. 누르면 찰칵, 끝."),
        ("미리보기 = 결과", "필터도 AI 보정도 없이, 아이가 본 그대로 저장됩니다."),
        ("바로 사진 보관함으로", "찍는 즉시 자동 저장. 부모 폰의 앨범에서 함께 봐요."),
        ("가이드 액세스 안내", "아이가 다른 앱으로 못 빠져나가게 잠그는 방법을 온보딩에서 단계별로."),
    ],
    "anti_label": "정직한 카메라", "anti_title": "없는 게 기능입니다.",
    "anti_items": ["앱 내 갤러리 탐색", "필터 · 스티커 · AI 효과", "동영상 녹화", "인앱 결제 · 광고", "계정 · 클라우드", "아이를 추적하는 분석"],
    "cta_title": "아이의 눈에 보이는 세상,<br>그대로 찍게 해주세요.",
    "cta_sub": "iPhone & iPad · 복잡한 건 전부 뺐습니다",
    "f_contact": "문의", "f_privacy": "개인정보 처리방침", "f_terms": "이용약관",
},
"en": {
    "name": "Honest Camera", "title": "Honest Camera — One shutter. A toddler's first camera.",
    "meta_desc": "The simplest camera a 3-year-old can use alone. One big yellow button, auto-save, no modes, no IAP, no ads.",
    "kicker": "My First Camera",
    "h1": "One button.<br><em>That's everything.</em>",
    "sub": "The simplest camera a three-year-old can handle alone. Press, it snaps; snap, it saves. There's no screen to accidentally wander into.",
    "cta": "Download on the App Store", "foot": "iPhone & iPad · Ages 3+",
    "feat_label": "Features", "feat_title": "Built for little hands.",
    "features": [
        ("One big yellow shutter", "Sized for small fingers and imprecise taps. Press — click — done."),
        ("Preview = result", "No filters, no AI touch-ups. What your kid sees is what gets saved."),
        ("Straight to Photos", "Every shot auto-saves instantly. Browse them together on your phone."),
        ("Guided Access walkthrough", "Step-by-step onboarding shows you how to lock the app so kids can't wander off."),
    ],
    "anti_label": "An honest camera", "anti_title": "What's missing is the feature.",
    "anti_items": ["In-app gallery browsing", "Filters · stickers · AI effects", "Video recording", "In-app purchases · ads", "Accounts · cloud", "Analytics that track your kid"],
    "cta_title": "The world through their eyes —<br>let them shoot it as-is.",
    "cta_sub": "iPhone & iPad · Everything complicated, removed",
    "f_contact": "Contact", "f_privacy": "Privacy", "f_terms": "Terms",
},
"ja": {
    "name": "Honest Camera", "title": "Honest Camera — シャッターひとつ、こどもの初めてのカメラ",
    "meta_desc": "3歳からひとりで使える、いちばんシンプルなカメラ。大きな黄色いボタンひとつ、自動保存。モード切替・課金・広告なし。",
    "kicker": "My First Camera",
    "h1": "ボタンはひとつ。<br><em>それがすべて。</em>",
    "sub": "3歳の子がひとりで扱える、いちばんシンプルなカメラ。押せば撮れて、撮ればすぐ写真アプリへ。間違って迷い込む画面がそもそもありません。",
    "cta": "App Storeでダウンロード", "foot": "iPhone & iPad · 3歳から",
    "feat_label": "機能", "feat_title": "小さな手に合わせて作りました。",
    "features": [
        ("大きな黄色いシャッター", "小さな指と不正確なタッチに合わせたサイズ。押せばカシャッ、それだけ。"),
        ("プレビュー = 結果", "フィルターもAI補正もなし。子どもが見たままが保存されます。"),
        ("すぐ写真アプリへ", "撮った瞬間に自動保存。あとで親のスマホで一緒に見られます。"),
        ("ガイドアクセス案内", "他のアプリへ抜け出せないようロックする方法を、オンボーディングでステップごとに。"),
    ],
    "anti_label": "正直なカメラ", "anti_title": "「ない」のが機能です。",
    "anti_items": ["アプリ内ギャラリー", "フィルター · ステッカー · AI効果", "動画撮影", "アプリ内課金 · 広告", "アカウント · クラウド", "子どもを追跡する分析"],
    "cta_title": "こどもの目に映る世界を、<br>そのまま撮らせてあげて。",
    "cta_sub": "iPhone & iPad · 複雑なものは全部抜きました",
    "f_contact": "お問い合わせ", "f_privacy": "プライバシー", "f_terms": "利用規約",
},
"zh-hant": {
    "name": "Honest Camera", "title": "Honest Camera — 只有一顆快門，孩子的第一台相機",
    "meta_desc": "3歲就能獨自使用的最簡單相機。一顆大大的黃色按鈕、自動儲存。沒有模式切換、內購、廣告。",
    "kicker": "My First Camera",
    "h1": "一顆按鈕。<br><em>就是全部。</em>",
    "sub": "3歲孩子能獨自操作的最簡單相機。按下就拍，拍了就存進照片。根本沒有會讓孩子迷路的畫面。",
    "cta": "在 App Store 下載", "foot": "iPhone & iPad · 3歲以上",
    "feat_label": "功能", "feat_title": "為小小的手設計。",
    "features": [
        ("一顆大大的黃色快門", "為小手指和不精準的觸碰設計的尺寸。按下喀嚓，就這樣。"),
        ("預覽 = 成品", "沒有濾鏡、沒有AI修圖。孩子看到什麼，就存下什麼。"),
        ("直接存入照片", "拍下立刻自動儲存，之後在爸媽的手機上一起看。"),
        ("引導使用模式教學", "新手引導會一步步教你鎖定 App，孩子跑不出去。"),
    ],
    "anti_label": "誠實的相機", "anti_title": "「沒有」就是功能。",
    "anti_items": ["App 內相簿瀏覽", "濾鏡 · 貼紙 · AI 效果", "錄影", "內購 · 廣告", "帳號 · 雲端", "追蹤孩子的分析工具"],
    "cta_title": "孩子眼中的世界，<br>讓他原樣拍下來。",
    "cta_sub": "iPhone & iPad · 複雜的東西全拿掉了",
    "f_contact": "聯絡我們", "f_privacy": "隱私權政策", "f_terms": "服務條款",
},
}

build_app(APP, S)
