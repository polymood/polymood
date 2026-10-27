"""Generate the Y2K profile: every SVG in assets/ and README.md. Usage: python3 gen.py

The README holds only HTML: each block is an SVG image, each project window is a link.
Edit the texts and the PROJECTS list here, then run this script again.
"""
import os, random, textwrap
from xml.sax.saxutils import escape, quoteattr

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "assets")
SANS = "Verdana, Tahoma, Geneva, 'DejaVu Sans', sans-serif"
MONO = "'Courier New', Courier, monospace"
W = 840
GH = "https://github.com/polymood/"

TAGLINE = ("open source developer", "I just try to make useful stuff")
WELCOME = ["Hello and welcome to my homepage!",
           "I am polymood, an open source developer. I just try to make useful stuff.",
           "Every window below is a project. Click a window or a button to open it."]
UPDATED = "October 2026"

# name, button file, mark, mark color, gradient top, gradient bottom, button text color, button line 2,
# description, built with, facts, new
PROJECTS = {
    "Remote sensing and imaging": ("Pixels from orbit and from radar", [
        ("eoview", "EO", "#2ee6a6", "#0a2a8a", "#14b8e6", "#fff", "EARTH OBS VIEWER",
         "Desktop viewer for Earth observation data: GeoTIFF and COG, JPEG 2000, NITF, EOPF Zarr, "
         "Sentinel-1, -2 and -3 SAFE, NetCDF-4 and HDF5. A chunk engine streams local files, HTTP and S3 "
         "while the interface stays fluid. Time series with a timeline, and a first 3D globe.",
         ["Rust", "wgpu", "egui"], ["Windows, Linux, macOS", "installers, self-update"], True),
        ("radview", "((o", "#7cff4f", "#001a00", "#0b5d0b", "#7cff4f", "SAR / ISAR VIEWER",
         "GPU viewer for SAR and ISAR imagery: NITF (SICD, SIDD), TIFF, BigTIFF and COG. Shows complex "
         "data as amplitude, phase, I or Q, opens files larger than 10 GB, and has editable color maps "
         "with a dB stretch.",
         ["Rust", "wgpu", "egui"], ["Windows, Linux, macOS", "checksums, build provenance"], False),
    ]),
    "Game tooling and preservation": ("Old formats and old engines, treated with respect", [
        ("Smithy", "S2", "#ffd84f", "#5a1e00", "#e0701a", "#fff", "SOURCE MAPPING",
         "Open-source mapping tools for Source engine games, built one useful piece at a time on the way "
         "to a Hammer++ replacement. Today: a texture browser that mounts VPKs, game detection from "
         "gameinfo.txt, lossless VMF round-trip, brush geometry and Python plugins.",
         ["C++", "Qt 6", "Python plugins"], ["status: pre-alpha"], False),
        ("tim2dump", "PS2", "#9fd1ff", "#1a0050", "#6b3fd6", "#fff", "PS2 TEXTURES",
         "Extracts PlayStation 2 TIM2 textures to BMP or PNG. Every pixel format, CLUT palettes, mipmaps "
         "and batch mode, plus GS register inspection and an ANSI preview in the terminal.",
         ["C++", "CMake"], ["command line"], False),
    ]),
    "Documents and the terminal": ("Small tools that do one job well", [
        ("DocumentIndexer", "PDF", "#d01010", "#f4f4f4", "#a8a8a8", "#101060", "PDF FULL TEXT",
         "Turns a pile of PDFs into a searchable library. It reads the text layer or runs OCR (Tesseract, "
         "or the DeepSeek-OCR vision model on a GPU), detects the language of each document, then feeds a "
         "Tantivy full-text index behind a desktop search interface.",
         ["Python", "PySide6", "Tantivy"], ["command line + desktop GUI"], False),
        ("nfod", ".nfo", "#39ff14", "#000", "#1c1c1c", "#39ff14", "NFO VIEWER",
         "An NFO viewer for the terminal. One C file, one compiler command.",
         ["C"], ["terminal"], False),
    ]),
}
MORE = [("WerZatSongGUI", "WZS", "#ffffff", "#003a6a", "#2a7fd6", "#fff", "SONG ID GUI"),
        ("beautiful-python", "py", "#ffe94f", "#1f3a5f", "#3c78b4", "#fff", "CLEAN PYTHON")]
