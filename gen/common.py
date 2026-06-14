# kkiruk studio 랜딩 생성기 — 공용 템플릿
# 사용: 각 gen_<app>.py 가 APP(테마·구조) + STRINGS(언어별 카피)를 정의하고 build_app() 호출.
# 카피 수정 → 해당 gen 스크립트 수정 → python3 gen/gen_<app>.py 재실행.

import os

SITE = os.path.join(os.path.dirname(__file__), "..")

APPLE_SVG = '<svg viewBox="0 0 384 512" aria-hidden="true"><path d="M318.7 268.7c-.2-36.7 16.4-64.4 50-84.8-18.8-26.9-47.2-41.7-84.7-44.6-35.5-2.8-74.3 20.7-88.5 20.7-15 0-49.4-19.7-76.4-19.7C63.3 141.2 4 184.8 4 273.5q0 39.3 14.4 81.2c12.8 36.7 59 126.7 107.2 125.2 25.2-.6 43-17.9 75.8-17.9 31.8 0 48.3 17.9 76.4 17.9 48.6-.7 90.4-82.5 102.6-119.3-65.2-30.7-61.7-90-61.7-91.9zm-56.6-164.2c27.3-32.4 24.8-61.9 24-72.5-24.1 1.4-52 16.4-67.9 34.9-17.5 19.8-27.8 44.3-25.6 71.9 26.1 2 49.9-11.4 69.5-34.3z"/></svg>'
GOOGLE_SVG = '<svg viewBox="0 0 512 512" class="gp" aria-hidden="true"><path d="M325.3 234.3 104.6 13l280.8 161.2-60.1 60.1zM47 0C34 6.8 25.3 19.2 25.3 35.3v441.3c0 16.1 8.7 28.5 21.7 35.3l256.6-256L47 0zm425.2 225.6-58.9-34.1-65.7 64.5 65.7 64.5 60.1-34.1c18-14.3 18-46.5-1.2-60.8zM104.6 499l280.8-161.2-60.1-60.1L104.6 499z"/></svg>'

PLAY_HL = {"zh-hans": "zh-CN", "zh-hant": "zh-TW"}  # 그 외 lang 그대로 사용

LANG_NAMES = {
    "en": "EN", "ko": "한국어", "ja": "日本語", "zh-hans": "简体中文", "zh-hant": "繁體中文",
    "es": "Español", "pt": "Português", "de": "Deutsch", "fr": "Français",
    "ru": "Русский", "th": "ไทย", "id": "Bahasa Indonesia", "vi": "Tiếng Việt",
}
HTML_LANG = {"zh-hans": "zh-Hans", "zh-hant": "zh-Hant"}
HREFLANG  = {"zh-hans": "zh-Hans", "zh-hant": "zh-Hant"}
STORE_CC  = {"ko": "kr/", "ja": "jp/", "zh-hant": "tw/"}  # 그 외 글로벌


def page_file(lang):
    return "index.html" if lang == "en" else f"{lang}.html"


