"""Fase 2 — dove si ottengono gli oggetti che contano per il progetto (sola lettura).

Oggetti evolutivi delle 251 (pietre, Roccia di Re, Metallopatina, Squama Drago, Upgrade), fossili,
Aromi (da togliere, D9) e strumenti che servono solo a evoluzioni verso gen 4 (da togliere o lasciare innocui).

Fonti lette:
  - strumenti a terra: eventi di zona (ROM a/0/3/2) con script 7000+N → voce N di scr_seq_0141 (quale oggetto)
  - oggetti nascosti: eventi di zona con script 8000+N → tabella sHiddenItemParam (codice ARM9)
  - negozio del Pokéathlon (per giorno della settimana, prima/dopo il Pokédex Nazionale), negozi speciali
  - Spaccaroccia: tabelle nel codice (overlay 1) + tipo per mappa (ROM a/2/5/3)
  - script: SetVar VAR_SPECIAL_x8004 <oggetto> seguito dalla quantità (regali, premi, scambi con PL)
  - strumenti tenuti dai Pokémon selvatici (personal)
Le tabelle che stanno nel codice (decomp pret) vengono cercate byte per byte nell'ARM9/overlay della ROM ITA:
se non si trovano, il report lo segnala.

Prerequisiti: python tools/roundtrip.py; python tools/get_pret.py
Uso:          python tools/items.py [--out docs/oggetti.md]
"""
import argparse
import collections
import json
import re
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ndsfs import parse_narc, u16  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
IPKI = ROOT / "work" / "IPKI"
ROM = IPKI / "files"
PRET = ROOT / "work" / "pret"
SCR = PRET / "files/fielddata/script/scr_seq"

ITEMS = {}
for m in re.finditer(r"#define (ITEM_\w+)\s+(\d+)", (PRET / "include/constants/items.h").read_text()):
    ITEMS.setdefault(int(m.group(2)), m.group(1))
ITEM_ID = {v: k for k, v in ITEMS.items()}

