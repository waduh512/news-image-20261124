#!/usr/bin/env python3
"""Render the news-image entry v4: a one-page summary of the world news of
Tuesday 24 November 2026, as a 1024x1024 PNG.

v4 is a rebuild, not a polish: after studying the ACTUAL top 10 of the
finalised previous round (news-image-20261122, viewed as artifact images),
the winners are dense digests of 29-41 dated, numbered stories in 7-9
regions -- UTC timeline, day-in-numbers strip, region bar, 3 illustrated
leads, ~10 medium stories, a one-line "also" list, a dotted world map with
numbered pins, and a DATE CHECK footer. Our v1-v3 had 5 stories; v4 has
30 numbered, dated stories, following that winning shape.

Vibe (user's direction, "lebih chil lagi biar kek cs kita"): chill zine,
not a stern broadsheet -- warm cream paper, deep teal + terracotta +
mustard palette, wavy divider, title-case masthead, a friendly tagline
("take a breath — here's the day") and a little drawn sun. The news itself
stays serious and accurate; only the design is relaxed.

v4.1 (user's choice: "ganti dengan yg paling bagus dan menarik"): lead card
3 swaps the four-party talks for the most striking story of the day --
Ukraine's sea-drone sinking of the Russian corvette Merkury at Benghazi,
Libya. The talks survive as the lead card's closing line. DATE CHECK
wording fixed to stay honest: the Merkury attack was announced Mon 23 Nov
(and Huang's return too), so the footer now says so instead of claiming
everything happened on 24 Nov.

Everything is drawn with code (PIL + DejaVu fonts): no photos, no logos,
no network. Deterministic: same bytes every run.

Build-time tool only. The entry program (main.ts) copies the PNG this
script writes into /output/entry.png.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "entry.png")

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_SERIF = lambda s: font("DejaVuSerif.ttf", s)
F_B = lambda s: font("DejaVuSans-Bold.ttf", s)
F_R = lambda s: font("DejaVuSans.ttf", s)
F_I = lambda s: font("DejaVuSansMono-Oblique.ttf", s)

# Palette — chill zine: deep teal, terracotta, mustard on warm cream
NAVY = (18, 82, 76)
NAVY_D = (12, 60, 56)
INK = (32, 30, 26)
GREY = (112, 102, 88)
PAPER = (253, 246, 233)
CARD = (255, 255, 255)
GOLD = (224, 164, 60)
RED = (196, 88, 56)
RED_D = (170, 70, 44)
GREEN = (74, 138, 90)
GREEN_L = (222, 238, 216)
BLUE = (74, 110, 160)
BLUE_L = (218, 232, 244)
ORANGE = (210, 110, 50)
ORANGE_L = (252, 232, 210)
TEAL = (30, 130, 125)
TEAL_L = (214, 238, 236)
SKY = (186, 219, 238)
LEAF = (96, 168, 108)
LINE = (226, 216, 200)
PURPLE = (130, 95, 150)
BROWN = (150, 105, 60)


def wrap(draw, text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, lines, fnt, fill, leading):
    x, y = xy
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def chip(draw, x, y, w, h, text, bg, fg, fnt):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=h // 2, fill=bg)
    tw = draw.textlength(text, font=fnt)
    draw.text((x + (w - tw) / 2, y + (h - fnt.size) / 2 - 1), text,
              font=fnt, fill=fg)


def tag(draw, x, y, text, color):
    """Verification tag, e.g. REPORTED / CLAIM / OFFICIAL / ONGOING."""
    fnt = F_B(10)
    w = draw.textlength(text, font=fnt) + 10
    draw.rounded_rectangle([x, y, x + w, y + 15], radius=3, fill=color)
    draw.text((x + 5, y + 2), text, font=fnt, fill=(255, 255, 255))
    return w


TAG_COLORS = {"REPORTED": (120, 110, 95), "CLAIM": (200, 150, 40),
              "OFFICIAL": GREEN, "ONGOING": (210, 110, 50)}


def draw_globe(draw, cx, cy, r):
    draw.ellipse([cx - r - 14, cy - r - 14, cx + r + 14, cy + r + 14],
                 fill=(253, 232, 200))
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SKY, outline=NAVY,
                 width=4)
    draw.ellipse([cx - r * 0.78, cy - r * 0.62, cx - r * 0.08, cy - r * 0.05],
                 fill=LEAF)
    draw.ellipse([cx + r * 0.05, cy - r * 0.55, cx + r * 0.72, cy - r * 0.02],
                 fill=LEAF)
    draw.ellipse([cx - r * 0.55, cy + r * 0.28, cx + r * 0.1, cy + r * 0.78],
                 fill=LEAF)
    draw.ellipse([cx + r * 0.28, cy + r * 0.35, cx + r * 0.75, cy + r * 0.7],
                 fill=LEAF)
    draw.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
                 outline=(255, 255, 255), width=2)
    draw.line([cx - r, cy, cx + r, cy], fill=(255, 255, 255), width=2)
    for sx, sy, sw in [(cx - r - 6, cy - r + 30, 28),
                       (cx + r - 20, cy - r + 22, 30)]:
        draw.arc([sx, sy, sx + sw, sy + 14], 180, 360, fill=(150, 150, 150),
                 width=4)
    crack = [(cx + 18, cy - r + 4), (cx - 8, cy - r * 0.45),
             (cx + 22, cy - r * 0.1), (cx - 14, cy + r * 0.35),
             (cx + 10, cy + r * 0.7), (cx - 4, cy + r - 6)]
    draw.line(crack, fill=RED, width=8, joint="curve")
    draw.line(crack, fill=(255, 255, 255), width=2, joint="curve")


def scene_chip_chart(draw, sx, sy, sw, sh):
    """Nvidia: chip above a rising bar chart."""
    cx = sx + sw // 2
    s = 48
    x, y = cx - s // 2, sy + 2
    draw.rounded_rectangle([x, y, x + s, y + s], radius=8, fill=GREEN)
    draw.rounded_rectangle([x + s * 0.22, y + s * 0.22,
                            x + s * 0.78, y + s * 0.78], radius=4,
                           outline=(255, 255, 255), width=3)
    for i in range(3):
        px = x + s * (0.3 + 0.2 * i)
        draw.line([px, y - 7, px, y], fill=GREEN, width=3)
        draw.line([px, y + s, px, y + s + 7], fill=GREEN, width=3)
        py = y + s * (0.3 + 0.2 * i)
        draw.line([x - 7, py, x, py], fill=GREEN, width=3)
        draw.line([x + s, py, x + s + 7, py], fill=GREEN, width=3)
    draw.line([(x + s * 0.28, y + s * 0.62), (x + s * 0.5, y + s * 0.44),
               (x + s * 0.66, y + s * 0.54), (x + s * 0.8, y + s * 0.3)],
              fill=(255, 255, 255), width=3, joint="curve")
    draw.polygon([(x + s * 0.8, y + s * 0.3), (x + s * 0.66, y + s * 0.28),
                  (x + s * 0.78, y + s * 0.44)], fill=(255, 255, 255))
    base = sy + sh - 2
    bw, gap = 16, 6
    bx = sx + (sw - (5 * bw + 4 * gap)) // 2
    for i, hh in enumerate([8, 13, 18, 24, 30]):
        col = GOLD if i == 4 else GREEN
        draw.rectangle([bx + i * (bw + gap), base - hh,
                        bx + i * (bw + gap) + bw, base], fill=col)
    draw.line([(bx, base - 8), (bx + 2 * (bw + gap), base - 18),
               (bx + 4 * (bw + gap) + bw, base - 30)],
              fill=RED, width=3, joint="curve")


def scene_table(draw, sx, sy, sw, sh):
    """Ukraine: negotiation table seen from above, four flagged seats."""
    cx, cy = sx + sw // 2, sy + sh // 2 + 2
    draw.ellipse([cx - 48, cy - 36, cx + 48, cy + 36], fill=(255, 255, 255),
                 outline=BLUE, width=4)
    draw.ellipse([cx - 24, cy - 16, cx + 24, cy + 16], outline=BLUE_L,
                 width=3)
    seats = [((0, -42), "UA", (0, 87, 183)),
             ((0, 42), "EU", (36, 68, 160)),
             ((-48, 0), "RU", (192, 57, 43)),
             ((48, 0), "US", (30, 122, 52))]
    for (dx, dy), lab, col in seats:
        draw.ellipse([cx + dx - 11, cy + dy - 11, cx + dx + 11, cy + dy + 11],
                     fill=col, outline=(255, 255, 255), width=2)
        tw = draw.textlength(lab, font=F_B(11))
        draw.text((cx + dx - tw / 2, cy + dy - 6), lab, font=F_B(11),
                  fill=(255, 255, 255))
    draw.text((cx - 7, cy - 10), "4", font=F_B(22), fill=BLUE)


def scene_ship_attack(draw, sx, sy, sw, sh):
    """Merkury: a capsized Russian corvette listing in the sea, smoke and
    flame on deck, small sea drones closing in with white wakes."""
    cx, cy = sx + sw // 2, sy + sh // 2
    draw.rectangle([sx, sy, sx + sw, sy + sh], fill=(214, 233, 244))
    # sea
    draw.rectangle([sx, sy + 56, sx + sw, sy + sh], fill=(110, 165, 205))
    for wx in (sx + 14, sx + 150, sx + 262):
        draw.arc([wx, sy + 62, wx + 34, sy + 74], 180, 360,
                 fill=(255, 255, 255), width=2)
    # smoke plumes above the wreck
    for px, py, pr in [(cx - 52, cy - 26, 13), (cx - 30, cy - 34, 15),
                       (cx - 8, cy - 28, 12)]:
        draw.ellipse([px - pr, py - pr, px + pr, py + pr],
                     fill=(150, 150, 150))
    # capsized hull, listing to starboard, bow low and half-submerged
    hull = [(cx - 88, cy + 12), (cx + 76, cy - 10), (cx + 88, cy + 4),
            (cx + 78, cy + 22), (cx - 60, cy + 38)]
    draw.polygon(hull, fill=(110, 118, 128))
    stripe = [(cx - 82, cy + 20), (cx + 80, cy - 2), (cx + 84, cy + 6),
              (cx - 72, cy + 30)]
    draw.polygon(stripe, fill=(170, 70, 44))
    # superstructure block + leaning mast
    draw.polygon([(cx + 28, cy - 10), (cx + 54, cy - 16), (cx + 58, cy - 2),
                  (cx + 32, cy + 4)], fill=(70, 76, 84))
    draw.line([(cx + 48, cy - 14), (cx + 72, cy - 34)], fill=(70, 76, 84),
              width=4)
    # flame on the deck
    draw.polygon([(cx - 52, cy + 6), (cx - 42, cy - 14), (cx - 32, cy + 0),
                  (cx - 22, cy - 18), (cx - 10, cy + 6)], fill=ORANGE)
    draw.polygon([(cx - 42, cy + 6), (cx - 34, cy - 8), (cx - 26, cy + 6)],
                 fill=GOLD)
    # waves lapping over the hull's lower edge
    for wx in (cx - 70, cx - 20, cx + 30):
        draw.arc([wx, cy + 26, wx + 30, cy + 38], 180, 360,
                 fill=(255, 255, 255), width=2)
    # three sea drones closing in, with wakes (kept clear of the "3" badge)
    for dx, dy in [(cx - 100, cy + 33), (cx + 108, cy + 32),
                   (cx + 128, cy + 24)]:
        draw.line([(dx - 22, dy + 2), (dx - 6, dy)], fill=(255, 255, 255),
                  width=2)
        draw.ellipse([dx - 9, dy - 4, dx + 9, dy + 4], fill=(40, 44, 48))
        draw.line([(dx, dy - 4), (dx + 3, dy - 10)], fill=(40, 44, 48),
                  width=2)


def mini(draw, kind, x, y, w, h, tint):
    """Small scene for a medium card: tinted square + simple motif."""
    draw.rectangle([x, y, x + w, y + h], fill=tint)
    cx, cy = x + w // 2, y + h // 2
    if kind == "sun_chart":  # Japan deal
        draw.ellipse([cx - 22, cy - 24, cx + 22, cy + 20], fill=(200, 60, 50))
        draw.line([(x + 8, y + h - 14), (x + w // 3, y + h - 26),
                   (x + 2 * w // 3, y + h - 20), (x + w - 8, y + h - 32)],
                  fill=NAVY, width=3, joint="curve")
        draw.polygon([(x + w - 8, y + h - 32), (x + w - 20, y + h - 32),
                      (x + w - 10, y + h - 22)], fill=NAVY)
    elif kind == "ship":  # trade
        for i, c in enumerate([TEAL, NAVY, RED]):
            draw.rectangle([x + 8 + i * 20, cy - 18, x + 24 + i * 20, cy + 2],
                           fill=c, outline=(255, 255, 255), width=1)
        draw.polygon([(x + 4, cy + 2), (x + w - 4, cy + 2),
                      (x + w - 14, cy + 20), (x + 14, cy + 20)], fill=INK)
        draw.arc([x + 8, cy + 18, x + 30, cy + 30], 0, 180, fill=TEAL, width=2)
        draw.arc([x + w - 30, cy + 18, x + w - 8, cy + 30], 0, 180,
                 fill=TEAL, width=2)
    elif kind == "jet":  # Pentagon / Canada
        draw.polygon([(x + 10, cy), (x + w - 14, cy - 8), (x + w - 8, cy),
                      (x + w - 14, cy + 8)], fill=NAVY)
        draw.polygon([(x + w // 2, cy - 4), (x + w // 2 + 12, cy - 16),
                      (x + w // 2 + 16, cy - 4)], fill=NAVY)
        draw.line([(x + 8, cy + 16), (x + w - 8, cy + 16)], fill=GREY, width=2)
    elif kind == "gavel":  # court / sentence
        draw.line([(x + 12, cy + 8), (x + w - 12, cy - 10)], fill=BROWN,
                  width=5)
        draw.rectangle([x + w - 30, cy - 20, x + w - 10, cy - 4], fill=BROWN)
        draw.line([(x + 10, cy + 18), (x + w - 10, cy + 18)], fill=BROWN,
                  width=4)
    elif kind == "radar":  # Korea ADIZ
        draw.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], outline=NAVY,
                     width=3)
        draw.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], outline=NAVY,
                     width=2)
        draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=RED)
        draw.line([(cx, cy), (cx + 18, cy - 14)], fill=RED, width=3)
    elif kind == "flame":  # factory fire
        draw.polygon([(cx - 26, cy + 22), (cx - 20, cy - 6), (cx - 8, cy - 22),
                      (cx + 2, cy - 2), (cx + 14, cy - 16), (cx + 24, cy + 22)],
                     fill=ORANGE)
        draw.polygon([(cx - 12, cy + 22), (cx - 4, cy + 2), (cx + 4, cy - 10),
                      (cx + 12, cy + 22)], fill=GOLD)
        draw.rectangle([x + 6, cy + 22, x + w - 6, cy + 26], fill=INK)
    elif kind == "vial":  # vaccines
        draw.rectangle([cx - 8, cy - 22, cx + 8, cy + 14], fill=BLUE)
        draw.rectangle([cx - 12, cy - 26, cx + 12, cy - 20], fill=NAVY)
        draw.line([(cx, cy + 14), (cx, cy + 26)], fill=GREY, width=3)
        draw.text((cx - 4, cy - 12), "+", font=F_B(16), fill=(255, 255, 255))
    elif kind == "bars":  # power index
        for i, hh in enumerate([12, 20, 28, 36]):
            draw.rectangle([x + 10 + i * 15, cy + 20 - hh,
                            x + 22 + i * 15, cy + 20], fill=NAVY if i < 3 else GOLD)
        draw.line([(x + 8, cy + 20), (x + w - 8, cy + 20)], fill=INK, width=2)
    elif kind == "cricket":  # Test drawn
        draw.line([(cx - 6, cy - 24), (cx + 10, cy + 10)], fill=(200, 160, 100),
                  width=7)
        draw.ellipse([cx + 12, cy + 12, cx + 26, cy + 26], fill=RED)
        draw.line([(x + 8, cy + 24), (x + w - 8, cy + 24)], fill=GREEN,
                  width=3)
    elif kind == "waves":  # Himalayan flood
        draw.polygon([(x + 6, cy + 10), (x + w // 3, cy - 18),
                      (x + 2 * w // 3, cy + 2), (x + w - 6, cy - 12),
                      (x + w - 6, cy + 10)], fill=(120, 120, 130))
        for yy in (cy + 12, cy + 20):
            draw.arc([x + 6, yy, x + 30, yy + 10], 180, 360, fill=BLUE,
                     width=3)
            draw.arc([x + w // 2, yy, x + w // 2 + 24, yy + 10], 180, 360,
                     fill=BLUE, width=3)
    elif kind == "dove":  # truce
        draw.ellipse([cx - 16, cy - 6, cx + 16, cy + 10], fill=(255, 255, 255),
                     outline=NAVY, width=2)
        draw.polygon([(cx + 10, cy - 6), (cx + 26, cy - 16), (cx + 22, cy + 2)],
                     fill=(255, 255, 255))
        draw.ellipse([cx + 12, cy - 8, cx + 18, cy - 2], fill=NAVY)
        draw.line([(cx - 4, cy + 12), (cx - 4, cy + 22)], fill=GREEN, width=2)
        draw.ellipse([cx - 10, cy + 20, cx + 2, cy + 26], fill=LEAF)


def lead_card(draw, x, y, w, h, color, kicker, num, headline, deck, tagname,
              scene):
    draw.rounded_rectangle([x + 2, y + 3, x + w + 2, y + h + 3], radius=10,
                           fill=(238, 229, 211))
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=CARD,
                           outline=LINE, width=2)
    # scene band across the top
    sh = 88
    draw.rectangle([x + 2, y + 2, x + w - 2, y + sh], fill=(250, 241, 226))
    scene(draw, x, y + 2, w, sh)
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10, outline=LINE,
                           width=2)
    tag(draw, x + w - 78, y + sh + 8, tagname, TAG_COLORS[tagname])
    ty = y + sh + 8
    draw.text((x + 12, ty), kicker, font=F_B(13), fill=color)
    ty += 20
    hl = wrap(draw, headline, F_B(22), w - 24)
    ty = text_block(draw, (x + 12, ty), hl, F_B(22), INK, 26)
    cap = wrap(draw, deck, F_R(13), w - 24)
    text_block(draw, (x + 12, ty + 4), cap, F_R(13), (60, 60, 60), 17)
    # story number badge, on the scene band's bottom-left corner
    draw.ellipse([x + 12, y + sh - 30, x + 34, y + sh - 8], fill=color)
    tw = draw.textlength(num, font=F_B(13))
    draw.text((x + 23 - tw / 2, y + sh - 27), num, font=F_B(13),
              fill=(255, 255, 255))


def medium_card(draw, x, y, w, h, color, num, kicker, headline, caption,
                tagname, kind, tint):
    draw.rounded_rectangle([x + 2, y + 2, x + w + 2, y + h + 2], radius=8,
                           fill=(238, 229, 211))
    draw.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=CARD,
                           outline=LINE, width=1)
    draw.rectangle([x + 2, y + 2, x + w - 2, y + 18], fill=color)
    draw.text((x + 8, y + 4), f"{num}  •  {kicker}", font=F_B(11),
              fill=(255, 255, 255))
    tw_tag = draw.textlength(tagname, font=F_B(10)) + 10
    tag(draw, x + w - 8 - tw_tag, y + 3, tagname, TAG_COLORS[tagname])
    sw = 74
    mini(draw, kind, x + w - sw - 6, y + 24, sw, h - 30, tint)
    tw = w - sw - 18
    hl = wrap(draw, headline, F_B(15), tw)
    ty = text_block(draw, (x + 8, y + 24), hl, F_B(15), INK, 17)
    cap = wrap(draw, caption, F_R(11), tw)
    text_block(draw, (x + 8, ty + 2), cap, F_R(11), (60, 60, 60), 13)


def draw_map(draw, x, y, w, h, pins):
    """Schematic dotted world map with numbered pins (approximate)."""
    draw.rectangle([x, y, x + w, y + h], fill=(243, 237, 222),
                   outline=LINE, width=1)
    # dotted grid over the whole map
    for gx in range(x + 8, x + w - 4, 9):
        for gy in range(y + 8, y + h - 4, 9):
            draw.ellipse([gx, gy, gx + 2, gy + 2], fill=(214, 205, 185))
    # continent blobs (schematic)
    blobs = [
        [(18, 22), (62, 14), (92, 30), (78, 62), (48, 66), (22, 48)],
        [(66, 66), (92, 64), (98, 94), (82, 114), (70, 94)],
        [(128, 18), (152, 12), (162, 32), (146, 44), (130, 38)],
        [(132, 46), (162, 42), (172, 64), (158, 92), (140, 78), (128, 58)],
        [(166, 10), (232, 8), (256, 30), (240, 58), (206, 70), (176, 50),
         (164, 30)],
        [(238, 94), (262, 90), (266, 106), (244, 110)],
    ]
    for poly in blobs:
        pts = [(x + px, y + py) for px, py in poly]
        draw.polygon(pts, fill=(200, 214, 192), outline=(165, 175, 155))
    # pins
    for (px, py, num, col) in pins:
        draw.ellipse([x + px - 8, y + py - 8, x + px + 8, y + py + 8],
                     fill=col, outline=(255, 255, 255), width=2)
        tw = draw.textlength(num, font=F_B(9))
        draw.text((x + px - tw / 2, y + py - 6), num, font=F_B(9),
                  fill=(255, 255, 255))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    d.rectangle([0, 0, W, 96], fill=NAVY)
    # wavy gold divider instead of a hard rule
    import math
    wave = [(xx, 98 + 2 * math.sin(xx / 38.0)) for xx in range(0, W + 1, 6)]
    d.line(wave, fill=GOLD, width=3, joint="curve")
    d.text((24, 10), "The World in One Day", font=F_SERIF_B(20), fill=GOLD)
    right = "30 STORIES  •  7 REGIONS  •  ALL FROM THIS ONE DAY"
    d.text((W - 24 - d.textlength(right, font=F_B(14)), 12), right,
           font=F_B(14), fill=(255, 255, 255))
    tagline = "take a breath — here's the day"
    d.text((W - 24 - d.textlength(tagline, font=F_SERIF(13)), 36), tagline,
           font=F_SERIF(13), fill=(255, 214, 150))
    d.text((24, 26), "Tuesday 24 November 2026", font=F_SERIF_B(46),
           fill=(255, 255, 255))
    d.text((24, 78),
           "COP31's collapse: what now?  •  Huang is back at Nvidia  •  "
           "Ukraine sinks a Russian warship in Libya",
           font=F_SERIF(13), fill=(255, 214, 170))
    # little drawn sun, bottom-right of the masthead (clear of the numbers)
    sx, sy = 942, 82
    for ang in range(0, 360, 45):
        r1, r2 = 12, 17
        x1 = sx + r1 * math.cos(math.radians(ang))
        y1 = sy + r1 * math.sin(math.radians(ang))
        x2 = sx + r2 * math.cos(math.radians(ang))
        y2 = sy + r2 * math.sin(math.radians(ang))
        d.line([(x1, y1), (x2, y2)], fill=GOLD, width=2)
    d.ellipse([sx - 9, sy - 9, sx + 9, sy + 9], fill=GOLD)

    # ---- The day in numbers ----
    nums = [("31.5%", "Nvidia jump"), ("24", "dead, Cikande"),
            ("50m", "children vaccinated"), ("$84bn", "EU tariff threat"),
            ("100", "missing, Himalayas"), ("6", "firms blacklisted")]
    ny, nh = 100, 36
    cw = (W - 48) // 6
    for i, (big, small) in enumerate(nums):
        cx0 = 24 + i * cw
        d.text((cx0 + cw // 2, ny), big, font=F_B(24), fill=RED_D,
               anchor="ma")
        d.text((cx0 + cw // 2, ny + 26), small, font=F_R(10), fill=GREY,
               anchor="ma")
        if i:
            d.line([cx0, ny + 4, cx0, ny + nh - 4], fill=LINE, width=1)

    # ---- Region bar ----
    ry = 140
    regions = [("WORLD", 4, NAVY), ("EUROPE", 3, BLUE),
               ("MID EAST", 2, RED), ("AFRICA", 6, (160, 120, 60)),
               ("ASIA", 9, GREEN), ("AMERICAS", 4, TEAL),
               ("OCEANIA", 2, PURPLE)]
    total = 30
    rx = 24
    for name, n, col in regions:
        wseg = (W - 48) * n // total
        d.rounded_rectangle([rx, ry, rx + wseg - 2, ry + 20], radius=10,
                            fill=col)
        lab = f"{name} {n}"
        d.text((rx + (wseg - 2) // 2, ry + 4), lab, font=F_B(10),
               fill=(255, 255, 255), anchor="ma")
        rx += wseg

    # ---- The day in UTC ----
    uy = 164
    d.rectangle([0, uy, W, uy + 22], fill=NAVY_D)
    d.text((24, uy + 4), "THE DAY IN UTC", font=F_B(12), fill=GOLD)
    utc = ("00:52  Megaspeed blacklisted   •   01:03  Pentagon rebukes "
           "Canada   •   02:37  China death sentence   •   04:20  Libya "
           "seeks UN probe   •   05:00  ICE arrests")
    d.text((24 + d.textlength("THE DAY IN UTC   ", font=F_B(12)), uy + 5),
           utc, font=F_R(11), fill=(255, 255, 255))

    # ---- Three lead stories ----
    ly, lh = 190, 240
    lw = (W - 48 - 2 * 10) // 3
    lead_card(d, 24, ly, lw, lh, RED, "WORLD  •  CLIMATE", "1",
              "After COP31 collapsed",
              "Two days after the talks ended with no deal, the UN chief "
              "says he is deeply disappointed — and the world asks what "
              "comes next.",
              "ONGOING",
              lambda dr, sx, sy, sw, sh: draw_globe(dr, sx + sw // 2,
                                                    sy + sh // 2 + 4, 44))
    lead_card(d, 24 + lw + 10, ly, lw, lh, GREEN,
              "TECH  •  CHIPS", "2",
              "Huang is back; US blacklists Megaspeed",
              "Nvidia reinstates its CEO after Trump pressed the board; "
              "hours later Washington puts Megaspeed and six affiliates "
              "on its Entity List. Shares jump 31.5%.",
              "REPORTED", scene_chip_chart)
    lead_card(d, 24 + 2 * (lw + 10), ly, lw, lh, BLUE,
              "EUROPE  •  WAR", "3",
              "Ukraine sinks Russian warship in Libya",
              "Seven sea drones hit the 344-ft corvette Merkury at "
              "Benghazi; she sank, a helicopter aboard destroyed. "
              "Zelensky: 'exemplary'. Kyiv also urges four-party talks.",
              "REPORTED", scene_ship_attack)

    # ---- Twelve medium stories, 4 x 3 ----
    med = [
        ("4", "ASIA  •  TRADE", "Japan deal lifts Nikkei",
         "Trump's Japan pact lifts the Nikkei.",
         "REPORTED", "sun_chart", GREEN_L),
        ("5", "WORLD  •  TRADE", "Indonesia deal; EU tariff threat",
         "Indonesia pact sealed; EU readies $84bn tariffs.",
         "REPORTED", "ship", TEAL_L),
        ("6", "AMERICAS", "Pentagon rebukes Canada",
         "US accuses Ottawa of defence shortfalls.",
         "REPORTED", "jet", BLUE_L),
        ("7", "ASIA  •  CHINA", "China death sentence",
         "Official Ma sentenced to death for spying.",
         "REPORTED", "gavel", (240, 235, 220)),
        ("8", "ASIA  •  KOREA", "Russian jets in S. Korea zone",
         "Seoul scrambles jets.",
         "REPORTED", "radar", BLUE_L),
        ("9", "ASIA  •  DISASTER", "Factory fire: rescue goes on",
         "24 dead in Cikande; ~30 missing, search goes on.",
         "ONGOING", "flame", ORANGE_L),
        ("10", "ASIA  •  HEALTH", "Bangladesh vaccinates 50m",
         "Month-long typhoid drive begins nationwide.",
         "REPORTED", "vial", BLUE_L),
        ("11", "ASIA  •  INDIA", "India holds 3rd in power index",
         "New Delhi keeps third in Asia Power Index.",
         "REPORTED", "bars", GREEN_L),
        ("12", "OCEANIA  •  SPORT", "India–NZ Test ends in a draw",
         "First Test in Wellington drawn after five days.",
         "OFFICIAL", "cricket", GREEN_L),
        ("13", "ASIA  •  FLOOD", "Himalayan flood: 4 dead",
         "Mud and debris tear down a valley; ~100 missing.",
         "REPORTED", "waves", BLUE_L),
        ("14", "ASIA  •  INDIA", "Ex-lawmaker jailed for life",
         "Prajwal Revanna gets life in prison for rape.",
         "OFFICIAL", "gavel", (240, 235, 220)),
        ("15", "ASIA  •  TRUCE", "Thai–Cambodia truce holds",
         "Fighting on hold after a border truce.",
         "REPORTED", "dove", GREEN_L),
    ]
    colors = {"ASIA": GREEN, "WORLD": NAVY, "AMERICAS": TEAL,
              "OCEANIA": PURPLE}
    mw = (W - 48 - 3 * 8) // 4
    mh = 86
    my0 = 438
    for i, (num, kick, head, cap, tg, kind, tint) in enumerate(med):
        col = colors.get(kick.split("  •  ")[0], NAVY)
        mx = 24 + (i % 4) * (mw + 8)
        my = my0 + (i // 4) * (mh + 6)
        medium_card(d, mx, my, mw, mh, col, num, kick, head, cap, tg, kind,
                    tint)

    # ---- Map + also list ----
    by = 714
    d.text((24, by), "WHERE IT HAPPENED", font=F_B(15), fill=NAVY)
    d.text((24 + d.textlength("WHERE IT HAPPENED  ", font=F_B(15)), by + 2),
           "pins approximate", font=F_R(11), fill=GREY)
    map_x, map_y, map_w, map_h = 24, by + 22, 300, 128
    # pins placed on the schematic continents: NA 18-92, SA 66-98,
    # Europe 128-162, Africa 128-172, Asia 164-256, Oceania 238-266
    pins = [(168, 32, "1", RED), (55, 45, "2", GREEN),
            (152, 58, "3", BLUE), (255, 45, "4", GREEN),
            (238, 68, "5", NAVY), (58, 26, "6", TEAL),
            (225, 40, "7", GREEN), (245, 38, "8", GREEN),
            (228, 74, "9", ORANGE), (230, 56, "10", GREEN),
            (212, 60, "11", GREEN), (262, 105, "12", PURPLE),
            (222, 46, "13", GREEN), (210, 66, "14", GREEN),
            (238, 60, "15", GREEN)]
    draw_map(d, map_x, map_y, map_w, map_h, pins)
    ax = 344
    d.text((ax, by), "ALSO ON TUESDAY 24 NOVEMBER", font=F_B(15), fill=NAVY)
    also = [
        ("16", "Niger coup: Europe readies evacuations"),
        ("17", "South Africans vote as ANC faces anger"),
        ("18", "RSF drones hit Sudan power grid; blackouts"),
        ("19", "DRC president signs constitutional reform"),
        ("20", "Kenya discharges last Ebola patient"),
        ("21", "Libya asks UN to probe Ukraine troops claim"),
        ("22", "Israeli strike kills 3 at Gaza police post"),
        ("23", "US sanctions Iran's underground banks"),
        ("24", "FAA ends O'Hare ground stop"),
        ("25", "EU hunts new ECB chief as Lagarde quits"),
        ("26", "Norway court voids disputed oil licences"),
        ("27", "Australia treats AI as foreign policy"),
        ("28", "UN chief: agree AI rules within a year"),
        ("29", "ICE agents arrest people at Seattle airport"),
        ("30", "Mexico to prosecute 'El Chapo Isidro'"),
    ]
    ay = by + 24
    col_w = 330
    for i, (num, txt) in enumerate(also):
        cx = ax + (i // 8) * col_w
        cy = ay + (i % 8) * 19
        d.text((cx, cy), num, font=F_B(12), fill=RED)
        d.text((cx + 24, cy), txt, font=F_R(12), fill=INK)

    # ---- Date check ----
    dy = 892
    d.rounded_rectangle([24, dy, W - 24, dy + 76], radius=6, fill=(255, 255, 255),
                        outline=RED, width=2)
    d.text((36, dy + 8), "DATE CHECK", font=F_B(14), fill=RED)
    dc = ("Every story here happened, or was first reported, on Tue 24 "
          "Nov 2026 (UTC) — except two announced Mon 23 Nov that still "
          "lead today's briefs: the Merkury sinking and Huang's return. "
          "Left out: COP31 collapse (Sun)  •  Liverpool 4–0 Man Utd (Sun)  •  "
          "Verstappen wins Las Vegas GP (Sun)  •  Hong Kong 98.79% turnout "
          "(Sun)  •  India 720/9 (Sun)  •  'El Chapo Isidro' captured "
          "(Fri–Sat 21 Nov).")
    lines = wrap(d, dc, F_R(12), W - 48 - 24)
    text_block(d, (36, dy + 28), lines, F_R(12), INK, 15)

    # ---- Footer ----
    d.text((W // 2, 976),
           "HOW SURE:  REPORTED = carried by the day's wires   •   CLAIM = one "
           "side's account, labelled as such   •   OFFICIAL = an official "
           "result or statement   •   ONGOING = still unfolding",
           font=F_R(11), fill=GREY, anchor="ma")
    d.text((W // 2, 992),
           "Sources: Reuters  •  AP  •  CNN  •  WSJ  •  NY Post  •  The "
           "Times  •  FT  •  "
           "BBC  •  AFP  •  Access24  •  Daily Summary of World  •  C54  •  "
           "Careerindia",
           font=F_R(11), fill=GREY, anchor="ma")
    d.text((W // 2, 1008),
           "Scenes and map drawn in code, not photographs  •  The day, "
           "summed up gently — Tuesday 24 November 2026",
           font=F_R(11), fill=GREY, anchor="ma")

    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, img.size, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