HOME = ("btn-home", "POLYMOOD", ".NET HOMEPAGE", "#5a0050", "#ff2bd6", "#fff", "www", "#ffe94f")


def save(name, w, h, body):
    with open(os.path.join(OUT, name), "w") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n{body}\n</svg>\n')


def wrap(text, width_px, size):
    return textwrap.wrap(text, int(width_px / (size * 0.62)))  # ponytail: Verdana average width, conservative


def lines(x, y, rows, step, **attrs):
    a = " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in attrs.items())
    return "".join(f'<text x="{x}" y="{y + i * step}" {a}>{escape(r)}</text>' for i, r in enumerate(rows))


SPARKLE = ('<path d="M0,-14 L3,-3 L14,0 L3,3 L0,14 L-3,3 L-14,0 L-3,-3 Z" fill="#fff">'
           '<animate attributeName="opacity" values="0;1;0" dur="{d}" repeatCount="indefinite"/></path>')
BLINK = '<animate attributeName="opacity" values="1;1;0" dur="1s" calcMode="discrete" repeatCount="indefinite"/>'


def header():
    random.seed(2000)
    stars = []
    for i in range(90):
        x, y, r = random.uniform(0, W), random.uniform(0, 150), random.choice([0.6, 0.8, 1.0, 1.4])
        tw = (f'<animate attributeName="opacity" values="1;0.15;1" dur="{random.uniform(1.5, 4):.1f}s" '
              f'begin="{random.uniform(0, 3):.1f}s" repeatCount="indefinite"/>') if i % 3 == 0 else ""
        stars.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#fff">{tw}</circle>')
    grid = [f'<line x1="0" y1="{150 + 62 * (k / 8) ** 2:.1f}" x2="{W}" y2="{150 + 62 * (k / 8) ** 2:.1f}"/>' for k in range(1, 9)]
    grid += [f'<line x1="{W / 2}" y1="150" x2="{W / 2 + k * 70}" y2="212"/>' for k in range(-14, 15)]
    title = (f'x="420" y="104" text-anchor="middle" font-family="{SANS}" font-weight="bold" font-style="italic" '
             f'font-size="80" letter-spacing="6"')
    save("header.svg", W, 212, f'''<defs>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#020024"/><stop offset="0.7" stop-color="#1d0650"/><stop offset="1" stop-color="#4b0a6e"/></linearGradient>
  <linearGradient id="chrome" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="0.42" stop-color="#cfe0ff"/>
    <stop offset="0.5" stop-color="#3b4a86"/><stop offset="0.58" stop-color="#9fb4ec"/><stop offset="1" stop-color="#ffffff"/></linearGradient>
  <filter id="glow" x="-10%" y="-30%" width="120%" height="160%"><feGaussianBlur stdDeviation="6"/></filter>
</defs>
<rect width="{W}" height="212" fill="url(#sky)"/><rect y="150" width="{W}" height="62" fill="#14002b"/>
{"".join(stars)}
<g stroke="#ff2bd6" stroke-width="1" opacity="0.65">{"".join(grid)}</g>
<line x1="0" y1="150" x2="{W}" y2="150" stroke="#ff9cf0" stroke-width="2"/>
<text {title} fill="#00e5ff" filter="url(#glow)" opacity="0.8">POLYMOOD</text>
<text {title} fill="url(#chrome)" stroke="#10104a" stroke-width="1.5">POLYMOOD</text>
<g transform="translate(676 40)">{SPARKLE.format(d="2.2s")}</g>
<g transform="translate(170 76) scale(0.6)">{SPARKLE.format(d="2.9s")}</g>
<text x="14" y="22" font-family="{MONO}" font-size="12" fill="#00e5ff">est. 2018</text>
<text x="{W - 14}" y="22" text-anchor="end" font-family="{MONO}" font-size="12" fill="#00e5ff">rust * c++ * c * python</text>
<text x="420" y="138" text-anchor="middle" font-family="{MONO}" font-size="17" font-weight="bold" fill="#7cff4f"
      stroke="#160535" stroke-width="4" paint-order="stroke">{escape(TAGLINE[0])}</text>
<text x="420" y="188" text-anchor="middle" font-family="{MONO}" font-size="17" font-weight="bold" fill="#ffe94f"
      stroke="#14002b" stroke-width="4" paint-order="stroke">{escape(TAGLINE[1])}</text>''')


