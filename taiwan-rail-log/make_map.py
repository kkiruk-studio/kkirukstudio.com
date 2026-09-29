#!/usr/bin/env python3
"""Bake the hero map (main island of Taiwan + the 39 lines) into `_src/railmap.svg`.

Run once when the seed or the county outlines change; `build.py` inlines the
result. Inputs come straight from the app repo so the page draws the same
network the app ships:

  - lines / stations: TwraillogApp/Resources/seed.json (straight segments
    between consecutive stations — fine at hero scale)
  - line colours:     TwraillogApp/DesignSystem/Tokens/LineColorRegistry.swift
  - counties:         TwraillogApp/scripts/_raw/osm_admin.json
                      (OSM admin_level 4, © OpenStreetMap contributors, ODbL)

Only the main island is drawn; 澎湖・金門・連江 fall outside the frame.

    python3 make_map.py
"""
import json
import math
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
APP = pathlib.Path.home() / "Taiwan Rail Log" / "TwraillogApp"
OUT = HERE / "_src" / "railmap.svg"

# Frame (degrees). Main island only.
LON0, LON1 = 119.95, 122.08
LAT0, LAT1 = 21.86, 25.36
W = 1000                      # viewBox width; height follows the projection
PAD = 30

# Lines that are "ridden" in the hero demo, in draw order. Everything else
# stays grey — the same unridden/ridden split the app's map shows.
# (id, css class, stagger group). Group n starts after group n-1 finishes.
RIDDEN = [
    # 環島 — the TRA loop, clockwise from Keelung
    ("tw-tra-wcl-n", "tra", 0), ("tw-tra-tcl", "tra", 1), ("tw-tra-wcl-s", "tra", 2),
    ("tw-tra-ptl", "tra", 3), ("tw-tra-sl", "tra", 4), ("tw-tra-ttl", "tra", 5),
    ("tw-tra-nl", "tra", 6), ("tw-tra-yl", "tra", 7),
    # then 高鐵, a branch line, 阿里山, and Taipei / Kaohsiung metro
    ("tw-thsr", "thsr", 8),
    ("tw-tra-px", "tra-br", 9), ("tw-tra-jj", "tra-br", 9),
    ("tw-afr-main", "afr", 10),
    ("tw-trtc-r", "trtc-r", 10), ("tw-trtc-bl", "trtc-bl", 10), ("tw-krtc-r", "krtc-r", 10),
]
# Stations that become "stamps" (dots that ink in) — endpoints of the loop legs.
MAJOR = {"基隆", "臺北", "新竹", "臺中", "彰化", "嘉義", "臺南", "高雄", "枋寮",
         "臺東", "花蓮", "蘇澳新", "宜蘭", "八堵"}
# Labels drawn on the map (zh-Hant, the app's own station names).
LABELS = [("臺北", "end", -14, -6), ("臺中", "end", -14, 6), ("高雄", "end", -14, 8),
          ("花蓮", "start", 14, 6), ("臺東", "start", 14, 8)]


def project(lon, lat):
    # Equirectangular with a cos(lat) squash at the island's mid-latitude —
    # indistinguishable from Mercator over 3.5° of latitude.
    k = (W - 2 * PAD) / ((LON1 - LON0) * math.cos(math.radians(23.6)))
    x = PAD + (lon - LON0) * math.cos(math.radians(23.6)) * k
    y = PAD + (LAT1 - lat) * k
    return x, y


H = round(project(LON0, LAT0)[1] + PAD)


def rdp(pts, eps):
    if len(pts) < 3:
        return pts
    (x1, y1), (x2, y2) = pts[0], pts[-1]
    dx, dy = x2 - x1, y2 - y1
    n = math.hypot(dx, dy) or 1e-9
    dmax, idx = 0, 0
    for i in range(1, len(pts) - 1):
        x0, y0 = pts[i]
        d = abs(dy * x0 - dx * y0 + x2 * y1 - y2 * x1) / n
        if d > dmax:
            dmax, idx = d, i
    if dmax > eps:
        return rdp(pts[: idx + 1], eps)[:-1] + rdp(pts[idx:], eps)
    return [pts[0], pts[-1]]


