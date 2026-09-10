#!/usr/bin/env python3
"""Run after any landing build; keep visible product facts and metadata in sync."""
import sys
sys.dont_write_bytecode = True
import json
import re
import runpy
from html import escape, unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'gen'))
from gen_jsonld import APPS, pages, main as app_metadata

# Stable product definitions. No unverified prices, ratings or changing inventories.
SUMMARIES = {
 'thanyesterday': ('어제보다', '오늘 날씨를 어제와 비교해 알려주는 날씨 앱입니다.', 'Than Yesterday compares today’s weather with yesterday’s to help you understand the change.'),
 'pinclip': ('Pinclip', '인스타그램 릴스와 유튜브 쇼츠 등에서 발견한 영상 링크를 한곳에 모으고 폴더로 정리하는 북마크 앱입니다.', 'Pinclip saves video links from services such as Instagram Reels and YouTube Shorts in one place, organized into folders.'),
 'sidefeed': ('Sidefeed', '여러 국가의 유튜브 인기 영상과 급상승 흐름을 살펴보는 크리에이터용 리서치 앱입니다.', 'Sidefeed helps creators research popular YouTube videos and rising trends across countries.'),
 'talkmemo': ('Talk Memo', 'Apple Watch에서 말로 남긴 생각을 iPhone에서 텍스트로 확인하는 음성 메모 앱입니다. Notion과 Obsidian 연동을 지원합니다.', 'Talk Memo captures spoken ideas on Apple Watch and turns them into text on iPhone, with Notion and Obsidian integrations.'),
 'honestcamera': ('Honest Camera', '유아도 사용할 수 있도록 큰 노란 셔터 버튼 하나로 촬영하고 사진 앱에 바로 저장하는 카메라 앱입니다.', 'Honest Camera is a simple camera for young children, with one large yellow shutter button and photos saved directly to the Photos app.'),
 'cats-cute': ('고양이는 정말 귀여워', '손그림 고양이를 모으고 마을을 꾸미는 힐링 방치형 게임입니다.', 'Cats are Cute is a relaxing idle game about collecting hand-drawn cats and building their village.'),
 'cats-pop': ('고양이는 정말 팡팡', '같은 고양이를 합쳐 더 큰 고양이를 만드는 고양이 합치기 퍼즐 게임입니다.', 'Cats are Cute: Pop Time! is a puzzle game where matching cats merge into bigger cats.'),
 'locallink': ('로컬링크', '장소 이름을 현지 문자 검색어로 바꾸고 현지 지도 앱으로 연결해 주는 여행 앱입니다.', 'Local Link converts place names into local-script search terms and opens them in local map apps.'),
 'runnote': ('RunNote', 'Apple Watch의 러닝 기록에 컨디션과 메모를 더하고 운동 후 AI 코칭을 받는 러닝 기록장입니다.', 'RunNote adds notes and how you felt to Apple Watch running records, with AI coaching after your run.'),
 'deskbreath': ('DeskBreath', '책상에서 호흡 운동과 스트레칭을 할 수 있도록 돕는 iPhone·Mac 앱입니다.', 'DeskBreath helps you take breathing and stretching breaks at your desk on iPhone and Mac.'),
 'tetsulog': ('테츠로그', '일본 철도역 방문과 탑승 기록을 지도에 남기는 철도 여행 기록 앱입니다.', 'Tetsulog records visits to Japanese railway stations and tracks the lines you have ridden on a map.'),
 'raillog': ('레일로그', '한국 철도역 방문과 탑승 노선을 지도와 스탬프북에 기록하는 철도 여행 앱입니다.', 'Raillog records visits to Korean railway stations and the lines you have ridden, using a map and stamp book.'),
 'nyc-subway-log': ('NYC Subway Log', '뉴욕 지하철역 방문과 탑승 기록을 남기는 지하철 여행 앱입니다.', 'NYC Subway Log tracks the New York subway stations you have visited and the lines you have ridden.'),
 'palette2048': ('Palette 2048', '숫자 대신 색을 합치며 명화의 색을 즐기는 2048 퍼즐 게임입니다.', 'Palette 2048 is a puzzle game that replaces numbers with colors inspired by works of art.'),
 'quote2048': ('명언 2048', '2048 타일을 합치며 명언과 작가 컬렉션을 모으는 문장 수집 퍼즐 게임입니다.', 'Quote 2048 combines the 2048 tile puzzle with collecting quotations and author collections.'),
 'salarycharm': ('직장인 부적', '출근길과 회사생활에 웃음과 응원을 전하는 부적을 받는 앱입니다.', 'Salary Charm offers playful charms and encouragement for everyday working life.'),
 'newsmaker': ('속보메이커', '헤드라인에 테마와 폰트를 입혀 공유용 속보 짤 이미지를 만드는 앱입니다.', 'NewsMaker turns a headline into a shareable breaking-news meme with themes and fonts.'),
 'everykeep': ('everykeep', '필터 교체, 청소 주기, 보증기간 등 잊기 쉬운 물건 관리 일정을 기록하고 알림을 받는 앱입니다.', 'everykeep tracks home maintenance such as filter replacements, cleaning cycles and warranties, and reminds you when upkeep is due.'),
 'cuttogether': ('CutTogether', '사진 속 사람을 iPhone 안에서 오려내 한 장의 스크랩북 포스터로 모으는 사진 콜라주 앱입니다. 계정이나 사진 업로드가 필요하지 않습니다.', 'CutTogether cuts people out of photos on your iPhone and gathers them into a scrapbook poster, without an account or photo uploads.'),
}
LABELS = {
 'ko': ('앱 안내', '지원 환경', '공식 다운로드', '제작'),
 'en': ('About this app', 'Platform', 'Official download', 'Developer'),
 'ja': ('アプリについて', '対応環境', '公式ダウンロード', '開発元'),
 'zh-hans': ('应用介绍', '支持平台', '官方下载', '开发者'),
 'zh-hant': ('應用程式介紹', '支援平台', '官方下載', '開發者'),
 'de': ('Über die App', 'Plattform', 'Offizieller Download', 'Entwickler'),
 'es': ('Acerca de la app', 'Plataforma', 'Descarga oficial', 'Desarrollador'),
 'fr': ('À propos de l’application', 'Plateforme', 'Téléchargement officiel', 'Développeur'),
 'pt': ('Sobre o aplicativo', 'Plataforma', 'Download oficial', 'Desenvolvedor'),
 'ru': ('О приложении', 'Платформа', 'Официальная загрузка', 'Разработчик'),
 'th': ('เกี่ยวกับแอป', 'แพลตฟอร์ม', 'ดาวน์โหลดอย่างเป็นทางการ', 'ผู้พัฒนา'),
 'vi': ('Giới thiệu ứng dụng', 'Nền tảng', 'Tải xuống chính thức', 'Nhà phát triển'),
 'id': ('Tentang aplikasi', 'Platform', 'Unduhan resmi', 'Pengembang'),
}
BEGIN, END = '<!-- product-facts:begin -->', '<!-- product-facts:end -->'

