"""Verifica delle nature neutre (D49) su un salvataggio: per ogni Pokémon in squadra confronta le statistiche salvate
dal gioco con quelle calcolate da specie, livello, IV ed EV, con e senza l'effetto della natura.

Formato (salvataggio HGSS, come in PKHeX / decomp pret): due copie da 0x40000 byte; blocco generale da 0xF628 byte con
contatore di salvataggio nel piè di pagina; squadra a 0x94 (numero) e 0x98 (6 x 236 byte). Ogni Pokémon: PID, 4 blocchi
da 32 byte cifrati (seme = checksum) e mescolati (ordine da PID), statistiche di lotta cifrate (seme = PID).
Statistiche base dalla ROM estratta (a/0/0/2, personal).

Uso:  python tools/verifica_nature.py FILE.sav [--base IPKI|IPKE]
"""
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ndsfs import parse_narc  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
GENERAL_SIZE = 0xF628
ORDERS = ["ABCD", "ABDC", "ACBD", "ACDB", "ADBC", "ADCB", "BACD", "BADC", "BCAD", "BCDA", "BDAC", "BDCA",
          "CABD", "CADB", "CBAD", "CBDA", "CDAB", "CDBA", "DABC", "DACB", "DBAC", "DBCA", "DCAB", "DCBA"]
NATURES = ["Ardita", "Schiva", "Audace", "Decisa", "Birbona", "Sicura", "Docile", "Placida", "Scaltra", "Fiacca",
           "Timida", "Lesta", "Seria", "Allegra", "Ingenua", "Modesta", "Mite", "Quieta", "Ritrosa", "Ardente",
           "Calma", "Gentile", "Vivace", "Cauta", "Furba"]
# natura → (statistica +10%, statistica -10%) con indici Att, Dif, Vel, AtSp, DiSp (ordine di gNatureStatMods)
STAT_NAMES = ["PS", "Att", "Dif", "Vel", "AtSp", "DiSp"]


def prng(seed, words):
    out = []
    for w in words:
        seed = (seed * 0x41C64E6D + 0x6073) & 0xFFFFFFFF
        out.append(w ^ (seed >> 16))
    return out


def decode_mon(raw):
    pid, _, checksum = struct.unpack_from("<IHH", raw, 0)
    data = prng(checksum, struct.unpack_from("<64H", raw, 8))
    b = struct.pack("<64H", *data)
    order = ORDERS[((pid >> 13) & 0x1F) % 24]
    blocks = {order[i]: b[i * 32:(i + 1) * 32] for i in range(4)}
    if sum(data) & 0xFFFF != checksum:
        return None
    battle = struct.pack("<50H", *prng(pid, struct.unpack_from("<50H", raw, 136)))
    species = struct.unpack_from("<H", blocks["A"], 0)[0]
    evs = list(blocks["A"][0x10:0x16])
    ivword = struct.unpack_from("<I", blocks["B"], 0x10)[0]
    ivs = [(ivword >> (5 * i)) & 31 for i in range(6)]
    is_egg = (ivword >> 30) & 1
    level = battle[4]
    stats = list(struct.unpack_from("<6H", battle, 8))   # PS max, Att, Dif, Vel, AtSp, DiSp
    return dict(pid=pid, species=species, level=level, evs=evs, ivs=ivs, egg=is_egg, stats=stats, nature=pid % 25)


def expected(base, ivs, evs, level, nature, with_nature):
    # ordine interno IV/EV: PS, Att, Dif, Vel, AtSp, DiSp; base personal: PS, Att, Dif, Vel, AtSp, DiSp
    out = [((2 * base[0] + ivs[0] + evs[0] // 4) * level) // 100 + level + 10]
    up, down = nature // 5, nature % 5          # gNatureStatMods: riga = natura, +1 su nature//5, -1 su nature%5
    for i in range(1, 6):
        v = ((2 * base[i] + ivs[i] + evs[i] // 4) * level) // 100 + 5
        if with_nature and up != down:
            if i - 1 == up:
                v = v * 110 // 100
            elif i - 1 == down:
                v = v * 90 // 100
        out.append(v)
    return out


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    args = [a for a in sys.argv[1:]]
    base_rom = "IPKI"
    if "--base" in args:
        i = args.index("--base"); base_rom = args[i + 1]; del args[i:i + 2]
    if len(args) != 1:
        sys.exit(__doc__)
    sav = Path(args[0]).read_bytes()
    copies = []
    for off in (0, 0x40000):
        gen = sav[off:off + GENERAL_SIZE]
        counter, size, magic = struct.unpack_from("<III", gen, GENERAL_SIZE - 0x10)
        if size == GENERAL_SIZE and magic == 0x20060623:      # copia valida (piè di pagina HGSS)
            copies.append((counter, gen))
    if not copies:
        sys.exit("Nessuna copia valida nel salvataggio (è di HeartGold/SoulSilver?)")
    counter, gen = max(copies, key=lambda c: c[0])
    personal = parse_narc((ROOT / "work" / base_rom / "files" / "a/0/0/2").read_bytes())
    n = struct.unpack_from("<I", gen, 0x94)[0]
    print(f"Copia del salvataggio con contatore {counter}; Pokémon in squadra: {n}")
    for k in range(min(n, 6)):
        m = decode_mon(gen[0x98 + k * 236:0x98 + (k + 1) * 236])
        if m is None:
            print(f"  {k + 1}: checksum non valido (salvataggio letto male?)")
            continue
        if m["egg"]:
            print(f"  {k + 1}: uovo, salto")
            continue
        base = list(personal[m["species"]][:6])
        neutral = expected(base, m["ivs"], m["evs"], m["level"], m["nature"], False)
        natured = expected(base, m["ivs"], m["evs"], m["level"], m["nature"], True)
        up, down = m["nature"] // 5, m["nature"] % 5
        effetto = "neutra di suo" if up == down else f"+{STAT_NAMES[up + 1]} -{STAT_NAMES[down + 1]}"
        if m["stats"] == neutral and neutral != natured:
            verdict = "SENZA effetto della natura (patch attiva)"
        elif m["stats"] == natured and neutral != natured:
            verdict = "CON effetto della natura (statistiche calcolate prima della patch?)"
        elif m["stats"] == neutral:
            verdict = "natura neutra di suo: non dice niente"
        else:
            verdict = "non corrisponde a nessuno dei due calcoli"
        print(f"  {k + 1}: specie {m['species']} lv {m['level']}, natura {NATURES[m['nature']]} ({effetto})")
        print(f"      salvate {m['stats']}  senza natura {neutral}  con natura {natured}  → {verdict}")


if __name__ == "__main__":
    main()
