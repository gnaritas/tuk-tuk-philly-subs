#!/usr/bin/env python3
"""og.png 1200x630 — Tuk Tuk Philly Subs (2x supersample, measured clearances).
Charcoal griddle night, amber glow, Thai-gold cabin tuk-tuk art, condensed cream/amber wordmark.
Shop identity only — zero builder tokens."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630
S = 2
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public", "og.png")

CHAR = (30, 21, 14); CHAR2 = (46, 32, 20); CREAM = (248, 239, 220); GOLD = (201, 154, 46)
AMBER = (217, 72, 15); AMBER2 = (140, 44, 8); SAND = (232, 219, 190); INK = (24, 16, 10)

def font(paths, size):
    bases = ["/System/Library/Fonts/Supplemental/", "/System/Library/Fonts/"]
    for b in bases:
        for n in paths:
            p = b + n
            if os.path.exists(p):
                try: return ImageFont.truetype(p, size)
                except Exception: pass
    return ImageFont.load_default()

cond  = lambda s: font(["Avenir Next Condensed Bold.ttf", "AvenirNextCondensed-Bold.ttf", "Futura.ttc", "HelveticaNeue-Bold.ttf"], s*S)
sans  = lambda s: font(["Avenir Next Medium.ttf", "AvenirNext-Medium.ttf", "HelveticaNeue.ttc", "Arial.ttf"], s*S)

L = 80                      # left text margin
cx0 = 795                   # tuk-tuk art box left edge — all text must end left of this
img = Image.new("RGB", (W*S, H*S), CHAR)
d = ImageDraw.Draw(img, "RGBA")

# night gradient + amber grill glow
for y in range(H*S):
    t = y / (H*S)
    d.line([(0, y), (W*S, y)], fill=(int(CHAR[0]+(CHAR2[0]-CHAR[0])*t*.9),
                                      int(CHAR[1]+(CHAR2[1]-CHAR[1])*t*.9),
                                      int(CHAR[2]+(CHAR2[2]-CHAR[2])*t*.9)))
glow = Image.new("RGBA", (W*S, H*S), (0,0,0,0))
gd = ImageDraw.Draw(glow)
gd.ellipse([900*S-330, 380*S-230, 900*S+330, 380*S+230], fill=(217,72,15,60))
glow = glow.filter(__import__("PIL.ImageFilter", fromlist=["GaussianBlur"]).GaussianBlur(130*S//2))
img.paste(glow, (0,0), glow)

def P(x, y): return (x*S, y*S)

# ---- tuk-tuk art (right side) ----
# cabin — gold body
d.polygon([P(822,208), P(1032,208), P(1108,322), P(1112,372), P(816,372)], fill=GOLD)
d.polygon([P(822,208), P(1032,208), P(1108,322), P(1112,372), P(816,372)], outline=AMBER2)
d.line([P(816,372), P(822,208)], fill=AMBER2, width=5*S)
d.line([P(822,208), P(1032,208)], fill=AMBER2, width=5*S)
d.line([P(1032,208), P(1108,322)], fill=AMBER2, width=5*S)
d.line([P(1108,322), P(1112,372)], fill=AMBER2, width=5*S)
d.line([P(1112,372), P(816,372)], fill=AMBER2, width=5*S)
# roof band, extended left
d.rectangle([P(795,196), P(1038,214)], fill=(143,107,23))
# windshield + side window (charcoal)
d.rounded_rectangle([P(846,240), P(988,318)], radius=10*S, fill=INK)
# window divider
d.line([P(917,240), P(917,318)], fill=GOLD, width=4*S)
# headlight
d.ellipse([P(1092,330), P(1114,352)], fill=CREAM)
# wheels
def wheel(cx, cy, r):
    d.ellipse([P(cx-r, cy-r), P(cx+r, cy+r)], fill=CHAR)
    d.ellipse([P(cx-r, cy-r), P(cx+r, cy+r)], outline=CREAM, width=7*S)
    d.ellipse([P(cx-r*.32, cy-r*.32), P(cx+r*.32, cy+r*.32)], fill=GOLD)
wheel(878, 424, 46)
wheel(1062, 424, 46)
# struts
d.line([P(878,378), P(878,398)], fill=CREAM, width=6*S)
d.line([P(1062,378), P(1062,398)], fill=CREAM, width=6*S)
# motion streaks
for i, (y0, x0, x1) in enumerate([(300,700,790),(340,660,788),(380,700,782)]):
    d.line([P(x0,y0), P(x1,y0)], fill=(217,72,15,150-i*35), width=6*S)
# ground shadow
d.ellipse([P(812,462), P(1128,486)], fill=(10,6,4,150))

# ---- text column ----
y = 128
k = cond(21)
kicker = "DOWNTOWN RICHMOND, VA  ·  NOW OPEN"
d.text((L*S, y*S), kicker, font=k, fill=GOLD)
y += 50

t1 = cond(96)
d.text((L*S, y*S), "TUK TUK", font=t1, fill=CREAM)
y += 108
t2 = cond(64)
d.text((L*S, y*S), "PHILLY SUBS", font=t2, fill=AMBER)
y += 100

# gold rule
d.line([P(L, y), P(L+120, y)], fill=GOLD, width=4*S)
y += 26

s1 = sans(23)
d.text((L*S, y*S), "Philly Cheesesteaks $11\u201316  ·  Subs  ·  Gyros", font=s1, fill=SAND)
y += 34
d.text((L*S, y*S), "1110 E Main St  ·  Mon\u2013Sat lunch & dinner", font=s1, fill=SAND)

# ---- measured clearance proof ----
def tw(f, s): return f.getlength(s)/S
right = max(tw(k, kicker), tw(t1, "TUK TUK"), tw(t2, "PHILLY SUBS"),
            tw(s1, "Philly Cheesesteaks $11\u201316  ·  Subs  ·  Gyros"),
            tw(s1, "1110 E Main St  ·  Mon\u2013Sat lunch & dinner")) + L
print("text right edge:", round(right), "| art left edge:", cx0, "| clearance:", cx0 - round(right))
assert right < cx0 - 30, "text collides with tuk-tuk art"

# ---- gold Thai-chevron base band ----
bar_y = H - 22
d.line([P(0, bar_y), P(W, bar_y)], fill=GOLD, width=5*S)
for i in range(int(W/28)+1):
    x0 = 4 + i*28
    d.polygon([P(x0, bar_y), P(x0+14, H-4), P(x0+28, bar_y)], fill=(217,72,15))

img = img.resize((W, H), Image.LANCZOS)
img.save(OUT, "PNG", optimize=True)
sz = os.path.getsize(OUT)
print("saved", OUT, f"{W}x{H}", f"{sz/1024:.1f} KB")
assert sz < 500*1024
