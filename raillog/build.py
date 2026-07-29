#!/usr/bin/env python3
"""Generate index.html for every locale from one template.

Usage: python3 build.py
Output: ./index.html (ko), ./en/index.html
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).parent
BASE_URL = "https://www.kkirukstudio.com/raillog/"
APP_STORE_URL = "https://apps.apple.com/kr/app/id6794330967"
DOTS = 9  # stations drawn in the hero transit-line demo (per line cycle)
PROGRESS_TOTAL = 55  # denominator shown in the top progress counter (matches "55 lines")

# One page-spine "stop" per major section, in document order:
# hero, step-01, step-02, step-03, stats, shots, feats, pro, final.
# Value = index into loc["spine_lines"] (6 real line colors, in spec order).
# A label is only drawn on the stop where a new color run begins.
STOP_LINE_IDX = [0, 0, 1, 1, 2, 3, 4, 4, 5]

APPLE_SVG = '<svg viewBox="0 0 384 512" aria-hidden="true"><path d="M318.7 268.7c-.2-36.7 16.4-64.4 50-84.8-18.8-26.9-47.2-41.7-84.7-44.6-35.5-2.8-74.3 20.7-88.5 20.7-15 0-49.4-19.7-76.4-19.7C63.3 141.2 4 184.8 4 273.5q0 39.3 14.4 81.2c12.8 36.7 59 126.7 107.2 125.2 25.2-.6 43-17.9 75.8-17.9 31.8 0 48.3 17.9 76.4 17.9 48.6-.7 90.4-82.5 102.6-119.3-65.2-30.7-61.7-90-61.7-91.9zm-56.6-164.2c27.3-32.4 24.8-61.9 24-72.5-24.1 1.4-52 16.4-67.9 34.9-17.5 19.8-27.8 44.3-25.6 71.9 26.1 2 49.9-11.4 69.5-34.3z"/></svg>'

LANG_LABELS = [("", "한국어"), ("en/", "EN")]

# Real Korean rail line colors, reused across the palette chips and the hero demo.
LINE_HEXES = {
    "1": "#0052A4", "2": "#00A84D", "3": "#EF7C1C", "4": "#00A5DE", "5": "#996CAC",
    "sinbundang": "#D4003B", "arex": "#0090D2", "ktx": "#00498A", "srt": "#762F90",
    "gyeongchun": "#178C72", "suinbundang": "#FABE00",
}

LOCALES = {
    "ko": {
        "dir": "", "lang": "ko", "font": '"Apple SD Gothic Neo", "Pretendard"', "shots": "ko",
        "title": "레일로그 — 탄 노선이, 색으로 남는다",
        "desc": "역을 탭해 방문 체크. 탄 노선은 지도에서 실제 노선 색으로 칠해지고 스탬프북에 쌓입니다. 전국 17개 사업자·55개 노선, 완주하면 인장 카드가 등장합니다.",
        "og_title": "레일로그 — 철도 답사 기록",
        "og_desc": "탄 노선이 지도에서 실제 색으로 칠해지고, 스탬프북에 쌓입니다.",
        "kicker_num": "철도 답사 기록",
        "h1": "탄 노선이,<br><em>색으로</em> 남는다.",
        "sub": "역을 탭하면 방문 체크. 탄 노선은 지도에서 진짜 노선 색으로 칠해지고, 스탬프북에 쌓입니다. 전국 17개 사업자·55개 노선 — 1호선부터 KTX·SRT까지.",
        "badge_small": "다운로드는", "note": "무료 · iPhone · 계정 불필요",
        "badge_aria": "App Store에서 다운로드",
        "hero_chips": [["17", "개 사업자"], ["55", "개 노선"], ["완주", "인장 카드"]],
        "hero_alt": "레일로그 지도 화면 — 탄 노선이 실제 노선 색으로 칠해진 모습",
        "spine_lines": [
            (LINE_HEXES["1"], "1호선"), (LINE_HEXES["2"], "2호선"),
            (LINE_HEXES["sinbundang"], "신분당선"), (LINE_HEXES["arex"], "공항철도"),
            (LINE_HEXES["ktx"], "KTX"), (LINE_HEXES["srt"], "SRT"),
        ],
        "how_kicker": "사용 방법",
        "how_h2": "역을 탭하는 순간, <em>지도가 색으로 채워진다</em>.",
        "step2_unridden": "안 탄 노선", "step2_ridden": "탄 노선",
        "steps": [
            ["기록", "역을 탭해 방문 체크", "예전에 탔던 노선도 소급해서 기록할 수 있어요. 역마다 사진과 메모도 남깁니다."],
            ["지도", "탄 노선이 실제 색으로", "탄 노선이 지도에서 진짜 노선 색으로 칠해집니다. 안 탄 노선만 보는 필터로 다음 답사도 계획하세요."],
            ["수집", "스탬프북에 쌓인다", "방문한 역이 스탬프로 쌓이고, 노선을 끝까지 타면 「전구간 완주」 인장 카드가 등장합니다."],
        ],
        "value_kicker": "전국 데이터", "value_num": "OSM 기반",
        "value_h2": "전국 철도를, <em>숫자</em>로.",
        "value_lede": "17개 사업자, 55개 노선, 1,191개 역 — 지하철부터 KTX·SRT까지 한 지도에서 답사합니다.",
        "stats": [["17", "사업자"], ["55", "노선"], ["1,191", "역"]],
        "line_chips": [
            ["1호선", LINE_HEXES["1"]], ["2호선", LINE_HEXES["2"]], ["3호선", LINE_HEXES["3"]],
            ["4호선", LINE_HEXES["4"]], ["5호선", LINE_HEXES["5"]], ["신분당선", LINE_HEXES["sinbundang"]],
            ["공항철도", LINE_HEXES["arex"]], ["KTX", LINE_HEXES["ktx"]], ["SRT", LINE_HEXES["srt"]],
            ["경춘선", LINE_HEXES["gyeongchun"]], ["수인분당선", LINE_HEXES["suinbundang"]],
        ],
        "shots_kicker": "화면", "shots_num": "IOS",
        "shots_h2": "꾸미기보다 <em>답사 도구</em>로.",
        "shots_caps": ["전국 철도를 한 지도에", "탄 역이 스탬프가 된다", "전구간 완주 인장"],
        "feat_kicker": "디테일", "feat_num": "06",
        "feat_h2": "작은 디테일까지 <em>기록</em>.",
        "feats": [
            ["사진·메모 첨부", "역마다 사진과 메모를 남길 수 있어요."],
            ["GPS로 근처 역 찾기", "GPS로 근처 역을 찾아 그 자리에서 기록합니다."],
            ["방문일 소급 입력", "방문일은 자유롭게 선택 — 예전에 탔던 노선도 소급해서 기록."],
            ["9:16 스토리 공유 카드", "완주 카드를 9:16 비율로 인스타그램 스토리에 바로 공유."],
            ["iCloud 동기화 · 백업", "iCloud로 기기를 바꿔도 기록이 이어지고, JSON·CSV로 백업·내보내기."],
            ["계정 불필요 · 오프라인", "가입 없이 바로 시작하고, 오프라인에서도 기록할 수 있어요."],
        ],
        "pro_kicker": "PRO", "pro_num": "선택 사항",
        "pro_h2": "무료로 시작해서, <em>필요할 때만</em> Pro.",
        "pro_lede": "노선 열람 · 승차 기록 · 스탬프북 · iCloud 동기화는 모두 무료입니다.",
        "prices": [["₩1,900", "월간"], ["₩9,900", "연간"], ["₩19,000", "평생"]],
        "pro_note": "Pro는 <strong>즐겨찾기 무제한, 상세 통계·17개 광역시도 히트맵, 워터마크 제거 공유 카드, PDF 스탬프북</strong>을 더합니다.",
        "final_h2": "탄 노선이, 색으로 남는다.", "final_lede": "iPhone 무료.",
        "f_contact": "문의", "f_privacy": "개인정보 처리방침", "f_terms": "이용약관",
        "data_note": "노선·역 데이터는 OpenStreetMap 등 공개 데이터를 기반으로 합니다.",
        "lines": [
            [LINE_HEXES["2"], "서울 2호선", 43],
            [LINE_HEXES["1"], "서울 1호선", 100],
            [LINE_HEXES["sinbundang"], "신분당선", 16],
            [LINE_HEXES["arex"], "공항철도", 14],
        ],
        "unit": "역",
        "stamp_html": "완주",
    },
    "en": {
        "dir": "en/", "lang": "en", "font": None, "shots": "en",
        "title": "Raillog — Every Line You Ride, In Color",
        "desc": "Tap a station to log it. Ridden lines turn their real color on the map and stack up as stamps in your book. Covers all 17 operators and 55 lines across Korea's rail network.",
        "og_title": "Raillog — Korean Rail Ride Log",
        "og_desc": "Ridden lines painted in their real color. Every station, a stamp.",
        "kicker_num": "RIDE LOG",
        "h1": "Every line you ride,<br>painted in <em>its color</em>.",
        "sub": "Tap a station to log it. Ridden lines turn their real color on the map, and every stop becomes a stamp in your book. Built for Korea's rail network — 17 operators, 55 lines, from the Seoul subway to the KTX and SRT.",
        "badge_small": "Download on the", "note": "FREE · IPHONE · NO ACCOUNT",
        "badge_aria": "Download on the App Store",
        "hero_chips": [["17", "operators"], ["55", "lines"], ["★", "Full Route seal"]],
        "hero_alt": "Raillog map screen showing ridden lines painted in their real line colors",
        "spine_lines": [
            (LINE_HEXES["1"], "LINE 1"), (LINE_HEXES["2"], "LINE 2"),
            (LINE_HEXES["sinbundang"], "SINBUNDANG"), (LINE_HEXES["arex"], "AREX"),
            (LINE_HEXES["ktx"], "KTX"), (LINE_HEXES["srt"], "SRT"),
        ],
        "how_kicker": "HOW IT WORKS",
        "how_h2": "Tap a station, and the <em>map fills in with color</em>.",
        "step2_unridden": "UNRIDDEN", "step2_ridden": "RIDDEN",
        "steps": [
            ["LOG", "Tap a station to check it off", "Backfill rides from years ago — pick any visit date. Attach a photo or note to any station."],
            ["MAP", "Ridden lines, real colors", "Every line you've ridden gets painted in its real color. Filter to unridden lines to plan your next trip."],
            ["COLLECT", "Stamps stack up", "Every station you visit becomes a stamp. Finish a line end-to-end and a Full Route seal card appears."],
        ],
        "value_kicker": "NATIONWIDE DATA", "value_num": "OSM-BASED",
        "value_h2": "Korea's rail network, <em>by the numbers</em>.",
        "value_lede": "17 operators, 55 lines, 1,191 stations — from the subway to the KTX and SRT, all logged on one map.",
        "stats": [["17", "OPERATORS"], ["55", "LINES"], ["1,191", "STATIONS"]],
        "line_chips": [
            ["Line 1", LINE_HEXES["1"]], ["Line 2", LINE_HEXES["2"]], ["Line 3", LINE_HEXES["3"]],
            ["Line 4", LINE_HEXES["4"]], ["Line 5", LINE_HEXES["5"]], ["Sinbundang", LINE_HEXES["sinbundang"]],
            ["AREX", LINE_HEXES["arex"]], ["KTX", LINE_HEXES["ktx"]], ["SRT", LINE_HEXES["srt"]],
            ["Gyeongchun", LINE_HEXES["gyeongchun"]], ["Suin-Bundang", LINE_HEXES["suinbundang"]],
        ],
        "shots_kicker": "SCREENS", "shots_num": "IOS",
        "shots_h2": "Built for logging, <em>not just looking</em>.",
        "shots_caps": ["All of Korea's rail on one map", "Every station, a stamp", "The Full Route seal"],
        "feat_kicker": "DETAILS", "feat_num": "06",
        "feat_h2": "Small app, <em>deliberate</em> details.",
        "feats": [
            ["Photos & notes", "Attach a photo or note to any station you log."],
            ["Find nearby stations by GPS", "GPS finds nearby stations so you can log them on the spot."],
            ["Backdate any visit", "Pick any date — backfill that Seoul subway trip from years ago."],
            ["9:16 story share cards", "Share your Full Route seal card straight to Instagram Stories."],
            ["iCloud sync & backup", "iCloud sync carries your log across devices; export as JSON or CSV."],
            ["No account, works offline", "Start logging with no sign-up, even without a connection."],
        ],
        "pro_kicker": "PRO", "pro_num": "OPTIONAL",
        "pro_h2": "Free to start. <em>Pro only if you need it</em>.",
        "pro_lede": "Browsing lines, logging rides, the stamp book, and iCloud sync are all free.",
        "prices": [["₩1,900", "MONTHLY"], ["₩9,900", "YEARLY"], ["₩19,000", "LIFETIME"]],
        "pro_note": "Pro adds <strong>unlimited favorite lines, detailed stats with a 17-province heatmap, watermark-free share cards, and a printable PDF stamp book</strong>. Priced in Korean won (KRW), the currency of the Korea App Store.",
        "final_h2": "Every line you ride, painted in its color.", "final_lede": "Free on iPhone.",
        "f_contact": "Contact", "f_privacy": "Privacy", "f_terms": "Terms",
        "data_note": "Line and station data are based on open data such as OpenStreetMap.",
        "lines": [
            [LINE_HEXES["2"], "Seoul Line 2", 43],
            [LINE_HEXES["1"], "Seoul Line 1", 100],
            [LINE_HEXES["sinbundang"], "Sinbundang Line", 16],
            [LINE_HEXES["arex"], "AREX", 14],
        ],
        "unit": " stations",
        "stamp_html": "FULL<br>ROUTE",
    },
}

SCRIPT_JS = """
  const APP_STORE_URL = "%%APPSTORE%%";
  if (APP_STORE_URL) {
    document.getElementById("storeLink").href = APP_STORE_URL;
    document.getElementById("storeLink2").href = APP_STORE_URL;
  }

  const LINES = %%LINES%%;
  const UNIT = %%UNIT%%;
  const DOTS = %%DOTS%%;

  const dotEl = document.getElementById("demoDot");
  const nameEl = document.getElementById("demoName");
  const countEl = document.getElementById("demoCount");
  const totalEl = document.getElementById("demoTotal");
  const trackEl = document.getElementById("demoTrack");
  const stampEl = document.getElementById("demoStamp");

  if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

    function buildTrack() {
      trackEl.innerHTML = "";
      for (let i = 0; i < DOTS; i++) {
        trackEl.appendChild(Object.assign(document.createElement("span"), { className: "station" }));
        if (i < DOTS - 1) {
          trackEl.appendChild(Object.assign(document.createElement("span"), { className: "segment" }));
        }
      }
    }
    buildTrack();
    const stations = () => trackEl.querySelectorAll(".station");
    const segments = () => trackEl.querySelectorAll(".segment");

    function countUp(from, to) {
      return new Promise((resolve) => {
        const steps = Math.max(4, Math.min(10, Math.abs(to - from)));
        const inc = (to - from) / steps;
        let cur = from;
        const t = setInterval(() => {
          cur += inc;
          const done = inc >= 0 ? cur >= to : cur <= to;
          if (done) { cur = to; clearInterval(t); resolve(); }
          countEl.textContent = Math.round(cur);
        }, 45);
      });
    }

    (async function loop() {
      let li = 0;
      for (;;) {
        const [color, name, total] = LINES[li % LINES.length];
        trackEl.style.setProperty("--lc", color);
        dotEl.style.background = color;
        nameEl.textContent = name;
        nameEl.style.color = color;
        totalEl.textContent = total + UNIT;
        countEl.textContent = "0";
        stations().forEach((s) => s.classList.remove("on"));
        segments().forEach((s) => s.classList.remove("on"));
        stampEl.classList.remove("shown");
        stations()[0].classList.add("on");
        await sleep(250);
        let shown = 0;
        for (let i = 0; i < DOTS - 1; i++) {
          segments()[i].classList.add("on");
          stations()[i + 1].classList.add("on");
          const target = Math.round((total * (i + 1)) / (DOTS - 1));
          await countUp(shown, target);
          shown = target;
          await sleep(160);
        }
        stampEl.classList.add("shown");
        await sleep(1500);
        li++;
      }
    })();
  }

  // ---- page spine: sticky progress bar + station-by-station line fill ----
  (function () {
    const REDUCE = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const stops = Array.from(document.querySelectorAll(".stop"));
    const fillEl = document.getElementById("progressFill");
    const countEl2 = document.getElementById("progressCount");
    const finishEl = document.getElementById("finishStamp");
    if (!stops.length || !fillEl || !countEl2) return;

    if (!REDUCE) {
      stops.forEach((s) => s.classList.remove("passed"));
      if (finishEl) finishEl.classList.remove("shown");
    }

    let ticking = false;
    function update() {
      ticking = false;
      const scrollable = document.documentElement.scrollHeight - window.innerHeight;
      const progress = scrollable > 0 ? Math.min(1, Math.max(0, window.scrollY / scrollable)) : 0;
      fillEl.style.width = (progress * 100).toFixed(2) + "%";
      countEl2.textContent = Math.round(progress * %%PROGRESS_TOTAL%%) + " / %%PROGRESS_TOTAL%%";
      if (!REDUCE) {
        let currentColor = "";
        stops.forEach((s) => {
          const passed = s.getBoundingClientRect().top < window.innerHeight * 0.5;
          s.classList.toggle("passed", passed);
          if (passed) currentColor = s.style.getPropertyValue("--stop-color");
        });
        if (currentColor) fillEl.style.background = currentColor;
        if (finishEl) finishEl.classList.toggle("shown", stops[stops.length - 1].classList.contains("passed"));
      }
    }
    function onScroll() {
      if (!ticking) { ticking = true; requestAnimationFrame(update); }
    }
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll);
    update();
  })();
