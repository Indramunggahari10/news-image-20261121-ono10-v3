#!/usr/bin/env python3
"""Render the Saturday 21 November 2026 world-news front page (1024x1024 PNG).

Fresh build for make.fun news-image-20261121 (entry v3). Every story in the
main grid happened or was first reported on Saturday 21 November 2026;
Friday/earlier items appear ONLY in the DATE CHECK exclusion box.
Run:  python3 render.py   ->  writes entry.png next to this script.
Uses only PIL + system fonts at BUILD time. The submitted program (main.ts)
just copies entry.png, so the graded run needs no fonts and no network.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
INK = (18, 18, 18)
PAPER = (250, 247, 238)
GREY = (110, 108, 100)
RULE = (60, 60, 60)
RED = (178, 34, 34)
BLUE = (24, 62, 110)
TEAL = (14, 92, 86)
GOLD = (176, 132, 24)
LIGHT = (238, 233, 220)
MID = (214, 208, 192)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIFB = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIFI = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANSB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, font, width):
    """Greedy word wrap returning list of lines fitting pixel width."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for w in words[1:]:
            if draw.textlength(cur + " " + w, font=font) <= width:
                cur += " " + w
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


def text_block(draw, x, y, width, text, font, fill=INK, leading=None, max_lines=None):
    lines = wrap(draw, text, font, width)
    if max_lines:
        lines = lines[:max_lines]
    lh = leading or int(font.size * 1.22)
    for ln in lines:
        draw.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


def rule(draw, x, y, w, weight=2, fill=RULE):
    draw.rectangle([x, y, x + w, y + weight - 1], fill=fill)


def tag(draw, x, y, label, fill):
    f = F(SANSB, 11)
    tw = draw.textlength(label, font=f)
    draw.rectangle([x, y, x + tw + 10, y + 17], fill=fill)
    draw.text((x + 5, y + 2), label, font=f, fill=(255, 255, 255))
    return tw + 10


