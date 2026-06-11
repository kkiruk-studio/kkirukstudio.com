# Talk Memo — 워치 한 탭 아이디어 캡처. 웜 크림+오렌지, 워치 파형→텍스트 히어로.
from common import build_app

APP = {
    "slug": "talkmemo",
    "trackId": "6764329223",
    "rating": None,
    "theme": {"bg": "#F8F3E9", "ink": "#2B231A", "ink2": "#9C8C77", "accent": "#E07A33"},
    "hero_html": """    <div class="tm">
      <div class="watch">
        <span class="rec"></span>
        <div class="wave"><i></i><i></i><i></i><i></i><i></i></div>
        <span class="crown"></span>
      </div>
      <span class="flow">→</span>
      <div class="note">
        <div class="nl" style="width:84%"></div>
        <div class="nl" style="width:68%"></div>
        <div class="nl" style="width:76%"></div>
        <div class="nl s" style="width:42%"></div>
      </div>
    </div>""",
    "extra_css": """
.tm { display:flex; align-items:center; gap:20px; }
.watch { width:148px; height:182px; border-radius:42px; background:#221C15; border:6px solid #3C3327;
  position:relative; display:flex; align-items:center; justify-content:center;
  box-shadow:0 24px 56px -18px rgba(43,35,26,.45); }
.watch .crown { position:absolute; right:-12px; top:46px; width:7px; height:26px; border-radius:4px; background:#3C3327; }
.rec { position:absolute; top:20px; width:13px; height:13px; border-radius:50%; background:#E0452F;
  animation:blink 1.6s ease-in-out infinite; }
.wave { display:flex; align-items:center; gap:5px; height:54px; }
.wave i { width:6px; border-radius:4px; background:var(--accent); animation:wv 1.05s ease-in-out infinite; }
.wave i:nth-child(1) { height:18px; } .wave i:nth-child(2) { height:38px; animation-delay:.12s; }
.wave i:nth-child(3) { height:52px; animation-delay:.24s; } .wave i:nth-child(4) { height:34px; animation-delay:.36s; }
.wave i:nth-child(5) { height:20px; animation-delay:.48s; }
.flow { font-size:24px; color:var(--ink2); }
.note { width:200px; background:#FFFDF8; border:1px solid rgba(43,35,26,.1); border-radius:22px; padding:22px 20px;
  box-shadow:0 22px 50px -20px rgba(43,35,26,.3); }
.nl { height:10px; border-radius:5px; background:rgba(43,35,26,.16); margin:11px 0; animation:appear 4.2s ease infinite; }
.nl:nth-child(2) { animation-delay:.35s; } .nl:nth-child(3) { animation-delay:.7s; } .nl:nth-child(4) { animation-delay:1.05s; }
.nl.s { opacity:.6; }
@keyframes wv { 0%,100% { transform:scaleY(.55); } 50% { transform:scaleY(1); } }
@keyframes blink { 0%,100% { opacity:1; } 50% { opacity:.35; } }
@keyframes appear { 0% { opacity:0; transform:translateX(-5px); } 18%,100% { opacity:1; transform:translateX(0); } }
@media (max-width:520px) { .tm { flex-direction:column; } .flow { transform:rotate(90deg); } }
""",
}

