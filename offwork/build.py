#!/usr/bin/env python3
"""Offwork 랜딩페이지 생성기. index.html 을 직접 고치지 말고 이 파일만 수정한 뒤 `python3 build.py` 실행."""
from pathlib import Path

BASE_URL = "https://www.kkirukstudio.com/offwork"
APP_STORE_URL = ""  # 심사 승인 후 채운다
CONTACT = "kkirukstudio.help@gmail.com"
PRIVACY = "https://www.kkirukstudio.com/legal/privacy/"
TERMS = "https://www.kkirukstudio.com/legal/terms/"

L = {
    "ko": {
        "lang": "ko", "dir": "", "other": ("en", "English", "en/"),
        "title": "Offwork — 댓글 없는 익명 직장인 커뮤니티",
        "desc": "자유 댓글이 없습니다. 내 이야기에는 내가 정한 선택지로만 답할 수 있어요. 퇴근하고 내려놓는 익명 직장인 커뮤니티.",
        "nav": ["어떻게 쓰나요", "화면", "안전"],
        "hero_kicker": "OFFWORK · 익명 직장인 커뮤니티",
        "h1": ["퇴근하고 내려놓는,", "익명 직장인", "커뮤니티"],
        "lead": "자유 댓글이 없습니다. 이야기를 쓸 때 반응 방식을 직접 고르면, 다른 사람은 그 선택지로만 답할 수 있어요. 악플이 생길 자리가 없습니다.",
        "cta_main": "App Store에서 곧 만나요", "cta_sub": "무엇이 다른지 보기",
        "demo_body": "팀장이 오늘 또 내가 만든 자료를 자기가 한 것처럼 보고했다. 이제 진짜 열심히 하고 싶지가 않다.",
        "demo_meta": "익명의 직장인 · 2시간 전", "demo_kicker": "어떻게 할까?",
        "demo_q": "이 상황에서 당신이라면?",
        "demo_opts": [("이야기한다", 64), ("그냥 넘긴다", 16), ("상사에게 알린다", 12), ("이직을 준비한다", 8)],
        "demo_hint": "↑ 눌러보세요 — 투표해야 결과가 보입니다",
        "demo_before": "선택하면 전체 결과를 볼 수 있어요", "demo_after": "총 88명 참여",
        "marquee": ["댓글 없음", "익명", "투표로만 반응", "가입 없이 바로", "공개 프로필 없음"],
        "steps_h2": "쓰고, 고르고, 확인합니다", "steps_sub": "글 하나를 올리는 데 30초. 반응은 탭 한 번.",
        "steps": [("01", "반응 방식을 먼저 고른다", "그냥 들어줘 · 내가 예민한가? · 어떻게 할까? · 사람들이 어떻게 생각할까? 중 하나. 이 선택이 다른 사람이 답할 수 있는 유일한 방법이 됩니다."),
                   ("02", "오늘 있었던 일을 쓴다", "회사명·실명 같은 개인 정보와 욕설, 외부 링크는 게시 전에 자동으로 걸러집니다."),
                   ("03", "투표하고 결과를 본다", "먼저 투표해야 전체 비율이 열립니다. 남의 의견에 휩쓸리기 전에 내 판단을 먼저 남겨요.")],
        "value_h2": "댓글창을 지웠습니다", "value_sub": "커뮤니티가 망가지는 자리를 아예 없앴어요.",
        "strike": "“그건 네가 잘못한 듯”",
        "value_h3": "긴 말 대신,\n네 개의 선택지",
        "value_p": "누구도 당신에게 문장을 쓸 수 없습니다. 남길 수 있는 건 당신이 정한 선택지 하나뿐이에요. 그래서 조언도, 비난도, 싸움도 쌓이지 않습니다.",
        "shots_h2": "화면", "shots_sub": "라디우스 없는 모더니스트 레이아웃. 읽는 데 방해되는 장식은 뺐습니다.",
        "shots": [("오늘", "오늘의 기분을 고르고, 다른 사람들의 이야기에 반응합니다."),
                   ("이야기", "본문 전문과 투표 결과. 공유·차단·신고가 한 자리에."),
                   ("설정", "계정 보관 · 운영 정책 · 문의. 필요한 것만 남겼습니다.")],
        "details_h2": "안전하게 운영합니다", "details_sub": "익명이라고 아무 말이나 할 수 있는 곳은 아닙니다.",
        "details": [("게시 전 필터", "욕설·혐오 표현, 전화번호·이메일 같은 개인 정보, 외부 링크는 게시되지 않습니다."),
                     ("신고 즉시 숨김", "신고한 이야기는 그 자리에서 사라지고, 접수된 신고는 24시간 안에 검토합니다."),
                     ("자동 노출 중단", "여러 명이 신고한 이야기는 사람이 검토하기 전에도 피드에서 내려갑니다."),
                     ("작성자 차단", "불편한 작성자를 차단하면 그 사람의 이야기는 더 이상 보이지 않습니다."),
                     ("공개 프로필 없음", "이름·이메일·회사 정보를 저장하지 않고, 팔로우도 DM도 없습니다."),
                     ("투표는 비공개", "누가 어떤 선택을 했는지 글쓴이에게 보이지 않습니다.")],
        "final_h2": "오늘 회사, 어땠어요?",
        "final_p": "판단은 각자 하되, 혼자 삼키지는 않도록.",
        "foot_tag": "댓글 없는 익명 직장인 커뮤니티",
        "foot_links": [("문의", f"mailto:{CONTACT}"), ("개인정보 처리방침", PRIVACY), ("이용약관", TERMS), ("kkiruk studio", "https://www.kkirukstudio.com")],
        "note": "한국어 커뮤니티입니다. 앱 화면은 한국어·영어·일본어·번체 중국어를 지원합니다.",
    },
    "en": {
        "lang": "en", "dir": "en/", "other": ("ko", "한국어", ""),
        "title": "Offwork — An anonymous work community without comments",
        "desc": "No free-form comments. People answer your story only with the options you choose. An anonymous community for people at work.",
        "nav": ["How it works", "Screens", "Safety"],
        "hero_kicker": "OFFWORK · ANONYMOUS WORK COMMUNITY",
        "h1": ["Clock out,", "put it down.", "Anonymously."],
        "lead": "There are no free-form comments. You pick how people may react when you post, and that's the only way they can answer. Abusive replies have nowhere to live.",
        "cta_main": "Coming to the App Store", "cta_sub": "See what's different",
        "demo_body": "My manager presented my work as his own again today. I don't feel like trying anymore.",
        "demo_meta": "Anonymous coworker · 2 hours ago", "demo_kicker": "What should I do?",
        "demo_q": "What would you do?",
        "demo_opts": [("Talk to them", 64), ("Let it go", 16), ("Tell their boss", 12), ("Start job hunting", 8)],
        "demo_hint": "↑ Tap one — you vote before you see results",
        "demo_before": "Vote to see the full results", "demo_after": "88 people voted",
        "marquee": ["NO COMMENTS", "ANONYMOUS", "VOTES ONLY", "NO SIGN-UP", "NO PUBLIC PROFILE"],
        "steps_h2": "Write, choose, see", "steps_sub": "Thirty seconds to post. One tap to react.",
        "steps": [("01", "Pick the reaction type first", "Just listen · Am I overreacting? · What should I do? · What do people think? Whatever you pick becomes the only way others can answer."),
                   ("02", "Write what happened today", "Company names, real names, profanity, and external links are filtered out before the story is posted."),
                   ("03", "Vote, then see results", "The full breakdown opens only after you vote, so you form your own judgment before seeing the crowd's.")],
        "value_h2": "We deleted the comment box", "value_sub": "The place where communities usually rot is simply gone.",
        "strike": "“Sounds like your fault tbh”",
        "value_h3": "Four options\ninstead of a paragraph",
        "value_p": "Nobody can write a sentence at you. All anyone can leave is one option you chose yourself — so advice, blame, and arguments never pile up.",
        "shots_h2": "Screens", "shots_sub": "A modernist layout with zero corner radius. Nothing decorative gets between you and the words.",
        "shots": [("Today", "Set today's mood and react to what other people left behind."),
                   ("Story", "The full text and the vote breakdown. Share, block, and report in one place."),
                   ("Settings", "Account backup, community policy, contact. Only what's needed.")],
        "details_h2": "Anonymous, not lawless", "details_sub": "Being anonymous doesn't mean anything goes.",
        "details": [("Filtered before posting", "Profanity, hate speech, phone numbers, emails, and external links never make it through."),
                     ("Hidden the moment you report", "A reported story disappears for you right away; reports are reviewed within 24 hours."),
                     ("Automatic takedown", "Stories reported by several people leave the feed before a human even looks."),
                     ("Block an author", "Block someone and their stories stop appearing for you."),
                     ("No public profile", "No name, email, or employer is stored — and there are no follows or DMs."),
                     ("Private votes", "The author never sees who picked what.")],
        "final_h2": "How was work today?",
        "final_p": "Judge for yourself — just don't swallow it alone.",
        "foot_tag": "An anonymous work community without comments",
        "foot_links": [("Contact", f"mailto:{CONTACT}"), ("Privacy Policy", PRIVACY), ("Terms of Service", TERMS), ("kkiruk studio", "https://www.kkirukstudio.com")],
        "note": "Offwork is a Korean-language community. The app interface supports English, Japanese, Korean, and Traditional Chinese.",
    },
}


