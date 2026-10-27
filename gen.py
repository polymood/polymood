"""Generate the profile: Albert Bierstadt's "Among the Sierra Nevada, California" (1868, public domain)
as an animated dot-ASCII scene (the middle dot, bullet and black circle characters as three dot sizes),
and a README that shows it.

Usage: python3 gen.py   (needs Pillow and numpy)

How it works: a hidden brightness image (one pixel per character cell, ordered-dithered) decides the
dot size of each cell: empty, small, medium or large. The scene animates that brightness image
(cloud shadows, valley light, falling water, lake ripples, glints), so the dots grow, shrink and flow
live. A color image (one pixel per cell) paints the dots. All motion is SMIL: smooth, no frames.
"""
import base64, io, os
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "assets", "bierstadt.jpg")  # 3000x1800, from the SAAM 10500x6298 TIFF
OUT = os.path.join(ROOT, "assets", "sierra.svg")
CELL = 5  # SVG units per character cell, square (the README scales the image to the page width)
COLS, ROWS = 252, 151
W, H = COLS * CELL, ROWS * CELL  # 1260 x 755
S = W / 1200  # 1200-wide painting coordinates -> SVG units
BG = "#05070d"
DOTS = [1.0, 1.6, 2.3]  # radius of the small, medium and large dot (middle dot, bullet, black circle)
BAYER = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16
# regions in 1200x720 painting coordinates
WATER = [(0, 553), (860, 553), (845, 585), (700, 622), (600, 650), (300, 656), (0, 642)]
FALLS = [(240, 195, 252, 330, 1, 0.15), (268, 425, 298, 528, 1, 0.3), (544, 492, 560, 548, 1, 0.45),
         (676, 470, 692, 550, 1, 0.3), (546, 556, 558, 612, -1, 0.2)]  # x0, y0, x1, y1, direction, strength
GLINTS = [(786, 108), (760, 142), (1128, 150), (905, 190), (845, 128), (470, 560), (520, 566), (610, 562)]
SHADOWS = [(450, 160, 150, 70, 0), (360, 135, 330, 55, -25), (420, 120, 470, 85, -60)]  # rx, ry, y, seconds, begin


