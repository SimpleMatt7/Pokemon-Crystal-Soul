"""Logo del titolo "Pokémon Versione Crystal Soul", generato al momento del build dal logo di SoulSilver della ROM.

Nel repository non c'è grafica del gioco: qui ci sono solo le operazioni (cancellature, spostamenti) e le forme
delle lettere nuove disegnate da noi (maschere a un bit qui sotto). I colori delle lettere nuove sono presi
dalla tavolozza del logo originale, riga per riga, per avere lo stesso aspetto metallico.

Uso:  python tools/logo.py anteprima OUT.png     (anteprima ingrandita 2x)
Da codice: build_logo() → (immagine indicizzata 256x256, tavolozza) ; encode(...) → (NCGR, NSCR) nuovi.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gfx  # noqa: E402

TITLE_NARC = "a/0/4/6"
SS_LOGO, SS_PAL, LOGO_SCR = 1, 2, 0     # membri di a/0/4/6 (title_screen.c: versione SoulSilver)

# --------------------------------------------------------------- lettere nuove (disegnate per questo progetto)
# '#' = pieno. Minuscole-maiuscoletto alte 15 righe (y 111..125 nel logo), maiuscola C alta 20 (y 106..125).
GLYPHS = {
    "C": """
.....#######...
...###########.
..#####...####.
.#####.....###.
.####.......##.
#####..........
####...........
####...........
####...........
####...........
####...........
####...........
####...........
#####..........
.####.......##.
.#####.....###.
..#####...####.
...###########.
.....#######...
......#####....
""",
    "R": """
#########..
##########.
####...####
####...####
####...####
####..####.
#########..
########...
####.####..
####..####.
####..####.
####...####
####...####
####....###
####....###
""",
    "Y": """
####....####
####....####
.####..####.
.####..####.
..########..
..########..
...######...
....####....
....####....
....####....
....####....
....####....
....####....
....####....
....####....
""",
    "S": """
..#######..
.#########.
####...####
####....##.
#####......
.########..
..########.
......#####
.......####
##.....####
####...####
.#########.
..#######..
...........
...........
""",
    "T": """
############
############
############
....####....
....####....
....####....
....####....
....####....
....####....
....####....
....####....
....####....
....####....
....####....
....####....
""",
    "A": """
....####....
....####....
...######...
...######...
..###..###..
..###..###..
.####..####.
.####..####.
.##########.
############
####....####
####....####
####....####
####....####
####....####
""",
    "L": """
