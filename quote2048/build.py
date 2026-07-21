#!/usr/bin/env python3
"""Quote 2048 landing — the game sells itself.
One screen: an animated merge on a real board, one line of copy, done.
Usage: python3 build.py
"""
import pathlib

ROOT = pathlib.Path(__file__).parent
BASE_URL = "https://www.kkirukstudio.com/quote2048/"
LANG_LABELS = [("", "EN"), ("ko/", "한국어"), ("ja/", "日本語"), ("zh-hans/", "简体"), ("zh-hant/", "繁體")]

L = {
 "en": dict(dir="", lang="en",
    title="Quote 2048 — 2048, played with quotes",
    desc="The classic 2048 — but every tile is a quote. Merge two matching lines and a greater quote takes their place. Reach 2048 to meet the crown quote. And 2048 isn't the end.",
    h1="2048,<br>played with <em>quotes</em>.",
    sub="Merge two matching lines — a greater quote takes their place.",
    reveal="And when you make the 2048 tile —", tease="2048 isn't the end.",
    soon="COMING SOON · iOS",
    tile_a="Well begun<br>is half done", tile_b="Well begun<br>is half done",
    tile_m="It's never<br>too late",
    crown="A great tree grows<br>from a small sprout",
    crown_meta="— Laozi",
    f_privacy="Privacy", f_terms="Terms", f_contact="Contact"),
 "ko": dict(dir="ko/", lang="ko",
    title="명언 2048 — 명언으로 하는 2048",
    desc="알던 그 2048 — 그런데 타일이 전부 명언입니다. 같은 문장 두 개를 합치면 한 단계 위의 명언이 나타나고, 2048에서 왕관 명언을 만납니다. 그리고 2048이 끝이 아닙니다.",
    h1="명언으로 하는<br><em>2048.</em>",
    sub="같은 문장 두 개를 합치면, 한 단계 위의 명언이 나타납니다.",
    reveal="그리고 2048 타일을 만들면 —", tease="2048이 끝이 아닙니다.",
    soon="곧 출시 · iOS",
    tile_a="시작이<br>반이다", tile_b="시작이<br>반이다",
    tile_m="늦은 때는<br>없다",
    crown="큰 나무도 작은 싹에서<br>자란다",
    crown_meta="— 노자",
    f_privacy="개인정보", f_terms="이용약관", f_contact="문의"),
 "ja": dict(dir="ja/", lang="ja",
    title="名言2048 — 名言で遊ぶ2048",
    desc="おなじみの2048 — ただしタイルはすべて名言。同じ文をふたつ合わせると、ひとつ上の名言が現れる。2048で王冠の名言に出会う。そして2048で終わりではない。",
    h1="名言で遊ぶ<br><em>2048。</em>",
    sub="同じ文をふたつ合わせると、ひとつ上の名言が現れます。",
    reveal="そして2048のタイルを作ると —", tease="2048で終わりではありません。",
    soon="近日公開 · iOS",
    tile_a="始まりは<br>半分の成功", tile_b="始まりは<br>半分の成功",
    tile_m="遅すぎることは<br>ない",
    crown="合抱の木も<br>毫末より生ず",
    crown_meta="— 老子",
    f_privacy="プライバシー", f_terms="利用規約", f_contact="お問い合わせ"),
 "zh-hans": dict(dir="zh-hans/", lang="zh-Hans",
    title="名言2048 — 用名言玩的2048",
    desc="熟悉的2048 — 但每个方块都是一句名言。合并两句相同的话，出现更高一级的名言；抵达2048，遇见王冠名言。而2048并不是终点。",
    h1="用名言玩的<br><em>2048。</em>",
    sub="合并两句相同的话，出现更高一级的名言。",
    reveal="当你合成出2048方块时 —", tease="2048并不是终点。",
    soon="即将上线 · iOS",
    tile_a="好的开始<br>是成功的一半", tile_b="好的开始<br>是成功的一半",
    tile_m="一切都<br>不算晚",
    crown="合抱之木<br>生于毫末",
    crown_meta="— 老子",
    f_privacy="隐私政策", f_terms="服务条款", f_contact="联系"),
 "zh-hant": dict(dir="zh-hant/", lang="zh-Hant",
    title="名言2048 — 用名言玩的2048",
    desc="熟悉的2048 — 但每個方塊都是一句名言。合併兩句相同的話，出現更高一級的名言；抵達2048，遇見王冠名言。而2048並不是終點。",
    h1="用名言玩的<br><em>2048。</em>",
    sub="合併兩句相同的話，出現更高一級的名言。",
    reveal="當你合成出2048方塊時 —", tease="2048並不是終點。",
    soon="即將上線 · iOS",
    tile_a="好的開始<br>是成功的一半", tile_b="好的開始<br>是成功的一半",
    tile_m="一切都<br>不算晚",
    crown="合抱之木<br>生於毫末",
    crown_meta="— 老子",
    f_privacy="隱私政策", f_terms="服務條款", f_contact="聯絡"),
}

