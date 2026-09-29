"""Sonda in sola lettura: dove compaiono specie > #251 nella ROM base.

Copre (per ora): evoluzioni, incontri selvatici, squadre allenatori.
Da estendere nella fase 2 (Headbutt, Safari, Gara Bug, scambi, script, Parco Lotta).

Uso:  python tools/probe.py [CODICE_ROM]
"""
import collections
import csv
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ndsfs import NdsFs, u16  # noqa: E402
from roms import BASE, load_rom  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
with open(ROOT / "data" / "species.csv", newline="") as f:
    NAMES = {int(r["id"]): r["const"] for r in csv.DictReader(line for line in f if not line.startswith("#"))}


def name(i):
    return NAMES.get(i, str(i))


# Percorsi NARC per HeartGold (SoulSilver usa percorsi diversi per alcuni archivi: da verificare)
PATHS = {"evo": "a/0/3/4", "wild": "a/0/3/7", "trdata": "a/0/5/5", "trpoke": "a/0/5/6"}

# Layout file incontri HGSS (196 byte): offset delle specie per categoria
WILD_SLOTS = [
    ("erba", [20 + k * 2 for k in range(36)]),
    ("radio Hoenn", [92, 94]),
    ("radio Sinnoh", [96, 98]),
    ("surf", [100 + k * 4 + 2 for k in range(5)]),
    ("spaccaroccia", [120 + k * 4 + 2 for k in range(2)]),
    ("pesca", [128 + k * 4 + 2 for k in range(15)]),
    ("sciami", [188 + k * 2 for k in range(4)]),
]


def main():
    code = sys.argv[1] if len(sys.argv) > 1 else BASE
    fs = NdsFs(load_rom(code))
    print("ROM:", code)

    evo = fs.narc(PATHS["evo"])
    print("\n== Evoluzioni da specie 1-251 verso specie > 251")
    for sp in range(1, 252):
        f = evo[sp]
        for k in range(0, len(f) - 5, 6):
            method, param, target = struct.unpack_from("<HHH", f, k)
            if method and target > 251:
                print(f"  {name(sp)} -> {name(target)} (metodo {method}, param {param})")

    wild = fs.narc(PATHS["wild"])
    print(f"\n== Incontri selvatici: {len(wild)} tabelle")
    bycat = collections.defaultdict(collections.Counter)
    tables = set()
    for i, f in enumerate(wild):
        for cat, offs in WILD_SLOTS:
            for o in offs:
                s = u16(f, o) & 0x3FF
                if s > 251:
                    bycat[cat][s] += 1
                    tables.add(i)
    print(f"  tabelle con almeno una specie > 251: {len(tables)}")
    for cat, c in bycat.items():
        print(f"  {cat}: " + ", ".join(f"{name(s)}x{n}" for s, n in c.most_common()))

    trd, trp = fs.narc(PATHS["trdata"]), fs.narc(PATHS["trpoke"])
    total = bad = 0
    hits = collections.Counter()
    trainers = []
    for idx, (d, p) in enumerate(zip(trd, trp)):
        if len(d) < 4 or d[3] == 0:
            continue
        n = d[3]
        size = len(p) // n
        found = []
        for k in range(n):
            s = u16(p, k * size + 4) & 0x3FF
            total += 1
            if s > 251:
                bad += 1
                hits[s] += 1
                found.append(name(s))
        if found:
            trainers.append((idx, found))
    print(f"\n== Allenatori: {total} Pokémon in squadra, {bad} > 251, {len(trainers)} allenatori coinvolti")
    for idx, found in trainers:
        print(f"  #{idx}: {', '.join(found)}")


if __name__ == "__main__":
    main()
