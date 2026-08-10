#!/usr/bin/env python3
"""라이브 사이트의 '스테일 예고' 자동 검출.

왜 스크립트인가: launch-checklist §4「통과 후」에 이미 "랜딩 App Store 뱃지 확인"
항목이 있었는데도 2026-08 에만 네 번 새어나갔다 —
  RunNote(08-07) · 홈 Local Link ja/zh(08-08) · 테츠로그 4로케일(08-10) ·
  홈 Local Link en(08-10, 08-08 수정이 en 을 빠뜨림)
사람이 지키는 체크 항목을 다섯 번째로 늘리는 대신 기계가 잡게 한다.

검출 항목:
  1. 앱 랜딩 페이지에 App Store 링크가 없음 (리다이렉트 스텁은 제외)
  2. 라이브 HTML 에 「곧 출시」류 문구가 남아 있음
  3. build.py 의 APP_STORE_URL 이 빈 문자열

Usage:
  python3 gen/check_stale.py          # 문제 있으면 exit 1
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

APP_DIRS = ["thanyesterday", "pinclip", "sidefeed", "talkmemo", "honestcamera",
            "cats-cute", "cats-pop", "locallink", "runnote", "deskbreath",
            "tetsulog", "raillog", "nyc-subway-log", "palette2048", "quote2048",
            "salarycharm", "newsmaker", "everykeep"]

HOME = ["index.html", "en.html", "ja.html", "zh-hans.html", "zh-hant.html"]

SOON = re.compile(r"곧 출시|출시 예정|近日公開|公開予定|即將上架|即将上线|即將上線|"
                  r"Coming soon|近日 App Store", re.I)

# 의도적으로 예고인 곳 — 앱 출시 상태와 무관
ALLOW = {
    "genkai-neko/index.html",   # 캐릭터 소개 「？？？ 近日登場」 티저
}

STUB = re.compile(r'http-equiv="refresh"|location\.replace\(')


def rel(p):
    return str(p.relative_to(ROOT))


def pages_of(d):
    base = ROOT / d
    out = []
    for p in sorted(list(base.glob("*.html")) + list(base.glob("*/index.html"))):
        if "drafts" in p.parts or re.search(r"og|src", p.name):
            continue
        out.append(p)
    return out


def main():
    problems = []

    # 1 · 2 — 앱 랜딩
    for d in APP_DIRS:
        if not (ROOT / d).is_dir():
            problems.append(f"[디렉토리없음] {d}")
            continue
        for p in pages_of(d):
            h = p.read_text(encoding="utf-8")
            if STUB.search(h):
                continue                      # 리다이렉트 스텁은 대상 외
            if "apps.apple.com/app/id" not in h:
                problems.append(f"[스토어링크없음] {rel(p)}")
            if rel(p) not in ALLOW and SOON.search(h):
                problems.append(f"[예고문구] {rel(p)} — {SOON.search(h).group(0)}")

    # 2 — 홈 5로케일
    for f in HOME:
        p = ROOT / f
        if not p.exists():
            continue
        h = p.read_text(encoding="utf-8")
        m = SOON.search(h)
        if m:
            problems.append(f"[예고문구·홈] {f} — {m.group(0)}")

    # 3 — 생성기의 빈 스토어 URL
    for p in ROOT.rglob("build.py"):
        if "drafts" in p.parts:
            continue
        if re.search(r'APP_STORE_URL\s*=\s*[\'"]{2}', p.read_text(encoding="utf-8")):
            problems.append(f"[APP_STORE_URL 비어있음] {rel(p)}")

    if problems:
        print(f"❌ 스테일 {len(problems)}건")
        for x in problems:
            print(f"   {x}")
        return 1
    print("✅ 스테일 예고 없음")
    return 0


if __name__ == "__main__":
    sys.exit(main())