def base_css(t):
    """t: theme dict — bg, ink, ink2, accent, card(optional), dark(bool)"""
    card = t.get("card", "color-mix(in srgb, var(--ink) 5%, transparent)")
    border = t.get("border", "color-mix(in srgb, var(--ink) 9%, transparent)")
    return f"""
:root {{ --bg:{t['bg']}; --ink:{t['ink']}; --ink2:{t['ink2']}; --accent:{t['accent']}; --maxw:1040px; }}
* {{ box-sizing:border-box; margin:0; padding:0; }}
body {{
  font-family:-apple-system,BlinkMacSystemFont,"Pretendard Variable",Pretendard,"Apple SD Gothic Neo","Hiragino Sans","Segoe UI",Roboto,sans-serif;
  background:var(--bg); color:var(--ink); line-height:1.55; -webkit-font-smoothing:antialiased;
}}
a {{ color:inherit; text-decoration:none; }}
.wrap {{ max-width:var(--maxw); margin:0 auto; padding:0 24px; }}
header {{ position:fixed; top:0; left:0; right:0; z-index:50;
  background:color-mix(in srgb, var(--bg) 75%, transparent);
  backdrop-filter:blur(14px); -webkit-backdrop-filter:blur(14px); }}
header .bar {{ max-width:var(--maxw); margin:0 auto; display:flex; align-items:center; justify-content:space-between; padding:14px 24px; }}
.wordmark {{ display:flex; align-items:center; gap:10px; font-weight:650; font-size:15px; }}
.wordmark img {{ width:26px; height:26px; border-radius:7px; }}
.nav-right {{ display:flex; align-items:center; gap:14px; font-size:13px; color:var(--ink2); }}
.lang-select {{ background:transparent; border:none; color:var(--ink2); font-size:13px; font-family:inherit; cursor:pointer; outline:none; }}
.lang-select option {{ color:#1A1A1A; }}
.nav-cta {{ color:var(--bg); background:var(--ink); padding:7px 14px; border-radius:99px; font-weight:600; font-size:13px; }}
.nav-cta:hover {{ opacity:.85; }}
.hero {{ min-height:92svh; display:grid; grid-template-columns:1.05fr .95fr; align-items:center; gap:44px;
  max-width:var(--maxw); margin:0 auto; padding:120px 24px 60px; }}
.kicker {{ font-size:12px; font-weight:600; letter-spacing:.14em; text-transform:uppercase; color:var(--ink2); margin-bottom:20px; }}
.hero h1 {{ font-size:clamp(32px,4.8vw,52px); font-weight:700; letter-spacing:-.02em; line-height:1.18; }}
.hero h1 em {{ font-style:normal; color:var(--accent); }}
.hero-sub {{ margin-top:18px; font-size:clamp(15px,1.6vw,17.5px); color:var(--ink2); max-width:30em; }}
.hero-cta-row {{ margin-top:32px; display:flex; align-items:center; gap:18px; flex-wrap:wrap; }}
.appstore-btn {{ display:inline-flex; align-items:center; gap:10px; background:var(--ink); color:var(--bg);
  padding:14px 24px; border-radius:14px; font-size:16px; font-weight:600; transition:transform .15s, opacity .2s; }}
.appstore-btn:hover {{ transform:translateY(-1px); opacity:.9; }}
.appstore-btn svg {{ width:18px; height:22px; fill:currentColor; }}
.rating {{ font-size:13px; color:var(--ink2); }}
.rating .stars {{ color:var(--accent); letter-spacing:1px; margin-right:6px; }}
.hero-foot {{ margin-top:16px; font-size:12.5px; color:var(--ink2); opacity:.85; }}
.hero-visual {{ display:flex; justify-content:center; align-items:center; }}
.shot {{ display:block; border-radius:26px; border:1px solid color-mix(in srgb, var(--ink) 10%, transparent);
  box-shadow:0 30px 70px -22px color-mix(in srgb, var(--ink) 45%, transparent); }}
section {{ padding:80px 0; }}
.sec-label {{ font-size:12px; font-weight:600; letter-spacing:.14em; text-transform:uppercase; color:var(--ink2); margin-bottom:14px; }}
.sec-title {{ font-size:clamp(25px,3.4vw,38px); font-weight:700; letter-spacing:-.02em; line-height:1.25; max-width:22em; }}
.features {{ display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-top:40px; }}
.feature {{ border-radius:20px; padding:26px; background:{card}; border:1px solid {border}; }}
.feature .dot {{ width:10px; height:10px; border-radius:50%; background:var(--accent); margin-bottom:14px; }}
.feature h3 {{ font-size:17px; font-weight:650; letter-spacing:-.01em; }}
.feature p {{ font-size:14px; color:var(--ink2); margin-top:7px; }}
.x-list {{ margin-top:36px; display:grid; grid-template-columns:1fr 1fr; gap:10px 24px; max-width:640px; }}
.x-item {{ font-size:15px; color:var(--ink2); display:flex; gap:10px; align-items:baseline; }}
.x-item::before {{ content:"✕"; color:var(--accent); font-weight:700; }}
.cta {{ text-align:center; padding:90px 0 110px; }}
.cta-title {{ font-size:clamp(26px,3.8vw,42px); font-weight:700; letter-spacing:-.02em; line-height:1.25; }}
.cta-sub {{ color:var(--ink2); margin-top:12px; font-size:15.5px; }}
.cta .appstore-btn {{ margin-top:30px; }}
footer {{ border-top:1px solid {border}; padding:34px 0 58px; font-size:13px; color:var(--ink2); }}
footer .cols {{ display:flex; justify-content:space-between; gap:20px; flex-wrap:wrap; }}
footer a:hover {{ color:var(--ink); }}
footer .links {{ display:flex; gap:16px; flex-wrap:wrap; }}
@media (max-width:860px) {{
  .hero {{ grid-template-columns:1fr; min-height:auto; padding-top:104px; text-align:center; gap:48px; }}
  .hero-sub {{ margin-left:auto; margin-right:auto; }}
  .hero-cta-row {{ justify-content:center; }}
  .features {{ grid-template-columns:1fr; }}
  .x-list {{ grid-template-columns:1fr; }}
  section {{ padding:60px 0; }}
}}
@media (prefers-reduced-motion:reduce) {{ * {{ animation:none !important; }} }}
"""


