#!/usr/bin/env python3
"""Draw the 25 November 2026 world-news front page (1024x1024 PNG).

Deterministic: fixed fonts, fixed geometry, no randomness, no network.
Run:  python3 draw.py            -> writes entry.png next to this file.

Design (my own): a one-page newspaper, "ONE DAY IN THE WORLD",
masthead dated Wednesday 25 November 2026, one lead story, two
column stories, three mid-page cards and an "ALSO TODAY" strip.
Every story was reported on 25 November 2026 (in at least one time
zone) and is worded as reported, without hype or speculation.
"""
import hashlib
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = Path(__file__).resolve().parent / "entry.png"

PAPER = (247, 243, 232)
INK = (28, 28, 26)
GREEN = (30, 77, 59)        # masthead
GREEN_DK = (20, 54, 41)
CREAM = (247, 243, 232)
GOLD = (192, 138, 44)
CRIMSON = (169, 50, 38)
NAVY = (20, 38, 58)         # lead panel
STEEL = (58, 84, 110)
CARD = (255, 253, 248)
BORDER = (214, 205, 184)
MUTED = (96, 90, 78)
TEAL = (14, 107, 107)
SKY = (174, 205, 220)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(f"{FONT_DIR}/{name}", size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)


def wrap(d, text, fnt, max_w):
    """Greedy word wrap; returns lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, fnt, color, max_w, leading=1.28):
    """Draw wrapped paragraph; return y below it."""
    for line in wrap(d, text, fnt, max_w):
        d.text((x, y), line, font=fnt, fill=color)
        y += int(fnt.size * leading)
    return y


def kicker(d, x, y, text, color=CRIMSON, size=15):
    d.text((x, y), text, font=SANS_B(size), fill=color)
    return y + size + 6


def rule(d, x0, x1, y, color=BORDER, width=2):
    d.line([(x0, y), (x1, y)], fill=color, width=width)


def card(d, x0, y0, x1, y1, fill=CARD):
    d.rounded_rectangle([x0, y0, x1, y1], radius=6, fill=fill,
                        outline=BORDER, width=2)


# ---------------------------------------------------------------- scene art
def draw_shield(d, cx, cy, s):
    """Gold shield + keyhole on the dark lead panel."""
    pts = [(cx, cy - s), (cx + s * 0.85, cy - s * 0.55),
           (cx + s * 0.7, cy + s * 0.45), (cx, cy + s),
           (cx - s * 0.7, cy + s * 0.45), (cx - s * 0.85, cy - s * 0.55)]
    d.polygon(pts, outline=GOLD, width=5)
    d.ellipse([cx - s * 0.28, cy - s * 0.35, cx + s * 0.28, cy + s * 0.15],
              fill=GOLD)
    d.polygon([(cx - s * 0.14, cy), (cx + s * 0.14, cy),
               (cx + s * 0.26, cy + s * 0.5), (cx - s * 0.26, cy + s * 0.5)],
              fill=GOLD)


def draw_nodes(d, x0, y0, x1, y1):
    """Small network of linked dots, lead panel decoration."""
    pts = [(x0 + 14, y0 + 18), (x0 + 62, y0 + 6), (x0 + 108, y0 + 26),
           (x0 + 34, y0 + 52), (x0 + 92, y0 + 62), (x0 + 130, y0 + 44)]
    for a, b in [(0, 1), (1, 2), (0, 3), (1, 4), (3, 4), (4, 5), (2, 5)]:
        d.line([pts[a], pts[b]], fill=(90, 120, 150), width=2)
    for p in pts:
        d.ellipse([p[0] - 5, p[1] - 5, p[0] + 5, p[1] + 5], fill=GOLD)


def draw_tanker(d, x0, y0, x1, y1):
    """Oil tanker and sea mines, Gulf panel."""
    d.rectangle([x0, y0, x1, y1], fill=(198, 222, 228))
    # hull: dark red-brown, low in the frame, with a white bridge tower
    d.polygon([(x0 + 12, y1 - 30), (x0 + 210, y1 - 30), (x0 + 196, y1 - 8),
               (x0 + 26, y1 - 8)], fill=(122, 44, 36))
    d.rectangle([x0 + 20, y1 - 52, x0 + 52, y1 - 30], fill=CRIMSON)
    d.rectangle([x0 + 56, y1 - 52, x0 + 88, y1 - 30], fill=GOLD)
    d.rectangle([x0 + 92, y1 - 52, x0 + 124, y1 - 30], fill=TEAL)
    d.rectangle([x0 + 176, y1 - 58, x0 + 200, y1 - 30], fill=(240, 240, 235))
    d.rectangle([x0 + 182, y1 - 66, x0 + 194, y1 - 58], fill=(240, 240, 235))
    # spiked sea mines, upper right
    for mx, my in [(x0 + 232, y0 + 20), (x0 + 258, y0 + 44),
                   (x0 + 226, y0 + 56)]:
        for ang in range(0, 360, 45):
            a = math.radians(ang)
            d.line([(mx + 7 * math.cos(a), my + 7 * math.sin(a)),
                    (mx + 13 * math.cos(a), my + 13 * math.sin(a))],
                   fill=INK, width=2)
        d.ellipse([mx - 8, my - 8, mx + 8, my + 8], fill=INK)
    # wave line
    d.line([(x0 + 6, y1 - 2), (x1 - 6, y1 - 2)], fill=(255, 255, 255),
           width=2)


def draw_cross(d, x0, y0, x1, y1):
    """Medical cross in a circle, health panel."""
    d.rectangle([x0, y0, x1, y1], fill=(222, 238, 234))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.ellipse([cx - 42, cy - 42, cx + 42, cy + 42], fill=TEAL)
    d.rectangle([cx - 10, cy - 28, cx + 10, cy + 28], fill=(255, 255, 255))
    d.rectangle([cx - 28, cy - 10, cx + 28, cy + 10], fill=(255, 255, 255))


def draw_radar(d, x0, y0, x1, y1):
    """Radar arcs and a small plane, Europe panel."""
    d.rectangle([x0, y0, x1, y1], fill=(214, 226, 232))
    cx, cy = (x0 + x1) // 2, y1 - 8
    for r in (30, 55, 80):
        d.arc([cx - r, cy - r, cx + r, cy + r], 180, 360, fill=STEEL, width=3)
    d.line([(cx, cy - 88), (cx, cy)], fill=STEEL, width=3)
    px, py = cx + 52, y0 + 26
    d.polygon([(px, py - 12), (px + 26, py + 8), (px, py + 4), (px - 26, py + 8)],
              fill=CRIMSON)


# ---------------------------------------------------------------- page
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 28  # margin

    # Masthead ------------------------------------------------------------
    d.rectangle([0, 0, W, 118], fill=GREEN)
    d.rectangle([0, 118, W, 122], fill=GOLD)
    d.text((M, 14), "ONE DAY IN THE WORLD", font=SERIF_B(50), fill=CREAM)
    d.text((M, 78), "WEDNESDAY, 25 NOVEMBER 2026",
           font=SANS_B(21), fill=GOLD)
    d.text((W - M - d.textlength("THE DAY'S WORLD NEWS IN ONE IMAGE",
                                 font=SANS(16)), 82),
           "THE DAY'S WORLD NEWS IN ONE IMAGE", font=SANS(16),
           fill=(210, 220, 205))

    # Lead: cyberattack ---------------------------------------------------
    lx0, ly0, lx1, ly1 = M, 136, 620, 428
    d.rounded_rectangle([lx0, ly0, lx1, ly1], radius=8, fill=NAVY)
    draw_shield(d, 560, 382, 38)
    draw_nodes(d, 44, 330, 200, 410)
    kicker(d, lx0 + 18, ly0 + 16, "CYBERATTACK  •  WASHINGTON", color=GOLD)
    y = para(d, lx0 + 18, ly0 + 48, "U.S. SPIES HACKED",
             SERIF_B(44), (255, 255, 255), lx1 - lx0 - 36)
    y = para(d, lx0 + 18, y + 8,
             "CIA and the Director of National Intelligence hit in a "
             "breach of unclassified systems — the latest in a string of "
             "cyber incidents rattling U.S. agencies.",
             SANS(17), (214, 224, 232), lx1 - lx0 - 36)
    d.text((lx0 + 18, ly1 - 30),
           "Officials: no classified systems affected.",
           font=SANS(14), fill=(150, 170, 190))

    # Right column: Ukraine + Riyadh --------------------------------------
    rx0, rx1 = 636, W - M
    # Ukraine
    uy0, uy1 = 136, 276
    card(d, rx0, uy0, rx1, uy1)
    d.text((rx0 + 12, uy0 + 10), "UKRAINE • BALTIC SEA",
           font=SANS_B(13), fill=CRIMSON)
    y = para(d, rx0 + 12, uy0 + 32, "Kyiv owns Baltic ship strike",
             SERIF_B(21), INK, rx1 - rx0 - 24, leading=1.15)
    para(d, rx0 + 12, y + 4,
         "Zelenskiy confirms Ukraine's drone hit on the Russian cargo "
         "ship Sparta II in the Gulf of Finland; ally Norway urges caution.",
         SANS(14), (52, 52, 48), rx1 - rx0 - 24, leading=1.25)
    # Riyadh
    ry0, ry1 = 288, 428
    card(d, rx0, ry0, rx1, ry1)
    d.text((rx0 + 12, ry0 + 10), "MIDDLE EAST • RIYADH",
           font=SANS_B(13), fill=CRIMSON)
    y = para(d, rx0 + 12, ry0 + 32, "Riyadh tower hit again",
             SERIF_B(21), INK, rx1 - rx0 - 24, leading=1.15)
    para(d, rx0 + 12, y + 4,
         "Houthi drone strikes the capital's tallest tower, home of the "
         "sovereign wealth fund — 11 wounded, the second hit in a week.",
         SANS(14), (52, 52, 48), rx1 - rx0 - 24, leading=1.25)

    # Mid row: three cards --------------------------------------------------
    my0, my1 = 442, 736
    cols = [(M, 336), (352, 660), (676, W - M)]
    stories = [
        ("GULF SHIPPING", "Mines in the Strait",
         "Iran says three oil tankers were hit by naval mines in the "
         "Strait of Hormuz, raising fears for shipping.", draw_tanker),
        ("HEALTH • CONGO", "Ebola staff flee fighting",
         "WHO evacuates health workers from a hospital in Ituri after "
         "three days sheltering from fierce fighting.", draw_cross),
        ("EUROPE • NATO", "NATO watches Poland's skies",
         "Early-warning aircraft to deploy in Poland after missiles "
         "landed there during an attack on Ukraine.", draw_radar),
    ]
    for (cx0, cx1), (kick, head, body, art) in zip(cols, stories):
        card(d, cx0, my0, cx1, my1)
        art(d, cx0 + 8, my0 + 8, cx1 - 8, my0 + 92)
        d.text((cx0 + 14, my0 + 102), kick, font=SANS_B(13), fill=CRIMSON)
        y = para(d, cx0 + 14, my0 + 126, head, SERIF_B(22), INK,
                 cx1 - cx0 - 28, leading=1.15)
        para(d, cx0 + 14, y + 8, body, SANS(15), (52, 52, 48),
             cx1 - cx0 - 28, leading=1.3)

    # Also today ------------------------------------------------------------
    ay0, ay1 = 750, 996
    d.rectangle([0, ay0, W, ay1], fill=GREEN_DK)
    d.text((M, ay0 + 12), "ALSO TODAY", font=SERIF_B(22), fill=GOLD)
    items_left = [
        "NEPAL — 5.6-magnitude quake hits Koshi Province.",
        "TECH — Huawei found guilty on 10 of 12 counts.",
        "U.S. — Trump pardons turkeys Freedom and Feathers.",
        "SPORT — England beat Australia in the 2nd T20I.",
    ]
    items_right = [
        "U.A.E. — 11 killed in Ras Al Khaimah road crash.",
        "U.S. — Giuliani receives the Medal of Freedom.",
        "MARKETS — Anthropic shares slide below $83 IPO price.",
        "INDIA — BJP and Akali Dal reunite for Punjab polls.",
    ]
    y = ay0 + 48
    for left, right in zip(items_left, items_right):
        d.text((M, y), "•  " + left, font=SANS(15), fill=CREAM)
        d.text((W // 2 + 8, y), "•  " + right, font=SANS(15), fill=CREAM)
        y += 30
    rule(d, M, W - M, ay1 - 34, color=(90, 120, 100), width=1)
    d.text((M, ay1 - 28),
           "25 November is the International Day for the Elimination of "
           "Violence against Women.",
           font=SANS(14), fill=(190, 200, 185))
    d.text((W - M - d.textlength("Sources: Reuters • CNN • NYT • AFP",
                                 font=SANS(13)), ay1 - 28),
           "Sources: Reuters • CNN • NYT • AFP", font=SANS(13),
           fill=(150, 165, 150))

    img.save(OUT, "PNG", optimize=True)
    data = OUT.read_bytes()
    print(f"wrote {OUT} {len(data)} bytes "
          f"sha256={hashlib.sha256(data).hexdigest()}")


if __name__ == "__main__":
    build()
