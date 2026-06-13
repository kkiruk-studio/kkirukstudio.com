# 고양이는 정말 팡팡 (Cats are Cute: Pop Time!) — 수박게임식 머지 퍼즐. 피치+비비드, 머지 볼 + 스크린샷.
from common import build_app

HERO = """    <div class="popwrap">
      <div class="fan">
        <img src="../shots/cats-pop/{lang}-1.jpg" alt="">
        <img src="../shots/cats-pop/{lang}-2.jpg" alt="">
        <div class="score">★ 4.8<span>3,900+</span></div>
        <div class="featpill">App Store<span>Featured Story</span></div>
      </div>
      <div class="merge"><i></i><i></i><i></i><i></i><b>!</b></div>
    </div>"""

CSS = """
.popwrap { display:flex; flex-direction:column; align-items:center; gap:26px; }
.fan { position:relative; width:330px; height:400px; }
.fan img { position:absolute; width:200px; border-radius:26px;
  box-shadow:0 26px 60px -18px rgba(63,42,30,.42); border:1px solid rgba(63,42,30,.08); }
.fan img:nth-child(1) { left:6px; top:26px; transform:rotate(-7deg); }
.fan img:nth-child(2) { left:120px; top:0; transform:rotate(5deg); z-index:2; }
.score { position:absolute; right:0; bottom:38px; z-index:3; background:#FFFDF8;
  border:1px solid rgba(63,42,30,.1); border-radius:18px; padding:12px 18px;
  font-size:22px; font-weight:800; color:#FF7A59; box-shadow:0 16px 36px -12px rgba(63,42,30,.3);
  animation:bob 4s ease-in-out infinite; }
.score span { display:block; font-size:11px; font-weight:600; color:#A88D7A; margin-top:1px; }
.featpill { position:absolute; left:-8px; top:18px; z-index:3; background:#3F2A1E; color:#FFF1E4;
  border-radius:14px; padding:9px 14px; font-size:12px; font-weight:800;
  box-shadow:0 14px 32px -10px rgba(63,42,30,.5); animation:bob 4s ease-in-out infinite; animation-delay:1s; }
.featpill span { display:block; font-size:10px; font-weight:600; opacity:.75; margin-top:1px; }
.merge { display:flex; align-items:flex-end; gap:10px; }
.merge i { border-radius:50%; background:linear-gradient(145deg,#FFC93C,#FF7A59);
  animation:pop 2.6s ease-in-out infinite; }
.merge i:nth-child(1) { width:18px; height:18px; }
.merge i:nth-child(2) { width:28px; height:28px; animation-delay:.2s; }
.merge i:nth-child(3) { width:42px; height:42px; animation-delay:.4s; }
.merge i:nth-child(4) { width:60px; height:60px; animation-delay:.6s; }
.merge b { font-size:30px; color:#FF7A59; animation:pop 2.6s ease-in-out infinite; animation-delay:.8s; }
@keyframes pop { 0%,100% { transform:scale(1); } 50% { transform:scale(1.14); } }
@keyframes bob { 0%,100% { transform:translateY(0); } 50% { transform:translateY(-7px); } }
@media (max-width:520px) { .fan { transform:scale(.84); margin:-26px 0; } }
.appstore-btn svg.gp { width:20px; height:20px; }
"""

APP = {
    "slug": "cats-pop",
    "trackId": "1556403381",
    "play_id": "com.game.kkiruk.catsarepop",
    "rating": "4.8 · 3,900+",
    "theme": {"bg": "#FFF1E4", "ink": "#3F2A1E", "ink2": "#A88D7A", "accent": "#FF7A59"},
    "hero_html": HERO,
    "extra_css": CSS,
}

