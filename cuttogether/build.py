#!/usr/bin/env python3
"""Generate index.html for every locale from one template.

Usage: python3 build.py
Output: ./index.html (en), ./ko/index.html, ./ja/index.html, ./zh-hant/index.html
Never edit the generated HTML — change this file and re-run.
"""
import pathlib

ROOT = pathlib.Path(__file__).parent
# Custom domain (www.kkirukstudio.com/cuttogether/) is not mapped yet, so
# canonical/hreflang point at the live Pages URL until it is.
BASE_URL = "https://www.kkirukstudio.com/cuttogether/"
APP_STORE_URL = ""  # filled in once the app is approved

APPLE_SVG = '<svg viewBox="0 0 384 512" aria-hidden="true"><path d="M318.7 268.7c-.2-36.7 16.4-64.4 50-84.8-18.8-26.9-47.2-41.7-84.7-44.6-35.5-2.8-74.3 20.7-88.5 20.7-15 0-49.4-19.7-76.4-19.7C63.3 141.2 4 184.8 4 273.5q0 39.3 14.4 81.2c12.8 36.7 59 126.7 107.2 125.2 25.2-.6 43-17.9 75.8-17.9 31.8 0 48.3 17.9 76.4 17.9 48.6-.7 90.4-82.5 102.6-119.3-65.2-30.7-61.7-90-61.7-91.9zm-56.6-164.2c27.3-32.4 24.8-61.9 24-72.5-24.1 1.4-52 16.4-67.9 34.9-17.5 19.8-27.8 44.3-25.6 71.9 26.1 2 49.9-11.4 69.5-34.3z"/></svg>'

LANG_LABELS = [("", "EN"), ("ko/", "한국어"), ("ja/", "日本語"), ("zh-hant/", "繁體")]

