# Sidefeed — 크리에이터용 트렌드 리서치. 다크 + 네온 그라데이션, 순위 보드 히어로.
from common import build_app

APP = {
    "slug": "sidefeed",
    "trackId": "6762836653",
    "rating": None,
    "theme": {"bg": "#0C0D13", "ink": "#F2F2F7", "ink2": "#8A8C9C", "accent": "#FF5C6A",
              "card": "rgba(255,255,255,.045)", "border": "rgba(255,255,255,.09)"},
    "hero_html": """    <div class="board">
      <div class="row"><span class="rank">1</span><i class="tbar" style="width:88%"></i><span class="badge up">▲3</span></div>
      <div class="row"><span class="rank">2</span><i class="tbar" style="width:72%"></i><span class="badge nw">NEW</span></div>
      <div class="row"><span class="rank">3</span><i class="tbar" style="width:64%"></i><span class="badge dn">▼1</span></div>
      <div class="row"><span class="rank">4</span><i class="tbar" style="width:55%"></i><span class="badge up">▲7</span></div>
      <div class="row"><span class="rank">5</span><i class="tbar" style="width:46%"></i><span class="badge up">▲2</span></div>
      <div class="chips">
        <i>KR</i><i>US</i><i>JP</i><i>UK</i><i>DE</i><i>FR</i><i>AU</i><i>CA</i><i>CH</i><i>NL</i><i>SE</i><i>SG</i>
      </div>
    </div>""",
    "extra_css": """
.board { width:330px; background:#14151E; border:1px solid rgba(255,255,255,.09);
  border-radius:24px; padding:22px 20px 18px; box-shadow:0 30px 70px -24px rgba(0,0,0,.8); }
.row { display:flex; align-items:center; gap:12px; padding:11px 2px; }
.row + .row { border-top:1px solid rgba(255,255,255,.05); }
.rank { font-weight:800; font-size:14px; width:18px; color:#5A5C6C; font-variant-numeric:tabular-nums; }
.tbar { height:11px; border-radius:6px; background:linear-gradient(90deg,#FF4D5E,#FF8A4D,#FFB14D);
  animation:barpulse 3.2s ease-in-out infinite; transform-origin:left center; }
.row:nth-child(2) .tbar { animation-delay:.4s; } .row:nth-child(3) .tbar { animation-delay:.8s; }
.row:nth-child(4) .tbar { animation-delay:1.2s; } .row:nth-child(5) .tbar { animation-delay:1.6s; }
.badge { font-size:11px; font-weight:800; margin-left:auto; }
.badge.up { color:#3DDC97; } .badge.dn { color:#FF6A6A; } .badge.nw { color:#FFB14D; }
.chips { display:flex; flex-wrap:wrap; gap:6px; margin-top:16px; }
.chips i { font-style:normal; font-size:9.5px; font-weight:700; letter-spacing:.04em; color:#8A8C9C;
  border:1px solid rgba(255,255,255,.12); border-radius:99px; padding:3px 8px; }
@keyframes barpulse { 0%,100% { transform:scaleX(1); opacity:1; } 50% { transform:scaleX(.96); opacity:.85; } }
""",
}

