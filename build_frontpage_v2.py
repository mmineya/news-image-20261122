#!/usr/bin/env python3
"""Build the dense 1024x1024 front page (v2) for the news-image-20261122 bounty.

35 stories: 3 photo-featured + 32 text tiles in a 4x8 grid.
Composites three AI-generated photographs with PIL.
Run: python3 build_frontpage_v2.py — writes entry.png in this directory.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")

W, H = 1024, 1024
BG = (250, 247, 240)          # newsprint off-white
INK = (17, 17, 17)
GREY = (51, 51, 51)
SEP = (221, 221, 221)
WHITE = (255, 255, 255)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# Tag colours (dark, white text on top).
TAG_COLORS = {
    "CLIMATE": (46, 125, 50),
    "WAR": (122, 31, 31),
    "DIPLOMACY": (122, 31, 31),
    "MIDEAST": (122, 31, 31),
    "MARKETS": (30, 80, 140),
    "SPORT": (27, 94, 32),
    "TECH": (106, 27, 154),
    "SCIENCE": (0, 105, 105),
    "AMERICAS": (27, 42, 74),
    "ASIA": (176, 84, 0),
    "AFRICA": (121, 85, 45),
    "EUROPE": (90, 90, 90),
    "COURT": (17, 17, 17),
    "TRADE": (0, 110, 130),
    "CULTURE": (128, 0, 32),
}

# (headline, summary, tag)
STORIES = [
    # featured 1, 2, 4 (also counted in the 35)
    ("COP31 COLLAPSES",
     "Climate talks end with no deal as EU rejects a text that omits fossil fuels.",
     "CLIMATE"),
    ("TRUMP, XI AND PUTIN MEET",
     "First trilateral summit ends with a nuclear-risk declaration \u2014 but no Ukraine breakthrough.",
     "DIPLOMACY"),
    ("TANKERS HIT BY MINES",
     "Two supertankers struck near the Strait of Hormuz as the Iran\u2013US standoff deepens.",
     "MIDEAST"),
]
GRID_STORIES = [
    ("IRAN STRIKES US BASES IN BAHRAIN",
     "Missiles and drones hit US bases; a civilian facility struck, 2 injured.",
     "MIDEAST"),
    ("MARKETS IN CORRECTION",
     "S&P 500 \u22123.7%, Nasdaq \u22125.3% as the AI sell-off spreads to Asia.",
     "MARKETS"),
    ("WORLD COURT: GENOCIDE",
     "Myanmar ruled responsible for the 2017 Rohingya genocide \u2014 a first for the court.",
     "COURT"),
    ("\u2018EL CHAPO ISIDRO\u2019 CAPTURED",
     "Cartel boss seized in a Sinaloa raid; 11 killed, including four soldiers.",
     "AMERICAS"),
    ("EU\u2013INDONESIA TRADE DEAL",
     "Landmark deal after 10 years scraps tariffs on up to 98.5% of goods.",
     "TRADE"),
    ("KRYVYI RIH STRUCK",
     "Russian missile hits Zelenskyy\u2019s hometown; a boy, 7, and a woman, 20, killed, 60 wounded.",
     "WAR"),
    ("DEMOCRATS TAKE HOUSE",
     "Largest US House majority since 1992 after a North Carolina recount.",
     "AMERICAS"),
    ("SUDAN DRONE ATTACKS",
     "RSF drones kill 4 near Khartoum and damage a UN building.",
     "AFRICA"),
    ("INDONESIA FACTORY FIRE",
     "Candy factory blaze in Cikande kills 3 workers, 36 missing.",
     "ASIA"),
    ("EUROPE PROTESTS",
     "Third straight day of protests over costs and housing.",
     "EUROPE"),
    ("Ukraine sinks Russian corvette at Benghazi",
     "Sea drones sank the Merkury at a Libyan naval base.",
     "WAR"),
    ("Russian strike kills 11 in Dymer",
     "Drone strike collapsed a five-storey block near Kyiv.",
     "WAR"),
    ("Two killed in Gaza; settlers attack West Bank",
     "Israeli forces killed two; settlers torched cars and buildings.",
     "MIDEAST"),
    ("Iran: Hormuz reopening \u2018not difficult\u2019",
     "Tehran says strait reopens if US accepts its conditions.",
     "MIDEAST"),
    ("Nepal PM begins state visit to India",
     "Balendra Shah arrives for two days of talks with Modi.",
     "ASIA"),
    ("India, China hold fresh border talks",
     "Commanders conclude second round over Arunachal frontier tensions.",
     "ASIA"),
    ("Japan economy contracts; BOJ hike looms",
     "Q3 shrank as inflation hit a 2026 high, subsidies lapsed.",
     "ASIA"),
    ("US Army to defy court on Iowa blast",
     "Emergency powers will detonate lead azide despite a court order.",
     "AMERICAS"),
    ("ICE protest in Gilroy; two seized",
     "Masked agents took two at Seattle airport; activists protest.",
     "AMERICAS"),
    ("AI bailout debate; data-centre bill advances",
     "Insiders float taxpayer rescue as deregulation bill reaches House.",
     "AMERICAS"),
    ("Salvadoran troops seize Haiti stadium",
     "Bukele\u2019s force takes Port-au-Prince stadium from gangs.",
     "AMERICAS"),
    ("Belize declares emergency after murders",
     "Seven weekend killings trigger 30-day emergency in 19 areas.",
     "AMERICAS"),
    ("Liverpool thrash Man Utd 4-0",
     "Pochettino\u2019s first match as United boss ends in rout.",
     "SPORT"),
    ("Boca win record third Copa Sudamericana",
     "Boca beat Atletico Mineiro 2-0 in the final.",
     "SPORT"),
    ("Atalanta 4-4 Inter in thriller",
     "Atalanta rally from 2-4 down in eight-goal draw.",
     "SPORT"),
    ("Columbus Crew stun Inter Miami 3-0",
     "Crew rout defending MLS champions in playoff opener.",
     "SPORT"),
    ("Gordon Bell Prize to Chinese team",
     "Exascale FeMoco chemistry simulation wins top HPC prize.",
     "TECH"),
    ("BepiColombo captures first cosmic X-rays",
     "MIXS telescope images Crab Nebula before Mercury arrival.",
     "SCIENCE"),
    ("OpenAI chief proposes shared AI limits",
     "Perplexity thresholds suggested as a common safety speed limit.",
     "TECH"),
    ("South Korea readies stock stabilisation fund",
     "Top officials prepare fund after Wall Street\u2019s Friday fall.",
     "MARKETS"),
    ("Amazon near $7.5B Decart buy",
     "Amazon close to buying chip-portability startup Decart.",
     "TECH"),
    ("\u2018We Are Born Good\u2019 wins Golden Horse",
     "Hong Kong drama takes best film at Taipei ceremony.",
     "CULTURE"),
]

assert len(STORIES) + len(GRID_STORIES) == 35, (
    len(STORIES) + len(GRID_STORIES))
assert len(GRID_STORIES) == 32


def font(path, size):
    return ImageFont.truetype(path, size)


def crop_to_fill(img, w, h):
    tw, th = img.size
    scale = max(w / tw, h / th)
    nw, nh = int(tw * scale + 0.5), int(th * scale + 0.5)
    img = img.resize((nw, nh), Image.LANCZOS)
    x = (nw - w) // 2
    y = (nh - h) // 2
    return img.crop((x, y, x + w, y + h))


def wrap_text(draw, text, fnt, max_width):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_text(draw, text, path, start_size, max_width, max_lines,
             min_size=9, line_factor=1.2):
    size = start_size
    while size >= min_size:
        fnt = font(path, size)
        lines = wrap_text(draw, text, fnt, max_width)
        if len(lines) <= max_lines:
            return fnt, lines
        size -= 1
    fnt = font(path, min_size)
    return fnt, wrap_text(draw, text, fnt, max_width)


def draw_lines(draw, lines, fnt, x, y, fill, line_factor=1.2):
    lh = int(fnt.size * line_factor)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def draw_tracked(draw, text, fnt, cx, y, fill, tracking=3):
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total // 2
    for ch, wd in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += wd + tracking


def main():
    page = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(page)

    # ---------- Masthead (y 0-58) ----------
    title_fnt = font(SERIF_BOLD, 46)
    draw.text(((W - draw.textlength("THE WORLD", font=title_fnt)) // 2, 0),
              "THE WORLD", font=title_fnt, fill=INK)
    date_fnt = font(SANS, 15)
    draw_tracked(draw, "SUNDAY, 22 NOVEMBER 2026  \u2022  35 STORIES  \u2022  7 REGIONS",
                 date_fnt, W // 2, 42, INK, tracking=3)
    draw.rectangle([0, 58, W - 1, 60], fill=INK)  # 3px rule

    # ---------- Featured row (y 61-238): 3 photo tiles ----------
    feat_y0, feat_y1 = 61, 238
    feat_h = feat_y1 - feat_y0  # 177
    photo_h = 112
    margin, gutter = 12, 12
    fw = (W - 2 * margin - 2 * gutter) // 3  # 325
    feat_imgs = [
        "media-generation-cop31-collapse-0-311baf8f-4cdc-423f-b557-f44c23036abe.webp",
        "media-generation-shenzhen-summit-0-28e0dc64-3ba8-4244-b3c1-cbaedf4356c9.webp",
        "media-generation-hormuz-tanker-0-db0878e7-878b-4d6c-822b-964a2cb83ce8.webp",
    ]
    for i, (headline, subhead, _tag) in enumerate(STORIES):
        x = margin + i * (fw + gutter)
        w = fw if i < 2 else (W - margin - x)
        img = Image.open(os.path.join(ASSETS, feat_imgs[i])).convert("RGB")
        page.paste(crop_to_fill(img, w, photo_h), (x, feat_y0))
        tx = x + 10
        tw = w - 20
        ty = feat_y0 + photo_h + 6
        hfnt, hlines = fit_text(draw, headline, SERIF_BOLD, 19, tw, 1,
                                min_size=14)
        ty = draw_lines(draw, hlines, hfnt, tx, ty, INK)
        sfnt, slines = fit_text(draw, subhead, SANS, 12, tw, 2, min_size=10)
        draw_lines(draw, slines, sfnt, tx, ty + 3, GREY)
    # separators between featured tiles
    for i in (1, 2):
        sx = margin + i * fw + (i - 1) * gutter + gutter // 2
        draw.line([sx, feat_y0, sx, feat_y1], fill=SEP, width=1)
    draw.line([0, feat_y1 + 1, W - 1, feat_y1 + 1], fill=INK, width=1)

    # ---------- Grid (y 242-1020): 4 cols x 8 rows, 32 tiles ----------
    grid_y0 = 242
    gx_margin, gx_gutter, gy_gutter = 10, 8, 6
    cols, rows = 4, 8
    tw_tile = (W - 2 * gx_margin - (cols - 1) * gx_gutter) // cols  # 245
    th_tile = 92
    pad = 8
    for idx, (headline, summary, tag) in enumerate(GRID_STORIES):
        r, c = divmod(idx, cols)
        x = gx_margin + c * (tw_tile + gx_gutter)
        y = grid_y0 + r * (th_tile + gy_gutter)
        # tile border
        draw.rectangle([x, y, x + tw_tile - 1, y + th_tile - 1],
                       outline=SEP, width=1)
        tx = x + pad
        tw = tw_tile - 2 * pad
        ty = y + 6
        # tag chip
        chip_fnt = font(SANS_BOLD, 10)
        chip_w = int(draw.textlength(tag, font=chip_fnt)) + 12
        chip_h = 15
        draw.rectangle([tx, ty, tx + chip_w - 1, ty + chip_h - 1],
                       fill=TAG_COLORS[tag])
        draw.text((tx + 6, ty + 2), tag, font=chip_fnt, fill=WHITE)
        ty += chip_h + 4
        # headline (max 2 lines)
        hfnt, hlines = fit_text(draw, headline, SERIF_BOLD, 14, tw, 2,
                                min_size=11)
        ty = draw_lines(draw, hlines, hfnt, tx, ty, INK)
        # summary (max 2 lines)
        sfnt, slines = fit_text(draw, summary, SANS, 11, tw, 2, min_size=9)
        draw_lines(draw, slines, sfnt, tx, ty + 2, GREY)

    out = os.path.join(HERE, "entry.png")
    page.save(out, "PNG", optimize=True, compress_level=9)
    print(f"Wrote {out} ({os.path.getsize(out)} bytes)")


if __name__ == "__main__":
    main()
