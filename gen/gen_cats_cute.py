# 고양이는 정말 귀여워 (Cats are Cute) — 힐링 수집 시뮬. 웜 크림+핑크, 실제 스크린샷 + ★4.9 소셜프루프.
from common import build_app

SHOTS = """    <div class="fan">
      <img src="../shots/cats-cute/{lang}-1.jpg" alt="">
      <img src="../shots/cats-cute/{lang}-2.jpg" alt="">
      <img src="../shots/cats-cute/{lang}-3.jpg" alt="">
      <div class="score">★ 4.9<span>180,000+</span></div>
    </div>"""

FAN_CSS = """
.fan { position:relative; width:360px; height:440px; }
.fan img { position:absolute; width:195px; border-radius:26px;
  box-shadow:0 26px 60px -18px rgba(74,59,42,.4); border:1px solid rgba(74,59,42,.08); }
.fan img:nth-child(1) { left:0; top:36px; transform:rotate(-8deg); }
.fan img:nth-child(2) { left:140px; top:0; transform:rotate(5deg); z-index:2; }
.fan img:nth-child(3) { left:64px; top:110px; transform:rotate(-1deg); z-index:3; }
.score { position:absolute; right:-4px; bottom:46px; z-index:4; background:#FFFDF8;
  border:1px solid rgba(74,59,42,.1); border-radius:18px; padding:12px 18px;
  font-size:22px; font-weight:800; color:#E8839B; box-shadow:0 16px 36px -12px rgba(74,59,42,.3);
  animation:bob 4s ease-in-out infinite; }
.score span { display:block; font-size:11px; font-weight:600; color:#9A8870; margin-top:1px; }
@keyframes bob { 0%,100% { transform:translateY(0); } 50% { transform:translateY(-7px); } }
@media (max-width:520px) { .fan { transform:scale(.82); margin:-30px 0; } }
"""

APP = {
    "slug": "cats-cute",
    "trackId": "1395888987",
    "rating": "4.9 · 180,000+",
    "theme": {"bg": "#FBF2E4", "ink": "#4A3B2A", "ink2": "#9A8870", "accent": "#E8839B"},
    "hero_html": SHOTS,
    "extra_css": FAN_CSS,
}