def stitch(ways):
    """Join way coordinate lists into closed rings by matching endpoints."""
    ways = [list(w) for w in ways if len(w) > 1]
    rings = []
    while ways:
        ring = ways.pop(0)
        changed = True
        while ring[0] != ring[-1] and changed:
            changed = False
            for i, w in enumerate(ways):
                if w[0] == ring[-1]:
                    ring += w[1:]
                elif w[-1] == ring[-1]:
                    ring += w[::-1][1:]
                elif w[-1] == ring[0]:
                    ring = w[:-1] + ring
                elif w[0] == ring[0]:
                    ring = w[::-1][:-1] + ring
                else:
                    continue
                ways.pop(i)
                changed = True
                break
        rings.append(ring)
    return rings


def fmt(pts):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)


def in_frame(ring):
    lons = [p[0] for p in ring]
    lats = [p[1] for p in ring]
    return (min(lons) > LON0 - .05 and max(lons) < LON1 + .05
            and min(lats) > LAT0 - .05 and max(lats) < LAT1 + .05)


def main():
    colours = {}
    src = (APP / "DesignSystem/Tokens/LineColorRegistry.swift").read_text()
    for m in re.finditer(r'light: 0x([0-9A-F]{6}).*?// (tw-[a-z0-9-]+)', src):
        colours[m.group(2)] = "#" + m.group(1)

    admin = json.loads((APP / "scripts/_raw/osm_admin.json").read_text())
    county_paths = []
    for rel in admin["elements"]:
        name = rel["tags"].get("name")
        outer = [[(g["lon"], g["lat"]) for g in m["geometry"]]
                 for m in rel["members"] if m.get("role") == "outer" and m.get("geometry")]
        d = []
        for ring in stitch(outer):
            if ring[0] != ring[-1] or not in_frame(ring) or len(ring) < 8:
                continue
            # A closed ring has start == end, which RDP collapses — simplify halves.
            proj = [project(*p) for p in ring]
            mid = len(proj) // 2
            pts = rdp(proj[: mid + 1], 1.5)[:-1] + rdp(proj[mid:], 1.5)
            if len(pts) < 4:
                continue
            d.append("M" + fmt(pts) + "Z")
        if d:
            county_paths.append((name, "".join(d)))

    seed = json.loads((APP / "Resources/seed.json").read_text())
    lines = {l["id"]: l for l in seed["lines"]}

    def line_pts(lid):
        return [project(s["lng"], s["lat"]) for s in lines[lid]["stations"]]

    # Stations on the ridden lines, counted per line like the app's "589" total.
    ridden_st = [s["id"] for lid, _, _ in RIDDEN for s in lines[lid]["stations"]]
    out = [f'<svg viewBox="0 0 {W} {H}" aria-hidden="true" data-ridden="{len(ridden_st)}">',
           '<g class="counties">']
    for name, d in county_paths:
        out.append(f'<path class="county" data-n="{name}" d="{d}"/>')
    out.append('</g><g class="net">')
    for lid in sorted(lines):
        pts = line_pts(lid)
        if len(pts) > 1:
            out.append(f'<polyline class="base" points="{fmt(pts)}"/>')
    out.append('</g><g class="ridden">')
    groups = {}
    for lid, cls, grp in RIDDEN:
        pts = line_pts(lid)
        colour = colours.get(lid, "#0B4EA2")
        out.append(f'<polyline class="ride {cls} g{grp}" pathLength="100" style="--c:{colour}" '
                   f'points="{fmt(pts)}"/>')
        groups.setdefault(grp, []).append(lid)
    out.append('</g><g class="stations">')
    seen = set()
    for lid, _, grp in RIDDEN:
        for s in lines[lid]["stations"]:
            if s["nameJa"] in MAJOR and s["nameJa"] not in seen:
                seen.add(s["nameJa"])
                x, y = project(s["lng"], s["lat"])
                out.append(f'<circle class="st g{grp}" cx="{x:.1f}" cy="{y:.1f}" r="9"/>')
    out.append('</g><g class="labels">')
    pos = {}
    for l in seed["lines"]:
        for s in l["stations"]:
            pos.setdefault(s["nameJa"], project(s["lng"], s["lat"]))
    for name, anchor, dx, dy in LABELS:
        x, y = pos[name]
        out.append(f'<text x="{x + dx:.0f}" y="{y + dy:.0f}" text-anchor="{anchor}">{name}</text>')
    out.append('</g></svg>')
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(HERE)} — {W}x{H}, {len(county_paths)} counties, "
          f"{len(RIDDEN)} ridden lines, {len(seen)} stamps, {OUT.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
