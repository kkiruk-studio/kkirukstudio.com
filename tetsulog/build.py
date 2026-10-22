#!/usr/bin/env python3
"""Generate index.html for every locale from one template.

Usage: python3 build.py
Output: ./index.html (ja, root/default), ./ko/index.html, ./en/index.html
"""
import pathlib
from html import escape as html_escape

ROOT = pathlib.Path(__file__).parent
BASE_URL = "https://www.kkirukstudio.com/tetsulog/"

# While empty, the CTA renders as a disabled "coming soon" pill instead of a
# real store badge. Filled 2026-08-10 — the app had been live for weeks while
# this landing still said 近日公開 (same trap as RunNote's badge_soon).
APP_STORE_URL = "https://apps.apple.com/app/id6787012765"

LANG_LABELS = [("", "日本語"), ("ko/", "한국어"), ("en/", "EN"), ("zh/", "繁體中文"), ("zh-hans/", "简体中文")]

# Shared marquee content across all locales: real Japanese line names plus the
# three otaku-culture words that anchor the app's concept, regardless of UI
# language (the app's own screens stay Japanese in every locale — see spec).
MARQUEE_ITEMS = [
    ("山手線", False), ("大阪環状線", False), ("銀座線", False),
    ("ゆいレール", False), ("函館市電", False), ("東海道新幹線", False),
    ("完乗", True), ("駅スタンプ", True), ("乗りつぶし", True),
]

# 山手線30駅を実際の経緯度からWebメルカトル図法で投影（z=14, タイル原点 x0=14549 y0=6448）。
# 背景地図（assets/yamanote-map.png, 1280x2048px）と1px単位で一致するviewBox。
# 分岐路線（中央線・京浜東北線・総武線）は同じ座標系上に実在駅を起点として延伸。
# viewBox/座標はデザイン確定案（drafts/railmap.html）と完全に一致させ、変更しないこと。
OSM_CREDIT = "© OpenStreetMap contributors"
RAILMAP_SVG = """<svg viewBox="0 0 1280 2048" aria-hidden="true">
  <path class="rail-casing" d="M1012.7,937.2 966.1,1027.5 910.2,1146.6 898.6,1308.6 785.5,1446.3 702.8,1589.6 681.9,1692.8 561.9,1819.0 502.4,1725.8 412.7,1615.4 348.6,1431.9 249.6,1269.9 262.4,1095.0 255.4,908.5 235.6,816.7 231.0,653.2 275.2,486.7 303.2,361.9 358.0,244.2 563.0,212.6 686.5,191.1 777.4,143.7 940.5,120.8 1009.2,205.4 1057.0,268.6 1147.9,364.7 1130.4,465.2 1099.0,559.9 1090.8,690.5 1055.8,786.6 Z"/>
  <path class="rail-base" d="M1012.7,937.2 966.1,1027.5 910.2,1146.6 898.6,1308.6 785.5,1446.3 702.8,1589.6 681.9,1692.8 561.9,1819.0 502.4,1725.8 412.7,1615.4 348.6,1431.9 249.6,1269.9 262.4,1095.0 255.4,908.5 235.6,816.7 231.0,653.2 275.2,486.7 303.2,361.9 358.0,244.2 563.0,212.6 686.5,191.1 777.4,143.7 940.5,120.8 1009.2,205.4 1057.0,268.6 1147.9,364.7 1130.4,465.2 1099.0,559.9 1090.8,690.5 1055.8,786.6 Z"/>
  <path class="rail-color c-loop" pathLength="100" d="M1012.7,937.2 966.1,1027.5 910.2,1146.6 898.6,1308.6 785.5,1446.3 702.8,1589.6 681.9,1692.8 561.9,1819.0 502.4,1725.8 412.7,1615.4 348.6,1431.9 249.6,1269.9 262.4,1095.0 255.4,908.5 235.6,816.7 231.0,653.2 275.2,486.7 303.2,361.9 358.0,244.2 563.0,212.6 686.5,191.1 777.4,143.7 940.5,120.8 1009.2,205.4 1057.0,268.6 1147.9,364.7 1130.4,465.2 1099.0,559.9 1090.8,690.5 1055.8,786.6 Z"/>

  <path class="rail-branch-casing" d="M235.6,816.7 150,798 70,782 0,768"/>
  <path class="rail-branch-base" d="M235.6,816.7 150,798 70,782 0,768"/>
  <path class="rail-color c-chuo" pathLength="100" d="M235.6,816.7 150,798 70,782 0,768"/>

  <path class="rail-branch-casing" d="M1130.4,465.2 1155,320 1185,160 1210,20"/>
  <path class="rail-branch-base" d="M1130.4,465.2 1155,320 1185,160 1210,20"/>
  <path class="rail-color c-keihin" pathLength="100" d="M1130.4,465.2 1155,320 1185,160 1210,20"/>
  <path class="rail-branch-casing" d="M681.9,1692.8 600,1830 520,1950 430,2048"/>
  <path class="rail-branch-base" d="M681.9,1692.8 600,1830 520,1950 430,2048"/>
  <path class="rail-color c-keihin" pathLength="100" d="M681.9,1692.8 600,1830 520,1950 430,2048"/>

  <path class="rail-branch-casing" d="M1090.8,690.5 1180,705 1250,725 1280,735"/>
  <path class="rail-branch-base" d="M1090.8,690.5 1180,705 1250,725 1280,735"/>
  <path class="rail-color c-sobu" pathLength="100" d="M1090.8,690.5 1180,705 1250,725 1280,735"/>

  <circle class="dot major loop" cx="1012.7" cy="937.2" r="16"/>
  <circle class="dot loop" cx="966.1" cy="1027.5" r="11"/>
  <circle class="dot loop" cx="910.2" cy="1146.6" r="11"/>
  <circle class="dot loop" cx="898.6" cy="1308.6" r="11"/>
  <circle class="dot loop" cx="785.5" cy="1446.3" r="11"/>
  <circle class="dot loop" cx="702.8" cy="1589.6" r="11"/>
  <circle class="dot major loop" cx="681.9" cy="1692.8" r="16"/>
  <circle class="dot loop" cx="561.9" cy="1819.0" r="11"/>
  <circle class="dot loop" cx="502.4" cy="1725.8" r="11"/>
  <circle class="dot loop" cx="412.7" cy="1615.4" r="11"/>
  <circle class="dot loop" cx="348.6" cy="1431.9" r="11"/>
  <circle class="dot major loop" cx="249.6" cy="1269.9" r="16"/>
  <circle class="dot loop" cx="262.4" cy="1095.0" r="11"/>
  <circle class="dot loop" cx="255.4" cy="908.5" r="11"/>
  <circle class="dot major loop" cx="235.6" cy="816.7" r="16"/>
  <circle class="dot loop" cx="231.0" cy="653.2" r="11"/>
  <circle class="dot loop" cx="275.2" cy="486.7" r="11"/>
  <circle class="dot loop" cx="303.2" cy="361.9" r="11"/>
  <circle class="dot major loop" cx="358.0" cy="244.2" r="16"/>
  <circle class="dot loop" cx="563.0" cy="212.6" r="11"/>
  <circle class="dot loop" cx="686.5" cy="191.1" r="11"/>
  <circle class="dot loop" cx="777.4" cy="143.7" r="11"/>
  <circle class="dot loop" cx="940.5" cy="120.8" r="11"/>
  <circle class="dot loop" cx="1009.2" cy="205.4" r="11"/>
  <circle class="dot loop" cx="1057.0" cy="268.6" r="11"/>
  <circle class="dot loop" cx="1147.9" cy="364.7" r="11"/>
  <circle class="dot major loop" cx="1130.4" cy="465.2" r="16"/>
  <circle class="dot loop" cx="1099.0" cy="559.9" r="11"/>
  <circle class="dot loop" cx="1090.8" cy="690.5" r="11"/>
  <circle class="dot loop" cx="1055.8" cy="786.6" r="11"/>

  <text class="eki-label" x="1032" y="930" text-anchor="start" font-size="46">東京</text>
  <text class="eki-label" x="212" y="810" text-anchor="end" font-size="46">新宿</text>
  <text class="eki-label" x="228" y="1290" text-anchor="end" font-size="46">渋谷</text>
  <text class="eki-label" x="338" y="230" text-anchor="end" font-size="46">池袋</text>
  <text class="eki-label" x="1150" y="450" text-anchor="start" font-size="46">上野</text>
  <text class="eki-label" x="681.9" y="1740" text-anchor="middle" font-size="46">品川</text>
</svg>"""

