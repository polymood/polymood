"""Generate the profile: one animated ASCII lava SVG and a README that shows it. Usage: python3 gen.py

How it works: soft white blobs drift on black (the "field"). For each brightness band of the field,
a mask keeps only that band, and a tiled pattern of one ASCII character fills it. Dim bands get
light characters (.), bright bands get dense ones (@). The browser moves the blobs continuously,
so the band edges glide through the characters at pixel precision, not cell by cell.
"""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
W, H = 840, 420
CW, CH, FONT = 7, 12, 12  # character cell and font size, px
MONO = "'DejaVu Sans Mono', Menlo, Consolas, 'Courier New', monospace"
BG = "#07020f"
# (character, color) from the dimmest band to the brightest; band 0 is the background texture
RAMP = [(".", "#1a0c33"), (":", "#3a1468"), ("-", "#5d1a94"), ("=", "#8a22a8"), ("+", "#c42c9c"),
        ("*", "#f23d78"), ("o", "#ff6a4d"), ("#", "#ffa040"), ("%", "#ffd45e"), ("@", "#fff6d0")]
# blobs: radius, orbit center x/y, orbit radius x/y, seconds per turn, clockwise
BLOBS = [(170, 210, 200, 120, 90, 19, 1), (160, 620, 210, 140, 110, 23, 0), (130, 420, 130, 220, 60, 17, 1),
         (120, 330, 300, 160, 70, 13, 0), (140, 520, 290, 120, 100, 29, 1), (100, 120, 110, 70, 60, 11, 0),
         (105, 740, 320, 60, 80, 15, 1)]


def field():
    """Blobs on black, the brightness source for every band mask."""
    out = [f'<rect width="{W}" height="{H}" fill="#000"/>']
    for r, cx, cy, rx, ry, dur, cw in BLOBS:
        d = f"M{rx},0 a{rx},{ry} 0 1,{cw} {-2 * rx},0 a{rx},{ry} 0 1,{cw} {2 * rx},0"
        out.append(f'<g transform="translate({cx} {cy})"><circle r="{r}" fill="url(#blob)">'
                   f'<animateMotion path="{d}" dur="{dur}s" repeatCount="indefinite"/></circle></g>')
    return "\n".join(out)


def svg():
    n = len(RAMP)
    defs = ['<radialGradient id="blob"><stop offset="0" stop-color="#fff"/>'
            '<stop offset="0.55" stop-color="#fff" stop-opacity="0.7"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>',
            f'<g id="field">{field()}</g>']
    layers = []
    for i, (ch, color) in enumerate(RAMP):
        # 2x2 cells, checker of this band and the band below it: ordered dither between bands
        lo_ch, lo_color = RAMP[max(i - 1, 0)]
        cells = [(0, 0, ch, color), (1, 1, ch, color), (1, 0, lo_ch, lo_color), (0, 1, lo_ch, lo_color)]
        defs.append(f'<pattern id="p{i}" width="{2 * CW}" height="{2 * CH}" patternUnits="userSpaceOnUse">' + "".join(
            f'<text x="{(cx + 0.5) * CW}" y="{(cy + 1) * CH - 3}" text-anchor="middle" font-family="{MONO}" '
            f'font-size="{FONT}" font-weight="bold" fill="{c}">{g}</text>' for cx, cy, g, c in cells) + '</pattern>')
        if i == 0:  # background texture everywhere, under the bands
            layers.append(f'<rect width="{W}" height="{H}" fill="url(#p0)"/>')
            continue
        table = " ".join("1" if k == i else "0" for k in range(n))  # keep only band i of the field
        defs.append(f'<filter id="f{i}" color-interpolation-filters="sRGB"><feComponentTransfer>'
                    f'<feFuncR type="discrete" tableValues="{table}"/><feFuncG type="discrete" tableValues="{table}"/>'
                    f'<feFuncB type="discrete" tableValues="{table}"/></feComponentTransfer></filter>')
        defs.append(f'<mask id="m{i}" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">'
                    f'<use href="#field" xlink:href="#field" filter="url(#f{i})"/></mask>')
        layers.append(f'<rect width="{W}" height="{H}" fill="url(#p{i})" mask="url(#m{i})"/>')
    defs.append('<pattern id="scan" width="4" height="3" patternUnits="userSpaceOnUse">'
                '<rect width="4" height="1" fill="#000" opacity="0.16"/></pattern>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{W}" height="{H}" viewBox="0 0 {W} {H}">\n<defs>\n' + "\n".join(defs) + "\n</defs>\n"
            f'<rect width="{W}" height="{H}" fill="{BG}"/>\n' + "\n".join(layers) +
            f'\n<rect width="{W}" height="{H}" fill="url(#scan)"/>\n</svg>\n')


def main():
    os.makedirs(os.path.join(ROOT, "assets"), exist_ok=True)
    with open(os.path.join(ROOT, "assets", "ascii.svg"), "w") as f:
        f.write(svg())
    with open(os.path.join(ROOT, "README.md"), "w") as f:
        f.write(f'<p align="center">\n  <img src="assets/ascii.svg" width="{W}" '
                f'alt="Animated ASCII art: glowing blobs drift and merge like a lava lamp, drawn with characters from . to @">\n</p>\n')
    print("ok")


if __name__ == "__main__":
    main()
