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
BOX = (14, 22, 242, 176)        # zona disponibile nello schermo superiore ("Developed by GAME FREAK" parte da y=181)
# parola gialla "Pokémon" nei loghi originali (x iniziale, y iniziale, larghezza): il logo nuovo viene scalato e
# posizionato perché la sua coincida. Italiano: x 37..221, y da 42; inglese: x 31..211, y da 47.
POKEMON_ORIG = {"ITA": (37, 42, 185), "ENG": (31, 47, 181)}
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


def yellow_bbox(img):
    """Riquadro dei pixel gialli (la parola "Pokémon")."""
    px = img.load()
    xs, ys = [], []
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = px[x, y]
            if a > 128 and r > 200 and g > 170 and b < 120:
                xs.append(x); ys.append(y)
    return min(xs), min(ys), max(xs), max(ys)


def main():
    if len(sys.argv) != 3 or sys.argv[2] not in ("ITA", "ENG"):
        sys.exit(__doc__)
    img = remove_white(Image.open(sys.argv[1]))
    img = img.crop(img.getbbox())
    bw, bh = BOX[2] - BOX[0], BOX[3] - BOX[1]
    yx0, yy0, yx1, _ = yellow_bbox(img)
    px0, py0, pw = POKEMON_ORIG[sys.argv[2]]
    s = pw / (yx1 - yx0 + 1)
    size = (max(1, round(img.width * s)), max(1, round(img.height * s)))
    x = round(px0 - yx0 * s)
    y = round(py0 - yy0 * s)
    if not (BOX[0] <= x and x + size[0] <= BOX[2] and BOX[1] <= y and y + size[1] <= BOX[3]):
        print(f"attenzione: alla grandezza originale il logo esce dalla zona {BOX}: lo riduco")
        s = min(bw / img.width, bh / img.height)
        size = (max(1, round(img.width * s)), max(1, round(img.height * s)))
        x, y = BOX[0] + (bw - size[0]) // 2, BOX[1] + (bh - size[1]) // 2
    small = img.resize(size, Image.LANCZOS)
    # niente semitrasparenze: il DS ha solo pieno/trasparente
    a = small.getchannel("A").point(lambda v: 255 if v >= 128 else 0)
    small.putalpha(a)
    out = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    out.paste(small, (x, y), small)
    dst = ROOT / "locale" / f"logo_titolo_{sys.argv[2]}.png"
    dst.parent.mkdir(exist_ok=True)
    out.save(dst)
    print(f"{dst.relative_to(ROOT)}: logo {size[0]}x{size[1]} in ({x},{y})")


if __name__ == "__main__":
    main()
