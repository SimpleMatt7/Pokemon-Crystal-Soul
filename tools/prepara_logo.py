"""Prepara un logo disegnato a parte (PNG/WebP qualsiasi, sfondo bianco o trasparente) per il titolo.

Toglie lo sfondo bianco partendo dai bordi (i bianchi interni restano), ritaglia, ridimensiona per stare nella
zona del logo del titolo (BOX) e salva un PNG 256x256 trasparente in locale/ (cartella non versionata: il logo
contiene il marchio ufficiale). Il build poi lo converte alla tavolozza del titolo (tools/logo.py).

Richiede Pillow (solo questo strumento facoltativo; il build usa solo la libreria standard).
Uso:  python tools/prepara_logo.py SORGENTE LINGUA      (LINGUA = ITA o ENG → locale/logo_titolo_LINGUA.png)
"""
import sys
from collections import deque
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
BOX = (18, 22, 238, 168)        # x0, y0, x1, y1 disponibili nello schermo superiore (sotto: "Developed by")
WHITE_TOL = 60                  # distanza massima dal bianco per considerare un pixel sfondo


def remove_white(img):
    img = img.convert("RGBA")
    w, h = img.size
    px = img.load()
    seen = bytearray(w * h)
    q = deque()
    for x in range(w):
        q.append((x, 0)); q.append((x, h - 1))
    for y in range(h):
        q.append((0, y)); q.append((w - 1, y))
    while q:
        x, y = q.popleft()
        if not (0 <= x < w and 0 <= y < h) or seen[y * w + x]:
            continue
        seen[y * w + x] = 1
        r, g, b, a = px[x, y]
        if a < 16 or (255 - min(r, g, b)) <= WHITE_TOL:
            px[x, y] = (255, 255, 255, 0)
            q.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))
    return img


def main():
    if len(sys.argv) != 3 or sys.argv[2] not in ("ITA", "ENG"):
        sys.exit(__doc__)
    img = remove_white(Image.open(sys.argv[1]))
    img = img.crop(img.getbbox())
    bw, bh = BOX[2] - BOX[0], BOX[3] - BOX[1]
    s = min(bw / img.width, bh / img.height)
    size = (max(1, round(img.width * s)), max(1, round(img.height * s)))
    small = img.resize(size, Image.LANCZOS)
    # niente semitrasparenze: il DS ha solo pieno/trasparente
    a = small.getchannel("A").point(lambda v: 255 if v >= 128 else 0)
    small.putalpha(a)
    out = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    x = BOX[0] + (bw - size[0]) // 2
    y = BOX[1] + (bh - size[1]) // 2
    out.paste(small, (x, y), small)
    dst = ROOT / "locale" / f"logo_titolo_{sys.argv[2]}.png"
    dst.parent.mkdir(exist_ok=True)
    out.save(dst)
    print(f"{dst.relative_to(ROOT)}: logo {size[0]}x{size[1]} in ({x},{y})")


if __name__ == "__main__":
    main()