# よくある質問(アプリ内 FAQ と同文。訳は Localizable.xcstrings の値。8 問目はサイト用に新規)
FAQ = {'ja': {'title': 'よくある質問',
        'items': [['乗った区間をまとめて記録するには？', '路線タブで路線を開き、「区間入力」で出発駅と到着駅を選ぶと、間の駅もまとめて訪問済みになります。地図の駅をタップして駅カードの「ここから区間を記録」を押しても同じ画面が開き、その駅が出発駅として入ります。'],
                  ['複数の路線が乗り入れる駅で、記録する路線を選ぶには？', '地図の駅カードで「ここから区間を記録」を押すと、その駅に乗り入れる路線の一覧が出るので、記録したい路線を選んでください。区間入力の画面に入ったあとは路線を変えられないため、別の路線にしたいときは一度閉じて選び直します。'],
                  ['乗っていない区間まで塗られてしまう', '地図は記録した駅と駅の間を乗車済みと推測します。A→BとC→Dだけ乗ったときにB→Cを塗りたくない場合は、設定の「区間を推測しない」をオンにしてください。'],
                  ['湘南新宿ラインや上野東京ラインが見つからない', '鉄ログは乗りつぶしの慣例に合わせて、正式な線路名称(東海道線・山手線など)を単位に記録します。運行系統の名前では収録していないので、走っている線路ごとに記録してください。例えば湘南新宿ラインの大崎〜西大井は「大崎支線」として記録します。'],
                  ['記録は別の端末でも見られる？', 'iCloudにサインインしていれば自動で同期されます。状態は設定の「iCloud 同期」で確認できます。'],
                  ['機種変更に備えるには？', '設定の「バックアップ」で記録をファイルに書き出し、新しい端末で「バックアップ復元」から読み込みます。「エクスポート」でCSVとしても取り出せます。'],
                  ['無料版とProの違いは？', '記録・地図・区間入力・iCloud同期は無料で全て使えます。Proでは、お気に入り無制限、会社別の統計と活動カレンダー、47都道府県ヒートマップ、共有カードのウォーターマーク非表示、PDF御朱印帳、前面展望の逆方向・区間指定が使えます。'],
                  ['山手線が品川〜田端までしかない', '鉄ログは乗りつぶしの慣例に合わせて、正式な線路名称を単位に記録します。山手線の正式な区間は品川〜新宿〜田端で、環状運転の東側(田端〜東京〜品川)は東北線・東海道線の一部です。環状線を一周した場合は、山手線・東北線(田端〜東京)・東海道線(東京〜品川)の3路線で記録してください。']]},
 'ko': {'title': '자주 묻는 질문',
        'items': [['탄 구간을 한꺼번에 기록하려면?', '노선 탭에서 노선을 열고 ‘구간 입력’에서 출발역과 도착역을 고르면 사이의 역도 한꺼번에 ‘방문 완료’가 돼요. 지도에서 역을 탭하고 역 카드의 ‘여기서 구간 기록’을 눌러도 같은 화면이 열리며, 그 역이 출발역으로 들어가요.'],
                  ['여러 노선이 들어오는 역에서 기록할 노선을 고르려면?', '지도의 역 카드에서 ‘여기서 구간 기록’을 누르면 그 역에 들어오는 노선 목록이 나와요. 기록할 노선을 고르세요. 구간 입력 화면에 들어간 뒤에는 노선을 바꿀 수 없으니, 다른 노선으로 바꾸려면 한 번 닫고 다시 선택하세요.'],
                  ['타지 않은 구간까지 칠해져요', '지도는 기록한 역과 역 사이를 탄 것으로 추측해요. A→B와 C→D만 탔는데 B→C는 칠해지지 않게 하려면 설정에서 ‘구간을 추측하지 않음’을 켜세요.'],
                  ['쇼난신주쿠 라인이나 우에노도쿄 라인을 찾을 수 없어요',
                   '철로그는 완승(노선 전체 탑승) 관례에 맞춰 정식 선로 명칭(도카이도선·야마노테선 등)을 단위로 기록해요. 운행 계통 이름으로는 수록하지 않았으니, 실제로 달리는 선로별로 기록해 주세요. 예를 들어 쇼난신주쿠 라인의 오사키~니시오이는 ‘오사키 지선’으로 기록해요.'],
                  ['기록을 다른 기기에서도 볼 수 있나요?', 'iCloud에 로그인되어 있으면 자동으로 동기화돼요. 상태는 설정의 ‘iCloud 동기화’에서 확인할 수 있어요.'],
                  ['기기를 바꿀 때를 대비하려면?', '설정의 ‘백업’에서 기록을 파일로 내보내고, 새 기기에서 ‘백업 복원’으로 불러오세요. ‘내보내기’로 CSV로도 꺼낼 수 있어요.'],
                  ['무료 버전과 Pro의 차이는?', '기록·지도·구간 입력·iCloud 동기화는 모두 무료로 쓸 수 있어요. Pro에서는 즐겨찾기 무제한, 회사별 통계와 활동 캘린더, 47도도부현 히트맵, 공유 카드 워터마크 제거, PDF 스탬프 수첩, 전면 전망의 역방향·구간 지정을 쓸 수 있어요.'],
                  ['야마노테선이 시나가와~타바타까지밖에 없어요',
                   '테츠로그는 노선 완주 기록의 관례에 맞춰 정식 선로 명칭을 단위로 기록합니다. 야마노테선의 정식 구간은 시나가와~신주쿠~타바타이고, 순환 운행의 동쪽 구간(타바타~도쿄~시나가와)은 도호쿠선·도카이도선의 일부입니다. 순환선을 한 바퀴 돌았다면 야마노테선·도호쿠선(타바타~도쿄)·도카이도선(도쿄~시나가와) 3개 노선으로 '
                   '기록해 주세요.']]},
 'en': {'title': 'FAQ',
        'items': [['How do I log a whole stretch I rode at once?',
                   'Open a line in the Lines tab, then choose a departure and arrival station under “Segment Entry” and every station in between is marked as Visited at once. Tapping a station on '
                   'the map and pressing “Log a segment from here” on its card opens the same screen, with that station filled in as the departure.'],
                  ['How do I choose which line to log at a station served by several lines?',
                   'Press “Log a segment from here” on the station card on the map and a list of the lines serving that station appears; pick the one you want to log. The line can’t be changed once '
                   'you are on the Segment Entry screen, so to switch lines, close it and choose again.'],
                  ['Stretches I didn’t ride get colored in',
                   'The map assumes you rode between the stations you have logged. If you only rode A→B and C→D and don’t want B→C colored in, turn on “Don’t infer segments” in Settings.'],
                  ['I can’t find the Shonan-Shinjuku Line or the Ueno-Tokyo Line',
                   'Following the convention of “riding every line”, Tetsulog records by official track name (Tokaido Line, Yamanote Line, etc.). Service names are not included, so please log each '
                   'track the train actually runs on. For example, the Osaki–Nishi-Oi section of the Shonan-Shinjuku Line is logged as the “Osaki Branch Line”.'],
                  ['Can I see my records on another device?', 'If you’re signed in to iCloud, your records sync automatically. You can check the status under “iCloud Sync” in Settings.'],
                  ['How do I prepare for switching to a new device?',
                   'Export your records to a file with “Backup” in Settings, then load it on the new device with “Restore Backup”. You can also take them out as CSV with “Export”.'],
                  ['What’s the difference between Free and Pro?',
                   'Logging, the map, Segment Entry and iCloud sync are all free. Pro adds unlimited favorites, per-operator stats and the activity calendar, the 47-prefecture heatmap, share cards '
                   'without the watermark, the PDF stamp book, and reverse direction and stretch selection in Cab View.'],
                  ['The Yamanote Line only runs from Shinagawa to Tabata',
                   'In keeping with the convention for riding every line, Tetsulog records by official track name. The Yamanote Line officially covers Shinagawa–Shinjuku–Tabata; the eastern side of '
                   'the loop (Tabata–Tokyo–Shinagawa) belongs to the Tohoku Line and the Tokaido Line. If you rode the full loop, record it on three lines: the Yamanote Line, the Tohoku Line '
                   '(Tabata–Tokyo) and the Tokaido Line (Tokyo–Shinagawa).']]},
 'zh': {'title': '常見問題',
        'items': [['如何一次記錄搭乘過的整段區間？', '在「路線」分頁開啟路線，透過「區間輸入」選擇出發站與抵達站，中間的車站也會一併標為「已造訪」。在地圖上點按車站，再按車站卡片上的「從這裡記錄區間」也會開啟同一畫面，並自動填入該站作為出發站。'],
                  ['在多條路線經過的車站，如何選擇要記錄的路線？', '在地圖的車站卡片上按「從這裡記錄區間」，會顯示經過該站的路線列表，請選擇要記錄的路線。進入區間輸入畫面後無法更換路線，想換路線時請先關閉再重新選擇。'],
                  ['沒搭過的區間也被塗上了顏色', '地圖會推測您記錄的車站之間都已搭乘。如果只搭了 A→B 和 C→D，不想讓 B→C 被塗色，請在設定中開啟「不推測區間」。'],
                  ['找不到湘南新宿線或上野東京線', '鉄ログ依照「搭乘全線」的慣例，以正式的路線名稱（東海道線、山手線等）為單位進行記錄。運行系統的名稱並未收錄，請依列車實際行駛的路線分別記錄。例如湘南新宿線的大崎～西大井區間，請記錄為「大崎支線」。'],
                  ['紀錄可以在其他裝置上查看嗎？', '只要登入了 iCloud，就會自動同步。可在設定的「iCloud 同步」中查看狀態。'],
                  ['換新裝置前該如何準備？', '在設定的「備份」中將紀錄匯出為檔案，然後在新裝置上透過「還原備份」讀取。也可以透過「匯出」取出為 CSV。'],
                  ['免費版與 Pro 有什麼差別？', '記錄、地圖、區間輸入和 iCloud 同步全部免費使用。Pro 額外提供收藏無上限、各營運公司統計與活動日曆、47 都道府縣熱力圖、隱藏分享卡片浮水印、PDF 集章冊，以及前面展望的反向與區間指定。'],
                  ['山手線只有品川～田端', '鐵ログ依照「乘遍全線」的慣例，以正式的線路名稱為單位記錄。山手線的正式區間是品川～新宿～田端，環狀運行的東側（田端～東京～品川）屬於東北線與東海道線的一部分。若乘坐了整圈環狀線，請以山手線、東北線（田端～東京）、東海道線（東京～品川）三條路線記錄。']]},
 'zh-hans': {'title': '常见问题',
             'items': [['如何一次记录乘坐过的整段区间？', '在“路线”标签页打开路线，通过“区间输入”选择出发站和到达站，中间的车站也会一并标为“已造访”。在地图上点按车站，再按车站卡片上的“从这里记录区间”也会打开同一界面，并自动填入该站作为出发站。'],
                       ['在多条线路经过的车站，如何选择要记录的线路？', '在地图的车站卡片上按“从这里记录区间”，会显示经过该站的线路列表，请选择要记录的线路。进入区间输入界面后无法更换线路，想换线路时请先关闭再重新选择。'],
                       ['没乘过的区间也被涂上了颜色', '地图会推测您记录的车站之间都已乘坐。如果只乘了 A→B 和 C→D，不想让 B→C 被涂色，请在设置中打开“不推测区间”。'],
                       ['找不到湘南新宿线或上野东京线', '鉄ログ依照“乘遍全线”的惯例，以正式的线路名称（东海道线、山手线等）为单位进行记录。运行系统的名称并未收录，请按列车实际行驶的线路分别记录。例如湘南新宿线的大崎～西大井区间，请记录为“大崎支线”。'],
                       ['记录可以在其他设备上查看吗？', '只要登录了 iCloud，就会自动同步。可在设置的“iCloud 同步”中查看状态。'],
                       ['换新设备前该如何准备？', '在设置的“备份”中将记录导出为文件，然后在新设备上通过“还原备份”读取。也可以通过“导出”取出为 CSV。'],
                       ['免费版与 Pro 有什么区别？', '记录、地图、区间输入和 iCloud 同步全部免费使用。Pro 额外提供收藏无上限、各运营公司统计与活动日历、47 都道府县热力图、隐藏分享卡片水印、PDF 集章册，以及前面展望的反向与区间指定。'],
                       ['山手线只有品川～田端', '鉄ログ依照“乘遍全线”的惯例，以正式的线路名称为单位记录。山手线的正式区间是品川～新宿～田端，环状运行的东侧（田端～东京～品川）属于东北线和东海道线的一部分。若乘坐了整圈环状线，请以山手线、东北线（田端～东京）、东海道线（东京～品川）三条线路记录。']]}}


