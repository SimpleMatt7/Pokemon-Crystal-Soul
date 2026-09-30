"""Grafica 2D del DS (formati Nitro): tavolozze NCLR, tile NCGR, mappe NSCR, compressione LZ10; PNG in uscita.
Solo libreria standard (PNG scritto a mano con zlib).

Uso:  python tools/gfx.py esporta a/0/4/6 OUTDIR     tutti i membri di un NARC: per ogni NSCR/NCGR un PNG
                                                     (tavolozza e tile scelti con euristica: vanno verificati)
      python tools/gfx.py png a/0/4/6 NCGR NCLR [NSCR] OUT.png [--pal N]
Da codice: nclr(b), ncgr(b), nscr(b), render(...), write_png(path, w, h, rgba)
"""
import struct
import sys
import zlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ndsfs import parse_narc  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


# ------------------------------------------------------------------ LZ10
def lz10_decompress(b):
    assert b[0] == 0x10, "non è LZ10"
    size = b[1] | (b[2] << 8) | (b[3] << 16)
    out = bytearray()
    i = 4
    while len(out) < size:
        flags = b[i]; i += 1
        for bit in range(8):
            if len(out) >= size:
                break
            if flags & (0x80 >> bit):
                n = (b[i] >> 4) + 3
                disp = (((b[i] & 0xF) << 8) | b[i + 1]) + 1
                i += 2
                for _ in range(n):
                    out.append(out[-disp])
            else:
                out.append(b[i]); i += 1
    return bytes(out)


def lz10_compress(data):
    """Compressione LZ10 semplice (ricerca nella finestra da 4 KB, greedy)."""
    out = bytearray([0x10, len(data) & 0xFF, (len(data) >> 8) & 0xFF, (len(data) >> 16) & 0xFF])
    i, n = 0, len(data)
    while i < n:
        flag_pos = len(out); out.append(0); flags = 0
        for bit in range(8):
            if i >= n:
                break
            best_len, best_disp = 0, 0
            start = max(0, i - 4096)
            maxlen = min(18, n - i)
            if maxlen >= 3:
                j = data.rfind(data[i:i + 3], start, i + 2)
                while j != -1 and j >= start:
                    if j < i:
                        ln = 3
                        while ln < maxlen and data[j + ln] == data[i + ln]:
                            ln += 1
                        if ln > best_len:
                            best_len, best_disp = ln, i - j
                            if ln == maxlen:
                                break
                    j = data.rfind(data[i:i + 3], start, j + 2) if j > start else -1
            if best_len >= 3:
                flags |= 0x80 >> bit
                d = best_disp - 1
                out += bytes([((best_len - 3) << 4) | (d >> 8), d & 0xFF])
                i += best_len
            else:
                out.append(data[i]); i += 1
        out[flag_pos] = flags
    while len(out) % 4:
        out.append(0)
    return bytes(out)


def maybe_lz(b):
    if b[:1] == b"\x10" and b[4:8] not in (b"RLCN", b"RGCN", b"RCSN") and len(b) > 4:
        try:
            d = lz10_decompress(b)
            if d[:4] in (b"RLCN", b"RGCN", b"RCSN", b"RECN", b"RNAN"):
                return d, True
        except Exception:  # noqa: BLE001
            pass
    return b, False


# ------------------------------------------------------------------ formati Nitro
def _section(b, magic):
    o = struct.unpack_from("<H", b, 12)[0]  # header size
    while o < len(b):
        m, size = b[o:o + 4], struct.unpack_from("<I", b, o + 4)[0]
        if m == magic:
            return o
        o += size
    raise ValueError(f"sezione {magic} non trovata")


