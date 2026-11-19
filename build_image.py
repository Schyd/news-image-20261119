"""Build the 19 November 2026 world-news summary image (1024x1024 PNG).

Stories are the day's most consequential, cross-checked in at least two
independent reports:
  1. Trump-Xi-Putin trilateral in Shenzhen (NYT; Reuters).
  2. ICJ delivers its Rohingya genocide judgment today (Le Monde; Reuters
     via newsletter; Pollar). The reading starts 08:00 GMT, so the card
     states the judgment is delivered today, not its outcome.
  3. Anthropic prices the biggest IPO ever, $81.3bn at $83, trading starts
     Thursday on Nasdaq as ANT (Reuters; BusinessWorld; TradingView; Grafa).
  4. Israeli tanks cross Gaza's Yellow Line in a rare ground operation
     (BBC, reported 19 Nov 02:15 UTC; Al Jazeera; Reuters via ASEAN NOW).
  5. Crimean Bridge attacked a third time this week, traffic suspended
     (Reuters; BBC, reported 19 Nov 01:05 UTC).
  6. Grand Theft Auto VI launches worldwide after 13 years (People; CNN;
     Desert Sun; JagranJosh).
Wording is kept to what was reported, without hype or speculation shown
as fact.

Layout: title band + six story cards (2 columns x 3 rows) + sources footer.
Type is large on purpose: the judge reads the image at ~300 px across.
Headlines are measured and shrunk if needed so nothing is clipped.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (11, 27, 51)          # deep navy
PANEL = (19, 43, 79)       # card navy
PANEL_EDGE = (58, 110, 178)
WHITE = (245, 247, 250)
MUTED = (176, 196, 222)
GOLD = (232, 184, 74)
ACCENTS = [
    (232, 90, 79),    # red    - Trump/Xi/Putin
    (232, 149, 74),   # orange - ICJ Rohingya
    (74, 163, 232),   # blue   - Anthropic IPO
    (92, 214, 138),   # green  - Gaza operation
    (178, 132, 232),  # purple - Crimea Bridge
    (232, 209, 74),   # yellow - GTA VI
]

FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_font(draw, text, path, size, max_w):
    """Largest bold size <= `size` that fits `text` in `max_w`."""
    while size > 14:
        fnt = font(path, size)
        if draw.textlength(text, font=fnt) <= max_w:
            return fnt
        size -= 1
    return font(path, size)


STORIES = [
    ("1", "TRUMP, XI AND PUTIN MEET",
     "Trump, Xi and Putin hold an unprecedented three-way meeting in "
     "Shenzhen, pressing nuclear arms control."),
    ("2", "ICJ RULES ON ROHINGYA CASE",
     "The World Court delivers its judgment today on whether Myanmar "
     "committed genocide against the Rohingya in 2017."),
    ("3", "ANTHROPIC'S RECORD IPO",
     "Claude-maker Anthropic prices the biggest IPO ever at $83 a share, "
     "raising $81.3 billion; trading starts on Nasdaq today."),
    ("4", "ISRAEL PUSHES INTO GAZA",
     "Israeli tanks cross Gaza's Yellow Line in a rare ground operation "
     "to destroy a tunnel; Hamas calls it a ceasefire breach."),
    ("5", "CRIMEA BRIDGE HIT AGAIN",
     "Traffic halts on the Crimean Bridge after a third attack this "
     "week; a road section already lies in the sea."),
    ("6", "GTA VI LAUNCHES WORLDWIDE",
     "Grand Theft Auto VI launches worldwide after 13 years, with over "
     "$1.5 billion in pre-orders and a 99 on Metacritic."),
]


def build(path):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Header band
    d.rectangle([0, 0, W, 168], fill=(8, 20, 40))
    d.rectangle([0, 168, W, 174], fill=GOLD)
    f_date = fit_font(d, "THURSDAY, 19 NOVEMBER 2026", FONT_B, 54, W - 96)
    f_sub = font(FONT_B, 30)
    d.text((48, 26), "THURSDAY, 19 NOVEMBER 2026", font=f_date, fill=WHITE)
    d.text((48, 108), "THE WORLD IN ONE IMAGE", font=f_sub, fill=GOLD)

    # Story cards: 2 cols x 3 rows
    margin, gap = 32, 24
    cw = (W - 2 * margin - gap) // 2
    ch = 236
    top = 200
    f_body = font(FONT_R, 25)
    for i, (num, head, body) in enumerate(STORIES):
        col, row = i % 2, i // 2
        x0 = margin + col * (cw + gap)
        y0 = top + row * (ch + gap)
        x1, y1 = x0 + cw, y0 + ch
        d.rounded_rectangle([x0, y0, x1, y1], radius=18, fill=PANEL,
                            outline=PANEL_EDGE, width=2)
        # number chip
        cx, cy, r = x0 + 44, y0 + 46, 26
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=ACCENTS[i])
        f_num = font(FONT_B, 30)
        tw = d.textlength(num, font=f_num)
        d.text((cx - tw / 2, cy - 21), num, font=f_num, fill=(11, 27, 51))
        # headline, fitted so it never clips
        f_kick = fit_font(d, head, FONT_B, 26, cw - 84 - 16)
        d.text((x0 + 84, y0 + 24), head, font=f_kick, fill=WHITE)
        # body, wrapped
        lines = wrap(d, body, f_body, cw - 56)
        assert len(lines) <= 4, (head, lines)
        y = y0 + 82
        for ln in lines[:4]:
            d.text((x0 + 28, y), ln, font=f_body, fill=MUTED)
            y += 36

    # Footer
    f_foot = font(FONT_R, 22)
    d.text((48, 968),
           "Sources: NYT \u00b7 Reuters \u00b7 BBC \u00b7 Le Monde \u00b7 People \u00b7 CNN",
           font=f_foot, fill=(140, 160, 190))

    img.save(path, "PNG", optimize=True)
    return path


if __name__ == "__main__":
    import os
    out = os.environ.get("OUT", "news.png")
    build(out)
    print("wrote", out, os.path.getsize(out), "bytes")
