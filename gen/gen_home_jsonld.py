#!/usr/bin/env python3
"""다국어 홈의 Organization/WebSite/CollectionPage JSON-LD를 갱신한다."""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://www.kkirukstudio.com/"
ORG_ID = SITE + "#organization"
WEBSITE_ID = SITE + "#website"
PAGES = ("index.html", "en.html", "ja.html", "zh-hans.html", "zh-hant.html")


def meta(html, pattern):
    match = re.search(pattern, html, re.I | re.S)
    return match.group(1).strip() if match else None


def graph(html):
    title = meta(html, r"<title>(.*?)</title>")
    description = meta(html, r'<meta\s+name="description"\s+content="(.*?)"')
    canonical = meta(html, r'<link\s+rel="canonical"\s+href="(.*?)"')
    language = meta(html, r'<html\s+[^>]*lang="(.*?)"')
    page_id = canonical + "#webpage"
    organization = {
        "@type": "Organization",
        "@id": ORG_ID,
        "name": "kkiruk studio",
        "url": SITE,
        "logo": SITE + "icons/cats-cute.png",
        "foundingDate": "2016",
        "founder": {"@type": "Person", "name": "Sunghyuk Yoon"},
        "description": "An independent app and game studio in Seoul with more than 10 million downloads.",
        "email": "kkirukstudio.help@gmail.com",
        "sameAs": [
            "https://instagram.com/kkiruk_studio",
            "https://twitter.com/kkirukstudio",
            "https://facebook.com/kkirukstudio",
            "https://github.com/kkiruk-studio",
            "https://apps.apple.com/us/developer/sunghyuk-yoon/id1081746441",
            "https://play.google.com/store/apps/dev?id=5655082418239481307",
        ],
    }
    website = {
        "@type": "WebSite",
        "@id": WEBSITE_ID,
        "url": SITE,
        "name": "kkiruk studio",
        "publisher": {"@id": ORG_ID},
        "inLanguage": ["ko", "en", "ja", "zh-Hans", "zh-Hant"],
    }
    page = {
        "@type": "CollectionPage",
        "@id": page_id,
        "url": canonical,
        "name": title,
        "description": description,
        "inLanguage": language,
        "isPartOf": {"@id": WEBSITE_ID},
        "about": {"@id": ORG_ID},
        "publisher": {"@id": ORG_ID},
    }
    return {"@context": "https://schema.org", "@graph": [organization, website, page]}


def main():
    updated = 0
    for filename in PAGES:
        path = ROOT / filename
        html = path.read_text(encoding="utf-8")
        scripts = list(re.finditer(r'<script type="application/ld\+json">.*?</script>', html, re.S))
        if not scripts:
            raise RuntimeError(f"JSON-LD block not found: {filename}")
        block = '<script type="application/ld+json">' + json.dumps(
            graph(html), ensure_ascii=False, separators=(",", ":")
        ) + '</script>'
        match = scripts[0]
        html = html[:match.start()] + block + html[match.end():]
        path.write_text(html, encoding="utf-8")
        updated += 1
    print(f"home JSON-LD — {updated}개 갱신")


if __name__ == "__main__":
    main()
