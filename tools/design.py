"""Fase 3 — applica le tabelle di design (data/design/*.csv) ai dati in memoria e verifica gli obiettivi:
0 specie > #251 in tutte le fonti controllate dall'audit e 251/251 specie ottenibili in una partita.

Non scrive nessuna ROM (lo farà build.py in fase 4). Report: docs/design.md.

Ordine di applicazione: scelte dedicate (selvatici.csv, eventi.csv, evoluzioni.csv, oggetti.csv), poi
sostituzioni.csv per tutto ciò che resta > #251 (allenatori, Parco Lotta, Pokéathlon, Bottintesta, Safari, Gara, …).

Uso: python tools/design.py
"""
import collections
import csv
import re
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ndsfs import parse_narc, u16  # noqa: E402
import audit  # noqa: E402
import items as items_mod  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DESIGN = ROOT / "data" / "design"
sp = audit.sp


def rows(name):
    with open(DESIGN / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(line for line in f if not line.startswith("#")))


def spc(const):
    return audit.SPECIES_BY_CONST["SPECIES_" + const]


def main():
    subs = {int(r["id"]): int(r["sostituto_id"]) for r in rows("sostituzioni.csv")}
    assert set(subs) == set(range(252, 494)), "sostituzioni.csv incompleta"
    assert all(1 <= v <= 251 for v in subs.values())
    S = lambda s: subs.get(s, s)  # noqa: E731
    log = collections.Counter()

    # ------------------------------------------------ evoluzioni
    evo = audit.read_evolutions()
    for r in rows("evoluzioni.csv"):
        a, t = spc(r["da"]), spc(r["verso"])
        k = next(i for i, (m, p, tt) in enumerate(evo[a]) if tt == t)
        if r["metodo"] == "NONE":
            evo[a].pop(k)
        else:
            prm = audit.ITEM_BY_CONST[r["parametro"]] if r["parametro"].startswith("ITEM_") else int(r["parametro"])
            evo[a][k] = (r["metodo"], prm, t)
        log["evoluzioni"] += 1
    personal = audit.read_personal()

    # ------------------------------------------------ selvatici (byte) + sostituzioni residue
    import json
    names = [e["map"] for e in json.loads((audit.PRET / "files/fielddata/encountdata/gs_enc_data.json").read_text())["encounters"]]
    wild_files = [bytearray(f) for f in parse_narc((audit.ROM / "a/0/3/7").read_bytes())]
    for r in rows("selvatici.csv"):
        f = wild_files[names.index(r["mappa"])]
        o = int(r["offset"])
        cur = u16(f, o)
        assert sp(cur & 0x3FF) == r["da"], (r, sp(cur & 0x3FF))
        new = next(k for k, v in audit.SPECIES.items() if sp(k) == r["a"])
        struct.pack_into("<H", f, o, (cur & ~0x3FF) | new)
        log["selvatici (dedicate)"] += 1
    for f in wild_files:
        for cat, offs, n in audit.WILD_SLOTS:
            for o in offs:
                s = u16(f, o) & 0x3FF
                if s > 251:
                    struct.pack_into("<H", f, o, (u16(f, o) & ~0x3FF) | S(s)); log["selvatici (sostituzioni)"] += 1
    orig_narc = audit.narc
    audit.narc = lambda p: [bytes(f) for f in wild_files] if p == "a/0/3/7" else orig_narc(p)
    checks = []
    wild = audit.read_wild(checks)
    audit.narc = orig_narc

    def sub_list(label, lst, idx):
        out = []
        for t in lst:
            t = list(t)
            if t[idx] > 251:
                t[idx] = S(t[idx]); log[label] += 1
            out.append(tuple(t))
        return out

    headbutt = sub_list("bottintesta", audit.read_headbutt(), 2)
    safari = sub_list("safari", audit.read_safari(checks), 2)
    bug = sub_list("gara", audit.read_bug_contest(), 1)
    trainers = []
    for i, c, n, party in audit.read_trainers(checks):
        p2 = []
        for s, lv in party:
            if s > 251:
                s = S(s); log["allenatori"] += 1
            p2.append((s, lv))
        trainers.append((i, c, n, p2))
    # scambi: righe dedicate di eventi.csv ("a/1/1/2 #N Nome (chiede)" = specie chiesta, altrimenti data), poi sostituzioni
    trade_fix = {}
    for r in rows("eventi.csv"):
        m = re.match(r"a/1/1/2 #(\d+)", r["dove"]) if r["tipo"] == "scambio" else None
        if m:
            trade_fix[(int(m.group(1)), "(chiede)" in r["dove"])] = (spc(r["da"]), spc(r["a"]))
    trades = []
    for i, (n, ask, give) in enumerate(audit.read_trades()):
        for is_ask in (True, False):
            cur = ask if is_ask else give
            if (i, is_ask) in trade_fix:
                old_, new_ = trade_fix[(i, is_ask)]
                assert cur == old_, (n, sp(cur), sp(old_))
                cur = new_; log["scambi"] += 1
            elif cur > 251:
                cur = S(cur); log["scambi"] += 1
            if is_ask:
                ask = cur
            else:
                give = cur
        trades.append((n, ask, give))
    frontier = {}
    for a, (d, c) in audit.read_frontier().items():
        c2 = collections.Counter()
        for s, k in c.items():
            c2[S(s)] += k
            log["Parco Lotta"] += k if s > 251 else 0
        frontier[a] = (d, c2)
    pokeathlon = [S(u16(f, k)) for f in parse_narc((audit.ROM / "a/2/5/8").read_bytes()) for k in (0, 2, 4)]
    dex = {s: n for s, n in audit.read_johto_dex().items() if s <= 251}  # le 5 voci gen 4 si tolgono (rinumerare)

    # ------------------------------------------------ script ed eventi
    ev = rows("eventi.csv")
    scripts = []
    replaced = {}
    for r in ev:
        if r["tipo"] in ("regalo", "statico", "vagante") and r["da"]:
            for key in r["dove"].split(" (")[0].split(" + "):
                replaced[key.strip()] = (r["tipo"], [spc(x) for x in r["a"].split("|")] if r["a"] else [], r)
    event_only = {"D51R0201", "0092_D36R0101", "0750_T03"}
    for f, cmd, species, note in audit.read_scripts():
        key = f.split("_", 1)[1] if "_" in f else f
        if key in replaced and any(s > 251 or key in ("T01R0301", "T11R0701") for s in species):
            tipo, new, r = replaced[key]
            if cmd == "CreateRoamer":
                log["script"] += 1
                continue  # vagante tolto
            if "evento" in r["condizione"] or "irraggiungibile" in r["condizione"]:
                species = [S(s) for s in species] if not new else new
            else:
                species = new
            log["script"] += 1
        species = [S(s) for s in species]
        scripts.append((f, cmd, species, note))

    # ------------------------------------------------ fonti e ottenibilità
    src = collections.defaultdict(set)
    for m, cat, s, normal in wild:
        if cat != "sciame mai attivo":
            src[s].add("selvatico" if normal else cat + " (dopo il Nazionale)")
    for m, g, s in headbutt:
        src[s].add("bottintesta")
    for a, cat, s, bonus, _ in safari:
        src[s].add("safari (bonus oggetti)" if bonus else "safari")
    for t, s in bug:
        src[s].add("gara coleottero" if t == 0 else f"gara coleottero t{t} (dopo il Nazionale)")
    for n, ask, give in trades:
        src[give].add(f"scambio ({n})")
    for f, cmd, species, note in scripts:
        if any(f.endswith(e) for e in event_only) or "evento" in note:
            continue
        for s in species:
            src[s].add({"GiveMon": "regalo", "WildBattle": "statico", "GiveEgg": "uovo regalo",
                        "CreateRoamer": "vagante", "GiveTogepiEgg": "uovo regalo"}.get(cmd, cmd) + f" [{f}]")
    for r in ev:
        if r["tipo"] == "nuovo":
            for x in r["a"].split("|"):
                src[spc(x)].add(f"nuovo evento [{r['dove']}] ({r['condizione']})")
    # fossili dalle tabelle Spaccaroccia modificate
    smash = {n: [it for it, _ in its] for n, its, maps in items_mod.rock_smash([]) if maps}
    for r in rows("oggetti.csv"):
        if r["tipo"] == "spaccaroccia":
            n, k = r["dove"].split(":")
            assert smash[n][int(k)] == audit.ITEM_BY_CONST[r["da"]], r
            smash[n][int(k)] = audit.ITEM_BY_CONST[r["a"]]
    have = {it for v in smash.values() for it in v}
    for it, s in {"ITEM_HELIX_FOSSIL": 138, "ITEM_DOME_FOSSIL": 140, "ITEM_OLD_AMBER": 142}.items():
        if audit.ITEM_BY_CONST[it] in have:
            src[s].add(f"fossile {it[5:]} (Spaccaroccia) rianimato [T03R0101]")

    obtain, via = audit.closure({s for s in src if 1 <= s <= 493}, evo, personal)
    missing = [s for s in range(1, 252) if s not in obtain]

    # ------------------------------------------------ specie > 251 rimaste
    left = collections.Counter()
    left["selvatici"] = sum(1 for m, c, s, n in wild if s > 251)
    left["bottintesta"] = sum(1 for m, g, s in headbutt if s > 251)
    left["safari"] = sum(1 for x in safari if x[2] > 251)
    left["gara"] = sum(1 for t, s in bug if s > 251)
    left["allenatori"] = sum(1 for *_, p in trainers for s, _ in p if s > 251)
    left["scambi"] = sum(1 for n, a, g in trades if a > 251 or g > 251)
    left["script"] = sum(1 for f, c, sps, n in scripts for s in sps if s > 251)
    left["Parco Lotta"] = sum(k for d, c in frontier.values() for s, k in c.items() if s > 251)
    left["Pokéathlon (a/2/5/8)"] = sum(1 for s in pokeathlon if s > 251)
    # starter e leggendari non devono comparire negli incontri casuali
    special = set(range(1, 10)) | set(range(152, 161)) | {144, 145, 146, 150, 151, 243, 244, 245, 249, 250, 251}
    left["starter/leggendari negli incontri casuali"] = (
        sum(1 for m, c, s, n in wild if s in special and c != "sciame mai attivo")
        + sum(1 for m, g, s in headbutt if s in special) + sum(1 for x in safari if x[2] in special)
        + sum(1 for t, s in bug if s in special))
    left["evoluzioni verso > 251"] = sum(1 for s in range(1, 252) for m, p, t in evo[s] if t > 251)
    left["evoluzioni impossibili da solo"] = sum(1 for s in range(1, 252) for m, p, t in evo[s]
                                                 if t <= 251 and m in audit.EVO_IMPOSSIBLE_SOLO)

    # ------------------------------------------------ report
    L = ["# Verifica del design (fase 3)", "",
         "Generato da `python tools/design.py`: applica `data/design/*.csv` ai dati di IPKI in memoria. Nessuna ROM scritta.", "",
         "## Obiettivi", "",
         f"- Specie > #251 rimaste: **{sum(left.values())}**" + ("" if sum(left.values()) else " ✔"),
         f"- Ottenibili in una partita: **{251 - len(missing)}/251**" + (" ✔" if not missing else
                                                                       " — mancano " + ", ".join(sp(s) for s in missing)),
         "", "## Specie > #251 rimaste per fonte", "", "| Fonte | Voci |", "|---|---|"]
    L += [f"| {k} | {v} |" for k, v in left.items()]
    L += ["", "## Modifiche applicate (conteggio)", "", "| Gruppo | Voci |", "|---|---|"]
    L += [f"| {k} | {v} |" for k, v in log.items()]
    newly = [s for s in range(1, 252) if s in obtain]
    L += ["", "## Da dove arrivano le specie che mancavano", "", "| # | Specie | Fonti |", "|---|---|---|"]
    before = {1, 2, 3, 4, 5, 6, 7, 8, 9, 37, 38, 52, 53, 65, 68, 76, 94, 140, 141, 151, 152, 153, 154, 155, 156, 157,
              158, 159, 160, 165, 166, 186, 199, 208, 212, 216, 217, 225, 227, 230, 233, 251}
    for s in sorted(before & set(newly)):
        L.append(f"| {s:03} | {sp(s)} | " + "; ".join(sorted(src.get(s, set())) + sorted(via.get(s, set()))) + " |")
    L += ["", "## Da fare in fase 4 (build)", "",
          "- Allenatori: se il sostituto non è coerente con il livello (es. forma base a livello alto), evolverlo o "
          "farlo regredire secondo i livelli di evoluzione; se l'allenatore ha mosse personalizzate, ricalcolarle dal learnset.",
          "- Parco Lotta: sostituire anche le mosse dei set (le mosse dei set gen 3-4 potrebbero non essere imparabili).",
          "- Pokédex di Johto: togliere le 5 voci gen 4 e rinumerare (tabella a/1/3/8 + liste di ordinamento).",
          "- Oggetti D7 usabili come pietre (`uso_pietra` in oggetti.csv): campo uso sul campo nei dati oggetto.",
          "- Script: Oak e Rocco con tutte e 3 le Poké Ball; Mew alla Torre Inclusa; Celebi al santuario; vaganti Lati tolti.", ""]
    out = ROOT / "docs" / "design.md"
    out.write_text("\n".join(L), encoding="utf-8")
    print(f"Report: {out.relative_to(ROOT)}")
    print(f"Specie > 251 rimaste: {sum(left.values())} " + str({k: v for k, v in left.items() if v}))
    print(f"Ottenibili: {251 - len(missing)}/251" + (f"; mancano {', '.join(sp(s) for s in missing)}" if missing else ""))


if __name__ == "__main__":
    main()