####.......
####.......
####.......
####.......
####.......
####.......
####.......
####.......
####.......
####.......
####.......
####.......
###########
###########
###########
""",
}


def glyph(ch):
    rows = [r for r in GLYPHS[ch].strip("\n").split("\n")]
    w = max(len(r) for r in rows)
    return [[1 if x < len(r) and r[x] == "#" else 0 for x in range(w)] for r in rows]


# --------------------------------------------------------------- logo di partenza (dalla ROM)
def load_indexed(member, pal, scr=LOGO_SCR, base="IPKI"):
    G = gfx.load_member(TITLE_NARC, member, base)
    P = gfx.load_member(TITLE_NARC, pal, base)
    S = gfx.load_member(TITLE_NARC, scr, base)
    bpp, tiles, _, _ = gfx.ncgr(G)
    _, cols, _ = gfx.nclr(P)
    w, h, ents, _ = gfx.nscr(S)
    img = [[0] * w for _ in range(h)]
    for k, e in enumerate(ents):
        tx, ty = (k % (w // 8)) * 8, (k // (w // 8)) * 8
        ti, hf, vf = e & 0x3FF, (e >> 10) & 1, (e >> 11) & 1
        for y in range(8):
            for x in range(8):
                img[ty + y][tx + x] = tiles[ti][(7 - y if vf else y) * 8 + (7 - x if hf else x)]
    return img, cols


# stile preso dal logo SS: riempimento per riga dalla colonna del gambo della E di "ARGENTO" (x=187, y=110..125)
FILL_COL, FILL_Y0, FILL_Y1 = 187, 110, 125
OUTLINE = 31        # blu scuro del contorno
SHADOW = (85, 26)   # righe d'ombra sotto le lettere


def draw_word(img, word, x, bottom, fill, spacing=1):
    masks = []
    for ch in word:
        g = glyph(ch)
        masks.append((x, bottom - len(g) + 1, g))
        x += len(g[0]) + spacing
    cover = set()
    for gx, gy, g in masks:
        for yy, row in enumerate(g):
            for xx, v in enumerate(row):
                if v:
                    cover.add((gx + xx, gy + yy))
    # ombra sotto, contorno intorno, poi riempimento
    for (px, py) in cover:
        for k, idx in enumerate(SHADOW, 1):
            if (px, py + k) not in cover:
                img[py + k][px] = idx
    for (px, py) in cover:
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1)):
            q = (px + dx, py + dy)
            if q not in cover:
                img[q[1]][q[0]] = OUTLINE
    for (px, py) in cover:
        # riga del riempimento proporzionale all'altezza della lettera
        gx, gy, g = next(m for m in masks if m[0] <= px < m[0] + len(m[2][0]))
        t = (py - gy) / max(1, len(g) - 1)
        img[py][px] = fill[round(t * (len(fill) - 1))]
    return x


def erase(img, x0, y0, x1, y1):
    for y in range(y0, y1):
        for x in range(x0, x1):
            img[y][x] = 0


def move(img, x0, y0, x1, y1, dx, dy):
    block = [row[x0:x1] for row in img[y0:y1]]
    erase(img, x0, y0, x1, y1)
    for yy, row in enumerate(block):
        for xx, v in enumerate(row):
            if v:
                img[y0 + yy + dy][x0 + xx + dx] = v


def cut(img, x0, y0, x1, y1):
    block = [row[x0:x1] for row in img[y0:y1]]
    return (x0, y0, block)


def paste(img, piece, dx):
    x0, y0, block = piece
    for yy, row in enumerate(block):
        for xx, v in enumerate(row):
            if v:
                img[y0 + yy][x0 + xx + dx] = v


def build_logo(base="IPKI"):
    img, cols = load_indexed(SS_LOGO, SS_PAL, base=base)
    custom = local_logo(base)
    if custom:                # logo rifatto a mano (cartella locale, non versionata)
        return import_png(custom, cols), cols
    fill = [img[y][FILL_COL] for y in range(FILL_Y0, FILL_Y1 + 1)]  # sfumatura, letta prima di cancellare
    # riga piccola (y <= 130): via "ARGENTO"
    erase(img, 131, 103, 245, 131)
    # riga grande (y >= 131): "SOUL" + ala di Lugia, senza "SILVER", centrati
    soul = cut(img, 56, 131, 117, 162)
    wing = cut(img, 191, 126, 228, 170)
    erase(img, 56, 131, 245, 172)
    paste(img, soul, +27)      # SOUL: x 83..143
    paste(img, wing, -47)      # ala subito dopo
    # riga piccola: "CRYSTAL" dopo "VERSIONE" (uno spazio)
    draw_word(img, "CRYSTAL", 138, 125, fill, spacing=0)
    return img, cols


LOCAL_DIR = Path(__file__).resolve().parent.parent / "locale"
LANG = {"IPKI": "ITA", "IPKE": "ENG"}


def local_logo(base):
    """Logo rifatto a mano per la lingua della ROM (locale/logo_titolo_ITA.png / _ENG.png), se c'è."""
    for name in (f"logo_titolo_{LANG.get(base, base)}.png", "logo_titolo.png"):
        if (LOCAL_DIR / name).exists():
            return LOCAL_DIR / name
    return None


def import_png(path, cols):
    """Logo rifatto (PNG 256x256, trasparente dove non c'è logo) → immagine indicizzata sulla tavolozza del
    logo SS (condivisa con il cielo del titolo: non si cambia, si usa il colore più vicino)."""
    w, h, px = gfx.read_png(path)
    assert (w, h) == (256, 256), f"il logo deve essere 256x256 (è {w}x{h})"
    cache, img = {}, []
    for y in range(h):
        row = []
        for x in range(w):
            r, g, b, a = px[y * w + x]
            if a < 128:
                row.append(0); continue
            k = (r >> 3, g >> 3, b >> 3)
            if k not in cache:
                cache[k] = min(range(1, len(cols)), key=lambda i: (cols[i][0] - r) ** 2 * 3 + (cols[i][1] - g) ** 2 * 4 + (cols[i][2] - b) ** 2 * 2)
            row.append(cache[k])
        img.append(row)
    return img


def encode(img, ncgr_orig, nscr_orig):
    """Immagine indicizzata (8bpp) → (NCGR, NSCR) nuovi, con tile deduplicati; intestazioni prese dagli originali."""
    import struct
    h, w = len(img), len(img[0])
    tiles, index, ents = [], {}, []
    for ty in range(0, h, 8):
        for tx in range(0, w, 8):
            t = bytes(img[ty + y][tx + x] for y in range(8) for x in range(8))
            if t not in index:
                index[t] = len(tiles)
                tiles.append(t)
            ents.append(index[t])
    # NCGR: sostituisce i dati della sezione RAHC
    o = gfx._section(ncgr_orig, b"RAHC")
    hdr = bytearray(ncgr_orig[o:o + 32])
    data = b"".join(tiles)
    struct.pack_into("<I", hdr, 4, 32 + len(data))        # dimensione sezione
    struct.pack_into("<HH", hdr, 8, 1, len(tiles))          # altezza, larghezza in tile
    struct.pack_into("<I", hdr, 24, len(data))              # dimensione dati
    rest = ncgr_orig[o + struct.unpack_from("<I", ncgr_orig, o + 4)[0]:]
    body = bytes(hdr) + data + rest
    head = bytearray(ncgr_orig[:o])
    struct.pack_into("<I", head, 8, len(head) + len(body))
    new_ncgr = bytes(head) + body
    # NSCR: stesse dimensioni, voci nuove (tavolozza 0, niente flip)
    so = gfx._section(nscr_orig, b"NRCS")
    sw, sh, _, size = struct.unpack_from("<HHII", nscr_orig, so + 8)
    assert (sw, sh) == (w, h), "dimensioni della mappa diverse dall'immagine"
    scr = bytearray(nscr_orig)
    struct.pack_into(f"<{len(ents)}H", scr, so + 20, *ents)
    return new_ncgr, bytes(scr), len(tiles)


