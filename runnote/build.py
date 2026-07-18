#!/usr/bin/env python3
"""Generate index.html for every locale from one template.

Usage: python3 build.py
Output: ./index.html (ko, root), ./en/index.html, ./ja/index.html

Root = Korean (kkiruk studio's primary market for RunNote). Do not hand-edit
the generated HTML files -- edit this file and re-run `python3 build.py`.
"""
import pathlib

ROOT = pathlib.Path(__file__).parent
BASE_URL = "https://www.kkirukstudio.com/runnote/"
APP_STORE_URL = ""  # fill in after App Store approval, e.g. https://apps.apple.com/app/id0000000000

LANG_LABELS = [("", "한국어"), ("en/", "EN"), ("ja/", "日本語"), ("zh/", "繁體")]

# Shared, non-localized decorative data ---------------------------------

# 35-cell (7x5) calendar mockup: '' = no run, d1/d2/d3 = run-day intensity
CAL_CELLS = ["", "", "d1", "", "", "", "d2",
             "", "", "", "d1", "", "", "",
             "d3", "", "", "d1", "", "", "d2",
             "", "", "d1", "", "", "", "d3",
             "", "d2", "", "", "d1", "", ""]

# HR 5-zone time-distribution widths (%), sum = 100
ZONE_WIDTHS = [10, 25, 35, 20, 10]

# km-split pace values in seconds/km -> shows the uphill fade
SPLIT_SECONDS = [358, 362, 370, 385, 400]
SPLIT_LABELS = ["1KM", "2KM", "3KM", "4KM", "5KM"]


def sec_to_pace(sec):
    m, s = divmod(sec, 60)
    return f"{m}:{s:02d}"


def split_bar_width(sec):
    lo, hi = min(SPLIT_SECONDS), max(SPLIT_SECONDS)
    return round(40 + (sec - lo) / (hi - lo) * 55)


