#!/usr/bin/env python3
"""Build the 1024x1024 newspaper front page for the news-image-20261122 bounty.

Composites four AI-generated photographs with PIL into a single front page
summing up 22 November 2026 world news. Run: python3 build_frontpage.py
Writes entry.png in this directory.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")

W, H = 1024, 1024
BG = (250, 247, 240)          # newsprint off-white
INK = (17, 17, 17)            # near-black text
GREY = (51, 51, 51)           # subhead grey
SEP = (221, 221, 221)         # panel separator
NAVY = (27, 42, 74)
RED = (122, 31, 31)
WHITE = (255, 255, 255)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

MARGIN = 12          # side margin for panel rows
GUTTER = 12          # gutter between panels


def font(path, size):
    return ImageFont.truetype(path, size)


def crop_to_fill(img, w, h):
    """Center-crop img to exactly w x h (cover)."""
    tw, th = img.size
    scale = max(w / tw, h / th)
    nw, nh = int(tw * scale + 0.5), int(th * scale + 0.5)
    img = img.resize((nw, nh), Image.LANCZOS)
    x = (nw - w) // 2
    y = (nh - h) // 2
    return img.crop((x, y, x + w, y + h))


def wrap_text(draw, text, fnt, max_width):
    """Greedy word wrap; returns list of lines."""
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
             min_size=9, line_factor=1.22):
    """Largest font size (<= start_size) whose wrap fits in max_lines."""
    size = start_size
    while size >= min_size:
        fnt = font(path, size)
        lines = wrap_text(draw, text, fnt, max_width)
        if len(lines) <= max_lines:
            return fnt, lines
        size -= 1
    fnt = font(path, min_size)
    return fnt, wrap_text(draw, text, fnt, max_width)


def text_block_height(lines, fnt, line_factor=1.22):
    return int(len(lines) * fnt.size * line_factor)


def draw_lines(draw, lines, fnt, x, y, fill, line_factor=1.22, align="left",
               max_width=None):
    """Draw lines starting at (x, y); returns bottom y."""
    lh = int(fnt.size * line_factor)
    for line in lines:
        lx = x
        if align == "center" and max_width is not None:
            lx = x + (max_width - draw.textlength(line, font=fnt)) // 2
        draw.text((lx, y), line, font=fnt, fill=fill)
        y += lh
    return y


def gradient_overlay(w, h, max_alpha=205):
    """Black vertical gradient: transparent at top, max_alpha at bottom."""
    grad = Image.new("L", (1, h))
    for y in range(h):
        t = y / max(h - 1, 1)
        grad.putpixel((0, y), int(max_alpha * t * t))
    grad = grad.resize((w, h))
    black = Image.new("RGBA", (w, h), (0, 0, 0, 255))
    transparent = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    return Image.composite(black, transparent, grad)


def draw_tracked(draw, text, fnt, cx, y, fill, tracking=3):
    """Draw centered text with letter tracking (for the date line)."""
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total // 2
    for ch, wd in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += wd + tracking


def photo_panel(page, draw, img_path, x, y, w, h, photo_h,
                headline, subhead, head_size, sub_size, head_max_lines=2,
                sub_max_lines=3, pad=12, gap_photo=8, gap_head=4):
    """Photo on top + headline + subhead inside a panel box (x, y, w, h)."""
    img = Image.open(img_path).convert("RGB")
    page.paste(crop_to_fill(img, w, photo_h), (x, y))
    tx = x + pad
    tw = w - 2 * pad
    ty = y + photo_h + gap_photo
    hfnt, hlines = fit_text(draw, headline, SERIF_BOLD, head_size, tw,
                            head_max_lines)
    ty = draw_lines(draw, hlines, hfnt, tx, ty, INK)
    sfnt, slines = fit_text(draw, subhead, SANS, sub_size, tw, sub_max_lines)
    draw_lines(draw, slines, sfnt, tx, ty + gap_head, GREY)
    return


def solid_panel(page, draw, x, y, w, h, color, headline, subhead,
                head_size, sub_size, head_max_lines=2, sub_max_lines=4,
                pad=16):
    """Solid-colour panel with white headline + subhead, vertically centred."""
    draw.rectangle([x, y, x + w - 1, y + h - 1], fill=color)
    tw = w - 2 * pad
    tx = x + pad
    hfnt, hlines = fit_text(draw, headline, SERIF_BOLD, head_size, tw,
                            head_max_lines)
    sfnt, slines = fit_text(draw, subhead, SANS, sub_size, tw, sub_max_lines)
    block_h = (text_block_height(hlines, hfnt) + 8
               + text_block_height(slines, sfnt))
    ty = y + (h - block_h) // 2
    ty = draw_lines(draw, hlines, hfnt, tx, ty, WHITE)
    draw_lines(draw, slines, sfnt, tx, ty + 8, (225, 225, 225))
    return


def main():
    page = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(page)

    # ---------- Masthead ----------
    title_fnt = font(SERIF_BOLD, 52)
    draw.text(((W - draw.textlength("THE WORLD", font=title_fnt)) // 2, 2),
              "THE WORLD", font=title_fnt, fill=INK)
    date_fnt = font(SANS, 15)
    draw_tracked(draw, "SUNDAY, 22 NOVEMBER 2026", date_fnt, W // 2, 52,
                 INK, tracking=4)
    draw.rectangle([0, 68, W - 1, 70], fill=INK)  # 3px rule

    # ---------- Hero: COP31 ----------
    hero_y0, hero_y1 = 71, 470
    hero_h = hero_y1 - hero_y0
    hero = Image.open(os.path.join(
        ASSETS, "media-generation-cop31-collapse-0-311baf8f-4cdc-423f-b557-f44c23036abe.webp"
    )).convert("RGB")
    hero = crop_to_fill(hero, W, hero_h)
    hero_rgba = hero.convert("RGBA")
    hero_rgba.alpha_composite(gradient_overlay(W, 165), (0, hero_h - 165))
    page.paste(hero_rgba.convert("RGB"), (0, hero_y0))

    # Hero text: headline + subhead, bottom-left, inside the gradient.
    hx = 24
    sub = "Climate talks end with no deal as EU rejects a text that omits fossil fuels"
    sub_fnt, sub_lines = fit_text(draw, sub, SANS, 21, W - 2 * hx, 2)
    sub_h = text_block_height(sub_lines, sub_fnt)
    head_fnt, head_lines = fit_text(draw, "COP31 COLLAPSES", SERIF_BOLD, 56,
                                    W - 2 * hx, 1)
    head_h = text_block_height(head_lines, head_fnt)
    bottom_pad = 20
    total = head_h + 8 + sub_h
    ty = hero_y1 - bottom_pad - total
    ty = draw_lines(draw, head_lines, head_fnt, hx, ty, WHITE)
    draw_lines(draw, sub_lines, sub_fnt, hx, ty + 8, (240, 240, 240))

    # ---------- Row 2: two photo panels ----------
    row2_y0, row2_y1 = 478, 700
    row2_h = row2_y1 - row2_y0
    pw2 = (W - 2 * MARGIN - GUTTER) // 2  # 494
    panels2 = [
        (MARGIN, os.path.join(
            ASSETS, "media-generation-shenzhen-summit-0-28e0dc64-3ba8-4244-b3c1-cbaedf4356c9.webp"),
         "TRUMP, XI AND PUTIN MEET",
         "First trilateral summit ends with a nuclear-risk declaration \u2014 but no Ukraine breakthrough"),
        (MARGIN + pw2 + GUTTER, os.path.join(
            ASSETS, "media-generation-hormuz-tanker-0-db0878e7-878b-4d6c-822b-964a2cb83ce8.webp"),
         "TANKERS HIT BY MINES",
         "Two supertankers struck near the Strait of Hormuz as the Iran\u2013US standoff deepens"),
    ]
    for x, img_path, headline, subhead in panels2:
        photo_panel(page, draw, img_path, x, row2_y0, pw2, row2_h, 135,
                    headline, subhead, 26, 16)
    # vertical separator between the two panels
    draw.line([W // 2, row2_y0, W // 2, row2_y1], fill=SEP, width=1)

    # ---------- Row 3: three panels ----------
    row3_y0, row3_y1 = 700, 960
    row3_h = row3_y1 - row3_y0
    pw3 = (W - 2 * MARGIN - 2 * GUTTER) // 3  # 325
    x1 = MARGIN
    x2 = MARGIN + pw3 + GUTTER
    x3 = MARGIN + 2 * (pw3 + GUTTER)
    # left: markets photo panel (width may be 326 for the last panel; use pw3+1)
    photo_panel(page, draw, os.path.join(
        ASSETS, "media-generation-markets-fall-0-93af17b7-a5ca-43bd-b2af-fb1dd92bd9ba.webp"),
        x1, row3_y0, pw3, row3_h, 140,
        "MARKETS IN CORRECTION",
        "S&P 500 \u22123.7%, Nasdaq \u22125.3% as the AI sell-off spreads to Asia",
        22, 15, head_max_lines=1)
    # middle: navy solid panel
    solid_panel(page, draw, x2, row3_y0, pw3, row3_h, NAVY,
                "WORLD COURT: GENOCIDE",
                "Myanmar ruled responsible for the 2017 Rohingya genocide \u2014 a first for the court",
                24, 15)
    # right: red solid panel
    solid_panel(page, draw, x3, row3_y0, W - MARGIN - x3, row3_h, RED,
                "\u2018EL CHAPO ISIDRO\u2019 CAPTURED",
                "Cartel boss seized in a Sinaloa raid; 11 killed, including four soldiers",
                24, 15)
    # vertical separators between the three panels
    draw.line([x2 - GUTTER // 2, row3_y0, x2 - GUTTER // 2, row3_y1],
              fill=SEP, width=1)
    draw.line([x3 - GUTTER // 2, row3_y0, x3 - GUTTER // 2, row3_y1],
              fill=SEP, width=1)
    # horizontal separator between row 2 and row 3
    draw.line([MARGIN, row3_y0, W - MARGIN, row3_y0], fill=SEP, width=1)

    # ---------- Footer ----------
    draw.rectangle([0, 960, W - 1, 961], fill=INK)  # 2px rule
    foot = ("Also: EU\u2013Indonesia sign landmark trade deal  \u2022  "
            "Russian strike hits Kryvyi Rih  \u2022  "
            "Democrats take largest House majority since 1992  \u2022  "
            "36 missing after Indonesia factory fire")
    ffnt, flines = fit_text(draw, foot, SANS, 15, W - 2 * MARGIN, 2)
    fh = text_block_height(flines, ffnt, line_factor=1.5)
    fy = 962 + (62 - fh) // 2
    draw_lines(draw, flines, ffnt, MARGIN, fy, INK, line_factor=1.5,
               align="center", max_width=W - 2 * MARGIN)

    out = os.path.join(HERE, "entry.png")
    page.save(out, "PNG", optimize=True, compress_level=9)
    print(f"Wrote {out} ({os.path.getsize(out)} bytes)")


if __name__ == "__main__":
    main()