S = {
"ko": {"name": "고양이는 정말 귀여워", "title": "고양이는 정말 귀여워 — 고양이 수집 힐링 마을",
    "meta_desc": "고양이를 모으고 마을을 꾸미는 힐링 방치 시뮬레이션. 짧게 켜도 충분하고 보상은 알아서 쌓여요. ★4.9 · 71,000+ 리뷰.",
    "kicker": "Cats are Cute",
    "h1": "고양이를 모으면,<br><em>마을이 자라요.</em>",
    "sub": "잔잔한 힐링 방치 시뮬레이션. 짧게 켜도 충분히 진행되고, 시간이 지나면 보상이 알아서 쌓입니다. 광고는 보고 싶을 때만.",
    "cta": "App Store에서 받기", "foot": "2018년부터 7년 · iOS·Android 누적 1,000만+ 다운로드",
    "feat_label": "이런 게임이에요", "feat_title": "복잡한 조작 없이, 가만히 바라보는 마을.",
    "features": [
        ("다양한 고양이 수집", "표정도 성격도 다른 고양이들. 모을수록 마을이 풍성해지고 새 장소가 열려요."),
        ("나만의 마을 꾸미기", "건물을 업그레이드하고 장식으로 고양이들의 공간을 채워주세요."),
        ("방치해도 괜찮아요", "게임을 꺼도 시간이 지나면 자동으로 진행. 출퇴근길, 잠들기 전 잠깐이면 충분해요."),
        ("강제 광고 없음", "광고가 끼어들지 않아요. 보상이 필요할 때만, 내가 선택해서."),
    ],
    "cta_title": "오늘도 고양이들이<br>기다리고 있어요.", "cta_sub": "무료 다운로드 · iOS & Android",
    "f_contact": "문의", "f_privacy": "개인정보 처리방침", "f_terms": "이용약관"},
"en": {"name": "Cats are Cute", "title": "Cats are Cute — A healing village of collectible cats",
    "meta_desc": "A calm idle game where you collect cats and grow a cozy village. Short sessions are enough; rewards stack on their own. ★4.9 · 71,000+ reviews.",
    "kicker": "Cats are Cute",
    "h1": "Collect cats,<br><em>watch your village grow.</em>",
    "sub": "A calm, healing idle sim. A short session is plenty — rewards keep stacking while you're away. Ads only when you choose to watch.",
    "cta": "Download on the App Store", "foot": "Since 2018 · 10M+ downloads across iOS & Android",
    "feat_label": "What it's like", "feat_title": "No tricky controls. Just a village to gaze at.",
    "features": [
        ("Collect all kinds of cats", "Each with its own face and personality. The more you collect, the richer your village grows."),
        ("Decorate your village", "Upgrade buildings and fill the cats' world with cozy decorations."),
        ("Idle-friendly", "Progress continues while the app is closed. Commutes and bedtime minutes are plenty."),
        ("No forced ads", "Nothing interrupts you. Watch ads only when you want the bonus."),
    ],
    "cta_title": "The cats are waiting<br>for you today, too.", "cta_sub": "Free download · iOS & Android",
    "f_contact": "Contact", "f_privacy": "Privacy", "f_terms": "Terms"},
"ja": {"name": "ねこはほんとかわいい", "title": "ねこはほんとかわいい — ねこを集める癒やしの村",
    "meta_desc": "ねこを集めて村を育てる癒やしの放置シミュレーション。短時間でも十分、報酬は勝手に貯まる。★4.9 · 71,000+ レビュー。",
    "kicker": "Cats are Cute",
    "h1": "ねこを集めると、<br><em>村が育つ。</em>",
    "sub": "穏やかな癒やしの放置シム。短く開くだけで十分、離れている間も報酬は勝手に貯まります。広告は見たいときだけ。",
    "cta": "App Storeでダウンロード", "foot": "2018年から7年 · iOS·Android累計1,000万+ダウンロード",
    "feat_label": "こんなゲーム", "feat_title": "難しい操作なし。ただ眺めたくなる村。",
    "features": [
        ("いろんなねこを集める", "表情も性格もちがうねこたち。集めるほど村がにぎやかになり、新しい場所が開きます。"),
        ("自分だけの村づくり", "建物をアップグレードして、デコレーションでねこたちの空間を。"),
        ("放置でも大丈夫", "アプリを閉じても時間で自動進行。通勤や寝る前の数分で十分。"),
        ("強制広告なし", "広告は割り込みません。ボーナスがほしいときだけ、自分で選んで。"),
    ],
    "cta_title": "今日もねこたちが<br>待っています。", "cta_sub": "無料ダウンロード · iOS & Android",
    "f_contact": "お問い合わせ", "f_privacy": "プライバシー", "f_terms": "利用規約"},
"zh-hans": {"name": "猫真的很可爱", "title": "猫真的很可爱 — 收集猫咪的治愈小村",
    "meta_desc": "收集猫咪、装扮小村的治愈放置游戏。开一小会儿就够，奖励自动累积。★4.9 · 71,000+ 评论。",
    "kicker": "Cats are Cute",
    "h1": "收集猫咪，<br><em>小村慢慢长大。</em>",
    "sub": "安静治愈的放置模拟。开一小会儿就足够，离开时奖励也在自动累积。广告只在你想看时出现。",
    "cta": "在 App Store 下载", "foot": "2018年至今 · iOS·Android 累计下载超1000万",
    "feat_label": "游戏特色", "feat_title": "不需要复杂操作，静静看着就好。",
    "features": [
        ("收集各种猫咪", "每只猫表情性格都不同。收集越多，小村越热闹，新场所也会解锁。"),
        ("装扮我的小村", "升级建筑，用装饰填满猫咪们的空间。"),
        ("放置也没关系", "关掉游戏也会自动推进。通勤路上、睡前几分钟就够了。"),
        ("没有强制广告", "不会被广告打断。想要奖励时，自己选择再看。"),
    ],
    "cta_title": "今天猫咪们<br>也在等你。", "cta_sub": "免费下载 · iOS & Android",
    "f_contact": "联系我们", "f_privacy": "隐私政策", "f_terms": "服务条款"},
"zh-hant": {"name": "貓咪真的很可愛", "title": "貓咪真的很可愛 — 收集貓咪的療癒小村",
    "meta_desc": "收集貓咪、佈置小村的療癒放置遊戲。開一下下就夠，獎勵自動累積。★4.9 · 71,000+ 則評論。",
    "kicker": "Cats are Cute",
    "h1": "收集貓咪，<br><em>小村慢慢長大。</em>",
    "sub": "安靜療癒的放置模擬。開一下下就足夠，離開時獎勵也在自動累積。廣告只在你想看時出現。",
    "cta": "在 App Store 下載", "foot": "2018年至今 · iOS·Android 累計下載超過1000萬",
    "feat_label": "遊戲特色", "feat_title": "不需要複雜操作，靜靜看著就好。",
    "features": [
        ("收集各種貓咪", "每隻貓表情個性都不同。收集越多，小村越熱鬧，新場所也會解鎖。"),
        ("佈置我的小村", "升級建築，用裝飾填滿貓咪們的空間。"),
        ("放置也沒關係", "關掉遊戲也會自動推進。通勤路上、睡前幾分鐘就夠了。"),
        ("沒有強制廣告", "不會被廣告打斷。想要獎勵時，自己選擇再看。"),
    ],
    "cta_title": "今天貓咪們<br>也在等你。", "cta_sub": "免費下載 · iOS & Android",
    "f_contact": "聯絡我們", "f_privacy": "隱私權政策", "f_terms": "服務條款"},
"es": {"name": "Cats are Cute", "title": "Cats are Cute — Un pueblo de gatos para relajarte",
    "meta_desc": "Juego idle relajante: colecciona gatos y haz crecer tu pueblo. Sesiones cortas bastan; las recompensas se acumulan solas. ★4.9 · 71.000+ reseñas.",
    "kicker": "Cats are Cute",
    "h1": "Colecciona gatos y<br><em>mira crecer tu pueblo.</em>",
    "sub": "Una simulación idle tranquila y relajante. Con sesiones cortas basta — las recompensas se acumulan mientras no estás. Anuncios solo cuando tú quieras.",
    "cta": "Descargar en el App Store", "foot": "Desde 2018 · Más de 10 millones de descargas en iOS y Android",
    "feat_label": "Cómo es", "feat_title": "Sin controles complicados. Solo un pueblo que mirar.",
    "features": [
        ("Colecciona gatos", "Cada uno con su cara y personalidad. Cuantos más reúnas, más crece tu pueblo."),
        ("Decora tu pueblo", "Mejora edificios y llena el espacio de tus gatos con decoraciones."),
        ("Perfecto para jugar a ratos", "El progreso continúa con la app cerrada. Unos minutos al día bastan."),
        ("Sin anuncios forzados", "Nada te interrumpe. Ve anuncios solo si quieres el bonus."),
    ],
    "cta_title": "Los gatos te esperan<br>también hoy.", "cta_sub": "Descarga gratis · iOS y Android",
    "f_contact": "Contacto", "f_privacy": "Privacidad", "f_terms": "Términos"},
"pt": {"name": "Cats are Cute", "title": "Cats are Cute — Uma vila de gatos para relaxar",
    "meta_desc": "Jogo idle relaxante: colecione gatos e faça sua vila crescer. Sessões curtas bastam; as recompensas acumulam sozinhas. ★4.9 · 71.000+ avaliações.",
    "kicker": "Cats are Cute",
    "h1": "Colecione gatos e<br><em>veja sua vila crescer.</em>",
    "sub": "Uma simulação idle calma e relaxante. Sessões curtas são suficientes — as recompensas acumulam enquanto você está fora. Anúncios só quando você quiser.",
    "cta": "Baixar na App Store", "foot": "Desde 2018 · Mais de 10 milhões de downloads em iOS e Android",
    "feat_label": "Como é", "feat_title": "Sem controles complicados. Só uma vila para admirar.",
    "features": [
        ("Colecione gatos", "Cada um com seu rosto e personalidade. Quanto mais você reúne, mais a vila cresce."),
        ("Decore sua vila", "Melhore construções e encha o espaço dos gatos com decorações."),
        ("Bom para jogar aos poucos", "O progresso continua com o app fechado. Alguns minutos por dia bastam."),
        ("Sem anúncios forçados", "Nada interrompe você. Veja anúncios só se quiser o bônus."),
    ],
    "cta_title": "Os gatos estão esperando<br>por você hoje também.", "cta_sub": "Download grátis · iOS e Android",
    "f_contact": "Contato", "f_privacy": "Privacidade", "f_terms": "Termos"},
"de": {"name": "Cats are Cute", "title": "Cats are Cute — Ein Katzendorf zum Entspannen",
    "meta_desc": "Entspannendes Idle-Spiel: Sammle Katzen und lass dein Dorf wachsen. Kurze Sessions genügen; Belohnungen sammeln sich von selbst. ★4.9 · 71.000+ Bewertungen.",
    "kicker": "Cats are Cute",
    "h1": "Sammle Katzen,<br><em>und dein Dorf wächst.</em>",
    "sub": "Eine ruhige Idle-Simulation. Kurze Sessions reichen völlig — Belohnungen sammeln sich auch in deiner Abwesenheit. Werbung nur, wenn du willst.",
    "cta": "Im App Store laden", "foot": "Seit 2018 · Über 10 Mio. Downloads auf iOS & Android",
    "feat_label": "So spielt es sich", "feat_title": "Keine komplizierte Steuerung. Nur ein Dorf zum Anschauen.",
    "features": [
        ("Katzen sammeln", "Jede mit eigenem Gesicht und Charakter. Je mehr du sammelst, desto größer wird dein Dorf."),
        ("Dein Dorf gestalten", "Verbessere Gebäude und fülle die Welt deiner Katzen mit Dekorationen."),
        ("Idle-freundlich", "Der Fortschritt läuft auch bei geschlossener App weiter. Ein paar Minuten am Tag genügen."),
        ("Keine Zwangswerbung", "Nichts unterbricht dich. Werbung nur, wenn du den Bonus möchtest."),
    ],
    "cta_title": "Die Katzen warten<br>auch heute auf dich.", "cta_sub": "Kostenlos laden · iOS & Android",
    "f_contact": "Kontakt", "f_privacy": "Datenschutz", "f_terms": "AGB"},
"fr": {"name": "Cats are Cute", "title": "Cats are Cute — Un village de chats pour se détendre",
    "meta_desc": "Jeu idle apaisant : collectionnez des chats et faites grandir votre village. De courtes sessions suffisent ; les récompenses s'accumulent toutes seules. ★4,9 · 71 000+ avis.",
    "kicker": "Cats are Cute",
    "h1": "Collectionnez des chats,<br><em>votre village grandit.</em>",
    "sub": "Une simulation idle calme et apaisante. De courtes sessions suffisent — les récompenses s'accumulent en votre absence. Des pubs seulement quand vous le voulez.",
    "cta": "Télécharger sur l'App Store", "foot": "Depuis 2018 · Plus de 10 millions de téléchargements (iOS, Android)",
    "feat_label": "L'expérience", "feat_title": "Pas de contrôles compliqués. Juste un village à contempler.",
    "features": [
        ("Collectionnez des chats", "Chacun a son visage et son caractère. Plus vous en réunissez, plus le village s'enrichit."),
        ("Décorez votre village", "Améliorez les bâtiments et remplissez l'espace des chats de décorations."),
        ("Parfait en mode idle", "La progression continue même app fermée. Quelques minutes par jour suffisent."),
        ("Pas de pubs forcées", "Rien ne vous interrompt. Regardez une pub seulement pour le bonus."),
    ],
    "cta_title": "Les chats vous attendent<br>aujourd'hui aussi.", "cta_sub": "Téléchargement gratuit · iOS et Android",
    "f_contact": "Contact", "f_privacy": "Confidentialité", "f_terms": "Conditions"},
"ru": {"name": "Cats are Cute", "title": "Cats are Cute — Уютная деревня котиков",
    "meta_desc": "Спокойная idle-игра: собирайте котиков и развивайте деревню. Хватит коротких сессий; награды копятся сами. ★4.9 · 71 000+ отзывов.",
    "kicker": "Cats are Cute",
    "h1": "Собирайте котиков —<br><em>деревня растёт.</em>",
    "sub": "Спокойный расслабляющий idle-симулятор. Короткой сессии достаточно — награды копятся, пока вас нет. Реклама только по вашему желанию.",
    "cta": "Загрузить в App Store", "foot": "С 2018 года · Более 10 млн загрузок на iOS и Android",
    "feat_label": "Что внутри", "feat_title": "Без сложного управления. Просто деревня, на которую приятно смотреть.",
    "features": [
        ("Собирайте котиков", "У каждого — свой характер и мордочка. Чем больше котиков, тем богаче деревня."),
        ("Украшайте деревню", "Улучшайте здания и наполняйте мир котиков украшениями."),
        ("Можно не заходить часто", "Прогресс идёт даже при закрытой игре. Пары минут в день достаточно."),
        ("Без навязчивой рекламы", "Ничего не прерывает игру. Реклама — только ради бонуса и только по желанию."),
    ],
    "cta_title": "Котики ждут вас<br>и сегодня.", "cta_sub": "Бесплатно · iOS и Android",
    "f_contact": "Связаться", "f_privacy": "Конфиденциальность", "f_terms": "Условия"},
"th": {"name": "Cats are Cute", "title": "Cats are Cute — หมู่บ้านแมวเหมียวแสนอบอุ่น",
    "meta_desc": "เกม idle ชิลๆ สะสมแมวและขยายหมู่บ้าน เล่นแป๊บเดียวก็พอ รางวัลสะสมเองอัตโนมัติ ★4.9 · รีวิว 71,000+",
    "kicker": "Cats are Cute",
    "h1": "สะสมแมวเหมียว<br><em>หมู่บ้านก็เติบโต</em>",
    "sub": "เกมจำลองแนว idle สุดชิล เปิดเล่นแป๊บเดียวก็พอ รางวัลสะสมเองตอนคุณไม่อยู่ โฆษณาดูเฉพาะตอนที่อยากดูเท่านั้น",
    "cta": "ดาวน์โหลดบน App Store", "foot": "ตั้งแต่ปี 2018 · ยอดดาวน์โหลดรวมกว่า 10 ล้านบน iOS และ Android",
    "feat_label": "เกมเป็นแบบไหน", "feat_title": "ไม่ต้องบังคับอะไรยากๆ แค่นั่งมองหมู่บ้านก็ฟิน",
    "features": [
        ("สะสมแมวหลากหลาย", "แต่ละตัวมีหน้าตาและนิสัยต่างกัน ยิ่งสะสมหมู่บ้านยิ่งคึกคัก"),
        ("แต่งหมู่บ้านของฉัน", "อัปเกรดอาคารและเติมของตกแต่งให้พื้นที่ของเหล่าแมว"),
        ("ปล่อยทิ้งไว้ได้", "ปิดเกมไปความคืบหน้าก็เดินต่อ วันละไม่กี่นาทีก็พอ"),
        ("ไม่มีโฆษณาบังคับ", "ไม่มีอะไรขัดจังหวะ ดูโฆษณาเฉพาะตอนอยากได้โบนัส"),
    ],
    "cta_title": "วันนี้เหล่าแมว<br>ก็รอคุณอยู่นะ", "cta_sub": "โหลดฟรี · iOS และ Android",
    "f_contact": "ติดต่อ", "f_privacy": "ความเป็นส่วนตัว", "f_terms": "ข้อกำหนด"},
"id": {"name": "Cats are Cute", "title": "Cats are Cute — Desa kucing yang menenangkan",
    "meta_desc": "Game idle santai: kumpulkan kucing dan kembangkan desamu. Sesi singkat sudah cukup; hadiah menumpuk sendiri. ★4.9 · 71.000+ ulasan.",
    "kicker": "Cats are Cute",
    "h1": "Kumpulkan kucing,<br><em>desamu pun tumbuh.</em>",
    "sub": "Simulasi idle yang tenang dan menenangkan. Sesi singkat sudah cukup — hadiah terus menumpuk saat kamu pergi. Iklan hanya saat kamu mau.",
    "cta": "Unduh di App Store", "foot": "Sejak 2018 · 10 juta+ unduhan di iOS & Android",
    "feat_label": "Seperti apa", "feat_title": "Tanpa kontrol rumit. Cukup desa yang enak dipandang.",
    "features": [
        ("Kumpulkan beragam kucing", "Tiap kucing punya wajah dan kepribadian sendiri. Makin banyak, desa makin ramai."),
        ("Hias desamu sendiri", "Tingkatkan bangunan dan isi ruang para kucing dengan dekorasi."),
        ("Cocok dimainkan santai", "Progres jalan terus walau aplikasi ditutup. Beberapa menit sehari sudah cukup."),
        ("Tanpa iklan paksa", "Tak ada yang menyela. Tonton iklan hanya jika ingin bonus."),
    ],
    "cta_title": "Hari ini pun para kucing<br>menunggumu.", "cta_sub": "Gratis · iOS & Android",
    "f_contact": "Kontak", "f_privacy": "Privasi", "f_terms": "Ketentuan"},
"vi": {"name": "Cats are Cute", "title": "Cats are Cute — Ngôi làng mèo chữa lành",
    "meta_desc": "Game idle thư giãn: sưu tầm mèo và phát triển ngôi làng. Chơi vài phút là đủ; phần thưởng tự tích lũy. ★4.9 · 71.000+ đánh giá.",
    "kicker": "Cats are Cute",
    "h1": "Sưu tầm mèo,<br><em>ngôi làng lớn dần.</em>",
    "sub": "Game mô phỏng idle nhẹ nhàng, chữa lành. Mỗi lần mở vài phút là đủ — phần thưởng vẫn tích lũy khi bạn vắng mặt. Quảng cáo chỉ khi bạn muốn xem.",
    "cta": "Tải trên App Store", "foot": "Từ 2018 · Hơn 10 triệu lượt tải trên iOS & Android",
    "feat_label": "Trò chơi thế nào", "feat_title": "Không thao tác phức tạp. Chỉ một ngôi làng để ngắm.",
    "features": [
        ("Sưu tầm đủ loại mèo", "Mỗi bé một gương mặt, một tính cách. Càng sưu tầm, làng càng đông vui."),
        ("Trang trí ngôi làng", "Nâng cấp công trình và lấp đầy không gian của các bé mèo bằng đồ trang trí."),
        ("Treo máy thoải mái", "Đóng game tiến trình vẫn chạy. Vài phút mỗi ngày là đủ."),
        ("Không quảng cáo ép buộc", "Không gì làm phiền bạn. Chỉ xem quảng cáo khi muốn nhận thưởng."),
    ],
    "cta_title": "Hôm nay các bé mèo<br>vẫn đang đợi bạn.", "cta_sub": "Tải miễn phí · iOS & Android",
    "f_contact": "Liên hệ", "f_privacy": "Quyền riêng tư", "f_terms": "Điều khoản"},
}

build_app(APP, S)