def welcome():
    rows = [wrap(t, 760, 13) for t in WELCOME[1:]]
    body = [r for rs in rows for r in rs]
    h = 64 + 20 * len(body)
    save("welcome.svg", W, h, f'''<rect width="{W}" height="{h}" fill="#000033"/>
<rect x="6" y="6" width="{W - 12}" height="{h - 12}" fill="none" stroke="#00e5ff" stroke-width="2" stroke-dasharray="6 4"/>
<text x="420" y="38" text-anchor="middle" font-family="{SANS}" font-size="19" font-weight="bold" fill="#ffff00">{escape(WELCOME[0])}<tspan fill="#ff2bd6">{BLINK}_</tspan></text>
{lines(420, 64, body, 20, text_anchor="middle", font_family=SANS, font_size="13", fill="#ffffff")}''')


def button(f, l1, l2, g1, g2, tc, mark, mc):
    save(f"{f}.svg", 88, 31, f'''<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{g1}"/><stop offset="1" stop-color="{g2}"/></linearGradient></defs>
<rect width="88" height="31" fill="#808080"/><path d="M0.5,30.5 V0.5 H87.5" fill="none" stroke="#fff"/>
<rect x="2" y="2" width="84" height="27" fill="url(#g)"/><rect x="3" y="3" width="25" height="25" fill="#000" opacity="0.35"/>
<text x="15.5" y="19" text-anchor="middle" font-family="{SANS}" font-size="{min(10, 22 / (0.75 * len(mark))):.1f}" font-weight="bold" fill="{mc}">{escape(mark)}</text>
<text x="31" y="14" font-family="{SANS}" font-size="{min(9.5, 53 / (0.78 * len(l1))):.1f}" font-weight="bold" fill="{tc}">{escape(l1)}</text>
<text x="31" y="24" font-family="{SANS}" font-size="{min(7, 53 / (0.72 * len(l2))):.1f}" fill="{tc}">{escape(l2)}</text>''')


def section(name, tag, slug):
    save(f"sec-{slug}.svg", W, 46, f'''<defs><linearGradient id="chrome" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="0.45" stop-color="#cfe0ff"/>
  <stop offset="0.52" stop-color="#3b4a86"/><stop offset="0.6" stop-color="#9fb4ec"/><stop offset="1" stop-color="#ffffff"/></linearGradient></defs>
<rect width="{W}" height="46" fill="#020024"/><rect y="42" width="{W}" height="4" fill="#ff2bd6"/>
<g transform="translate(22 21) scale(0.7)">{SPARKLE.format(d="1.8s")}</g>
<text x="42" y="30" font-family="{SANS}" font-size="21" font-weight="bold" font-style="italic" fill="url(#chrome)" stroke="#10104a" stroke-width="0.8">{escape(name.upper())}</text>
<text x="{W - 14}" y="29" text-anchor="end" font-family="{MONO}" font-size="12" fill="#7cff4f">{escape(tag.lower())}</text>''')


def winbtn(x, y, glyph):
    return (f'<g transform="translate({x} {y})"><rect width="18" height="16" fill="#c0c0c0"/>'
            f'<path d="M0,16 V0 H18" fill="none" stroke="#fff"/><path d="M0,16 H18 V0" fill="none" stroke="#404040"/>{glyph}</g>')


