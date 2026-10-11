#!/usr/bin/env python3
"""Local Link place pages (programmatic SEO) — one generator, idempotent, stdlib only.

Source data (read-only) is the app's own bundled data in ~/Find Local:
  Data/RecommendedPlaces.swift   411 places (name, localName, country, city)
  Data/aliases.json              spelling variants (romanized / English / ja / zh)
  {en,ko,ja,zh-Hans,zh-Hant}.lproj/Localizable.strings   country/city display names
Map-app priority and search/route URL formats mirror the app (Country.defaultProviders,
MapLauncher, SavedPlacesView.mapQuery).

Usage (repo root or anywhere):
  python3 locallink/places_build.py                      # regenerate all pages + sitemap
  python3 locallink/places_build.py --geo-input FILE     # write geocoder input JSON and exit

Geocoding (coordinates are optional; pages without them skip the walking-route buttons):
  swiftc -O -parse-as-library locallink/places_geocode.swift -o /tmp/places_geocode
  /tmp/places_geocode FILE locallink/places_geo.json
Manual corrections: locallink/places_overrides.csv  (slug,lat,lng — wins over the cache;
an empty lat/lng drops the coordinate for that slug, e.g. macau/mgm-cotai matched MGM Macau).

Output (5 languages × (411 places + 8 country indexes + 1 hub) = 2,100 pages):
  en       /locallink/places/  /locallink/places/<country>/  /locallink/places/<country>/<place>/
  others   /locallink/<ja|ko|zh-hans|zh-hant>/places/...
Pages carry `<!-- seo:build-owned -->` so gen/gen_jsonld.py and gen/refresh_seo.py skip them.
Files are only rewritten when their content changes (sitemap lastmod uses mtime).
"""
import csv
import html
import json
import pathlib
import re
import sys
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parent            # locallink/
SITE_ROOT = ROOT.parent
APP = pathlib.Path.home() / "Find Local" / "Find Local"
SITE = "https://www.kkirukstudio.com"
APP_STORE_URL = "https://apps.apple.com/app/id6767477190"
GEO_CACHE = ROOT / "places_geo.json"
OVERRIDES = ROOT / "places_overrides.csv"

COUNTRY_SLUG = {"korea": "korea", "china": "china", "taiwan": "taiwan", "japan": "japan",
                "thailand": "thailand", "vietnam": "vietnam", "hongKong": "hong-kong", "macau": "macau"}
COUNTRY_KEY = {"korea": "korea", "china": "china", "taiwan": "taiwan", "japan": "japan",
               "thailand": "thailand", "vietnam": "vietnam", "hongKong": "hongkong", "macau": "macau"}
COUNTRY_EN = {"korea": "Korea", "china": "China", "taiwan": "Taiwan", "japan": "Japan", "thailand": "Thailand",
              "vietnam": "Vietnam", "hongKong": "Hong Kong", "macau": "Macau"}
COUNTRY_ISO = {"korea": "KR", "china": "CN", "taiwan": "TW", "japan": "JP", "thailand": "TH",
               "vietnam": "VN", "hongKong": "HK", "macau": "MO"}
# Country.defaultProviders (app)
PROVIDERS = {"korea": ["naver", "kakao", "apple", "google"], "china": ["amap", "apple"]}
DEFAULT_PROVIDERS = ["google", "apple"]
# MapProvider.prefersLocalCityQualifier
LOCAL_QUALIFIED = {"naver", "kakao", "amap"}

LANGS = ["en", "ko", "ja", "zh-hans", "zh-hant"]
LANG_DIR = {"en": "", "ko": "ko/", "ja": "ja/", "zh-hans": "zh-hans/", "zh-hant": "zh-hant/"}
HTML_LANG = {"en": "en", "ko": "ko", "ja": "ja", "zh-hans": "zh-Hans", "zh-hant": "zh-Hant"}
LPROJ = {"en": "en", "ko": "ko", "ja": "ja", "zh-hans": "zh-Hans", "zh-hant": "zh-Hant"}


# ---------------------------------------------------------------- app data
def parse_strings(path):
    out = {}
    for m in re.finditer(r'^"([^"]+)"\s*=\s*"((?:[^"\\]|\\.)*)";', path.read_text(encoding="utf-8"), re.M):
        out[m.group(1)] = m.group(2).replace('\\"', '"')
    return out


def parse_city_enum():
    """TravelCity: case → (rawValue, displayName key, localQualifier, lat, lng)."""
    src = (APP / "Models" / "TravelCity.swift").read_text(encoding="utf-8")
    raw = dict(re.findall(r'case (\w+) = "([^"]+)"', src))
    disp = dict(re.findall(r'case \.(\w+):\s*return String\(localized: "([^"]+)"\)', src))
    local_block = src[src.index("var localQualifier"):]
    local = dict(re.findall(r'case \.(\w+):\s*return "([^"]*)"', local_block))
    coord = {}
    for case, lat, lng in re.findall(r'case \.(\w+):\s*return "([\d.]+)°N · ([\d.]+)°E"', src):
        coord[case] = (float(lat), float(lng))
    cities = {}
    for case, rv in raw.items():
        if case == "none":
            continue
        cities[case] = {"raw": rv, "key": disp[case], "local": local[case], "coord": coord[case]}
    return cities


def ascii_slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = s.lower().replace("'", "").replace("’", "")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def load_places():
    src = (APP / "Data" / "RecommendedPlaces.swift").read_text(encoding="utf-8")
    pat = re.compile(r'RecommendedPlace\(name: "([^"]*)", localName: "([^"]*)", country: \.(\w+), city: \.(\w+)\)')
    places = [dict(name=n, local=l, country=c, city=ci) for n, l, c, ci in pat.findall(src)]
    if len(places) != 411:
        sys.exit(f"expected 411 places, parsed {len(places)}")
    seen = {}
    for p in places:
        base = ascii_slug(p["name"]) or "place"
        slug = base
        if (p["country"], slug) in seen:
            slug = f"{base}-{ascii_slug(CITIES[p['city']]['raw'])}"
        n = 2
        while (p["country"], slug) in seen:
            slug = f"{base}-{n}"
            n += 1
        seen[(p["country"], slug)] = p
        p["slug"] = slug
        p["cslug"] = COUNTRY_SLUG[p["country"]]
        p["key"] = f"{p['cslug']}/{slug}"
    return places


CITIES = parse_city_enum()
STRINGS = {lang: parse_strings(APP / f"{LPROJ[lang]}.lproj" / "Localizable.strings") for lang in LANGS}


def city_name(case, lang):
    return STRINGS[lang][CITIES[case]["key"]]


def country_name(country, lang):
    return STRINGS[lang][f"country.{COUNTRY_KEY[country]}"]


