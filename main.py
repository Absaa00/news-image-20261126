#!/usr/bin/env python3
"""news-image-20261126: one newspaper-style image summing up the world's
news of Thursday 26 November 2026.

Deterministic: no network, no clock, no unseeded randomness. Running the
program twice writes byte-identical PNGs. Output: /output/entry.png
(1024x1024, well under 1 MiB).
"""
import os
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.environ.get("OUTPUT", "/output/entry.png")

INK = (18, 18, 18)
PAPER = (250, 247, 238)
RULE = (120, 110, 95)
RED = (178, 34, 34)
NAVY = (23, 42, 74)
GOLD = (176, 132, 30)
TEAL = (14, 110, 110)
GREY = (90, 86, 78)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    try:
        return ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    except Exception:
        return ImageFont.load_default()


F_TITLE = font("DejaVuSerif-Bold.ttf", 64)
F_HEAD = font("DejaVuSerif-Bold.ttf", 27)
F_HEAD_SMALL = font("DejaVuSerif-Bold.ttf", 23)
F_SUB = font("DejaVuSans.ttf", 17)
F_SUB_SMALL = font("DejaVuSans.ttf", 15)
F_TAG = font("DejaVuSans-Bold.ttf", 15)
F_FOOT = font("DejaVuSans.ttf", 14)


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_panel(img, d, box, tag, tag_bg, headline, sub, art, head_font=F_HEAD,
               art_h=118):
    x0, y0, x1, y1 = box
    d.rectangle([x0, y0, x1, y1], fill=(255, 255, 255),
                outline=RULE, width=2)
    # tag ribbon
    d.rectangle([x0, y0, x0 + 8, y1], fill=tag_bg)
    tx = x0 + 20
    d.text((tx, y0 + 12), tag, font=F_TAG, fill=tag_bg)
    ty = y0 + 34
    for line in wrap(d, headline, head_font, x1 - tx - 14):
        d.text((tx, ty), line, font=head_font, fill=INK)
        ty += head_font.size + 3
    ty += 4
    for line in wrap(d, sub, F_SUB_SMALL, x1 - tx - 14):
        d.text((tx, ty), line, font=F_SUB_SMALL, fill=GREY)
        ty += 20
    # Art on its own layer so nothing can bleed past the panel edges.
    layer = Image.new("RGBA", (x1 - x0, art_h - 10), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    art(ld, 0, 0, x1 - x0, art_h - 10)
    img.paste(layer, (x0, y1 - art_h), layer)


def sky(d, box, top, bottom):
    x0, y0, x1, y1 = box
    for i in range(y1 - y0):
        t = i / max(1, (y1 - y0 - 1))
        c = tuple(int(top[j] + (bottom[j] - top[j]) * t) for j in range(3))
        d.line([(x0, y0 + i), (x1, y0 + i)], fill=c)


def art_refinery(d, x0, y0, x1, y1):
    sky(d, (x0, y0, x1, y1), (40, 30, 40), (120, 60, 40))
    for cx, h in ((x0 + 60, 60), (x0 + 110, 80), (x0 + 170, 55)):
        d.rectangle([cx, y1 - h, cx + 14, y1], fill=(60, 55, 55))
    d.rectangle([x0 + 200, y1 - 40, x1 - 20, y1], fill=(70, 62, 58))
    for fx in (x0 + 240, x0 + 290):
        d.polygon([(fx, y1 - 40), (fx + 14, y1 - 78), (fx + 28, y1 - 40)],
                  fill=(255, 140, 0))
        d.polygon([(fx + 7, y1 - 40), (fx + 14, y1 - 62), (fx + 21, y1 - 40)],
                  fill=(255, 220, 80))
    for sx, sy, r in ((x0 + 250, y0 + 22, 12), (x0 + 285, y0 + 12, 16),
                      (x0 + 320, y0 + 26, 10)):
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(90, 80, 80))