def png(img):
    buf = io.BytesIO()
    img.save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def cells(img):
    """(brightness image, color image), one pixel per cell."""
    small = img.resize((COLS, ROWS), Image.LANCZOS)
    hsv = np.asarray(small.convert("HSV")).astype(float) / 255
    v = hsv[..., 2]
    lo, hi = np.percentile(v, [2, 99.6])
    v = np.clip((v - lo) / (hi - lo), 0, 1)
    rank = v.ravel().argsort().argsort().reshape(v.shape) / (v.size - 1)
    v = 0.45 * v + 0.55 * rank  # partial histogram equalization: the dark painting uses all four dot sizes
    bayer = np.tile(BAYER, (ROWS // 4 + 1, COLS // 4 + 1))[:ROWS, :COLS]
    lum = np.clip(v ** 1.1 + (bayer - 0.5) * 0.24, 0, 1)  # ordered dither across the 4 dot levels
    hsv[..., 1] = np.clip(hsv[..., 1] * 1.7, 0, 1)
    hsv[..., 2] = 0.66 + 0.34 * v ** 0.7  # the dot size carries the brightness; keep small dots visible
    color = Image.fromarray((hsv * 255).astype(np.uint8), "HSV").convert("RGB")
    return Image.fromarray((lum * 255).astype(np.uint8), "L"), color


def poly(points):
    return " ".join(f"{x * S:.1f},{y * S:.1f}" for x, y in points)


def field():
    """The animated brightness field: dithered painting plus everything that moves."""
    out = ['<use href="#lum" xlink:href="#lum"/>']
    # lake: each row of cells slides a little, out of phase with the next one
    for r in range(int(553 * S / CELL), int(656 * S / CELL) + 1):
        out.append(f'<g clip-path="url(#lake)"><svg y="{r * CELL}" height="{CELL}" width="{W}" viewBox="0 {r * CELL} {W} {CELL}">'
                   f'<use href="#lum" xlink:href="#lum"><animateTransform attributeName="transform" type="translate" '
                   f'values="0 0;{CELL * 0.8} 0;0 0;{-CELL * 0.8} 0;0 0" dur="5s" begin="{-0.3 * r:.2f}s" '
                   f'repeatCount="indefinite"/></use></svg></g>')
    # falling water: bright bars scroll down the falls (up in the reflection)
    for x0, y0, x1, y1, d, k in FALLS:
        out.append(f'<rect x="{x0 * S:.1f}" y="{y0 * S:.1f}" width="{max(x1 - x0, 8) * S:.1f}" height="{(y1 - y0) * S:.1f}" '
                   f'fill="url(#fall{d})" opacity="{k}"/>')
    # valley light breathes, cloud shadows drift, snow and water glint
    out.append(f'<ellipse cx="{560 * S:.0f}" cy="{290 * S:.0f}" rx="{260 * S / 0.7:.0f}" ry="{185 * S / 0.7:.0f}" fill="url(#sun)" opacity="0.1">'
               f'<animate attributeName="opacity" values="0.05;0.32;0.05" dur="9s" repeatCount="indefinite" calcMode="spline" '
               f'keyTimes="0;0.5;1" keySplines="0.4 0 0.6 1;0.4 0 0.6 1"/></ellipse>')
    for rx, ry, y, dur, begin in SHADOWS:
        out.append(f'<ellipse cy="{y * S:.0f}" rx="{rx}" ry="{ry}" fill="url(#shade)"><animate attributeName="cx" '
                   f'from="{-rx}" to="{W + rx}" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/></ellipse>')
    for i, (x, y) in enumerate(GLINTS):
        out.append(f'<circle cx="{x * S:.1f}" cy="{y * S:.1f}" r="{CELL * 1.2}" fill="#fff" opacity="0"><animate attributeName="opacity" '
                   f'values="0;0;1;0" dur="{3.5 + 0.7 * i:.1f}s" begin="{-1.3 * i:.1f}s" repeatCount="indefinite"/></circle>')
    # on load, the scene grows in from the top
    out.append(f'<rect width="{W}" height="{H}" fill="#000"><animate attributeName="y" from="0" to="{H}" dur="2.6s" fill="freeze" '
               f'calcMode="spline" keyTimes="0;1" keySplines="0.45 0 0.2 1"/></rect>')
    return "\n".join(out)


def svg(lum, color):
    defs = [f'<image id="lum" href="{png(lum)}" width="{W}" height="{H}" preserveAspectRatio="none" '
            f'image-rendering="optimizeSpeed" style="image-rendering:pixelated"/>',
            f'<clipPath id="lake"><polygon points="{poly(WATER)}"/></clipPath>',
            '<radialGradient id="sun"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>',
            '<radialGradient id="shade"><stop offset="0" stop-color="#000" stop-opacity="0.55"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>',
            f'<g id="field">{field()}</g>']
    for d in (1, -1):
        defs.append(f'<pattern id="fall{d}" width="{W}" height="{5 * CELL}" patternUnits="userSpaceOnUse">'
                    f'<animateTransform attributeName="patternTransform" type="translate" from="0 0" to="0 {d * 5 * CELL}" '
                    f'dur="0.8s" repeatCount="indefinite"/><rect width="{W}" height="{CELL}" fill="#fff"/></pattern>')
    dots = []
    defs.append(f'<image id="color" href="{png(color)}" width="{W}" height="{H}" preserveAspectRatio="none" '
                f'image-rendering="optimizeSpeed" style="image-rendering:pixelated"/>')
    for k, r in enumerate(DOTS, start=1):
        table = " ".join("1" if j == k else "0" for j in range(4))  # brightness quarter k -> dot size k
        defs.append(f'<filter id="band{k}" x="0" y="0" width="1" height="1" color-interpolation-filters="sRGB"><feComponentTransfer>'
                    f'<feFuncR type="discrete" tableValues="{table}"/><feFuncG type="discrete" tableValues="{table}"/>'
                    f'<feFuncB type="discrete" tableValues="{table}"/></feComponentTransfer></filter>')
        defs.append(f'<mask id="m{k}" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">'
                    f'<use href="#field" xlink:href="#field" filter="url(#band{k})"/></mask>')
        defs.append(f'<pattern id="dot{k}" width="{CELL}" height="{CELL}" patternUnits="userSpaceOnUse">'
                    f'<circle cx="{CELL / 2}" cy="{CELL / 2}" r="{r}" fill="#fff"/></pattern>')
        defs.append(f'<mask id="d{k}" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">'
                    f'<rect width="{W}" height="{H}" fill="url(#dot{k})"/></mask>')
        # one mask level per element (Chromium drops masks nested inside mask content):
        # the group keeps band k of the field, the image inside keeps the dots of size k
        dots.append(f'<g mask="url(#m{k})"><use href="#color" xlink:href="#color" mask="url(#d{k})"/></g>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}">\n'
            '<defs>\n' + "\n".join(defs) + '\n</defs>\n'
            f'<rect width="{W}" height="{H}" fill="{BG}"/>\n' + "\n".join(dots) + '\n</svg>\n')


def main():
    lum, color = cells(Image.open(SRC).convert("RGB"))
    with open(OUT, "w") as f:
        f.write(svg(lum, color))
    with open(os.path.join(ROOT, "README.md"), "w") as f:
        f.write('<p align="center">\n  <img src="assets/sierra.svg" width="100%" alt="Animated dot art after '
                'Albert Bierstadt, Among the Sierra Nevada, California (1868): waterfalls flow, the lake shimmers, '
                'cloud shadows drift over the valley">\n</p>\n')
    print("ok", os.path.getsize(OUT) // 1024, "KB")


if __name__ == "__main__":
    main()
