#!/usr/bin/env python3
"""Draw the 19 November 2026 world-news summary as a single 1024x1024 PNG.

Everything here is drawn with Pillow primitives: a navy canvas, a header
block, a gold rule, and six story cards in a 2x3 grid. No network access,
no randomness, no timestamps in the output -- running this script twice
must produce byte-identical files.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- canvas ---
SIZE = 1024
NAVY = (11, 18, 38)          # page background
CARD_FILL = (22, 35, 63)     # card background
CARD_EDGE = (46, 74, 122)    # card outline
GOLD = (233, 181, 76)        # accent / subheader
WHITE = (245, 247, 250)
BODY = (199, 210, 226)       # body text
FOOT = (139, 152, 175)       # footer text
DARK = (15, 20, 35)          # number glyphs on coloured discs

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
BOLD = str(FONT_DIR / "DejaVuSans-Bold.ttf")
PLAIN = str(FONT_DIR / "DejaVuSans.ttf")

# ------------------------------------------------------------------ data ---
@dataclass(frozen=True)
class Story:
    number: int
    disc: tuple[int, int, int]
    headline: str
    body: str


STORIES = (
    Story(1, (255, 107, 97), "TRUMP, XI AND PUTIN MEET",
          "Trump, Xi and Putin hold an unprecedented three-way meeting in "
          "Shenzhen, pressing nuclear arms control."),
    Story(2, (255, 166, 77), "ICJ RULES ON ROHINGYA CASE",
          "The World Court delivers its judgment today on whether Myanmar "
          "committed genocide against the Rohingya in 2017."),
    Story(3, (96, 165, 250), "ANTHROPIC'S RECORD IPO",
          "Claude-maker Anthropic prices the biggest IPO ever at $83 a "
          "share, raising $81.3 billion; trading starts on Nasdaq today."),
    Story(4, (74, 222, 128), "ISRAEL PUSHES INTO GAZA",
          "Israeli tanks cross Gaza's Yellow Line in a rare ground "
          "operation to destroy a tunnel; Hamas calls it a ceasefire "
          "breach."),
    Story(5, (192, 132, 252), "CRIMEA BRIDGE HIT AGAIN",
          "Traffic halts on the Crimean Bridge after a third attack this "
          "week; a road section already lies in the sea."),
    Story(6, (250, 204, 21), "GTA VI LAUNCHES WORLDWIDE",
          "Grand Theft Auto VI launches worldwide after 13 years, with "
          "over $1.5 billion in pre-orders and a 99 on Metacritic."),
)

FOOTER = "Sources: NYT \u00b7 Reuters \u00b7 BBC \u00b7 Le Monde \u00b7 People \u00b7 CNN"

# ---------------------------------------------------------------- helpers ---
def load(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(BOLD if bold else PLAIN, size)


def wrap(draw: ImageDraw.ImageDraw, text: str,
         font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    """Greedy word wrap measured with the real font metrics."""
    lines: list[str] = []
    current = ""
    for word in text.split():
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_header(draw: ImageDraw.ImageDraw) -> None:
    draw.text((48, 36), "THURSDAY, 19 NOVEMBER 2026",
              font=load(50, bold=True), fill=WHITE)
    draw.text((48, 104), "THE WORLD IN ONE IMAGE",
              font=load(28, bold=True), fill=GOLD)
    draw.rectangle([0, 158, SIZE, 164], fill=GOLD)


def draw_card(draw: ImageDraw.ImageDraw, story: Story,
              x: int, y: int, w: int, h: int) -> None:
    draw.rounded_rectangle([x, y, x + w, y + h], radius=18,
                           fill=CARD_FILL, outline=CARD_EDGE, width=2)
    pad = 22
    disc_r = 27
    cx, cy = x + pad + disc_r, y + pad + disc_r
    draw.ellipse([cx - disc_r, cy - disc_r, cx + disc_r, cy + disc_r],
                 fill=story.disc)
    num_font = load(30, bold=True)
    num = str(story.number)
    nw = draw.textlength(num, font=num_font)
    draw.text((cx - nw / 2, cy - 21), num, font=num_font, fill=DARK)

    title_font = load(25, bold=True)
    title_x = x + pad + 2 * disc_r + 14
    title_top = y + pad + 8
    # Shrink the headline only if it would overflow the card width.
    while (draw.textlength(story.headline, font=title_font)
           > x + w - pad - title_x):
        title_font = load(title_font.size - 1, bold=True)
    draw.text((title_x, title_top), story.headline,
              font=title_font, fill=WHITE)

    body_font = load(23)
    text_w = w - 2 * pad
    lines = wrap(draw, story.body, body_font, text_w)
    # Body sits closer under the headline so the card bottom does not
    # carry a large empty band on the four-line stories.
    ly = title_top + 58
    for line in lines:
        draw.text((x + pad, ly), line, font=body_font, fill=BODY)
        ly += 33


def build() -> Image.Image:
    canvas = Image.new("RGB", (SIZE, SIZE), NAVY)
    draw = ImageDraw.Draw(canvas)
    draw_header(draw)

    margin, gap = 32, 24
    card_w = (SIZE - 2 * margin - gap) // 2
    card_h = 238
    top = 190
    for i, story in enumerate(STORIES):
        col, row = i % 2, i // 2
        x = margin + col * (card_w + gap)
        y = top + row * (card_h + gap)
        draw_card(draw, story, x, y, card_w, card_h)

    foot_font = load(21)
    draw.text((margin, SIZE - 42), FOOTER, font=foot_font, fill=FOOT)
    return canvas


def main() -> None:
    here = Path(__file__).resolve().parent
    out = here / "news.png"
    build().save(out, format="PNG")
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