# oggetto → (categoria, a cosa serve)
WATCH = {
    "ITEM_FIRE_STONE": ("evoluzione 251", "Vulpix, Growlithe, Eevee"),
    "ITEM_WATER_STONE": ("evoluzione 251", "Poliwhirl, Shellder, Staryu, Eevee"),
    "ITEM_THUNDERSTONE": ("evoluzione 251", "Pikachu, Eevee"),
    "ITEM_LEAF_STONE": ("evoluzione 251", "Gloom, Weepinbell, Exeggcute"),
    "ITEM_MOON_STONE": ("evoluzione 251", "Nidorina, Nidorino, Clefairy, Jigglypuff"),
    "ITEM_SUN_STONE": ("evoluzione 251", "Gloom (Bellossom), Sunkern"),
    "ITEM_KINGS_ROCK": ("evoluzione 251", "Poliwhirl (Politoed), Slowpoke (Slowking) — D7"),
    "ITEM_METAL_COAT": ("evoluzione 251", "Onix, Scyther — D7"),
    "ITEM_DRAGON_SCALE": ("evoluzione 251", "Seadra — D7"),
    "ITEM_UPGRADE": ("evoluzione 251", "Porygon — D7"),
    "ITEM_HELIX_FOSSIL": ("fossile", "Omanyte"),
    "ITEM_DOME_FOSSIL": ("fossile", "Kabuto"),
    "ITEM_OLD_AMBER": ("fossile", "Aerodactyl"),
    "ITEM_ROOT_FOSSIL": ("fossile gen 3-4", "Lileep — da togliere"),
    "ITEM_CLAW_FOSSIL": ("fossile gen 3-4", "Anorith — da togliere"),
    "ITEM_ARMOR_FOSSIL": ("fossile gen 3-4", "Shieldon — da togliere"),
    "ITEM_SKULL_FOSSIL": ("fossile gen 3-4", "Cranidos — da togliere"),
    "ITEM_SEA_INCENSE": ("aroma (D9)", "Marill → Azurill"),
    "ITEM_LAX_INCENSE": ("aroma (D9)", "Snorlax → Munchlax"),
    "ITEM_ROSE_INCENSE": ("aroma (D9)", "Roselia → Budew (gen 3-4, innocuo)"),
    "ITEM_PURE_INCENSE": ("aroma (D9)", "Chimecho → Chingling (gen 3-4, innocuo)"),
    "ITEM_ROCK_INCENSE": ("aroma (D9)", "Sudowoodo → Bonsly"),
    "ITEM_ODD_INCENSE": ("aroma (D9)", "Mr. Mime → Mime Jr."),
    "ITEM_LUCK_INCENSE": ("aroma (D9)", "Chansey → Happiny"),
    "ITEM_WAVE_INCENSE": ("aroma (D9)", "Mantine → Mantyke"),
    "ITEM_FULL_INCENSE": ("aroma (D9)", "Snorlax → Munchlax"),
    "ITEM_SHINY_STONE": ("solo gen 4", "Togetic → Togekiss (D8)"),
    "ITEM_DUSK_STONE": ("solo gen 4", "Murkrow, Misdreavus (D8)"),
    "ITEM_DAWN_STONE": ("solo gen 4", "Kirlia/Snorunt (gen 3)"),
    "ITEM_OVAL_STONE": ("solo gen 4", "Happiny"),
    "ITEM_PROTECTOR": ("solo gen 4", "Rhydon (D8)"),
    "ITEM_ELECTIRIZER": ("solo gen 4", "Electabuzz (D8)"),
    "ITEM_MAGMARIZER": ("solo gen 4", "Magmar (D8)"),
    "ITEM_DUBIOUS_DISC": ("solo gen 4", "Porygon2 (D8)"),
    "ITEM_RAZOR_CLAW": ("solo gen 4", "Sneasel (D8)"),
    "ITEM_RAZOR_FANG": ("solo gen 4", "Gligar (D8)"),
    "ITEM_REAPER_CLOTH": ("solo gen 4", "Dusclops"),
    "ITEM_DEEPSEATOOTH": ("solo gen 3", "Clamperl"),
    "ITEM_DEEPSEASCALE": ("solo gen 3", "Clamperl"),
}
WATCH_IDS = {ITEM_ID[k] for k in WATCH}
DAYS = ["domenica", "lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato"]


def name(i):
    return ITEMS.get(i, f"#{i}")


# ---------------------------------------------------------------- codice ROM (ARM9 + overlay)
CODE = {p.name: p.read_bytes() for p in [IPKI / "arm9/arm9.bin", *sorted((IPKI / "arm9_overlays").glob("*.bin"))]}


def find_code(blob):
    """Dove compare `blob` nel codice della ROM ITA ('' se assente)."""
    for n, d in CODE.items():
        i = d.find(blob)
        if i >= 0:
            return f"{n}+0x{i:X}"
    return ""


def pack16(values):
    return b"".join(struct.pack("<H", v) for v in values)


def c_item(tok):
    tok = tok.strip()
    return int(tok) if tok.isdigit() else ITEM_ID[tok]


# ---------------------------------------------------------------- mappe
MAP_BY_CODE, MAP_BY_ID = {}, {}
for m in re.finditer(r"#define (MAP_\w+)\s+(\d+)\s*// MAP_(\w+)", (PRET / "include/constants/maps.h").read_text()):
    MAP_BY_CODE[m.group(3)] = m.group(1)
    MAP_BY_ID[int(m.group(2))] = m.group(3)


def mapname(code):
    full = MAP_BY_CODE.get(code, "")
    return f"{code} ({full[4:].replace('_', ' ').title()})" if full else code


STD = {m.group(1): int(m.group(2)) for m in re.finditer(r"#define (std_\w+)\s+(\d+)", (PRET / "include/constants/std_script.h").read_text())}