S = {
"ko": {
    "name": "Sidefeed", "title": "Sidefeed — 크리에이터를 위한 12개국 트렌드 리서치",
    "meta_desc": "12개국 유튜브 트렌딩과 Radar Score 분석을 한 화면에서. 큰 채널에 묻힌 급상승을 잡아내는 크리에이터용 리서치 앱.",
    "kicker": "Trend research for creators",
    "h1": "다음 영상의 단서는<br><em>차트 밖</em>에 있다.",
    "sub": "12개국 트렌딩과 Sidefeed 레이더 분석을 한 화면에서 비교하세요. 절대 조회수 차트가 놓치는 작은 채널의 급상승까지 — 영상 기획에 필요한 신호만 추렸습니다.",
    "cta": "App Store에서 받기", "foot": "무료 다운로드 · iPhone & iPad",
    "feat_label": "기능", "feat_title": "기획에 필요한 신호만, 한 화면에.",
    "features": [
        ("12개국 트렌딩", "한국·미국·일본·영국·독일 등 12개국 인기 차트를 탭 한 번으로 전환. 내 분야가 다른 시장에선 뭐로 통하는지."),
        ("Radar Score", "시간당 조회수·반응률·순위 변동을 가중합해 재정렬. 큰 채널 차트에 묻힌 breakout을 표면화합니다."),
        ("Top Movers", "모든 영상에 ▲N/▼N/NEW 뱃지로 6시간 전 대비 변동 표시. 상승폭 큰 영상은 따로 모아서."),
        ("카테고리 분포", "색상 스택 바로 지금 차트를 점유한 분야를 한 줄에. 14개 카테고리 중 관심 분야만 골라 보기."),
    ],
    "cta_title": "다음 영상,<br>감이 아니라 신호로.", "cta_sub": "무료로 시작 · iPhone & iPad",
    "f_contact": "문의", "f_privacy": "개인정보 처리방침", "f_terms": "이용약관",
},
"en": {
    "name": "Sidefeed", "title": "Sidefeed — Trend research for creators, across 12 countries",
    "meta_desc": "YouTube trending across 12 countries plus Radar Score analysis on one screen. Surface breakouts buried under big channels.",
    "kicker": "Trend research for creators",
    "h1": "Your next video's clue is<br><em>off the charts.</em>",
    "sub": "Compare trending across 12 countries with Sidefeed's radar analysis — surfacing small-channel breakouts that raw view-count charts bury. Just the signals you need to plan your next video.",
    "cta": "Download on the App Store", "foot": "Free download · iPhone & iPad",
    "feat_label": "Features", "feat_title": "Only the signals that matter, on one screen.",
    "features": [
        ("Trending in 12 countries", "Korea, US, Japan, UK, Germany and more — switch charts with one tap and see what your niche looks like in other markets."),
        ("Radar Score", "Re-ranks by views-per-hour, engagement, and rank momentum — surfacing breakouts that absolute view counts hide."),
        ("Top Movers", "▲N / ▼N / NEW badges show movement vs. 6 hours ago, with big climbers collected in one place."),
        ("Category mix", "A color-stacked bar shows which categories own the chart right now. Follow only the ones you care about, out of 14."),
    ],
    "cta_title": "Plan your next video<br>on signal, not gut.", "cta_sub": "Free to start · iPhone & iPad",
    "f_contact": "Contact", "f_privacy": "Privacy", "f_terms": "Terms",
},
"ja": {
    "name": "Sidefeed", "title": "Sidefeed — クリエイターのための12カ国トレンドリサーチ",
    "meta_desc": "12カ国のYouTube急上昇とRadar Score分析をひとつの画面で。大手チャンネルに埋もれたブレイクアウトを発見。",
    "kicker": "Trend research for creators",
    "h1": "次の動画のヒントは<br><em>チャートの外</em>にある。",
    "sub": "12カ国の急上昇とSidefeedレーダー分析をひとつの画面で比較。再生数チャートが見落とす小さなチャンネルの急騰まで — 企画に必要なシグナルだけを集めました。",
    "cta": "App Storeでダウンロード", "foot": "無料ダウンロード · iPhone & iPad",
    "feat_label": "機能", "feat_title": "企画に効くシグナルだけ、ひとつの画面に。",
    "features": [
        ("12カ国の急上昇", "韓国・米国・日本・英国・ドイツなど12カ国のチャートをワンタップで切替。自分のジャンルが他の市場でどう動くか。"),
        ("Radar Score", "時間あたり再生数・反応率・順位変動を加重して再ランキング。大手に埋もれたブレイクアウトを表面化。"),
        ("Top Movers", "全動画に▲N/▼N/NEWバッジで6時間前比の変動を表示。急上昇はまとめて確認。"),
        ("カテゴリ分布", "カラースタックバーで今チャートを占めるジャンルが一目で。14カテゴリから関心分野だけ。"),
    ],
    "cta_title": "次の動画は、<br>勘ではなくシグナルで。", "cta_sub": "無料で始める · iPhone & iPad",
    "f_contact": "お問い合わせ", "f_privacy": "プライバシー", "f_terms": "利用規約",
},
}

build_app(APP, S)