def save(p, content):
    if p.read_text(encoding='utf-8') != content:
        p.write_text(content, encoding='utf-8')

def main():
    app_metadata()
    total = 0
    for slug in APPS:
        for p in pages(slug):
            html = p.read_text(encoding='utf-8')
            if re.search(r'http-equiv=["\x27]refresh', html, re.I):
                continue
            nodes = []
            for raw in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
                obj = json.loads(raw)
                nodes.extend(obj.get('@graph', [obj]))
            app = next((n for n in nodes if n.get('@type') == 'SoftwareApplication'), None)
            if not app:
                raise ValueError(f'Missing app: {p}')
            lang = re.search(r'<html[^>]*lang="([^"]+)"', html, re.I)[1].lower()
            labels = LABELS.get(lang, LABELS.get(lang.split('-')[0], LABELS['en']))
            desc = unescape(app.get('description', ''))
            if lang in ('ko', 'en'):
                name, ko, en = SUMMARIES[slug]
                desc = name + ' — ' + ko if lang == 'ko' else en
            stores = [u for u in app.get('sameAs', []) if 'apps.apple.com/' in u or 'play.google.com/' in u]
            if not stores:
                stores = [app['installUrl']]
            links = ' · '.join(f'<a href="{escape(u, quote=True)}">{"Google Play" if "play.google" in u else "App Store"}</a>' for u in dict.fromkeys(stores))
            block = f'''{BEGIN}
<section class="product-facts" aria-labelledby="product-facts-heading">
<h2 id="product-facts-heading">{escape(app['name'])} · {labels[0]}</h2>
<p>{escape(desc)}</p>
<dl><div><dt>{labels[1]}</dt><dd>{escape(app['operatingSystem'])}</dd></div>
<div><dt>{labels[2]}</dt><dd>{links}</dd></div>
<div><dt>{labels[3]}</dt><dd><a href="/">kkiruk studio · 끼룩 스튜디오</a></dd></div></dl>
</section>
{END}
'''
            html = re.sub(re.escape(BEGIN) + '.*?' + re.escape(END) + r'\n?', '', html, flags=re.S)
            # Static HTML is readable without running any JavaScript.
            marker = re.search(r'<footer\b', html, re.I)
            pos = marker.start() if marker else html.index('</body>')
            html = html[:pos] + block + html[pos:]
            css = '<link rel="stylesheet" href="/product-facts.css">'
            if css not in html:
                marker = '<!-- jsonld:app:begin -->' if '<!-- jsonld:app:begin -->' in html else '</head>'
                html = html.replace(marker, css + '\n' + marker, 1)
            save(p, html)
            total += 1
    homes = {
        'index.html': ('끼룩 스튜디오 — iPhone 앱과 고양이 게임', '끼룩 스튜디오(kkiruk studio)는 서울의 1인 앱·게임 개발 스튜디오입니다. 날씨 비교 앱 어제보다, Apple Watch 음성 메모 Talk Memo, 영상 북마크 Pinclip, 고양이는 정말 귀여워 등 일상 앱과 게임을 만듭니다.'),
        'en.html': ('kkiruk studio — iPhone apps and cat games', 'kkiruk studio is an independent, one-person app and game studio in Seoul. Its products include Than Yesterday for weather comparisons, Talk Memo for Apple Watch voice notes, Pinclip for video bookmarks, and Cats are Cute.'),
        'ja.html': ('kkiruk studio — iPhoneアプリとねこゲーム', 'kkiruk studioは、ソウルでひとりでアプリとゲームを開発するスタジオです。天気を昨日と比較する「昨日より」、Apple Watchの音声メモ「Talk Memo」、動画ブックマーク「Pinclip」、ゲーム「ねこはほんとかわいい」などを制作しています。'),
        'zh-hans.html': ('kkiruk studio — iPhone 应用与猫咪游戏', 'kkiruk studio 是位于首尔的独立个人应用与游戏工作室，作品包括比较今日与昨日天气的「比昨天」、Apple Watch 语音笔记 Talk Memo、视频书签 Pinclip 和游戏「猫真的很可爱」。'),
        'zh-hant.html': ('kkiruk studio — iPhone App 與貓咪遊戲', 'kkiruk studio 是位於首爾的獨立個人 App 與遊戲工作室，作品包括比較今日與昨日天氣的「比昨天」、Apple Watch 語音筆記 Talk Memo、影片書籤 Pinclip 和遊戲「貓咪真的很可愛」。'),
    }
    for filename, (title, description) in homes.items():
        p = ROOT / filename
        html = p.read_text(encoding='utf-8')
        html = re.sub(r'<title>.*?</title>', '<title>' + escape(title) + '</title>', html, count=1)
        html = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="' + escape(description, quote=True) + '">', html, count=1)
        intro = f'<!-- studio-intro:begin --><section class="product-facts"><h2>{escape(title)}</h2><p>{escape(description)}</p></section><!-- studio-intro:end -->\n'
        html = re.sub(r'<!-- studio-intro:begin -->.*?<!-- studio-intro:end -->\n?', '', html, flags=re.S)
        pos = html.index('<footer')
        html = html[:pos] + intro + html[pos:]
        css = '<link rel="stylesheet" href="/product-facts.css">'
        if css not in html:
            html = html.replace('</head>', css + '\n</head>', 1)
        save(p, html)
    for filename in ('gen_home_jsonld.py', 'gen_page_jsonld.py', 'gen_sitemap.py'):
        runpy.run_path(str(ROOT / 'gen' / filename), run_name='__main__')
    print(f'Product facts: {total} pages')

if __name__ == '__main__':
    main()