LOCALES = {
    "en": {
        "dir": "", "lang": "en", "font": None, "shots": "en",
        "title": "CutTogether — Cut the people out, keep the trip",
        "desc": "CutTogether finds the people in your photos, cuts them out on your iPhone, and gathers them onto one scrapbook poster. No account, no upload.",
        "og_title": "CutTogether — Photo cut-out poster maker",
        "og_desc": "Back from a trip with 400 photos? Cut the people out and keep them on one page.",
        "kicker": "ON-DEVICE SCRAPBOOK POSTERS",
        "h1": "Back with 400 photos.<br>Keep the <em>people</em>.",
        "lede": "CutTogether finds everyone in the photos you pick, cuts them out as stickers, and lays them onto a single scrapbook poster. The cutting is automatic. The trip stays yours.",
        "badge_small": "Coming soon to the", "badge_big": "App Store",
        "note": "IPHONE &amp; IPAD · NO ACCOUNT · NOTHING LEAVES YOUR PHONE",
        "chips": ["Automatic cut-outs", "Die-cut sticker edges", "Masking tape", "PNG export"],
        "caption": "august 2026",
        "marquee": ["TRIPS", "REUNIONS", "WEDDINGS", "BIRTHDAYS", "GRADUATIONS", "ROAD TRIPS", "FAMILY DINNERS", "FESTIVALS"],
        "how_kicker": "HOW IT WORKS",
        "how_h2": "From camera roll to <em>one page</em>, in three steps.",
        "steps": [
            ["CHOOSE", "Pick up to 20 photos", "Straight from the photo picker. No album to build, no tagging, no sorting."],
            ["CUT", "Everyone gets cut out", "Apple's Vision framework finds each person on your device and lifts them off the background — several people per photo."],
            ["ARRANGE", "The poster builds itself", "Stickers land on the paper one by one. Drag, pinch, rotate or scatter until it feels like yours, then export a PNG."],
        ],
        "shots_kicker": "SCREENS",
        "shots_h2": "A scrapbook page, <em>not a photo editor</em>.",
        "shots_caps": ["EVERYONE, CUT OUT", "EXPORT AS PNG", "YOUR POSTER LIBRARY"],
        "feat_kicker": "DETAILS",
        "feat_h2": "Small app. <em>Deliberate</em> choices.",
        "feats": [
            ["Nothing leaves your iPhone", "Detection and background removal run on device. No upload, no account, no analytics."],
            ["Die-cut sticker edges", "A white, cream, ink or terracotta outline traces each cut-out — or none at all."],
            ["Four papers", "White, cream, ink and kraft, plus a transparent export for putting people anywhere."],
            ["Dated from the photos", "The handwritten caption reads the capture date out of the photos themselves."],
            ["Your poster library", "Every poster you share is kept, ready to re-share or delete."],
            ["Four languages", "English, 한국어, 日本語, 繁體中文 — each with its own display and handwriting type."],
        ],
        "privacy_kicker": "PRIVACY",
        "privacy_h2": "Your photos never leave the device.",
        "privacy_body": "There is no server. No sign-in. No third-party SDK of any kind. Photo analysis, background removal and rendering all happen on your iPhone, and the only photos the app can see are the ones you hand it in the system picker.",
        "final_h2": "Keep the people, not the folder.",
        "final_lede": "Coming to iPhone and iPad.",
        "f_contact": "Contact", "f_privacy": "Privacy", "f_terms": "Terms",
    },
    "ko": {
        "dir": "ko/", "lang": "ko", "font": '"Apple SD Gothic Neo", "Pretendard"', "shots": "ko",
        "title": "CutTogether — 사람만 오려서, 여행을 한 장에",
        "desc": "사진 속 사람을 iPhone 안에서 찾아 오려내고, 한 장의 스크랩북 포스터로 모아줍니다. 계정도, 업로드도 없습니다.",
        "og_title": "CutTogether — 사진 오려 만드는 포스터",
        "og_desc": "여행 다녀와서 사진만 400장? 사람만 오려 한 페이지에 모으세요.",
        "kicker": "온디바이스 스크랩북 포스터",
        "h1": "사진은 400장.<br>남는 건 <em>사람</em>.",
        "lede": "고른 사진에서 인물을 전부 찾아 스티커처럼 오려내고, 한 장의 스크랩북 포스터에 올려줍니다. 오리는 건 자동으로, 여행은 그대로.",
        "badge_small": "곧 만나요", "badge_big": "App Store",
        "note": "iPHONE &amp; iPAD · 계정 없음 · 사진은 기기 밖으로 나가지 않음",
        "chips": ["자동 누끼", "다이컷 스티커 테두리", "마스킹테이프", "PNG 내보내기"],
        "caption": "2026년 8월",
        "marquee": ["여행", "가족모임", "결혼식", "생일", "졸업", "드라이브", "집밥", "축제"],
        "how_kicker": "이렇게 만들어요",
        "how_h2": "카메라 롤에서 <em>한 페이지</em>까지, 세 단계.",
        "steps": [
            ["고르기", "사진 최대 20장", "사진 선택 화면에서 바로. 앨범을 만들 필요도, 태그를 달 필요도 없습니다."],
            ["오리기", "인물이 전부 오려져요", "Apple Vision 프레임워크가 기기 안에서 사람을 찾아 배경에서 떼어냅니다. 한 장에 여러 명이어도 각각."],
            ["배치", "포스터가 알아서 완성", "스티커가 한 장씩 종이에 내려앉습니다. 옮기고 키우고 돌리고 흩뿌려 마음에 들면 PNG로 저장."],
        ],
        "shots_kicker": "화면",
        "shots_h2": "사진 편집기가 아니라, <em>스크랩북 한 장</em>.",
        "shots_caps": ["모두, 오려서", "PNG로 내보내기", "내 포스터 보관함"],
        "feat_kicker": "디테일",
        "feat_h2": "작은 앱. <em>분명한</em> 선택.",
        "feats": [
            ["사진은 기기 밖으로 안 나갑니다", "인물 검출과 배경 제거 모두 기기 안에서. 업로드도, 계정도, 분석 도구도 없습니다."],
            ["다이컷 스티커 테두리", "흰색·크림·잉크·테라코타 중에서 누끼 외곽선을 고르거나, 아예 없이."],
            ["종이 4종", "화이트·크림·잉크·크라프트, 그리고 어디든 붙일 수 있는 투명 배경 내보내기."],
            ["날짜는 사진에서", "손글씨 캡션의 날짜를 사진의 촬영 정보에서 바로 읽어옵니다."],
            ["포스터 보관함", "공유한 포스터는 전부 보관돼요. 다시 공유하거나 지우면 됩니다."],
            ["4개 언어", "English, 한국어, 日本語, 繁體中文 — 언어마다 어울리는 제목·손글씨 폰트까지."],
        ],
        "privacy_kicker": "프라이버시",
        "privacy_h2": "사진은 이 기기를 떠나지 않습니다.",
        "privacy_body": "서버가 없습니다. 로그인도, 서드파티 SDK도 없습니다. 사진 분석·배경 제거·렌더링이 전부 iPhone 안에서 이루어지고, 앱이 볼 수 있는 사진은 시스템 선택 화면에서 직접 건네준 것뿐입니다.",
        "final_h2": "폴더 말고, 사람을 남기세요.",
        "final_lede": "iPhone과 iPad에 곧 출시됩니다.",
        "f_contact": "문의", "f_privacy": "개인정보", "f_terms": "이용약관",
    },
    "ja": {
        "dir": "ja/", "lang": "ja", "font": '"Hiragino Sans", "Yu Gothic"', "shots": "ja",
        "title": "CutTogether — 人だけ切り抜いて、旅を1枚に",
        "desc": "写真の中の人を iPhone の中で見つけて切り抜き、1枚のスクラップブックポスターにまとめます。アカウントもアップロードも不要。",
        "og_title": "CutTogether — 切り抜きポスターメーカー",
        "og_desc": "旅から帰って写真が400枚？ 人だけ切り抜いて、1ページにまとめましょう。",
        "kicker": "オンデバイスのスクラップブック",
        "h1": "写真は400枚。<br>残るのは<em>人</em>。",
        "lede": "選んだ写真から全員を見つけてステッカーのように切り抜き、1枚のスクラップブックポスターに並べます。切り抜きは自動、旅の記憶はそのまま。",
        "badge_small": "近日公開", "badge_big": "App Store",
        "note": "iPHONE ＆ iPAD · アカウント不要 · 写真は端末の外に出ません",
        "chips": ["自動切り抜き", "ダイカット風の枠", "マスキングテープ", "PNG 書き出し"],
        "caption": "2026年8月",
        "marquee": ["旅行", "同窓会", "結婚式", "誕生日", "卒業", "ドライブ", "家族の食卓", "お祭り"],
        "how_kicker": "使い方",
        "how_h2": "カメラロールから<em>1ページ</em>まで、3ステップ。",
        "steps": [
            ["選ぶ", "写真は最大20枚", "写真ピッカーからそのまま。アルバムを作る必要も、タグ付けも要りません。"],
            ["切り抜く", "全員が切り抜かれます", "Apple の Vision フレームワークが端末内で人物を見つけ、背景から持ち上げます。1枚に複数人いてもそれぞれ。"],
            ["並べる", "ポスターは自動で仕上がる", "ステッカーが1枚ずつ紙に降りてきます。動かす・拡大する・回す・散らすで整えて、PNG で書き出し。"],
        ],
        "shots_kicker": "画面",
        "shots_h2": "写真編集アプリではなく、<em>スクラップブックの1ページ</em>。",
        "shots_caps": ["全員、切り抜いて", "PNG で書き出し", "マイポスター"],
        "feat_kicker": "ディテール",
        "feat_h2": "小さなアプリ。<em>明確な</em>選択。",
        "feats": [
            ["写真は端末から出ません", "人物検出も背景除去も端末内で完結。アップロードもアカウントも解析ツールもありません。"],
            ["ダイカット風のふち", "ホワイト・クリーム・インク・テラコッタから枠を選択。なしにもできます。"],
            ["4種類の紙", "ホワイト・クリーム・インク・クラフト、そしてどこにでも貼れる透明背景の書き出し。"],
            ["日付は写真から", "手書き風キャプションの日付を、写真の撮影情報から自動で読み取ります。"],
            ["ポスターライブラリ", "シェアしたポスターは保存され、再シェアも削除も自由です。"],
            ["4言語対応", "English、한국어、日本語、繁體中文 — 言語ごとに見出しと手書きの書体まで。"],
        ],
        "privacy_kicker": "プライバシー",
        "privacy_h2": "写真はこの端末から出ません。",
        "privacy_body": "サーバーはありません。ログインも、サードパーティ SDK もありません。写真の解析・背景除去・描画はすべて iPhone の中で行われ、アプリが見られるのはシステムのピッカーで渡した写真だけです。",
        "final_h2": "フォルダではなく、人を残す。",
        "final_lede": "iPhone と iPad に近日公開。",
        "f_contact": "お問い合わせ", "f_privacy": "プライバシー", "f_terms": "利用規約",
    },
    "zh-hant": {
        "dir": "zh-hant/", "lang": "zh-Hant", "font": '"PingFang TC", "Noto Sans TC"', "shots": "zh-Hant",
        "title": "CutTogether — 把人剪下來，把旅行留成一頁",
        "desc": "在 iPhone 上找出照片裡的人、剪下來，集合成一張剪貼簿海報。不需帳號，不會上傳。",
        "og_title": "CutTogether — 照片剪貼海報",
        "og_desc": "旅行回來有 400 張照片？把人剪下來，留成一頁。",
        "kicker": "裝置端剪貼簿海報",
        "h1": "照片 400 張。<br>留下的是<em>人</em>。",
        "lede": "從你挑的照片中找出每個人，像貼紙一樣剪下來，排進同一張剪貼簿海報。剪裁自動完成，旅行還是你的。",
        "badge_small": "即將上架", "badge_big": "App Store",
        "note": "iPHONE ＆ iPAD · 免帳號 · 照片不會離開手機",
        "chips": ["自動去背", "模切貼紙外框", "紙膠帶", "PNG 匯出"],
        "caption": "2026年8月",
        "marquee": ["旅行", "聚會", "婚禮", "生日", "畢業", "公路旅行", "家庭聚餐", "祭典"],
        "how_kicker": "使用方式",
        "how_h2": "從相機膠卷到<em>一頁</em>，只要三步。",
        "steps": [
            ["挑選", "最多 20 張照片", "直接從照片選擇器挑。不用建相簿，也不用加標籤。"],
            ["剪裁", "每個人都被剪下來", "Apple Vision 框架在裝置上找出人物，把他們從背景抬起來。一張照片有多人也各自處理。"],
            ["排版", "海報自己完成", "貼紙一張張落在紙上。移動、縮放、旋轉或散布，滿意後匯出 PNG。"],
        ],
        "shots_kicker": "畫面",
        "shots_h2": "這不是修圖 App，而是<em>一頁剪貼簿</em>。",
        "shots_caps": ["每個人，都剪下來", "匯出成 PNG", "我的海報收藏"],
        "feat_kicker": "細節",
        "feat_h2": "小巧的 App。<em>刻意的</em>選擇。",
        "feats": [
            ["照片不會離開你的 iPhone", "人物偵測與去背都在裝置上完成。不上傳、不需帳號、沒有分析工具。"],
            ["模切貼紙外框", "白色、奶油色、墨色或陶土色的外框，也可以完全不加。"],
            ["四種紙張", "白色、奶油色、墨色與牛皮紙，還有可以貼到任何地方的透明背景匯出。"],
            ["日期來自照片", "手寫風說明文字的日期，直接讀自照片的拍攝資訊。"],
            ["海報收藏庫", "分享過的海報都會保存，隨時可以再分享或刪除。"],
            ["四種語言", "English、한국어、日本語、繁體中文 — 每種語言都有合適的標題與手寫字體。"],
        ],
        "privacy_kicker": "隱私",
        "privacy_h2": "照片不會離開這台裝置。",
        "privacy_body": "沒有伺服器，不需登入，也沒有任何第三方 SDK。照片分析、去背與繪製全部在 iPhone 上完成，而 App 能看到的只有你在系統選擇器裡交給它的照片。",
        "final_h2": "留下人，而不是資料夾。",
        "final_lede": "即將在 iPhone 與 iPad 上推出。",
        "f_contact": "聯絡我們", "f_privacy": "隱私權", "f_terms": "服務條款",
    },
}


