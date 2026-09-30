"""Scena 1 dell'intro con Ho-Oh e poi Lugia: sprite combinato costruito al build dalle risorse della ROM.

Risorse in a/2/6/2 (gs_opening): Ho-Oh (versione HG, usata dal codice) = 23 NCLR, 24 NCGR, 25 NANR, 26 NCER;
Lugia (SS) = 27, 28, 29, 30. In entrambe: cella 0 = sole (tavolozza 0), celle 1-6 = uccello (tavolozza 1);
sequenza 0 = sole, 1 = volo dell'uccello (112 fotogrammi SRT da 3 tick, scala crescente), 2 = ciclo.

Combinato (scritto nei membri 23-26, quelli che il codice HG carica):
  - NCGR: tile di Ho-Oh + tile di Lugia; NCLR: tavolozza 2 = tavolozza 1 di Lugia
  - NCER: celle di Ho-Oh + celle 1-6 di Lugia (tile spostati, tavolozza 2)
  - NANR sequenza 1: Ho-Oh esce dal sole (HOOH_OUT fotogrammi), ci rientra (al contrario, più veloce), poi esce Lugia.
Codice (codice.csv): 3 tavolozze caricate invece di 2; l'uccello compare dopo 10 tick invece di 128 e la
dissolvenza parte dopo 208 invece di 90 (durata totale della scena invariata: la musica resta sincronizzata).
"""
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gfx  # noqa: E402

NARC = "a/2/6/2"
HOOH = dict(pal=23, chr=24, anm=25, cel=26)
LUGIA = dict(pal=27, chr=28, anm=29, cel=30)
HOOH_OUT = 28          # fotogrammi di Ho-Oh in uscita (scala ~0.33)
HOOH_BACK_STEP = 3     # rientro nel sole: un fotogramma ogni 3, al contrario (più veloce)


def _sec(b, magic):
    o = gfx._section(b, magic)
    return o, struct.unpack_from("<I", b, o + 4)[0]


def _replace_section(b, magic, new_body):
    """Sostituisce il contenuto (dopo magic+size) di una sezione, aggiornando le dimensioni."""
    o, size = _sec(b, magic)
    sec = magic + struct.pack("<I", 8 + len(new_body)) + new_body
    out = bytearray(b[:o] + sec + b[o + size:])
    struct.pack_into("<I", out, 8, len(out))
    return bytes(out)


# ------------------------------------------------------------------ NCER
def ncer_cells(b):
    o, _ = _sec(b, b"KBEC")
    B = o + 8
    n, attr, off = struct.unpack_from("<HHI", b, B)
    esz = 16 if attr == 1 else 8
    oam0 = B + off + n * esz
    cells = []
    for i in range(n):
        e = b[B + off + i * esz:B + off + (i + 1) * esz]
        noam, _cattr, ooff = struct.unpack_from("<HHI", e, 0)
        oams = [list(struct.unpack_from("<HHH", b, oam0 + ooff + k * 6)) for k in range(noam)]
        cells.append((e, oams))
    return B, off, attr, cells


def ncer_build(orig, cells):
    B, off, attr, _ = ncer_cells(orig)
    head = bytearray(orig[B:B + off])
    struct.pack_into("<H", head, 0, len(cells))
    entries, oams = bytearray(), bytearray()
    for e, ol in cells:
        e = bytearray(e)
        struct.pack_into("<HI", e, 0, len(ol), 0)
        struct.pack_into("<H", e, 0, len(ol))
        struct.pack_into("<I", e, 4, len(oams))
        entries += e
        for a in ol:
            oams += struct.pack("<HHH", *a)
    body = bytes(head) + bytes(entries) + bytes(oams)
    while len(body) % 4:
        body += b"\0"
    return _replace_section(orig, b"KBEC", body)


# ------------------------------------------------------------------ NANR
ELEM_SIZE = {0: 2, 1: 16, 2: 8}


