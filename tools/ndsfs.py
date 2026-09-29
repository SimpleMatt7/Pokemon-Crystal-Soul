"""Lettura in memoria del file system NDS (FNT/FAT) e degli archivi NARC.

Solo lettura: la ricostruzione della ROM la fa `dsrom` (vedi NOTES.md).
"""
import struct


def u16(b, o):
    return struct.unpack_from("<H", b, o)[0]


def u32(b, o):
    return struct.unpack_from("<I", b, o)[0]


class NdsFs:
    def __init__(self, rom: bytes):
        self.rom = rom
        self.fnt = u32(rom, 0x40)
        self.fat = u32(rom, 0x48)

    def file_by_id(self, fid):
        s, e = u32(self.rom, self.fat + fid * 8), u32(self.rom, self.fat + fid * 8 + 4)
        return self.rom[s:e]

    def lookup(self, path):
        """Ritorna il contenuto del file al percorso dato, es. 'a/0/3/7'."""
        rom, fnt = self.rom, self.fnt
        d = 0xF000
        parts = path.strip("/").split("/")
        for i, part in enumerate(parts):
            base = fnt + (d & 0xFFF) * 8
            p = fnt + u32(rom, base)
            fid = u16(rom, base + 4)
            while True:
                t = rom[p]; p += 1
                if t == 0:
                    raise KeyError(path)
                ln = t & 0x7F
                name = rom[p:p + ln].decode("ascii"); p += ln
                if t & 0x80:
                    did = u16(rom, p); p += 2
                    if name == part:
                        d = did
                        break
                else:
                    if name == part and i == len(parts) - 1:
                        return self.file_by_id(fid)
                    fid += 1
        raise KeyError(path)

    def narc(self, path):
        return parse_narc(self.lookup(path))


def parse_narc(b):
    """Ritorna la lista dei sotto-file di un NARC."""
    if b[:4] != b"NARC":
        raise ValueError("non è un NARC")
    o = 16
    if b[o:o + 4] != b"BTAF":
        raise ValueError("BTAF mancante")
    size, n = u32(b, o + 4), u16(b, o + 8)
    entries = [(u32(b, o + 12 + i * 8), u32(b, o + 16 + i * 8)) for i in range(n)]
    o += size
    o += u32(b, o + 4)  # salta BTNF
    if b[o:o + 4] != b"GMIF":
        raise ValueError("GMIF mancante")
    g = o + 8
    return [b[g + s:g + e] for s, e in entries]