def window(name, mark, mc, g1, g2, desc, built, facts, new):
    """Internet Explorer 5 style window: title bar, address bar, page, status bar."""
    text = wrap(desc, 590, 13)
    right = ["BUILT WITH"] + built + ["", "DETAILS"] + facts
    body_h = max(len(text), len(right)) * 19 + 26
    h = 3 + 24 + 30 + body_h + 6 + 22 + 3
    by = 57  # page top
    url = f"github.com/polymood/{name}"
    newtag = (f'<g transform="translate({W - 120} 7)"><rect width="38" height="15" fill="#d01010"/>'
              f'<text x="19" y="11.5" text-anchor="middle" font-family="{SANS}" font-size="10" font-weight="bold" fill="#ff0">NEW!</text>{BLINK}</g>') if new else ""
    rcol = "".join(
        f'<text x="640" y="{by + 26 + i * 19}" font-family="{SANS}" font-size="{11 if r.isupper() else 12}" '
        f'font-weight="{"bold" if r.isupper() else "normal"}" fill="{"#000080" if r.isupper() else "#222"}">{escape(r)}</text>'
        for i, r in enumerate(right) if r)
    save(f"win-{name.lower()}.svg", W, h, f'''<defs><linearGradient id="t" x1="0" x2="1"><stop offset="0" stop-color="#000080"/><stop offset="1" stop-color="#1084d0"/></linearGradient>
<linearGradient id="i" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{g1}"/><stop offset="1" stop-color="{g2}"/></linearGradient></defs>
<rect width="{W}" height="{h}" fill="#c0c0c0"/><path d="M0.5,{h - 0.5} V0.5 H{W - 0.5}" fill="none" stroke="#fff"/><path d="M0.5,{h - 0.5} H{W - 0.5} V0.5" fill="none" stroke="#404040"/>
<rect x="3" y="3" width="{W - 6}" height="24" fill="url(#t)"/>
<rect x="8" y="7" width="16" height="16" fill="url(#i)"/><text x="16" y="18.5" text-anchor="middle" font-family="{SANS}" font-size="{min(8, 15 / (0.7 * len(mark))):.1f}" font-weight="bold" fill="{mc}">{escape(mark)}</text>
<text x="31" y="20" font-family="{SANS}" font-size="13" font-weight="bold" fill="#fff">{escape(name)} - Microsoft Internet Explorer</text>
{newtag}
{winbtn(W - 66, 7, '<rect x="4" y="11" width="8" height="2" fill="#000"/>')}
{winbtn(W - 46, 7, '<rect x="4" y="3" width="10" height="9" fill="none" stroke="#000" stroke-width="1.5"/><rect x="4" y="3" width="10" height="2" fill="#000"/>')}
{winbtn(W - 24, 7, '<path d="M5,4 L13,12 M13,4 L5,12" stroke="#000" stroke-width="2"/>')}
<text x="10" y="47" font-family="{SANS}" font-size="12" fill="#000">Address</text>
<rect x="66" y="33" width="{W - 130}" height="20" fill="#fff"/><path d="M66.5,53 V33.5 H{W - 64.5}" fill="none" stroke="#808080"/>
<text x="72" y="47" font-family="{MONO}" font-size="13" fill="#000">https://{escape(url)}</text>
<g transform="translate({W - 58} 33)"><rect width="48" height="20" fill="#c0c0c0"/><path d="M0.5,20 V0.5 H48" fill="none" stroke="#fff"/><path d="M0,19.5 H47.5 V0" fill="none" stroke="#404040"/>
<text x="24" y="14.5" text-anchor="middle" font-family="{SANS}" font-size="12" fill="#000">Go</text></g>
<rect x="6" y="{by}" width="{W - 12}" height="{body_h}" fill="#fff"/><path d="M6.5,{by + body_h} V{by + 0.5} H{W - 6}" fill="none" stroke="#808080"/>
{lines(20, by + 26, text, 19, font_family=SANS, font_size="13", fill="#000")}
<line x1="624" y1="{by + 12}" x2="624" y2="{by + body_h - 12}" stroke="#c0c0c0"/>
{rcol}
<rect x="6" y="{h - 25}" width="{W - 12}" height="20" fill="#c0c0c0"/><path d="M6.5,{h - 5} V{h - 24.5} H{W - 6}" fill="none" stroke="#808080"/>
<text x="12" y="{h - 10.5}" font-family="{SANS}" font-size="11" fill="#000">Done. Click to open the repository.</text>
<text x="{W - 12}" y="{h - 10.5}" text-anchor="end" font-family="{SANS}" font-size="11" fill="#000">Internet</text>''')
    return h