def store_url(app, lang):
    return f"https://apps.apple.com/{STORE_CC.get(lang, '')}app/id{app['trackId']}"


def play_url(app, lang):
    """app['play_id'](안드로이드 패키지명)가 있을 때만 Google Play URL 반환, 없으면 None."""
    pid = app.get("play_id")
    if not pid:
        return None
    return f"https://play.google.com/store/apps/details?id={pid}&hl={PLAY_HL.get(lang, lang)}"

# ── 공유 빌딩블록 (단순·리치 랜딩 모두 사용) ──────────────────
def render_head(app, lang, langs, s, icon=None, og_image=None, extra_head=""):
    """공통 <head> + <body> 시작. 리치 랜딩은 extra_head 로 추가 메타/프리로드 주입."""
    slug = app["slug"]
    htmllang = HTML_LANG.get(lang, lang)
    icon = icon or f"../icons/{slug}.png"
    # 와이드 소셜 카드: 스튜디오 루트 카드 재사용 (앱별 전용 카드는 후속).
    og_image = og_image or "https://www.kkirukstudio.com/og-image.png"
    base = f"https://www.kkirukstudio.com/{slug}"
    page_url = f"{base}/{page_file(lang)}"
    hreflangs = "\n".join(
        f'<link rel="alternate" hreflang="{HREFLANG.get(l, l)}" href="{base}/{page_file(l)}">' for l in langs
    ) + f'\n<link rel="alternate" hreflang="x-default" href="{base}/index.html">'
    hreflangs += f'\n<link rel="canonical" href="{page_url}">'
    return f"""<!DOCTYPE html>
<html lang="{htmllang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{s['title']}</title>
<meta name="description" content="{s['meta_desc']}">
<link rel="icon" type="image/png" href="{icon}">
<link rel="apple-touch-icon" href="{icon}">
{hreflangs}
<meta property="og:title" content="{s['title']}">
<meta property="og:description" content="{s['meta_desc']}">
<meta property="og:image" content="{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:url" content="{page_url}">
<meta property="og:site_name" content="kkiruk studio">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{s['title']}">
<meta name="twitter:description" content="{s['meta_desc']}">
<meta name="twitter:image" content="{og_image}">
<link rel="stylesheet" href="style.css">{extra_head}
<script src="/ga.js"></script>
</head>
<body>"""


def render_header(app, lang, langs, s, icon=None):
    """공통 고정 헤더 (워드마크 + 언어 셀렉터 + App Store CTA)."""
    slug = app["slug"]
    icon = icon or f"../icons/{slug}.png"
    store = store_url(app, lang)
    options = "\n".join(
        f'        <option value="{page_file(l)}"{" selected" if l == lang else ""}>{LANG_NAMES[l]}</option>'
        for l in langs
    )
    return f"""<header>
  <div class="bar">
    <a class="wordmark" href="{page_file(lang)}"><img src="{icon}" alt="{s['name']}">{s['name']}</a>
    <nav class="nav-right">
      <select class="lang-select" onchange="location.href=this.value" aria-label="Language">
{options}
      </select>
      <a class="nav-cta" href="{store}" target="_blank" rel="noopener">App Store</a>
    </nav>
  </div>
</header>"""