S = {
"ko": {"name": "고양이는 정말 팡팡", "title": "고양이는 정말 팡팡 — 합칠수록 커지는 고양이 머지 퍼즐",
    "meta_desc": "수박게임 스타일의 귀여운 고양이 머지 퍼즐. 11종 진화, 4가지 모드, 90가지 꾸미기, 글로벌 랭킹. ★4.8.",
    "kicker": "Cats are Cute: Pop Time!",
    "h1": "합칠수록 커지는,<br><em>고양이 팡팡!</em>",
    "sub": "수박게임 스타일의 귀여운 고양이 머지 퍼즐. 같은 고양이를 떨어뜨려 합치면 더 큰 고양이로 — 잠깐 쉬어가기 딱 좋은 한 판.",
    "cta": "App Store에서 받기", "cta_play": "Google Play에서 받기", "foot": "오프라인에서도 OK · 인터넷 없이 언제든 한 판",
    "feat_label": "이런 게임이에요", "feat_title": "간단한 조작, 부드러운 사운드, 부담 없는 한 판.",
    "features": [
        ("11종 고양이 진화", "합칠수록 더 귀여워지는 고양이들. 가장 큰 고양이까지 가면 깜짝 놀랄 거예요."),
        ("4가지 모드", "클래식, 스피드, 5분 도전, 1000점 도전 — 기분 따라 골라서."),
        ("90가지 꾸미기", "고양이 액세서리와 배경 테마로 나만의 보드를."),
        ("글로벌 랭킹", "전 세계 플레이어와 점수 경쟁. 오늘의 최고 기록에 도전해보세요."),
    ],
    "cta_title": "가장 큰 고양이까지,<br>가보실래요?", "cta_sub": "무료 다운로드 · iOS & Android",
    "f_contact": "문의", "f_privacy": "개인정보 처리방침", "f_terms": "이용약관"},
"en": {"name": "Cats are Cute: Pop Time!", "title": "Cats are Cute: Pop Time! — The cat merge puzzle that grows",
    "meta_desc": "A cute suika-style cat merge puzzle. 11 evolutions, 4 modes, 90 cosmetics, global rankings. ★4.8.",
    "kicker": "Cats are Cute: Pop Time!",
    "h1": "Merge them and they grow —<br><em>pop pop cats!</em>",
    "sub": "A cute suika-style merge puzzle. Drop matching cats to merge them into bigger ones — the perfect round for a short break.",
    "cta": "Download on the App Store", "cta_play": "Get it on Google Play", "foot": "Works offline · A quick round anytime, no internet needed",
    "feat_label": "What it's like", "feat_title": "Simple controls, soft sounds, zero pressure.",
    "features": [
        ("11 cat evolutions", "Cats get cuter as they merge. Reach the biggest one and you're in for a surprise."),
        ("4 game modes", "Classic, Speed, 5-Minute Challenge, Race to 1000 — pick your mood."),
        ("90 cosmetics", "Cat accessories and board themes to make it yours."),
        ("Global rankings", "Compete with players worldwide. Chase today's high score."),
    ],
    "cta_title": "Think you can reach<br>the biggest cat?", "cta_sub": "Free download · iOS & Android",
    "f_contact": "Contact", "f_privacy": "Privacy", "f_terms": "Terms"},
"ja": {"name": "ねこはほんとポンポン", "title": "ねこはほんとポンポン — 合体するほど大きくなる、ねこマージパズル",
    "meta_desc": "スイカゲーム風のかわいいねこマージパズル。11種の進化、4モード、90種の着せ替え、グローバルランキング。★4.8。",
    "kicker": "Cats are Cute: Pop Time!",
    "h1": "合体するほど大きくなる、<br><em>ねこポンポン!</em>",
    "sub": "スイカゲーム風のかわいいねこマージパズル。同じねこを落として合体させると、もっと大きなねこに — ちょっとした息抜きにぴったりの一局。",
    "cta": "App Storeでダウンロード", "cta_play": "Google Playでダウンロード", "foot": "オフラインOK · ネットなしでもいつでも一局",
    "feat_label": "こんなゲーム", "feat_title": "簡単操作、やさしいサウンド、気軽な一局。",
    "features": [
        ("ねこ11種の進化", "合体するほどかわいくなるねこたち。いちばん大きなねこまで行くと、びっくりしますよ。"),
        ("4つのモード", "クラシック、スピード、5分チャレンジ、1000点チャレンジ — 気分で選んで。"),
        ("90種の着せ替え", "ねこのアクセサリーと背景テーマで自分だけのボードに。"),
        ("グローバルランキング", "世界中のプレイヤーとスコア競争。今日のハイスコアに挑戦。"),
    ],
    "cta_title": "いちばん大きなねこまで、<br>行けますか?", "cta_sub": "無料ダウンロード · iOS & Android",
    "f_contact": "お問い合わせ", "f_privacy": "プライバシー", "f_terms": "利用規約"},
"es": {"name": "Cats are Cute: Pop Time!", "title": "Cats are Cute: Pop Time! — El puzzle de gatos que crecen al fusionarse",
    "meta_desc": "Un adorable puzzle de fusión estilo suika. 11 evoluciones, 4 modos, 90 cosméticos, ranking global. ★4,8.",
    "kicker": "Cats are Cute: Pop Time!",
    "h1": "Fusiónalos y crecen —<br><em>¡pop pop gatos!</em>",
    "sub": "Un adorable puzzle de fusión estilo suika. Deja caer gatos iguales para fusionarlos en otros más grandes — la partida perfecta para un descanso corto.",
    "cta": "Descargar en el App Store", "cta_play": "Descargar en Google Play", "foot": "Funciona sin conexión · Una partida rápida en cualquier momento",
    "feat_label": "Cómo es", "feat_title": "Controles simples, sonidos suaves, cero presión.",
    "features": [
        ("11 evoluciones de gatos", "Los gatos se vuelven más adorables al fusionarse. Llega al más grande y te llevarás una sorpresa."),
        ("4 modos de juego", "Clásico, Velocidad, Reto de 5 minutos, Carrera a 1000 — según tu ánimo."),
        ("90 cosméticos", "Accesorios para gatos y temas de tablero para hacerlo tuyo."),
        ("Ranking global", "Compite con jugadores de todo el mundo. Persigue el récord de hoy."),
    ],
    "cta_title": "¿Llegarás hasta<br>el gato más grande?", "cta_sub": "Descarga gratis · iOS y Android",
    "f_contact": "Contacto", "f_privacy": "Privacidad", "f_terms": "Términos"},
"pt": {"name": "Cats are Cute: Pop Time!", "title": "Cats are Cute: Pop Time! — O puzzle de gatos que crescem ao se fundir",
    "meta_desc": "Um fofo puzzle de fusão estilo suika. 11 evoluções, 4 modos, 90 cosméticos, ranking global. ★4,8.",
    "kicker": "Cats are Cute: Pop Time!",
    "h1": "Funda e eles crescem —<br><em>pop pop gatos!</em>",
    "sub": "Um fofo puzzle de fusão estilo suika. Solte gatos iguais para fundi-los em gatos maiores — a partida perfeita para uma pausa rápida.",
    "cta": "Baixar na App Store", "cta_play": "Baixar no Google Play", "foot": "Funciona offline · Uma partida rápida a qualquer hora",
    "feat_label": "Como é", "feat_title": "Controles simples, sons suaves, zero pressão.",
    "features": [
        ("11 evoluções de gatos", "Os gatos ficam mais fofos ao se fundir. Chegue ao maior e prepare-se para uma surpresa."),
        ("4 modos de jogo", "Clássico, Velocidade, Desafio de 5 minutos, Corrida até 1000 — escolha seu clima."),
        ("90 cosméticos", "Acessórios de gatos e temas de tabuleiro para deixar do seu jeito."),
        ("Ranking global", "Compita com jogadores do mundo todo. Persiga o recorde de hoje."),
    ],
    "cta_title": "Consegue chegar<br>ao maior gato?", "cta_sub": "Download grátis · iOS e Android",
    "f_contact": "Contato", "f_privacy": "Privacidade", "f_terms": "Termos"},
"zh-hans": {"name": "猫真的很砰砰", "title": "猫真的很砰砰 — 越合越大的猫咪合成拼图",
    "meta_desc": "西瓜游戏风格的可爱猫咪合成拼图。11种进化、4种模式、90种装扮、全球排行。★4.8。",
    "kicker": "Cats are Cute: Pop Time!",
    "h1": "越合越大，<br><em>猫咪砰砰!</em>",
    "sub": "西瓜游戏风格的可爱猫咪合成拼图。把相同的猫咪合在一起，变成更大的猫 — 适合小憩一下的轻松一局。",
    "cta": "在 App Store 下载", "cta_play": "在 Google Play 下载", "foot": "支持离线 · 没网也能随时来一局",
    "feat_label": "游戏特色", "feat_title": "操作简单，音效柔和，毫无压力。",
    "features": [
        ("11种猫咪进化", "越合越可爱的猫咪们。合到最大的那只，你会大吃一惊。"),
        ("4种模式", "经典、极速、5分钟挑战、1000分挑战 — 看心情选。"),
        ("90种装扮", "猫咪配饰和背景主题，打造专属棋盘。"),
        ("全球排行榜", "和全世界玩家比分数，挑战今日最高纪录。"),
    ],
    "cta_title": "敢挑战<br>最大的猫吗?", "cta_sub": "免费下载 · iOS & Android",
    "f_contact": "联系我们", "f_privacy": "隐私政策", "f_terms": "服务条款"},
"zh-hant": {"name": "貓咪真的很砰砰", "title": "貓咪真的很砰砰 — 越合越大的貓咪合成拼圖",
    "meta_desc": "西瓜遊戲風格的可愛貓咪合成拼圖。11種進化、4種模式、90種裝扮、全球排行。★4.8。",
    "kicker": "Cats are Cute: Pop Time!",
    "h1": "越合越大，<br><em>貓咪砰砰!</em>",
    "sub": "西瓜遊戲風格的可愛貓咪合成拼圖。把相同的貓咪合在一起，變成更大的貓 — 適合小歇一下的輕鬆一局。",
    "cta": "在 App Store 下載", "cta_play": "在 Google Play 下載", "foot": "支援離線 · 沒網路也能隨時來一局",
    "feat_label": "遊戲特色", "feat_title": "操作簡單，音效柔和，毫無壓力。",
    "features": [
        ("11種貓咪進化", "越合越可愛的貓咪們。合到最大的那隻，你會大吃一驚。"),
        ("4種模式", "經典、極速、5分鐘挑戰、1000分挑戰 — 看心情選。"),
        ("90種裝扮", "貓咪配飾和背景主題，打造專屬棋盤。"),
        ("全球排行榜", "和全世界玩家比分數，挑戰今日最高紀錄。"),
    ],
    "cta_title": "敢挑戰<br>最大的貓嗎?", "cta_sub": "免費下載 · iOS & Android",
    "f_contact": "聯絡我們", "f_privacy": "隱私權政策", "f_terms": "服務條款"},
}

build_app(APP, S)