def nanr_seqs(b):
    o, _ = _sec(b, b"KNBA")
    B = o + 8
    ns, nf, so, fo, do = struct.unpack_from("<HHIII", b, B)
    seqs = []
    for i in range(ns):
        n, loop, at, pm, fof = struct.unpack_from("<HHIII", b, B + so + i * 16)
        et = at & 0xFFFF
        frames = []
        for k in range(n):
            doff, dur, _ = struct.unpack_from("<IHH", b, B + fo + fof + k * 8)
            elem = bytes(b[B + do + doff:B + do + doff + ELEM_SIZE[et]])
            frames.append((elem, dur))
        seqs.append(dict(loop=loop, at=at, pm=pm, frames=frames))
    return seqs


def nanr_build(orig, seqs):
    o, _ = _sec(orig, b"KNBA")
    B = o + 8
    head = bytearray(orig[B:B + 0x18])
    seq_tab, frame_tab, data = bytearray(), bytearray(), bytearray()
    for s in seqs:
        seq_tab += struct.pack("<HHIII", len(s["frames"]), s["loop"], s["at"], s["pm"], len(frame_tab))
        for elem, dur in s["frames"]:
            frame_tab += struct.pack("<IHH", len(data), dur, 0xBEEF)
            data += elem
            while len(data) % 4:
                data += b"\0"
    so = 0x18
    fo = so + len(seq_tab)
    do = fo + len(frame_tab)
    struct.pack_into("<HHIII", head, 0, len(seqs), sum(len(s["frames"]) for s in seqs), so, fo, do)
    body = bytes(head) + bytes(seq_tab) + bytes(frame_tab) + bytes(data)
    return _replace_section(orig, b"KNBA", body)


# ------------------------------------------------------------------ NCGR / NCLR
def ncgr_append(orig, extra_tiles_data):
    o, size = _sec(orig, b"RAHC")
    hdr = bytearray(orig[o + 8:o + 32])
    data_size = struct.unpack_from("<I", hdr, 16)[0]
    data = orig[o + 32:o + 32 + data_size] + extra_tiles_data
    struct.pack_into("<I", hdr, 16, len(data))
    return _replace_section(orig, b"RAHC", bytes(hdr) + data)


def ncgr_data(b):
    o, _ = _sec(b, b"RAHC")
    size = struct.unpack_from("<I", b, o + 24)[0]
    return b[o + 32:o + 32 + size]


def nclr_set_bank(orig, bank, src, src_bank):
    out = bytearray(orig)
    _, _, po = gfx.nclr(orig)
    _, _, ps = gfx.nclr(src)
    out[po + bank * 32:po + bank * 32 + 32] = src[ps + src_bank * 32:ps + src_bank * 32 + 32]
    return bytes(out)