def art_tanker(d, x0, y0, x1, y1):
    sky(d, (x0, y0, x1, y1), (30, 70, 120), (120, 180, 210))
    d.rectangle([x0, y1 - 22, x1, y1], fill=(20, 60, 110))
    d.rectangle([x0 + 40, y1 - 62, x1 - 60, y1 - 22], fill=(150, 40, 35))
    for cx in range(x0 + 55, x1 - 75, 34):
        d.rectangle([cx, y1 - 84, cx + 28, y1 - 62], fill=(240, 200, 60))
    d.rectangle([x1 - 58, y1 - 92, x1 - 38, y1 - 62], fill=(230, 230, 230))
    for mx, my in ((x0 + 70, y0 + 26), (x1 - 90, y0 + 18)):
        d.ellipse([mx - 9, my - 9, mx + 9, my + 9], fill=(40, 40, 40))
        for ang in range(0, 360, 45):
            import math
            ex = mx + 15 * math.cos(math.radians(ang))
            ey = my + 15 * math.sin(math.radians(ang))
            d.line([(mx, my), (ex, ey)], fill=(40, 40, 40), width=2)


def art_space(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(8, 12, 34))
    rng = random.Random(20261126)
    hh = y1 - y0
    for _ in range(46):
        sx = rng.randint(x0 + 4, x1 - 4)
        sy = rng.randint(y0 + 4, y1 - 4)
        r = rng.choice([1, 1, 2])
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 255, 255))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    er = int(hh * 0.42)
    d.ellipse([cx - er, cy + hh // 4, cx + er, cy + hh // 4 + 2 * er],
              fill=(40, 110, 200))
    d.arc([cx - er, cy + hh // 4, cx + er, cy + hh // 4 + 2 * er], 180, 360,
          fill=(140, 200, 255), width=3)
    ry = y0 + 6
    d.polygon([(cx - 10, y1 - 6), (cx, ry), (cx + 10, y1 - 6)],
              fill=(220, 220, 220))
    d.polygon([(cx - 10, ry + 24), (cx, ry), (cx + 10, ry + 24)],
              fill=(200, 40, 40))
    d.rectangle([cx - 44, cy - 12, cx - 6, cy + 6], fill=(180, 180, 190))
    d.rectangle([cx + 6, cy - 12, cx + 44, cy + 6], fill=(180, 180, 190))
    d.rectangle([cx - 6, cy - 18, cx + 6, cy + 12], fill=(210, 210, 215))


def art_wage(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(235, 245, 235))
    hh = y1 - y0
    base = y1 - 12
    vals = [0.30, 0.44, 0.58, 0.82]
    bw = (x1 - x0 - 60) // 4
    for i, v in enumerate(vals):
        bx = x0 + 24 + i * bw
        col = TEAL if i < 3 else (20, 150, 60)
        d.rectangle([bx, base - int(v * (hh - 30)), bx + bw - 12, base],
                    fill=col)
    d.line([(x0 + 24, base - int(0.88 * (hh - 30))),
            (x1 - 30, base - int(0.92 * (hh - 30)))], fill=RED, width=4)
    d.polygon([(x1 - 30, base - int(0.92 * (hh - 30))),
               (x1 - 44, base - int(0.92 * (hh - 30)) - 6),
               (x1 - 44, base - int(0.92 * (hh - 30)) + 6)], fill=RED)
    d.text((x0 + 24, y0 + 6), "+36%  minimum wage", font=F_TAG, fill=RED)


def art_chart(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(245, 240, 235))
    hh = y1 - y0
    d.text((x0 + 18, y0 + 6), "≈ 500,000  lost", font=F_TAG, fill=RED)
    for i in range(9):
        bx = x0 + 22 + i * 30
        h = int((0.14 + i * 0.09) * (hh - 30))
        d.rectangle([bx, y1 - 12 - h, bx + 20, y1 - 12], fill=(150, 40, 35))
    d.line([(x0 + 16, y1 - 12), (x1 - 14, y1 - 12)], fill=INK, width=2)


def art_cricket(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(30, 130, 60))
    d.rectangle([x0, y0 + 44, x1, y1 - 20], fill=(210, 190, 140))
    d.line([(x0 + 40, y0 + 44), (x0 + 40, y1 - 20)], fill=(255, 255, 255),
           width=2)
    for sx in (x1 - 60, x1 - 52, x1 - 44):
        d.rectangle([sx, y1 - 62, sx + 4, y1 - 30], fill=(240, 210, 120))
    import math
    cx, cy = x0 + 90, (y0 + y1) // 2
    d.ellipse([cx - 46, cy - 46, cx + 46, cy + 46], fill=(255, 255, 255),
              outline=(255, 255, 255), width=3)
    d.text((cx - 34, cy - 15), "204", font=F_TAG, fill=INK)
    d.text((cx - 30, cy + 4), "53 balls", font=F_TAG, fill=INK)
    d.ellipse([x1 - 110, y0 + 16, x1 - 94, y0 + 32], fill=(178, 34, 34))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # Masthead
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.text((36, 14), "THE WORLD TODAY", font=F_TITLE, fill=(255, 255, 255))
    d.text((36, 88), "Thursday 26 November 2026  •  One day, six stories",
           font=F_SUB, fill=(200, 210, 230))
    d.text((W - 330, 88), "No. 330  •  Free edition", font=F_SUB,
           fill=(200, 210, 230))
    d.line([(0, 118), (W, 118)], fill=GOLD, width=4)

    # Lead story
    draw_panel(img, d, (24, 134, 1000, 470), "MIDDLE EAST • LEAD", RED,
               "Houthis strike Saudi Arabia's Ras Tanura oil refinery",
               "Yemen's Houthis say they attacked the world's largest oil "
               "terminal, setting fires at Ras Tanura — a new flashpoint for "
               "global energy markets.", art_refinery, art_h=200)

    # Row 1
    draw_panel(img, d, (24, 486, 344, 742), "ENERGY", TEAL,
               "Two tankers hit mines in the Strait of Hormuz",
               "Blasts in the world's busiest oil chokepoint rattle shipping.",
               art_tanker, F_HEAD_SMALL, 92)
    draw_panel(img, d, (352, 486, 672, 742), "SPACE", NAVY,
               "First Pakistani astronaut bound for China's space station",
               "Zeeshan Ali joins the Shenzhou-24 crew for Tiangong.",
               art_space, F_HEAD_SMALL, 92)
    draw_panel(img, d, (680, 486, 1000, 742), "WORKERS", GOLD,
               "Bangladesh garment workers win a 36% pay rise",
               "Minimum wage lifted after talks; millions of factory workers "
               "benefit.", art_wage, F_HEAD_SMALL, 92)

    # Row 2
    draw_panel(img, d, (24, 758, 500, 962), "UKRAINE WAR", RED,
               "Russia's own figures show nearly 500,000 war dead",
               "Moscow's data reveals the scale of battlefield losses.",
               art_chart, F_HEAD_SMALL, 92)
    draw_panel(img, d, (508, 758, 1000, 962), "SPORT • RECORD", TEAL,
               "15-year-old smashes world record: 204 off 53 balls",
               "Sooryavanshi hits the fastest List A double century.",
               art_cricket, F_HEAD_SMALL, 92)

    d.line([(24, 982), (1000, 982)], fill=RULE, width=1)
    d.text((24, 990),
           "Compiled from world news wires, 26 Nov 2026 • Also today: India "
           "marks Constitution Day; Gukesh faces Sindarov for the world chess "
           "crown.", font=F_FOOT, fill=GREY)

    os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
    img.save(OUT, format="PNG", optimize=True)


if __name__ == "__main__":
    main()