S = {
"ko": {
    "name": "Talk Memo", "title": "Talk Memo — 손목에서 녹음, iPhone에 텍스트로",
    "meta_desc": "Apple Watch 한 탭으로 생각을 녹음하면 iPhone에 텍스트로 도착. 한 번 결제 평생 사용, 구독·광고 없음. Notion·Bear·Obsidian 내보내기.",
    "kicker": "Voice on Watch, text on iPhone",
    "h1": "손목에서 한 탭,<br><em>생각이 텍스트로.</em>",
    "sub": "러닝 중에, 운전 중에, 설거지 중에 — 좋은 생각은 폰을 꺼내는 사이 사라지죠. 워치를 탭하고 말하세요. iPhone에 텍스트로 도착해 있습니다.",
    "cta": "App Store에서 받기",
    "foot": "한 번 결제, 평생 사용 · 구독 없음 · 광고 없음 · 추적 없음",
    "feat_label": "기능", "feat_title": "흐름을 끊지 않는 캡처.",
    "features": [
        ("워치 한 탭", "화면 탭으로 녹음 시작, 다시 탭하면 끝. 폰은 주머니에 그대로."),
        ("자동 텍스트 변환", "녹음은 iPhone으로 자동 전송되고, 기기 안에서 텍스트가 됩니다. 서버로 나가지 않아요."),
        ("원하는 곳으로", "Notion, Bear, Obsidian — 쓰시는 노트 앱으로 깔끔하게 내보내기."),
        ("시작 방법 4가지", "Ultra 액션 버튼, 워치 페이스 콤플리케이션, 도크, Siri·단축어까지."),
    ],
    "cta_title": "다음 좋은 생각은<br>놓치지 마세요.",
    "cta_sub": "한 번 결제 · 평생 사용 · Apple Watch + iPhone",
    "f_contact": "문의", "f_privacy": "개인정보 처리방침", "f_terms": "이용약관",
},
"en": {
    "name": "Talk Memo", "title": "Talk Memo — Voice on Watch, text on iPhone",
    "meta_desc": "Tap your Apple Watch, speak your idea — it arrives on iPhone as text. One-time purchase, no subscription, no ads. Export to Notion, Bear, Obsidian.",
    "kicker": "Voice on Watch, text on iPhone",
    "h1": "One tap on your wrist.<br><em>Ideas become text.</em>",
    "sub": "Mid-run, mid-drive, mid-dishes — good ideas vanish while you dig out your phone. Tap your watch and speak. It's waiting on your iPhone as text.",
    "cta": "Download on the App Store",
    "foot": "One-time purchase · No subscription · No ads · No tracking",
    "feat_label": "Features", "feat_title": "Capture without breaking flow.",
    "features": [
        ("One tap on the watch", "Tap to record, tap to stop. Your phone stays in your pocket."),
        ("Automatic transcription", "Recordings sync to iPhone and become text on-device. Nothing leaves your phone."),
        ("Send it anywhere", "Clean export to Notion, Bear, Obsidian — whatever notes app you live in."),
        ("Four ways to start", "Ultra Action Button, watch-face complication, the Dock, or Siri & Shortcuts."),
    ],
    "cta_title": "Don't lose<br>your next good idea.",
    "cta_sub": "Pay once · Yours forever · Apple Watch + iPhone",
    "f_contact": "Contact", "f_privacy": "Privacy", "f_terms": "Terms",
},
"ja": {
    "name": "Talk Memo", "title": "Talk Memo — 手首で録音、iPhoneにテキストで",
    "meta_desc": "Apple Watchをタップして話すだけ、iPhoneにテキストで届く。買い切り、サブスクなし、広告なし。Notion・Bear・Obsidianへ書き出し。",
    "kicker": "Voice on Watch, text on iPhone",
    "h1": "手首でワンタップ、<br><em>ひらめきがテキストに。</em>",
    "sub": "ランニング中、運転中、皿洗い中 — いいアイデアはスマホを取り出す間に消えてしまう。ウォッチをタップして話すだけ。iPhoneにテキストで届いています。",
    "cta": "App Storeでダウンロード",
    "foot": "買い切り · サブスクなし · 広告なし · トラッキングなし",
    "feat_label": "機能", "feat_title": "流れを止めないキャプチャ。",
    "features": [
        ("ウォッチをワンタップ", "タップで録音開始、もう一度タップで終了。スマホはポケットの中のまま。"),
        ("自動テキスト変換", "録音はiPhoneに自動転送され、デバイス内でテキストに。外部サーバーには送りません。"),
        ("好きな場所へ", "Notion、Bear、Obsidian — お使いのノートアプリへきれいに書き出し。"),
        ("始め方は4通り", "Ultraのアクションボタン、文字盤コンプリケーション、Dock、Siri・ショートカット。"),
    ],
    "cta_title": "次のひらめきを<br>逃さないで。",
    "cta_sub": "買い切り · ずっと使える · Apple Watch + iPhone",
    "f_contact": "お問い合わせ", "f_privacy": "プライバシー", "f_terms": "利用規約",
},
}

build_app(APP, S)
