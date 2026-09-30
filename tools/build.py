"""Fase 4 — costruisce la ROM modificata applicando data/design/*.csv all'estrazione di IPKI.

Passi:
  1. copia work/IPKI → work/build (l'estrazione originale non si tocca)
  2. applica le modifiche ai dati (NARC, script 0141, overlay 1)
  3. verifica sui file costruiti (audit rieseguito su work/build: 0 specie > 251 dove previsto)
  4. dsrom build → out/PokemonCrystalNew_IPKI.nds e patch BPS → out/PokemonCrystalNew_IPKI.bps

Prerequisiti: python tools/roundtrip.py (work/IPKI), python tools/get_pret.py.
Uso: python tools/build.py [--no-rom]   (--no-rom: solo modifiche e verifica, senza dsrom/BPS)
"""
import argparse
import collections
import csv
import re
import shutil
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ndsfs import pack_narc, parse_narc, u16  # noqa: E402
import audit  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "work" / "IPKI"
BUILD = ROOT / "work" / "build"
DESIGN = ROOT / "data" / "design"
OUT = ROOT / "out"
NAME = "PokemonCrystalNew_IPKI"
sp = audit.sp
LEVEL_METHODS = {"LEVEL", "LEVEL_ATK_GT_DEF", "LEVEL_ATK_EQ_DEF", "LEVEL_ATK_LT_DEF", "LEVEL_PID_LO", "LEVEL_PID_HI",
                 "LEVEL_NINJASK", "LEVEL_MALE", "LEVEL_FEMALE"}


def rows(name):
    with open(DESIGN / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(line for line in f if not line.startswith("#")))


def spc(const):
    return audit.SPECIES_BY_CONST["SPECIES_" + const]


class Narc:
    """NARC di work/build modificabile: n = Narc('a/0/3/7'); n[i] = bytes; n.save()."""
    def __init__(self, path):
        self.path = BUILD / "files" / path
        self.orig = self.path.read_bytes()
        self.files = [bytearray(f) for f in parse_narc(self.orig)]

    def save(self):
        self.path.write_bytes(pack_narc([bytes(f) for f in self.files], self.orig))


def set16(buf, o, v):
    struct.pack_into("<H", buf, o, v)


class Ctx:
    def __init__(self):
        self.subs = {int(r["id"]): int(r["sostituto_id"]) for r in rows("sostituzioni.csv")}
        self.log = collections.Counter()
        self.evo = None  # dopo apply_evolutions: {specie: [(metodo, param, target)]}
        self.learn = [[(e & 0x1FF, e >> 9) for e in struct.unpack_from(f"<{len(f) // 2}H", f) if e != 0xFFFF]
                      for f in parse_narc((SRC / "files/a/0/3/3").read_bytes())]

    def S(self, s):
        return self.subs.get(s, s)

    def moves_at(self, species, level):
        """Le ultime 4 mosse diverse imparate per livello fino a `level` (come fa il gioco di default)."""
        out = []
        for mv, lv in self.learn[species]:
            if lv <= level and mv not in out:
                out.append(mv)
        out = out[-4:]
        return out + [0] * (4 - len(out))

    def fit_level(self, s, level):
        """Evolve o fa regredire `s` secondo le evoluzioni per livello, per essere coerente con `level`."""
        pre = {t: (a, m, p) for a, lst in self.evo.items() for m, p, t in lst if 1 <= t <= 251}
        changed = True
        while changed:
            changed = False
            if s in pre and pre[s][1] in LEVEL_METHODS and level < pre[s][2]:
                s = pre[s][0]; changed = True; continue
            for m, p, t in self.evo.get(s, []):
                if m in LEVEL_METHODS and 1 <= t <= 251 and p <= level:
                    s = t; changed = True; break
        return s


