"""Fase 2 — audit in sola lettura: dove compaiono specie > #251 e quali delle 251 sono ottenibili in una partita.

Prerequisiti:  python tools/roundtrip.py   (estrazione in work/IPKI)
               python tools/get_pret.py    (decomp in work/pret: nomi e script in chiaro)
Uso:           python tools/audit.py [--out docs/audit.md]

I valori binari sono letti da work/IPKI (ROM ITA). La decomp serve per i nomi (mappe, allenatori)
e per gli script: per ogni tabella il report controlla che la decomp concordi con i byte della ROM.
Il report contiene solo nomi/ID, nessun dato binario del gioco.
"""
import argparse
import collections
import csv
import json
import re
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ndsfs import parse_narc, u16  # noqa: E402
import items as items_mod  # noqa: E402  (fonti degli oggetti: Spaccaroccia per i fossili)

ROOT = Path(__file__).resolve().parent.parent
ROM = ROOT / "work" / "IPKI" / "files"
PRET = ROOT / "work" / "pret"

# ---------------------------------------------------------------- nomi e costanti
with open(ROOT / "data" / "species.csv", newline="") as f:
    SPECIES = {int(r["id"]): r["const"] for r in csv.DictReader(line for line in f if not line.startswith("#"))}
SPECIES_BY_CONST = {"SPECIES_" + v: k for k, v in SPECIES.items()}


def sp(i):
    return SPECIES.get(i, f"#{i}").title().replace("_", "-")


def gen(i):
    return 1 if i <= 151 else 2 if i <= 251 else 3 if i <= 386 else 4 if i <= 493 else 0


def load_defines(path, prefix):
    out = {}
    for m in re.finditer(rf"#define ({prefix}\w+)\s+(\d+)", path.read_text()):
        out[int(m.group(2))] = m.group(1)
    return out


ITEMS = load_defines(PRET / "include/constants/items.h", "ITEM_")
ITEM_BY_CONST = {v: k for k, v in ITEMS.items()}

EVO = ["NONE", "FRIENDSHIP", "FRIENDSHIP_DAY", "FRIENDSHIP_NIGHT", "LEVEL", "TRADE", "TRADE_ITEM", "STONE",
       "LEVEL_ATK_GT_DEF", "LEVEL_ATK_EQ_DEF", "LEVEL_ATK_LT_DEF", "LEVEL_PID_LO", "LEVEL_PID_HI",
       "LEVEL_NINJASK", "LEVEL_SHEDINJA", "BEAUTY", "STONE_MALE", "STONE_FEMALE", "ITEM_DAY", "ITEM_NIGHT",
       "HAS_MOVE", "OTHER_PARTY_MON", "LEVEL_MALE", "LEVEL_FEMALE", "CORONET", "ETERNA", "ROUTE217"]
EVO_IMPOSSIBLE_SOLO = {"TRADE", "TRADE_ITEM", "CORONET", "ETERNA", "ROUTE217"}
EVO_ITEM_PARAM = {"TRADE_ITEM", "STONE", "STONE_MALE", "STONE_FEMALE", "ITEM_DAY", "ITEM_NIGHT"}


def narc(path):
    return parse_narc((ROM / path).read_bytes())


class Report:
    def __init__(self):
        self.lines = []

    def h(self, level, text):
        self.lines += ["", "#" * level + " " + text, ""]

    def p(self, text=""):
        self.lines.append(text)

    def table(self, header, rows):
        self.lines.append("| " + " | ".join(header) + " |")
        self.lines.append("|" + "---|" * len(header))
        for r in rows:
            self.lines.append("| " + " | ".join(str(c) for c in r) + " |")
        self.lines.append("")


def fmt_counter(c):
    return ", ".join(f"{sp(s)}×{n}" if n > 1 else sp(s) for s, n in sorted(c.items(), key=lambda x: (-x[1], x[0])))


# ---------------------------------------------------------------- sorgenti
def read_evolutions():
    """{specie: [(metodo, param, target)]}"""
    out = {}
    for i, f in enumerate(narc("a/0/3/4")):
        lst = []
        for k in range(0, 42, 6):
            m, prm, t = struct.unpack_from("<HHH", f, k)
            if m:
                lst.append((EVO[m] if m < len(EVO) else str(m), prm, t))
        out[i] = lst
    return out


