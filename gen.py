"""Generate the profile: an animated ASCII version of Albert Bierstadt's "Among the Sierra Nevada,
California" (1868, public domain), and a README that shows it.

Usage: python3 gen.py   (needs Pillow and numpy)

The painting becomes a grid of colored characters: density from brightness, color from the paint.
A dim blurred copy of the painting sits behind the characters. Then the scene lives: water flows down
the falls, lake rows ripple like a reflection, cloud shadows drift, the sunlit valley breathes, the
snow glints, and a scan line draws the picture on load. All motion is SMIL, so it is smooth and the
SVG works as a plain image on GitHub.
"""
import base64, io, os
import numpy as np
from PIL import Image
from xml.sax.saxutils import escape

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "assets", "bierstadt.jpg")  # 3000x1800, from the SAAM 10500x6298 TIFF
OUT = os.path.join(ROOT, "assets", "sierra.svg")
W, H, COLS, ROWS = 840, 504, 140, 46
CW, CH, FONT = W / COLS, H / ROWS, 10
S = W / 1200  # source pixel -> output pixel
MONO = "'DejaVu Sans Mono', Menlo, Consolas, 'Courier New', monospace"
RAMP = " .,:;~=+*oxO#%@"
EDGE_SHARE = 0.16  # strongest edges (share of cells) drawn with | - / \ along the edge
COLORS = 64
# regions in source pixels
WATER = [(0, 553), (860, 553), (845, 585), (700, 622), (600, 650), (300, 656), (0, 642)]
FALLS = [(238, 195, 252, 330, 1, 0.3), (268, 425, 298, 528, 1, 0.8), (544, 492, 560, 548, 1, 0.9),
         (676, 470, 692, 550, 1, 0.7), (546, 556, 558, 612, -1, 0.35)]  # x0, y0, x1, y1, direction, opacity
GLINTS = [(786, 108), (760, 142), (1128, 150), (905, 190), (845, 128), (470, 560), (520, 566), (610, 562)]
SHADOWS = [(300, 110, 150, 70, 0), (240, 90, 330, 55, -25), (280, 80, 470, 85, -60)]  # rx, ry, y, seconds, begin


def inside(x, y, poly):
    hit = False
    for (x1, y1), (x2, y2) in zip(poly, poly[1:] + poly[:1]):
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            hit = not hit
    return hit


def fall_cells(x0, y0, x1, y1):
    """Fall rectangle snapped to the character grid: (col0, row0, col1, row1), end exclusive."""
    return int(x0 * S / CW), int(y0 * S / CH), int(np.ceil(x1 * S / CW)), int(np.ceil(y1 * S / CH))