LOCALES = {
    "ja": {
        "dir": "", "lang": "ja", "font": None,
        "title": "鉄ログ — 乗った駅が、そのまま地図になる",
        "desc": "駅をタップするだけで乗車を記録。乗った路線の色が地図に広がり、完乗すると朱色のスタンプが押されます。全国163社・571路線・9,706駅対応の乗りつぶしアプリ。",
        "og_title": "鉄ログ — 乗りつぶし記録アプリ",
        "og_desc": "乗った駅が、そのまま地図になる。全国163社・571路線・9,706駅。",
        "brand": "鉄ログ",
        "kicker_word": "STAMP BOOK",
        "kicker_num": "全国 9,706 駅",
        "h1": "乗った駅が、<br>そのまま<em>地図になる</em>。",
        "sub": "地図の駅をタップするだけで乗車を記録。乗った路線の色がそのまま地図に広がります。全国163社・571路線・9,706駅の乗りつぶしを、鉄ログでスタンプ帳のように記録しましょう。",
        "cta_note": "iPhone・iPad・一部無料",
        "badge_small": "近日公開",
        "badge_live": "ダウンロード",
        "railmap_caption": "路線をタップで記録、色が広がり、スタンプが押される。",
        "how_kicker": "使い方", "how_num": "01–03",
        "how_h2": "駅をタップしてから、<em>スタンプが押される</em>まで。",
        "steps": [
            ["記録", "駅をタップして記録", "地図の駅をタップするだけ。乗った日付と区間を鉄ログが記録します。"],
            ["着色", "地図が色づく", "乗った路線の色が地図に広がります。未乗の区間はグレーのまま、乗った実感が一目でわかります。"],
            ["収集", "スタンプが貯まる", "路線を完乗すると、朱色の「完乗」スタンプが押されます。帳面のページが少しずつ埋まっていきます。"],
        ],
        "value_kicker": "全国データ", "value_num": "JR・私鉄・第三セクター",
        "value_h2": "全国<em>163社・571路線・9,706駅</em>を、これ一つで。",
        "value_lede": "JRグループ・大手私鉄・地方私鉄・第三セクターの路線データをあらかじめ収録。山手線一周でも、全国完乗でも、鉄ログが記録を引き継ぎます。",
        "stats": [["163", "鉄道会社"], ["571", "路線"], ["9,706", "駅"]],
        "shots_kicker": "画面", "shots_num": "IOS",
        "shots_h2": "旅先で書き足す<em>乗車記録。</em>",
        "shots_caps": ["地図がそのまま乗車記録に", "駅スタンプ帳で会社別に管理", "完乗の瞬間に届く記念カード"],
        "feat_kicker": "こだわり", "feat_num": "06",
        "feat_h2": "記録する人のための、<em>心配り</em>。",
        "feats": [
            ["過去の乗車もOK", "昔の乗車履歴もあとから登録できます。今日から始めても、過去の完乗記録はそのまま有効です。", False],
            ["区間まとめて入力", "起点と終点を選ぶだけで、区間内の駅をまとめて乗車済みにできます。", False],
            ["完乗祝いカード", "路線を完乗すると、朱印風の記念カードが自動で作られます。SNSでのシェアにも使えます。", False],
            ["47都道府県ヒートマップ", "都道府県ごとの乗車率を地図の濃淡で可視化。旅の足跡が色でわかります。", True],
            ["PDF御朱印帳", "スタンプ帳をPDFで書き出して、印刷したり手元に保存したりできます。", True],
            ["記録は手元に残る", "iCloudで同期し、JSONバックアップとCSV書き出しにいつでも対応。機種変更しても、ほかのツールへ移しても、記録はあなたのものです。無料。", False],
        ],
        "final_h2": "次の一駅から、<em>乗りつぶし</em>を記録しよう。",
        "final_lede": "App Store で配信中。",
        "f_contact": "お問い合わせ", "f_privacy": "プライバシーポリシー", "f_terms": "利用規約",
    },
    "ko": {
        "dir": "ko/", "lang": "ko", "font": '"Apple SD Gothic Neo", "Pretendard"',
        "title": "테츠로그 — 탄 역이, 그대로 지도가 됩니다",
        "desc": "역을 탭하면 탑승이 기록됩니다. 탄 노선의 색이 지도 위에 퍼지고, 완주하면 붉은 인장 스탬프가 찍힙니다. 일본 전국 163개사·571개 노선·9,706개 역을 담은 철도 여행 기록 앱.",
        "og_title": "테츠로그 — 일본 철도 여행 기록",
        "og_desc": "탄 역이, 그대로 지도가 됩니다. 전국 163개사·571개 노선·9,706개 역.",
        "brand": "테츠로그",
        "kicker_word": "스탬프북",
        "kicker_num": "전국 9,706개 역",
        "h1": "탄 역이,<br>그대로 <em>지도가 됩니다</em>.",
        "sub": "지도 위 역을 탭하기만 하면 탑승이 기록됩니다. 탄 노선의 색이 그대로 지도에 퍼져요. 일본 여행에서 탄 노선을, 전국 163개사·571개 노선·9,706개 역 규모로 테츠로그의 스탬프북에 기록하세요.",
        "cta_note": "iPhone·iPad · 일부 무료",
        "badge_small": "곧 출시",
        "badge_live": "다운로드",
        "railmap_caption": "노선을 탭해 기록하면 색이 채워지고, 스탬프가 찍힙니다.",
        "how_kicker": "사용 방법", "how_num": "01–03",
        "how_h2": "역을 탭한 순간부터, <em>스탬프가 찍히기</em>까지.",
        "steps": [
            ["기록", "지나온 역을 탭해서 기록", "지도 위 역을 탭하기만 하면 됩니다. 탄 날짜와 구간을 테츠로그가 기록해요."],
            ["채색", "지도가 색으로 채워짐", "탄 노선의 색이 지도 위에 퍼집니다. 안 탄 구간은 회색 그대로라 탄 흔적이 한눈에 보여요."],
            ["수집", "스탬프가 쌓임", "노선을 완주하면 붉은 인장 느낌의 '완승' 스탬프가 찍힙니다. 페이지가 한 장씩 채워지는 재미가 있어요."],
        ],
        "value_kicker": "전국 데이터", "value_num": "JR·사철·제3섹터",
        "value_h2": "전국 <em>163개사·571개 노선·9,706개 역</em>을 이 앱 하나로.",
        "value_lede": "JR그룹·대형 사철·지방 사철·제3섹터 노선 데이터를 미리 담아뒀어요. 야마노테선 한 바퀴든, 전국 완주든 테츠로그가 기록을 이어줍니다.",
        "stats": [["163", "철도회사"], ["571", "노선"], ["9,706", "역"]],
        "shots_kicker": "화면", "shots_num": "IOS",
        "shots_h2": "여행하며 채워가는 <em>탑승 기록장.</em>",
        "shots_caps": ["지도가 곧 탑승 기록이 됩니다", "회사별 역 스탬프북으로 정리", "완주 순간, 기념 카드가 도착"],
        "feat_kicker": "디테일", "feat_num": "06",
        "feat_h2": "기록할 때 유용한 <em>기능들.</em>",
        "feats": [
            ["과거 탑승도 OK", "예전에 탄 기록도 나중에 등록할 수 있어요. 오늘 시작해도 과거 완주 기록은 그대로 인정됩니다.", False],
            ["구간 한 번에 입력", "출발역과 도착역만 고르면 구간 전체가 한 번에 탑승 처리됩니다.", False],
            ["완승 기념 카드", "노선을 완주하면 인장 느낌의 기념 카드가 자동으로 만들어져요. SNS 공유도 가능합니다.", False],
            ["47개 도도부현 히트맵", "도도부현별 탑승률을 지도 색의 농도로 확인. 여행한 흔적이 그대로 드러나요.", True],
            ["PDF 고슈인초", "스탬프북을 PDF로 내보내 인쇄하거나 보관할 수 있어요.", True],
            ["기록은 내 손에 남는다", "iCloud로 동기화하고, JSON 백업과 CSV 내보내기를 언제든. 기기를 바꿔도, 다른 도구로 옮겨도 기록은 당신의 것입니다. 무료.", False],
        ],
        "final_h2": "다음 한 정거장부터, <em>완주 기록</em>을 시작하세요.",
        "final_lede": "App Store에서 만나보세요.",
        "f_contact": "문의", "f_privacy": "개인정보 처리방침", "f_terms": "이용약관",
    },
    "en": {
        "dir": "en/", "lang": "en", "font": None,
        "title": "Tetsulog — Every station you ride becomes a map",
        "desc": "Tap a station to log the ride. The line's color spreads across the map, and completing a line presses a vermilion stamp. A Japan rail trip log covering 163 operators, 571 lines, 9,706 stations.",
        "og_title": "Tetsulog — Japan Rail Trip Log",
        "og_desc": "Every station you ride becomes a map. 163 operators · 571 lines · 9,706 stations.",
        "brand": "Tetsulog",
        "kicker_word": "STAMP BOOK",
        "kicker_num": "9,706 STATIONS",
        "h1": "Every station you ride<br>becomes <em>a map</em>.",
        "sub": "Tap a station on the map and the ride is logged. The line's color spreads right across the map. Log your Japan rail trips — 163 operators, 571 lines, 9,706 stations — the way a stamp book fills, one page at a time.",
        "cta_note": "iPhone & iPad · Free, Pro available",
        "badge_small": "Coming soon",
        "badge_live": "Download on the",
        "railmap_caption": "Tap a line to log it — color spreads, a stamp is pressed.",
        "how_kicker": "HOW IT WORKS", "how_num": "01–03",
        "how_h2": "From a tap on the map to <em>a stamp in the book</em>.",
        "steps": [
            ["LOG", "Tap a station to log it", "Tap any station on the map. Tetsulog records the date and the segment you rode."],
            ["COLOR", "The map fills in color", "Ridden lines spread across the map in color. Unridden stretches stay gray, so your progress is obvious at a glance."],
            ["STAMP", "Stamps fill the book", "Complete a line and a vermilion “line complete” stamp is pressed. Page by page, the book fills up."],
        ],
        "value_kicker": "NATIONWIDE DATA", "value_num": "JR · PRIVATE · THIRD-SECTOR",
        "value_h2": "163 operators · 571 lines · <em>9,706 stations</em> — one app for all of Japan.",
        "value_lede": "Every JR group, major private railway, regional line and third-sector railway is preloaded. Whether it's one loop around the Yamanote Line or a lifelong completion run, Tetsulog keeps the log.",
        "stats": [["163", "operators"], ["571", "lines"], ["9,706", "stations"]],
        "shots_kicker": "SCREENS", "shots_num": "IOS",
        "shots_h2": "A notebook for <em>your rail trips.</em>",
        "shots_caps": ["The map is the ride log", "A stamp book organized by operator", "A keepsake card the moment you finish a line"],
        "feat_kicker": "DETAILS", "feat_num": "06",
        "feat_h2": "Built for <em>the record-keeper</em>.",
        "feats": [
            ["Backfill past rides", "Log rides you took years ago. Starting today doesn't erase the lines you'd already completed.", False],
            ["Log a whole segment at once", "Pick a start and end station — every stop between gets marked ridden in one step.", False],
            ["Line-complete keepsake card", "Finish a line and a stamp-style keepsake card is generated automatically. Shareable, too.", False],
            ["47-prefecture heatmap", "See your ridden ratio by prefecture on a shaded map of Japan.", True],
            ["PDF stamp book", "Export your stamp book as a PDF to print or archive.", True],
            ["Your records stay yours", "Synced via iCloud, with JSON backup and CSV export any time. New phone or another tool — the log is yours. Free.", False],
        ],
        "final_h2": "Start logging your <em>next line</em> today.",
        "final_lede": "Available on the App Store.",
        "f_contact": "Contact", "f_privacy": "Privacy", "f_terms": "Terms",
    },
    "zh": {
        "dir": "zh/", "lang": "zh-Hant", "font": '"PingFang TC"',
        "title": "Tetsulog 鉄ログ — 搭過的車站，直接變成地圖",
        "desc": "點一下車站就能記錄乘車。搭過的路線顏色會在地圖上蔓延，完乘時蓋下朱紅印章。收錄全日本163家公司、571條路線、9,706個車站的鐵道乘車紀錄 App。",
        "og_title": "Tetsulog 鉄ログ — 日本鐵道乘車紀錄",
        "og_desc": "搭過的車站，直接變成地圖。全日本163家公司・571條路線・9,706個車站。",
        "brand": "Tetsulog",
        "kicker_word": "集章帳",
        "kicker_num": "全日本 9,706 站",
        "h1": "搭過的車站，<br>直接<em>變成地圖</em>。",
        "sub": "只要點一下地圖上的車站，就能記錄這趟乘車。搭過的路線顏色會直接在地圖上蔓延。把日本之旅搭過的路線，以全日本163家公司・571條路線・9,706個車站的規模，像集章帳一樣記錄在 Tetsulog 裡。",
        "cta_note": "iPhone・iPad・部分免費",
        "badge_small": "即將上架",
        "badge_live": "下載",
        "railmap_caption": "點選路線記錄，顏色蔓延，印章蓋下。",
        "how_kicker": "使用方法", "how_num": "01–03",
        "how_h2": "從點一下車站，到<em>蓋下印章</em>為止。",
        "steps": [
            ["記錄", "點一下車站來記錄", "只要點地圖上的車站即可。乘車日期與區間都由 Tetsulog 記下。"],
            ["上色", "地圖染上顏色", "搭過的路線顏色會在地圖上蔓延。未搭乘的區間保持灰色，搭過多少一目瞭然。"],
            ["收集", "印章慢慢累積", "完乘一條路線，就會蓋下朱紅色的「完乘」印章。帳簿的頁面一點一點被填滿。"],
        ],
        "value_kicker": "全日本資料", "value_num": "JR・私鐵・第三部門",
        "value_h2": "全日本<em>163家公司・571條路線・9,706個車站</em>，一個 App 全收錄。",
        "value_lede": "JR 集團、大型私鐵、地方私鐵、第三部門鐵道的路線資料全部內建。不論是山手線一圈，還是全日本完乘，Tetsulog 都會替你記下來。",
        "stats": [["163", "鐵道公司"], ["571", "路線"], ["9,706", "車站"]],
        "shots_kicker": "畫面", "shots_num": "IOS",
        "shots_h2": "邊旅行邊記下的<em>搭乘紀錄。</em>",
        "shots_caps": ["地圖本身就是乘車紀錄", "依公司整理的車站集章帳", "完乘瞬間送達的紀念卡"],
        "feat_kicker": "堅持", "feat_num": "06",
        "feat_h2": "為記錄的人準備的<em>貼心設計</em>。",
        "feats": [
            ["過去的乘車也 OK", "以前搭過的紀錄也能事後補登。就算今天才開始，過去的完乘紀錄一樣有效。", False],
            ["整段區間一次輸入", "只要選擇起點與終點，區間內的車站就能一次全部標記為已搭乘。", False],
            ["完乘紀念卡", "完乘一條路線，就會自動生成朱印風的紀念卡，也能直接分享到社群。", False],
            ["47都道府縣熱度地圖", "以地圖深淺呈現各都道府縣的乘車率，旅行的足跡用顏色一看就懂。", True],
            ["PDF 御朱印帳", "可將集章帳匯出成 PDF，列印或留存都方便。", True],
            ["紀錄留在你手上", "透過 iCloud 同步，隨時可匯出 JSON 備份與 CSV。換機或搬到其他工具，紀錄都是你的。免費。", False],
        ],
        "final_h2": "從下一站開始，記錄你的<em>完乘之旅</em>。",
        "final_lede": "已在 App Store 上架。",
        "f_contact": "聯絡我們", "f_privacy": "隱私權政策", "f_terms": "使用條款",
    },
    "zh-hans": {
        "dir": "zh-hans/", "lang": "zh-Hans", "font": '"PingFang SC"',
        "title": "Tetsulog 鉄ログ — 搭过的车站，直接变成地图",
        "desc": "点一下车站就能记录乘车。搭过的路线颜色会在地图上蔓延，完乘时盖下朱红印章。收录全日本163家公司、571条路线、9,706个车站的铁道乘车记录 App。",
        "og_title": "Tetsulog 鉄ログ — 日本铁道乘车记录",
        "og_desc": "搭过的车站，直接变成地图。全日本163家公司・571条路线・9,706个车站。",
        "brand": "Tetsulog",
        "kicker_word": "集章帐",
        "kicker_num": "全日本 9,706 站",
        "h1": "搭过的车站，<br>直接<em>变成地图</em>。",
        "sub": "只要点一下地图上的车站，就能记录这趟乘车。搭过的路线颜色会直接在地图上蔓延。把日本之旅搭过的路线，以全日本163家公司・571条路线・9,706个车站的规模，像集章帐一样记录在 Tetsulog 里。",
        "cta_note": "iPhone・iPad・部分免费",
        "badge_small": "即将上架",
        "badge_live": "下载",
        "railmap_caption": "点击路线记录，颜色蔓延，印章盖下。",
        "how_kicker": "使用方法", "how_num": "01–03",
        "how_h2": "从点一下车站，到<em>盖下印章</em>为止。",
        "steps": [
            ["记录", "点一下车站来记录", "只要点地图上的车站即可。乘车日期与区间都由 Tetsulog 记下。"],
            ["上色", "地图染上颜色", "搭过的路线颜色会在地图上蔓延。未乘坐的区间保持灰色，搭过多少一目了然。"],
            ["收集", "印章慢慢累积", "完乘一条路线，就会盖下朱红色的「完乘」印章。帐簿的页面一点一点被填满。"],
        ],
        "value_kicker": "全日本数据", "value_num": "JR・私铁・第三部门",
        "value_h2": "全日本<em>163家公司・571条路线・9,706个车站</em>，一个 App 全收录。",
        "value_lede": "JR 集团、大型私铁、地方私铁、第三部门铁道的路线数据全部内置。不论是山手线一圈，还是全日本完乘，Tetsulog 都会替你记下来。",
        "stats": [["163", "铁道公司"], ["571", "路线"], ["9,706", "车站"]],
        "shots_kicker": "画面", "shots_num": "IOS",
        "shots_h2": "边旅行边记下的<em>乘坐记录。</em>",
        "shots_caps": ["地图本身就是乘车记录", "依公司整理的车站集章帐", "完乘瞬间送达的纪念卡"],
        "feat_kicker": "坚持", "feat_num": "06",
        "feat_h2": "为记录的人准备的<em>贴心设计</em>。",
        "feats": [
            ["过去的乘车也 OK", "以前搭过的记录也能事后补登。就算今天才开始，过去的完乘记录一样有效。", False],
            ["整段区间一次输入", "只要选择起点与终点，区间内的车站就能一次全部标记为已乘坐。", False],
            ["完乘纪念卡", "完乘一条路线，就会自动生成朱印风的纪念卡，也能直接分享到社区。", False],
            ["47都道府县热度地图", "以地图深浅呈现各都道府县的乘车率，旅行的足迹用颜色一看就懂。", True],
            ["PDF 御朱印帐", "可将集章帐导出成 PDF，打印或留存都方便。", True],
            ["记录留在你手上", "通过 iCloud 同步，随时可导出 JSON 备份与 CSV。换机或搬到其他工具，记录都是你的。免费。", False],
        ],
        "final_h2": "从下一站开始，记录你的<em>完乘之旅</em>。",
        "final_lede": "已在 App Store 上架。",
        "f_contact": "联系我们", "f_privacy": "隐私权政策", "f_terms": "使用条款",
    },
}


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