def render_footer(app, lang, langs, s):
    """공통 푸터 (© + 홈·문의·개인정보·약관 + 언어 링크)."""
    footer_langs = " ".join(
        f'<a href="{page_file(l)}">{LANG_NAMES[l]}</a>' for l in langs if l != lang
    )
    return f"""<footer>
  <div class="wrap cols">
    <span>© kkiruk studio</span>
    <nav class="links">
      <a href="/">kkiruk studio</a>
      <a href="mailto:kkirukstudio.help@gmail.com">{s['f_contact']}</a>
      <a href="https://kkiruk-studio.github.io/privacy-policy-app/" target="_blank" rel="noopener">{s['f_privacy']}</a>
      <a href="https://kkiruk-studio.github.io/terms-of-service-app/" target="_blank" rel="noopener">{s['f_terms']}</a>
      {footer_langs}
    </nav>
  </div>
</footer>"""


def render_page(app, lang, s, langs):
    store = store_url(app, lang)
    # Google Play 버튼 — play_id 있는 앱만. 없으면 빈 문자열이라 iOS 전용 앱 출력은 불변.
    play = play_url(app, lang)
    play_btn = play_btn_cta = ""
    if play:
        plabel = s.get("cta_play", "Google Play")
        play_btn = f'\n      <a class="appstore-btn" href="{play}" target="_blank" rel="noopener">{GOOGLE_SVG}{plabel}</a>'
        play_btn_cta = f'\n    <a class="appstore-btn" href="{play}" target="_blank" rel="noopener">{GOOGLE_SVG}{plabel}</a>'

    feats = "\n".join(
        f'      <div class="feature"><div class="dot"></div><h3>{t}</h3><p>{d}</p></div>'
        for t, d in s["features"]
    )

    anti = ""
    if s.get("anti_items"):
        items = "\n".join(f'      <div class="x-item">{x}</div>' for x in s["anti_items"])
        anti = f"""
<section>
  <div class="wrap">
    <p class="sec-label">{s['anti_label']}</p>
    <h2 class="sec-title">{s['anti_title']}</h2>
    <div class="x-list">
{items}
    </div>
  </div>
</section>"""

    rating = f'<span class="rating"><span class="stars">★★★★★</span>{app["rating"]}</span>' if app.get("rating") else ""

    return f"""{render_head(app, lang, langs, s)}

{render_header(app, lang, langs, s)}

<main>
<div class="hero">
  <div class="hero-copy">
    <p class="kicker">{s['kicker']}</p>
    <h1>{s['h1']}</h1>
    <p class="hero-sub">{s['sub']}</p>
    <div class="hero-cta-row">
      <a class="appstore-btn" href="{store}" target="_blank" rel="noopener">{APPLE_SVG}{s['cta']}</a>{play_btn}
      {rating}
    </div>
    <p class="hero-foot">{s['foot']}</p>
  </div>
  <div class="hero-visual" aria-hidden="true">
{app['hero_html'].replace('{lang}', lang)}
  </div>
</div>

<section>
  <div class="wrap">
    <p class="sec-label">{s['feat_label']}</p>
    <h2 class="sec-title">{s['feat_title']}</h2>
    <div class="features">
{feats}
    </div>
  </div>
</section>
{anti}
<section class="cta">
  <div class="wrap">
    <h2 class="cta-title">{s['cta_title']}</h2>
    <p class="cta-sub">{s['cta_sub']}</p>
    <a class="appstore-btn" href="{store}" target="_blank" rel="noopener">{APPLE_SVG}{s['cta']}</a>{play_btn_cta}
  </div>
</section>
</main>

{render_footer(app, lang, langs, s)}

</body>
</html>
"""


def build_app(app, strings):
    langs = list(strings.keys())
    outdir = os.path.join(SITE, app["slug"])
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "style.css"), "w") as f:
        f.write(base_css(app["theme"]) + app.get("extra_css", ""))
    for lang in langs:
        with open(os.path.join(outdir, page_file(lang)), "w") as f:
            f.write(render_page(app, lang, strings[lang], langs))
    print(f"✓ {app['slug']}: {len(langs)} pages ({', '.join(langs)})")
