"""Prepara un logo disegnato a parte (PNG/WebP qualsiasi, sfondo bianco o trasparente) per il titolo.

Toglie lo sfondo bianco partendo dai bordi (i bianchi interni restano) e separa le parti del disegno: la parola
"Pokémon" (scalata come quella originale), il ™ (scartato: il build usa quello originale) e la scritta sotto,
ridimensionata per stare nel riquadro della scritta del logo originale di SoulSilver della stessa lingua. Salva un
PNG 256x256 trasparente in locale/ (cartella non versionata: il logo contiene il marchio ufficiale). Il build poi lo
converte alla tavolozza del titolo (tools/logo.py). Serve la ROM estratta (work/IPKI o work/IPKE).

Richiede Pillow (solo questo strumento facoltativo; il build usa solo la libreria standard).
Uso:  python tools/prepara_logo.py SORGENTE LINGUA [--scritta=0.9]   (LINGUA = ITA o ENG → locale/logo_titolo_LINGUA.png)
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
# scritta sotto "Pokémon" rispetto al riquadro di quella originale (--scritta=0.9 per cambiarla): in italiano un po'
# più piccola perché lasci spazio a Suicune nell'angolo in basso a sinistra del titolo
SUB_SCALE = {"ITA": 0.85, "ENG": 1.0}


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


def components(img):
    """Parti staccate del logo (pixel pieni collegati): [(area, pixel gialli, riquadro, maschera di indici)]."""
    w, h = img.size
    a = img.getchannel("A").tobytes()
    px = img.load()
    lab = bytearray(w * h)
    out = []
    for s in range(w * h):
        if a[s] <= 128 or lab[s]:
            continue
        lab[s] = 1
        q, pts, yel = deque([s]), [], 0
        while q:
            p = q.popleft()
            pts.append(p)
            y, x = divmod(p, w)
            r, g, b, _ = px[x, y]
            yel += r > 200 and g > 170 and b < 120
            for d in (p - 1, p + 1, p - w, p + w):
                if 0 <= d < w * h and not lab[d] and a[d] > 128 and abs(d % w - x) <= 1:
                    lab[d] = 1
                    q.append(d)
        xs, ys = [p % w for p in pts], [p // w for p in pts]
        out.append((len(pts), yel, (min(xs), min(ys), max(xs) + 1, max(ys) + 1), pts))
    return out


def only(img, parts):
    """Copia dell'immagine con solo i pixel delle parti indicate."""
    w = img.width
    keep = bytearray(w * img.height)
    for *_, pts in parts:
        for p in pts:
            keep[p] = 1
    out = Image.new("RGBA", img.size, (0, 0, 0, 0))
    src, dst = img.load(), out.load()
    for p in range(len(keep)):
        if keep[p]:
            dst[p % w, p // w] = src[p % w, p // w]
    return out


def original_subtitle_box(lang):
    """Riquadro della scritta sotto "Pokémon" nel logo originale di SoulSilver della stessa lingua (dalla ROM)."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import logo
    base = {"ITA": "IPKI", "ENG": "IPKE"}[lang]
    img, cols = logo.load_indexed(logo.SS_LOGO, logo.SS_PAL, base=base)
    yel = [y for y in range(256) for x in range(256)
           if img[y][x] and cols[img[y][x]][0] > 200 and cols[img[y][x]][1] > 170 and cols[img[y][x]][2] < 120]
    pts = [(x, y) for y in range(max(yel) + 8, 180) for x in range(256) if img[y][x]]
    return min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts) + 1, max(p[1] for p in pts) + 1


def binarize(im):
    """Niente semitrasparenze: il DS ha solo pieno/trasparente."""
    im.putalpha(im.getchannel("A").point(lambda v: 255 if v >= 128 else 0))
    return im


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--scritta=")]
    scale_sub = next((float(a.split("=")[1]) for a in sys.argv[1:] if a.startswith("--scritta=")), None)
    if len(args) != 2 or args[1] not in ("ITA", "ENG"):
        sys.exit(__doc__)
    lang = args[1]
    if scale_sub is None:
        scale_sub = SUB_SCALE[lang]
    img = remove_white(Image.open(args[0]))
    img = img.crop(img.getbbox())
    parts = components(img)
    total = sum(p[0] for p in parts)
    pokemon = max(parts, key=lambda p: p[1])                   # la parte con il giallo
    small = [p for p in parts if p is not pokemon and p[0] < total * 0.01]   # ™ (T e M): si usa quello originale
    subtitle = [p for p in parts if p is not pokemon and p not in small]
    # "Pokémon": scalata e posizionata come quella originale (poi il build usa comunque la parola originale)
    yx0, yy0, yx1, _ = yellow_bbox(img)
    px0, py0, pw = POKEMON_ORIG[lang]
    s = pw / (yx1 - yx0 + 1)
    top = only(img, [pokemon])
    top = binarize(top.resize((max(1, round(img.width * s)), max(1, round(img.height * s))), Image.LANCZOS))
    out = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    out.alpha_composite(top, (round(px0 - yx0 * s), round(py0 - yy0 * s)))
    # scritta sotto: nel riquadro di quella originale ("Versione Argento / SoulSilver"), centrata, in alto
    sub = only(img, subtitle)
    sub = sub.crop(sub.getbbox())
    bx0, by0, bx1, by1 = original_subtitle_box(lang)
    k = min((bx1 - bx0) / sub.width, (by1 - by0) / sub.height) * scale_sub
    sub = binarize(sub.resize((max(1, round(sub.width * k)), max(1, round(sub.height * k))), Image.LANCZOS))
    out.alpha_composite(sub, ((bx0 + bx1 - sub.width) // 2, by0))
    dst = ROOT / "locale" / f"logo_titolo_{lang}.png"
    dst.parent.mkdir(exist_ok=True)
    out.save(dst)
    print(f"{dst.relative_to(ROOT)}: scritta {sub.width}x{sub.height} nel riquadro originale "
          f"{bx1 - bx0}x{by1 - by0} in ({bx0},{by0}); ™ originale")


if __name__ == "__main__":
    main()