def rainbow():
    save("rainbow.svg", W, 6, f'''<defs><linearGradient id="r" gradientUnits="userSpaceOnUse" x1="0" x2="420" spreadMethod="repeat">
<stop offset="0" stop-color="#ff0000"/><stop offset="0.17" stop-color="#ff9900"/><stop offset="0.33" stop-color="#ffff00"/>
<stop offset="0.5" stop-color="#00ff00"/><stop offset="0.67" stop-color="#00ccff"/><stop offset="0.83" stop-color="#6633ff"/><stop offset="1" stop-color="#ff0000"/>
<animateTransform attributeName="gradientTransform" type="translate" from="0 0" to="420 0" dur="3s" repeatCount="indefinite"/>
</linearGradient></defs><rect width="{W}" height="6" fill="url(#r)"/>''')


def footer():
    save("footer.svg", W, 44, f'''<text x="420" y="18" text-anchor="middle" font-family="{SANS}" font-size="11" fill="#808080">Releases, changelogs and build instructions live in each repository.</text>
<text x="420" y="36" text-anchor="middle" font-family="{SANS}" font-size="11" fill="#808080">Last updated: {escape(UPDATED)}.</text>''')


def img(src, alt, w, h):
    return f'<img src="assets/{src}" width="{w}" height="{h}" alt={quoteattr(alt)}>'


def link(href, inner):
    return f'<a href="{href}">{inner}</a>'


def center(*items):
    return '<p align="center">\n' + "\n".join(f"  {i}" for i in items) + "\n</p>\n"


def main():
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):  # assets are all generated: start clean
        if f.endswith(".svg"):
            os.remove(os.path.join(OUT, f))
    header(); welcome(); rainbow(); footer()
    button(*HOME)
    md = [center(img("header.svg", f"POLYMOOD: {TAGLINE[0]}. {TAGLINE[1]}.", W, 212)),
          center(img("welcome.svg", " ".join(WELCOME), W, 64 + 20 * sum(len(wrap(t, 760, 13)) for t in WELCOME[1:])))]
    nav, wins = [], []
    for sec, (tag, projs) in PROJECTS.items():
        slug = sec.split()[0].lower()
        section(sec, tag, slug)
        wins.append(center(img(f"sec-{slug}.svg", f"{sec}: {tag}.", W, 46)))
        for name, mark, mc, g1, g2, tc, l2, desc, built, facts, new in projs:
            button(f"btn-{name.lower()}", name.upper(), l2, g1, g2, tc, mark, mc)
            nav.append(link(GH + name, img(f"btn-{name.lower()}.svg", name, 88, 31)))
            h = window(name, mark, mc, g1, g2, desc, built, facts, new)
            alt = f"{name}: {desc} Built with {', '.join(built)}. {'. '.join(facts)}."
            wins.append(center(link(GH + name, img(f"win-{name.lower()}.svg", alt, W, h))))
    nav.append(link("https://polymood.net", img("btn-home.svg", "polymood.net", 88, 31)))
    more = []
    for name, mark, mc, g1, g2, tc, l2 in MORE:
        button(f"btn-{name.lower()}", name.upper(), l2, g1, g2, tc, mark, mc)
        more.append(link(GH + name, img(f"btn-{name.lower()}.svg", name, 88, 31)))
    md += [center(*nav), center(img("rainbow.svg", "", W, 6))] + wins
    md += [center(*more), center(img("rainbow.svg", "", W, 6)),
           center(img("footer.svg", f"Releases, changelogs and build instructions live in each repository. Last updated: {UPDATED}.", W, 44))]
    with open(os.path.join(ROOT, "README.md"), "w") as f:
        f.write("\n".join(md))
    print("ok", len(os.listdir(OUT)), "assets")


if __name__ == "__main__":
    main()