"""


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


def step_viz(i, color, loc):
    """SSR-static mini diagram illustrating step `i` (0=log, 1=map color, 2=stamps).
    Fully rendered up front (no JS) so it holds up under prefers-reduced-motion."""
    if i == 0:
        # a mini station strip: 3 already-visited stops, 1 just-tapped stop, 2 not yet visited.
        cells = []
        for n in range(6):
            st_cls = "viz-st on tap" if n == 3 else ("viz-st on" if n < 3 else "viz-st")
            cells.append(f'<span class="{st_cls}"></span>')
            if n < 5:
                seg_cls = "viz-seg on" if n < 3 else "viz-seg"
                cells.append(f'<span class="{seg_cls}"></span>')
        inner = f'<div class="step-viz strip-viz" style="--vc:{color}" aria-hidden="true">{"".join(cells)}</div>'
    elif i == 1:
        inner = f"""<div class="step-viz line-viz" aria-hidden="true">
      <div class="line-row"><span class="line-cap">{loc['step2_unridden']}</span><span class="line-bar"></span></div>
      <div class="line-row on"><span class="line-cap" style="color:{color}">{loc['step2_ridden']}</span><span class="line-bar" style="background:{color}"></span></div>
    </div>"""
    else:
        # i == 2: a 3x2 stamp-book miniature — 4 stamped cells, 2 still-empty cells.
        cells = "".join(f'<span class="mini-stamp{" filled" if n < 4 else ""}"></span>' for n in range(6))
        inner = f'<div class="step-viz stamp-viz" aria-hidden="true">{cells}</div>'
    return f'<div class="step-viz-card">{inner}</div>'


def render(key):
    loc = LOCALES[key]
    rel = "../" if loc["dir"] else ""
    font_override = f'<style>body{{font-family:-apple-system,BlinkMacSystemFont,{loc["font"]},"Segoe UI",sans-serif}}</style>' if loc["font"] else ""

    chips = "".join(
        f'<div class="chip c{i+1}"><span class="g">{g}</span>{label}</div>'
        for i, (g, label) in enumerate(loc["hero_chips"])
    )
    # ---- spine stops: one per major section (hero, 3 steps, stats, shots, feats, pro, final) ----
    def stop(idx, big=False):
        """Return (markers_html, stop_color) for spine stop `idx`. A vertical line-name
        label is only drawn on the stop where a new real-line color run begins."""
        color, label = loc["spine_lines"][STOP_LINE_IDX[idx]]
        show_label = idx == 0 or STOP_LINE_IDX[idx] != STOP_LINE_IDX[idx - 1]
        dot_cls = "stop-dot stop-dot-final" if big else "stop-dot"
        lbl = f'<span class="stop-label" aria-hidden="true">{label}</span>' if show_label else ""
        return f'<span class="{dot_cls}" aria-hidden="true"></span>{lbl}', color

    step_stops = []
    for i, (tag, h, p) in enumerate(loc["steps"]):
        markers, color = stop(1 + i)
        intro = f"<h2>{loc['how_h2']}</h2>" if i == 0 else ""
        viz = step_viz(i, color, loc)
        step_stops.append(f"""<section class="stop passed step-stop" style="--stop-color:{color}">
  {markers}
  <div class="wrap">
    <div class="kicker"><span>{tag}</span><span class="rule"></span><span class="num">0{i+1}</span></div>
    {intro}
    <div class="step"><h3>{h}</h3><p>{p}</p>{viz}</div>
  </div>
