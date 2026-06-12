#!/usr/bin/env python3
"""sitemap.xml 생성기 — 콘텐츠 페이지를 스캔해 canonical URL 목록을 만든다.

규칙:
- drafts/ gen/ icons/ shots/ assets/ legal/ 및 *-ko 리다이렉트 폴더 제외
- meta refresh(리다이렉트 스텁) 제외
- 페이지에 rel=canonical 이 있으면 그 URL, 없으면 경로 기반 URL (index.html → 디렉토리/)
- 중복 canonical 은 1개만

사용: python3 gen/gen_sitemap.py  (repo 루트 기준 sitemap.xml 갱신)
"""
import os, re, datetime

BASE = "https://www.kkirukstudio.com"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {"drafts", "gen", "icons", "shots", ".git", ".github"}
SKIP_PARTS = {"assets", "legal", "raw"}
SKIP_TOP = {"404.html"}
REDIRECT_DIRS = {"thanyesterday-ko", "talkmemo-ko", "pinclip-ko", "sidefeed-ko", "honestcamera-ko"}

urls = {}
for dirpath, dirnames, filenames in os.walk(ROOT):
    rel = os.path.relpath(dirpath, ROOT)
    parts = [] if rel == "." else rel.split(os.sep)
    dirnames[:] = [d for d in dirnames
                   if d not in SKIP_DIRS and d not in SKIP_PARTS and d not in REDIRECT_DIRS]
    if any(p in SKIP_PARTS for p in parts):
        continue
    for fn in filenames:
        if not fn.endswith(".html"):
            continue
        relf = os.path.join(rel, fn) if rel != "." else fn
        if relf in SKIP_TOP:
            continue
        path = os.path.join(dirpath, fn)
        try:
            head = open(path, encoding="utf-8", errors="ignore").read(4000)
        except OSError:
            continue
        if 'http-equiv="refresh"' in head:
            continue
        m = re.search(r'rel="canonical"\s+href="([^"]+)"', head)
        if m and m.group(1).startswith("http"):
            url = m.group(1)
        else:
            p = relf.replace(os.sep, "/")
            if p.endswith("index.html"):
                p = p[: -len("index.html")]
            url = f"{BASE}/{p}" if p else BASE + "/"
        urls[url] = max(urls.get(url, ""), datetime.date.fromtimestamp(os.path.getmtime(path)).isoformat())

today = datetime.date.today().isoformat()
lines = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for url in sorted(urls):
    lines.append(f"  <url><loc>{url}</loc><lastmod>{urls[url]}</lastmod></url>")
lines.append("</urlset>")
out = os.path.join(ROOT, "sitemap.xml")
open(out, "w", encoding="utf-8").write("\n".join(lines) + "\n")
print(f"sitemap.xml — {len(urls)}개 URL")
