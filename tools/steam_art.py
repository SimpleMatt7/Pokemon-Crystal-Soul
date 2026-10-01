"""Grafiche per Steam ROM Manager (uso personale): copertina, griglia, hero, logo e icona di "Pokémon Crystal Soul".

Composte al momento dalla ROM estratta (cielo del titolo, sprite di Ho-Oh e Lugia, icona del banner costruita) e
dal logo disegnato in locale/ (logo_sorgente_<lingua>.webp, cartella non versionata). Le immagini contengono
marchio e grafica del gioco: vanno in out/steam/<lingua>/ (ignorata da git), mai nel repository.
Come nel titolo del gioco (D39-D40): cielo dorato con Ho-Oh a sinistra, azzurro con Lugia a destra.

Richiede Pillow (strumento facoltativo, come prepara_logo.py) e un build già fatto (per l'icona del banner).
Uso:  python tools/steam_art.py [--base IPKI|IPKE]
"""
import sys
from pathlib import Path

from PIL import Image, ImageFilter

sys.path.insert(0, str(Path(__file__).resolve().parent))
import logo  # noqa: E402
from prepara_logo import remove_white  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
HO_OH, LUGIA, SUICUNE = 250, 249, 245
SIZES = {"poster": (600, 900), "grid": (920, 430), "hero": (1920, 620)}   # nomi come in Steam ROM Manager


def indexed_to_image(img, cols, transparent0=True):
    h, w = len(img), len(img[0])
    out = Image.new("RGBA", (w, h))
    out.putdata([(0, 0, 0, 0) if (v == 0 and transparent0) else (*cols[v], 255) for row in img for v in row])
    return out


def sky(base, w, h):
    """Cielo del titolo, oro a sinistra e azzurro a destra (sfumati al centro), ingrandito per coprire w x h."""
    # cielo senza Suicune: ingrandito, il Suicune dell'angolo spunterebbe a pezzi dietro gli uccelli
    img, cols = logo.load_indexed(logo.SKY_CHR, logo.SS_PAL, scr=logo.SKY_SCR, base=base)
    blue = indexed_to_image(img, cols, transparent0=False).convert("RGB")
    gold = indexed_to_image(img, logo.gold_colors(cols), transparent0=False).convert("RGB")
    s = max(w / 256, h / 192)
    size = (round(256 * s), round(192 * s))
    box = ((size[0] - w) // 2, (size[1] - h) // 2)
    blue, gold = (im.resize(size, Image.BICUBIC).crop((*box, box[0] + w, box[1] + h)) for im in (blue, gold))
    mask = Image.new("L", (w, h))
    ramp = []
    for x in range(w):
        t = min(1.0, max(0.0, (x / w - 0.3) / 0.4))
        ramp.append(round(255 * t * t * (3 - 2 * t)))
    mask.putdata(ramp * h)
    mixed = Image.composite(blue, gold, mask)
    # oro + azzurro a metà danno verde: la transizione passa invece dal bianco del bagliore
    glow = Image.new("L", (w, h))
    glow.putdata([round(r * (255 - r) * 4 * 0.8 / 255) for r in ramp] * h)
    return Image.composite(Image.new("RGB", (w, h), (255, 255, 250)), mixed, glow).convert("RGBA")


def sprite(base, species, scale, mirror=False):
    img, cols = logo.pokemon_front(species, base)
    im = indexed_to_image(img, cols)
    im = im.crop(im.getbbox())
    if mirror:
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    return im.resize((im.width * scale, im.height * scale), Image.NEAREST)


def logo_image(base):
    src = ROOT / "locale" / f"logo_sorgente_{logo.LANG[base]}.webp"
    if not src.exists():
        sys.exit(f"Manca {src.relative_to(ROOT)} (logo disegnato, cartella locale)")
    im = remove_white(Image.open(src))
    return im.crop(im.getbbox())


def fit(im, width):
    return im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)


def paste_shadow(canvas, im, xy, blur=12, opacity=110):
    """Incolla con un'ombra morbida sotto (leggibilità sul cielo chiaro)."""
    a = im.getchannel("A").point(lambda v: opacity if v else 0)
    pad = blur * 3
    sh = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    black = Image.new("RGBA", im.size, (0, 0, 0, 255))
    sh.paste(black, (pad, pad), a)
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    canvas.alpha_composite(sh, (xy[0] - pad + blur // 2, xy[1] - pad + blur))
    canvas.alpha_composite(im, xy)


def compose(base, kind, lg):
    w, h = SIZES[kind]
    c = sky(base, w, h)
    if kind == "hero":           # niente logo: Steam lo mette sopra da solo
        ho, lu = sprite(base, HO_OH, 6, mirror=True), sprite(base, LUGIA, 6)
        paste_shadow(c, ho, (w * 27 // 100 - ho.width // 2, (h - ho.height) // 2), blur=16)
        paste_shadow(c, lu, (w * 73 // 100 - lu.width // 2, (h - lu.height) // 2), blur=16)
        su = sprite(base, SUICUNE, 5)                    # al centro, tra i due (guarda a destra come nel titolo)
        paste_shadow(c, su, ((w - su.width) // 2, h - su.height - 40), blur=14)
    elif kind == "poster":
        ho, lu = sprite(base, HO_OH, 4, mirror=True), sprite(base, LUGIA, 4)
        paste_shadow(c, ho, (w // 4 - ho.width // 2 - 20, h - ho.height - 140))
        paste_shadow(c, lu, (w * 3 // 4 - lu.width // 2 + 20, h - lu.height - 140))
        su = sprite(base, SUICUNE, 3)                    # davanti, al centro in basso
        paste_shadow(c, su, ((w - su.width) // 2, h - su.height - 15))
        l2 = fit(lg, w - 60)
        paste_shadow(c, l2, ((w - l2.width) // 2, 70))
    else:                        # grid (orizzontale)
        ho, lu = sprite(base, HO_OH, 3, mirror=True), sprite(base, LUGIA, 3)
        paste_shadow(c, ho, (20, (h - ho.height) // 2 + 20))
        paste_shadow(c, lu, (w - lu.width - 20, (h - lu.height) // 2 + 20))
        l2 = fit(lg, 440)
        paste_shadow(c, l2, ((w - l2.width) // 2, (h - l2.height) // 2 - 10))
    return c


def main():
    base = "IPKI"
    if "--base" in sys.argv:
        base = sys.argv[sys.argv.index("--base") + 1]
    lang = logo.LANG[base]
    out = ROOT / "out" / "steam" / lang
    out.mkdir(parents=True, exist_ok=True)
    lg = logo_image(base)
    for kind in SIZES:
        compose(base, kind, lg).save(out / f"{kind}.png")
    fit(lg, min(1280, lg.width)).save(out / "logo.png")
    build = ROOT / "work" / ("build" if base == "IPKI" else f"build_{base}") / "banner" / "bitmap.png"
    if build.exists():           # icona: quella del banner (Poké Ball azzurro cristallo, D41), 8x
        Image.open(build).convert("RGBA").resize((256, 256), Image.NEAREST).save(out / "icon.png")
    else:
        print(f"icona saltata: manca {build.relative_to(ROOT)} (eseguire prima il build)")
    for f in sorted(out.iterdir()):
        print(f.relative_to(ROOT), Image.open(f).size)


if __name__ == "__main__":
    main()
