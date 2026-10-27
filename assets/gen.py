"""Generate the Y2K SVG assets of the polymood profile README. Usage: python3 gen.py OUT_DIR"""
import os, random, sys
from xml.sax.saxutils import escape

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
SANS = "Verdana, Tahoma, Geneva, sans-serif"
MONO = "'Courier New', Courier, monospace"
W = 840


def save(name, w, h, body):
    with open(os.path.join(out, name), "w") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n{body}\n</svg>\n')


# --- header: starfield, synthwave grid, chrome title -------------------------------
random.seed(2000)
stars = []
for i in range(90):
    x, y, r = random.uniform(0, W), random.uniform(0, 150), random.choice([0.6, 0.8, 1.0, 1.4])
    tw = (f'<animate attributeName="opacity" values="1;0.15;1" dur="{random.uniform(1.5, 4):.1f}s" '
          f'begin="{random.uniform(0, 3):.1f}s" repeatCount="indefinite"/>') if i % 3 == 0 else ""
    stars.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#fff">{tw}</circle>')
grid = []
for k in range(1, 9):  # horizontal lines, closer near the horizon
    y = 150 + 62 * (k / 8) ** 2
    grid.append(f'<line x1="0" y1="{y:.1f}" x2="{W}" y2="{y:.1f}"/>')
for k in range(-14, 15):  # vertical lines to the vanishing point
    grid.append(f'<line x1="{W / 2}" y1="150" x2="{W / 2 + k * 70}" y2="212"/>')
sparkle = ('<path d="M0,-14 L3,-3 L14,0 L3,3 L0,14 L-3,3 L-14,0 L-3,-3 Z" fill="#fff">'
           '<animate attributeName="opacity" values="0;1;0" dur="2.2s" repeatCount="indefinite"/></path>')
save("header.svg", W, 212, f'''<defs>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#020024"/><stop offset="0.7" stop-color="#1d0650"/><stop offset="1" stop-color="#4b0a6e"/>
  </linearGradient>
  <linearGradient id="chrome" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#ffffff"/><stop offset="0.42" stop-color="#cfe0ff"/>
    <stop offset="0.5" stop-color="#3b4a86"/><stop offset="0.58" stop-color="#9fb4ec"/><stop offset="1" stop-color="#ffffff"/>
  </linearGradient>
  <filter id="glow" x="-10%" y="-30%" width="120%" height="160%"><feGaussianBlur stdDeviation="6"/></filter>
</defs>
<rect width="{W}" height="212" fill="url(#sky)"/>
<rect y="150" width="{W}" height="62" fill="#14002b"/>
{"".join(stars)}
<g stroke="#ff2bd6" stroke-width="1" opacity="0.65">{"".join(grid)}</g>
<line x1="0" y1="150" x2="{W}" y2="150" stroke="#ff9cf0" stroke-width="2"/>
<text x="420" y="104" text-anchor="middle" font-family="{SANS}" font-weight="bold" font-style="italic"
      font-size="80" letter-spacing="6" fill="#00e5ff" filter="url(#glow)" opacity="0.8">POLYMOOD</text>
<text x="420" y="104" text-anchor="middle" font-family="{SANS}" font-weight="bold" font-style="italic"
      font-size="80" letter-spacing="6" fill="url(#chrome)" stroke="#10104a" stroke-width="1.5">POLYMOOD</text>
<g transform="translate(676 40)">{sparkle}</g>
<g transform="translate(170 76) scale(0.6)"><g>{sparkle.replace('2.2s', '2.9s')}</g></g>
<text x="14" y="22" font-family="{MONO}" font-size="12" fill="#00e5ff">est. 2018</text>
<text x="{W - 14}" y="22" text-anchor="end" font-family="{MONO}" font-size="12" fill="#00e5ff">rust * c++ * c * python</text>
<text x="420" y="136" text-anchor="middle" font-family="{MONO}" font-size="15" font-weight="bold" fill="#7cff4f"
      stroke="#160535" stroke-width="4" paint-order="stroke">fast viewers for data that most software will not open</text>
<text x="420" y="186" text-anchor="middle" font-family="{MONO}" font-size="15" font-weight="bold" fill="#ffe94f"
      stroke="#14002b" stroke-width="4" paint-order="stroke">and careful tools for file formats that nobody documented</text>''')