LOCALES = {
    "ko": {
        "dir": "", "lang": "ko", "font": '"Apple SD Gothic Neo", "Pretendard"',
        "title": "RunNote — 러닝 후 한 줄 회고로 완성되는 AI 코칭",
        "desc": "실시간 트래킹이 아닌 회고 기반 러닝 기록장. 워치로 뛰고 컨디션과 한 줄만 남기면, 기록이 쌓일수록 Claude AI 코칭이 정교해집니다.",
        "og_title": "RunNote — 나를 아는 AI 러닝 코치",
        "og_desc": "한 줄 회고가 쌓일수록 정교해지는 AI 코칭.",
        "kicker_num": "러닝 회고 저널",
        "h1": "뛰고 나서 한 줄,<br>기록이 쌓일수록 <em>나를 아는 코치</em>가 됩니다",
        "sub": "실시간 트래킹 앱이 아니에요. 워치로 뛰고 앱을 열면 기록은 자동으로 들어와 있고, 남기는 건 컨디션과 한 줄 회고뿐. 그 한 줄이 쌓일수록 Claude AI가 당신의 패턴을 더 정확히 짚어냅니다.",
        "note": "출시 예정 · iPhone &amp; Apple Watch · 7일 무료 체험",
        "badge_small": "다운로드는", "badge_aria": "App Store에서 다운로드",
        "badge_soon": "곧 App Store에서 만나요",
        "chips": [["5K", "km 오늘"], ["Z3", "심박존"], ["AI", "코칭 완료"]],
        "marquee": ["HEALTHKIT 자동 동기화", "AI 코칭", "심박 5구간", "케이던스", "코치 노트", "러너 레벨", "신발 거리", "훈련 플랜"],
        "demo": {
            "stat_labels": ["거리", "시간", "평균 심박"],
            "stat_values": ["5.2 km", "32:10", "155 bpm"],
            "mood": "🙂",
            "note": "막판에 오르막에서 페이스가 무너졌다",
            "ai_label": "AI 코치",
            "ai_lines": [
                "최근 3번의 러닝에서 같은 패턴이 보여요. 오르막 전 케이던스를 5spm 올려보세요.",
                "이번 주말 같은 코스, 다시 도전해볼까요?",
            ],
        },
        "how_kicker": "사용 방법", "how_num": "01–03",
        "how_h2": "뛰고, 한 줄 남기고, <em>코칭</em>을 받으세요.",
        "steps": [
            ["워치로 뛰기", "Apple Watch로 뛰기만 하면 끝. HealthKit이 거리·페이스·심박을 자동으로 가져옵니다."],
            ["한 줄 회고", "컨디션 이모지 하나, 한 줄 메모. 아팠던 곳이 있으면 부위까지. 그게 전부예요."],
            ["AI 코칭 받기", "쌓인 회고를 바탕으로 Claude가 패턴을 짚고, 다음 러닝을 위한 질문을 남깁니다."],
        ],
        "value_kicker": "정교해지는 코칭", "value_num": "1 → 20 RUNS",
        "value_h2": "회고가 <em>10줄</em>이 되면, 코칭이 달라집니다.",
        "value_lede": "1회차는 누구에게나 하는 조언, 10회차는 당신의 오르막 페이스 패턴을 아는 조언. 기록이 쌓일수록 코칭 정밀도가 올라갑니다.",
        "value_axis": "코칭 정밀도",
        "chart_points": [["1회", 40], ["5회", 65], ["10회", 82], ["20회", 96]],
        "notes": [
            ["3주 전 관찰", "오르막에서 페이스가 무너지는 패턴이 반복됩니다."],
            ["2주 전 관찰", "왼쪽 무릎 통증이 3주 연속 기록됐어요."],
            ["이번 주 관찰", "주말 장거리 후 회복이 빠른 편이에요."],
        ],
        "shots_kicker": "화면", "shots_num": "SCREENS",
        "shots_h2": "기록에서 <em>코칭</em>까지, 한눈에.",
        "shots_caps": ["홈 · 오늘의 러닝", "러닝 상세 기록", "AI 코칭 카드", "히스토리 · 캘린더"],
        "cal_head": "2026년 7월 · 12회 · 68km",
        "cal_list": [["7월 28일", "5.2 km", "5:58/km"], ["7월 25일", "8.0 km", "6:20/km"], ["7월 21일", "3.1 km", "6:05/km"]],
        "zone_legend": ["Z1", "Z2", "Z3", "Z4", "Z5"],
        "coach_mock_lines": [
            "이번 주 3번의 러닝 모두 오르막에서 페이스가 5~8% 떨어졌어요.",
            "다음 러닝 전, 오르막 구간 케이던스를 5spm 올려보는 건 어떨까요?",
        ],
        "coach_mock_tag": "코치 노트 · 3주 연속 관찰",
        "feat_kicker": "디테일", "feat_num": "06",
        "feat_h2": "작은 기록장, <em>분명한 차별점</em>.",
        "feats": [
            ["HealthKit 자동 동기화", "워치로 뛰고 앱만 열면 거리·페이스·심박이 자동으로 들어와 있어요."],
            ["러닝 당시 날씨 자동 기록", "WeatherKit이 그날의 기온과 습도를 기록에 남깁니다."],
            ["러닝 다이내믹스 + 자세 점수", "수직 진폭·접지 시간·보폭·파워로 매기는 자세 점수."],
            ["심박 5구간 · km 스플릿 · 고도", "존별 시간 분포와 구간별 페이스, 고도 변화까지 한눈에."],
            ["통증 부위별 관리 가이드", "무릎, 발목… 부위별 원인과 스트레칭, 쉬어야 할 신호까지."],
            ["코치 노트 (장기 기억)", "러닝을 거듭할수록 AI가 당신에 대해 기억하는 것들이 쌓입니다."],
        ],
        "final_h2": "이제, 뛰고 한 줄만 남기세요.",
        "final_lede": "출시 후 7일 무료 체험 · iPhone &amp; Apple Watch",
        "f_contact": "문의", "f_privacy": "개인정보 처리방침", "f_terms": "이용약관",
    },
    "en": {
        "dir": "en/", "lang": "en", "font": None,
        "title": "RunNote — A one-line running journal with AI coaching that knows you",
        "desc": "Not a live-tracking app. Run with your Watch, log one line about how you felt, and Claude's coaching gets sharper with every entry.",
        "og_title": "RunNote — An AI running coach that learns you",
        "og_desc": "Coaching that gets sharper with every one-line reflection.",
        "kicker_num": "RUNNING JOURNAL",
        "h1": "Run. Write one line.<br>Get a coach that <em>actually knows you</em>.",
        "sub": "This isn't a live-tracking app. Run with your Watch, open RunNote, and your data's already there. All you add is how you felt — one line. The more you write, the sharper Claude's coaching gets.",
        "note": "Coming soon · iPhone &amp; Apple Watch · 7-day free trial",
        "badge_small": "Download on the", "badge_aria": "Download on the App Store",
        "badge_soon": "Coming soon to the App Store",
        "chips": [["5K", "km today"], ["Z3", "HR zone"], ["AI", "coached"]],
        "marquee": ["HEALTHKIT SYNC", "AI COACHING", "HR ZONES", "CADENCE", "COACH NOTES", "RUNNER LEVELS", "SHOE MILEAGE", "TRAINING PLANS"],
        "demo": {
            "stat_labels": ["DISTANCE", "TIME", "AVG HR"],
            "stat_values": ["5.2 km", "32:10", "155 bpm"],
            "mood": "🙂",
            "note": "Legs gave out on the last hill at parkrun again",
            "ai_label": "AI COACH",
            "ai_lines": [
                "Same pattern the last 3 runs — you fade on climbs after 2 miles. Try lifting cadence 5 spm before the hill.",
                "Want to hit that same hill again this Saturday?",
            ],
        },
        "how_kicker": "HOW IT WORKS", "how_num": "01–03",
        "how_h2": "Run, write one line, get <em>coached</em>.",
        "steps": [
            ["Run", "Just run with your Apple Watch. HealthKit pulls in distance, pace and heart rate automatically."],
            ["Reflect", "One condition emoji, one line. Add where it hurt, if it did. That's it."],
            ["Get coached", "Claude reads your history, spots the pattern, and leaves you a question for next time."],
        ],
        "value_kicker": "SHARPER OVER TIME", "value_num": "1 → 20 RUNS",
        "value_h2": "Ten entries in, the coaching <em>changes</em>.",
        "value_lede": "Run one gets generic advice. Run ten gets advice that knows your hill-pace pattern. Coaching gets sharper the more you log.",
        "value_axis": "Coaching precision",
        "chart_points": [["RUN 1", 40], ["RUN 5", 65], ["RUN 10", 82], ["RUN 20", 96]],
        "notes": [
            ["Observed 3 weeks ago", "You keep fading on climbs — same pattern for 3 runs."],
            ["Observed 2 weeks ago", "Left knee soreness logged 3 weeks running."],
            ["Observed this week", "You recover fast after long weekend runs."],
        ],
        "shots_kicker": "SCREENS", "shots_num": "SCREENS",
        "shots_h2": "From your log to <em>your coaching</em>, at a glance.",
        "shots_caps": ["HOME · TODAY'S RUN", "RUN DETAIL", "AI COACHING CARD", "HISTORY · CALENDAR"],
        "cal_head": "JULY 2026 · 12 RUNS · 68 KM",
        "cal_list": [["Jul 28", "5.2 km", "5:58/km"], ["Jul 25", "8.0 km", "6:20/km"], ["Jul 21", "3.1 km", "6:05/km"]],
        "zone_legend": ["Z1", "Z2", "Z3", "Z4", "Z5"],
        "coach_mock_lines": [
            "All three runs this week lost 5-8% pace on climbs.",
            "Before your next run, try lifting cadence 5 spm on the uphill sections.",
        ],
        "coach_mock_tag": "Coach note · observed 3 weeks running",
        "feat_kicker": "DETAILS", "feat_num": "06",
        "feat_h2": "Small journal. <em>Deliberate</em> differences.",
        "feats": [
            ["HealthKit auto-sync", "Run with your Watch, open the app — distance, pace and heart rate are already there."],
            ["Weather, logged automatically", "WeatherKit tags every run with the temperature and humidity at the time."],
            ["Running Dynamics + form score", "Vertical oscillation, ground contact time, stride length and power, scored."],
            ["5 HR zones · km splits · elevation", "Zone time distribution, per-km pace, and elevation, all at a glance."],
            ["Pain-area guide", "Knee, ankle, whatever hurts — causes, stretches, and when to actually rest."],
            ["Coach notes (long-term memory)", "The more you run, the more the AI remembers about you."],
        ],
        "final_h2": "Run. Write one line. That's it.",
        "final_lede": "7-day free trial at launch · iPhone &amp; Apple Watch",
        "f_contact": "Contact", "f_privacy": "Privacy", "f_terms": "Terms",
    },
    "ja": {
        "dir": "ja/", "lang": "ja", "font": '"Hiragino Kaku Gothic ProN", "Hiragino Sans", "Yu Gothic"',
        "title": "RunNote — ひと言の振り返りで磨かれるAIランニングコーチ",
        "desc": "リアルタイムトラッキングではなく、振り返り型のランニング記録アプリ。Apple Watchで走ってひと言残すだけで、ClaudeのAIコーチングが記録とともに的確になります。",
        "og_title": "RunNote — あなたを知るAIランニングコーチ",
        "og_desc": "ひと言の振り返りが積み重なるほど的確になるコーチング。",
        "kicker_num": "ランニング日記",
        "h1": "走って、ひと言書くだけ。<br>記録が増えるほど<em>あなたを知るコーチ</em>に。",
        "sub": "リアルタイムのトラッキングアプリではありません。Apple Watchで走ってRunNoteを開けば、記録はもう入っています。書くのは体調とひと言だけ。積み重なるほどClaudeのコーチングが的確になります。",
        "note": "近日公開 · iPhone &amp; Apple Watch · 7日間無料トライアル",
        "badge_small": "ダウンロードは", "badge_aria": "App Store でダウンロード",
        "badge_soon": "近日App Storeで公開",
        "chips": [["5K", "本日の距離"], ["Z3", "心拍ゾーン"], ["AI", "コーチ済み"]],
        "marquee": ["HEALTHKIT連携", "AIコーチング", "心拍5ゾーン", "ケイデンス", "コーチノート", "ランナーレベル", "シューズ距離", "トレーニング計画"],
        "demo": {
            "stat_labels": ["距離", "時間", "平均心拍"],
            "stat_values": ["5.2 km", "32:10", "155 bpm"],
            "mood": "🙂",
            "note": "皇居ランの坂道で、また後半ペースが落ちた",
            "ai_label": "AIコーチ",
            "ai_lines": [
                "直近3回のランで同じパターンが出ています。坂の前でケイデンスを5spm上げてみましょう。",
                "今週末も同じコースで試してみますか？",
            ],
        },
        "how_kicker": "使い方", "how_num": "01–03",
        "how_h2": "走って、ひと言残して、<em>コーチングを受ける</em>。",
        "steps": [
            ["走る", "Apple Watchで走るだけ。HealthKitが距離・ペース・心拍を自動で取り込みます。"],
            ["ひと言残す", "体調の絵文字ひとつと、ひと言メモ。痛みがあれば部位も。それだけです。"],
            ["コーチングを受ける", "積み重なった記録からClaudeがパターンを見つけ、次のランへの問いを残します。"],
        ],
        "value_kicker": "積み重ねるほど的確に", "value_num": "1 → 20 RUNS",
        "value_h2": "記録が<em>10回</em>を超えると、コーチングが変わります。",
        "value_lede": "1回目は誰にでも当てはまる助言。10回目はあなたの坂道ペースの癖を知った助言。積み重ねるほどコーチングは的確になります。",
        "value_axis": "コーチング精度",
        "chart_points": [["1回目", 40], ["5回目", 65], ["10回目", 82], ["20回目", 96]],
        "notes": [
            ["3週間前の観察", "坂道で失速するパターンが3回連続で見られます。"],
            ["2週間前の観察", "左膝の違和感が3週連続で記録されています。"],
            ["今週の観察", "週末のロング走の翌週、回復が早い傾向です。"],
        ],
        "shots_kicker": "画面", "shots_num": "SCREENS",
        "shots_h2": "記録から<em>コーチング</em>まで、ひと目で。",
        "shots_caps": ["ホーム・今日のラン", "ラン詳細記録", "AIコーチングカード", "履歴・カレンダー"],
        "cal_head": "2026年7月 · 12回 · 68km",
        "cal_list": [["7月28日", "5.2 km", "5:58/km"], ["7月25日", "8.0 km", "6:20/km"], ["7月21日", "3.1 km", "6:05/km"]],
        "zone_legend": ["Z1", "Z2", "Z3", "Z4", "Z5"],
        "coach_mock_lines": [
            "今週の3回のランすべてで、坂道でペースが5〜8%落ちています。",
            "次のランの前に、坂道区間のケイデンスを5spm上げてみませんか？",
        ],
        "coach_mock_tag": "コーチノート・3週連続の傾向",
        "feat_kicker": "こだわり", "feat_num": "06",
        "feat_h2": "小さな記録帳、<em>明確な違い</em>。",
        "feats": [
            ["HealthKit自動連携", "Watchで走ってアプリを開くだけ。距離・ペース・心拍はもう入っています。"],
            ["その日の天気を自動記録", "WeatherKitがランニング当時の気温・湿度を記録に残します。"],
            ["ランニングダイナミクス + フォームスコア", "上下動・接地時間・歩幅・パワーからフォームを採点。"],
            ["心拍5ゾーン・kmスプリット・高度", "ゾーン別の時間配分、区間ペース、高度変化がひと目でわかります。"],
            ["部位別 痛みガイド", "膝、足首… 部位ごとの原因・ストレッチ・休むべきサインまで。"],
            ["コーチノート(長期記憶)", "走るほど、AIがあなたについて覚えていることが増えていきます。"],
        ],
        "final_h2": "走って、ひと言書くだけ。",
        "final_lede": "公開時7日間無料トライアル · iPhone &amp; Apple Watch",
        "f_contact": "お問い合わせ", "f_privacy": "プライバシーポリシー", "f_terms": "利用規約",
    },
    "zh": {
        "dir": "zh/", "lang": "zh-Hant", "font": '"PingFang TC", "Microsoft JhengHei"',
        "title": "RunNote — 用一句跑後筆記,打造懂你的 AI 教練",
        "desc": "不是即時追蹤,而是以筆記為核心的跑步紀錄。用手錶跑完,只需留下狀態和一句話,記錄越多,Claude AI 教練就越精準。",
        "og_title": "RunNote — 懂你的 AI 跑步教練",
        "og_desc": "一句筆記累積越多,教練建議越精準。",
        "kicker_num": "跑步筆記日誌",
        "h1": "跑完寫一句,<br>記錄越多,就成為<em>懂你的教練</em>",
        "sub": "這不是即時追蹤 App。用 Apple Watch 跑步後打開 App,記錄早已自動同步,你只需留下狀態和一句筆記。這一句話累積越多,Claude AI 就能越精準掌握你的模式。",
        "note": "即將推出 · iPhone &amp; Apple Watch · 7 天免費試用",
        "badge_small": "立即下載", "badge_aria": "前往 App Store 下載",
        "badge_soon": "即將於 App Store 上架",
        "chips": [["5K", "今日公里"], ["Z3", "心率區間"], ["AI", "教練完成"]],
        "marquee": ["HEALTHKIT 自動同步", "AI 教練", "心率5區間", "步頻", "教練筆記", "跑者等級", "鞋子里程", "訓練計畫"],
        "demo": {
            "stat_labels": ["距離", "時間", "平均心率"],
            "stat_values": ["5.2 km", "32:10", "155 bpm"],
            "mood": "🙂",
            "note": "最後在上坡配速崩潰了",
            "ai_label": "AI 教練",
            "ai_lines": [
                "最近3次跑步都出現同樣模式。上坡前試著把步頻提高5spm。",
                "這個週末要不要再挑戰一次同樣路線?",
            ],
        },
        "how_kicker": "使用方法", "how_num": "01–03",
        "how_h2": "跑步、留下一句話、接受<em>教練指導</em>。",
        "steps": [
            ["用手錶跑步", "只要戴著Apple Watch跑步就好。HealthKit會自動抓取距離、配速、心率。"],
            ["寫一句筆記", "一個狀態表情符號,加一句話。如果哪裡不舒服,寫下部位。就這麼簡單。"],
            ["接受AI教練指導", "根據累積的筆記,Claude會指出模式,並為下次跑步留下提問。"],
        ],
        "value_kicker": "越來越精準的教練", "value_num": "1 → 20 RUNS",
        "value_h2": "筆記累積到<em>10篇</em>,教練建議就會不同。",
        "value_lede": "第1次是給任何人的建議,第10次是了解你上坡配速模式的建議。記錄越多,教練精準度越高。",
        "value_axis": "教練精準度",
        "chart_points": [["第1次", 40], ["第5次", 65], ["第10次", 82], ["第20次", 96]],
        "notes": [
            ["3週前的觀察", "上坡配速崩潰的模式反覆出現。"],
            ["2週前的觀察", "左膝疼痛已連續記錄3週。"],
            ["本週觀察", "週末長跑後恢復速度較快。"],
        ],
        "shots_kicker": "畫面", "shots_num": "SCREENS",
        "shots_h2": "從記錄到<em>教練指導</em>,一目了然。",
        "shots_caps": ["首頁 · 今日跑步", "跑步詳細記錄", "AI 教練卡片", "歷史記錄 · 日曆"],
        "cal_head": "2026年7月 · 12次 · 68公里",
        "cal_list": [["7月28日", "5.2 km", "5:58/km"], ["7月25日", "8.0 km", "6:20/km"], ["7月21日", "3.1 km", "6:05/km"]],
        "zone_legend": ["Z1", "Z2", "Z3", "Z4", "Z5"],
        "coach_mock_lines": [
            "本週3次跑步,上坡配速都掉了5~8%。",
            "下次跑步前,試著把上坡路段的步頻提高5spm如何?",
        ],
        "coach_mock_tag": "教練筆記 · 連續3週觀察",
        "feat_kicker": "細節", "feat_num": "06",
        "feat_h2": "小小的記錄本,<em>明確的差異</em>。",
        "feats": [
            ["HealthKit 自動同步", "用手錶跑步後打開App,距離、配速、心率都已自動同步。"],
            ["自動記錄跑步當時天氣", "WeatherKit會將當天的氣溫與濕度記錄下來。"],
            ["跑步動態 + 姿勢評分", "以垂直振幅、觸地時間、步幅、功率評出的姿勢分數。"],
            ["心率5區間 · 公里分段 · 高度", "區間時間分布、分段配速、高度變化,一目了然。"],
            ["依部位管理的疼痛指南", "膝蓋、腳踝……各部位的原因、伸展方式,以及該休息的訊號。"],
            ["教練筆記(長期記憶)", "跑得越多,AI對你的了解就累積得越多。"],
        ],
        "final_h2": "現在,跑完只需留下一句話。",
        "final_lede": "上線後7天免費試用 · iPhone &amp; Apple Watch",
        "f_contact": "聯絡我們", "f_privacy": "隱私權政策", "f_terms": "使用條款",
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


def badge(loc, el_id):
    return (f'<a class="store-badge" id="{el_id}" href="#" aria-label="{loc["badge_aria"]}">{APPLE_SVG}'
            f'<span class="txt"><small>{loc["badge_small"]}</small><strong>App Store</strong></span></a>')


APPLE_SVG = '<svg viewBox="0 0 384 512" aria-hidden="true"><path d="M318.7 268.7c-.2-36.7 16.4-64.4 50-84.8-18.8-26.9-47.2-41.7-84.7-44.6-35.5-2.8-74.3 20.7-88.5 20.7-15 0-49.4-19.7-76.4-19.7C63.3 141.2 4 184.8 4 273.5q0 39.3 14.4 81.2c12.8 36.7 59 126.7 107.2 125.2 25.2-.6 43-17.9 75.8-17.9 31.8 0 48.3 17.9 76.4 17.9 48.6-.7 90.4-82.5 102.6-119.3-65.2-30.7-61.7-90-61.7-91.9zm-56.6-164.2c27.3-32.4 24.8-61.9 24-72.5-24.1 1.4-52 16.4-67.9 34.9-17.5 19.8-27.8 44.3-25.6 71.9 26.1 2 49.9-11.4 69.5-34.3z"/></svg>'


def chart_svg(points, axis_label):
    w, h = 500, 170
    xs = [60 + i * ((w - 120) / (len(points) - 1)) for i in range(len(points))]
    ys = [140 - (v / 100) * 120 for _, v in points]
    poly = " ".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))
    circles = "".join(f'<circle class="pt" cx="{x:.1f}" cy="{y:.1f}" r="5"></circle>' for x, y in zip(xs, ys))
    val_labels = "".join(
        f'<text class="pt-label" x="{x:.1f}" y="{y-14:.1f}" text-anchor="middle">{v}%</text>'
        for x, y, (_, v) in zip(xs, ys, points)
    )
    x_labels = "".join(
        f'<text class="x-label" x="{x:.1f}" y="163" text-anchor="middle">{label}</text>'
        for x, (label, _) in zip(xs, points)
    )
    return (f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{axis_label}">'
            f'<polyline class="curve" points="{poly}"></polyline>{circles}{val_labels}{x_labels}</svg>')


