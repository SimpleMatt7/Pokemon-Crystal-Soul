"""Fase 3 — prima bozza della tabella di sostituzione specie > #251 → specie #001-#251.

Per ogni specie di gen 3-4 cerca la specie di gen 1-2 più simile: tipi, stadio evolutivo, se è forma finale,
statistiche totali (BST); penalizza i sostituti già usati molte volte per non avere 30 volte lo stesso Pokémon.
I leggendari/misteriosi di gen 3-4 si sostituiscono solo con leggendari di gen 1-2.

La bozza va poi rivista a mano: le correzioni si scrivono nella colonna `sostituto` di data/design/sostituzioni.csv.
Se il file esiste già, le righe con `rivisto` = sì non vengono toccate.

Uso: python tools/design_subs.py
"""
import collections
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ndsfs import parse_narc  # noqa: E402
import audit  # noqa: E402  (evoluzioni, nomi)

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "design" / "sostituzioni.csv"
TYPES = ["Normale", "Lotta", "Volante", "Veleno", "Terra", "Roccia", "Coleottero", "Spettro", "Acciaio", "???",
         "Fuoco", "Acqua", "Erba", "Elettro", "Psico", "Ghiaccio", "Drago", "Buio"]
LEGEND_OLD = {144, 145, 146, 150, 151, 243, 244, 245, 249, 250, 251}
LEGEND_NEW = set(range(377, 387)) | {480, 481, 482, 483, 484, 485, 486, 487, 488, 489, 490, 491, 492, 493}


def personal():
    out = {}
    for i, f in enumerate(parse_narc((audit.ROM / "a/0/0/2").read_bytes())):
        if 1 <= i <= 493:
            out[i] = {"bst": sum(f[0:6]), "types": (f[6], f[7])}
    return out


def stages(evo):
    pre = {}
    for s, lst in evo.items():
        for m, prm, t in lst:
            if 1 <= t <= 493:
                pre.setdefault(t, s)
    def depth(s):
        d = 0
        while s in pre:
            s = pre[s]; d += 1
        return d
    final = {s: not any(1 <= t <= 493 for _, _, t in evo.get(s, [])) for s in range(1, 494)}
    # le evoluzioni verso gen 4 verranno tolte (D8): per le 251 conta la catena senza di esse
    final_251 = {s: not any(1 <= t <= 251 for _, _, t in evo.get(s, [])) for s in range(1, 252)}
    return {s: depth(s) for s in range(1, 494)}, final, final_251


def tname(tt):
    a, b = tt
    return TYPES[a] if a == b else f"{TYPES[a]}/{TYPES[b]}"


def main():
    evo = audit.read_evolutions()
    per = personal()
    depth, final, final_251 = stages(evo)

    reviewed = {}
    if OUT.exists():
        with open(OUT, newline="", encoding="utf-8") as f:
            for r in csv.DictReader(line for line in f if not line.startswith("#")):
                if r.get("rivisto", "").strip().lower() in ("sì", "si", "x", "1"):
                    reviewed[int(r["id"])] = r

    used = collections.Counter()
    for r in reviewed.values():
        used[int(r["sostituto_id"])] += 1
    rows = []
    for x in range(252, 494):
        if x in reviewed:
            r = dict(reviewed[x])
            y = int(r["sostituto_id"])
            r.update(specie=audit.sp(x), tipo=tname(per[x]["types"]), stadio=depth[x], bst=per[x]["bst"],
                     sostituto=audit.sp(y), tipo_sost=tname(per[y]["types"]), stadio_sost=depth[y], bst_sost=per[y]["bst"])
            rows.append(r); continue
        px = per[x]
        tx = set(px["types"])
        cands = LEGEND_OLD if x in LEGEND_NEW else set(range(1, 252)) - LEGEND_OLD
        best = None
        for y in cands:
            py = per[y]
            ty = set(py["types"])
            score = 0.0
            score += 4 if px["types"][0] == py["types"][0] else 0
            score += 2 * len(tx & ty)
            score -= 2 * len(ty - tx)
            score += 2 if min(depth[x], 2) == min(depth[y], 2) else 0
            score += 2 if final[x] == final_251[y] else 0
            score -= abs(px["bst"] - py["bst"]) / 25
            score -= 1.5 * used[y]
            if best is None or score > best[0]:
                best = (score, y)
        y = best[1]
        used[y] += 1
        rows.append({"id": x, "specie": audit.sp(x), "tipo": tname(px["types"]), "stadio": depth[x], "bst": px["bst"],
                     "sostituto_id": y, "sostituto": audit.sp(y), "tipo_sost": tname(per[y]["types"]),
                     "stadio_sost": depth[y], "bst_sost": per[y]["bst"], "rivisto": "", "nota": ""})

    OUT.parent.mkdir(parents=True, exist_ok=True)
    cols = ["id", "specie", "tipo", "stadio", "bst", "sostituto_id", "sostituto", "tipo_sost", "stadio_sost",
            "bst_sost", "rivisto", "nota"]
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        f.write("# Sostituzione globale specie > #251 → #001-#251 (allenatori, Parco Lotta, Pokéathlon, radio, Bottintesta,\n"
                "# Safari, Gara). Bozza da tools/design_subs.py; correzioni a mano in sostituto_id + rivisto=sì.\n"
                "# Le fonti con una scelta dedicata (selvatici.csv, eventi.csv) hanno la precedenza.\n")
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in cols})
    print(f"{OUT.relative_to(ROOT)}: {len(rows)} righe ({len(reviewed)} già riviste)")
    print("Sostituti più usati:", ", ".join(f"{audit.sp(y)}×{n}" for y, n in used.most_common(12)))


if __name__ == "__main__":
    main()