# --- marquee -------------------------------------------------------------------------
msg = ("*** WELCOME TO MY HOMEPAGE *** EOVIEW AND RADVIEW BINARIES ARE IN THEIR RELEASES *** "
       "SMITHY IS PRE-ALPHA, HARD HAT AREA *** BEST VIEWED IN 800X600 *** SIGN MY GUESTBOOK *** ")
tw = int(len(msg) * 9.0)  # Courier 15px is about 9px per character
save("marquee.svg", W, 30, f'''<rect x="1" y="1" width="{W - 2}" height="28" fill="#000" stroke="#39ff14" stroke-width="2"/>
<clipPath id="c"><rect x="3" y="3" width="{W - 6}" height="24"/></clipPath>
<g clip-path="url(#c)" font-family="{MONO}" font-size="15" font-weight="bold" fill="#ffff00">
  <g><animateTransform attributeName="transform" type="translate" from="{W} 0" to="{-tw} 0" dur="24s" repeatCount="indefinite"/>
    <text x="0" y="20">{escape(msg)}</text><text x="{tw}" y="20">{escape(msg)}</text></g>
</g>''')

# --- Windows 98 title bars for the sections -----------------------------------------
def winbtn(x, glyph):
    return (f'<g transform="translate({x} 7)"><rect width="18" height="16" fill="#c0c0c0"/>'
            f'<path d="M0,16 V0 H18" fill="none" stroke="#fff"/><path d="M0,16 H18 V0" fill="none" stroke="#404040"/>'
            f'{glyph}</g>')


glyphs = [winbtn(W - 64, '<rect x="4" y="11" width="8" height="2" fill="#000"/>'),
          winbtn(W - 44, '<rect x="4" y="3" width="10" height="9" fill="none" stroke="#000" stroke-width="1.5"/>'
                         '<rect x="4" y="3" width="10" height="2" fill="#000"/>'),
          winbtn(W - 22, '<path d="M5,4 L13,12 M13,4 L5,12" stroke="#000" stroke-width="2"/>')]
for name, title in [("bar-remote", "C:\\POLYMOOD\\REMOTE_SENSING_AND_IMAGING"),
                    ("bar-games", "C:\\POLYMOOD\\GAME_TOOLING_AND_PRESERVATION"),
                    ("bar-docs", "C:\\POLYMOOD\\DOCUMENTS_AND_THE_TERMINAL")]:
    save(f"{name}.svg", W, 30, f'''<defs><linearGradient id="t" x1="0" x2="1"><stop offset="0" stop-color="#000080"/><stop offset="1" stop-color="#1084d0"/></linearGradient></defs>
<rect width="{W}" height="30" fill="#c0c0c0"/><rect x="2" y="2" width="{W - 4}" height="26" fill="url(#t)"/>
<rect x="9" y="8" width="14" height="12" fill="#ffd84f" stroke="#7a5c00"/><rect x="9" y="6" width="7" height="3" fill="#ffd84f" stroke="#7a5c00"/>
<text x="32" y="20" font-family="{SANS}" font-size="13" font-weight="bold" fill="#fff">{escape(title)}</text>
{"".join(glyphs)}''')