def bgr555(c):
    r, g, bl = c & 31, (c >> 5) & 31, (c >> 10) & 31
    return (r * 255 // 31, g * 255 // 31, bl * 255 // 31)


def nclr(b):
    """→ (bit per pixel, [colori (r,g,b)]) """
    o = _section(b, b"TTLP")
    depth, _, size, off = struct.unpack_from("<IIII", b, o + 8)
    data = b[o + 8 + off:o + 8 + off + size]
    cols = [bgr555(c) for c in struct.unpack_from(f"<{len(data) // 2}H", data)]
    return (4 if depth == 3 else 8), cols, (o + 8 + off)


def ncgr(b):
    """→ (bpp, tiles: lista di 64 indici per tile, larghezza in tile (o 0))"""
    o = _section(b, b"RAHC")
    h, w, depth, _mapping, tiled, size, off = struct.unpack_from("<HHIIIII", b, o + 8)
    bpp = 4 if depth == 3 else 8
    data = b[o + 8 + off:o + 8 + off + size]
    tiles = []
    step = 32 if bpp == 4 else 64
    for t in range(0, len(data) - step + 1, step):
        chunk = data[t:t + step]
        if bpp == 4:
            px = []
            for byte in chunk:
                px += [byte & 0xF, byte >> 4]
        else:
            px = list(chunk)
        tiles.append(px)
    return bpp, tiles, (w if w != 0xFFFF else 0), (o + 8 + off)


def nscr(b):
    """→ (larghezza px, altezza px, [voci u16])"""
    o = _section(b, b"NRCS")
    w, h, _, size = struct.unpack_from("<HHII", b, o + 8)
    data = b[o + 20:o + 20 + size]
    return w, h, list(struct.unpack_from(f"<{len(data) // 2}H", data)), o + 20


def render(tiles, colors, bpp, screen=None, width_tiles=None, pal_base=0):
    """Immagine RGBA. Con `screen` (w, h, voci) usa la mappa; altrimenti dispone i tile su `width_tiles` colonne."""
    if screen:
        w, h, ents = screen[:3]
        tw = w // 8
    else:
        tw = width_tiles or 16
        ents = list(range(len(tiles)))
        w, h = tw * 8, ((len(ents) + tw - 1) // tw) * 8
    rgba = bytearray(w * h * 4)
    for k, e in enumerate(ents):
        tx, ty = (k % tw) * 8, (k // tw) * 8
        if ty >= h:
            break
        if screen:
            ti, hf, vf, pal = e & 0x3FF, (e >> 10) & 1, (e >> 11) & 1, e >> 12
        else:
            ti, hf, vf, pal = e, 0, 0, 0
        if ti >= len(tiles):
            continue
        px = tiles[ti]
        for y in range(8):
            for x in range(8):
                sx, sy = (7 - x if hf else x), (7 - y if vf else y)
                v = px[sy * 8 + sx]
                ci = (pal_base + pal) * 16 + v if bpp == 4 else v
                c = colors[ci] if ci < len(colors) else (255, 0, 255)
                o = ((ty + y) * w + tx + x) * 4
                rgba[o:o + 4] = bytes((*c, 255))
    return w, h, bytes(rgba)


def write_png(path, w, h, rgba):
    raw = b"".join(b"\0" + rgba[y * w * 4:(y + 1) * w * 4] for y in range(h))
    def chunk(t, d):
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)
    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b"")
    Path(path).write_bytes(png)


def load_member(narc_path, i, base="IPKI"):
    files = parse_narc((ROOT / "work" / base / "files" / narc_path).read_bytes())
    return maybe_lz(files[i])[0]


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    a = sys.argv[1:]
    if len(a) >= 2 and a[0] == "esporta":
        files = [maybe_lz(f)[0] for f in parse_narc((ROOT / "work/IPKI/files" / a[1]).read_bytes())]
        out = Path(a[2]); out.mkdir(parents=True, exist_ok=True)
        kinds = {i: f[:4] for i, f in enumerate(files)}
        pals = [i for i, k in kinds.items() if k == b"RLCN"]
        for i, k in kinds.items():
            print(i, k.decode(errors="replace"), len(files[i]))
            if k != b"RGCN" or not pals:
                continue
            p = max((x for x in pals if x < i), default=pals[0])
            bpp, tiles, wt, _ = ncgr(files[i])
            _, cols, _ = nclr(files[p])
            write_png(out / f"{i:03d}_tiles_pal{p}.png", *render(tiles, cols, bpp, width_tiles=wt or 32))
            nxt = [j for j, kk in kinds.items() if kk == b"RCSN" and j > i]
            if nxt:
                write_png(out / f"{i:03d}_scr{nxt[0]}_pal{p}.png", *render(tiles, cols, bpp, screen=nscr(files[nxt[0]])))
    elif len(a) >= 5 and a[0] == "png":
        pal = int(a[a.index("--pal") + 1]) if "--pal" in a else 0
        args = [x for x in a[2:] if x != "--pal" and not (a.index(x) > 0 and a[a.index(x) - 1] == "--pal")]
        g, p = load_member(a[1], int(args[0])), load_member(a[1], int(args[1]))
        bpp, tiles, wt, _ = ncgr(g)
        _, cols, _ = nclr(p)
        scr = nscr(load_member(a[1], int(args[2]))) if len(args) > 3 else None
        write_png(args[-1], *render(tiles, cols, bpp, screen=scr, width_tiles=wt or 32, pal_base=pal))
        print(args[-1])
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()


def read_png(path):
    """PNG non interlacciato, 8 bit per canale (RGB, RGBA, grigio, indicizzato) → (w, h, [(r,g,b,a)] riga per riga)."""
    b = Path(path).read_bytes()
    assert b[:8] == b"\x89PNG\r\n\x1a\n", "non è un PNG"
    o, idat, plte, trns = 8, b"", None, None
    while o < len(b):
        n = struct.unpack(">I", b[o:o + 4])[0]
        t, d = b[o + 4:o + 8], b[o + 8:o + 8 + n]
        if t == b"IHDR":
            w, h, depth, ctype, _, _, inter = struct.unpack(">IIBBBBB", d)
        elif t == b"PLTE":
            plte = [tuple(d[i:i + 3]) for i in range(0, len(d), 3)]
        elif t == b"tRNS":
            trns = d
        elif t == b"IDAT":
            idat += d
        o += 12 + n
    assert depth == 8 and inter == 0, "servono PNG a 8 bit non interlacciati"
    ch = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}[ctype]
    raw = zlib.decompress(idat)
    stride = w * ch
    prev = bytearray(stride)
    px = []
    i = 0
    for _ in range(h):
        f = raw[i]; line = bytearray(raw[i + 1:i + 1 + stride]); i += 1 + stride
        for k in range(stride):
            a = line[k - ch] if k >= ch else 0
            up = prev[k]
            c = prev[k - ch] if k >= ch else 0
            if f == 1:
                line[k] = (line[k] + a) & 255
            elif f == 2:
                line[k] = (line[k] + up) & 255
            elif f == 3:
                line[k] = (line[k] + (a + up) // 2) & 255
            elif f == 4:
                p = a + up - c
                pa, pb, pc = abs(p - a), abs(p - up), abs(p - c)
                line[k] = (line[k] + (a if pa <= pb and pa <= pc else up if pb <= pc else c)) & 255
        prev = line
        for x in range(w):
            q = line[x * ch:(x + 1) * ch]
            if ctype == 6:
                px.append(tuple(q))
            elif ctype == 2:
                px.append((*q, 255))
            elif ctype == 0:
                px.append((q[0], q[0], q[0], 255))
            elif ctype == 4:
                px.append((q[0], q[0], q[0], q[1]))
            else:
                al = trns[q[0]] if trns and q[0] < len(trns) else 255
                px.append((*plte[q[0]], al))
    return w, h, px
