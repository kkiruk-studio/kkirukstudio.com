#!/usr/bin/env python3
"""Generate index.html for every locale from one template.

Usage: python3 build.py
Output: ./index.html (en), ./ko/index.html
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).parent
BASE_URL = "https://www.kkirukstudio.com/newsmaker/"

APPLE_SVG = '<svg viewBox="0 0 384 512" aria-hidden="true"><path d="M318.7 268.7c-.2-36.7 16.4-64.4 50-84.8-18.8-26.9-47.2-41.7-84.7-44.6-35.5-2.8-74.3 20.7-88.5 20.7-15 0-49.4-19.7-76.4-19.7C63.3 141.2 4 184.8 4 273.5q0 39.3 14.4 81.2c12.8 36.7 59 126.7 107.2 125.2 25.2-.6 43-17.9 75.8-17.9 31.8 0 48.3 17.9 76.4 17.9 48.6-.7 90.4-82.5 102.6-119.3-65.2-30.7-61.7-90-61.7-91.9zm-56.6-164.2c27.3-32.4 24.8-61.9 24-72.5-24.1 1.4-52 16.4-67.9 34.9-17.5 19.8-27.8 44.3-25.6 71.9 26.1 2 49.9-11.4 69.5-34.3z"/></svg>'

LANG_LABELS = [("", "EN"), ("ko/", "한국어")]

LOCALES = {
    "en": {
        "dir": "", "lang": "en", "font": None,
        "title": "Newsmaker — Turn your day into breaking-news memes",
        "desc": "Type one headline, pick a theme and font, and Newsmaker turns your ordinary day into a shareable breaking-news meme. No account, no ads, all on-device. Free for iPhone.",
        "og_title": "Newsmaker — Breaking Meme Maker",
        "og_desc": "Turn your ordinary day into a breaking-news meme in seconds.",
        "kicker_num": "BREAKING MEME MAKER",
        "h1": "Your ordinary day.<br>One <em>breaking-news</em> headline.",
        "pairs": [
            ["Meeting canceled", "BREAKING: Meeting canceled"],
            ["Package arrived", "BREAKING: Package arrived early"],
            ["PR maxed", "BREAKING: New PR — 500 total"],
            ["Got the job", "BREAKING: Final offer received"],
        ],
        "sub": "Type one line about your day. Newsmaker turns it into a red-alert headline card — pick a theme, pick a font, drop in a cut-out photo of yourself, and save it as a shareable image.",
        "badge_small": "Download on the", "note": "FREE · IPHONE · NO ACCOUNT",
        "badge_aria": "Download on the App Store",
        "chips": [["!", "Meeting canceled"], ["!", "Package"], ["!", "Concert tix"], ["!", "PR day"]],
        "hero_alt": "Newsmaker headline maker screen showing a breaking-news style card being created",
        "marquee": ["MEETING CANCELED", "PACKAGE ARRIVED", "CONCERT TICKETS", "NEW PR", "FINAL OFFER", "LUNCH DECIDED", "STOCK UP", "VACATION APPROVED"],
        "how_kicker": "HOW IT WORKS",
        "how_h2": "From a normal sentence to a <em>front page</em> in three taps.",
        "steps": [
            ["HEADLINE", "Type one line", "Whatever happened today — big or small. That's your headline."],
            ["STYLE", "Pick a theme and font", "14 card themes from breaking-news red to newspaper broadsheet, 12 display fonts to match the mood."],
            ["SHARE", "Save and share", "Export as an image in the ratio you need and send it to the group chat."],
        ],
        "conv_kicker": "CONVERSION", "conv_num": "MUNDANE → BREAKING",
        "conv_h2": "Nothing happened. <em>Everything happened.</em>",
        "conv_lede": "Newsmaker takes the smallest events of your day and gives them the full breaking-news treatment — red banner, bold type, all caps.",
        "conv_rows": [
            ["Meeting canceled", "BREAKING: Meeting canceled", "OFFICE · RELIEF"],
            ["Package arrived", "BREAKING: Package arrived early", "DELIVERY · WIN"],
            ["PR maxed", "BREAKING: New PR — 500 total", "GYM · MILESTONE"],
            ["Got the job", "BREAKING: Final offer received", "CAREER · GOOD NEWS"],
        ],
        "styles_kicker": "STYLE", "styles_num": "YOURS TO MIX",
        "styles_h2": "14 themes. 12 fonts. <em>Endless front pages.</em>",
        "styles_lede": "Mix and match a look for every kind of news, and drop yourself into the story with a one-tap cut-out sticker.",
        "providers": [
            ["📰", "14 Card Themes", [["속", "Breaking News"], ["자", "Caption / Yellow"]]],
            ["🔤", "12 Display Fonts", [["Aa", "Impact / Serif"], ["가", "Handwriting / Round"]]],
            ["✂️", "Cut-out Sticker", [["👤", "Auto background removal"]]],
            ["🎯", "Interest Presets", [["🎮", "Student · Work · Gym · Gaming…"]]],
        ],
        "shots_kicker": "SCREENS", "shots_num": "IOS 26",
        "shots_h2": "Built for <em>fast, funny front pages</em>.",
        "shots_caps": ["14 THEMES", "12 FONTS", "MY LIBRARY"],
        "feat_kicker": "DETAILS", "feat_num": "06",
        "feat_h2": "Small app. <em>Loaded</em> toolbox.",
        "feats": [
            ["14 card themes", "Breaking news, broadcast caption, tabloid, newspaper, magazine, emergency alert and more."],
            ["12 display fonts", "Impact, handwriting, serif, bold rounded — every headline has a voice."],
            ["Cut-out photo sticker", "Auto background removal turns any photo into a sticker you can drop into the story."],
            ["Interest-based examples", "Student, office worker, fandom, gym, dating, pets, job hunting, gaming, stocks — ready-made lines to remix."],
            ["4 aspect ratios", "Square, feed 4:5, story 9:16, or widescreen 16:9 — export for wherever you're posting."],
            ["No account, no ads", "Everything happens on your device. Free, iPhone only, nothing to sign up for."],
        ],
        "final_h2": "Make today's breaking news.", "final_lede": "Free on iPhone.",
        "f_contact": "Contact", "f_privacy": "Privacy", "f_terms": "Terms",
    },
    "ko": {
        "dir": "ko/", "lang": "ko", "font": '"Apple SD Gothic Neo", "Pretendard"',
        "title": "속보메이커 — 평범한 하루를 속보 짤로",
        "desc": "헤드라인 한 줄만 입력하면 속보메이커가 테마와 폰트를 입혀 공유용 짤로 만들어줍니다. 계정도 광고도 없이, 모든 처리는 기기 안에서. 아이폰 무료 앱.",
        "og_title": "속보메이커 — 속보 짤 제조기",
        "og_desc": "평범한 하루를 웃긴 속보 짤로, 몇 초 만에.",
        "kicker_num": "속보 짤 제조기",
        "h1": "평범한 하루도,<br>한 줄이면 <em>속보</em>가 된다",
        "pairs": [
            ["회의 취소", "속보: 회의 전격 취소"],
            ["택배 도착", "속보: 택배 하루 만에 도착"],
            ["오운완", "속보: 오운완 3대 500 달성"],
            ["최종 합격", "속보: 최종 합격 통보"],
        ],
        "sub": "오늘 있었던 일, 한 줄이면 충분해요. 속보메이커가 빨간 속보 배너 스타일로 바꿔줍니다. 테마 고르고, 폰트 고르고, 내 사진으로 누끼 스티커까지 붙여서 짤로 저장하세요.",
        "badge_small": "다운로드는", "note": "무료 · 아이폰 · 계정 불필요",
        "badge_aria": "App Store에서 다운로드",
        "chips": [["속", "회의취소"], ["속", "택배"], ["속", "티켓팅"], ["속", "오운완"]],
        "hero_alt": "속보메이커 헤드라인 제작 화면 — 속보 스타일 카드를 만드는 모습",
        "marquee": ["회의취소", "택배", "티켓팅", "오운완", "최종합격", "점심결정", "주식떡상", "휴가확정"],
        "how_kicker": "사용 방법",
        "how_h2": "평범한 한 줄이 <em>1면 속보</em>가 되기까지 세 번의 탭.",
        "steps": [
            ["헤드라인", "한 줄 입력", "오늘 있었던 일, 크든 작든 한 줄이면 헤드라인 완성."],
            ["스타일", "테마·폰트 고르기", "속보부터 신문 지면까지 14가지 테마, 분위기에 맞는 폰트 12종."],
            ["공유", "저장하고 공유", "필요한 비율로 이미지 저장해서 단톡방에 바로 투척."],
        ],
        "conv_kicker": "변환", "conv_num": "평범한 하루 → 속보",
        "conv_h2": "아무 일도 없었는데, <em>다 속보였다</em>.",
        "conv_lede": "속보메이커는 하루의 사소한 순간을 빨간 속보 배너, 굵은 글씨, 전체 대문자로 격상시켜줍니다.",
        "conv_rows": [
            ["회의 취소", "속보: 회의 전격 취소", "회사 · 안도"],
            ["택배 도착", "속보: 택배 하루 만에 도착", "택배 · 승리"],
            ["오운완", "속보: 오운완 3대 500 달성", "헬스 · 신기록"],
            ["최종 합격", "속보: 최종 합격 통보", "커리어 · 경사"],
        ],
        "styles_kicker": "스타일", "styles_num": "자유롭게 조합",
        "styles_h2": "테마 14종, 폰트 12종. <em>매번 다른 1면.</em>",
        "styles_lede": "뉴스 종류마다 다른 룩을 조합하고, 누끼 스티커로 내 얼굴을 뉴스 주인공으로 만드세요.",
        "providers": [
            ["📰", "카드 테마 14종", [["속", "속보 · 방송자막"], ["옐", "옐로 · 재난문자"]]],
            ["🔤", "폰트 12종", [["가", "임팩트 · 명조"], ["손", "손글씨 · 통통 라운드"]]],
            ["✂️", "누끼 스티커", [["👤", "배경 자동 제거"]]],
            ["🎯", "관심사별 예시", [["🎮", "학생 · 직장인 · 헬스 · 게임…"]]],
        ],
        "shots_kicker": "화면", "shots_num": "IOS 26",
        "shots_h2": "빠르고 웃긴 <em>1면 제작소</em>.",
        "shots_caps": ["테마 14종", "폰트 12종", "내 보관함"],
        "feat_kicker": "디테일", "feat_num": "06",
        "feat_h2": "작은 앱, <em>꽉 찬</em> 도구함.",
        "feats": [
            ["카드 테마 14종", "속보, 방송자막, 예능자막, 신문, 매거진, 재난문자 등 상황별 스타일."],
            ["디스플레이 폰트 12종", "임팩트, 손글씨, 명조, 통통 라운드 — 헤드라인마다 다른 목소리."],
            ["누끼 포토 스티커", "배경을 자동으로 제거해서 어떤 사진이든 뉴스 속 등장인물로 만들어줘요."],
            ["관심사별 예시", "학생·직장인·덕질·헬스·연애·반려동물·취준·게임·주식까지, 바로 쓰는 예시 문구."],
            ["4가지 비율", "정사각형, 피드 4:5, 스토리 9:16, 가로 16:9 — 올릴 곳에 맞춰 내보내기."],
            ["계정·광고 없음", "모든 처리는 내 기기 안에서. 무료, 아이폰 전용, 가입할 필요 없음."],
        ],
        "final_h2": "오늘의 속보를 만들어보세요.", "final_lede": "아이폰 무료.",
        "f_contact": "문의", "f_privacy": "개인정보 처리방침", "f_terms": "이용약관",
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
    return (f'<a class="store-badge" id="{el_id}" href="#" aria-label="{loc["badge_aria"]}">{APPLE_SVG}'
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
    shot_files = ["2-theme", "3-font", "4-gallery"]
    shots = "".join(
        f'<figure><div class="phone"><img src="{rel}assets/shot-{f}.png" alt="{cap}" loading="lazy"><div class="island"></div></div><figcaption>{cap}</figcaption></figure>'
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
    <a class="wordmark" href="{rel if rel else './'}"><img src="{rel}assets/icon-180.png" alt=""><span>NEWS·MAKER</span></a>
    <div class="lang">{lang_nav(loc['dir'], rel)}</div>
  </div>
</nav>

<header class="hero">
  <div class="ghost">속보</div>
  <div class="wrap">
    <div>
      <div class="kicker"><span>NEWS · MAKER</span><span class="rule"></span><span class="num">{loc['kicker_num']}</span></div>
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
      <div class="phone"><img src="{rel}assets/shot-1-hero.png" alt="{loc['hero_alt']}"><div class="island"></div></div>
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
    <div class="kicker"><span>{loc['styles_kicker']}</span><span class="rule"></span><span class="num">{loc['styles_num']}</span></div>
    <h2>{loc['styles_h2']}</h2>
    <p class="lede">{loc['styles_lede']}</p>
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
      <a href="https://www.kkirukstudio.com/legal/privacy/">{loc['f_privacy']}</a>
      <a href="https://www.kkirukstudio.com/legal/terms/">{loc['f_terms']}</a>
    </div>
    <div>© 2026 kkiruk studio</div>
  </div>
</footer>

<script>
  // After App Store approval, set the real URL here (e.g. https://apps.apple.com/app/id1234567890)
  const APP_STORE_URL = "";
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
