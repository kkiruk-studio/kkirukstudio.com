# Search publishing checks

Run `python3 gen/refresh_seo.py` after manual content edits and
`python3 gen/check_seo.py` before publishing. Each app's `build.py` runs the
refresh automatically. The refresh preserves body copy and only owns the
marked facts/introduction blocks and discovery metadata.

`refresh_seo.py` contains reviewed Korean/English product definitions. Other
languages use their existing localized descriptions. Keep these definitions
aligned with the actual app when its behavior changes. Prices and ratings are
not added by this pipeline. DeskBreath's richer app schema remains owned by
its builder; its platforms and store links supply the visible facts.

Measure results in the existing GA4 property: compare weekly landing sessions
with session source `chatgpt.com` (including `utm_source=chatgpt.com`), engaged
sessions, and destination pages. Compare the four weeks before and after
deployment, accounting for other releases/campaigns. More schema and a 200
response do not demonstrate more search impressions or citations.

References:
- https://help.openai.com/en/articles/12627856
- https://developers.google.com/search/docs/appearance/ai-features
