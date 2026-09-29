#!/usr/bin/env python3
"""Copy the app icon and the raw (unframed) simulator screenshots into assets/.

The page frames screenshots in its own CSS phone, so it takes the raw captures
(`fastlane/screenshots_raw/`, status bar already 9:41) rather than the framed
store images. Re-run after the screenshots are regenerated:

    python3 sync_assets.py && python3 build.py
"""
import pathlib
import subprocess

HERE = pathlib.Path(__file__).resolve().parent
APP = pathlib.Path.home() / "Taiwan Rail Log" / "TwraillogApp"
ICON = APP / "Resources/Assets.xcassets/AppIcon.appiconset/icon-1024.png"
RAW = APP / "fastlane/screenshots_raw"

# page locale dir → screenshot locale prefix
LOCALES = {"zh-hant": "zh-Hant", "en": "en", "ja": "ja", "ko": "ko"}
SHOTS = ["1-map", "2-flyover", "4-stamps"]


def sips(src, dst, size, jpeg=False):
    dst.parent.mkdir(parents=True, exist_ok=True)
    fmt = ["-s", "format", "jpeg", "-s", "formatOptions", "82"] if jpeg else []
    subprocess.run(["sips", "-Z", str(size), *fmt, str(src), "--out", str(dst)],
                   check=True, capture_output=True)


def main():
    assets = HERE / "assets"
    sips(ICON, assets / "icon-180.png", 180)
    sips(ICON, assets / "icon-512.png", 512)
    for d, prefix in LOCALES.items():
        for s in SHOTS:
            # 1320x2868 → 600x1304. JPEG: the satellite / map captures are ~1 MB
            # each as PNG at this size, ~150 KB as JPEG with no visible loss.
            sips(RAW / f"{prefix}-iphone-{s}.png", assets / "shots" / d / f"shot-{s}.jpg", 1304,
                 jpeg=True)
    total = sum(p.stat().st_size for p in assets.rglob("*") if p.is_file())
    print(f"assets synced — {total // 1024} KB")


if __name__ == "__main__":
    main()