def read_personal():
    """{specie: (egg1, egg2, item1, item2)}"""
    out = {}
    for i, f in enumerate(narc("a/0/0/2")):
        if len(f) >= 0x16:
            out[i] = (f[0x14], f[0x15], u16(f, 0x0C), u16(f, 0x0E))
    return out


WILD_SLOTS = [
    ("erba", [20 + k * 2 for k in range(36)], True),
    ("radio Hoenn", [92, 94], False),
    ("radio Sinnoh", [96, 98], False),
    ("surf", [100 + k * 4 + 2 for k in range(5)], True),
    ("spaccaroccia", [120 + k * 4 + 2 for k in range(2)], True),
    ("pesca", [128 + k * 4 + 2 for k in range(15)], True),
    ("pesca notturna", [192], True),  # nightFish: sostituisce uno slot di Amo Buono/Super Amo di notte, sempre attivo
    ("sciame erba", [188], False),
    ("sciame surf", [190], False),
    ("sciame pesca", [194], False),
]
SWARM_KIND = {0: "sciame erba", 1: "sciame surf", 2: "sciame pesca"}


def read_swarm_maps(checks):
    """{(codice mappa, categoria)} degli sciami possibili: sSwarmMapLUT (codice), verificata nella ROM ITA.
    Gli sciami si attivano con il Pokédex Nazionale (EnableMassOutbreaks in P01R0101); ogni giorno una mappa a caso."""
    maps = {}
    for m in re.finditer(r"#define (MAP_\w+)\s+(\d+)\s*// MAP_(\w+)", (PRET / "include/constants/maps.h").read_text()):
        maps[m.group(1)] = (int(m.group(2)), m.group(3))
    lut = [(maps[a], int(b)) for a, b in
           re.findall(r"\{\s*(MAP_\w+),\s*(\d)\s*\}", (PRET / "src/unk_02097F6C.c").read_text())]
    blob = b"".join(struct.pack("<HH", mid, k) for (mid, _), k in lut)
    where = items_mod.find_code(blob)
    checks.append(("Mappe degli sciami (sSwarmMapLUT): decomp = ROM", bool(where), f"{len(lut)} mappe, {where or 'non trovata'}"))
    return {(code, SWARM_KIND[k]) for (_, code), k in lut}


def read_wild(checks):
    files = narc("a/0/3/7")
    names = [e["map"] for e in json.loads((PRET / "files/fielddata/encountdata/gs_enc_data.json").read_text())["encounters"]]
    checks.append(("Nomi tabelle selvatici (gs_enc_data.json)", len(names) == len(files), f"{len(names)} nomi / {len(files)} tabelle"))
    swarms = read_swarm_maps(checks)
    out = []  # (mappa, categoria, specie, normale?)
    for i, f in enumerate(files):
        name = names[i] if i < len(names) else f"#{i}"
        for cat, offs, normal in WILD_SLOTS:
            for o in offs:
                s = u16(f, o) & 0x3FF
                if s:
                    if cat.startswith("sciame") and (name, cat) not in swarms:
                        cat_ = "sciame mai attivo"  # mappa non nella tabella degli sciami: dato morto
                    else:
                        cat_ = cat
                    out.append((name, cat_, s, normal))
    return out