# ---------------------------------------------------------------- spelling variants
_SIM_TRAD = ("东東 车車 门門 马馬 鸟鳥 龙龍 鱼魚 见見 长長 风風 飞飛 广廣 庙廟 园園 馆館 汤湯 湾灣 场場 桥橋 楼樓 "
             "区區 华華 国國 观觀 记記 汉漢 云雲 关關 坛壇 阳陽 线線 铁鐵 历歷 纪紀 乐樂 兰蘭 岛島 头頭 万萬 庆慶 "
             "宝寶 鸡雞 饭飯 点點 汇匯 业業 时時 间間 电電 视視 买買 卖賣 钟鐘 览覽 艺藝 术術 剧劇 际際 会會 环環 "
             "滩灘 层層 厦廈 圣聖 发發 体體 厅廳 处處 号號 读讀 书書 画畫 刘劉 张張 陈陳 杨楊 赵趙 吴吳 郑鄭 罗羅 "
             "叶葉 苏蘇 卢盧 邓鄧 许許 钱錢 银銀 鲜鮮 虾蝦 烧燒 鸭鴨 猪豬 肠腸 饺餃 丝絲 酱醬 龟龜 凤鳳 狮獅 宁寧 "
             "静靜 丰豐 沪滬 兴興 讲講 语語 话話 说說 齐齊 贝貝 门門 塔塔 网網 开開 机機 港港 湖湖 动動 物物 "
             "馆館 剧劇 车車 渔漁 灯燈 庙廟 宫宮 坊坊 寿壽 鸣鳴 门門 应應 满滿 测測 证證 节節 帅帥 将將 战戰 "
             "军軍 农農 尔爾 亚亞 伦倫 欧歐 罗羅 兰蘭 归歸 远遠 达達 边邊 过過 还還 进進 运運 这這 连連 选選 "
             "缘緣 纳納 红紅 绿綠 蓝藍 紫紫 黄黃 广廣 莲蓮 荣榮 药藥 叶葉 铜銅 钻鑽 锦錦 闻聞 阁閣 陆陸 隆隆")
# Japanese-only (shinjitai) forms, e.g. 広蔵市場 for 광장시장 (traditional 廣藏, simplified 广藏).
JP_SHINJITAI = set("広駅沢浜鉄図売読楽桜恵歳県円気発辺継転雑験戦歴労営覚蔵拝渋徳黒")
SIMP_ONLY, TRAD_ONLY = set(), set()
for _pair in _SIM_TRAD.split():
    if _pair[0] != _pair[1]:
        SIMP_ONLY.add(_pair[0])
        TRAD_ONLY.add(_pair[1])


def script_of(s, country):
    if re.search(r"[가-힣]", s):
        return "hangul"
    if re.search(r"[฀-๿]", s):
        return "thai"
    if re.search(r"[぀-ヿ]", s):
        return "japanese"
    if re.search(r"[一-鿿]", s):
        if country == "japan" or any(c in JP_SHINJITAI for c in s):
            return "japanese"
        sim, trad = any(c in SIMP_ONLY for c in s), any(c in TRAD_ONLY for c in s)
        if sim and not trad:
            return "simplified"
        if trad and not sim:
            return "traditional"
        return "han"
    if re.search(r"[À-ỹ]", s) and country == "vietnam":
        return "vietnamese"
    return "latin"


def nkey(s):
    s = unicodedata.normalize("NFKC", s).lower()
    return re.sub(r"[\W_]+", "", s)


def _load_aliases():
    data = json.loads((APP / "Data" / "aliases.json").read_text(encoding="utf-8"))["aliases"]
    by_country = {}
    for r in data:
        by_country.setdefault(r["country"], []).append(r)
    return by_country


ALIASES = _load_aliases()


QUALIFIER_WORDS = ["map", "지도", "地图", "地圖", "マップ", "야경", "夜景", "nightview"]


def qualifier_tokens(p):
    case = p["city"]
    toks = {CITIES[case]["raw"], CITIES[case]["local"], CITIES[case]["local"].rstrip("ฯ"),
            COUNTRY_EN[p["country"]]}
    toks |= {city_name(case, lang) for lang in LANGS}
    toks |= {country_name(p["country"], lang) for lang in LANGS}
    toks |= set(QUALIFIER_WORDS)
    return sorted({nkey(t) for t in toks if nkey(t)}, key=len, reverse=True)


GENERATED_TAGS = {"recommended-place-variant"}
STATION_WORDS = ("station", "역", "站", "駅")


def collect_variants(p):
    """All spellings the app knows for this place → (variants list, is_chain).

    Generated qualifier permutations ("Shanghai 外滩", "WaitanTheBund") are skipped;
    variants that only add a city/country/"map" word to a known spelling are dropped."""
    keys = {nkey(p["local"]), nkey(p["name"])} | {nkey(x) for x in p["name"].split(" · ")}
    keys.discard("")
    found, chain = [], False
    for r in ALIASES[COUNTRY_EN[p["country"]]]:
        terms = [r["input"]] + r["candidates"]
        if not keys & {nkey(t) for t in terms}:
            continue
        if "generated-chain" in r.get("tags", []):
            chain = True
        if GENERATED_TAGS & set(r.get("tags", [])):
            continue
        found.extend(terms)
    parts = p["name"].split(" · ") if " · " in p["name"] else []
    own = [p["name"]] + parts
    ordered, seen = [], {nkey(p["local"])}
    for v in own + found:
        v = v.strip()
        k = nkey(v)
        if not k or k in seen:
            continue
        seen.add(k)
        ordered.append(v)
    qtoks = qualifier_tokens(p)
    base = {nkey(v) for v in ordered} | {nkey(p["local"])}
    protected = {nkey(x) for x in own}
    is_station = any(w in nkey(p["name"]) or w in p["local"] for w in STATION_WORDS)
    out = []
    for v in ordered:
        k = nkey(v)
        if k not in protected:
            stripped = k
            for t in qtoks:
                stripped = stripped.replace(t, "")
            if stripped != k and (not stripped or stripped in base):
                continue
            if not is_station and any(k.endswith(w) for w in STATION_WORDS):
                continue
        out.append(v)
    return out, chain


def display_variants(p, limit=8):
    """Up to `limit` variants, the English name first, then one per script, then the rest."""
    vs, _ = collect_variants(p)
    first, rest, scripts = vs[:1], [], set()
    for v in vs[1:]:
        sc = script_of(v, p["country"])
        if sc not in scripts:
            scripts.add(sc)
            first.append(v)
        else:
            rest.append(v)
    return (first + rest)[:limit]


def geo_input(places):
    return [{"slug": p["key"], "name": p["name"], "localName": p["local"],
             "cityLocal": CITIES[p["city"]]["local"], "cityEn": CITIES[p["city"]]["raw"],
             "cityLat": CITIES[p["city"]]["coord"][0], "cityLng": CITIES[p["city"]]["coord"][1],
             "terms": collect_variants(p)[0], "chain": collect_variants(p)[1]}
            for p in places]


