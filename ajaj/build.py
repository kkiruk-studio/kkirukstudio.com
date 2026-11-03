#!/usr/bin/env python3
"""Generate ajaj landing pages (ar default at /ajaj/, en at /ajaj/en/).

Usage: python3 build.py   (generated HTML is not edited by hand)
"""
import json, pathlib

ROOT = pathlib.Path(__file__).parent
BASE_URL = "https://www.kkirukstudio.com/ajaj/"
OG_IMAGE = BASE_URL + "og.png"
APP_STORE_URL = ""  # TODO: fill after App Store approval (pre-release: "coming soon" button)

LEVEL_COLORS = ["#9a9a8c", "#c9a766", "#B8792A", "#8f5a16", "#5e3a0c"]

LOCALES = {
    "ar": {
        "dir": "", "lang": "ar", "rtl": True, "shot": "ar",
        "title": "عجاج: طقس وغبار ورياح — تطبيق طقس للخليج",
        "desc": "هل الغبار اليوم أسوأ من أمس؟ ومن أي جهة تأتي الريح؟ عجاج يجيبك بنظرة واحدة. تطبيق طقس لدول الخليج يضع الغبار والرياح أولاً.",
        "og_title": "عجاج — الغبار والرياح بنظرة واحدة",
        "kicker": "طقس الخليج",
        "levels": ["صافٍ", "غبار خفيف", "غبار", "غبار كثيف", "عاصفة ترابية"],
        "compare": "هل الغبار اليوم أسوأ من أمس؟",
        "sub": "عجاج تطبيق طقس لدول الخليج يضع الغبار والرياح أولاً. افتح التطبيق وسترى الجواب بخط كبير، وهل هو أسوأ أو أنظف من أمس في نفس الساعة.",
        "soon": "قريباً على App Store", "note": "مجاني · iPhone",
        "hero_alt": "الشاشة الرئيسية لتطبيق عجاج",
        "lv_kicker": "مستوى الغبار", "lv_h2": "خمس مستويات، <em>كلمة واحدة</em>.",
        "feat_kicker": "التفاصيل", "feat_h2": "كل ما يهمّك <em>عن الجو.</em>",
        "feats": [
            ["مستوى الغبار الآن", "صافٍ، غبار خفيف، غبار، غبار كثيف، عاصفة ترابية."],
            ["مقارنة مع أمس", "هل هو أسوأ أو أنظف من أمس في نفس الساعة."],
            ["توقعات الساعات القادمة", "متى يبدأ الغبار ومتى يخفّ."],
            ["اتجاه الرياح وسرعتها", "من أي جهة تأتي الريح وبأي قوة."],
            ["بوصلة الرياح", "وجّه هاتفك لتعرف من أين يأتي الغبار فعلاً، وعندما تواجه الريح يهتز الهاتف."],
            ["الحرارة والرؤية والمزيد", "درجة الحرارة والحرارة المحسوسة والرؤية والرطوبة والأشعة فوق البنفسجية."],
        ],
        "region": "صُمّم للسعودية والإمارات والكويت وبقية الخليج. يعرض الأرقام بحسب إعدادات جهازك.",
        "data": "مصدر البيانات: Open-Meteo (نماذج CAMS لجودة الهواء وتوقعات الطقس). القيم تقديرية وقد تختلف عن القياس المحلي.",
        "final_h2": "الغبار والرياح، <em>بنظرة واحدة</em>.",
        "support_h": "الدعم", "support_p": "أسئلة أو ملاحظات؟ راسلنا:",
        "f_privacy": "سياسة الخصوصية", "f_terms": "الشروط",
    },
    "en": {
        "dir": "en/", "lang": "en", "rtl": False, "shot": "en",
        "title": "Ajaj: Dust & Wind Weather — Gulf sandstorm forecast",
        "desc": "Is the dust worse than yesterday? Which way is the wind coming from? Ajaj answers at a glance. A Gulf weather app that puts dust and wind first.",
        "og_title": "Ajaj — Dust and wind at a glance",
        "kicker": "GULF WEATHER",
        "levels": ["Clear", "Light dust", "Dusty", "Heavy dust", "Dust storm"],
        "compare": "Is the dust worse than yesterday?",
        "sub": "Ajaj is a Gulf weather app that puts dust and wind first. Open it and the answer is right there in big type, and whether it is worse or cleaner than yesterday at the same hour.",
        "soon": "Coming soon to the App Store", "note": "FREE · IPHONE",
        "hero_alt": "Ajaj main screen",
        "lv_kicker": "DUST LEVELS", "lv_h2": "Five levels, <em>one word</em>.",
        "feat_kicker": "DETAILS", "feat_h2": "Everything you need <em>about the air.</em>",
        "feats": [
            ["Dust level now", "Clear, Light dust, Dusty, Heavy dust, Dust storm."],
            ["Compared with yesterday", "Worse or cleaner than yesterday at the same hour."],
            ["Dust over the next hours", "When it starts and when it eases."],
            ["Wind direction and speed", "Where the wind is coming from, and how hard."],
            ["Wind compass", "Point your phone to see where the dust is really coming from, and feel a tap when you face the wind."],
            ["Temperature and more", "Temperature, feels like, visibility, humidity and UV."],
        ],
        "region": "Made for Saudi Arabia, the UAE, Kuwait and the rest of the Gulf. Numbers follow your device settings.",
        "data": "Data: Open-Meteo (CAMS air-quality and weather models). Values are estimates and may differ from local measurements.",
        "final_h2": "Dust and wind, <em>at a glance</em>.",
        "support_h": "Support", "support_p": "Questions or feedback? Write to us:",
        "f_privacy": "Privacy", "f_terms": "Terms",
    },
}

