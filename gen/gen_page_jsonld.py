#!/usr/bin/env python3
"""앱 외 주요 랜딩에 WebPage 계열 JSON-LD를 주입한다."""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://www.kkirukstudio.com/"
ORG_ID = SITE + "#organization"
WEBSITE_ID = SITE + "#website"
BEGIN, END = "<!-- jsonld:page:begin -->", "<!-- jsonld:page:end -->"
PAGES = {
    "10years/index.html": "AboutPage",
    "10years/en.html": "AboutPage",
    "artwork/index.html": "CollectionPage",
    "artwork/departures/index.html": "WebPage",
    "genkai-neko/index.html": "CollectionPage",
    "jixian-mao/index.html": "CollectionPage",
    "offwork/index.html": "WebPage",
    "offwork/en/index.html": "WebPage",
}


def meta(html, pattern):
    match = re.search(pattern, html, re.I | re.S)
    return match.group(1).strip() if match else None


def block(html, page_type):
    title = meta(html, r"<title>(.*?)</title>")
    description = meta(html, r'<meta\s+name="description"\s+content="(.*?)"')
    canonical = meta(html, r'<link\s+rel="canonical"\s+href="(.*?)"')
    language = meta(html, r'<html\s+[^>]*lang="(.*?)"')
    image = meta(html, r'<meta\s+property="og:image"\s+content="(.*?)"')
    if not all((title, description, canonical, language)):
        raise RuntimeError("title, description, canonical or lang missing")
    page = {
        "@type": page_type,
        "@id": canonical + "#webpage",
        "url": canonical,
        "name": title,
        "description": description,
        "inLanguage": language,
        "isPartOf": {"@id": WEBSITE_ID},
        "publisher": {"@id": ORG_ID},
    }
    if image and image.startswith("http"):
        page["primaryImageOfPage"] = {"@type": "ImageObject", "url": image}
    data = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Organization",
                "@id": ORG_ID,
                "name": "kkiruk studio",
                "url": SITE,
            },
            {
                "@type": "WebSite",
                "@id": WEBSITE_ID,
                "url": SITE,
                "name": "kkiruk studio",
                "publisher": {"@id": ORG_ID},
            },
            page,
        ],
    }
    return BEGIN + '\n<script type="application/ld+json">' + json.dumps(
        data, ensure_ascii=False, separators=(",", ":")
    ) + '</script>\n' + END + '\n'


def main():
    updated = 0
    for filename, page_type in PAGES.items():
        path = ROOT / filename
        html = path.read_text(encoding="utf-8")
        html = re.sub(re.escape(BEGIN) + r".*?" + re.escape(END) + r"\n?", "", html, flags=re.S)
        html = html.replace("</head>", block(html, page_type) + "</head>", 1)
        if path.read_text(encoding="utf-8") != html:
            path.write_text(html, encoding="utf-8")
        updated += 1
    print(f"page JSON-LD — {updated}개 갱신")


if __name__ == "__main__":
    main()