# ------------------------------------------------------------------ modifiche
def apply_evolutions(c):
    n = Narc("a/0/3/4")
    evo = {}
    for r in rows("evoluzioni.csv"):
        a, t = spc(r["da"]), spc(r["verso"])
        f = n.files[a]
        for k in range(0, 42, 6):
            m, p, tt = struct.unpack_from("<HHH", f, k)
            if tt == t and m:
                break
        else:
            raise SystemExit(f"evoluzione {r['da']} → {r['verso']} non trovata")
        if r["metodo"] == "NONE":
            struct.pack_into("<HHH", f, k, 0, 0, 0)
        else:
            prm = audit.ITEM_BY_CONST[r["parametro"]] if r["parametro"].startswith("ITEM_") else int(r["parametro"])
            struct.pack_into("<HHH", f, k, audit.EVO.index(r["metodo"]), prm, t)
        c.log["evoluzioni"] += 1
    # compatta: niente buchi tra le voci (il gioco scorre le 7 voci; un buco è innocuo ma teniamo ordine pulito)
    for i, f in enumerate(n.files):
        ent = [struct.unpack_from("<HHH", f, k) for k in range(0, 42, 6)]
        ent = [e for e in ent if e[0]] + [(0, 0, 0)] * sum(1 for e in ent if not e[0])
        for k, e in enumerate(ent):
            struct.pack_into("<HHH", f, k * 6, *e)
        evo[i] = [(audit.EVO[m] if m < len(audit.EVO) else str(m), p, t) for m, p, t in ent if m]
    n.save()
    c.evo = evo


def apply_wild(c):
    import json
    names = [e["map"] for e in json.loads((audit.PRET / "files/fielddata/encountdata/gs_enc_data.json").read_text())["encounters"]]
    n = Narc("a/0/3/7")
    for r in rows("selvatici.csv"):
        f = n.files[names.index(r["mappa"])]
        o = int(r["offset"])
        cur = u16(f, o)
        if sp(cur & 0x3FF) != r["da"]:
            raise SystemExit(f"selvatici.csv: {r} ma nella ROM c'è {sp(cur & 0x3FF)}")
        set16(f, o, (cur & ~0x3FF) | next(k for k, v in audit.SPECIES.items() if sp(k) == r["a"]))
        c.log["selvatici (dedicate)"] += 1
    for f in n.files:
        for cat, offs, _ in audit.WILD_SLOTS:
            for o in offs:
                s = u16(f, o) & 0x3FF
                if s > 251:
                    set16(f, o, (u16(f, o) & ~0x3FF) | c.S(s)); c.log["selvatici (sostituzioni)"] += 1
    n.save()


def apply_simple(c):
    # Bottintesta: 18 voci da 4 byte da offset 4 (specie u16)
    n = Narc("a/2/5/2")
    for f in n.files:
        if len(f) >= 4 and u16(f, 0):
            for k in range(18):
                o = 4 + k * 4
                if u16(f, o) > 251:
                    set16(f, o, c.S(u16(f, o))); c.log["bottintesta"] += 1
    n.save()
    # Safari: tutte le voci specie (u16 ogni 4 byte dopo l'intestazione di 8 byte, esclusi i blocchi condizione)
    n = Narc("a/2/3/0")
    import json
    js = json.loads((audit.PRET / "files/arc/safari_enc.json").read_text())["encounters"]
    for i, f in enumerate(n.files):
        o = 8
        bonus_n = list(f[0:5])
        for ci, cat in enumerate(["land", "surf", "oldrod", "goodrod", "superrod"]):
            for _ in range(3 * len(js[i][cat]["mons"]["morn"]) + 3 * bonus_n[ci]):
                if u16(f, o) > 251:
                    set16(f, o, c.S(u16(f, o))); c.log["safari"] += 1
                o += 4
            o += 4 * bonus_n[ci]
        assert o == len(f)
    n.save()
    # Gara Pigliamosche: record da 8 byte, specie a 0
    p = BUILD / "files/data/mushi/mushi_encount.bin"
    b = bytearray(p.read_bytes())
    for k in range(0, len(b), 8):
        if u16(b, k) > 251:
            set16(b, k, c.S(u16(b, k))); c.log["gara"] += 1
    p.write_bytes(bytes(b))
    # Pokéathlon (ipotesi) a/2/5/8: 3 specie u16
    n = Narc("a/2/5/8")
    for f in n.files:
        for o in (0, 2, 4):
            if u16(f, o) > 251:
                set16(f, o, c.S(u16(f, o))); c.log["Pokéathlon"] += 1
    n.save()


def apply_trainers(c):
    trd, trp = Narc("a/0/5/5"), Narc("a/0/5/6")
    for d, p in zip(trd.files, trp.files):
        cnt = d[3] if len(d) >= 4 else 0
        if not cnt:
            continue
        flags = d[0]
        size = 8 + (2 if flags & 2 else 0) + (8 if flags & 1 else 0)
        for k in range(cnt):
            o = k * size
            raw = u16(p, o + 4)
            s, lv = raw & 0x3FF, u16(p, o + 2)
            if s <= 251:
                continue
            new = c.fit_level(c.S(s), lv)
            set16(p, o + 4, (raw & ~0x3FF) | new)
            if flags & 1:
                mo = o + 6 + (2 if flags & 2 else 0)
                struct.pack_into("<4H", p, mo, *c.moves_at(new, lv))
            c.log["allenatori"] += 1
    trp.save()


