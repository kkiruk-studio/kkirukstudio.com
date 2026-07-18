#!/usr/bin/env python3
"""Generate index.html for every locale from one template (poster theme).

Usage: python3 build.py
Output: ./index.html (ko, root), ./en/index.html, ./ja/index.html, ./zh/index.html

Root = Korean (kkiruk studio's primary market for RunNote). Do not hand-edit
the generated HTML files -- edit this file and re-run `python3 build.py`.

Design source of truth: drafts/poster.html (7-poster editorial layout).
"""
import pathlib

ROOT = pathlib.Path(__file__).parent
BASE_URL = "https://www.kkirukstudio.com/runnote/"
APP_STORE_URL = ""  # fill in after App Store approval, e.g. https://apps.apple.com/app/id0000000000

LANG_LABELS = [("", "한국어"), ("en/", "EN"), ("ja/", "日本語"), ("zh/", "繁體")]

LOCALES = {
    "ko": {
        "dir": "", "lang": "ko", "font": '"Apple SD Gothic Neo", "Pretendard"', "keep_all": True,
        "title": "RunNote — 러닝 후 한 줄 노트로 완성되는 AI 코칭",
        "desc": "실시간 트래킹이 아닌 노트 기반 러닝 기록장. 워치로 뛰고 컨디션과 한 줄만 남기면, 기록이 쌓일수록 AI 코칭이 정교해집니다.",
        "og_title": "RunNote — 나를 아는 AI 러닝 코치",
        "og_desc": "한 줄 노트가 쌓일수록 정교해지는 AI 코칭.",
        "badge_soon": "곧 App Store에서",
        "p1_meta": ["RUN·NOTE", "AI Running Journal", "iPhone · Watch"],
        "p1_h1": ["뛰고 나서,", "<em>한 줄.</em>"],
        "p1_lede": "실시간 트래킹 아님 — 기록은 자동, 당신은 한 줄만",
        "p2_note_value": "한 줄이면 끝",
        "p3_h2": ["기록이 쌓일수록,", "<em>코치는 당신을 외웁니다.</em>"],
        "p3_lede": "궁금한 건 물어보고, 부족한 건 다음 러닝에서 보완하고 —<br>그렇게 러닝은 점점 더 즐거워집니다.",
        "p3_notes": [
            ["RUN 01", '"왜 오르막만 오면 숨이 찰까?" — 물어보세요. 코치가 답합니다.'],
            ["RUN 10", "오르막에서 페이스가 무너지는 패턴 — 다음 러닝은 케이던스로 보완해요."],
            ["RUN 20", "오르막 페이스 유지 성공. 뛸수록 나아지고, 나아질수록 즐거워집니다."],
        ],
        "p3b_meta2": "매 러닝이 다음 러닝을 만듭니다",
        "p3b_steps": [
            ["뛴다.", "워치가 알아서 기록합니다"],
            ["적는다.", "컨디션·통증·기분, 딱 한 줄"],
            ["배운다.", "코치가 부족한 부분을 짚어줍니다"],
            ["다시 뛴다.", "이번엔 보완해서 — 그래서 더 즐겁게"],
        ],
        "p3b_loopmark": "그리고 다시 01로 — 반복할수록 코치는 정확해집니다",
        "p3c_h2": ["궁금한 건", "<em>코치에게 물어보세요.</em>"],
        "p3c_qs": [
            ['"왜 5km만 넘으면 페이스가 떨어질까?"', "당신의 심박·케이던스 기록을 근거로 답합니다"],
            ['"무릎이 좀 아픈데, 내일 뛰어도 돼?"', "통증 노트 3주 치를 기억하고 있는 코치의 답은 다릅니다"],
            ['"장마철엔 어떻게 뛰어야 해?"', "날씨는 자동 기록 — 빗속 러닝 데이터도 코칭 재료가 됩니다"],
            ['"다음 목표는 뭘로 잡을까?"', "지금 실력에서 반 발짝 앞 — 부담 없는 다음 목표를 제안합니다"],
        ],
        "p4_idx": ["HealthKit 자동 동기화", "한 줄 노트 · 통증 부위", "심박 5구간 · 케이던스", "AI 코치", "코치 노트 — 장기 기억", "날씨 자동 기록"],
        "p5_h2": ["오늘 뛰었다면,", "<em>한 줄 남기세요.</em>"],
        "p5_note": "7-Day Free Trial · iPhone &amp; Apple Watch",
        "f_contact": "문의", "f_privacy": "개인정보 처리방침", "f_terms": "이용약관",
    },
    "en": {
        "dir": "en/", "lang": "en", "font": None, "keep_all": False,
        "title": "RunNote — A one-line running journal with AI coaching that knows you",
        "desc": "Not a live-tracking app. Run with your Watch, log one line about how you felt, and the AI coaching gets sharper with every entry.",
        "og_title": "RunNote — An AI running coach that learns you",
        "og_desc": "Coaching that gets sharper with every one-line note.",
        "badge_soon": "Coming soon",
        "p1_meta": ["RUN·NOTE", "AI Running Journal", "iPhone · Watch"],
        "p1_h1": ["Run first,", "<em>then one line.</em>"],
        "p1_lede": "Not live tracking — logging is automatic, you write one line",
        "p2_note_value": "One line, done",
        "p3_h2": ["The more you log,", "<em>the more your coach knows you.</em>"],
        "p3_lede": "Ask what you're curious about, fix what's missing next run —<br>and running keeps getting more fun.",
        "p3_notes": [
            ["RUN 01", '"Why do I lose my breath on every climb?" — just ask. The coach answers.'],
            ["RUN 10", "Pace fades on climbs, same pattern — next run, fix it with cadence."],
            ["RUN 20", "Pace held on the climb. The more you run, the better it gets — and the more fun."],
        ],
        "p3b_meta2": "Every run shapes the next one",
        "p3b_steps": [
            ["Run.", "Your Watch logs it automatically"],
            ["Write.", "Condition, soreness, mood — one line"],
            ["Learn.", "The coach points out what's missing"],
            ["Run again.", "This time, fixed — so it's more fun"],
        ],
        "p3b_loopmark": "Then back to 01 — the more you repeat it, the sharper the coach gets",
        "p3c_h2": ["Curious about", "<em>something? Ask your coach.</em>"],
        "p3c_qs": [
            ['"Why does my pace drop after 5km?"', "Answered from your own heart rate and cadence data"],
            ['"My knee hurts a bit — okay to run tomorrow?"', "A coach that remembers 3 weeks of pain notes answers differently"],
            ['"How should I run in the rainy season?"', "Weather is logged automatically — even rainy runs become coaching material"],
            ['"What should my next goal be?"', "Half a step beyond where you are now — no-pressure next goals"],
        ],
        "p4_idx": ["HealthKit auto-sync", "One-line notes · pain areas", "5 HR zones · cadence", "AI coach", "Coach notes — long-term memory", "Weather, logged automatically"],
        "p5_h2": ["If you ran today,", "<em>leave one line.</em>"],
        "p5_note": "7-Day Free Trial · iPhone &amp; Apple Watch",
        "f_contact": "Contact", "f_privacy": "Privacy", "f_terms": "Terms",
    },
    "ja": {
        "dir": "ja/", "lang": "ja", "font": '"Hiragino Kaku Gothic ProN", "Hiragino Sans", "Yu Gothic"', "keep_all": False,
        "title": "RunNote — ひと言のノートで磨かれるAIランニングコーチ",
        "desc": "リアルタイムトラッキングではなく、ノート型のランニング記録アプリ。Apple Watchで走ってひと言残すだけで、AIコーチングが記録とともに的確になります。",
        "og_title": "RunNote — あなたを知るAIランニングコーチ",
        "og_desc": "ひと言のノートが積み重なるほど的確になるコーチング。",
        "badge_soon": "近日公開",
        "p1_meta": ["RUN·NOTE", "AI Running Journal", "iPhone · Watch"],
        "p1_h1": ["走って、", "<em>ひと言。</em>"],
        "p1_lede": "リアルタイム計測ではありません — 記録は自動、あなたはひと言だけ",
        "p2_note_value": "ひと言で完了",
        "p3_h2": ["記録が増えるほど、", "<em>コーチはあなたを覚えます。</em>"],
        "p3_lede": "気になることは聞いて、足りない部分は次のランで補う —<br>そうやってランニングはどんどん楽しくなります。",
        "p3_notes": [
            ["RUN 01", "「なぜ坂道だけで息が上がるんだろう?」— 聞いてみてください。コーチが答えます。"],
            ["RUN 10", "坂道でペースが崩れる傾向 — 次のランはケイデンスで補いましょう。"],
            ["RUN 20", "坂道ペース維持に成功。走るほど良くなり、良くなるほど楽しくなります。"],
        ],
        "p3b_meta2": "毎回のランが次のランを作ります",
        "p3b_steps": [
            ["走る。", "Watchが自動で記録します"],
            ["書く。", "体調・痛み・気分をひと言で"],
            ["学ぶ。", "コーチが足りない部分を指摘します"],
            ["また走る。", "今度は補って — もっと楽しく"],
        ],
        "p3b_loopmark": "そしてまた01へ — 繰り返すほどコーチは正確になります",
        "p3c_h2": ["気になることは", "<em>コーチに聞いてみましょう。</em>"],
        "p3c_qs": [
            ["「5kmを超えるとなぜペースが落ちるの?」", "あなたの心拍・ケイデンス記録をもとに答えます"],
            ["「膝が少し痛いけど、明日走ってもいい?」", "3週間分の痛みノートを覚えているコーチの答えは違います"],
            ["「梅雨の時期はどう走ればいい?」", "天気は自動記録 — 雨の日のランもコーチングの材料に"],
            ["「次の目標は何にしよう?」", "今の実力から半歩先 — 無理のない次の目標を提案します"],
        ],
        "p4_idx": ["HealthKit自動連携", "ひと言ノート・痛みの部位", "心拍5ゾーン・ケイデンス", "AIコーチ", "コーチノート — 長期記憶", "天気の自動記録"],
        "p5_h2": ["今日走ったなら、", "<em>ひと言残しましょう。</em>"],
        "p5_note": "7日間無料トライアル · iPhone &amp; Apple Watch",
        "f_contact": "お問い合わせ", "f_privacy": "プライバシーポリシー", "f_terms": "利用規約",
    },
    "zh": {
        "dir": "zh/", "lang": "zh-Hant", "font": '"PingFang TC", "Microsoft JhengHei"', "keep_all": False,
        "title": "RunNote — 用一句跑後筆記,打造懂你的 AI 教練",
        "desc": "不是即時追蹤,而是以筆記為核心的跑步紀錄。用手錶跑完,只需留下狀態和一句話,記錄越多,AI 教練就越精準。",
        "og_title": "RunNote — 懂你的 AI 跑步教練",
        "og_desc": "一句筆記累積越多,教練建議越精準。",
        "badge_soon": "即將推出",
        "p1_meta": ["RUN·NOTE", "AI Running Journal", "iPhone · Watch"],
        "p1_h1": ["跑完之後,", "<em>寫一句。</em>"],
        "p1_lede": "不是即時追蹤 — 記錄自動完成,你只需寫一句話",
        "p2_note_value": "一句話就好",
        "p3_h2": ["記錄越多,", "<em>教練就越了解你。</em>"],
        "p3_lede": "有疑問就問,不足的下次跑步再補強 ——<br>跑步也就越來越有趣。",
        "p3_notes": [
            ["RUN 01", "「為什麼一到上坡就喘不過氣?」— 問問看,教練會回答。"],
            ["RUN 10", "上坡配速崩潰的模式 — 下次跑步用步頻來補強。"],
            ["RUN 20", "成功維持上坡配速。跑得越多越進步,越進步就越有趣。"],
        ],
        "p3b_meta2": "每一次跑步,都造就下一次",
        "p3b_steps": [
            ["跑步。", "手錶自動幫你記錄"],
            ["寫下。", "狀態、疼痛、心情,一句就好"],
            ["學習。", "教練點出不足之處"],
            ["再跑一次。", "這次補強了 — 更有趣"],
        ],
        "p3b_loopmark": "然後回到01 — 重複越多次,教練就越精準",
        "p3c_h2": ["有疑問就", "<em>問教練吧。</em>"],
        "p3c_qs": [
            ["「為什麼一超過5km配速就掉?」", "根據你的心率、步頻記錄回答"],
            ["「膝蓋有點痛,明天可以跑嗎?」", "記得3週疼痛筆記的教練,答案不一樣"],
            ["「梅雨季該怎麼跑?」", "天氣自動記錄 — 雨中跑步的數據也是教練素材"],
            ["「下一個目標該設多少?」", "從目前實力再進半步 — 提出沒有壓力的下一個目標"],
        ],
        "p4_idx": ["HealthKit 自動同步", "一句筆記 · 疼痛部位", "心率5區間 · 步頻", "AI 教練", "教練筆記 — 長期記憶", "天氣自動記錄"],
        "p5_h2": ["今天跑了嗎?", "<em>留下一句話。</em>"],
        "p5_note": "7 天免費試用 · iPhone &amp; Apple Watch",
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


APPLE_SVG = '<svg viewBox="0 0 384 512" aria-hidden="true"><path d="M318.7 268.7c-.2-36.7 16.4-64.4 50-84.8-18.8-26.9-47.2-41.7-84.7-44.6-35.5-2.8-74.3 20.7-88.5 20.7-15 0-49.4-19.7-76.4-19.7C63.3 141.2 4 184.8 4 273.5q0 39.3 14.4 81.2c12.8 36.7 59 126.7 107.2 125.2 25.2-.6 43-17.9 75.8-17.9 31.8 0 48.3 17.9 76.4 17.9 48.6-.7 90.4-82.5 102.6-119.3-65.2-30.7-61.7-90-61.7-91.9zm-56.6-164.2c27.3-32.4 24.8-61.9 24-72.5-24.1 1.4-52 16.4-67.9 34.9-17.5 19.8-27.8 44.3-25.6 71.9 26.1 2 49.9-11.4 69.5-34.3z"/></svg>'

POSTER_CSS = """
:root{
  --cols:12; --gutter:24px; --margin:64px; --baseline:8px;
  --accent:#1E9B52; --ink:#141414; --paper:#F4F1E8; --paper2:#ECE8DB;
}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  background:var(--paper); color:var(--ink);
  font:16px/24px "Helvetica Neue", Helvetica, "Apple SD Gothic Neo", Pretendard, sans-serif;
  -webkit-font-smoothing:antialiased;
}
.grid{
  display:grid; grid-template-columns:repeat(var(--cols),1fr);
  column-gap:var(--gutter); max-width:1240px; margin-inline:auto;
  padding-inline:var(--margin); position:relative;
}

/* ── 포스터 공통 ── */
.poster{min-height:100vh;display:flex;flex-direction:column;justify-content:center;
  padding-block:96px;position:relative;overflow:hidden;border-bottom:2px solid var(--ink)}
.meta{font-size:15px;line-height:24px;letter-spacing:.12em;font-weight:700;text-transform:uppercase}
.rule{height:8px;background:var(--accent)}
.mono{font-family:"SF Mono", ui-monospace, Menlo, monospace}

/* 언어 스위처 */
.langnav{position:absolute;top:24px;right:64px;z-index:5;display:flex;gap:16px}
.langnav a{font-size:13px;letter-spacing:.08em;font-weight:700;color:#00000088;text-decoration:none}
.langnav a.cur{color:var(--ink);text-decoration:underline}

/* P1 표지 */
.p1 h1{font-size:clamp(64px,10vw,152px);line-height:.96;font-weight:800;letter-spacing:-.03em}
.p1 h1 em{font-style:normal;color:var(--accent)}
.p1 .top{grid-column:1/-1;display:flex;justify-content:space-between;margin-bottom:120px;flex-wrap:wrap;gap:8px}
.p1 .h1w{grid-column:1/12}
.p1 .foot{grid-column:1/-1;display:flex;justify-content:space-between;align-items:flex-end;margin-top:120px;flex-wrap:wrap;gap:16px}
.p1 .foot .rule{width:200px}
.p1 .lede-meta{font-size:18px;letter-spacing:.04em;text-transform:none;font-weight:700}
.p1 .side{position:absolute;right:28px;top:50%;transform:rotate(90deg) translateX(-50%);transform-origin:right top;
  font-size:14px;letter-spacing:.3em;font-weight:700;color:#00000055}

/* P2 숫자 */
.p2{background:var(--accent);color:#fff;border-bottom:none}
.p2 .big{grid-column:1/-1;font-weight:800;letter-spacing:-.04em;
  font-size:clamp(120px,24vw,340px);line-height:.9}
.p2 .big small{font-size:.22em;font-weight:700;letter-spacing:0;vertical-align:.16em;margin-left:8px}
.p2 .stats{grid-column:1/-1;display:grid;grid-template-columns:subgrid;margin-top:64px;
  border-top:2px solid #ffffff66;padding-top:24px}
.p2 .stat{grid-column:span 3}
.p2 .stat b{display:block;font-size:40px;line-height:48px;font-weight:800}
.p2 .stat span{font-size:15px;letter-spacing:.12em;font-weight:700;opacity:.8}
.p2 .contour{position:absolute;inset:0;opacity:.12;pointer-events:none}
.p2 .meta-row{grid-column:1/-1;display:flex;justify-content:space-between;margin-bottom:56px}

/* P3 코치 */
.p3 .h2w{grid-column:1/9}
.p3 h2{font-size:clamp(40px,6.4vw,88px);line-height:1.04;font-weight:800;letter-spacing:-.02em}
.p3 h2 em{font-style:normal;background:linear-gradient(transparent 62%, color-mix(in srgb,var(--accent) 38%, transparent) 62%)}
.p3 .lede{grid-column:1/8;font-size:19px;line-height:32px;font-weight:600;color:#000000B3;margin-top:8px}
.p3 .notes{grid-column:1/-1;margin-top:80px;display:grid;grid-template-columns:subgrid}
.p3 .note{grid-column:span 4;border-top:2px solid var(--ink);padding-top:16px}
.p3 .note .meta{color:var(--accent)}
.p3 .note p{margin-top:16px;font-size:20px;line-height:32px;font-weight:700}
.p3 .note:nth-child(1) p{opacity:.35}
.p3 .note:nth-child(2) p{opacity:.7}

/* P3B 루프 */
.p3b{background:var(--paper2)}
.p3b .metah{grid-column:1/-1;display:flex;justify-content:space-between;margin-bottom:88px;flex-wrap:wrap;gap:8px}
.p3b .loop{grid-column:1/-1}
.p3b .step{display:flex;align-items:baseline;gap:32px;border-top:2px solid var(--ink);padding:24px 0;
  font-size:clamp(32px,5.6vw,76px);line-height:1.05;font-weight:800;letter-spacing:-.02em}
.p3b .step .no{font-family:"SF Mono",ui-monospace,monospace;font-size:16px;font-weight:700;color:var(--accent)}
.p3b .step .sub{margin-left:auto;font-size:17px;line-height:26px;font-weight:600;color:#00000099;letter-spacing:0;max-width:320px;text-align:right}
.p3b .step:last-child{border-bottom:2px solid var(--ink)}
.p3b .step:last-child strong{color:var(--accent)}
.p3b .loopmark{grid-column:1/-1;margin-top:48px;display:flex;align-items:center;gap:16px}
.p3b .loopmark svg{width:40px;height:40px;flex:none}
.p3b .loopmark .meta{color:#00000099}

/* P3C 질문 */
.p3c .h2w{grid-column:1/-1;margin-bottom:72px}
.p3c h2{font-size:clamp(40px,6.4vw,88px);line-height:1.04;font-weight:800;letter-spacing:-.02em}
.p3c h2 em{font-style:normal;color:var(--accent)}
.p3c .qs{grid-column:1/-1;display:grid;grid-template-columns:subgrid;row-gap:40px}
.p3c .q{grid-column:span 6;border-left:8px solid var(--accent);padding-left:24px}
.p3c .q p{font-size:clamp(22px,2.6vw,34px);line-height:1.3;font-weight:800;letter-spacing:-.01em}
.p3c .q span{display:block;margin-top:12px;font-size:17px;line-height:26px;font-weight:600;color:#00000099}

/* P4 인덱스 + 실물 */
.p4 .idx{grid-column:1/7}
.p4 .idx h3{font-size:15px;letter-spacing:.12em;font-weight:700;color:var(--accent);margin-bottom:40px}
.p4 ol{list-style:none;counter-reset:n}
.p4 li{counter-increment:n;display:flex;gap:24px;align-items:baseline;
  border-top:1px solid #00000033;padding:16px 0;font-size:26px;line-height:38px;font-weight:800;letter-spacing:-.01em}
.p4 li::before{content:counter(n,decimal-leading-zero);font-size:14px;font-weight:700;color:var(--accent);
  font-family:"SF Mono",ui-monospace,monospace}
.p4 .shot{grid-column:8/13;align-self:center}
.p4 .shot img{width:100%;border-radius:24px;box-shadow:0 32px 64px -24px #00000040}
.p4 .shot figcaption{margin-top:16px;font-size:14px;letter-spacing:.12em;font-weight:700;color:#00000088}

/* P5 CTA */
.p5{background:var(--ink);color:var(--paper);border-bottom:none;min-height:80vh}
.p5 .h2w{grid-column:1/-1}
.p5 h2{font-size:clamp(56px,10vw,136px);line-height:.98;font-weight:800;letter-spacing:-.03em}
.p5 h2 em{font-style:normal;color:var(--accent)}
.p5 .foot{grid-column:1/-1;display:flex;justify-content:space-between;align-items:center;margin-top:96px;flex-wrap:wrap;gap:16px}
.p5 .btn{display:inline-block;border:2px solid var(--paper);border-radius:999px;
  padding:16px 40px;color:var(--paper);text-decoration:none;font-weight:800;font-size:16px}
.p5 .btn:hover{background:var(--accent);border-color:var(--accent)}
.p5 .btn.disabled{cursor:default}
.p5 .langnav a{color:#ffffff88}
.p5 .langnav a.cur{color:var(--paper)}

/* ── 배경 패턴 (러닝 포스터) ── */
.bg{position:absolute;inset:0;pointer-events:none}
.p1 .bg path{stroke:var(--ink);opacity:.13}
.p1 .bg .pin{fill:var(--accent);opacity:.9}
.p3b .bg{opacity:.1}
.p3b .bg path{stroke:var(--ink)}
.p3c .bg{right:-4%;left:auto;width:46%;opacity:.07;display:flex;align-items:center;justify-content:flex-end}
.p3c .bg span{font-size:clamp(400px,44vw,640px);font-weight:800;line-height:1;color:var(--ink)}
.p5 .bg{opacity:.14}
.p5 .bg path{stroke:var(--paper)}

/* ── 모션 ── */
.io{opacity:0;transform:translateY(24px);transition:opacity .7s ease,transform .7s cubic-bezier(.2,.7,.2,1)}
.io.in{opacity:1;transform:none}
.io.d1{transition-delay:.12s}.io.d2{transition-delay:.24s}.io.d3{transition-delay:.36s}
.io.d4{transition-delay:.48s}.io.d5{transition-delay:.6s}.io.d6{transition-delay:.72s}
.p1 h1 .line{display:block;overflow:hidden}
.p1 h1 .line span{display:inline-block;transform:translateY(110%);transition:transform .8s cubic-bezier(.2,.7,.2,1)}
.p1.in h1 .line:nth-child(1) span{transform:none;transition-delay:.1s}
.p1.in h1 .line:nth-child(2) span{transform:none;transition-delay:.28s}
.p1 .rule{transform-origin:left;transform:scaleX(0);transition:transform .9s cubic-bezier(.2,.7,.2,1) .6s}
.p1.in .rule{transform:scaleX(1)}
.p2 .contour path{stroke-dasharray:1600;stroke-dashoffset:1600;transition:stroke-dashoffset 2.4s ease}
.p2.in .contour path{stroke-dashoffset:0}
.p2.in .contour path:nth-child(2){transition-delay:.15s}
.p2.in .contour path:nth-child(3){transition-delay:.3s}
.p2.in .contour path:nth-child(4){transition-delay:.45s}
.p2.in .contour path:nth-child(5){transition-delay:.6s}
.p2 .big{clip-path:inset(0 100% 0 0);transition:clip-path 1s cubic-bezier(.2,.7,.2,1) .2s}
.p2.in .big{clip-path:inset(0 0 0 0)}
.p3 h2 em{background-size:0% 100%;background-repeat:no-repeat;transition:background-size .9s ease .5s}
.p3.in h2 em{background-size:100% 100%}
.p5 h2 em{position:relative}
@media (prefers-reduced-motion: reduce){
  .io,.p1 h1 .line span,.p1 .rule,.p2 .big,.p2 .contour path,.p3 h2 em{transition:none!important;transform:none!important;opacity:1!important;clip-path:none!important;stroke-dashoffset:0!important;background-size:100% 100%!important}
}

@media (max-width:760px){
  :root{--margin:24px;--gutter:16px}
  .langnav{position:static;justify-content:flex-end;margin-bottom:16px}
  .p1 .h1w{grid-column:1/-1}
  .p2 .stat{grid-column:span 6;margin-bottom:24px}
  .p3 .h2w{grid-column:1/-1}
  .p3 .lede{grid-column:1/-1}
  .p3 .note{grid-column:1/-1;margin-bottom:24px}
  .p3b .step{flex-wrap:wrap;gap:12px}
  .p3b .step .sub{margin-left:0;text-align:left;max-width:none;flex-basis:100%}
  .p3c .q{grid-column:1/-1}
  .p4 .idx{grid-column:1/-1}
  .p4 .shot{grid-column:1/-1;margin-top:48px}
}
"""


def render(key):
    loc = LOCALES[key]
    rel = "../" if loc["dir"] else ""
    font_override = f'<style>body{{font-family:-apple-system,BlinkMacSystemFont,{loc["font"]},"Segoe UI",sans-serif}}</style>' if loc["font"] else ""
    word_break = "word-break:keep-all;" if loc.get("keep_all") else ""

    notes_html = "".join(
        f'<div class="note io d{i*2+1}"><span class="meta">{tag}</span><p>{txt}</p></div>'
        for i, (tag, txt) in enumerate(loc["p3_notes"])
    )
    steps_html = "".join(
        f'<div class="step io d{i+1}"><span class="no">0{i+1}</span><strong>{h}</strong><span class="sub">{sub}</span></div>'
        for i, (h, sub) in enumerate(loc["p3b_steps"])
    )
    qs_html = "".join(
        f'<div class="q io d{i+1}"><p>{p}</p><span>{s}</span></div>'
        for i, (p, s) in enumerate(loc["p3c_qs"])
    )
    idx_html = "".join(
        f'<li class="io d{i+1}">{item}</li>' for i, item in enumerate(loc["p4_idx"])
    )

    lang_nav_html = f'<div class="langnav">{lang_nav(loc["dir"], rel)}</div>'
    btn_href = APP_STORE_URL if APP_STORE_URL else "#"

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
<style>
{POSTER_CSS}
body{{{word_break}}}
</style>
{font_override}
</head>
<body>

<!-- P1 · 표지 포스터 -->
<section class="poster p1">
  {lang_nav_html}
  <svg class="bg" viewBox="0 0 1440 900" preserveAspectRatio="xMidYMid slice" fill="none">
    <path class="route" d="M-40 780 C 220 700, 300 830, 520 760 S 820 560, 960 480 S 1180 300, 1300 180 S 1420 80, 1480 40"
      stroke-width="3" stroke-dasharray="2 14" stroke-linecap="round"/>
    <circle class="pin" cx="1300" cy="180" r="7"/>
  </svg>
  <div class="grid">
    <div class="top">
      <span class="meta io">{loc['p1_meta'][0]}</span>
      <span class="meta io d2">{loc['p1_meta'][1]}</span>
      <span class="meta io d4">{loc['p1_meta'][2]}</span>
    </div>
    <div class="h1w">
      <h1><span class="line"><span>{loc['p1_h1'][0]}</span></span><span class="line"><span>{loc['p1_h1'][1]}</span></span></h1>
    </div>
    <div class="foot">
      <div class="rule"></div>
      <span class="meta lede-meta io d3">{loc['p1_lede']}</span>
    </div>
  </div>
  <span class="side">RUNNING POSTER SERIES — 01</span>
</section>

<!-- P2 · 숫자 포스터 -->
<section class="poster p2">
  <svg class="contour" viewBox="0 0 1200 800" preserveAspectRatio="xMidYMid slice">
    <g fill="none" stroke="#fff" stroke-width="1.5">
      <path d="M-50 640 C 200 560, 340 700, 620 620 S 1000 500, 1260 590"/>
      <path d="M-50 560 C 180 470, 380 620, 640 540 S 980 420, 1260 500"/>
      <path d="M-50 480 C 160 390, 420 540, 660 460 S 960 340, 1260 410"/>
      <path d="M-50 400 C 140 310, 460 460, 680 380 S 940 260, 1260 320"/>
      <path d="M-50 320 C 120 230, 500 380, 700 300 S 920 180, 1260 230"/>
    </g>
  </svg>
  <div class="grid">
    <div class="meta-row io"><span class="meta">TODAY'S RUN</span><span class="meta">07 · 14 · TUE</span></div>
    <div class="big">5.00<small>KM</small></div>
    <div class="stats">
      <div class="stat io d1"><span>PACE</span><b class="mono">5'43"</b></div>
      <div class="stat io d2"><span>TIME</span><b class="mono">31:04</b></div>
      <div class="stat io d3"><span>ZONE</span><b class="mono">Z3</b></div>
      <div class="stat io d4"><span>NOTE</span><b>{loc['p2_note_value']}</b></div>
    </div>
  </div>
</section>

<!-- P3 · 코치 포스터 -->
<section class="poster p3">
  <div class="grid">
    <div class="h2w io">
      <h2>{loc['p3_h2'][0]}<br>{loc['p3_h2'][1]}</h2>
    </div>
    <p class="lede io d2">{loc['p3_lede']}</p>
    <div class="notes">
      {notes_html}
    </div>
  </div>
</section>

<!-- P3B · 루프 포스터 -->
<section class="poster p3b">
  <svg class="bg" viewBox="0 0 1440 900" preserveAspectRatio="xMidYMid slice" fill="none" stroke-width="2">
    <path d="M-60 900 C 300 620, 900 620, 1500 880"/>
    <path d="M-60 830 C 300 540, 900 540, 1500 810"/>
    <path d="M-60 760 C 300 460, 900 460, 1500 740"/>
    <path d="M-60 690 C 300 380, 900 380, 1500 670"/>
  </svg>
  <div class="grid">
    <div class="metah io"><span class="meta">THE LOOP</span><span class="meta">{loc['p3b_meta2']}</span></div>
    <div class="loop">
      {steps_html}
    </div>
    <div class="loopmark io d5">
      <svg viewBox="0 0 40 40" fill="none" stroke="var(--accent)" stroke-width="3">
        <path d="M33 20a13 13 0 1 1-4-9.4"/><path d="M29 4v7h7" stroke-linejoin="round"/>
      </svg>
      <span class="meta">{loc['p3b_loopmark']}</span>
    </div>
  </div>
</section>

<!-- P3C · 질문 포스터 -->
<section class="poster p3c">
  <div class="bg"><span>?</span></div>
  <div class="grid">
    <div class="h2w io">
      <h2>{loc['p3c_h2'][0]}<br>{loc['p3c_h2'][1]}</h2>
    </div>
    <div class="qs">
      {qs_html}
    </div>
  </div>
</section>

<!-- P4 · 인덱스 + 실물 -->
<section class="poster p4">
  <div class="grid">
    <div class="idx">
      <h3>INDEX — WHAT'S INSIDE</h3>
      <ol>
        {idx_html}
      </ol>
    </div>
    <figure class="shot io d2">
      <img src="{rel}assets/hero-{key}.png" alt="RunNote">
      <figcaption class="io d4">ACTUAL APP — NO MOCKUP</figcaption>
    </figure>
  </div>
</section>

<!-- P5 · CTA 포스터 -->
<section class="poster p5">
  {lang_nav_html}
  <svg class="bg" viewBox="0 0 1440 900" preserveAspectRatio="xMidYMid slice" fill="none" stroke-width="2">
    <path d="M-60 760 L 1500 640"/>
    <path d="M-60 810 L 1500 690"/>
    <path d="M-60 860 L 1500 740"/>
    <path d="M-60 910 L 1500 790"/>
  </svg>
  <div class="grid">
    <div class="h2w io">
      <h2>{loc['p5_h2'][0]}<br>{loc['p5_h2'][1]}</h2>
    </div>
    <div class="foot io d2">
      <a class="btn" id="storeLink" href="{btn_href}">{loc['badge_soon']}</a>
      <span class="meta io d3">{loc['p5_note']}</span>
    </div>
  </div>
</section>

<footer style="padding:48px 64px;font-size:13px;letter-spacing:.06em;color:#00000088;display:flex;justify-content:space-between;flex-wrap:wrap;gap:12px;background:var(--ink);color:#ffffff88">
  <span>© 2026 kkiruk studio</span>
  <span style="display:flex;gap:20px">
    <a href="mailto:kkirukstudio.help@gmail.com" style="color:inherit;text-decoration:none">{loc['f_contact']}</a>
    <a href="https://kkiruk-studio.github.io/privacy-policy-app/" style="color:inherit;text-decoration:none">{loc['f_privacy']}</a>
    <a href="https://kkiruk-studio.github.io/terms-of-service-app/" style="color:inherit;text-decoration:none">{loc['f_terms']}</a>
  </span>
</footer>

<script>
  const APP_STORE_URL = "{APP_STORE_URL}";
  document.querySelectorAll("#storeLink").forEach((el) => {{
    if (APP_STORE_URL) {{
      el.href = APP_STORE_URL;
    }} else {{
      el.classList.add("disabled");
      el.removeAttribute("href");
      el.setAttribute("aria-disabled", "true");
    }}
  }});
  const obs = new IntersectionObserver(es => es.forEach(e => {{
    if (e.isIntersecting) {{ e.target.classList.add('in'); obs.unobserve(e.target); }}
  }}), {{threshold: .25}});
  document.querySelectorAll('.poster').forEach(p => obs.observe(p));
  const obs2 = new IntersectionObserver(es => es.forEach(e => {{
    if (e.isIntersecting) {{ e.target.classList.add('in'); obs2.unobserve(e.target); }}
  }}), {{threshold: .3}});
  document.querySelectorAll('.io').forEach(el => obs2.observe(el));
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