# --------------------------------------------------------------- cielo del titolo con Suicune
SKY_CHR, SKY_SCR = 36, 37          # cielo azzurro (SS), tavolozza SS_PAL (la stessa del logo)
POKEGRA = "a/0/0/4"                # sprite dei Pokémon: 6 file per specie (retro f/m, fronte f/m, tavolozze)
SUICUNE = 245
SUICUNE_POS = (2, 190)             # angolo in basso a sinistra (x sinistro, y del fondo), specchiato verso il logo
# posti liberi della tavolozza del titolo (né cielo né logo; 124-126 li usa la riga "Developed by GAME FREAK")
FREE_SLOTS = [117, 118, 119, 120, 121, 122, 123, 127]
EXACT_DIST = 900                   # oltre questa distanza il colore di Suicune prende un posto libero
SUICUNE_WITH_CUSTOM_LOGO = False   # con un logo disegnato a mano Suicune si sovrappone alle lettere: per ora niente


def pokemon_front(species, base="IPKI"):
    """Sprite frontale 80x80 (prima posa) decifrato → (righe di indici 0-15, colori)."""
    import struct
    G = gfx.load_member(POKEGRA, species * 6 + 3, base)
    P = gfx.load_member(POKEGRA, species * 6 + 4, base)
    o = gfx._section(G, b"RAHC")
    size, off = struct.unpack_from("<II", G, o + 24)
    d = list(struct.unpack_from(f"<{size // 2}H", G, o + 8 + off))
    seed = d[0]
    for i in range(len(d)):          # cifratura degli sprite HGSS: XOR con LCG, seme = prima parola
        d[i] ^= seed
        seed = (seed * 1103515245 + 24691) & 0xFFFF
    raw = struct.pack(f"<{len(d)}H", *d)
    W = 160
    img = [[(raw[(y * W + x) // 2] >> (4 if x & 1 else 0)) & 15 for x in range(80)] for y in range(80)]
    return img, gfx.nclr(P)[1]


def nearest(cols, rgb):
    r, g, b = rgb
    return min(range(1, len(cols)), key=lambda i: (cols[i][0] - r) ** 2 * 3 + (cols[i][1] - g) ** 2 * 4 + (cols[i][2] - b) ** 2 * 2)


def build_sky(base="IPKI"):
    sky, cols = load_indexed(SKY_CHR, SS_PAL, scr=SKY_SCR, base=base)
    if local_logo(base) and not SUICUNE_WITH_CUSTOM_LOGO:
        return sky, cols, {}
    mon, mcols = pokemon_front(SUICUNE, base)
    ys = [y for y in range(80) if any(mon[y])]
    xs = [x for x in range(80) if any(mon[y][x] for y in range(80))]
    x0, y1 = SUICUNE_POS
    top = y1 - (ys[-1] - ys[0])
    used_v = sorted({v for r in mon for v in r if v})
    cmap, extra, free = {}, {}, list(FREE_SLOTS)
    for v in used_v:
        i = nearest(cols, mcols[v])
        d = sum((a - b) ** 2 for a, b in zip(cols[i], mcols[v]))
        if d > EXACT_DIST and free:
            i = free.pop(0)
            extra[i] = mcols[v]
        cmap[v] = i
    cols = list(cols)
    for i, rgb in extra.items():
        cols[i] = rgb
    for y in range(ys[0], ys[-1] + 1):
        for x in range(xs[0], xs[-1] + 1):
            v = mon[y][x]
            if v:
                sky[top + y - ys[0]][x0 + (xs[-1] - x)] = cmap[v]   # specchiato
    return sky, cols, extra


def preview(path, img, cols, z=2):
    h, w = len(img), len(img[0])
    rgba = bytearray()
    for y in range(h * z):
        for x in range(w * z):
            v = img[y // z][x // z]
            rgba += bytes((*(cols[v] if v else (40, 40, 40)), 255))
    gfx.write_png(path, w * z, h * z, bytes(rgba))


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if len(sys.argv) == 3 and sys.argv[1] == "anteprima":
        img, cols = build_logo()
        preview(sys.argv[2], [r[0:256] for r in img[20:180]], cols)
        print(sys.argv[2])
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