def apply_trades(c):
    n = Narc("a/1/1/2")
    fix = {}
    for r in rows("eventi.csv"):
        m = re.match(r"a/1/1/2 #(\d+)", r["dove"]) if r["tipo"] == "scambio" else None
        if m:
            fix[(int(m.group(1)), "(chiede)" in r["dove"])] = (spc(r["da"]), spc(r["a"]))
    for i, f in enumerate(n.files):
        for is_ask, o in ((True, 0x4C), (False, 0)):
            cur = struct.unpack_from("<I", f, o)[0]
            if (i, is_ask) in fix:
                assert cur == fix[(i, is_ask)][0]
                struct.pack_into("<I", f, o, fix[(i, is_ask)][1]); c.log["scambi"] += 1
            elif cur > 251:
                struct.pack_into("<I", f, o, c.S(cur)); c.log["scambi"] += 1
    n.save()


def apply_frontier(c):
    # set da 16 byte: specie (11 bit + forma), 4 mosse, EV, natura, strumento, forma
    for a in ("a/1/2/9", "a/2/0/3", "a/2/0/4"):
        n = Narc(a)
        for f in n.files:
            if len(f) < 10:
                continue
            raw = u16(f, 0)
            s = raw & 0x7FF
            if s > 251:
                new = c.S(s)
                set16(f, 0, new)  # forma azzerata: la forma della specie tolta non vale per il sostituto
                struct.pack_into("<4H", f, 2, *c.moves_at(new, 100))
                c.log["Parco Lotta"] += 1
        n.save()


def apply_items(c):
    # strumenti a terra: voce N di scr_seq_0141 = "SetVar 0x8008, oggetto" (opcode 41)
    std = {m.group(1): int(m.group(2)) for m in re.finditer(r"#define (std_\w+)\s+(\d+)", (audit.PRET / "include/constants/std_script.h").read_text())}
    n = Narc("a/0/1/2")
    s = n.files[141]
    offs, o = [], 0
    while (struct.unpack_from("<I", s, o)[0] & 0xFFFF) != 0xFD13:
        offs.append(o + 4 + struct.unpack_from("<i", s, o)[0]); o += 4
    item_rows = [r for r in rows("oggetti.csv") if r["tipo"] == "a_terra"]
    for r in item_rows:
        q = offs[std[r["dove"]] - 7000]
        op, var, val = struct.unpack_from("<HHH", s, q)
        assert (op, var, val) == (41, 0x8008, audit.ITEM_BY_CONST[r["da"]]), (r, op, var, val)
        set16(s, q + 4, audit.ITEM_BY_CONST[r["a"]]); c.log["strumenti a terra"] += 1
    n.save()
    # Spaccaroccia (overlay 1): tabelle HG cercate per contenuto
    ov = BUILD / "arm9_overlays/ov001.bin"
    b = bytearray(ov.read_bytes())
    txt = (audit.PRET / "src/field/rock_smash_item.c").read_text()
    hg = re.sub(r"#else.*?#endif[^\n]*", "", txt, flags=re.S)
    tables = {nm: [audit.ITEM_BY_CONST[t] for t in re.findall(r"ITEM_\w+", body)]
              for nm, body in re.findall(r"static const u16 sRockSmashItems_(\w+)\[\] = \{(.*?)\};", hg, re.S)}
    where = {}
    for nm, its in tables.items():
        blob = struct.pack(f"<{len(its)}H", *its)
        assert b.count(blob) == 1, f"tabella Spaccaroccia {nm} non univoca in ov001"
        where[nm] = b.find(blob)
    for r in rows("oggetti.csv"):
        if r["tipo"] == "spaccaroccia":
            nm, k = r["dove"].split(":")
            o = where[nm] + 2 * int(k)
            assert u16(b, o) == audit.ITEM_BY_CONST[r["da"]], r
            set16(b, o, audit.ITEM_BY_CONST[r["a"]]); c.log["Spaccaroccia"] += 1
    ov.write_bytes(bytes(b))
    # oggetti usabili come pietre (D7): copia uso sul campo/party dalla Pietrafocaia
    idx = {m.group(1): int(m.group(2)) for m in re.finditer(r"\[(ITEM_\w+)\]\s*=\s*\{\s*NARC_item_data_(\d+)_bin", (audit.PRET / "src/item.c").read_text())}
    n = Narc("a/0/1/7")
    fire = n.files[idx["ITEM_FIRE_STONE"]]
    assert fire[10] == 20 and fire[12] == 1, "dati Pietrafocaia inattesi"
    for r in rows("oggetti.csv"):
        if r["tipo"] == "uso_pietra":
            f = n.files[idx[r["dove"]]]
            f[10], f[12] = fire[10], fire[12]
            f[14:32] = fire[14:32]
            c.log["oggetti come pietre"] += 1
    n.save()