def kicker(word_glyph_text, num_text, extra_class=""):
    return (f'<div class="kicker {extra_class}"><span class="glyph">帳</span>'
            f'<span>· {word_glyph_text}</span><span class="rule"></span><span class="num">{num_text}</span></div>')


def badge(loc, el_id):
    if APP_STORE_URL:
        apple_svg = '<svg viewBox="0 0 384 512" aria-hidden="true"><path d="M318.7 268.7c-.2-36.7 16.4-64.4 50-84.8-18.8-26.9-47.2-41.7-84.7-44.6-35.5-2.8-74.3 20.7-88.5 20.7-15 0-49.4-19.7-76.4-19.7C63.3 141.2 4 184.8 4 273.5q0 39.3 14.4 81.2c12.8 36.7 59 126.7 107.2 125.2 25.2-.6 43-17.9 75.8-17.9 31.8 0 48.3 17.9 76.4 17.9 48.6-.7 90.4-82.5 102.6-119.3-65.2-30.7-61.7-90-61.7-91.9zm-56.6-164.2c27.3-32.4 24.8-61.9 24-72.5-24.1 1.4-52 16.4-67.9 34.9-17.5 19.8-27.8 44.3-25.6 71.9 26.1 2 49.9-11.4 69.5-34.3z"/></svg>'
        return (f'<a class="store-badge" id="{el_id}" href="{APP_STORE_URL}" aria-label="App Store">{apple_svg}'
                f'<span class="txt"><small>{loc['badge_live']}</small><strong>App Store</strong></span></a>')
    return (f'<span class="store-badge disabled" id="{el_id}" aria-disabled="true">'
            f'<span class="txt"><small>{loc["badge_small"]}</small><strong>App Store</strong></span></span>')


