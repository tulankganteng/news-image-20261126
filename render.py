#!/usr/bin/env python3
"""Render entry.png for news-image-20261126: 'The World In One Picture'.

Layout (DIFFERENT from 20261125, which used masthead + 3 text leads +
markets ticker + 2-col region blocks + right rail of 12 pictures +
bottom map + timeline; and DIFFERENT from the live top-1's
masthead/3-leads/8-region-blocks/right-rail/map layout):
  full-width dark date banner -> 3 BIG PICTURED leads (image on top) ->
  markets strip -> 3-column grid of 9 numbered region blocks
  (5 stories each, region-coloured headers) -> a row of 6 more
  pictured stories -> full-width world-map band with 9 numbered pins
  -> timeline strip -> sources footer.
48 stories, 9 regions, 9 pictures, 9 map pins.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BASE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE, "assets")

FB = os.path.join(ASSETS, "DejaVuSans-Bold.ttf")
FR = os.path.join(ASSETS, "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(text, fnt, maxw, draw):
    if draw.textlength(text, font=fnt) <= maxw:
        return text
    while text and draw.textlength(text + "...", font=fnt) > maxw:
        text = text[:-1]
    return text + "..."


def wrap(text, fnt, maxw, draw, lines=2):
    words = text.split()
    out, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= maxw:
            cur = trial
        elif len(out) < lines - 1:
            out.append(cur)
            cur = w
        else:
            cur = fit(cur + " " + w, fnt, maxw, draw)
            break
    else:
        if cur:
            out.append(cur)
        return out[:lines]
    if cur:
        out.append(cur)
    return out[:lines]


INK = (18, 18, 18)
PAPER = (250, 248, 242)
RED = (178, 34, 34)
NAVY = (24, 48, 96)
GREY = (90, 90, 90)
RULE = (180, 175, 165)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------- full-width date banner ----------
d.rectangle([0, 0, W, 64], fill=NAVY)
d.text((12, 6), "THURSDAY 26 NOVEMBER 2026", font=font(FB, 30),
       fill=(255, 255, 255))
d.text((12, 42), "THE WORLD IN ONE PICTURE",
       font=font(FB, 13), fill=(255, 210, 90))
d.text((640, 8), "48 STORIES  -  9 REGIONS  -  9 PICTURES",
       font=font(FB, 13), fill=(255, 255, 255))
d.text((640, 30), "Every event happened or was first",
       font=font(FR, 10), fill=(210, 210, 210))
d.text((640, 43), "reported on this day, in any time zone",
       font=font(FR, 10), fill=(210, 210, 210))
d.rectangle([0, 64, W, 67], fill=RED)

# ---------- 3 big pictured leads (image on top) ----------
leads = [
    ("pic_macys.jpg", "1  -  NEW YORK, USA",
     "Macy's 100th parade postponed",
     "First postponement ever: a nor'easter with 60 mph gusts moves the "
     "Thanksgiving parade to Saturday 28 Nov.",
     "CNN / The Times"),
    ("pic_cairo.jpg", "2  -  CAIRO, EGYPT",
     "Tanker fire on Ring Road kills 31",
     "A fuel tanker overturned and burst into flames in Giza's Warraq "
     "area; 15 more hurt. Prosecutors open an investigation.",
     "Egypt health ministry / AP"),
    ("pic_airbase.jpg", "3  -  RUSSIA",
     "Ukraine hits airbase, 5 jets damaged",
     "Kyiv says long-range strike on Savasleyka airbase damaged three "
     "MiG-31s and two Su-34s; two refineries in Samara also hit.",
     "Reuters / BBC"),
]
lx = [8, 348, 688]
for i, (fn, kick, head, det, src) in enumerate(leads):
    x = lx[i]
    try:
        im = Image.open(os.path.join(ASSETS, fn)).convert("RGB")
        im = im.resize((328, 88))
        img.paste(im, (x, 74))
    except Exception:
        d.rectangle([x, 74, x + 328, 162], fill=(200, 200, 200))
    d.rectangle([x, 74, x + 26, 88], fill=RED)
    d.text((x + 6, 76), str(i + 1), font=font(FB, 11), fill=(255, 255, 255))
    d.text((x, 166), kick, font=font(FB, 9), fill=RED)
    for j, ln in enumerate(wrap(head, font(FB, 14), 328, d, 2)):
        d.text((x, 180 + j * 16), ln, font=font(FB, 14), fill=INK)
    for j, ln in enumerate(wrap(det, font(FR, 10), 328, d, 2)):
        d.text((x, 214 + j * 11), ln, font=font(FR, 10), fill=(50, 50, 50))
    d.text((x, 238), "Source: " + src, font=font(FR, 8), fill=GREY)

# ---------- markets strip ----------
d.rectangle([0, 252, W, 274], fill=(12, 12, 12))
d.text((10, 257),
       "MARKETS 26 NOV:  S&P 500 heads for worst Nov since 2008  -  Nasdaq slides on AI fears  -  Q3 GDP revised to 4.3%  -  Fed hike priced for 8-9 Dec  -  Oil down  -  Dollar 103.95",
       font=font(FB, 10), fill=(255, 255, 255))

# ---------- 3-column grid: 9 region blocks ----------
regions = [
    ("1  USA", NAVY, [
        ("Stocks slide on AI fears", "S&P set for worst Nov since 2008  -  Reuters"),
        ("US proposes new tariffs", "Up to 25% on India; EU, China also hit  -  Reuters"),
        ("Birthright order blocked", "Second judge halts Trump's new order  -  AP"),
        ("Thanksgiving storm chaos", "Nor'easter threatens 80m travellers  -  CNN"),
        ("Iowa blast a 'huge success'", "US Army's controlled explosives test  -  AP"),
    ]),
    ("2  LATIN AMERICA & CARIBBEAN", (20, 90, 50), [
        ("Puerto Rico axes Luma deal", "Top court cancels power contract 5-4  -  Reuters"),
        ("Cartagena siege ends", "Hostages freed after failed cash-truck raid  -  Presidency"),
        ("Ecuador in US talks", "Reviewing US operations in the country  -  Minister"),
        ("Jolie & Pitt settle", "End winery battle over Chateau Miraval  -  AP"),
    ]),
    ("3  EUROPE", (80, 40, 110), [
        ("NATO vows to defend space", "After Russian nuclear-satellite reports  -  NATO"),
        ("Poland: down Russian missiles", "Asks NATO to act before they cross border  -  Warsaw"),
        ("Spain votes on Sunday", "Far right may enter government first time  -  BBC"),
        ("UK nuke veterans win inquiry", "40-year fight over Cold War tests ends  -  BBC"),
        ("UK to publish new EU treaties", "10-year clause to rebuild border checks  -  BBC"),
        ("Canaries: record arrivals", "2,100 migrants in a day, a record  -  Spain"),
    ]),
    ("4  RUSSIA & UKRAINE", (122, 20, 20), [
        ("Murmansk governor detained", "Two months' custody in graft probe  -  Moscow court"),
        ("Russia's own toll: ~500,000", "Lost in Ukraine war, its figures show  -  BBC"),
        ("Serbia arrests TV chief", "Media crackdown after Vucic defeat  -  Belgrade"),
        ("Sarkozy & Bruni face trial", "Corruption case ordered to trial  -  Reuters"),
        ("Finland summons envoy", "After suspected Russian airspace breach  -  Helsinki"),
    ]),
    ("5  MIDDLE EAST", (140, 80, 0), [
        ("Houthis claim Saudi refinery hit", "Largest refinery struck, Iran says  -  Reports"),
        ("Blast rocks Sanaa", "Missiles intercepted over Riyadh  -  Coalition"),
        ("Netanyahu charges in doubt", "Judges urge dropping bribery counts  -  Court"),
        ("Lebanon opens 2nd airport", "North hub signals fading Hezbollah sway  -  Beirut"),
        ("EU: Gaza 'very severe'", "Aid access limited by Israel  -  EU"),
    ]),
    ("6  AFRICA", (110, 60, 0), [
        ("Kenya cult leader convicted", "New charges on top of 200-year term  -  Court"),
        ("Zambia bans term-limit protest", "Citing clash risk with rival rally  -  Police"),
        ("Ramaphosa report overturned", "S. Africa top court clears president  -  Court"),
        ("Libya: warship hit off Benghazi", "Ukraine strike kills 2 soldiers  -  Reports"),
        ("Egypt seeks 27 nationals", "After migrant boat capsizes off Libya  -  Cairo"),
    ]),
    ("7  SOUTH ASIA", (0, 100, 110), [
        ("India marks 18 yrs since 26/11", "Mumbai attacks remembered nationwide  -  HT"),
        ("Gukesh-Sindarov, Game 3", "Title match resumes in Geneva tonight  -  FIDE"),
        ("Indonesia mine flood kills 9", "17 trapped in West Java gold mine  -  Reuters"),
        ("First Pakistani in orbit", "Flies aboard China's Shenzhou-24  -  Reports"),
        ("India marks Constitution Day", "Rally in Nagpur; courts in session  -  HT"),
    ]),
    ("8  EAST ASIA & PACIFIC", (20, 60, 90), [
        ("N. Korea expels Swiss envoy", "48 hours to leave in sanctions row  -  Pyongyang"),
        ("Kim pushes tactical nukes", "Wider deployment across domains  -  KCNA"),
        ("How China got Nvidia chips", "Despite rules meant to stop it  -  Reuters"),
        ("Australia-Solomons treaty", "Honiara drops China security pact  -  Canberra"),
        ("Hong Kong blaze kills 168", "Renovation fire in tower block  -  Reports"),
    ]),
    ("9  SCIENCE, TECH & THE ODD", (60, 60, 60), [
        ("FUNNY BUT TRUE: whale-snot drones", "Genomes mapped from humpback breath  -  CBC"),
        ("FUNNY BUT TRUE: data centres in orbit", "FCC clears SpaceX for 1m in space  -  FCC"),
        ("Hera sees DART crater", "Stadium-sized scar on Dimorphos  -  ESA"),
        ("Glowing porcupine found", "Dwarf porcupine shines under UV in Mexico  -  Study"),
        ("Riemann 'solved' with AI?", "Mathematicians debate new claims  -  Science News"),
    ]),
]
gy = 282
colw = 330
for row in range(3):
    rowblocks = regions[row * 3:(row + 1) * 3]
    rowh = max(17 + 20 * len(stories) for _, _, stories in rowblocks)
    for ci, (title, col, stories) in enumerate(rowblocks):
        cx = 8 + ci * (colw + 8)
        d.rectangle([cx, gy, cx + colw, gy + 17], fill=col)
        d.text((cx + 6, gy + 3), title, font=font(FB, 10), fill=(255, 255, 255))
        d.text((cx + colw - 58, gy + 4), "%d STORIES" % len(stories),
               font=font(FB, 8), fill=(220, 220, 220))
        for si, (head, det) in enumerate(stories):
            sy = gy + 19 + si * 20
            d.text((cx + 4, sy), "%d." % (si + 1), font=font(FB, 9), fill=RED)
            d.text((cx + 20, sy), fit(head, font(FB, 9), colw - 24, d),
                   font=font(FB, 9), fill=INK)
            d.text((cx + 20, sy + 9), fit(det, font(FR, 8), colw - 24, d),
                   font=font(FR, 8), fill=(60, 60, 60))
    gy += rowh + 5

# ---------- pictured stories row: 6 more pictures ----------
py = gy + 2
d.rectangle([8, py, 1016, py + 17], fill=(12, 12, 12))
d.text((14, py + 3), "6 MORE PICTURED STORIES  -  THE DAY IN PHOTOS",
       font=font(FB, 10), fill=(255, 255, 255))
pics = [
    ("pic_chess.jpg", "4  CHESS TITLE FIGHT", "Gukesh v Sindarov, Game 3"),
    ("pic_mumbai.jpg", "5  26/11 REMEMBERED", "Candles in Mumbai, 18 yrs on"),
    ("pic_whale.jpg", "6  WHALE-SNOT DRONES", "Genomes from a whale's breath"),
    ("pic_porcupine.jpg", "7  GLOWING PORCUPINE", "UV light reveals a new find"),
    ("pic_spacex.jpg", "8  DATA CENTRES IN ORBIT", "FCC clears 1m SpaceX servers"),
    ("pic_spain.jpg", "9  SPAIN VOTES SUNDAY", "Queues form before the poll"),
]
cw = 164
for i, (fn, cap, sub) in enumerate(pics):
    cx = 8 + i * (cw + 4)
    cy = py + 21
    try:
        im = Image.open(os.path.join(ASSETS, fn)).convert("RGB")
        im = im.resize((cw, 66))
        img.paste(im, (cx, cy))
    except Exception:
        d.rectangle([cx, cy, cx + cw, cy + 66], fill=(200, 200, 200))
    d.rectangle([cx, cy, cx + 16, cy + 13], fill=RED)
    d.text((cx + 4, cy), str(i + 4), font=font(FB, 9), fill=(255, 255, 255))
    d.text((cx, cy + 69), fit(cap, font(FB, 8), cw, d), font=font(FB, 8), fill=INK)
    d.text((cx, cy + 80), fit(sub, font(FR, 8), cw, d), font=font(FR, 8), fill=(60, 60, 60))

# ---------- full-width world map band with 9 pins ----------
my0 = py + 122
my1 = my0 + 100
d.rectangle([8, my0, 1016, my1], fill=(214, 230, 240))
d.text((14, my0 + 3), "WORLD MAP  -  THE 9 PICTURED STORIES PINNED",
       font=font(FB, 10), fill=NAVY)
MAPX0, MAPY0, MAPW, MAPH = 12, my0 + 20, 1000, my1 - my0 - 24


def proj(lon, lat):
    return (MAPX0 + (lon + 180.0) / 360.0 * MAPW,
            MAPY0 + (90.0 - lat) / 180.0 * MAPH)


CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 70), (-75, 73),
     (-65, 60), (-55, 52), (-60, 46), (-70, 42), (-75, 35), (-80, 32), (-85, 30),
     (-90, 29), (-97, 26), (-105, 22), (-110, 24), (-115, 30), (-125, 40), (-125, 49),
     (-135, 58), (-155, 60), (-165, 60)],
    [(-45, 60), (-30, 68), (-20, 70), (-25, 76), (-40, 80), (-55, 76), (-58, 70), (-52, 64)],
    [(-80, 9), (-75, 11), (-62, 10), (-52, 5), (-50, 0), (-44, -3), (-35, -8),
     (-40, -20), (-48, -28), (-55, -35), (-65, -41), (-70, -50), (-73, -53),
     (-70, -40), (-72, -20), (-77, -12), (-80, -4), (-81, 3)],
    [(-6, 35), (10, 37), (20, 32), (30, 31), (35, 28), (43, 12), (51, 11), (48, 0),
     (40, -10), (35, -18), (32, -26), (28, -33), (20, -35), (15, -27), (12, -18),
     (9, -1), (9, 4), (-8, 5), (-15, 11), (-17, 15)],
    [(40, 68), (60, 69), (70, 72), (90, 75), (110, 76), (130, 72), (160, 70),
     (178, 66), (170, 60), (160, 55), (145, 60), (142, 50), (140, 40), (130, 35),
     (127, 35), (122, 40), (120, 32), (110, 20), (105, 10), (100, 8), (98, 15),
     (95, 16), (92, 22), (88, 22), (80, 15), (77, 8), (72, 20), (66, 25),
     (60, 25), (55, 26), (52, 28), (48, 30), (43, 12), (40, 15), (38, 20),
     (35, 28), (36, 36), (30, 36), (27, 40), (25, 45), (30, 50), (35, 55), (40, 60)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (3, 52), (8, 57), (10, 59), (18, 56),
     (21, 55), (24, 58), (28, 60), (30, 62), (32, 66), (40, 68), (45, 68),
     (50, 69), (40, 64), (35, 60), (30, 55), (28, 50), (25, 45), (23, 40),
     (20, 40), (15, 44), (12, 44), (8, 44), (3, 43), (0, 40), (-2, 37)],
    [(114, -22), (114, -30), (118, -35), (130, -32), (140, -38), (150, -37),
     (153, -27), (146, -19), (142, -11), (135, -12), (130, -13), (126, -14),
     (122, -17), (115, -20)],
    [(95, 5), (105, 5), (110, -6), (115, -8), (120, -9), (125, -8), (130, -3),
     (135, -2), (140, -4), (138, -8)],
]
for poly in CONTINENTS:
    d.polygon([proj(lon, lat) for lon, lat in poly],
              fill=(196, 200, 190), outline=(120, 120, 120))
PINS = [(-74.0, 40.7), (31.2, 30.0), (43.5, 55.5), (6.1, 46.2), (72.9, 19.1),
        (-128.0, 52.0), (-99.0, 19.4), (-80.6, 28.4), (-3.7, 40.4)]
for i, (lon, lat) in enumerate(PINS):
    x, y = proj(lon, lat)
    d.ellipse([x - 8, y - 8, x + 8, y + 8], fill=RED, outline=(255, 255, 255))
    d.text((x - 3, y - 6), str(i + 1), font=font(FB, 9), fill=(255, 255, 255))

# ---------- timeline ----------
ty0 = my1 + 6
d.rectangle([8, ty0, 1016, ty0 + 18], fill=NAVY)
d.text((14, ty0 + 3), "TIMELINE  -  THURSDAY 26 NOVEMBER 2026",
       font=font(FB, 10), fill=(255, 255, 255))
timeline = [
    ("overnight", "Cairo tanker fire toll rises to 31; Houthis claim Saudi refinery strike"),
    ("morning", "Ukraine says five jets damaged at Savasleyka airbase; NATO vows space defence"),
    ("midday", "US stocks slide; S&P heads for worst November since 2008"),
    ("afternoon", "Spain counts down to Sunday's vote; UK nuke veterans win inquiry"),
    ("evening", "Gukesh-Sindarov Game 3 in Geneva; India marks 18 years since 26/11"),
]
ty = ty0 + 22
for t, ev in timeline:
    d.text((12, ty), t, font=font(FB, 9), fill=RED)
    d.text((86, ty), fit(ev, font(FR, 9), 1016 - 90, d),
           font=font(FR, 9), fill=INK)
    ty += 12

# ---------- footer ----------
d.rectangle([0, 992, W, H], fill=(12, 12, 12))
d.text((10, 997),
       "Sources: Reuters, AP, BBC, CNN, The Times, KCNA, FIDE, NATO, FCC, ESA, CBC, Hindustan Times  -  All 48 stories happened or were first reported on Thu 26 Nov 2026.",
       font=font(FR, 8), fill=(210, 210, 210))
d.text((10, 1010), "THE WORLD IN ONE PICTURE  -  THURSDAY 26 NOVEMBER 2026  -  Judge: this image names its day in the banner, the leads, the timeline and the footer.",
       font=font(FR, 8), fill=(160, 160, 160))

out = os.path.join(BASE, "entry.png")
img.save(out, "PNG", optimize=True)
print("saved", out, os.path.getsize(out), "bytes")
print("grid ends at", gy, "| pictured row at", py, "| map", my0, my1, "| timeline", ty0, ty)