def grid(img):
    small = img.resize((COLS, ROWS), Image.BOX)
    a = np.asarray(small).astype(float) / 255
    lum = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
    lo, hi = np.percentile(lum, [3, 99.5])  # stretch the contrast of the dark, muted paint
    level = np.clip((lum - lo) / (hi - lo), 0, 1) ** 1.15
    chars = np.vectorize(lambda v: RAMP[int(round(v * (len(RAMP) - 1)))])(level)
    # edges: Sobel on a 4x4 sampling of each cell, averaged per cell
    g = np.asarray(img.convert("L").resize((4 * COLS, 4 * ROWS), Image.LANCZOS)).astype(float) / 255
    gx = np.zeros_like(g); gy = np.zeros_like(g)
    gx[1:-1, 1:-1] = (g[:-2, 2:] + 2 * g[1:-1, 2:] + g[2:, 2:]) - (g[:-2, :-2] + 2 * g[1:-1, :-2] + g[2:, :-2])
    gy[1:-1, 1:-1] = (g[2:, :-2] + 2 * g[2:, 1:-1] + g[2:, 2:]) - (g[:-2, :-2] + 2 * g[:-2, 1:-1] + g[:-2, 2:])
    gx = gx.reshape(ROWS, 4, COLS, 4).mean((1, 3)); gy = gy.reshape(ROWS, 4, COLS, 4).mean((1, 3))
    mag = np.hypot(gx, gy)
    strong = (mag > np.quantile(mag, 1 - EDGE_SHARE)) & (level > 0.12)
    angle = (np.degrees(np.arctan2(gy, gx)) + 180) % 180  # gradient direction; the edge runs across it
    edge = np.choose(((angle + 22.5) // 45).astype(int) % 4, ["|", "/", "-", "\\"])
    chars = np.where(strong, edge, chars)
    hsv = np.asarray(small.convert("HSV")).astype(float) / 255
    hsv[..., 1] = np.clip(hsv[..., 1] * 1.5, 0, 1)  # push the color
    hsv[..., 2] = 0.45 + 0.55 * np.clip((hsv[..., 2] - lo) / (hi - lo), 0, 1) ** 0.8  # glow over the backdrop
    lit = Image.fromarray((hsv * 255).astype(np.uint8), "HSV").convert("RGB")
    q = lit.quantize(colors=COLORS, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette()[:3 * COLORS]
    return chars, np.asarray(q), ["#%02x%02x%02x" % tuple(pal[3 * i:3 * i + 3]) for i in range(COLORS)]


def backdrop(img):
    """The painting at 2x3 pixels per character cell, dithered to a small palette, dimmed under the text."""
    b = img.resize((2 * COLS, 3 * ROWS), Image.LANCZOS)
    hsv = np.asarray(b.convert("HSV")).astype(float) / 255
    hsv[..., 1] = np.clip(hsv[..., 1] * 1.4, 0, 1)
    lum = hsv[..., 2]
    lo, hi = np.percentile(lum, [2, 99.5])
    hsv[..., 2] = np.clip((lum - lo) / (hi - lo), 0, 1) ** 0.9 * 0.62
    b = Image.fromarray((hsv * 255).astype(np.uint8), "HSV").convert("RGB")
    b = b.quantize(colors=32, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG).convert("RGB")
    buf = io.BytesIO()
    b.save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def text_rows(chars, cls):
    falls = [fall_cells(*f[:4]) for f in FALLS]
    out = []
    for r in range(ROWS):
        groups = {False: {}, True: {}}  # water? -> class -> [(x, char)]
        for c in range(COLS):
            ch = chars[r, c]
            if ch == " " or any(c0 <= c < c1 and r0 <= r < r1 for c0, r0, c1, r1 in falls):
                continue
            water = inside((c + 0.5) * CW / S, (r + 0.5) * CH / S, WATER)
            groups[water].setdefault(cls[r, c], []).append((c * CW, ch))
        y = (r + 1) * CH - 2.3
        for water, by_cls in groups.items():
            if not by_cls:
                continue
            spans = "".join(f'<tspan class="c{k}" x="{" ".join(f"{x:.1f}" for x, _ in v)}">{escape("".join(ch for _, ch in v))}</tspan>'
                            for k, v in sorted(by_cls.items()))
            anim = (f'<animateTransform attributeName="transform" type="translate" values="0 0;1.6 0;0 0;-1.6 0;0 0" '
                    f'dur="5s" begin="{-0.37 * r:.2f}s" repeatCount="indefinite"/>') if water else ""
            out.append(f'<text y="{y:.1f}">{anim}{spans}</text>')
    return "\n".join(out)


def falls_svg():
    defs, rects = [], []
    for d in (1, -1):
        glyphs = "".join(f'<text x="{CW / 2:.1f}" y="{(i + 1) * CH - 2.3:.1f}" text-anchor="middle" fill="{c}">{g}</text>'
                         for i, (g, c) in enumerate([("|", "#f4f8ff"), (":", "#bcd2ec"), ("|", "#ffffff"), ("'", "#9fb8d8")]))
        defs.append(f'<pattern id="fall{d}" width="{CW:.2f}" height="{4 * CH:.2f}" patternUnits="userSpaceOnUse">'
                    f'<animateTransform attributeName="patternTransform" type="translate" from="0 0" to="0 {d * 4 * CH:.2f}" '
                    f'dur="0.9s" repeatCount="indefinite"/>{glyphs}</pattern>')
    for f in FALLS:
        c0, r0, c1, r1 = fall_cells(*f[:4])
        rects.append(f'<rect x="{c0 * CW:.1f}" y="{r0 * CH:.1f}" width="{(c1 - c0) * CW:.1f}" height="{(r1 - r0) * CH:.1f}" '
                     f'fill="url(#fall{f[4]})" opacity="{f[5]}"/>')
    return defs, rects


def light_svg():
    defs = ['<radialGradient id="sun"><stop offset="0" stop-color="#fff1c2" stop-opacity="0.9"/><stop offset="1" stop-color="#fff1c2" stop-opacity="0"/></radialGradient>',
            '<radialGradient id="shade"><stop offset="0" stop-color="#000" stop-opacity="0.5"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>',
            '<radialGradient id="vignette" r="0.75"><stop offset="0.6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="0.6"/></radialGradient>']
    out = [f'<ellipse cx="{560 * S:.0f}" cy="{290 * S:.0f}" rx="270" ry="190" fill="url(#sun)" opacity="0.08">'
           f'<animate attributeName="opacity" values="0.05;0.17;0.05" dur="9s" repeatCount="indefinite" calcMode="spline" '
           f'keyTimes="0;0.5;1" keySplines="0.4 0 0.6 1;0.4 0 0.6 1"/></ellipse>']
    for rx, ry, y, dur, begin in SHADOWS:
        out.append(f'<ellipse cy="{y * S:.0f}" rx="{rx}" ry="{ry}" fill="url(#shade)"><animate attributeName="cx" '
                   f'from="{-rx}" to="{W + rx}" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/></ellipse>')
    for i, (x, y) in enumerate(GLINTS):
        out.append(f'<path transform="translate({x * S:.1f} {y * S:.1f})" d="M0,-5 L1,-1 L5,0 L1,1 L0,5 L-1,1 L-5,0 L-1,-1 Z" '
                   f'fill="#fff" opacity="0"><animate attributeName="opacity" values="0;0;1;0" dur="{3.5 + 0.7 * i:.1f}s" '
                   f'begin="{-1.3 * i:.1f}s" repeatCount="indefinite"/></path>')
    out.append(f'<rect width="{W}" height="{H}" fill="url(#vignette)"/>')
    return defs, out


def reveal():
    spline = 'calcMode="spline" keyTimes="0;1" keySplines="0.45 0 0.2 1"'
    return (f'<rect width="{W}" height="{H}" fill="#000"><animate attributeName="y" from="0" to="{H}" dur="2.6s" fill="freeze" {spline}/></rect>'
            f'<rect width="{W}" height="2" fill="#d8ecff"><animate attributeName="y" from="0" to="{H}" dur="2.6s" fill="freeze" {spline}/>'
            f'<animate attributeName="opacity" values="1;1;0" keyTimes="0;0.9;1" dur="2.8s" fill="freeze"/></rect>')


def main():
    img = Image.open(SRC).convert("RGB")
    chars, cls, palette = grid(img)
    fdefs, frects = falls_svg()
    ldefs, light = light_svg()
    style = (f"text{{font-family:{MONO};font-size:{FONT}px;font-weight:bold}}" +
             "".join(f".c{i}{{fill:{c}}}" for i, c in enumerate(palette)))
    bd = backdrop(img)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}">\n'
           f'<style>{style}</style>\n<defs>\n' + "\n".join(fdefs + ldefs) + '\n</defs>\n'
           f'<rect width="{W}" height="{H}" fill="#000"/>\n'
           f'<image href="{bd}" xlink:href="{bd}" width="{W}" height="{H}" preserveAspectRatio="none" '
           f'image-rendering="optimizeSpeed" style="image-rendering:pixelated"/>\n'
           + text_rows(chars, cls) + "\n" + "\n".join(frects + light) + "\n" + reveal() + "\n</svg>\n")
    with open(OUT, "w") as f:
        f.write(svg)
    with open(os.path.join(ROOT, "README.md"), "w") as f:
        f.write(f'<p align="center">\n  <img src="assets/sierra.svg" width="{W}" alt="Animated ASCII version of '
                f'Albert Bierstadt, Among the Sierra Nevada, California (1868): waterfalls flow, the lake ripples, '
                f'cloud shadows drift over the valley">\n</p>\n<p align="center"><sub>after Albert Bierstadt, '
                f'<i>Among the Sierra Nevada, California</i>, 1868, Smithsonian American Art Museum</sub></p>\n')
    print("ok", os.path.getsize(OUT) // 1024, "KB")


if __name__ == "__main__":
    main()