</section>""")
    step_stops_html = "\n".join(step_stops)

    stats = "".join(f'<div class="stat"><div class="v">{v}</div><div class="l">{l}</div></div>' for v, l in loc["stats"])
    line_chips = "".join(
        f'<span class="line-chip"><span class="sw" style="background:{hexv}"></span>{name}</span>'
        for name, hexv in loc["line_chips"]
    )
    shot_files = ["map", "stamps", "complete"]
    shots = "".join(
        f'<figure><div class="phone"><img src="{rel}assets/shot-{loc["shots"]}-{f}.png" alt="{cap}" decoding="async"><div class="island"></div></div><figcaption>{cap}</figcaption></figure>'
        for f, cap in zip(shot_files, loc["shots_caps"])
    )
    feats = "".join(f'<div class="feat"><h3>{h}</h3><p>{p}</p></div>' for h, p in loc["feats"])
    prices = "".join(
        f'<div class="price-card"><div class="p">{p}</div><div class="t">{t}</div></div>'
        for p, t in loc["prices"]
    )

    # initial (SSR) transit-line demo — the fully-completed state, shown as-is
    # when JS never runs (prefers-reduced-motion, or scripting disabled).
    first_color, first_name, first_total = loc["lines"][0]
    track_cells = []
    for i in range(DOTS):
        track_cells.append('<span class="station on"></span>')
        if i < DOTS - 1:
            track_cells.append('<span class="segment on"></span>')
    track_html = "".join(track_cells)

    lines_json = json.dumps(loc["lines"], ensure_ascii=False)
    unit_json = json.dumps(loc["unit"], ensure_ascii=False)
    script_js = (
        SCRIPT_JS
        .replace("%%APPSTORE%%", APP_STORE_URL)
        .replace("%%LINES%%", lines_json)
        .replace("%%UNIT%%", unit_json)
        .replace("%%DOTS%%", str(DOTS))
        .replace("%%PROGRESS_TOTAL%%", str(PROGRESS_TOTAL))
    )

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
    <a class="wordmark" href="{rel if rel else './'}"><img src="{rel}assets/icon-180.png" alt=""><span>RAILLOG</span></a>
    <div class="progress-counter" id="progressCount">0 / {PROGRESS_TOTAL}</div>
    <div class="lang">{lang_nav(loc['dir'], rel)}</div>
  </div>
  <div class="progress-rail"><div class="progress-fill" id="progressFill"></div></div>
</nav>

<div class="spine-wrap">

<header class="hero stop passed" style="--stop-color:{stop(0)[1]}">
  {stop(0)[0]}
  <div class="ghost">RL</div>
  <div class="wrap">
    <div>
      <div class="kicker"><span>RAILLOG</span><span class="rule"></span><span class="num">{loc['kicker_num']}</span></div>
      <h1>{loc['h1']}</h1>
      <div class="demo-transit">
        <div class="demo-head">
          <span class="demo-dot" id="demoDot" style="background:{first_color}"></span>
          <span class="demo-name" id="demoName" style="color:{first_color}">{first_name}</span>
          <span class="demo-count"><strong id="demoCount">{first_total}</strong> / <span id="demoTotal">{first_total}{loc['unit']}</span></span>
        </div>
        <div class="demo-track" id="demoTrack" style="--lc:{first_color}">{track_html}</div>
        <div class="demo-stamp shown" id="demoStamp">{loc['stamp_html']}</div>
      </div>
      <p class="sub">{loc['sub']}</p>
      <div class="cta">
        {badge(loc, 'storeLink')}
        <span class="note">{loc['note']}</span>
      </div>
    </div>
    <div class="phone-col">
      {chips}
      <div class="phone"><img src="{rel}assets/shot-{loc['shots']}-map.png" alt="{loc['hero_alt']}"><div class="island"></div></div>
    </div>
  </div>
</header>

{step_stops_html}

<section class="stop passed" style="--stop-color:{stop(4)[1]};padding-top:0">
  {stop(4)[0]}
  <div class="wrap">
    <div class="kicker"><span>{loc['value_kicker']}</span><span class="rule"></span><span class="num">{loc['value_num']}</span></div>
    <h2>{loc['value_h2']}</h2>
    <p class="lede">{loc['value_lede']}</p>
    <div class="stat-poster">{stats}</div>
    <div class="line-chips">{line_chips}</div>
  </div>
</section>

<section class="stop passed shots" style="--stop-color:{stop(5)[1]}">
  {stop(5)[0]}
  <div class="wrap">
    <div class="kicker"><span>{loc['shots_kicker']}</span><span class="rule"></span><span class="num">{loc['shots_num']}</span></div>
    <h2>{loc['shots_h2']}</h2>
    <div class="row">{shots}</div>
  </div>
</section>

<section class="stop passed" style="--stop-color:{stop(6)[1]}">
  {stop(6)[0]}
  <div class="wrap">
    <div class="kicker"><span>{loc['feat_kicker']}</span><span class="rule"></span><span class="num">{loc['feat_num']}</span></div>
    <h2>{loc['feat_h2']}</h2>
    <div class="grid6">{feats}</div>
  </div>
</section>

<section class="stop passed" style="--stop-color:{stop(7)[1]};padding-top:0">
  {stop(7)[0]}
  <div class="wrap">
    <div class="kicker"><span>{loc['pro_kicker']}</span><span class="rule"></span><span class="num">{loc['pro_num']}</span></div>
    <h2>{loc['pro_h2']}</h2>
    <p class="lede">{loc['pro_lede']}</p>
    <div class="pricing">{prices}</div>
    <p class="pricing-note">{loc['pro_note']}</p>
  </div>
</section>

<section class="stop passed stop-final final" style="--stop-color:{stop(8, big=True)[1]}">
  {stop(8, big=True)[0]}
  <div class="wrap">
    <div class="finish-stamp shown" id="finishStamp">{loc['stamp_html']}</div>
    <h2>{loc['final_h2']}</h2>
    <p class="lede">{loc['final_lede']}</p>
    <div class="cta">{badge(loc, 'storeLink2')}</div>
  </div>
</section>

</div>

<footer>
  <div class="wrap">
    <div class="row">
      <div class="brand"><img src="{rel}assets/icon-180.png" alt=""><strong>kkiruk studio</strong></div>
      <div class="links">
        <a href="mailto:kkirukstudio.help@gmail.com">{loc['f_contact']}</a>
        <a href="https://kkiruk-studio.github.io/privacy-policy-app/">{loc['f_privacy']}</a>
        <a href="https://kkiruk-studio.github.io/terms-of-service-app/">{loc['f_terms']}</a>
      </div>
      <div>© 2026 kkiruk studio</div>
    </div>
    <div class="data-note">{loc['data_note']}</div>
  </div>
</footer>

<script>{script_js}</script>
</body>
</html>
"""
    out = ROOT / loc["dir"] / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)} ({len(html)} bytes)")


for key in LOCALES:
    render(key)