# ---------------------------------------------------------------- sorgenti
def item_balls():
    """{indice N: oggetto} dalle voci di scr_seq_0141 (script 7000+N)."""
    text = (SCR / "scr_seq_0141.s").read_text()
    out = {}
    for m in re.finditer(r"scr_seq_0141_(\d+):\s*\n\s*SetVar VAR_SPECIAL_x8008, (\w+)\s*\n\s*SetVar VAR_SPECIAL_x8009, (\d+)", text):
        out[int(m.group(1))] = (c_item(m.group(2)), int(m.group(3)))
    return out


def hidden_table(checks):
    """{indice: (oggetto, quantità)} da sHiddenItemParam; verifica la tabella nel codice ROM."""
    text = (PRET / "src/data/fieldmap/hidden_items.h").read_text()
    rows = [(c_item(a), int(b), int(c), int(d), int(e))
            for a, b, c, d, e in re.findall(r"\{\s*(\w+),\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+)\s*\}", text)]
    blob = b"".join(struct.pack("<HBBHH", *r) for r in rows)
    where = find_code(blob)
    checks.append(("Tabella oggetti nascosti (sHiddenItemParam)", bool(where), f"{len(rows)} voci, {where or 'non trovata'}"))
    return {r[4]: (r[0], r[1]) for r in rows}


def zone_events(checks):
    """[(codice mappa, 'a terra'|'nascosto', script)] dalla ROM, confrontati con i JSON della decomp."""
    files = parse_narc((ROM / "a/0/3/2").read_bytes())
    jsons = sorted((PRET / "files/fielddata/eventdata/zone_event").glob("*.json"))
    out, agree, total = [], 0, 0
    for idx, d in enumerate(files):
        code = jsons[idx].stem.split("_", 1)[1] if idx < len(jsons) else f"#{idx}"
        nb = struct.unpack_from("<I", d, 0)[0]
        bgs = [u16(d, 4 + k * 20) for k in range(nb)]
        o = 4 + nb * 20
        no = struct.unpack_from("<I", d, o)[0]
        objs = [u16(d, o + 4 + k * 32 + 10) for k in range(no)]
        rom_ids = sorted(s for s in bgs + objs if 7000 <= s < 9000)
        if idx < len(jsons):
            js = json.loads(jsons[idx].read_text())
            dec = sorted(STD[e["scriptId"]] for e in js.get("bgs", []) + js.get("objects", [])
                         if STD.get(e["scriptId"], 0) >= 7000 and STD[e["scriptId"]] < 9000)
            total += 1
            agree += dec == rom_ids
        for s in objs:
            if 7000 <= s < 8000:
                out.append((code, "a terra", s))
        for s in bgs:
            if 8000 <= s < 9000:
                out.append((code, "nascosto", s))
    checks.append(("Eventi di zona: oggetti a terra/nascosti decomp = ROM", agree == total, f"{agree}/{total} mappe"))
    return out


def marts(checks):
    """[(negozio, condizione, oggetto)] dal negozio del Pokéathlon e dai negozi speciali."""
    text = (PRET / "src/scrcmd_mart.c").read_text()
    out = []
    tabs = {n: [(c_item(a), int(b)) for a, b in re.findall(r"\{\s*(\w+),\s*(\d+)\s*\}", body) if a != "0xFFFF"]
            for n, body in re.findall(r"const struct MartItem (_\w+)\[\] = \{(.*?)\};", text, re.S)}
    order = re.findall(r"_\w+", re.search(r"_0210FA04\[\] = \{(.*?)\};", text, re.S).group(1))
    found = 0
    for i, n in enumerate(order):
        found += bool(find_code(b"".join(struct.pack("<HH", *x) for x in tabs[n]) + b"\xff\xff"))
        for it, price in tabs[n]:
            out.append(("Pokéathlon (punti atleta)", f"{DAYS[i % 7]}, {'dopo' if i >= 7 else 'prima del'} Pokédex Nazionale", it, price))
    checks.append(("Negozio Pokéathlon per giorno: decomp = ROM", found == len(order), f"{found}/{len(order)} tabelle"))
    for n, body in re.findall(r"const u16 (_\w+)\[\] = \{(.*?)\};", text, re.S):
        its = [ITEM_ID[t] for t in re.findall(r"ITEM_\w+", body)]
        for it in its:
            out.append(("negozio speciale " + n, "", it, None))
    return out


