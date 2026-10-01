"""Pokédex in un salvataggio di HeartGold/SoulSilver: mostra quante specie risultano viste/catturate, oppure le segna
come catturate (per provare i diplomi del Pokédex, D51, con la ROM di prova).

Formato (decomp pret: include/pokedex.h, src/save.c): due copie del salvataggio da 0x40000 byte; blocco generale da
0xF628 byte con piè di pagina (contatore, dimensione, magic 0x20060623, indice, CRC16-CCITT del blocco senza i 16 byte
del piè di pagina). Pokédex a 0x12B8 del blocco: magic 0xBEEFCAFE, 16 parole di bit "catturato", 16 di bit "visto"
(specie N = bit N-1), ordine delle forme di Unown visto/catturato a +0x10C/+0x128 (0xFF = vuoto).
Si modifica solo la copia più recente; prima viene salvata una copia del file (.bak).

Uso:  python tools/pokedex_sav.py mostra FILE.sav
      python tools/pokedex_sav.py segna FILE.sav [ULTIMA]     (segna viste e catturate le specie 1..ULTIMA, default 251)
"""
import shutil
import struct
import sys
from pathlib import Path

GENERAL_SIZE = 0xF628
FOOTER_MAGIC = 0x20060623
DEX = 0x12B8
DEX_MAGIC = 0xBEEFCAFE
UNOWN = 201


def crc16(data):
    crc = 0xFFFF
    for b in data:
        crc ^= b << 8
        for _ in range(8):
            crc = ((crc << 1) ^ 0x1021) & 0xFFFF if crc & 0x8000 else (crc << 1) & 0xFFFF
    return crc


def newest_copy(sav):
    best = None
    for off in (0, 0x40000):
        counter, size, magic = struct.unpack_from("<III", sav, off + GENERAL_SIZE - 0x10)
        crc = struct.unpack_from("<H", sav, off + GENERAL_SIZE - 2)[0]
        if size == GENERAL_SIZE and magic == FOOTER_MAGIC and crc16(sav[off:off + GENERAL_SIZE - 0x10]) == crc:
            if best is None or counter > best[1]:
                best = (off, counter)
    if best is None:
        sys.exit("Nessuna copia valida nel salvataggio (è di HeartGold/SoulSilver?)")
    return best


def counts(sav, off):
    p = off + DEX
    caught = struct.unpack_from("<16I", sav, p + 4)
    seen = struct.unpack_from("<16I", sav, p + 0x44)
    has = lambda words, n: (words[(n - 1) // 32] >> ((n - 1) % 32)) & 1  # noqa: E731
    return (sum(has(caught, n) for n in range(1, 494)), sum(has(seen, n) for n in range(1, 494)),
            sum(has(caught, n) for n in range(1, 252)))


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if len(sys.argv) < 3 or sys.argv[1] not in ("mostra", "segna"):
        sys.exit(__doc__)
    path = Path(sys.argv[2])
    sav = bytearray(path.read_bytes())
    off, counter = newest_copy(sav)
    if struct.unpack_from("<I", sav, off + DEX)[0] != DEX_MAGIC:
        sys.exit("Pokédex non trovato all'offset atteso (salvataggio di un altro gioco?)")
    c, s, c251 = counts(sav, off)
    print(f"Copia con contatore {counter}: catturate {c}, viste {s} (catturate tra le 251: {c251})")
    if sys.argv[1] == "mostra":
        return
    last = int(sys.argv[3]) if len(sys.argv) > 3 else 251
    p = off + DEX
    for base in (p + 4, p + 0x44):                       # catturate, viste
        words = list(struct.unpack_from("<16I", sav, base))
        for n in range(1, last + 1):
            words[(n - 1) // 32] |= 1 << ((n - 1) % 32)
        struct.pack_into("<16I", sav, base, *words)
    for order in (p + 0x10C, p + 0x128):                 # Unown: almeno la forma A registrata
        if last >= UNOWN and sav[order] == 0xFF:
            sav[order] = 0
    struct.pack_into("<H", sav, off + GENERAL_SIZE - 2, crc16(sav[off:off + GENERAL_SIZE - 0x10]))
    shutil.copyfile(path, path.with_suffix(path.suffix + ".bak"))
    path.write_bytes(bytes(sav))
    c, s, c251 = counts(sav, off)
    print(f"Fatto (copia di sicurezza: {path.name}.bak): catturate {c}, viste {s} (tra le 251: {c251})")


if __name__ == "__main__":
    main()