def read_headbutt():
    files = narc("a/2/5/2")
    names = [t["Map"] for t in json.loads((PRET / "files/arc/headbutt.json").read_text())["tables"]]
    out = []  # (mappa, gruppo, specie)
    for i, f in enumerate(files):
        if len(f) < 4 or u16(f, 0) == 0:
            continue
        for k in range(18):
            s = u16(f, 4 + k * 4)
            if s:
                out.append((names[i] if i < len(names) else f"#{i}", ("comune", "raro", "segreto")[k // 6], s))
    return out


def read_safari(checks):
    files = narc("a/2/3/0")
    js = json.loads((PRET / "files/arc/safari_enc.json").read_text())["encounters"]
    cats = ["land", "surf", "oldrod", "goodrod", "superrod"]
    out = []  # (area, categoria, specie, bonus?, condizioni)
    ok = True
    for i, f in enumerate(files):
        area = js[i]["area"] if i < len(js) else f"#{i}"
        bonus_n = list(f[0:5])
        o = 8
        for c, cat in enumerate(cats):
            n = len(js[i][cat]["mons"]["morn"]) if i < len(js) else 0
            for _ in range(3 * n):
                s = u16(f, o); o += 4
                if s:
                    out.append((area, cat, s, False, ""))
            b = bonus_n[c]
            bonus_sp = []
            for _ in range(3 * b):
                s = u16(f, o); o += 4
                bonus_sp.append(s)
            conds = []
            for _ in range(b):
                conds.append(tuple(f[o:o + 4])); o += 4
            for k, s in enumerate(bonus_sp):
                if s:
                    cnd = conds[k % b]
                    out.append((area, cat, s, True, f"oggetti tipo {cnd[0]}×{cnd[1]}" + (f" + tipo {cnd[2]}×{cnd[3]}" if cnd[3] else "")))
        if o != len(f):
            ok = False
    checks.append(("Layout Safari coerente con la decomp", ok, f"{len(files)} aree"))
    return out


def read_bug_contest():
    b = (ROM / "data/mushi/mushi_encount.bin").read_bytes()
    out = []  # (tabella, specie)
    for k in range(len(b) // 8):
        out.append((k // 10, u16(b, k * 8)))
    return out


def read_trainers(checks):
    trd, trp = narc("a/0/5/5"), narc("a/0/5/6")
    js = json.loads((PRET / "files/poketool/trainer/trainers.json").read_text())["trainers"]
    checks.append(("Nomi allenatori (trainers.json)", len(js) == len(trd), f"{len(js)} nomi / {len(trd)} allenatori"))
    agree = 0
    out = []  # (idx, classe, nome, [(specie, livello)])
    for i, (d, p) in enumerate(zip(trd, trp)):
        n = d[3] if len(d) >= 4 else 0
        party = []
        if n:
            size = len(p) // n
            for k in range(n):
                party.append((u16(p, k * size + 4) & 0x3FF, u16(p, k * size + 2)))
        cls = js[i]["class"].replace("TRAINERCLASS_", "") if i < len(js) else "?"
        name = re.sub(r"\{[^}]*\}", "", js[i]["name"]) if i < len(js) else "?"
        if i < len(js) and [SPECIES_BY_CONST.get(m["species"], -1) for m in js[i]["party"]] == [s for s, _ in party]:
            agree += 1
        out.append((i, cls, name, party))
    checks.append(("Squadre allenatori: decomp = ROM", agree == len(trd), f"{agree}/{len(trd)} identiche"))
    return out


TRADE_NAMES = ["Rocky (Onix)", "Muscle (Machop)", "Billy (Voltorb)", "Doris (Dodrio)", "Sprints (Rapidash)",
               "Rusty (Steelix)", "Shuckie (Shuckle, prestito)", "Kenya (Spearow, prestito)", "Maggie (Magneton)",
               "Paul (Xatu)", "Volty (Pikachu)", "Hornlette (Rhyhorn)", "Iron (Beldum)"]


def read_trades():
    out = []  # (nome, dai, ricevi)
    for i, f in enumerate(parse_narc((ROM / "data/tradelist.narc").read_bytes())):
        give, ask = struct.unpack_from("<I", f, 0)[0], struct.unpack_from("<I", f, 0x4C)[0]
        out.append((TRADE_NAMES[i] if i < len(TRADE_NAMES) else f"#{i}", ask, give))
    return out


def read_frontier():
    out = {}
    # set da 16 byte: specie, 4 mosse, EV, natura, strumento, forma (FrontierMonNarcData in unk_0204B538.c).
    # Allenatori (104 byte): classe u16, numero di set u16, indici dei set u16: si puliscono cambiando solo i set.
    for a, desc in [("a/1/2/9", "set A, allenatori a/1/2/8 (altra struttura, codice non decompilato)"),
                    ("a/2/0/3", "set B, allenatori a/2/0/2 (Torre Lotta, unk_0204B538.c)"),
                    ("a/2/0/4", "set C (478, probabilmente noleggi Factory)")]:
        c = collections.Counter(u16(f, 0) & 0x7FF for f in narc(a) if len(f) >= 2)
        c.pop(0, None)
        out[a] = (desc, c)
    return out


def read_johto_dex():
    """{specie nazionale: numero nel Pokédex di Johto} da a/1/3/8 (johtozukan.narc): una tabella u16 indicizzata
    per numero nazionale (0..493), 0 = assente."""
    data = parse_narc((ROM / "a/1/3/8").read_bytes())[0]
    return {s: u16(data, s * 2) for s in range(1, len(data) // 2) if u16(data, s * 2)}


# --- script (dalla decomp; a/0/1/2 identico tra IPKI e IPKE)
SCRIPT_CMDS = ("GiveMon", "WildBattle", "GiveEgg", "CreateRoamer", "GiveSpikyEarPichu", "GiveTogepiEgg")
ROAMERS = {0: "RAIKOU", 1: "ENTEI", 2: "LATIAS", 3: "LATIOS"}  # da script T06 (ScrCmd_452 + CreateRoamer)


def read_scripts():
    """[(file, comando, [specie], livello/nota)]"""
    out = []
    for p in sorted((PRET / "files/fielddata/script/scr_seq").glob("*.s")):
        text = p.read_text(errors="replace")
        lines = text.splitlines()
        varvals = collections.defaultdict(set)
        for m in re.finditer(r"(?:SetVar|SetOrCopyVar)\s+(VAR_\w+),\s*(SPECIES_\w+|\d+)", text):
            v = m.group(2)
            n = SPECIES_BY_CONST.get(v) if v.startswith("SPECIES_") else int(v)
            if n and 1 <= n <= 493:
                varvals[m.group(1)].add(n)
        for ln in lines:
            t = ln.strip()
            cmd = t.split()[0] if t else ""
            if cmd not in SCRIPT_CMDS:
                continue
            args = [a.strip() for a in t[len(cmd):].split(",")]
            species, note = [], ""
            if cmd == "CreateRoamer":
                species = [SPECIES_BY_CONST["SPECIES_" + ROAMERS[int(args[0])]]]
                note = "vagante"
            elif cmd == "GiveSpikyEarPichu":
                species, note = [172], "solo con Pichu evento"
            elif cmd == "GiveTogepiEgg":
                species, note = [175], "uovo"
            else:
                a0 = args[0]
                if a0.startswith("SPECIES_"):
                    species = [SPECIES_BY_CONST[a0]]
                elif a0.startswith("VAR_"):
                    species = sorted(varvals.get(a0, []))
                    note = "da variabile"
                if cmd in ("GiveMon", "WildBattle") and len(args) > 1:
                    note = (note + " " if note else "") + f"lv {args[1]}"
                if cmd == "GiveEgg":
                    note = "uovo"
            out.append((p.stem.replace("scr_seq_", ""), cmd, species, note))
    return out


def script_items():
    """Oggetti di interesse dati/trovati negli script: {item_const: [file]}"""
    wanted = re.compile(r"ITEM_(\w*(INCENSE|STONE)|METAL_COAT|DRAGON_SCALE|KINGS_ROCK|UPGRADE|DUBIOUS_DISC|PROTECTOR|"
                        r"ELECTIRIZER|MAGMARIZER|RAZOR_FANG|RAZOR_CLAW|REAPER_CLOTH|DEEPSEA_\w+|PRISM_SCALE|\w*FOSSIL|OLD_AMBER)\b")
    out = collections.defaultdict(set)
    for p in (PRET / "files/fielddata/script/scr_seq").glob("*.s"):
        for m in wanted.finditer(p.read_text(errors="replace")):
            out[m.group(0)].add(p.stem.replace("scr_seq_", ""))
    return out


# ---------------------------------------------------------------- analisi ottenibilità
def closure(start, evo, personal):
    """Specie ottenibili partendo da `start` con evoluzioni fattibili in solitario e allevamento.
    Ritorna (insieme, {specie: [come]})."""
    obtain = set(start)
    via = collections.defaultdict(set)
    pre = {}
    for s, lst in evo.items():
        for m, prm, t in lst:
            pre.setdefault(t, s)
    changed = True
    while changed:
        changed = False
        for s in list(obtain):
            for m, prm, t in evo.get(s, []):
                if m in EVO_IMPOSSIBLE_SOLO:
                    via[t].add(f"evoluzione {m} (impossibile da solo)")
                    continue
                if t not in obtain:
                    obtain.add(t); changed = True
                    via[t].add(f"evoluzione da {sp(s)}")
            eg = personal.get(s, (15, 15))
            if 15 not in eg[:2]:  # 15 = gruppo uova "Sconosciuto"
                base = s
                while base in pre and pre[base] <= 493:
                    base = pre[base]
                if base not in obtain and 1 <= base <= 251:
                    obtain.add(base); changed = True
                    via[base].add(f"allevamento da {sp(s)}")
    return obtain, via


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "docs" / "audit.md"))
    args = ap.parse_args()
    for need, hint in [(ROM, "python tools/roundtrip.py"), (PRET / "include", "python tools/get_pret.py")]:
        if not need.exists():
            sys.exit(f"Manca {need}: eseguire prima `{hint}`")

    checks = []
    evo = read_evolutions()
    personal = read_personal()
    wild = read_wild(checks)
    headbutt = read_headbutt()
    safari = read_safari(checks)
    bug = read_bug_contest()
    trainers = read_trainers(checks)
    trades = read_trades()
    frontier = read_frontier()
    dex = read_johto_dex()
    scripts = read_scripts()
    items = script_items()

    # fonti per specie (<= 251 per la matrice; > 251 per la pulizia)
    src = collections.defaultdict(set)
    for m, cat, s, normal in wild:
        if cat == "sciame mai attivo":
            continue
        src[s].add("selvatico" if normal else cat + " (dopo il Nazionale)")
    for m, g, s in headbutt:
        src[s].add("bottintesta")
    for a, cat, s, bonus, _ in safari:
        src[s].add("safari (bonus oggetti)" if bonus else "safari")
    for t, s in bug:
        # tabella 0 prima del Nazionale; dopo, martedì/giovedì/sabato → 1/2/3 (overlay_bug_contest.c)
        src[s].add("gara coleottero" if t == 0 else f"gara coleottero t{t} (dopo il Nazionale)")
    for name, ask, give in trades:
        src[give].add(f"scambio ({name})")
    # Sinjoh (Arceus evento), Pichu spunzorecchio (Pichu evento), Lati statico di Plumbeopoli (Pietrenigma evento)
    event_only = {"D51R0201", "0092_D36R0101", "0750_T03"}
    # regali "1 su 3": Oak dopo Red (T01R0301, starter di Kanto) e Rocco (T11R0701, oggi starter di Hoenn).
    # Dopo la scelta le altre Poké Ball spariscono: si trattano come gruppi di starter, non come 3 regali.
    choice_gifts = {"T01R0301": (1, 4, 7), "T11R0701": (252, 255, 258)}
    for f, cmd, species, note in scripts:
        if any(f.endswith(e) or f == e for e in event_only) or "evento" in note:
            continue
        if any(f.endswith(k) and set(species) <= set(v) for k, v in choice_gifts.items()):
            continue
        for s in species:
            src[s].add({"GiveMon": "regalo", "WildBattle": "statico", "GiveEgg": "uovo regalo",
                        "CreateRoamer": "vagante", "GiveTogepiEgg": "uovo regalo"}.get(cmd, cmd) + f" [{f}]")
    # fossili: rianimati al Museo di Plumbeopoli (script T03R0101); il fossile si trova solo con Spaccaroccia
    # (tabelle nel codice, lette e verificate da tools/items.py)
    smash_items = {it for _, its, maps in items_mod.rock_smash([]) if maps for it, _ in its}
    for it, s in {"ITEM_HELIX_FOSSIL": 138, "ITEM_DOME_FOSSIL": 140, "ITEM_OLD_AMBER": 142}.items():
        if ITEM_BY_CONST[it] in smash_items:
            src[s].add(f"fossile {it[5:]} (Spaccaroccia) rianimato [T03R0101]")

    # chiusura: evoluzioni fattibili in solitario + allevamento
    obtain, via = closure({s for s in src if 1 <= s <= 493}, evo, personal)
    # gruppi "1 su 3": starter di Johto (inizio) e starter di Kanto (Oak dopo Red). Per ogni gruppo una famiglia è
    # ottenibile, le altre due contano come mancanti
    groups = {"starter di Johto": (152, 155, 158), "starter di Kanto (Oak, dopo Red)": (1, 4, 7)}
    starter_fam = {}  # base → (gruppo, famiglia)
    for g, bases in groups.items():
        for s in bases:
            if s not in obtain:
                fam, _ = closure({s}, evo, personal)
                starter_fam[s] = (g, {x for x in fam if x not in obtain and x <= 251})
    starter_species = set().union(*(f for _, f in starter_fam.values())) if starter_fam else set()
    for g, fam in starter_fam.values():
        for s in fam:
            src[s].add(f"{g} (1 famiglia su 3)")

    # ---------------------------------------------------------------- report
    r = Report()
    r.p("# Audit HeartGold ITA (IPKI) — specie > #251 e ottenibilità delle 251")
    r.p()
    r.p("Generato da `python tools/audit.py`. Dati letti da `work/IPKI` (ROM ITA estratta); nomi e script dalla "
        "decomp pret/pokeheartgold (commit in `tools/get_pret.py`). Contiene solo nomi e ID.")

    r.h(2, "Controlli di coerenza ROM ↔ decomp")
    r.table(["Controllo", "Esito", "Dettaglio"], [(c, "OK" if ok else "**NO**", d) for c, ok, d in checks])

    # riepilogo sporco
    r.h(2, "Riepilogo: dove compaiono specie > #251")
    rows = []
    def add(label, species_iter):
        c = collections.Counter(s for s in species_iter if s > 251)
        g3 = sum(n for s, n in c.items() if gen(s) == 3); g4 = sum(n for s, n in c.items() if gen(s) == 4)
        rows.append((label, g3, g4, len(c)))
    add("Selvatici — slot normali", (s for m, cat, s, n in wild if n))
    add("Selvatici — radio Hoenn/Sinnoh", (s for m, cat, s, n in wild if cat.startswith("radio")))
    add("Selvatici — sciami attivi (20 mappe)", (s for m, cat, s, n in wild if cat.startswith("sciame ") and cat != "sciame mai attivo"))
    add("Selvatici — sciami mai attivi (dato morto)", (s for m, cat, s, n in wild if cat == "sciame mai attivo"))
    add("Bottintesta", (s for m, g, s in headbutt))
    add("Safari — base", (s for a, c, s, b, _ in safari if not b))
    add("Safari — bonus oggetti", (s for a, c, s, b, _ in safari if b))
    add("Gara Pigliamosche", (s for t, s in bug))
    add("Allenatori", (s for i, c, n, party in trainers for s, _ in party))
    add("Scambi in gioco (ricevuti)", (give for _, _, give in trades))
    add("Script (regali/statici/vaganti)", (s for f, cmd, sps, note in scripts for s in sps))
    for a, (desc, c) in frontier.items():
        add(f"Parco Lotta {desc}", c.elements())
    add("Pokédex di Johto (voci)", dex)
    r.table(["Fonte", "slot gen 3", "slot gen 4", "specie distinte"], rows)

    r.h(2, "Evoluzioni verso specie > #251 (da rimuovere, D8)")
    r.table(["Da", "A", "Metodo", "Parametro"],
            [(sp(s), sp(t), m, ITEMS.get(prm, prm) if m in EVO_ITEM_PARAM else prm)
             for s in range(1, 252) for m, prm, t in evo[s] if t > 251])

    r.h(2, "Evoluzioni tra le 251 impossibili senza scambio (D7)")
    r.table(["Da", "A", "Metodo", "Oggetto"],
            [(sp(s), sp(t), m, ITEMS.get(prm, "-") if m == "TRADE_ITEM" else "-")
             for s in range(1, 252) for m, prm, t in evo[s] if t <= 251 and m in EVO_IMPOSSIBLE_SOLO])

    r.h(2, "Condizioni di sblocco (dal codice)")
    r.p("- **Radio Suono Hoenn / Suono Sinnoh** (programma Musica Pokémon): solo con il Pokédex Nazionale, "
        "Hoenn il mercoledì, Sinnoh il giovedì (`pokemon_music.c`). Sostituiscono gli slot erba 2-5.")
    r.p("- **Sciami**: attivati da Oak alla consegna del Pokédex Nazionale (`EnableMassOutbreaks`, P01R0101); ogni giorno "
        "una delle 20 mappe di `sSwarmMapLUT`. Gli sciami delle altre mappe non si attivano mai (dato morto).")
    r.p("- **Pesca notturna** (`nightFish`): di notte sostituisce uno slot di Amo Buono/Super Amo, sempre attiva.")
    r.p("- **Gara Pigliamosche**: tabella 0 prima del Nazionale; dopo, martedì/giovedì/sabato → tabelle 1/2/3 "
        "(`overlay_bug_contest.c`). Le specie gen 3-4 sono solo nelle tabelle 2-3.")

    r.h(2, "Sciami attivi")
    r.table(["Mappa", "Tipo", "Specie"],
            [(m, c, f"**{sp(s)}**" if s > 251 else sp(s)) for m, c, s, n in sorted(wild)
             if c.startswith("sciame ") and c != "sciame mai attivo"])

    r.h(2, "Selvatici: radio e sciami per mappa")
    by = collections.defaultdict(collections.Counter)
    for m, cat, s, n in wild:
        if not n and s > 251:
            by[(m, cat)][s] += 1
    r.table(["Mappa", "Categoria", "Specie > 251"], [(m, c, fmt_counter(v)) for (m, c), v in sorted(by.items())])

    r.h(2, "Bottintesta")
    hb = collections.defaultdict(collections.Counter)
    for m, g, s in headbutt:
        if s > 251:
            hb[(m, g)][s] += 1
    r.p(f"Tabelle con alberi: {len({m for m, g, s in headbutt})}. Voci con specie > 251: {sum(sum(v.values()) for v in hb.values())}.")
    if hb:
        r.table(["Mappa", "Gruppo", "Specie"], [(m, g, fmt_counter(v)) for (m, g), v in sorted(hb.items())])

    r.h(2, "Safari")
    sf = collections.defaultdict(collections.Counter)
    for a, c, s, b, cond in safari:
        if s > 251:
            sf[(a, c, "bonus" if b else "base", cond)][s] += 1
    r.table(["Area", "Categoria", "Tipo", "Condizione", "Specie > 251"],
            [(a, c, t, cond, fmt_counter(v)) for (a, c, t, cond), v in sorted(sf.items())])

    r.h(2, "Gara Pigliamosche")
    r.table(["Tabella", "Specie"], [(t, ", ".join(sp(s) for tt, s in bug if tt == t)) for t in sorted({t for t, _ in bug})])

    r.h(2, "Allenatori con specie > #251")
    r.table(["#", "Classe", "Nome", "Squadra (liv.)"],
            [(i, c, n, ", ".join(f"**{sp(s)}**" if s > 251 else sp(s) for s, lv in party) + f" ({min(lv for _, lv in party)}-{max(lv for _, lv in party)})")
             for i, c, n, party in trainers if any(s > 251 for s, _ in party)])

    r.h(2, "Scambi in gioco")
    r.table(["NPC", "Chiede", "Dà"], [(n, sp(a), f"**{sp(g)}**" if g > 251 else sp(g)) for n, a, g in trades])

    r.h(2, "Script: regali, incontri statici, uova, vaganti")
    r.table(["Script", "Comando", "Specie", "Note"],
            [(f, c, ", ".join(f"**{sp(s)}**" if s > 251 else sp(s) for s in sps) or "?", note) for f, c, sps, note in scripts])

    r.h(2, "Parco Lotta (set di Pokémon)")
    r.p("Formato set (16 byte): specie, 4 mosse, EV, natura, strumento, forma. Gli allenatori contengono solo indici "
        "dei set: per ripulire basta sostituire le specie (e le mosse) nei set gen 3-4.")
    r.p()
    r.table(["Archivio", "Descrizione", "Set totali", "Set gen 3", "Set gen 4"],
            [(a, d, sum(c.values()), sum(n for s, n in c.items() if gen(s) == 3), sum(n for s, n in c.items() if gen(s) == 4))
             for a, (d, c) in frontier.items()])

    r.h(2, "Altri archivi controllati")
    r.p("- `a/0/6/6` (64×12 B): dati delle **bacche** (vasi di bacche, `overlay_16_022014A0.c`): i numeri non sono specie.")
    r.p("- `a/2/5/8` (100×8 B): 3 specie + indice per voce; codice non decompilato. Ipotesi: squadre avversarie del "
        "Pokéathlon. Contiene qualche specie gen 3-4 (da ripulire per coerenza, non si catturano).")
    r.p("- `a/2/5/4` = `photo_data` (foto dello studio fotografico).")

    r.h(2, "Pokédex di Johto")
    extra = sorted((n, s) for s, n in dex.items() if s > 251)
    absent = [s for s in range(1, 252) if s not in dex]
    r.p(f"a/1/3/8 = tabella numero nazionale → numero di Johto. Voci: {len(dex)}, numeri da 1 a {max(dex.values())}. "
        f"Specie > 251 presenti: {len(extra)}" + (" — " + ", ".join(f"{sp(s)} (J{n})" for n, s in extra) if extra else "")
        + f". Specie 1-251 assenti dal Pokédex di Johto: {len(absent)}"
        + (" — " + ", ".join(sp(s) for s in absent) if absent else "") + ".")

    r.h(2, "Oggetti per evoluzioni/allevamento negli script")
    r.p("Solo oggetti citati per costante negli script. Quadro completo (a terra, nascosti, negozi, Spaccaroccia, "
        "premi): `docs/oggetti.md` (`python tools/items.py`).")
    held = collections.defaultdict(set)
    for s, (e1, e2, i1, i2) in personal.items():
        for it in (i1, i2):
            if it and ITEMS.get(it, "") in {k for k in items} | {"ITEM_METAL_COAT", "ITEM_DRAGON_SCALE", "ITEM_KINGS_ROCK", "ITEM_UPGRADE"}:
                held[ITEMS[it]].add(sp(s))
    r.table(["Oggetto", "Script", "Tenuto da selvatici"],
            [(k, ", ".join(sorted(v)[:8]) + (" …" if len(v) > 8 else ""), ", ".join(sorted(held.get(k, []))) or "-")
             for k, v in sorted(items.items())]
            + [(k, "-", ", ".join(sorted(v))) for k, v in sorted(held.items()) if k not in items])

    r.h(2, "Matrice di ottenibilità #001-#251 (una partita, HeartGold, senza scambi né eventi)")
    missing = [s for s in range(1, 252) if s not in obtain and s not in starter_species]
    # "solo condizionale": ottenibile, ma non più se si tolgono radio, sciami, bonus Safari e gara post-Nazionale
    def conditional(x):
        return x.startswith(("radio", "sciame", "safari (bonus")) or "dopo il Nazionale" in x
    uncond, _ = closure({s for s, v in src.items() if 1 <= s <= 493 and not all(conditional(x) for x in v)}, evo, personal)
    only_cond = [s for s in range(1, 252) if s in obtain and s not in uncond]
    one_per_group = sum(max(len(f) for gg, f in starter_fam.values() if gg == g)
                        for g in {gg for gg, _ in starter_fam.values()})
    n_ok = 251 - len(missing) - len(starter_species) + one_per_group
    r.p(f"**Ottenibili: {n_ok}/251** (contando una famiglia per ogni scelta di starter). Mancanti: {len(missing)}"
        + (f" + le {len(starter_species) - one_per_group} specie delle famiglie di starter non scelte "
           "(2 su 3 per Johto e per Kanto)." if starter_species else "."))
    r.p()
    r.table(["#", "Specie", "Stato", "Fonti"],
            [(f"{s:03}", sp(s), "MANCA" if s in missing else "starter 1 su 3" if s in starter_species
              else ("solo condizionale" if s in only_cond else "ok"),
              "; ".join(sorted(src.get(s, set())) + sorted(via.get(s, set()))) or "-") for s in range(1, 252)])

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(r.lines).lstrip() + "\n", encoding="utf-8")
    print(f"Report: {out.relative_to(ROOT)}")
    print(f"Ottenibili {n_ok}/251 (1 famiglia per scelta di starter); mancanti: {', '.join(sp(s) for s in missing)}")
    for c, ok, d in checks:
        print(f"[{'OK' if ok else 'NO'}] {c}: {d}")


if __name__ == "__main__":
    main()