def rock_smash(checks):
    """[(tabella, [(oggetto, probabilità %)], [mappe con probabilità di trovare oggetti])]"""
    text = (PRET / "src/field/rock_smash_item.c").read_text()
    hg = re.sub(r"#else.*?#endif[^\n]*", "", text, flags=re.S)  # tiene i rami HEARTGOLD
    probs = [25, 20, 10, 10, 10, 10, 10, 5]
    tables = {}
    for n, body in re.findall(r"static const u16 sRockSmashItems_(\w+)\[\] = \{(.*?)\};", hg, re.S):
        its = [ITEM_ID[t] for t in re.findall(r"ITEM_\w+", body)]
        tables[n] = its
    ok = all(find_code(pack16(v)) for v in tables.values())
    checks.append(("Tabelle oggetti Spaccaroccia (HG): decomp = ROM", ok, ", ".join(tables)))
    per_map = collections.defaultdict(list)
    for mid, d in enumerate(parse_narc((ROM / "a/2/5/3").read_bytes())):
        odds, typ = struct.unpack_from("<HH", d, 0)
        if odds:
            per_map[["Default", "RuinsOfAlph", "CliffCave"][typ]].append(f"{mapname(MAP_BY_ID.get(mid, str(mid)))} {odds}%")
    return [(n, list(zip(its, probs)), per_map.get(n, [])) for n, its in tables.items()]


def script_gifts():
    """[(file, riga, oggetto)]: GoToIfNoItemSpace/GiveItemNoCheck <oggetto>, oppure
    SetVar VAR_SPECIAL_x8004 <oggetto> seguito dalla quantità o da un give_item."""
    out = []
    for p in sorted(SCR.glob("*.s")):
        if p.name == "scr_seq_0141.s":
            continue
        lines = p.read_text(errors="replace").splitlines()
        for k, ln in enumerate(lines):
            m = re.match(r"\s*(?:GoToIfNoItemSpace|GiveItemNoCheck) (ITEM_\w+)", ln)
            if m and ITEM_ID.get(m.group(1)) in WATCH_IDS:
                out.append((p.stem.replace("scr_seq_", ""), k + 1, ITEM_ID[m.group(1)]))
                continue
            m = re.match(r"\s*SetVar VAR_SPECIAL_x8004, (\w+)\s*$", ln)
            if not m:
                continue
            v = m.group(1)
            it = ITEM_ID.get(v) if v.startswith("ITEM_") else int(v) if v.isdigit() else None
            if it not in WATCH_IDS:
                continue
            nxt = " ".join(lines[k + 1:k + 4])
            if v.startswith("ITEM_") or "VAR_SPECIAL_x8005" in nxt or re.search(r"std_(give|obtain)_item", nxt):
                out.append((p.stem.replace("scr_seq_", ""), k + 1, it))
    return out


def held_items():
    """{oggetto: [specie <= 251 che lo tengono]} da personal (strumento 50%/5%)."""
    species = {}
    for m in re.finditer(r"#define SPECIES_(\w+)\s+(\d+)", (PRET / "include/constants/species.h").read_text()):
        species.setdefault(int(m.group(2)), m.group(1).title())
    out = collections.defaultdict(list)
    for i, f in enumerate(parse_narc((ROM / "a/0/0/2").read_bytes())):
        if 1 <= i <= 251 and len(f) >= 0x10:
            for slot, pct in ((0x0C, "50%"), (0x0E, "5%")):
                it = u16(f, slot)
                if it in WATCH_IDS:
                    out[it].append(f"{species.get(i, i)} ({pct})")
    return out