LANG_LABELS = [("", "العربية"), ("en/", "EN")]


def render(key):
    loc = LOCALES[key]
    rel = "../" if loc["dir"] else ""
    canonical = BASE_URL + loc["dir"]
    hreflang = (f'<link rel="alternate" hreflang="x-default" href="{BASE_URL}">\n'
                f'<link rel="alternate" hreflang="ar" href="{BASE_URL}">\n'
                f'<link rel="alternate" hreflang="en" href="{BASE_URL}en/">')
    nav = "".join(f'<a href="{(rel + d) if d else (rel or "./")}"{" class=cur" if d == loc["dir"] else ""} hreflang="{"en" if d else "ar"}">{l}</a>' for d, l in LANG_LABELS)
    button = (f'<a class="btn-soon" id="storeLink" href="#" aria-disabled="true">{loc["soon"]}</a>')
    levels = "".join(f'<div style="color:{c}">{w}</div>' for w, c in zip(loc["levels"], LEVEL_COLORS))
    feats = "".join(f'<div class="feat"><h3>{h}</h3><p>{p}</p></div>' for h, p in loc["feats"])
    jsonld = json.dumps({"@context": "https://schema.org", "@type": "MobileApplication",
        "name": loc["title"].split(" — ")[0], "operatingSystem": "iOS", "applicationCategory": "WeatherApplication",
        "description": loc["desc"], "url": canonical, "inLanguage": loc["lang"],
        "author": {"@type": "Organization", "name": "kkiruk studio", "url": "https://www.kkirukstudio.com/"}},
        ensure_ascii=False)
    html = f"""<!doctype html>
<html lang="{loc['lang']}" dir="{'rtl' if loc['rtl'] else 'ltr'}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{loc['title']}</title>
<meta name="description" content="{loc['desc']}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{loc['og_title']}">
<meta property="og:description" content="{loc['desc']}">
<meta property="og:image" content="{OG_IMAGE}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="kkiruk studio">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{loc['og_title']}">
<meta name="twitter:description" content="{loc['desc']}">
<meta name="twitter:image" content="{OG_IMAGE}">
{hreflang}
<link rel="icon" type="image/png" href="{rel}assets/icon-180.png">
<link rel="apple-touch-icon" href="{rel}assets/icon-180.png">
<link rel="stylesheet" href="{rel}assets/style.css">
<script type="application/ld+json">{jsonld}</script>
<script src="/ga.js"></script>
</head>
<body>
<nav><div class="wrap">
  <a class="wordmark" href="{rel or './'}"><img src="{rel}assets/icon-180.png" alt=""><span>{'عجاج' if loc['rtl'] else 'Ajaj'}</span></a>
  <div class="lang">{nav}</div>
</div></nav>

<header class="hero"><div class="wrap">
  <div class="kicker"><span>{loc['kicker']}</span><span class="rule"></span><span>AJAJ</span></div>
  <div class="hero-grid">
    <div>
      <div class="bigword" id="word" aria-live="off">{loc['levels'][2]}</div>
      <p class="compare">{loc['compare']}</p>
      <p class="sub">{loc['sub']}</p>
      <div class="cta">{button}<span class="note">{loc['note']}</span></div>
    </div>
    <div class="phone"><img src="{rel}assets/shot-{loc['shot']}.png" alt="{loc['hero_alt']}" width="900" height="1957"></div>
  </div>
</div></header>

<section><div class="wrap">
  <div class="kicker"><span>{loc['lv_kicker']}</span><span class="rule"></span><span>05</span></div>
  <h2>{loc['lv_h2']}</h2>
  <div class="levels">{levels}</div>
</div></section>

<section><div class="wrap">
  <div class="kicker"><span>{loc['feat_kicker']}</span><span class="rule"></span><span>06</span></div>
  <h2>{loc['feat_h2']}</h2>
  <div class="grid6">{feats}</div>
  <p class="disclaimer" style="margin-top:28px">{loc['region']}<br>{loc['data']}</p>
</div></section>

<section><div class="wrap">
  <div class="kicker"><span>{loc['support_h']}</span><span class="rule"></span><span>@</span></div>
  <h2 style="font-size:clamp(22px,3vw,30px)">{loc['support_p']} <a href="mailto:kkirukstudio.help@gmail.com" style="color:var(--dust-deep)">kkirukstudio.help@gmail.com</a></h2>
</div></section>

<section class="final"><div class="wrap">
  <h2>{loc['final_h2']}</h2>
  <div class="cta">{button.replace('storeLink', 'storeLink2')}</div>
</div></section>

<footer><div class="wrap">
  <strong>kkiruk studio</strong>
  <div>
    <a href="mailto:kkirukstudio.help@gmail.com">kkirukstudio.help@gmail.com</a>
    <a href="/legal/privacy/">{loc['f_privacy']}</a>
    <a href="/legal/terms/">{loc['f_terms']}</a>
  </div>
  <div>© 2026 kkiruk studio</div>
</div></footer>

<script>
  // After App Store approval, set the real URL (also set APP_STORE_URL in build.py)
  const APP_STORE_URL = "{APP_STORE_URL}";
  if (APP_STORE_URL) {{
    for (const id of ["storeLink", "storeLink2"]) {{
      const a = document.getElementById(id);
      a.href = APP_STORE_URL; a.textContent = "App Store"; a.removeAttribute("aria-disabled"); a.style.cursor = "pointer";
    }}
  }}
  const words = {json.dumps(loc['levels'], ensure_ascii=False)};
  const colors = {json.dumps(LEVEL_COLORS)};
  const el = document.getElementById("word");
  const show = (i) => {{ el.textContent = words[i]; el.style.color = colors[i]; }};
  show(2);
  if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {{
    let i = 2;
    setInterval(() => {{ i = (i + 1) % words.length; show(i); }}, 2200);
  }}
</script>
</body>
</html>
"""
    out = ROOT / loc["dir"] / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)} ({len(html)} bytes)")


for k in LOCALES:
    render(k)