if __name__ == "__main__" and "--geo-input" in sys.argv:
    out = pathlib.Path(sys.argv[sys.argv.index("--geo-input") + 1])
    out.write_text(json.dumps(geo_input(load_places()), ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {out}")
    sys.exit(0)


# ---------------------------------------------------------------- coordinates
# The first shortcut section per country in RecommendedPlaces.swift is a brand list (tea, coffee,
# drugstores...). A chain has many branches and we cannot know which one the traveller means, so
# chains never get a pin. Brand entries that name one specific store or mall are kept.
BRAND_SECTIONS = {"taiwan.taipei.tea", "china.shanghai.brands", "japan.tokyo.beauty", "thailand.bangkok.spa",
                  "vietnam.hcm.coffee", "hk.beauty.shopping", "macau.shopping.beauty"}
SPECIFIC_STORES = {"誠品生活松菸", "@cosme TOKYO", "ユニクロ 銀座", "無印良品 銀座", "Big C Ratchadamri",
                   "海港城", "K11 MUSEA", "新八佰伴", "倫敦人購物中心"}
# Chains that appear outside the brand sections (verified against the geocoding review).
CHAIN_EXTRA = set()


def chain_locals():
    src = (APP / "Data" / "RecommendedPlaces.swift").read_text(encoding="utf-8")
    out = set(CHAIN_EXTRA)
    for sid, names in re.findall(r'section\("([^"]+)", "[^"]*", "[^"]*", \.\w+, \[([^\]]*)\]\)', src):
        if sid in BRAND_SECTIONS:
            out |= set(re.findall(r'"([^"]*)"', names)) - SPECIFIC_STORES
    return out


def load_geo(places):
    chains = chain_locals()
    no_pin = {p["key"] for p in places if p["local"] in chains}
    geo = {}
    if GEO_CACHE.exists():
        for slug, e in json.loads(GEO_CACHE.read_text(encoding="utf-8")).items():
            if e.get("status") == "ok":
                geo[slug] = (float(e["lat"]), float(e["lng"]))
    if OVERRIDES.exists():
        with OVERRIDES.open(encoding="utf-8") as f:
            for row in csv.DictReader(f):
                slug = (row.get("slug") or "").strip()
                if not slug or slug.startswith("#"):
                    continue
                lat, lng = (row.get("lat") or "").strip(), (row.get("lng") or "").strip()
                if lat and lng:
                    geo[slug] = (float(lat), float(lng))
                else:
                    geo.pop(slug, None)
    for k in no_pin:
        geo.pop(k, None)
    return geo


# ---------------------------------------------------------------- UI strings
APPLE_SVG = '<svg viewBox="0 0 384 512" aria-hidden="true"><path d="M318.7 268.7c-.2-36.7 16.4-64.4 50-84.8-18.8-26.9-47.2-41.7-84.7-44.6-35.5-2.8-74.3 20.7-88.5 20.7-15 0-49.4-19.7-76.4-19.7C63.3 141.2 4 184.8 4 273.5q0 39.3 14.4 81.2c12.8 36.7 59 126.7 107.2 125.2 25.2-.6 43-17.9 75.8-17.9 31.8 0 48.3 17.9 76.4 17.9 48.6-.7 90.4-82.5 102.6-119.3-65.2-30.7-61.7-90-61.7-91.9zm-56.6-164.2c27.3-32.4 24.8-61.9 24-72.5-24.1 1.4-52 16.4-67.9 34.9-17.5 19.8-27.8 44.3-25.6 71.9 26.1 2 49.9-11.4 69.5-34.3z"/></svg>'
LANG_LABEL = {"en": "EN", "ko": "한국어", "ja": "日本語", "zh-hans": "简体", "zh-hant": "繁體"}
FONT = {"en": None, "ko": '"Apple SD Gothic Neo", "Pretendard"', "ja": '"Hiragino Kaku Gothic ProN", "Hiragino Sans", "Yu Gothic"',
        "zh-hans": '"PingFang SC", "Heiti SC"', "zh-hant": '"PingFang TC", "Heiti TC"'}

APP_NAMES = {
    "en": {"naver": "Naver Map", "kakao": "KakaoMap", "amap": "Amap (Gaode)", "google": "Google Maps", "apple": "Apple Maps"},
    "ko": {"naver": "네이버 지도", "kakao": "카카오맵", "amap": "고덕지도", "google": "구글 지도", "apple": "애플 지도"},
    "ja": {"naver": "NAVER マップ", "kakao": "カカオマップ", "amap": "高徳地図", "google": "Google マップ", "apple": "Apple マップ"},
    "zh-hans": {"naver": "Naver 地图", "kakao": "Kakao 地图", "amap": "高德地图", "google": "谷歌地图", "apple": "苹果地图"},
    "zh-hant": {"naver": "Naver 地圖", "kakao": "Kakao 地圖", "amap": "高德地圖", "google": "Google 地圖", "apple": "Apple 地圖"},
}
GLYPH = {"naver": "N", "kakao": "K", "amap": "高", "google": "G", "apple": "A"}

T = {
    "en": {
        "brand": "Local Link", "places": "Places", "and": " & ",
        "h1": "How to find {n} on {apps}",
        "title": "{n} ({local}) — find it on {apps} | Local Link",
        "desc": "{n} in {city}, {country}. Local maps match the local name {local}: copy it, show it full-screen, or open {apps} in one tap.",
        "lede": "Local map apps match the local-script name. Search for <b>{local}</b> — or show it to a taxi driver.",
        "copy": "Copy", "copied": "Copied", "show": "Show to a taxi driver or local", "close": "Tap anywhere to close",
        "var_h": "Other spellings", "var_note": "Spellings the Local Link app recognizes for this place.",
        "scripts": {"latin": "Latin / English", "hangul": "Korean (Hangul)", "japanese": "Japanese", "simplified": "Simplified Chinese",
                    "traditional": "Traditional Chinese", "han": "Chinese characters", "thai": "Thai", "vietnamese": "Vietnamese"},
        "maps_h": "Maps that work in {country}",
        "why": {"korea": "In Korea, Google Maps covers public transit only — no walking directions for the last stretch. Naver Map and KakaoMap do the walk, and they match Korean names.",
                "china": "Google Maps doesn't work in mainland China. Amap (高德地图) is the map locals use; Apple Maps also works.",
                "other": "Google Maps works well here and matches local-script names; Apple Maps is the built-in alternative."},
        "search_btn": "Search in {app}", "open_note": "Opens the app if it's installed, otherwise the web map.",
        "route_h": "Walking route", "route_btn": "Walk there with {app}",
        "route_note": "Destination pin from an Apple Maps search for this name — check the sign when you arrive.",
        "more_h": "More places in {city}",
        "cta_h": "Search any place the local way",
        "cta_p": "Local Link converts the names you know into local script and opens them in the map that works there. Free on iPhone and iPad.",
        "badge_small": "Download on the", "badge_aria": "Download on the App Store",
        "owner": "Own this shop or place? Make a “how to find us” card →",
        "hub_title": "Find places on local maps — {count} places in 8 destinations | Local Link",
        "hub_desc": "Local-script names, other spellings and one-tap map links for {count} places in Korea, Japan, China, Taiwan, Thailand, Vietnam, Hong Kong and Macau.",
        "hub_h1": "Find it on the map locals use",
        "hub_lede": "For each place: the local-script name to search, the spellings you might know, and links that open Naver Map, KakaoMap, Amap, Google Maps or Apple Maps.",
        "c_title": "{country}: {count} places by local name — {apps} | Local Link",
        "c_desc": "{count} places in {country} with the local-script name to search in {apps}, other spellings and one-tap map links.",
        "c_h1": "{country}: find places on {apps}",
        "n_places": "{n} places",
        "f_contact": "Contact", "f_privacy": "Privacy", "f_terms": "Terms",
    },
    "ko": {
        "brand": "로컬링크", "places": "장소", "and": "·",
        "h1": "{n}, {apps}에서 찾는 법",
        "title": "{n} ({local}) — {apps}에서 찾기 | 로컬링크",
        "desc": "{country} {city}의 {n}. 현지 지도앱은 현지 표기 {local}로 찾습니다. 복사하거나 크게 보여주거나, {apps}를 한 번에 여세요.",
        "lede": "현지 지도앱은 현지 문자 이름으로 검색해야 나옵니다. <b>{local}</b>로 검색하거나, 택시 기사님께 보여주세요.",
        "copy": "복사", "copied": "복사됨", "show": "택시 기사·현지인에게 보여주기", "close": "아무 곳이나 누르면 닫혀요",
        "var_h": "다른 표기", "var_note": "로컬링크 앱이 이 장소로 알아듣는 표기들입니다.",
        "scripts": {"latin": "로마자·영문", "hangul": "한글", "japanese": "일본어", "simplified": "간체자",
                    "traditional": "번체자", "han": "한자", "thai": "태국어", "vietnamese": "베트남어"},
        "maps_h": "{country}에서 되는 지도",
        "why": {"korea": "한국에서 구글 지도는 대중교통 길찾기만 됩니다 — 도보 길찾기가 없어요. 걸어가는 마지막 구간은 네이버 지도·카카오맵이 맡고, 한글 이름으로 찾아야 합니다.",
                "china": "중국 본토에서는 구글 지도를 쓸 수 없습니다. 현지인은 고덕지도(高德地图)를 쓰고, 애플 지도도 동작합니다.",
                "other": "이곳은 구글 지도가 잘 되고 현지 문자 이름도 잘 찾습니다. 애플 지도는 기본 대안입니다."},
        "search_btn": "{app}에서 검색", "open_note": "앱이 설치돼 있으면 앱으로, 없으면 웹 지도로 열립니다.",
        "route_h": "도보 길찾기", "route_btn": "{app}로 걸어가기",
        "route_note": "목적지 핀은 이 이름으로 애플 지도를 검색한 결과입니다. 도착하면 간판을 확인하세요.",
        "more_h": "{city}의 다른 장소",
        "cta_h": "어떤 장소든 현지 방식으로 검색하세요",
        "cta_p": "로컬링크는 아는 이름을 현지 문자로 바꿔, 그곳에서 실제로 되는 지도로 열어줍니다. iPhone·iPad 무료.",
        "badge_small": "다운로드는", "badge_aria": "App Store에서 다운로드",
        "owner": "이 가게·장소의 주인이신가요? 찾아오는 길 카드 만들기 →",
        "hub_title": "현지 지도에서 장소 찾기 — 8개 여행지 {count}곳 | 로컬링크",
        "hub_desc": "한국·일본·중국·대만·태국·베트남·홍콩·마카오 {count}곳의 현지 표기, 다른 표기, 지도앱 바로 열기.",
        "hub_h1": "현지인이 쓰는 지도에서 찾기",
        "hub_lede": "장소마다 검색할 현지 표기, 알고 있을 법한 다른 표기, 그리고 네이버 지도·카카오맵·고덕지도·구글·애플 지도를 바로 여는 링크를 모았습니다.",
        "c_title": "{country} {count}곳 현지 표기 — {apps} | 로컬링크",
        "c_desc": "{country} {count}곳을 {apps}에서 찾는 현지 표기, 다른 표기, 지도 바로 열기.",
        "c_h1": "{country}, {apps}에서 찾기",
        "n_places": "{n}곳",
        "f_contact": "문의", "f_privacy": "개인정보 처리방침", "f_terms": "이용약관",
    },
    "ja": {
        "brand": "ロコリンク", "places": "スポット", "and": "・",
        "h1": "{n}を{apps}で探す方法",
        "title": "{n}（{local}）を{apps}で探す | ロコリンク",
        "desc": "{country}・{city}の{n}。現地の地図アプリは現地表記「{local}」で探します。コピー、全画面表示、{apps}をワンタップで。",
        "lede": "現地の地図アプリは現地の文字の名前で検索します。<b>{local}</b> で検索するか、タクシーの運転手に見せましょう。",
        "copy": "コピー", "copied": "コピーしました", "show": "タクシー運転手・現地の人に見せる", "close": "どこかをタップで閉じる",
        "var_h": "ほかの表記", "var_note": "ロコリンクアプリがこの場所として認識する表記です。",
        "scripts": {"latin": "ローマ字・英語", "hangul": "韓国語（ハングル）", "japanese": "日本語", "simplified": "簡体字",
                    "traditional": "繁体字", "han": "漢字", "thai": "タイ語", "vietnamese": "ベトナム語"},
        "maps_h": "{country}で使える地図",
        "why": {"korea": "韓国の Google マップは電車・バスの案内まで。最後の徒歩ルートは出ません。歩く区間は NAVER マップ・カカオマップの出番で、ハングルの名前で探します。",
                "china": "中国本土では Google マップが使えません。現地の人は高徳地図（高德地图）を使います。Apple マップも使えます。",
                "other": "ここでは Google マップがよく使え、現地の文字の名前もよく見つかります。Apple マップも使えます。"},
        "search_btn": "{app}で検索", "open_note": "アプリが入っていればアプリで、なければウェブ地図で開きます。",
        "route_h": "徒歩ルート", "route_btn": "{app}で歩いて行く",
        "route_note": "目的地のピンはこの名前で Apple マップを検索した結果です。到着したら看板を確認してください。",
        "more_h": "{city}のほかのスポット",
        "cta_h": "どんな場所も現地のやり方で検索",
        "cta_p": "ロコリンクは知っている名前を現地の文字に変換し、その国で使える地図で開きます。iPhone・iPad 無料。",
        "badge_small": "ダウンロードは", "badge_aria": "App Store でダウンロード",
        "owner": "このお店・場所のオーナーですか？ 道案内カードを作る →",
        "hub_title": "現地の地図でスポットを探す — 8つの旅行先 {count}か所 | ロコリンク",
        "hub_desc": "韓国・日本・中国・台湾・タイ・ベトナム・香港・マカオの{count}か所の現地表記、ほかの表記、地図アプリをワンタップで。",
        "hub_h1": "現地の人が使う地図で探す",
        "hub_lede": "スポットごとに、検索する現地表記、知っているかもしれないほかの表記、NAVER マップ・カカオマップ・高徳地図・Google・Apple マップを開くリンクをまとめました。",
        "c_title": "{country}の{count}か所を現地表記で — {apps} | ロコリンク",
        "c_desc": "{country}の{count}か所を{apps}で探すための現地表記、ほかの表記、地図リンク。",
        "c_h1": "{country}：{apps}で探す",
        "n_places": "{n}か所",
        "f_contact": "お問い合わせ", "f_privacy": "プライバシーポリシー", "f_terms": "利用規約",
    },
    "zh-hans": {
        "brand": "当地链接", "places": "地点", "and": "、",
        "h1": "如何在{apps}上找到{n}",
        "title": "{n}（{local}）— 在{apps}上查找 | 当地链接",
        "desc": "{country}{city}的{n}。当地地图要用当地写法「{local}」搜索：复制、全屏展示，或一键打开{apps}。",
        "lede": "当地地图应用要用当地文字的名称才搜得到。搜索 <b>{local}</b>，或者给出租车司机看。",
        "copy": "复制", "copied": "已复制", "show": "给出租车司机或当地人看", "close": "点击任意处关闭",
        "var_h": "其他写法", "var_note": "当地链接应用能识别的这个地点的写法。",
        "scripts": {"latin": "拉丁字母 / 英文", "hangul": "韩文", "japanese": "日文", "simplified": "简体中文",
                    "traditional": "繁体中文", "han": "汉字", "thai": "泰文", "vietnamese": "越南文"},
        "maps_h": "在{country}能用的地图",
        "why": {"korea": "在韩国，谷歌地图只有公共交通路线，没有步行导航。最后一段步行要靠 Naver 地图和 Kakao 地图，而且要用韩文名称搜索。",
                "china": "中国大陆无法使用谷歌地图。当地人用高德地图，苹果地图也可以用。",
                "other": "这里谷歌地图很好用，也能搜到当地文字的名称；苹果地图是系统自带的备选。"},
        "search_btn": "在{app}中搜索", "open_note": "已安装应用时用应用打开，否则打开网页地图。",
        "route_h": "步行路线", "route_btn": "用{app}步行前往",
        "route_note": "目的地坐标来自用此名称搜索苹果地图的结果，到达后请核对招牌。",
        "more_h": "{city}的其他地点",
        "cta_h": "用当地的方式搜索任何地点",
        "cta_p": "当地链接把你知道的名字转换成当地文字，并用当地能用的地图打开。iPhone · iPad 免费。",
        "badge_small": "下载于", "badge_aria": "在 App Store 下载",
        "owner": "你是这家店或这个地点的主人吗？制作“怎么找到我们”卡片 →",
        "hub_title": "在当地地图上找地点 — 8 个目的地 {count} 处 | 当地链接",
        "hub_desc": "韩国、日本、中国、台湾、泰国、越南、香港、澳门 {count} 处地点的当地写法、其他写法和一键地图链接。",
        "hub_h1": "在当地人用的地图上找到它",
        "hub_lede": "每个地点都有要搜索的当地写法、你可能知道的其他写法，以及一键打开 Naver、Kakao、高德、谷歌或苹果地图的链接。",
        "c_title": "{country} {count} 处地点的当地写法 — {apps} | 当地链接",
        "c_desc": "{country} {count} 处地点：在{apps}中搜索的当地写法、其他写法和一键地图链接。",
        "c_h1": "{country}：在{apps}上查找",
        "n_places": "{n} 处",
        "f_contact": "联系我们", "f_privacy": "隐私政策", "f_terms": "服务条款",
    },
    "zh-hant": {
        "brand": "在地連結", "places": "地點", "and": "、",
        "h1": "如何在{apps}上找到{n}",
        "title": "{n}（{local}）— 在{apps}上查找 | 在地連結",
        "desc": "{country}{city}的{n}。在地地圖要用當地寫法「{local}」搜尋：複製、全螢幕展示，或一鍵開啟{apps}。",
        "lede": "在地地圖 App 要用當地文字的名稱才搜得到。搜尋 <b>{local}</b>，或拿給計程車司機看。",
        "copy": "複製", "copied": "已複製", "show": "拿給計程車司機或當地人看", "close": "點任意處關閉",
        "var_h": "其他寫法", "var_note": "在地連結 App 能辨識的這個地點的寫法。",
        "scripts": {"latin": "拉丁字母 / 英文", "hangul": "韓文", "japanese": "日文", "simplified": "簡體中文",
                    "traditional": "繁體中文", "han": "漢字", "thai": "泰文", "vietnamese": "越南文"},
        "maps_h": "在{country}能用的地圖",
        "why": {"korea": "在韓國，Google 地圖只有大眾運輸路線，沒有步行導航。最後一段步行要靠 Naver 地圖和 Kakao 地圖，而且要用韓文名稱搜尋。",
                "china": "中國大陸無法使用 Google 地圖。當地人用高德地圖，Apple 地圖也可以用。",
                "other": "這裡 Google 地圖很好用，也搜得到當地文字的名稱；Apple 地圖是系統內建的備選。"},
        "search_btn": "在{app}中搜尋", "open_note": "已安裝 App 時用 App 開啟，否則開啟網頁地圖。",
        "route_h": "步行路線", "route_btn": "用{app}步行前往",
        "route_note": "目的地座標來自用此名稱搜尋 Apple 地圖的結果，抵達後請核對招牌。",
        "more_h": "{city}的其他地點",
        "cta_h": "用在地的方式搜尋任何地點",
        "cta_p": "在地連結把你知道的名稱轉成在地文字，並用當地能用的地圖開啟。iPhone · iPad 免費。",
        "badge_small": "下載於", "badge_aria": "在 App Store 下載",
        "owner": "你是這家店或這個地點的主人嗎？製作「怎麼找到我們」卡片 →",
        "hub_title": "在在地地圖上找地點 — 8 個目的地 {count} 處 | 在地連結",
        "hub_desc": "韓國、日本、中國、台灣、泰國、越南、香港、澳門 {count} 處地點的在地寫法、其他寫法和一鍵地圖連結。",
        "hub_h1": "在當地人用的地圖上找到它",
        "hub_lede": "每個地點都有要搜尋的在地寫法、你可能知道的其他寫法，以及一鍵開啟 Naver、Kakao、高德、Google 或 Apple 地圖的連結。",
        "c_title": "{country} {count} 處地點的在地寫法 — {apps} | 在地連結",
        "c_desc": "{country} {count} 處地點：在{apps}中搜尋的在地寫法、其他寫法和一鍵地圖連結。",
        "c_h1": "{country}：在{apps}上查找",
        "n_places": "{n} 處",
        "f_contact": "聯絡我們", "f_privacy": "隱私權政策", "f_terms": "服務條款",
    },
}
COUNTRY_ORDER = ["korea", "japan", "china", "taiwan", "hongKong", "macau", "thailand", "vietnam"]
FLAG = {"korea": "🇰🇷", "japan": "🇯🇵", "china": "🇨🇳", "taiwan": "🇹🇼", "hongKong": "🇭🇰", "macau": "🇲🇴",
        "thailand": "🇹🇭", "vietnam": "🇻🇳"}
# Script that a reader of each UI language can read, for picking the displayed place name.
LANG_SCRIPTS = {"en": ["latin"], "ko": ["hangul"], "ja": ["japanese"],
                "zh-hans": ["simplified", "han"], "zh-hant": ["traditional", "han"]}
LOCAL_LANG = {"korea": "ko", "japan": "ja", "china": "zh-Hans", "taiwan": "zh-Hant", "hongKong": "zh-Hant",
              "macau": "zh-Hant", "thailand": "th", "vietnam": "vi"}
SCRIPT_LANG = {"hangul": "ko", "japanese": "ja", "simplified": "zh-Hans", "traditional": "zh-Hant", "thai": "th",
               "vietnamese": "vi", "latin": "en"}
LOCAL_SCRIPT_OK = {"ko": {"korea"}, "ja": {"japan"}, "zh-hans": {"china"},
                   "zh-hant": {"taiwan", "hongKong", "macau"}}


def lang_attr(code):
    return f' lang="{code}"' if code else ""


def esc(s):
    return html.escape(s, quote=True)


def q(s):
    """RFC 3986 unreserved only (same rule as the app's MapLauncher, commit c62252b)."""
    from urllib.parse import quote
    return quote(s, safe="")


def providers(country):
    return PROVIDERS.get(country, DEFAULT_PROVIDERS)


def primary_apps(country, lang):
    names = APP_NAMES[lang]
    if country == "korea":
        return names["naver"] + T[lang]["and"] + names["kakao"]
    if country == "china":
        return names["amap"]
    return names["google"]


def why_key(country):
    return country if country in ("korea", "china") else "other"


def display_name(p, lang):
    if lang == "en":
        return p["name"]
    if p["country"] in LOCAL_SCRIPT_OK[lang]:
        return p["local"]
    for v in collect_variants(p)[0]:
        if script_of(v, p["country"]) in LANG_SCRIPTS[lang]:
            return v
    if script_of(p["local"], p["country"]) in LANG_SCRIPTS[lang]:
        return p["local"]
    return p["name"]


# ---------------------------------------------------------------- URLs
def page_path(lang, cslug=None, slug=None):
    path = f"/locallink/{LANG_DIR[lang]}places/"
    if cslug:
        path += f"{cslug}/"
    if slug:
        path += f"{slug}/"
    return path


def search_query(p, prov):
    """SavedPlacesView.mapQuery with the place's localName as the query."""
    c = CITIES[p["city"]]
    if prov in LOCAL_QUALIFIED:
        return f"{p['local']} {c['local']}"
    return f"{p['local']} {c['raw']} {COUNTRY_EN[p['country']]}"


def search_links(p, prov, page_url):
    e = q(search_query(p, prov))
    if prov == "naver":   # Naver: appname is required; for mobile web it is the page URL
        return f"nmap://search?query={e}&appname={q(page_url)}", f"https://map.naver.com/p/search/{e}"
    if prov == "kakao":
        return f"kakaomap://search?q={e}", f"https://map.kakao.com/link/search/{e}"
    if prov == "amap":    # Amap iOS URI: poi search takes `name` (+ required sourceApplication)
        return f"iosamap://poi?sourceApplication=LocalLink&name={e}", f"https://uri.amap.com/search?keyword={e}&src=LocalLink"
    if prov == "google":
        return f"comgooglemaps://?q={e}", f"https://www.google.com/maps/search/?api=1&query={e}"
    return None, f"https://maps.apple.com/?q={e}"


# MapKit returns GCJ-02 coordinates in mainland China (verified: Shanghai Tower came back ~+0.004° lng
# off its WGS-84 position). Amap expects GCJ-02, but schema.org geo and Apple's URL scheme assume
# WGS-84, so Chinese pins are used only for the Amap route.
GCJ02_COUNTRIES = {"china"}


def route_providers(country):
    # Korea: Google has no walking directions there, so only Naver/Kakao get a route button.
    if country == "korea":
        return ["naver", "kakao"]
    if country in GCJ02_COUNTRIES:
        return ["amap"]
    return providers(country)


def route_links(p, prov, lat, lng, page_url):
    name = q(p["local"])
    ll = f"{lat:.6f},{lng:.6f}"
    if prov == "naver":
        return (f"nmap://route/walk?dlat={lat:.6f}&dlng={lng:.6f}&dname={name}&appname={q(page_url)}",
                f"https://map.naver.com/p/search/{q(search_query(p, 'naver'))}")
    if prov == "kakao":
        return f"kakaomap://route?ep={ll}&by=FOOT", f"https://map.kakao.com/link/to/{name},{ll}"
    if prov == "amap":    # coordinates from MapKit in mainland China are GCJ-02 → dev=0
        return (f"iosamap://path?sourceApplication=LocalLink&dlat={lat:.6f}&dlon={lng:.6f}&dname={name}&dev=0&t=2",
                f"https://uri.amap.com/navigation?to={lng:.6f},{lat:.6f},{name}&mode=walk&src=LocalLink&callnative=0")
    if prov == "google":
        return (f"comgooglemaps://?daddr={ll}&directionsmode=walking",
                f"https://www.google.com/maps/dir/?api=1&destination={q(ll)}&travelmode=walking")
    return None, f"https://maps.apple.com/?daddr={ll}&dirflg=w"


# ---------------------------------------------------------------- page chrome
def head(lang, title, desc, canonical_path, alt_paths, jsonld):
    canonical = SITE + canonical_path
    alts = [f'<link rel="alternate" hreflang="{HTML_LANG[l]}" href="{SITE}{alt_paths[l]}">' for l in LANGS]
    alts.append(f'<link rel="alternate" hreflang="x-default" href="{SITE}{alt_paths["en"]}">')
    font = (f'<style>body{{font-family:-apple-system,BlinkMacSystemFont,{FONT[lang]},"Segoe UI",sans-serif}}</style>\n'
            if FONT[lang] else "")
    return f"""<!doctype html>
<html lang="{HTML_LANG[lang]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<!-- seo:build-owned locallink/places_build.py -->
<title>{esc(title)}</title>
<link rel="canonical" href="{canonical}">
<meta name="description" content="{esc(desc)}">
{chr(10).join(alts)}
<meta name="color-scheme" content="light dark">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{SITE}/locallink/og.png">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="kkiruk studio">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="/locallink/assets/icon-180.png">
<link rel="apple-touch-icon" href="/locallink/assets/icon-180.png">
<link rel="stylesheet" href="/locallink/places/places.css">
{font}<script src="/ga.js"></script>
<script type="application/ld+json">
{json.dumps(jsonld, ensure_ascii=False, separators=(",", ":"))}
</script>
</head>
"""


def nav(lang, alt_paths):
    links = "".join(
        f'<a href="{alt_paths[l]}"{" class=cur aria-current=page" if l == lang else ""} hreflang="{HTML_LANG[l]}">{LANG_LABEL[l]}</a>'
        for l in LANGS)
    return f"""<body>
<nav class="top"><div class="wrap">
  <a class="wordmark" href="/locallink/{LANG_DIR[lang]}"><img src="/locallink/assets/icon-180.png" alt="" width="28" height="28"><span>LOCAL·LINK</span></a>
  <div class="lang">{links}</div>
</div></nav>
"""


def crumbs_html(items):
    parts = []
    for i, (label, path) in enumerate(items):
        if i == len(items) - 1:
            parts.append(f'<span aria-current="page">{esc(label)}</span>')
        else:
            parts.append(f'<a href="{path}">{esc(label)}</a>')
    return '<ol class="crumbs">' + "".join(f"<li>{x}</li>" for x in parts) + "</ol>"


def crumbs_ld(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": label, "item": SITE + path}
        for i, (label, path) in enumerate(items)]}


def badge(lang):
    t = T[lang]
    return (f'<a class="store-badge" href="{APP_STORE_URL}" aria-label="{t["badge_aria"]}">{APPLE_SVG}'
            f'<span class="txt"><small>{t["badge_small"]}</small><strong>App Store</strong></span></a>')


def cta(lang, owner=True):
    t = T[lang]
    own = f'<p class="owner"><a href="/locallink/card/">{t["owner"]}</a></p>' if owner else ""
    return f"""<section class="cta-band"><div class="wrap">
  <h2>{t['cta_h']}</h2>
  <p>{t['cta_p']}</p>
  {badge(lang)}
  {own}
</div></section>
"""


def footer(lang):
    t = T[lang]
    return f"""<footer><div class="wrap">
  <span class="brand">kkiruk studio</span>
  <span class="links"><a href="mailto:kkirukstudio.help@gmail.com">{t['f_contact']}</a><a href="/legal/privacy/">{t['f_privacy']}</a><a href="/legal/terms/">{t['f_terms']}</a></span>
  <span>© 2026 kkiruk studio</span>
</div></footer>
<script src="/locallink/places/places.js" defer></script>
</body>
</html>
"""


ORG = {"@type": "Organization", "@id": SITE + "/#organization", "name": "kkiruk studio", "url": SITE + "/"}
WEBSITE = {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "kkiruk studio",
           "publisher": {"@id": SITE + "/#organization"}}


def map_buttons(links, lang, kind):
    out = []
    for prov, app, web in links:
        label = T[lang]["search_btn" if kind == "search" else "route_btn"].format(app=APP_NAMES[lang][prov])
        data = f' data-app="{esc(app)}"' if app else ""
        out.append(f'<a class="mapbtn" href="{esc(web)}"{data} rel="nofollow noopener"><span class="g">{GLYPH[prov]}</span>{esc(label)}</a>')
    return '<div class="mapbtns">' + "".join(out) + "</div>"


def provider_chips(country, lang):
    return "".join(f'<li><span class="g">{GLYPH[p]}</span>{APP_NAMES[lang][p]}</li>' for p in providers(country))


# ---------------------------------------------------------------- pages
def render_place(p, lang, by_city, geo):
    t = T[lang]
    city = city_name(p["city"], lang)
    country = country_name(p["country"], lang)
    n = display_name(p, lang)
    apps = primary_apps(p["country"], lang)
    path = page_path(lang, p["cslug"], p["slug"])
    alt = {l: page_path(l, p["cslug"], p["slug"]) for l in LANGS}
    url = SITE + path
    variants = display_variants(p)
    fmt = dict(n=n, local=p["local"], city=city, country=country, apps=apps)
    title = t["title"].format(**fmt) if n != p["local"] else t["title"].format(**fmt).replace(f" ({p['local']})", "").replace(f"（{p['local']}）", " ")
    desc = t["desc"].format(**fmt)
    crumbs = [(t["brand"], f"/locallink/{LANG_DIR[lang]}"), (t["places"], page_path(lang)),
              (country, page_path(lang, p["cslug"])), (n, path)]

    alt_names = []
    for v in [p["local"], p["name"]] + variants:
        if v != n and v not in alt_names:
            alt_names.append(v)
    place_ld = {"@type": "Place", "@id": url + "#place", "name": n, "alternateName": alt_names,
                "address": {"@type": "PostalAddress", "addressCountry": COUNTRY_ISO[p["country"]],
                            "addressLocality": city}}
    ll = geo.get(p["key"])
    if ll and p["country"] not in GCJ02_COUNTRIES:
        place_ld["geo"] = {"@type": "GeoCoordinates", "latitude": round(ll[0], 6), "longitude": round(ll[1], 6)}
    jsonld = {"@context": "https://schema.org", "@graph": [
        ORG, WEBSITE,
        {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": title, "description": desc,
         "inLanguage": HTML_LANG[lang], "isPartOf": {"@id": SITE + "/#website"}, "about": {"@id": url + "#place"},
         "breadcrumb": {"@id": url + "#breadcrumb"}, "publisher": {"@id": SITE + "/#organization"}},
        place_ld,
        dict(crumbs_ld(crumbs), **{"@id": url + "#breadcrumb"}),
    ]}

    var_rows = "".join(
        f'<tr><th scope="row">{t["scripts"][sc]}</th><td{lang_attr(SCRIPT_LANG.get(sc))}>{esc(v)}</td></tr>'
        for v, sc in ((v, script_of(v, p["country"])) for v in variants))
    var_sec = (f"""<section class="block"><div class="wrap">
  <div class="kicker"><span>{t['var_h']}</span><span class="rule"></span><span class="num">{len(variants):02d}</span></div>
  <table class="variants"><tbody>{var_rows}</tbody></table>
  <p class="note">{t['var_note']}</p>
</div></section>
""" if variants else "")

    search = [(pr, *search_links(p, pr, url)) for pr in providers(p["country"])]
    route_sec = ""
    if ll:
        rlinks = [(pr, *route_links(p, pr, ll[0], ll[1], url)) for pr in route_providers(p["country"])]
        route_sec = f"""  <h3>{t['route_h']}</h3>
  {map_buttons(rlinks, lang, 'route')}
  <p class="note">{t['route_note']}</p>
"""

    same = by_city[p["city"]]
    i = same.index(p)
    others = [same[(i + k) % len(same)] for k in range(1, len(same))][:6]
    more = ""
    if others:
        items = "".join(
            f'<li><a href="{page_path(lang, o["cslug"], o["slug"])}"><span class="nm">{esc(display_name(o, lang))}</span>'
            f'<span class="lc"{lang_attr(LOCAL_LANG[o["country"]])}>{esc(o["local"])}</span></a></li>' for o in others)
        more = f"""<section class="block"><div class="wrap">
  <div class="kicker"><span>{t['more_h'].format(city=esc(city))}</span><span class="rule"></span></div>
  <ul class="placelist">{items}</ul>
</div></section>
"""

    body = f"""{nav(lang, alt)}<main>
<header class="place-hero"><div class="wrap">
  {crumbs_html(crumbs)}
  <div class="kicker"><span>{esc(country)} · {esc(city)}</span><span class="rule"></span><span class="num">{COUNTRY_ISO[p['country']]}</span></div>
  <h1>{esc(t['h1'].format(**fmt))}</h1>
  <p class="lede">{t['lede'].format(local=esc(p['local']))}</p>
  <div class="local-card">
    <p class="local" id="localName" lang="{LOCAL_LANG[p['country']]}">{esc(p['local'])}</p>
    <p class="local-sub" lang="{LOCAL_LANG[p['country']]}">{esc(CITIES[p['city']]['local'])}</p>
    <div class="actions">
      <button type="button" class="btn" data-copy="{esc(p['local'])}" data-done="{t['copied']}">{t['copy']}</button>
      <button type="button" class="btn primary" data-show>{t['show']}</button>
    </div>
  </div>
</div></header>
{var_sec}<section class="block"><div class="wrap">
  <div class="kicker"><span>{t['maps_h'].format(country=esc(country))}</span><span class="rule"></span></div>
  <p class="why">{t['why'][why_key(p['country'])]}</p>
  {map_buttons(search, lang, 'search')}
  <p class="note">{t['open_note']}</p>
{route_sec}</div></section>
{more}{cta(lang)}</main>
<div class="showcase" id="showcase" hidden role="dialog" aria-modal="true" aria-label="{esc(p['local'])}" lang="{LOCAL_LANG[p['country']]}">
  <p class="big">{esc(p['local'])}</p>
  <p class="big-sub">{esc(CITIES[p['city']]['local'])}</p>
  <p class="hint" lang="{HTML_LANG[lang]}">{t['close']}</p>
</div>
{footer(lang)}"""
    return head(lang, title, desc, path, alt, jsonld) + body


def render_country(country, lang, places, by_city):
    t = T[lang]
    cslug = COUNTRY_SLUG[country]
    cname = country_name(country, lang)
    apps = primary_apps(country, lang)
    path = page_path(lang, cslug)
    alt = {l: page_path(l, cslug) for l in LANGS}
    url = SITE + path
    cps = [p for p in places if p["country"] == country]
    fmt = dict(country=cname, count=len(cps), apps=apps)
    title, desc = t["c_title"].format(**fmt), t["c_desc"].format(**fmt)
    crumbs = [(t["brand"], f"/locallink/{LANG_DIR[lang]}"), (t["places"], page_path(lang)), (cname, path)]
    groups = []
    for case in [c for c in CITIES if CITIES[c] and any(p["city"] == c for p in cps)]:
        items = "".join(
            f'<li><a href="{page_path(lang, cslug, p["slug"])}"><span class="nm">{esc(display_name(p, lang))}</span>'
            f'<span class="lc"{lang_attr(LOCAL_LANG[country])}>{esc(p["local"])}</span></a></li>' for p in by_city[case])
        groups.append(f'<h2 class="city">{esc(city_name(case, lang))} <span>{esc(CITIES[case]["local"])}</span></h2><ul class="placelist">{items}</ul>')
    jsonld = {"@context": "https://schema.org", "@graph": [
        ORG, WEBSITE,
        {"@type": "CollectionPage", "@id": url + "#webpage", "url": url, "name": title, "description": desc,
         "inLanguage": HTML_LANG[lang], "isPartOf": {"@id": SITE + "/#website"},
         "breadcrumb": {"@id": url + "#breadcrumb"}, "publisher": {"@id": SITE + "/#organization"}},
        dict(crumbs_ld(crumbs), **{"@id": url + "#breadcrumb"}),
    ]}
    body = f"""{nav(lang, alt)}<main>
<header class="place-hero"><div class="wrap">
  {crumbs_html(crumbs)}
  <div class="kicker"><span>{FLAG[country]} {esc(cname)}</span><span class="rule"></span><span class="num">{t['n_places'].format(n=len(cps))}</span></div>
  <h1>{esc(t['c_h1'].format(**fmt))}</h1>
  <p class="why">{t['why'][why_key(country)]}</p>
  <ul class="chips">{provider_chips(country, lang)}</ul>
</div></header>
<section class="block"><div class="wrap">
  {''.join(groups)}
</div></section>
{cta(lang, owner=False)}</main>
{footer(lang)}"""
    return head(lang, title, desc, path, alt, jsonld) + body


def render_hub(lang, places):
    t = T[lang]
    path = page_path(lang)
    alt = {l: page_path(l) for l in LANGS}
    url = SITE + path
    fmt = dict(count=len(places))
    title, desc = t["hub_title"].format(**fmt), t["hub_desc"].format(**fmt)
    crumbs = [(t["brand"], f"/locallink/{LANG_DIR[lang]}"), (t["places"], path)]
    cards = []
    for c in COUNTRY_ORDER:
        cps = [p for p in places if p["country"] == c]
        cities = []
        for p in cps:
            name = city_name(p["city"], lang)
            if name not in cities:
                cities.append(name)
        cards.append(
            f'<li class="country"><a href="{page_path(lang, COUNTRY_SLUG[c])}">'
            f'<span class="flag">{FLAG[c]}</span><span class="cn">{esc(country_name(c, lang))}</span>'
            f'<span class="count">{t["n_places"].format(n=len(cps))}</span>'
            f'<span class="cities">{esc(" · ".join(cities))}</span>'
            f'<span class="apps">{esc(primary_apps(c, lang))}</span></a></li>')
    jsonld = {"@context": "https://schema.org", "@graph": [
        ORG, WEBSITE,
        {"@type": "CollectionPage", "@id": url + "#webpage", "url": url, "name": title, "description": desc,
         "inLanguage": HTML_LANG[lang], "isPartOf": {"@id": SITE + "/#website"},
         "breadcrumb": {"@id": url + "#breadcrumb"}, "publisher": {"@id": SITE + "/#organization"}},
        dict(crumbs_ld(crumbs), **{"@id": url + "#breadcrumb"}),
    ]}
    why = "".join(f'<li><strong>{FLAG[c]} {esc(country_name(c, lang))}</strong> {t["why"][why_key(c)]}</li>'
                  for c in ("korea", "china"))
    others = " · ".join(country_name(c, lang) for c in COUNTRY_ORDER if c not in ("korea", "china"))
    why += f'<li><strong>🌏 {esc(others)}</strong> {t["why"]["other"]}</li>'
    body = f"""{nav(lang, alt)}<main>
<header class="place-hero"><div class="wrap">
  {crumbs_html(crumbs)}
  <div class="kicker"><span>LOCAL · LINK</span><span class="rule"></span><span class="num">{t['n_places'].format(n=len(places))}</span></div>
  <h1>{esc(t['hub_h1'])}</h1>
  <p class="lede">{t['hub_lede']}</p>
</div></header>
<section class="block"><div class="wrap">
  <ul class="countries">{''.join(cards)}</ul>
</div></section>
<section class="block"><div class="wrap">
  <ul class="whylist">{why}</ul>
</div></section>
{cta(lang, owner=False)}</main>
{footer(lang)}"""
    return head(lang, title, desc, path, alt, jsonld) + body


# ---------------------------------------------------------------- build
def write_if_changed(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return False
    path.write_text(content, encoding="utf-8")
    return True


def main():
    places = load_places()
    geo = load_geo(places)
    by_city = {}
    for p in places:
        by_city.setdefault(p["city"], []).append(p)
    pages = {}
    for lang in LANGS:
        pages[page_path(lang)] = render_hub(lang, places)
        for c in COUNTRY_ORDER:
            pages[page_path(lang, COUNTRY_SLUG[c])] = render_country(c, lang, places, by_city)
        for p in places:
            pages[page_path(lang, p["cslug"], p["slug"])] = render_place(p, lang, by_city, geo)
    changed = 0
    for path, content in pages.items():
        changed += write_if_changed(SITE_ROOT / path.lstrip("/") / "index.html", content)
    # Remove pages for places that no longer exist (only inside places/ trees).
    wanted = {SITE_ROOT / path.lstrip("/") / "index.html" for path in pages}
    removed = 0
    for lang in LANGS:
        base = SITE_ROOT / "locallink" / LANG_DIR[lang] / "places"
        for f in base.rglob("index.html"):
            if f not in wanted:
                f.unlink()
                removed += 1
                try:
                    f.parent.rmdir()
                except OSError:
                    pass
    with_geo = sum(1 for p in places if p["key"] in geo)
    print(f"places: {len(pages)} pages ({len(LANGS)} langs × ({len(places)} places + {len(COUNTRY_ORDER)} countries + 1 hub)) "
          f"· written {changed} · removed {removed} · with coordinates {with_geo}/{len(places)}")
    import runpy
    runpy.run_path(str(SITE_ROOT / "gen" / "gen_sitemap.py"), run_name="__main__")


if __name__ == "__main__":
    main()