# ---------------------------------------------------------------- report
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "docs" / "oggetti.md"))
    args = ap.parse_args()
    for need, hint in [(ROM, "python tools/roundtrip.py"), (PRET / "src/field", "python tools/get_pret.py")]:
        if not need.exists():
            sys.exit(f"Manca {need}: eseguire prima `{hint}`")

    checks = []
    balls = item_balls()
    hidden = hidden_table(checks)
    events = zone_events(checks)
    shop = marts(checks)
    smash = rock_smash(checks)
    gifts = script_gifts()
    held = held_items()

    src = collections.defaultdict(list)  # oggetto → [(tipo, dettaglio)]
    for code, kind, s in events:
        it, qty = balls.get(s - 7000, (None, 0)) if kind == "a terra" else hidden.get(s - 8000, (None, 0))
        if it in WATCH_IDS:
            src[it].append((kind, mapname(code) + (f" ×{qty}" if qty > 1 else "")))
    day_sets = collections.defaultdict(list)
    for shopname, cond, it, price in shop:
        if it in WATCH_IDS:
            if shopname.startswith("Pokéathlon"):
                day_sets[it].append(cond)
            else:
                src[it].append(("negozio", shopname))
    for it, conds in day_sets.items():
        pre = [c.split(",")[0] for c in conds if "prima" in c]
        post = [c.split(",")[0] for c in conds if "dopo" in c]
        txt = []
        if pre:
            txt.append("prima del Nazionale: " + ", ".join(pre))
        if post:
            txt.append("dopo il Nazionale: " + ", ".join(post))
        src[it].append(("negozio Pokéathlon", "; ".join(txt)))
    for n, its, maps in smash:
        tot = collections.Counter()
        for it, pct in its:
            tot[it] += pct
        for it, pct in tot.items():
            if it in WATCH_IDS:
                src[it].append(("Spaccaroccia", f"tabella {n} ({pct}% per roccia con oggetto) — mappe: " + (", ".join(maps) or "nessuna")))
    for f, line, it in gifts:
        src[it].append(("script", f"{f}:{line}"))
    for it, sps in held.items():
        src[it].append(("tenuto da selvatici", ", ".join(sps)))

    L = ["# Fonti degli oggetti rilevanti — HeartGold ITA (IPKI)", "",
         "Generato da `python tools/items.py`. Oggetti a terra/nascosti e tipo Spaccaroccia letti dalla ROM ITA; "
         "script e tabelle del codice dalla decomp pret, cercate byte per byte nella ROM ITA (controlli sotto). "
         "Solo nomi e ID.", "",
         "## Controlli di coerenza ROM ↔ decomp", "", "| Controllo | Esito | Dettaglio |", "|---|---|---|"]
    L += [f"| {c} | {'OK' if ok else '**NO**'} | {d} |" for c, ok, d in checks]
    L += ["", "## Riepilogo per oggetto", "",
          "Le righe `script` sono punti in cui uno script prepara l'oggetto per darlo (regalo, premio, scambio con PL): "
          "il file indica la mappa. `tenuto da selvatici` = ottenibile con Furto/Covo o catturando.", "",
          "| Oggetto | Categoria | Serve per | Fonti |", "|---|---|---|---|"]
    for k, (cat, use) in WATCH.items():
        it = ITEM_ID[k]
        s = src.get(it, [])
        fonti = "<br>".join(f"**{t}**: {d}" for t, d in s) or "**nessuna trovata**"
        L.append(f"| {k[5:]} | {cat} | {use} | {fonti} |")

    L += ["", "## Spaccaroccia: tabelle complete (HeartGold)", ""]
    for n, its, maps in smash:
        L.append(f"- **{n}**: " + ", ".join(f"{name(i)[5:]} {p}%" for i, p in its) + f". Mappe: {', '.join(maps) or '-'}.")
    L.append("")

    out = Path(args.out)
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"Report: {out.relative_to(ROOT)}")
    for c, ok, d in checks:
        print(f"[{'OK' if ok else 'NO'}] {c}: {d}")
    missing = [k[5:] for k, (cat, _) in WATCH.items() if cat == "evoluzione 251" or cat == "fossile"
               if not src.get(ITEM_ID[k])]
    print("Oggetti necessari senza fonte:", ", ".join(missing) or "nessuno")


if __name__ == "__main__":
    main()