def badge(loc):
    disabled = "" if APP_STORE_URL else ' aria-disabled="true"'
    href = APP_STORE_URL or "#"
    return (
        f'<a class="badge" href="{href}"{disabled}>{APPLE_SVG}'
        f'<span class="txt"><span>{loc["badge_small"]}</span><b>{loc["badge_big"]}</b></span></a>'
    )


def render(code, loc):
    depth = "" if not loc["dir"] else "../"
    alternates = "\n  ".join(
        f'<link rel="alternate" hreflang="{other["lang"]}" href="{BASE_URL}{other["dir"]}">'
        for other in LOCALES.values()
    )
    langs = "\n      ".join(
        f'<a href="{BASE_URL}{path}"{" aria-current=\"page\"" if path == loc["dir"] else ""}>{label}</a>'
        for path, label in LANG_LABELS
    )
    cutouts = "\n        ".join(
        f'<figure style="--tilt: {tilt}deg"><img src="{depth}assets/cut-{i}.png" alt="" loading="lazy"></figure>'
        for i, tilt in zip(range(1, 5), (-3, 2.5, -1.5, 3))
    )
    steps = "\n        ".join(
        f'<div class="step"><div class="n">{n}</div><h3>{h}</h3><p>{p}</p></div>'
        for n, h, p in loc["steps"]
    )
    shots = "\n        ".join(
        f'<figure><img src="{depth}assets/shot-{loc["shots"]}-{name}.png" alt="{cap}" loading="lazy">'
        f'<figcaption>{cap}</figcaption></figure>'
        for name, cap in zip(("editor", "export", "home"), loc["shots_caps"])
    )
    feats = "\n        ".join(
        f'<div class="feat"><h3>{h}</h3><p>{p}</p></div>' for h, p in loc["feats"]
    )
    chips = "\n          ".join(f'<span class="chip">{c}</span>' for c in loc["chips"])
    marquee_items = "".join(f"<span>{m}</span>" for m in loc["marquee"] * 2)
    font_line = f"\n    :root {{ --body-font: {loc['font']}, -apple-system, BlinkMacSystemFont, sans-serif; }}" if loc["font"] else ""

    return f"""<!DOCTYPE html>
<html lang="{loc['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{loc['title']}</title>
<meta name="description" content="{loc['desc']}">
<link rel="canonical" href="{BASE_URL}{loc['dir']}">
  {alternates}
<link rel="alternate" hreflang="x-default" href="{BASE_URL}">
<meta property="og:type" content="website">
<meta property="og:title" content="{loc['og_title']}">
<meta property="og:description" content="{loc['og_desc']}">
<meta property="og:image" content="{BASE_URL}assets/icon-512.png">
<meta property="og:url" content="{BASE_URL}{loc['dir']}">
<meta name="twitter:card" content="summary_large_image">
<link rel="apple-touch-icon" href="{depth}assets/icon-180.png">
<link rel="icon" href="{depth}assets/icon-180.png">
<link rel="stylesheet" href="{depth}assets/style.css">
<style>{font_line}
</style>
</head>
<body>
<header class="wrap top">
  <img src="{depth}assets/icon-180.png" alt="" width="34" height="34" style="border-radius:9px">
  <div class="mark">CutTogether</div>
  <nav class="langs" aria-label="Language">
      {langs}
  </nav>
</header>

<main>
  <section class="wrap hero">
    <div>
      <div class="kicker">{loc['kicker']}</div>
      <h1>{loc['h1']}</h1>
      <p class="lede">{loc['lede']}</p>
      {badge(loc)}
      <div class="note">{loc['note']}</div>
      <div class="chips">
          {chips}
      </div>
    </div>
    <div class="demo">
      <div class="poster">
        <div class="tape"></div>
        {cutouts}
        <div class="caption">{loc['caption']}</div>
      </div>
    </div>
  </section>

  <div class="marquee" aria-hidden="true"><div>{marquee_items}</div></div>

  <section class="wrap">
    <div class="kicker">{loc['how_kicker']}</div>
    <h2>{loc['how_h2']}</h2>
    <div class="steps">
        {steps}
    </div>
  </section>

  <section class="wrap">
    <div class="kicker">{loc['shots_kicker']}</div>
    <h2>{loc['shots_h2']}</h2>
    <div class="shots">
        {shots}
    </div>
  </section>

  <section class="wrap">
    <div class="privacy">
      <div class="kicker">{loc['privacy_kicker']}</div>
      <h2>{loc['privacy_h2']}</h2>
      <p class="sec-lede" style="margin-bottom:0">{loc['privacy_body']}</p>
    </div>
  </section>

  <section class="wrap">
    <div class="kicker">{loc['feat_kicker']}</div>
    <h2>{loc['feat_h2']}</h2>
    <div class="feats">
        {feats}
    </div>
  </section>

  <section class="wrap final">
    <h2>{loc['final_h2']}</h2>
    <p>{loc['final_lede']}</p>
    {badge(loc)}
  </section>
</main>

<footer>
  <div class="wrap">
    <a href="mailto:kkirukstudio.help@gmail.com">{loc['f_contact']}</a>
    <a href="https://www.kkirukstudio.com/legal/privacy/">{loc['f_privacy']}</a>
    <a href="https://www.kkirukstudio.com/legal/terms/">{loc['f_terms']}</a>
    <div class="copy">© 2026 kkiruk studio</div>
  </div>
</footer>
</body>
</html>
"""


def main():
    for code, loc in LOCALES.items():
        out = ROOT / loc["dir"] / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render(code, loc), encoding="utf-8")
        print("wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
