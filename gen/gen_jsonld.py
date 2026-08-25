#!/usr/bin/env python3
"""앱 랜딩에 SoftwareApplication JSON-LD 주입 (멱등).

왜: 2026-08-10 진단에서 135 페이지 중 구조화 데이터가 0개로 확인됐다.
    웹 검색 리치결과 + AI 모델이 앱을 인용할 때의 근거 양쪽에 쓰인다.

원칙 — 날조 금지:
  - name/description/url 은 **페이지에 이미 있는 title·description·canonical 에서 읽는다**.
    새 카피를 만들지 않는다.
  - aggregateRating 은 넣지 않는다. 평점·리뷰수는 시간에 따라 변하고, 구조화 데이터에
    박아두면 곧 사실과 어긋난다. 가시 카피의 소셜프루프로 충분.
  - offers(가격)도 넣지 않는다. 앱별·지역별로 다르고 검증 없이 넣으면 허위가 된다.

⚠️ 각 앱 build.py 재생성 후에는 이 스크립트를 다시 돌려야 한다
   (canonical 이 재생성 때 사라지던 것과 같은 함정 — website.md 참조).

Usage:
  python3 gen/gen_jsonld.py          # 주입/갱신
  python3 gen/gen_jsonld.py --check  # 미주입 페이지만 보고 (파일 수정 안 함)
"""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BEGIN, END = "<!-- jsonld:app:begin -->", "<!-- jsonld:app:end -->"

# dir → (App Store id, Play package|None, schema.org applicationCategory)
APPS = {
    "thanyesterday":  ("6761168631", None, "UtilitiesApplication"),
    "pinclip":        ("6761982511", None, "ProductivityApplication"),
    "sidefeed":       ("6762836653", None, "EntertainmentApplication"),
    "talkmemo":       ("6764329223", None, "ProductivityApplication"),
    "honestcamera":   ("6766827649", None, "MultimediaApplication"),
    "cats-cute":      ("1395888987", "com.game.kkiruk.myadorablecats", "GameApplication"),
    "cats-pop":       ("1556403381", "com.game.kkiruk.catsarepop", "GameApplication"),
    "locallink":      ("6767477190", None, "TravelApplication"),
    "runnote":        ("6787010935", None, "HealthApplication"),
    "deskbreath":     ("6786591689", None, "HealthApplication"),
    "tetsulog":       ("6787012765", None, "TravelApplication"),
    "raillog":        ("6794330967", None, "TravelApplication"),
    "nyc-subway-log": ("6795853224", None, "TravelApplication"),
    "palette2048":    ("6767449110", None, "GameApplication"),
    "quote2048":      ("6788598686", None, "GameApplication"),
    "salarycharm":    ("6785930647", None, "EntertainmentApplication"),
    "newsmaker":      ("6787015246", None, "EntertainmentApplication"),
    "everykeep":      ("6781988992", None, "UtilitiesApplication"),
}

PUBLISHER = {"@type": "Organization", "name": "kkiruk studio",
             "url": "https://www.kkirukstudio.com/"}

# 자기 build.py 가 이미 더 정확한 블록을 생성하는 앱 — 여기서 건드리면 오히려 후퇴한다.
# deskbreath: 맥/iOS 양 플랫폼 앱이라 operatingSystem 에 macOS 가 반드시 들어가야 하고,
#             featureList·검증된 offers·alternateName 까지 build.py 가 로케일별로 생성한다.
#             이 스크립트가 덮으면 operatingSystem 이 "iOS" 로 되돌아간다 (2026-08-25).
BUILD_OWNED = {"deskbreath"}


def _meta(html, pattern):
    m = re.search(pattern, html, re.I)
    return m.group(1).strip() if m else None


def build(html, ios_id, play_id, category):
    title = _meta(html, r"<title>(.*?)</title>")
    desc = _meta(html, r'<meta\s+name="description"\s+content="(.*?)"')
    canon = _meta(html, r'<link\s+rel="canonical"\s+href="(.*?)"')
    if not (title and canon):
        return None
    # "everykeep — 소모품 교체·관리 알림" → 앱 이름만
    name = re.split(r"\s+[—–|:]\s+", title)[0].strip()
    stores = [f"https://apps.apple.com/app/id{ios_id}"]
    os_list = ["iOS"]
    if play_id:
        stores.append(f"https://play.google.com/store/apps/details?id={play_id}")
        os_list.append("Android")
    data = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": name,
        "url": canon,
        "applicationCategory": category,
        "operatingSystem": ", ".join(os_list),
        "publisher": PUBLISHER,
        "sameAs": stores,
        "installUrl": stores[0],
    }
    if desc:
        data["description"] = desc
    return (BEGIN + '\n<script type="application/ld+json">\n'
            + json.dumps(data, ensure_ascii=False, indent=2)
            + "\n</script>\n" + END + "\n")


def pages(d):
    base = ROOT / d
    for p in sorted(list(base.glob("*.html")) + list(base.glob("*/index.html"))):
        if "drafts" in p.parts:
            continue
        yield p


def main(check_only=False):
    injected = missing = skipped = 0
    for d, (ios_id, play_id, cat) in APPS.items():
        if d in BUILD_OWNED:
            print(f"  ⏭  {d} — 자체 build.py 가 생성함(더 정확), 건너뜀")
            skipped += 1
            continue
        if not (ROOT / d).is_dir():
            print(f"  ⚠️  디렉토리 없음: {d}")
            continue
        for p in pages(d):
            html = p.read_text(encoding="utf-8")
            if "http-equiv=\"refresh\"" in html or "location.replace(" in html:
                skipped += 1          # 리다이렉트 스텁
                continue
            block = build(html, ios_id, play_id, cat)
            if block is None:
                print(f"  ⚠️  title/canonical 없음, 건너뜀: {p.relative_to(ROOT)}")
                skipped += 1
                continue
            if check_only:
                if BEGIN not in html:
                    missing += 1
                    print(f"  미주입: {p.relative_to(ROOT)}")
                continue
            # 멱등: 기존 블록 제거 후 </head> 앞에 삽입
            html = re.sub(re.escape(BEGIN) + r".*?" + re.escape(END) + r"\n?",
                          "", html, flags=re.S)
            if "</head>" not in html:
                print(f"  ⚠️  </head> 없음: {p.relative_to(ROOT)}")
                skipped += 1
                continue
            html = html.replace("</head>", block + "</head>", 1)
            p.write_text(html, encoding="utf-8")
            injected += 1
    if check_only:
        print(f"\n미주입 {missing}개 · 대상외 {skipped}개")
    else:
        print(f"\n✅ 주입 {injected}개 · 대상외 {skipped}개")


if __name__ == "__main__":
    main(check_only="--check" in sys.argv)