def hreflang():
    t=[f'<link rel="alternate" hreflang="{l}" href="{BASE_URL}{d}">' for d,l in [("","en"),("ko/","ko"),("ja/","ja"),("zh-hans/","zh-Hans"),("zh-hant/","zh-Hant")]]
    t.append(f'<link rel="alternate" hreflang="x-default" href="{BASE_URL}">')
    return "\n".join(t)

def nav(active, rel):
    out=[]
    for d,label in LANG_LABELS:
        href=f"{rel}{d}" if d else (rel if rel else "./")
        out.append(f'<a{" class=on" if d==active else ""} href="{href}">{label}</a>')
    return '<nav class="langs">'+" ".join(out)+"</nav>"

def render(key):
    o=L[key]; rel="../" if o["dir"] else ""
    html=f"""<!DOCTYPE html>
<html lang="{o['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{o['title']}</title>
<meta name="description" content="{o['desc']}">
<meta property="og:title" content="{o['title']}">
<meta property="og:description" content="{o['desc']}">
<meta property="og:image" content="{BASE_URL}assets/icon-512.png">
<meta property="og:type" content="website">
<link rel="canonical" href="{BASE_URL}{o['dir']}">
{hreflang()}
<link rel="icon" type="image/png" href="{rel}assets/icon-180.png">
<link rel="apple-touch-icon" href="{rel}assets/icon-180.png">
<link rel="stylesheet" href="{rel}assets/style.css">
<script defer src="/ga.js"></script>
</head>
<body>
<header class="top">
  <a class="mark" href="{rel if rel else './'}"><img src="{rel}assets/icon-180.png" alt=""><span>QUOTE·2048</span></a>
  {nav(o['dir'], rel)}
</header>

<main>
  <h1>{o['h1']}</h1>
  <p class="sub">{o['sub']}</p>

  <div class="stage" aria-hidden="true">
    <div class="cell c1"></div><div class="cell c2"></div><div class="cell c3"></div><div class="cell c4"></div>
    <div class="tile a">{o['tile_a']}</div>
    <div class="tile b">{o['tile_b']}</div>
    <div class="tile m">{o['tile_m']}</div>
  </div>

  <p class="reveal">{o['reveal']}</p>

  <blockquote class="crown">
    <p>{o['crown']}</p>
    <cite>{o['crown_meta']}</cite>
    <span class="badge">👑 2048</span>
  </blockquote>

  <p class="tease">{o['tease']}<span class="dots"> ✦ 4096 · ⭐ 131072</span></p>

  <p class="soon">{o['soon']}</p>
</main>

<footer>
  <span>© kkiruk studio</span>
  <a href="https://kkiruk-studio.github.io/privacy-policy-app/">{o['f_privacy']}</a>
  <a href="https://kkiruk-studio.github.io/terms-of-service-app/">{o['f_terms']}</a>
  <a href="mailto:kkirukstudio@gmail.com">{o['f_contact']}</a>
</footer>
</body>
</html>"""
    out=ROOT/o["dir"] if o["dir"] else ROOT
    out.mkdir(exist_ok=True)
    (out/"index.html").write_text(html, encoding="utf-8")
    print("wrote", (out/"index.html").relative_to(ROOT))

if __name__ == "__main__":
    for k in L: render(k)