def render(key):
    loc = LOCALES[key]
    rel = "../" if loc["dir"] else ""
    font_override = f'<style>body{{font-family:-apple-system,BlinkMacSystemFont,{loc["font"]},"Segoe UI",sans-serif}}</style>' if loc["font"] else ""

    chips = "".join(
        f'<div class="chip c{i+1}"><span class="g">{g}</span>{label}</div>'
        for i, (g, label) in enumerate(loc["chips"])
    )
    marquee = "".join(f"<span>{m}</span>" for m in loc["marquee"] * 2)

    steps = "".join(
        f'<div class="step"><span class="n">0{i+1}</span><span class="tag">STEP 0{i+1}</span><h3>{h}</h3><p>{p}</p></div>'
        for i, (h, p) in enumerate(loc["steps"])
    )

    d = loc["demo"]
    demo_stats = "".join(
        f'<div class="stat"><b>{val}</b><span>{lbl}</span></div>'
        for lbl, val in zip(d["stat_labels"], d["stat_values"])
    )
    ai_paras = "".join(f"<p>{line}</p>" for line in d["ai_lines"])

    notes = "".join(
        f'<div class="note-card n{i+1}"><span class="tag">{tag}</span>{txt}</div>'
        for i, (tag, txt) in enumerate(loc["notes"])
    )
    chart = chart_svg(loc["chart_points"], loc["value_axis"])

    cal_grid = "".join(f'<span class="{c}"></span>' for c in CAL_CELLS)
    cal_list = "".join(
        f'<div class="row2"><span class="d">{date}</span><span class="k">{dist}</span><span>{pace}</span></div>'
        for date, dist, pace in loc["cal_list"]
    )

    zone_bar = "".join(f'<span class="z{i+1}" style="width:{w}%"></span>' for i, w in enumerate(ZONE_WIDTHS))
    zone_legend = "".join(f'<span><i class="z{i+1}"></i>{z}</span>' for i, z in enumerate(loc["zone_legend"]))
    splits = "".join(
        f'<div class="split-row"><span class="km">{lbl}</span><span class="bar" style="width:{split_bar_width(sec)}%"></span><span class="pace">{sec_to_pace(sec)}</span></div>'
        for lbl, sec in zip(SPLIT_LABELS, SPLIT_SECONDS)
    )

    coach_mock_paras = "".join(f"<p>{line}</p>" for line in loc["coach_mock_lines"])

    feats = "".join(f'<div class="feat"><h3>{h}</h3><p>{p}</p></div>' for h, p in loc["feats"])

    shots = "".join(
        f'<figure class="shot-card">'
        f'<img src="{rel}assets/shot-{key}-{i:02d}.png" alt="{cap}" loading="lazy" width="294" height="640">'
        f'<figcaption>{cap}</figcaption></figure>'
        for i, cap in enumerate(loc["shots_caps"], start=1)
    )

    demo_note_json = repr(d["note"])

    html = f"""<!doctype html>
<html lang="{loc['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{loc['title']}</title>
<meta name="description" content="{loc['desc']}">
<meta property="og:title" content="{loc['og_title']}">
<meta property="og:description" content="{loc['og_desc']}">
<meta property="og:image" content="{BASE_URL}assets/icon-512.png">
<meta property="og:type" content="website">
<link rel="canonical" href="{BASE_URL}{loc['dir']}">
{hreflang_block()}
<link rel="icon" type="image/png" sizes="32x32" href="{rel}assets/icon-32.png">
<link rel="apple-touch-icon" href="{rel}assets/icon-180.png">
<link rel="stylesheet" href="{rel}assets/style.css">
{font_override}
</head>
<body>

<nav>
  <div class="wrap">
    <a class="wordmark" href="{rel if rel else './'}"><span class="mark">RN.</span><span>RUN·NOTE</span></a>
    <div class="lang">{lang_nav(loc['dir'], rel)}</div>
  </div>
</nav>

<header class="hero">
  <div class="ghost">RN</div>
  <div class="wrap">
    <div>
      <div class="kicker"><span>RUN · NOTE</span><span class="rule"></span><span class="num">{loc['kicker_num']}</span></div>
      <h1>{loc['h1']}</h1>
      <p class="sub">{loc['sub']}</p>
      <div class="cta">
        {badge(loc, 'storeLink')}
        <span class="note">{loc['note']}</span>
      </div>
    </div>
    <div class="phone-col">
      {chips}
      <div class="phone">
        <div class="screen">
          <div class="demo-screen">
            <div class="run-card" id="demoRun"><div class="stats">{demo_stats}</div></div>
            <div class="retro-card" id="demoRetro"><span class="mood">{d['mood']}</span><div class="txt" id="demoRetroTxt"></div></div>
            <div class="coach-block" id="demoCoach"><div class="lbl">{d['ai_label']}</div>{ai_paras}</div>
          </div>
        </div>
        <div class="island"></div>
      </div>
    </div>
  </div>
</header>

<div class="marquee" aria-hidden="true"><div class="track">{marquee}</div></div>

<section>
  <div class="wrap">
    <div class="kicker"><span>{loc['how_kicker']}</span><span class="rule"></span><span class="num">{loc['how_num']}</span></div>
    <h2>{loc['how_h2']}</h2>
    <div class="steps">{steps}</div>
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap">
    <div class="kicker"><span>{loc['value_kicker']}</span><span class="rule"></span><span class="num">{loc['value_num']}</span></div>
    <h2>{loc['value_h2']}</h2>
    <p class="lede">{loc['value_lede']}</p>
    <div class="value-wrap">
      <div class="value-chart">
        {chart}
        <div class="value-legend"><span>{loc['value_axis']}</span></div>
      </div>
      <div class="note-stack">{notes}</div>
    </div>
  </div>
</section>

<section class="shots">
  <div class="wrap">
    <div class="kicker"><span>{loc['shots_kicker']}</span><span class="rule"></span><span class="num">{loc['shots_num']}</span></div>
    <h2>{loc['shots_h2']}</h2>
    <div class="row row-4">{shots}</div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="kicker"><span>{loc['feat_kicker']}</span><span class="rule"></span><span class="num">{loc['feat_num']}</span></div>
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

<footer>
  <div class="wrap">
    <div class="brand"><span class="mark">RN.</span><strong>kkiruk studio</strong></div>
    <div class="links">
      <a href="mailto:kkirukstudio.help@gmail.com">{loc['f_contact']}</a>
      <a href="https://kkiruk-studio.github.io/privacy-policy-app/">{loc['f_privacy']}</a>
      <a href="https://kkiruk-studio.github.io/terms-of-service-app/">{loc['f_terms']}</a>
    </div>
    <div>© 2026 kkiruk studio</div>
  </div>
</footer>

<script>
  // After App Store approval, set the real URL here (e.g. https://apps.apple.com/app/id1234567890)
  const APP_STORE_URL = "{APP_STORE_URL}";
  document.querySelectorAll(".store-badge").forEach((el) => {{
    if (APP_STORE_URL) {{
      el.href = APP_STORE_URL;
    }} else {{
      el.classList.add("disabled");
      el.removeAttribute("href");
      el.setAttribute("aria-disabled", "true");
      const txt = el.querySelector(".txt");
      if (txt) txt.innerHTML = "<strong>{loc['badge_soon']}</strong>";
    }}
  }});

  (function () {{
    const runCard = document.getElementById("demoRun");
    const retroCard = document.getElementById("demoRetro");
    const retroTxt = document.getElementById("demoRetroTxt");
    const coachBlock = document.getElementById("demoCoach");
    const note = {demo_note_json};
    const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    if (reduced) {{
      runCard.classList.add("show");
      retroCard.classList.add("show", "done");
      retroTxt.textContent = note;
      coachBlock.classList.add("show");
      return;
    }}

    const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
    (async function loop() {{
      for (;;) {{
        runCard.classList.remove("show");
        retroCard.classList.remove("show", "done");
        coachBlock.classList.remove("show");
        retroTxt.textContent = "";
        await sleep(500);
        runCard.classList.add("show");
        await sleep(900);
        retroCard.classList.add("show");
        await sleep(300);
        for (const ch of note) {{
          retroTxt.textContent += ch;
          await sleep(45);
        }}
        retroCard.classList.add("done");
        await sleep(700);
        coachBlock.classList.add("show");
        await sleep(4200);
      }}
    }})();
  }})();
</script>
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
