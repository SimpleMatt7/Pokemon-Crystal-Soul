"""Opzione O1: trova la tabella gNatureStatMods[25][5] (s8) nel codice estratto.

Uso:  python tools/find_nature_table.py [CODICE_ROM]   (richiede work/<CODICE>/ da roundtrip.py)
Stampa file e offset di ogni occorrenza, nel codice decompresso.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Da pret/pokeheartgold src/pokemon.c; colonne: ATK, DEF, SPEED, SPATK, SPDEF
ROWS = [
    (0, 0, 0, 0, 0), (1, -1, 0, 0, 0), (1, 0, -1, 0, 0), (1, 0, 0, -1, 0), (1, 0, 0, 0, -1),
    (-1, 1, 0, 0, 0), (0, 0, 0, 0, 0), (0, 1, -1, 0, 0), (0, 1, 0, -1, 0), (0, 1, 0, 0, -1),
    (-1, 0, 1, 0, 0), (0, -1, 1, 0, 0), (0, 0, 0, 0, 0), (0, 0, 1, -1, 0), (0, 0, 1, 0, -1),
    (-1, 0, 0, 1, 0), (0, -1, 0, 1, 0), (0, 0, -1, 1, 0), (0, 0, 0, 0, 0), (0, 0, 0, 1, -1),
    (-1, 0, 0, 0, 1), (0, -1, 0, 0, 1), (0, 0, -1, 0, 1), (0, 0, 0, -1, 1), (0, 0, 0, 0, 0),
]
PATTERN = bytes(v & 0xFF for row in ROWS for v in row)


def main():
    code = sys.argv[1] if len(sys.argv) > 1 else "IPKI"
    work = ROOT / "work" / code
    files = [work / "arm9" / "arm9.bin"] + sorted((work / "arm9_overlays").glob("*.bin"))
    hits = 0
    for f in files:
        data = f.read_bytes()
        i = data.find(PATTERN)
        while i != -1:
            print(f"{f.relative_to(work)}  offset 0x{i:X}")
            hits += 1
            i = data.find(PATTERN, i + 1)
    print(f"occorrenze: {hits}")


if __name__ == "__main__":
    main()