def render(key):
    loc = LOCALES[key]
    rel = "../" if loc["dir"] else ""
    font_override = (f'<style>body{{font-family:-apple-system,BlinkMacSystemFont,{loc["font"]},'
                      f'"Segoe UI",sans-serif}}</style>') if loc["font"] else ""

    marquee = "".join(
        f'<span class="{"hl" if hl else ""}">{m}</span>'
        for m, hl in MARQUEE_ITEMS * 2
    )
    steps = "".join(
        f'<div class="step"><span class="tag">{tag}</span><span class="n">0{i+1}</span><h3>{h}</h3><p>{p}</p></div>'
        for i, (tag, h, p) in enumerate(loc["steps"])
    )
    stats = "".join(
        f'<div class="stat"><div class="n">{n}</div><div class="l">{l}</div></div>'
        for n, l in loc["stats"]
    )
    shot_files = ["1-map", "2-stamps", "3-completion"]
    shots = "".join(
        f'<figure><div class="phone"><img src="{rel}assets/shot-{f}.png" alt="{cap}" loading="lazy"><div class="island"></div></div><figcaption>{cap}</figcaption></figure>'
        for f, cap in zip(shot_files, loc["shots_caps"])
    )
    feats = "".join(
        f'<div class="feat"><h3>{h}{"<span class=\'pro\'>PRO</span>" if pro else ""}</h3><p>{p}</p></div>'
        for h, p, pro in loc["feats"]
    )

    faq_items = "".join(
        f"<details><summary>{html_escape(q)}</summary><p>{html_escape(a)}</p></details>"
        for q, a in FAQ[key]["items"]
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
<meta property="og:image" content="{BASE_URL}assets/og-image.png">
<meta property="og:type" content="website">
<meta property="og:url" content="{BASE_URL}{loc['dir']}">
<meta name="twitter:card" content="summary_large_image">
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
    <a class="wordmark" href="{rel if rel else './'}"><img src="{rel}assets/icon-180.png" alt=""><span>{loc['brand']}</span></a>
    <div class="lang">{lang_nav(loc['dir'], rel)}</div>
  </div>
</nav>

<header class="hero">
  <div class="wrap">
    <div>
      <div class="ekimeihyo">
        <div class="bar"></div>
        <div class="body">
          <div class="adj adj-prev"><span class="roundel">鉄</span><span class="arrow">← {loc['kicker_word']}</span></div>
          <div class="name"><span class="jp">{loc['brand']}</span><span class="en">TETSULOG</span></div>
          <div class="adj adj-next"><span class="arrow">{loc['kicker_num']} →</span></div>
        </div>
      </div>
      <h1>{loc['h1']}</h1>
      <p class="sub">{loc['sub']}</p>
      <div class="cta">
        {badge(loc, 'storeLink')}
        <span class="note">{loc['cta_note']}</span>
      </div>
    </div>
    <div class="railmap-col">
      <div class="railmap">
        <div class="railmap-underlay" aria-hidden="true" style="background-image:url('{rel}assets/yamanote-map.png')"></div>
        {RAILMAP_SVG}
        <div class="stamp"><span>完乗</span></div>
      </div>
      <div class="railmap-caption">
        <span>{loc['railmap_caption']}</span>
        <span class="railmap-legend"><span><i class="g"></i></span></span>
      </div>
      <div class="railmap-credit">{OSM_CREDIT}</div>
    </div>
  </div>
</header>

<div class="marquee" aria-hidden="true"><div class="track">{marquee}</div></div>

<section>
  <div class="wrap">
    {kicker(loc['how_kicker'], loc['how_num'])}
    <h2>{loc['how_h2']}</h2>
    <div class="steps">{steps}</div>
  </div>
</section>

<section class="value">
  <div class="ghost">9,706</div>
  <div class="wrap">
    {kicker(loc['value_kicker'], loc['value_num'])}
    <h2>{loc['value_h2']}</h2>
    <p class="lede">{loc['value_lede']}</p>
    <div class="stats">{stats}</div>
  </div>
</section>

<section class="shots">
  <div class="wrap">
    {kicker(loc['shots_kicker'], loc['shots_num'])}
    <h2>{loc['shots_h2']}</h2>
    <div class="row">{shots}</div>
  </div>
</section>

<section>
  <div class="wrap">
    {kicker(loc['feat_kicker'], loc['feat_num'])}
    <h2>{loc['feat_h2']}</h2>
    <div class="grid6">{feats}</div>
  </div>
</section>

<section class="final">
  <div class="wrap">
    <h2>{loc['final_h2']}</h2>
    <p class="lede">{loc['final_lede']}</p>
    <div class="cta">{badge(loc, 'storeLink2')}</div>
  </div>
</section>

<section class="faq" id="faq">
  <div class="wrap">
    <h2>{FAQ[key]['title']}</h2>
    <div class="faq-list">{faq_items}</div>
  </div>
</section>

<footer>
  <div class="wrap">
    <div class="brand"><img src="{rel}assets/icon-180.png" alt=""><strong>kkiruk studio</strong></div>
    <div class="links">
      <a href="mailto:kkirukstudio.help@gmail.com">{loc['f_contact']}</a>
      <a href="/legal/privacy/">{loc['f_privacy']}</a>
      <a href="/legal/terms/">{loc['f_terms']}</a>
    </div>
    <div>© 2026 kkiruk studio</div>
  </div>
</footer>

<script src="/ga.js"></script>
</body>
</html>
"""
    out = ROOT / loc["dir"] / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)} ({len(html)} bytes)")


for key in LOCALES:
    render(key)

# Preserve discovery metadata and visible product facts after regeneration.
if __name__ == "__main__":
    import runpy as _seo_runpy
    from pathlib import Path as _SeoPath
    _seo_runpy.run_path(str(_SeoPath(__file__).resolve().parent.parent / "gen" / "refresh_seo.py"), run_name="__main__")