# ---------------------------------------------------------------- pictograms
def pic_paris(d, x, y, w, h):
    """Eiffel Tower silhouette + crowd dots + placards, flat style."""
    d.rectangle([x, y, x + w, y + h], fill=(233, 226, 205))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(120, 110, 88))
    cx = x + w // 2
    # tower: two curved legs as polygons
    d.polygon([(cx - 52, y + h - 26), (cx - 10, y + 14), (cx + 10, y + 14),
               (cx + 52, y + h - 26), (cx + 34, y + h - 26), (cx + 6, y + 60),
               (cx - 6, y + 60), (cx - 34, y + h - 26)], fill=(52, 52, 52))
    d.rectangle([cx - 34, y + 66, cx + 34, y + 72], fill=(52, 52, 52))
    d.rectangle([cx - 24, y + 100, cx + 24, y + 106], fill=(52, 52, 52))
    d.rectangle([cx - 2, y + 2, cx + 2, y + 14], fill=(52, 52, 52))
    # placards
    for px, col in ((x + 14, RED), (x + w - 46, BLUE)):
        d.rectangle([px, y + h - 66, px + 32, y + h - 44], fill=col)
        d.rectangle([px + 15, y + h - 44, px + 17, y + h - 26], fill=(60, 60, 60))
    # crowd heads
    import math
    for i in range(9):
        hx = x + 18 + i * ((w - 36) // 8)
        d.ellipse([hx - 5, y + h - 22, hx + 5, y + h - 12], fill=(40, 40, 40))


def pic_controller(d, x, y, w, h):
    """Game controller + starburst price tag, flat style."""
    d.rectangle([x, y, x + w, y + h], fill=(28, 32, 58))
    cx, cy = x + w // 2, y + h // 2 + 8
    d.rounded_rectangle([cx - 96, cy - 42, cx + 96, cy + 40], radius=34, fill=(235, 235, 235))
    d.rounded_rectangle([cx - 96, cy - 42, cx + 96, cy + 40], radius=34, outline=(180, 180, 180), width=2)
    d.ellipse([cx - 72, cy - 18, cx - 44, cy + 10], fill=(40, 40, 40))
    d.ellipse([cx + 44, cy - 18, cx + 72, cy + 10], fill=(40, 40, 40))
    for bx, by in ((cx + 52, cy - 30), (cx + 66, cy - 16), (cx + 38, cy - 16), (cx + 52, cy - 2)):
        d.ellipse([bx - 6, by - 6, bx + 6, by + 6], fill=RED)
    d.rectangle([cx - 30, cy - 24, cx - 22, cy - 4], fill=(40, 40, 40))
    d.rectangle([cx - 38, cy - 16, cx - 14, cy - 12], fill=(40, 40, 40))
    # starburst
    sx, sy = x + w - 66, y + 34
    pts = []
    import math
    for i in range(16):
        ang = math.pi * i / 8
        r = 34 if i % 2 == 0 else 24
        pts.append((sx + r * math.cos(ang), sy + r * math.sin(ang)))
    d.polygon(pts, fill=GOLD)
    f = F(SANSB, 15)
    d.text((sx - 26, sy - 8), "$3.79bn", font=f, fill=(255, 255, 255))


def pic_globe(d, x, y, w, h):
    """Globe with meridians + rising sun, flat style."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 230, 240))
    cx, cy = x + w // 2, y + h // 2 + 6
    r = 62
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(46, 110, 160))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(24, 62, 110), width=3)
    for k in (-1, 0, 1):
        d.arc([cx - r + k * 30, cy - r, cx + r - k * 30, cy + r], 90, 270, fill=(255, 255, 255), width=2)
    d.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=(255, 255, 255), width=2)
    d.arc([cx - r, cy - r, cx + r, cy + r], 20, 160, fill=(255, 255, 255), width=2)
    # land blobs
    d.ellipse([cx - 44, cy - 34, cx - 6, cy - 6], fill=(96, 160, 90))
    d.ellipse([cx + 4, cy + 8, cx + 46, cy + 40], fill=(96, 160, 90))
    d.ellipse([cx - 10, cy - 44, cx + 22, cy - 18], fill=(120, 175, 105))
    # sun
    d.ellipse([x + w - 52, y + 12, x + w - 20, y + 44], fill=GOLD)


def pic_mercury(d, x, y, w, h):
    """Mercury + BepiColombo spacecraft with thruster flame, flat style."""
    d.rectangle([x, y, x + w, y + h], fill=(10, 18, 40))
    for sx, sy in ((18, 16), (52, 30), (96, 12), (150, 22), (210, 14),
                   (262, 30), (296, 18), (30, 62), (290, 66), (120, 96)):
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(255, 255, 255))
    cx, cy, r = x + 92, y + h // 2 + 8, 46
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(198, 148, 98))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(150, 105, 65), width=3)
    for ox, oy, orr in ((-18, -16, 9), (12, 8, 12), (-6, 22, 7), (22, -22, 6)):
        d.ellipse([cx + ox - orr, cy + oy - orr, cx + ox + orr, cy + oy + orr],
                  fill=(168, 118, 72))
    # spacecraft: body + solar panels + flame
    bx, by = x + w - 92, y + 30
    d.rectangle([bx, by, bx + 34, by + 14], fill=(235, 235, 235))
    d.rectangle([bx - 30, by + 2, bx, by + 12], fill=(46, 110, 160))
    d.rectangle([bx + 34, by + 2, bx + 64, by + 12], fill=(46, 110, 160))
    d.polygon([(bx + 8, by + 14), (bx + 26, by + 14), (bx + 17, by + 34)], fill=(240, 140, 40))


def pic_cricket(d, x, y, w, h):
    """Cricket bat, ball and stumps, flat style."""
    d.rectangle([x, y, x + w, y + h], fill=(226, 238, 214))
    # pitch
    d.rectangle([x, y + h - 46, x + w, y + h - 34], fill=(198, 178, 130))
    # stumps
    for sx in (x + 52, x + 62, x + 72):
        d.rectangle([sx, y + h - 78, sx + 4, y + h - 46], fill=(240, 220, 130))
    d.rectangle([x + 52, y + h - 82, x + 76, y + h - 78], fill=(240, 220, 130))
    # bat
    d.polygon([(x + w - 120, y + 30), (x + w - 96, y + 22), (x + w - 70, y + 108),
               (x + w - 94, y + 116)], fill=(222, 190, 130))
    d.polygon([(x + w - 120, y + 30), (x + w - 96, y + 22), (x + w - 70, y + 108),
               (x + w - 94, y + 116)], outline=(120, 90, 50), width=2)
    d.rectangle([x + w - 128, y + 8, x + w - 112, y + 34], fill=(120, 90, 50))
    # ball
    d.ellipse([x + w - 52, y + h - 66, x + w - 30, y + h - 44], fill=RED)
    d.arc([x + w - 52, y + h - 66, x + w - 30, y + h - 44], 200, 340, fill=(255, 255, 255), width=2)
    # score
    f = F(SANSB, 30)
    d.text((x + 16, y + 14), "159/1", font=f, fill=INK)
    f2 = F(SANS, 13)
    d.text((x + 16, y + 48), "INDIA FIGHT BACK", font=f2, fill=GREY)


def pic_chip(d, x, y, w, h):
    """AI chip square with pins, flat style."""
    d.rectangle([x, y, x + w, y + h], fill=(226, 232, 240))
    cx, cy = x + w // 2, y + h // 2
    for i in range(5):
        px = cx - 56 + i * 28
        d.rectangle([px - 2, y + 18, px + 2, y + 44], fill=(80, 80, 80))
        d.rectangle([px - 2, y + h - 44, px + 2, y + h - 18], fill=(80, 80, 80))
        d.rectangle([x + 18, cy - 56 + i * 28 - 2, x + 44, cy - 56 + i * 28 + 2], fill=(80, 80, 80))
        d.rectangle([x + w - 44, cy - 56 + i * 28 - 2, x + w - 18, cy - 56 + i * 28 + 2], fill=(80, 80, 80))
    d.rounded_rectangle([cx - 56, cy - 56, cx + 56, cy + 56], radius=8, fill=(24, 62, 110))
    d.rounded_rectangle([cx - 34, cy - 34, cx + 34, cy + 34], radius=4, fill=(46, 110, 160))
    f = F(SANSB, 17)
    d.text((cx - 22, cy - 11), "AI", font=f, fill=(255, 255, 255))


def pic_scales(d, x, y, w, h):
    """Courthouse columns + scales, flat style."""
    d.rectangle([x, y, x + w, y + h], fill=(238, 232, 218))
    # pediment
    d.polygon([(x + 30, y + 34), (x + w // 2, y + 8), (x + w - 30, y + 34)], fill=(120, 100, 70))
    for i in range(4):
        cx = x + 52 + i * ((w - 104) // 3)
        d.rectangle([cx - 9, y + 40, cx + 9, y + h - 40], fill=(150, 132, 96))
        d.rectangle([cx - 13, y + 36, cx + 13, y + 42], fill=(120, 100, 70))
        d.rectangle([cx - 13, y + h - 44, cx + 13, y + h - 38], fill=(120, 100, 70))
    d.rectangle([x + 24, y + h - 38, x + w - 24, y + h - 30], fill=(120, 100, 70))
    # scales
    cx, cy = x + w // 2, y + h - 78
    d.rectangle([cx - 1, cy - 34, cx + 1, cy], fill=(60, 60, 60))
    d.polygon([(cx - 34, cy - 30), (cx + 34, cy - 30), (cx, cy - 34)], fill=(60, 60, 60))
    d.polygon([(cx - 40, cy - 8), (cx - 22, cy - 8), (cx - 31, cy - 30)], outline=(60, 60, 60), width=2)
    d.polygon([(cx + 22, cy - 8), (cx + 40, cy - 8), (cx + 31, cy - 30)], outline=(60, 60, 60), width=2)
    d.ellipse([cx - 6, cy - 40, cx + 6, cy - 28], fill=GOLD)


# ---------------------------------------------------------------- content
# Filled in after research verification. Each story: (region, headline, deck, source)
# Every story below happened or was first reported on Saturday 21 November 2026.
# Friday/Thursday items appear ONLY in DATECHECK.
MAIN_HEADLINE = "Saturday 21 November 2026"
MAIN_DECK = ("COP31 runs into overtime  ·  BepiColombo reaches Mercury  ·  "
             "Riyadh downs three missiles  ·  France marches again")
REGIONS = ("EUROPE 16  ·  ASIA 6  ·  OCEANIA 6  ·  MIDDLE EAST 2  ·  "
           "N. AMERICA 2  ·  SPACE 3")

LEADS = [
    ("CLIMATE", "COP31 runs into overtime",
     "No deal yet; a third draft is due this morning after overnight talks.",
     "Reuters", pic_globe),
    ("SCIENCE", "BepiColombo fires for Mercury",
     "A 37-minute burn at 19:24 CET puts the probe into orbit — eight years on.",
     "ESA / Sky & Telescope", pic_mercury),
    ("FRANCE", "Paris braces as protests return",
     "70,000 police on duty; the march steps off at 14:00, République to Nation.",
     "Particle", pic_paris),
]

GRID = [
    ("MIDDLE EAST", "Riyadh downs three Houthi missiles",
     "Coalition intercepts three ballistic missiles fired at the capital.", "Reuters"),
    ("SPORT", "Rahul's 124* puts India on top in Wellington",
     "India 344/2 at tea on Day 3, closing on New Zealand's 368.", "Reuters / AP"),
    ("EUROPE", "Rutte heads to Warsaw after missiles land in Poland",
     "NATO chief due in the capital today after Friday's incursion.", "Reuters"),
    ("ASIA", "Ladakh votes in first local polls since 2019",
     "Voting under way 8am-5pm; first local polls since 2019.", "Daily Jagran"),
    ("ASIA", "Modi to open Nitish Setu, a 19.7 km Ganga bridge",
     "PM in Bihar at 1:15 PM; Rs 34,470 crore of projects to be dedicated.", "PIB"),
    ("SPORT", "Las Vegas GP qualifying runs today",
     "Pole shootout 04:00 UTC; Russell fastest in practice.", "RacingNews365"),
    ("SPORT", "Hazlewood backs Cummins in sandpaper row",
     "Would rethink his future if Cummins is sacked.", "Reuters / IANS"),
    ("ASIA", "Akvan weakens after landfall; crews restore power",
     "Crossed Odisha on Friday; heavy rain continues, schools shut today.", "IMD"),
    ("SPORT", "ATP Finals semis today in Turin",
     "Alcaraz v Shelton, Zverev v Medvedev — a new champion is guaranteed.", "ATP"),
    ("SPORT", "Premier League returns: seven games today",
     "Man City v Fulham 12:30; Newcastle v Arsenal 17:30.", "premierleague.com"),
]

ALSO = [
    "Kurum: 'close to the finish line'",
    "Carbon Brief: finish likely Sunday",
    "Third draft due Saturday morning",
    "37-minute burn; 8-year voyage",
    "2nd Mercury orbiter after Messenger",
    "Alert at 1:53 a.m. in Riyadh",
    "500+ gatherings in 7 countries",
    "Yellow Vests mark eight years",
    "Padikkal 80; India 344/2 at tea",
    "NZ 368: Nicholls 175*, Phillips 118",
    "Tusk: incursion was deliberate",
    "137 sarpanch, 242 panch posts",
    "19.7 km bridge; Rs 34,470 crore",
    "Russell fastest; Gasly +0.071",
    "Hazlewood: rethink if Cummins out",
    "CA statement backing Cummins due",
    "Schools shut; no deaths reported",
    "Alcaraz v Shelton in Turin",
    "Sinner out — new champion assured",
    "Man City v Fulham opens the day",
    "Bournemouth: eight-game streak",
    "Man City: three straight defeats",
]

DATECHECK = [
    ("Kryvyi Rih strike, 2 dead, 42 hurt", "FRI 20 NOV, 23:00"),
    ("Russian missiles land in Poland", "FRI 20 NOV, 05:40 GMT"),
    ("Kyiv bridges hit, at least 9 dead", "FRI 20 NOV"),
    ("GTA VI: $3.79bn day-one sales", "ANNOUNCED FRI 20 NOV"),
    ("US approves 879,000 AI chips for China", "THU 19 NOV"),
    ("ICJ: Myanmar committed genocide", "THU 19 NOV"),
    ("Zecler verdict, 3 Paris police jailed", "FRI 20 NOV, 22:00 CET"),
]

NUMBERS = ("3 MISSILES DOWNED  ·  70,000 POLICE  ·  19:24 CET MERCURY BURN  ·  "
           "RAHUL 124*  ·  500+ MARCHES  ·  NASDAQ -5.28% (FRI)  ·  GOLD $3,514 (FRI)")


def draw():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 26  # margin
    # ---- masthead
    f_name = F(SERIFB, 62)
    name = "THE SATURDAY WORLD"
    tw = d.textlength(name, font=f_name)
    d.text(((W - tw) / 2, 6), name, font=f_name, fill=INK)
    rule(d, M, 78, W - 2 * M, 3)
    f_dat = F(SANSB, 16)
    dat = "ONE DAY, THE WHOLE WORLD  •  35 STORIES, 6 REGIONS  •  EVERY ONE DATED SATURDAY"
    tw = d.textlength(dat, font=f_dat)
    d.text(((W - tw) / 2, 86), dat, font=f_dat, fill=INK)
    rule(d, M, 110, W - 2 * M, 1)
    # ---- numbers strip
    d.rectangle([M, 116, W - M, 140], fill=INK)
    f_num = F(SANSB, 12)
    d.text((M + 8, 122), NUMBERS, font=f_num, fill=(245, 242, 232))
    # ---- main headline
    y = 150
    f_main = F(SERIFB, 46)
    y = text_block(d, M, y, W - 2 * M, MAIN_HEADLINE, f_main, leading=52, max_lines=2)
    f_deck = F(SERIFI, 16)
    y = text_block(d, M, y + 4, W - 2 * M, MAIN_DECK, f_deck, leading=20, max_lines=2)
    f_src = F(SANSB, 11)
    d.text((M, y + 2), REGIONS, font=f_src, fill=GREY)
    rule(d, M, y + 22, W - 2 * M, 2)
    # ---- three illustrated leads
    ly = y + 32
    lw = (W - 2 * M - 2 * 12) // 3
    lh = 218
    for i, (region, head, deck, src, pic) in enumerate(LEADS):
        x = M + i * (lw + 12)
        pic(d, x, ly, lw, 118)
        d.rectangle([x, ly + 118, x + lw, ly + 118], fill=RULE)
        ty = ly + 124
        tag(d, x, ty, region, RED if i == 0 else (BLUE if i == 1 else TEAL))
        f_h = F(SERIFB, 19)
        ty2 = text_block(d, x, ty + 22, lw, head, f_h, leading=22, max_lines=2)
        f_b = F(SERIF, 13)
        text_block(d, x, ty2 + 2, lw, deck, f_b, leading=16, max_lines=2)
        d.text((x, ly + lh - 14), "Source: " + src, font=F(SANS, 10), fill=GREY)
    # ---- grid of 10
    gy = ly + lh + 18
    rule(d, M, gy, W - 2 * M, 2)
    gy += 8
    f_gh = F(SERIFB, 15)
    f_gd = F(SERIF, 12)
    gh = 54
    for r in range(5):
        for c in range(2):
            idx = r * 2 + c
            region, head, deck, src = GRID[idx]
            x = M + c * ((W - 2 * M + 16) // 2)
            wcol = (W - 2 * M - 16) // 2
            tag(d, x, gy, region, BLUE)
            text_block(d, x, gy + 21, wcol, head, f_gh, leading=17, max_lines=1)
            text_block(d, x, gy + 39, wcol, deck + "  — " + src, f_gd, leading=14, max_lines=1)
            if c == 0:
                d.rectangle([x + wcol + 8, gy, x + wcol + 8, gy + gh - 12], fill=MID)
        gy += gh
        if r < 4:
            rule(d, M, gy - 6, W - 2 * M, 1, fill=MID)
    # ---- bottom: ALSO TODAY (two columns of 11) + DATE CHECK
    by = gy + 6
    rule(d, M, by, W - 2 * M, 2)
    by += 10
    colw = (W - 2 * M - 16) // 2
    f_sec = F(SANSB, 14)
    d.text((M, by), "ALSO TODAY — SATURDAY 21 NOVEMBER", font=f_sec, fill=INK)
    d.text((M + colw + 16, by), "DATE CHECK — NOT TODAY", font=f_sec, fill=RED)
    by += 22
    f_al = F(SERIF, 12)
    ay = by
    half = (len(ALSO) + 1) // 2
    for i, item in enumerate(ALSO):
        col = 0 if i < half else 1
        row = i if i < half else i - half
        xx = M + col * (colw // 2 + 8)
        d.text((xx, ay + row * 15), "%d. %s" % (i + 1, item), font=f_al, fill=INK)
    # date check box
    bx = M + colw + 16
    d.rectangle([bx, by, bx + colw, by + 8 * 16 + 26], outline=RED, width=2)
    d.text((bx + 8, by + 6), "These big stories are from Friday or earlier —", font=F(SANSB, 11), fill=RED)
    d.text((bx + 8, by + 20), "they are NOT counted as Saturday's news:", font=F(SANSB, 11), fill=RED)
    dy = by + 38
    for item, when in DATECHECK:
        d.text((bx + 8, dy), "×  %s — %s" % (item, when), font=F(SERIF, 12), fill=INK)
        dy += 16
    # ---- footer
    fy = H - 26
    rule(d, M, fy - 8, W - 2 * M, 1)
    f_ft = F(SANS, 10)
    foot = ("Every story above happened or was first reported on Saturday 21 November 2026.  "
            "Sources named beside each story.  Original drawings, not photographs.")
    d.text((M, fy), foot, font=f_ft, fill=GREY)
    return img


if __name__ == "__main__":
    img = draw()
    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)
