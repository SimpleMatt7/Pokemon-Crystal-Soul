"""Patch BPS (formato di byuu/beat): creazione e applicazione, solo libreria standard.

La creazione cerca le parti uguali allo stesso offset (SourceRead) e, per i dati spostati, blocchi uguali
allineati a 512 byte (l'allineamento dei file nella ROM ricostruita da dsrom) (SourceCopy); il resto è TargetRead.

Uso:  python tools/bps.py crea ORIGINALE MODIFICATA PATCH.bps
      python tools/bps.py applica ORIGINALE PATCH.bps USCITA
"""
import struct
import sys
import zlib
from pathlib import Path

BLOCK = 512
KEY = 64


def _num(n):
    out = bytearray()
    while True:
        x = n & 0x7F
        n >>= 7
        if n == 0:
            out.append(0x80 | x)
            return bytes(out)
        out.append(x)
        n -= 1


def _read_num(b, o):
    data, shift = 0, 1
    while True:
        x = b[o]; o += 1
        data += (x & 0x7F) * shift
        if x & 0x80:
            return data, o
        shift <<= 7
        data += shift


def create(src: bytes, dst: bytes) -> bytes:
    index = {}
    for s in range(0, len(src) - KEY, BLOCK):
        index.setdefault(src[s:s + KEY], s)
    out = bytearray(b"BPS1" + _num(len(src)) + _num(len(dst)) + _num(0))
    src_rel = 0  # posizione relativa per SourceCopy
    lit_start = None
    t, n = 0, len(dst)

    def flush_lit(end):
        nonlocal lit_start
        if lit_start is not None and end > lit_start:
            out.extend(_num(((end - lit_start - 1) << 2) | 1))
            out.extend(dst[lit_start:end])
        lit_start = None

    while t < n:
        # 1) stessi byte allo stesso offset
        if t < len(src) and src[t] == dst[t]:
            e = t
            lim = min(n, len(src))
            while e < lim and src[e] == dst[e]:
                e += 1
            if e - t >= 8 or e == n:
                flush_lit(t)
                out.extend(_num(((e - t - 1) << 2) | 0))
                t = e
                continue
        # 2) blocco spostato
        if t % BLOCK == 0:
            s = index.get(dst[t:t + KEY])
            if s is not None and s != t:
                e = 0
                while t + e < n and s + e < len(src) and src[s + e] == dst[t + e]:
                    e += 1
                flush_lit(t)
                rel = s - src_rel
                out.extend(_num(((e - 1) << 2) | 2))
                out.extend(_num((abs(rel) << 1) | (rel < 0)))
                src_rel = s + e
                t += e
                continue
        if lit_start is None:
            lit_start = t
        t += 1
    flush_lit(n)
    out += struct.pack("<II", zlib.crc32(src), zlib.crc32(dst))
    out += struct.pack("<I", zlib.crc32(out))
    return bytes(out)


def apply(src: bytes, patch: bytes) -> bytes:
    assert patch[:4] == b"BPS1", "non è una patch BPS"
    assert zlib.crc32(patch[:-4]) == struct.unpack("<I", patch[-4:])[0], "CRC della patch errato"
    o = 4
    ssize, o = _read_num(patch, o)
    tsize, o = _read_num(patch, o)
    msize, o = _read_num(patch, o)
    o += msize
    assert len(src) == ssize and zlib.crc32(src) == struct.unpack("<I", patch[-12:-8])[0], "ROM di partenza sbagliata"
    out = bytearray()
    src_rel = tgt_rel = 0
    end = len(patch) - 12
    while o < end:
        d, o = _read_num(patch, o)
        cmd, ln = d & 3, (d >> 2) + 1
        if cmd == 0:
            out += src[len(out):len(out) + ln]
        elif cmd == 1:
            out += patch[o:o + ln]; o += ln
        else:
            v, o = _read_num(patch, o)
            rel = -(v >> 1) if v & 1 else v >> 1
            if cmd == 2:
                src_rel += rel
                out += src[src_rel:src_rel + ln]; src_rel += ln
            else:
                tgt_rel += rel
                for _ in range(ln):
                    out.append(out[tgt_rel]); tgt_rel += 1
    assert len(out) == tsize and zlib.crc32(out) == struct.unpack("<I", patch[-8:-4])[0], "risultato non valido"
    return bytes(out)


def main():
    if len(sys.argv) != 5 or sys.argv[1] not in ("crea", "applica"):
        sys.exit(__doc__)
    a, b, c = (Path(x) for x in sys.argv[2:])
    if sys.argv[1] == "crea":
        p = create(a.read_bytes(), b.read_bytes())
        c.write_bytes(p)
        print(f"{c}: {len(p)} byte")
    else:
        c.write_bytes(apply(a.read_bytes(), b.read_bytes()))
        print(f"{c}: scritto")


if __name__ == "__main__":
    main()