# --- 88x31 buttons ---------------------------------------------------------------------
buttons = [  # file, line 1, line 2, gradient top, gradient bottom, text color, mark, mark color
    ("btn-eoview", "EOVIEW", "EARTH OBS VIEWER", "#0a2a8a", "#14b8e6", "#fff", "EO", "#2ee6a6"),
    ("btn-radview", "RADVIEW", "SAR / ISAR VIEWER", "#001a00", "#0b5d0b", "#7cff4f", "((o", "#7cff4f"),
    ("btn-smithy", "SMITHY", "SOURCE MAPPING", "#5a1e00", "#e0701a", "#fff", "S2", "#ffd84f"),
    ("btn-tim2dump", "TIM2DUMP", "PS2 TEXTURES", "#1a0050", "#6b3fd6", "#fff", "PS2", "#9fd1ff"),
    ("btn-docindex", "DOCINDEX", "PDF FULL TEXT", "#f4f4f4", "#a8a8a8", "#101060", "PDF", "#d01010"),
    ("btn-nfod", "NFOD", "NFO VIEWER", "#000", "#1c1c1c", "#39ff14", ".nfo", "#39ff14"),
    ("btn-home", "POLYMOOD", ".NET HOMEPAGE", "#5a0050", "#ff2bd6", "#fff", "www", "#ffe94f"),
    ("btn-guestbook", "GUESTBOOK", "SIGN IT HERE", "#7a5c00", "#ffd84f", "#000", "GB", "#d01010"),
    ("btn-800x600", "BEST VIEWED", "AT 800X600", "#003a3a", "#00a3a3", "#fff", "CRT", "#e6ffff"),
    ("btn-rust", "RUST", "POWERED", "#2a1408", "#b7410e", "#fff", "rs", "#ffd8b0"),
]
for f, l1, l2, g1, g2, tc, mark, mc in buttons:
    save(f"{f}.svg", 88, 31, f'''<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{g1}"/><stop offset="1" stop-color="{g2}"/></linearGradient></defs>
<rect width="88" height="31" fill="#808080"/><path d="M0.5,30.5 V0.5 H87.5" fill="none" stroke="#fff"/>
<rect x="2" y="2" width="84" height="27" fill="url(#g)"/>
<rect x="3" y="3" width="25" height="25" fill="#000" opacity="0.35"/>
<text x="15.5" y="19" text-anchor="middle" font-family="{SANS}" font-size="{min(10, 22 / (0.75 * len(mark))):.1f}" font-weight="bold" fill="{mc}">{escape(mark)}</text>
<text x="31" y="14" font-family="{SANS}" font-size="{min(9.5, 53 / (0.78 * len(l1))):.1f}" font-weight="bold" fill="{tc}">{escape(l1)}</text>
<text x="31" y="24" font-family="{SANS}" font-size="{min(7, 53 / (0.72 * len(l2))):.1f}" fill="{tc}">{escape(l2)}</text>''')

# --- small pieces ------------------------------------------------------------------------
save("new.svg", 34, 15, '''<g><rect width="34" height="15" fill="#d01010"/>
<text x="17" y="11.5" text-anchor="middle" font-family="Verdana, sans-serif" font-size="10" font-weight="bold" fill="#ffff00">NEW!</text>
<animate attributeName="opacity" values="1;1;0" dur="1s" calcMode="discrete" repeatCount="indefinite"/></g>''')

save("rainbow.svg", W, 6, f'''<defs><linearGradient id="r" gradientUnits="userSpaceOnUse" x1="0" x2="420" spreadMethod="repeat">
<stop offset="0" stop-color="#ff0000"/><stop offset="0.17" stop-color="#ff9900"/><stop offset="0.33" stop-color="#ffff00"/>
<stop offset="0.5" stop-color="#00ff00"/><stop offset="0.67" stop-color="#00ccff"/><stop offset="0.83" stop-color="#6633ff"/><stop offset="1" stop-color="#ff0000"/>
<animateTransform attributeName="gradientTransform" type="translate" from="0 0" to="420 0" dur="3s" repeatCount="indefinite"/>
</linearGradient></defs><rect width="{W}" height="6" fill="url(#r)"/>''')

save("construction.svg", 360, 54, f'''<defs><pattern id="s" width="28" height="28" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
<rect width="14" height="28" fill="#ffd400"/><rect x="14" width="14" height="28" fill="#111"/>
<animateTransform attributeName="patternTransform" type="translate" additive="sum" from="0 0" to="28 0" dur="1.2s" repeatCount="indefinite"/>
</pattern></defs>
<rect width="360" height="54" fill="url(#s)"/><rect x="18" y="9" width="324" height="36" fill="#111" stroke="#ffd400" stroke-width="2"/>
<text x="180" y="26" text-anchor="middle" font-family="{SANS}" font-size="14" font-weight="bold" fill="#ffd400" letter-spacing="2">UNDER CONSTRUCTION</text>
<text x="180" y="39" text-anchor="middle" font-family="{MONO}" font-size="10" fill="#fff">this homepage is never finished</text>''')
print("ok", len(os.listdir(out)), "files")