def page(t):
    is_root = t["dir"] == ""
    asset = "assets/" if is_root else "../assets/"
    other_code, other_label, other_path = t["other"]
    canonical = f"{BASE_URL}/{t['dir']}"
    opts = "\n".join(
        f'''          <button class="opt" data-pct="{p}" type="button">
            <span class="fill"></span><span class="label">{o}</span><span class="pct">{p}%</span>
          </button>'''
        for o, p in t["demo_opts"])
    steps = "\n".join(
        f'''        <article class="step"><div class="num">{n}</div><h3>{h}</h3><p>{d}</p></article>'''
        for n, h, d in t["steps"])
    shots = "\n".join(
        f'''        <figure class="shot"><img src="{asset}shot-{f}.png" alt="{c}" loading="lazy" width="900"><figcaption>{c} — {d}</figcaption></figure>'''
        for (c, d), f in zip(t["shots"], ["feed", "detail", "settings"]))
    details = "\n".join(
        f'''        <article class="detail"><h4>{h}</h4><p>{d}</p></article>'''
        for h, d in t["details"])
    foot_links = "\n".join(f'          <a href="{u}">{n}</a>' for n, u in t["foot_links"])
    marquee = "".join(f"<span>{m}</span>" for m in t["marquee"] * 2)
    cta_attr = f'href="{APP_STORE_URL}"' if APP_STORE_URL else 'href="#how" data-disabled="true"'

    return f'''<!DOCTYPE html>
<html lang="{t['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t['title']}</title>
<meta name="description" content="{t['desc']}">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="ko" href="{BASE_URL}/">
<link rel="alternate" hreflang="en" href="{BASE_URL}/en/">
<link rel="alternate" hreflang="x-default" href="{BASE_URL}/">
<link rel="icon" href="{asset}icon.png">
<meta property="og:type" content="website">
<meta property="og:title" content="{t['title']}">
<meta property="og:description" content="{t['desc']}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{BASE_URL}/assets/icon.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="{asset}style.css">
<script src="/ga.js" defer></script>
</head>
<body>
<nav class="nav"><div class="wrap nav-in">
  <span class="brand">OFF<span class="w">WORK</span></span>
  <a href="#how">{t['nav'][0]}</a>
  <a href="#screens">{t['nav'][1]}</a>
  <a href="#safety">{t['nav'][2]}</a>
  <a class="lang" href="{BASE_URL}/{other_path}" hreflang="{other_code}">{other_label}</a>
</div></nav>

<header class="hero"><div class="wrap hero-grid">
  <div>
    <div class="kicker">{t['hero_kicker']}</div>
    <h1>{t['h1'][0]}<br><em>{t['h1'][1]}</em><br>{t['h1'][2]}</h1>
    <p class="lead">{t['lead']}</p>
    <div class="cta-row">
      <a class="btn btn-primary" {cta_attr}>{t['cta_main']} <span>→</span></a>
      <a class="btn btn-secondary" href="#how">{t['cta_sub']} <span>↓</span></a>
    </div>
  </div>
  <div class="phone">
    <div class="phone-bar"><span>9:41</span><span class="island"></span><span>100%</span></div>
    <div class="demo-card demo" id="demo">
      <div class="kicker">{t['demo_kicker']}</div>
      <p class="demo-body">{t['demo_body']}</p>
      <div class="demo-meta">{t['demo_meta']}</div>
      <hr class="rule-thin" style="margin:12px 0">
      <div class="demo-q">{t['demo_q']}</div>
{opts}
      <div class="demo-caption" id="demo-caption" data-after="{t['demo_after']}">{t['demo_before']}</div>
      <div class="demo-hint">{t['demo_hint']}</div>
    </div>
  </div>
</div></header>

<div class="marquee"><div class="marquee-track">{marquee}</div></div>

<section id="how"><div class="wrap">
  <div class="sec-head"><h2>{t['steps_h2']}</h2><p>{t['steps_sub']}</p></div>
  <div class="steps">
{steps}
  </div>
</div></section>

<section><div class="wrap">
  <div class="sec-head"><h2>{t['value_h2']}</h2><p>{t['value_sub']}</p></div>
  <div class="value">
    <div class="value-box">
      <p class="strike">{t['strike']}</p>
      <div class="opt picked" style="cursor:default"><span class="fill" style="width:64%"></span><span class="label">{t['demo_opts'][0][0]}</span><span class="pct" style="opacity:1">64%</span></div>
      <div class="opt" style="cursor:default"><span class="fill" style="width:16%"></span><span class="label">{t['demo_opts'][1][0]}</span><span class="pct" style="opacity:1">16%</span></div>
    </div>
    <div>
      <h3>{t['value_h3'].split(chr(10))[0]}<br>{t['value_h3'].split(chr(10))[1]}</h3>
      <p>{t['value_p']}</p>
    </div>
  </div>
</div></section>

<section id="screens"><div class="wrap">
  <div class="sec-head"><h2>{t['shots_h2']}</h2><p>{t['shots_sub']}</p></div>
  <div class="shots">
{shots}
  </div>
</div></section>

<section id="safety"><div class="wrap">
  <div class="sec-head"><h2>{t['details_h2']}</h2><p>{t['details_sub']}</p></div>
  <div class="details">
{details}
  </div>
</div></section>

<section class="final"><div class="wrap">
  <h2>{t['final_h2']}</h2>
  <p style="font-size:18px;max-width:32em">{t['final_p']}</p>
  <div class="cta-row"><a class="btn btn-secondary" {cta_attr}>{t['cta_main']} <span>→</span></a></div>
</div></section>

<footer><div class="wrap">
  <div class="foot-grid">
    <div>
      <div class="brand">OFF<span class="w">WORK</span></div>
      <p style="opacity:.7;margin-top:6px">{t['foot_tag']}</p>
      <p style="opacity:.55;margin-top:10px;max-width:30em;font-size:12px">{t['note']}</p>
    </div>
    <div class="spacer foot-links">
{foot_links}
    </div>
  </div>
  <p class="copyright">© 2026 kkiruk studio</p>
</div></footer>

<script>
(function () {{
  var demo = document.getElementById('demo');
  if (!demo) return;
  var caption = document.getElementById('demo-caption');
  demo.querySelectorAll('.opt').forEach(function (btn) {{
    btn.addEventListener('click', function () {{
      demo.querySelectorAll('.opt').forEach(function (o) {{
        o.classList.remove('picked');
        o.querySelector('.fill').style.width = o.dataset.pct + '%';
      }});
      btn.classList.add('picked');
      demo.classList.add('revealed');
      caption.textContent = caption.dataset.after;
    }});
  }});
}})();
</script>
</body>
</html>
'''


root = Path(__file__).parent
(root / "index.html").write_text(page(L["ko"]), encoding="utf-8")
(root / "en").mkdir(exist_ok=True)
(root / "en" / "index.html").write_text(page(L["en"]), encoding="utf-8")
print("generated: index.html, en/index.html")