def apply_map_objects(c):
    sprites = {m.group(1): int(m.group(2)) for m in re.finditer(r"#define (SPRITE_\w+)\s+(\d+)", (audit.PRET / "include/constants/sprites.h").read_text())}
    n = Narc("a/0/3/2")
    for r in rows("oggetti_mappa.csv"):
        f = n.files[int(r["zona"])]
        nb = struct.unpack_from("<I", f, 0)[0]
        o = 4 + nb * 20 + 4 + int(r["oggetto"]) * 32 + {"sprite": 2}[r["campo"]]
        assert u16(f, o) == sprites[r["da"]], (r, u16(f, o))
        set16(f, o, sprites[r["a"]]); c.log["oggetti delle mappe"] += 1
    n.save()


def apply_scripts(c):
    import scrpatch
    n = Narc("a/0/1/2")
    for idx, b in scrpatch.patched_scripts().items():
        n.files[idx] = bytearray(b); c.log["script"] += 1
    n.save()


def apply_pokedex(c):
    """Pokédex di Johto senza le specie > 251 (le 5 evoluzioni gen 4): tabella nazionale → Johto rinumerata
    (a/1/3/8) e lista in ordine di Johto (membro 12 di a/0/7/4 e a/2/1/4, lunghezza letta dal gioco come size/2)."""
    n = Narc("a/1/3/8")
    lut = n.files[0]
    num = {s: u16(lut, s * 2) for s in range(len(lut) // 2)}
    order = sorted((j, s) for s, j in num.items() if j and s <= 251)
    for s in num:
        set16(lut, s * 2, 0)
    for k, (j, s) in enumerate(order, 1):
        set16(lut, s * 2, k)
    c.log["Pokédex di Johto (voci)"] = len(order)
    n.save()
    for a in ("a/0/7/4", "a/2/1/4"):
        n = Narc(a)
        lst = struct.unpack(f"<{len(n.files[12]) // 2}H", n.files[12])
        assert len(lst) == 256 and lst[0] == 152, f"{a}: lista di Johto inattesa"
        new = [s for s in lst if s <= 251]
        assert [s for _, s in order] == new, "ordine di Johto incoerente tra a/1/3/8 e la lista"
        n.files[12] = bytearray(struct.pack(f"<{len(new)}H", *new))
        n.save()


def apply_code(c):
    for r in rows("codice.csv"):
        p = BUILD / r["file"]
        b = bytearray(p.read_bytes())
        if r["contesto"] == "FINE":   # codice aggiunto in coda a un overlay (senza bss: vedi NOTES)
            assert len(b) == int(r["posizione"]), f"{r['file']}: lunghezza {len(b)} inattesa"
            b += bytes.fromhex(r["a"])
            p.write_bytes(bytes(b))
            ov = int(re.search(r"ov(\d+)\.bin", r["file"]).group(1))
            y = (BUILD / "arm9_overlays/overlays.yaml").read_text()
            m = re.search(rf"(- id: {ov}\n(?:    .*\n)*?    code_size: )(\d+)", y)
            assert m and int(m.group(2)) == int(r["posizione"])
            assert re.search(rf"- id: {ov}\n(?:    .*\n)*?    bss_size: 0\n", y), "overlay con bss: non si può allungare"
            y = y[:m.start(2)] + str(len(b)) + y[m.end(2):]
            (BUILD / "arm9_overlays/overlays.yaml").write_text(y)
            c.log["codice"] += 1
            continue
        ctx = bytes.fromhex(r["contesto"])
        if b.count(ctx) != 1:
            raise SystemExit(f"codice.csv: contesto trovato {b.count(ctx)} volte in {r['file']}: {r['motivo']}")
        o = b.find(ctx) + int(r["posizione"])
        da, a = bytes.fromhex(r["da"]), bytes.fromhex(r["a"])
        assert b[o:o + len(da)] == da, r
        b[o:o + len(a)] = a
        p.write_bytes(bytes(b)); c.log["codice"] += 1


def apply_intro(c):
    """Scena 1 dell'intro: Ho-Oh poi Lugia (tools/intro.py) nei membri 23-26 di a/2/6/2."""
    import intro
    from gfx import maybe_lz, lz10_compress
    n = Narc(intro.NARC)
    dec, was_lz = [], []
    for f in n.files:
        d, lz = maybe_lz(bytes(f))
        dec.append(d); was_lz.append(lz)
    for i, data in intro.build(dec).items():
        n.files[i] = bytearray(lz10_compress(data) if was_lz[i] else data)
        c.log["intro (risorse)"] += 1
    n.save()


def apply_copies(c):
    narcs = {}
    for r in rows("copia_membri.csv"):
        n = narcs.setdefault(r["narc"], Narc(r["narc"]))
        n.files[int(r["destinazione"])] = bytearray(n.files[int(r["origine"])])
        c.log["membri copiati"] += 1
    for n in narcs.values():
        n.save()


def apply_title_logo(c):
    """Logo "Versione Crystal Soul" (tools/logo.py) al posto del logo SoulSilver (membro 1) di a/0/4/6;
    la mappa 0 è condivisa tra i loghi HG e SS: il titolo usa la versione SS (D31)."""
    import logo
    from gfx import maybe_lz
    n = Narc(logo.TITLE_NARC)
    g, glz = maybe_lz(bytes(n.files[logo.SS_LOGO]))
    s, slz = maybe_lz(bytes(n.files[logo.LOGO_SCR]))
    assert not glz and not slz, "logo compresso: non previsto"
    img, _ = logo.build_logo(base=SRC.name)
    ng, ns, ntiles = logo.encode(img, g, s)
    orig_tiles = len(logo.gfx.ncgr(g)[1])
    assert ntiles <= max(orig_tiles, 459), f"logo: {ntiles} tile, troppi (originale {orig_tiles})"
    n.files[logo.SS_LOGO] = bytearray(ng)
    n.files[3] = bytearray(ng)      # logo della variante Ho-Oh (HG): stesso logo, tavolozza copiata da copia_membri.csv
    n.files[logo.LOGO_SCR] = bytearray(ns)
    n.save()
    c.log["logo (tile)"] = ntiles


def apply_palettes(c):
    import colorsys
    from gfx import maybe_lz, _section
    narcs = {}
    for r in rows("tavolozze.csv"):
        n = narcs.setdefault(r["narc"], Narc(r["narc"]))
        src, lz = maybe_lz(bytes(n.files[int(r["origine"])]))
        assert not lz, "tavolozza compressa: non prevista"
        b = bytearray(src)
        o = _section(b, b"TTLP")
        size, off = struct.unpack_from("<II", b, o + 16)
        lo, hi, dh, light = float(r["tinta_min"]), float(r["tinta_max"]), float(r["tinta_delta"]), float(r["luce"])
        for k in range(o + 8 + off, o + 8 + off + size, 2):
            v = u16(b, k)
            rr, gg, bb = (v & 31) / 31, ((v >> 5) & 31) / 31, ((v >> 10) & 31) / 31
            h, s, vv = colorsys.rgb_to_hsv(rr, gg, bb)
            if s > 0.15 and lo <= h * 360 <= hi:
                h = ((h * 360 + dh) % 360) / 360
                vv = min(1.0, vv * light)
                rr, gg, bb = colorsys.hsv_to_rgb(h, s, vv)
                set16(b, k, round(rr * 31) | (round(gg * 31) << 5) | (round(bb * 31) << 10) | (v & 0x8000))
        n.files[int(r["membro"])] = b
        c.log["tavolozze"] += 1
    for n in narcs.values():
        n.save()


def apply_texts(c, lang="ITA"):
    import msg
    n = Narc(msg.MSG_NARC)
    for f in sorted((ROOT / "data" / "testi" / lang).glob("msg_*.csv")):
        idx = int(re.match(r"msg_(\d+)", f.stem).group(1))
        key, texts = msg.read_texts(bytes(n.files[idx]))
        with open(f, newline="", encoding="utf-8") as fh:
            for r in csv.DictReader(line for line in fh if not line.startswith("#")):
                texts[int(r["indice"])] = r["testo"]
                c.log["testi"] += 1
        n.files[idx] = bytearray(msg.write(key, texts))
    n.save()


def apply_banner(c):
    p = BUILD / "banner" / "banner.yaml"
    y = p.read_text(encoding="utf-8")
    for r in rows("banner.csv"):
        lines = r["titolo"].split("\\n")  # nel CSV "\n" (due caratteri) separa le righe
        block = f"  {r['lingua']}: |-\n" + "".join(f"    {ln}\n" for ln in lines)
        y, k = re.subn(rf"  {r['lingua']}: \|-\n(?:    .*\n)+", lambda _m: block, y)
        assert k == 1, r
        c.log["banner"] += 1
    p.write_text(y, encoding="utf-8")


# ------------------------------------------------------------------ verifica sui file costruiti
def verify(c):
    audit.ROM = BUILD / "files"
    checks = []
    left = collections.Counter()
    left["selvatici"] = sum(1 for m, cat, s, n in audit.read_wild(checks) if s > 251)
    left["bottintesta"] = sum(1 for m, g, s in audit.read_headbutt() if s > 251)
    left["safari"] = sum(1 for x in audit.read_safari(checks) if x[2] > 251)
    left["gara"] = sum(1 for t, s in audit.read_bug_contest() if s > 251)
    left["allenatori"] = sum(1 for *_, p in audit.read_trainers([]) for s, _ in p if s > 251)
    left["scambi"] = sum(1 for n, a, g in audit.read_trades() if a > 251 or g > 251)
    left["Parco Lotta"] = sum(k for d, cc in audit.read_frontier().values() for s, k in cc.items() if s > 251)
    evo = audit.read_evolutions()
    left["evoluzioni verso > 251"] = sum(1 for s in range(1, 252) for m, p, t in evo[s] if t > 251)
    dex = audit.read_johto_dex()
    left["Pokédex di Johto: specie > 251"] = sum(1 for s in dex if s > 251)
    left["Pokédex di Johto: numeri non 1..251"] = int(sorted(dex.values()) != list(range(1, 252)))
    left["evoluzioni solo con scambio"] = sum(1 for s in range(1, 252) for m, p, t in evo[s] if m in audit.EVO_IMPOSSIBLE_SOLO)
    audit.ROM = SRC / "files"
    return left


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # console Windows cp1252
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-rom", action="store_true")
    ap.add_argument("--base", default="IPKI", help="ROM di partenza: IPKI (ITA, default) o IPKE (USA)")
    args = ap.parse_args()
    global SRC, BUILD, NAME
    SRC = ROOT / "work" / args.base
    BUILD = ROOT / "work" / f"build_{args.base}" if args.base != "IPKI" else BUILD
    NAME = f"PokemonCrystalNew_{args.base}"
    audit.ROM = SRC / "files"
    lang = {"IPKI": "ITA", "IPKE": "ENG"}[args.base]
    if not SRC.exists():
        sys.exit(f"Manca {SRC.relative_to(ROOT)}: eseguire prima python tools/roundtrip.py {args.base}")
    if BUILD.exists():
        shutil.rmtree(BUILD)
    print(f"Copia {SRC.relative_to(ROOT)} → {BUILD.relative_to(ROOT)} ...")
    shutil.copytree(SRC, BUILD)

    c = Ctx()
    for step in (apply_evolutions, apply_wild, apply_simple, apply_trainers, apply_trades, apply_frontier, apply_items,
                 apply_map_objects, apply_scripts, apply_pokedex, apply_code, apply_intro, apply_copies, apply_title_logo, apply_palettes, apply_banner):
        step(c)
    apply_texts(c, lang)
    print("Modifiche:", ", ".join(f"{k} {v}" for k, v in c.log.items()))
    left = verify(c)
    print("Verifica sui file costruiti (specie > 251 rimaste):", dict(left))
    if any(left.values()):
        sys.exit("ERRORE: restano specie > 251 o evoluzioni per scambio")

    if args.no_rom:
        return
    from roundtrip import run_dsrom
    import bps
    OUT.mkdir(exist_ok=True)
    rom = OUT / f"{NAME}.nds"
    print(f"dsrom build → {rom.relative_to(ROOT)} ...")
    run_dsrom("build", "--config", str(BUILD / "config.yaml"), "--rom", str(rom))
    print("Patch BPS ...")
    patch = bps.create((ROOT / "work" / f"{args.base}_orig.nds").read_bytes(), rom.read_bytes())
    (OUT / f"{NAME}.bps").write_bytes(patch)
    print(f"{NAME}.bps: {len(patch)} byte")


if __name__ == "__main__":
    main()
