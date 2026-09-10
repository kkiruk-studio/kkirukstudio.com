#!/usr/bin/env python3
"""Check actual app pages, including pages with optional language redirects."""
import sys
sys.dont_write_bytecode = True
import ast
import json
import re
from pathlib import Path
from urllib.parse import urlparse, unquote
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from gen_jsonld import APPS, pages, ROOT

class Facts(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.links = []
    def handle_data(self, data):
        self.text.append(data)
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.links.append(dict(attrs).get('href', ''))

def main():
    errors = []
    count = 0
    for slug in APPS:
        ids = set()
        for p in pages(slug):
            html = p.read_text()
            if re.search(r'http-equiv=["\x27]refresh', html, re.I):
                continue
            count += 1
            nodes = []
            for raw in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
                obj = json.loads(raw)
                nodes.extend(obj.get('@graph', [obj]))
            app = next((n for n in nodes if n.get('@type') == 'SoftwareApplication'), None)
            if not app:
                errors.append(f'{p}: missing app')
                continue
            if slug != 'deskbreath':
                ids.add(app['@id'])
            facts = re.findall(r'<!-- product-facts:begin -->(.*?)<!-- product-facts:end -->', html, re.S)
            if len(facts) != 1:
                errors.append(f'{p}: expected one visible facts block')
                continue
            parser = Facts()
            parser.feed(facts[0])
            text = ''.join(parser.text)
            if app['name'] not in text or app['operatingSystem'] not in text:
                errors.append(f'{p}: facts/schema mismatch')
            if not any('apps.apple.com/' in link for link in parser.links):
                errors.append(f'{p}: no static download link')
        if slug != 'deskbreath' and len(ids) != 1:
            errors.append(f'{slug}: locale app IDs are not shared')
    for filename in ('index.html', 'en.html', 'ja.html', 'zh-hans.html', 'zh-hant.html'):
        html = (ROOT / filename).read_text()
        graph = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)[1])['@graph']
        collection = next(n for n in graph if n['@type'] == 'CollectionPage')
        if len(collection['mainEntity']['itemListElement']) < 10:
            errors.append(f'{filename}: incomplete home catalog')
    urls = [n.text for n in ET.parse(ROOT / 'sitemap.xml').iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
    for url in urls:
        part = unquote(urlparse(url).path).lstrip('/')
        p = ROOT / part
        if p.is_dir():
            p = p / 'index.html'
        if not p.is_file() or p.name in ('og.html', 'og-src.html'):
            errors.append(f'sitemap: {url}')
    for p in list(ROOT.glob('*/build.py')) + list((ROOT / 'gen').glob('*.py')):
        ast.parse(p.read_text())
    print(f'App pages: {count}; home catalogs: 5; sitemap URLs: {len(urls)}; errors: {len(errors)}')
    for error in errors:
        print(error)
    return bool(errors)

if __name__ == '__main__':
    sys.exit(main())
