"""Fase 3 — genera data/design/selvatici.csv: modifiche puntuali agli incontri selvatici di HeartGold (a/0/3/7).

Tre gruppi di righe, ognuna con offset di byte nella tabella della mappa (u16 specie):
  - D16 esclusive SoulSilver: dove la tabella SS (a/1/3/6) ha un'esclusiva SS e HG ha un'altra specie.
    Se la specie HG è comune (si trova anche altrove) lo slot passa del tutto alla specie SS; se è un'esclusiva HG
    o una specie rara, gli slot si dividono a metà (uno sì e uno no) così restano ottenibili entrambe.
    Gli sciami di mappe fuori da sSwarmMapLUT non si toccano (dato morto).
  - Radio Suono Hoenn/Sinnoh: le 4 specie radio diventano le specie degli slot erba 2 e 4 (giorno) della stessa
    mappa: la radio non cambia più gli incontri (scelta neutra).
  - D18 sciami gen 3-4: sostituiti con specie gen 1-2 rare in natura (SCIAMI qui sotto).

Uso: python tools/design_wild.py
"""
import collections
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ndsfs import parse_narc, u16  # noqa: E402
import audit  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "design" / "selvatici.csv"
SS_EXCL = {37, 38, 52, 53, 165, 166, 216, 217, 225, 227}
HG_EXCL = {56, 57, 58, 59, 167, 168, 207, 226, 231, 232}
KEEP_HALF = HG_EXCL | {83, 198}  # + Farfetch'd, Murkrow: poche mappe, non si tolgono del tutto

# (mappa, categoria) → specie: D18
SCIAMI = {
    ("D46R0101", "sciame erba"): "PIKACHU",      # Bosco Smeraldo
    ("R01", "sciame erba"): "EKANS",
    ("R03", "sciame erba"): "EEVEE",
    ("R09", "sciame erba"): "ELECTABUZZ",        # vicino alla Centrale
    ("R12", "sciame pesca"): "DRATINI",
    ("R25", "sciame erba"): "KANGASKHAN",
    ("R27", "sciame surf"): "LAPRAS",
    ("R34", "sciame erba"): "MR_MIME",
    ("R45", "sciame erba"): "LARVITAR",
    ("T06", "sciame surf"): "SEEL",              # Aranciopoli
    ("T22", "sciame pesca"): "HORSEA",           # Violapoli
    ("W19", "sciame surf"): "SHELLDER",
}
SWARM_OFF = {"sciame erba": 188, "sciame surf": 190, "sciame pesca": 194}


def slot_name(o):
    if 20 <= o < 92:
        k = (o - 20) // 2
        return f"erba {('mattino', 'giorno', 'notte')[k // 12]} slot {k % 12}"
    if 100 <= o < 120:
        return f"surf slot {(o - 102) // 4}"
    if 120 <= o < 128:
        return f"spaccaroccia slot {(o - 122) // 4}"
    if 128 <= o < 188:
        k = (o - 130) // 4
        return f"pesca {('amo vecchio', 'amo buono', 'super amo')[k // 5]} slot {k % 5}"
    return {92: "radio Hoenn 0", 94: "radio Hoenn 1", 96: "radio Sinnoh 0", 98: "radio Sinnoh 1",
            188: "sciame erba", 190: "sciame surf", 192: "pesca notturna", 194: "sciame pesca"}.get(o, str(o))


def main():
    names = [e["map"] for e in json.loads((audit.PRET / "files/fielddata/encountdata/gs_enc_data.json").read_text())["encounters"]]
    hg = parse_narc((audit.ROM / "a/0/3/7").read_bytes())
    ss = parse_narc((audit.ROM / "a/1/3/6").read_bytes())
    swarms = audit.read_swarm_maps([])
    normal = [o for cat, offs, n in audit.WILD_SLOTS if n for o in offs]
    rows = []

    # D16
    for i, (h, s) in enumerate(zip(hg, ss)):
        pairs = collections.defaultdict(list)
        for o in normal + [188, 190, 194]:
            a, b = u16(h, o) & 0x3FF, u16(s, o) & 0x3FF
            if b in SS_EXCL and a != b:
                if o in SWARM_OFF.values():
                    cat = {v: k for k, v in SWARM_OFF.items()}[o]
                    if (names[i], cat) not in swarms:
                        continue
                pairs[(a, b)].append(o)
        for (a, b), offs in pairs.items():
            half = a in KEEP_HALF
            for k, o in enumerate(offs):
                if half and k % 2 == 0:
                    continue
                rows.append((names[i], o, slot_name(o), audit.sp(a), audit.sp(b),
                             "D16 esclusiva SS" + (" (slot divisi con la specie HG)" if half else "")))

    # radio
    for i, h in enumerate(hg):
        day2, day4 = u16(h, 20 + (12 + 2) * 2) & 0x3FF, u16(h, 20 + (12 + 4) * 2) & 0x3FF
        for o, new in ((92, day2), (94, day4), (96, day2), (98, day4)):
            old = u16(h, o) & 0x3FF
            if old and old != new:
                rows.append((names[i], o, slot_name(o), audit.sp(old), audit.sp(new), "radio neutra (= erba giorno 2/4)"))

    # D18
    for (m, cat), new in SCIAMI.items():
        i = names.index(m)
        o = SWARM_OFF[cat]
        old = u16(hg[i], o) & 0x3FF
        assert old > 251, (m, cat, audit.sp(old))
        rows.append((m, o, slot_name(o), audit.sp(old), audit.sp(audit.SPECIES_BY_CONST["SPECIES_" + new]), "D18 sciame"))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        f.write("# Modifiche puntuali agli incontri HG (a/0/3/7). offset = byte nella tabella della mappa (u16 specie).\n"
                "# Generato da tools/design_wild.py; si può correggere a mano (lo script lo sovrascrive: modificare le regole lì).\n")
        w = csv.writer(f)
        w.writerow(["mappa", "offset", "slot", "da", "a", "motivo"])
        w.writerows(rows)
    c = collections.Counter(r[5].split(" (")[0] for r in rows)
    print(f"{OUT.relative_to(ROOT)}: {len(rows)} righe — " + ", ".join(f"{k}: {v}" for k, v in c.items()))


if __name__ == "__main__":
    main()