# ------------------------------------------------------------------ combinazione
def build(files):
    """files: lista dei membri (già decompressi) di a/2/6/2 → {indice: bytes nuovi (non compressi)}"""
    H = {k: files[v] for k, v in HOOH.items()}
    L = {k: files[v] for k, v in LUGIA.items()}
    ntiles_h = len(ncgr_data(H["chr"])) // 32
    new_chr = ncgr_append(H["chr"], ncgr_data(L["chr"]))
    new_pal = nclr_set_bank(H["pal"], 2, L["pal"], 1)
    _, _, _, hc = ncer_cells(H["cel"])
    _, _, _, lc = ncer_cells(L["cel"])
    base_l = len(hc) - 1                     # cella Lugia c (1..6) → indice base_l + c
    cells = list(hc)
    for e, oams in lc[1:]:
        moved = []
        for a0, a1, a2 in oams:
            tile, pal = a2 & 0x3FF, a2 >> 12
            assert pal == 1, "tavolozza inattesa nelle celle di Lugia"
            moved.append([a0, a1, (a2 & 0x0C00) | (2 << 12) | (tile + ntiles_h)])
        cells.append((e, moved))
    assert max(a[2] & 0x3FF for _, ol in cells for a in ol) < 1024
    new_cel = ncer_build(H["cel"], cells)
    hs, ls = nanr_seqs(H["anm"]), nanr_seqs(L["anm"])
    fly_h, fly_l = hs[1]["frames"], ls[1]["frames"]
    lugia = []
    for elem, dur in fly_l:
        e = bytearray(elem)
        struct.pack_into("<H", e, 0, struct.unpack_from("<H", e, 0)[0] + base_l)
        lugia.append((bytes(e), dur))
    out = fly_h[:HOOH_OUT]
    back = list(reversed(fly_h[:HOOH_OUT:HOOH_BACK_STEP]))
    seq1 = dict(hs[1], frames=out + back + lugia)
    new_anm = nanr_build(H["anm"], [hs[0], seq1, hs[2]])
    return {HOOH["chr"]: new_chr, HOOH["pal"]: new_pal, HOOH["cel"]: new_cel, HOOH["anm"]: new_anm}


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    from ndsfs import parse_narc
    root = Path(__file__).resolve().parent.parent
    raw = parse_narc((root / "work/IPKI/files" / NARC).read_bytes())
    files = [gfx.maybe_lz(f)[0] for f in raw]
    new = build(files)
    # verifica: rilettura
    _, _, _, cells = ncer_cells(new[HOOH["cel"]])
    seqs = nanr_seqs(new[HOOH["anm"]])
    print("celle:", len(cells), "tile:", len(ncgr_data(new[HOOH["chr"]])) // 32,
          "sequenze:", [len(s["frames"]) for s in seqs], "durata volo:", sum(d for _, d in seqs[1]["frames"]))
    # anteprima delle celle (senza scala), 64x64 ciascuna
    bpp, tiles, _, _ = gfx.ncgr(new[HOOH["chr"]])
    _, cols, _ = gfx.nclr(new[HOOH["pal"]])
    W = 64 * len(cells)
    rgba = bytearray(W * 64 * 4)
    shapes = {(0, 0): (8, 8), (0, 1): (16, 16), (0, 2): (32, 32), (0, 3): (64, 64), (1, 0): (16, 8), (1, 1): (32, 8),
              (1, 2): (32, 16), (1, 3): (64, 32), (2, 0): (8, 16), (2, 1): (8, 32), (2, 2): (16, 32), (2, 3): (32, 64)}
    for ci, (_, oams) in enumerate(cells):
        for a0, a1, a2 in reversed(oams):
            y = a0 & 0xFF; y = y - 256 if y > 127 else y
            x = a1 & 0x1FF; x = x - 512 if x > 255 else x
            w, h = shapes[(a0 >> 14, a1 >> 14)]
            hf, vf = (a1 >> 12) & 1, (a1 >> 13) & 1
            if a0 & 0x100:   # affine: niente flip
                hf = vf = 0
            t0, pal = a2 & 0x3FF, a2 >> 12
            for ty in range(h // 8):
                for tx in range(w // 8):
                    t = t0 + ty * (w // 8) + tx
                    if t >= len(tiles):
                        continue
                    for py in range(8):
                        for px in range(8):
                            v = tiles[t][py * 8 + px]
                            if not v:
                                continue
                            X = tx * 8 + px; Y = ty * 8 + py
                            if hf: X = w - 1 - X
                            if vf: Y = h - 1 - Y
                            gx, gy = ci * 64 + 32 + x + X, 32 + y + Y
                            if 0 <= gx < W and 0 <= gy < 64 and ci * 64 <= gx < ci * 64 + 64:
                                o = (gy * W + gx) * 4
                                rgba[o:o + 4] = bytes((*cols[pal * 16 + v], 255))
    gfx.write_png(root / "work/intro_celle.png", W, 64, bytes(rgba))
    print("anteprima: work/intro_celle.png")


if __name__ == "__main__":
    main()
