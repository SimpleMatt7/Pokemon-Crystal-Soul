"""Fase 1: estrai -> ricostruisci -> confronta, sulla ROM base non modificata.

Uso:  python tools/roundtrip.py [CODICE_ROM]
Crea work/<CODICE>/ (estrazione dsrom) e out/roundtrip_<CODICE>.nds. Entrambe ignorate da git.
Esito atteso: ROM identica salvo i CRC dell'header (che dsrom/DSPRE non possono ricalcolare senza BIOS).
"""
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from get_tools import dsrom_path, get_dsrom  # noqa: E402
from roms import BASE, load_rom  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

# Campi header che possono legittimamente differire (offset, lunghezza, nome)
HEADER_FIELDS = [(0x15C, 2, "CRC logo"), (0x15E, 2, "CRC header"), (0x6C, 2, "CRC area sicura")]


def run_dsrom(*args):
    """Esegue dsrom mostrando il suo log (molto verboso) solo in caso di errore."""
    p = subprocess.run([str(dsrom_path()), *args], capture_output=True, text=True)
    if p.returncode != 0:
        sys.stderr.write(p.stdout + p.stderr)
        sys.exit(f"dsrom {args[0]} fallito (exit {p.returncode})")


def diff_ranges(a, b):
    ranges, start = [], None
    n = max(len(a), len(b))
    for i in range(n):
        same = i < len(a) and i < len(b) and a[i] == b[i]
        if not same and start is None:
            start = i
        elif same and start is not None:
            ranges.append((start, i))
            start = None
    if start is not None:
        ranges.append((start, n))
    return ranges


def field_name(off):
    for o, ln, name in HEADER_FIELDS:
        if o <= off < o + ln:
            return name
    return None


def main():
    code = sys.argv[1] if len(sys.argv) > 1 else BASE
    get_dsrom()
    rom = load_rom(code)
    work = ROOT / "work" / code
    out = ROOT / "out"
    out.mkdir(exist_ok=True)
    src = ROOT / "work" / f"{code}_orig.nds"
    src.parent.mkdir(exist_ok=True)
    src.write_bytes(rom)
    if work.exists():
        shutil.rmtree(work)

    print(f"Estrazione in {work.relative_to(ROOT)} ...")
    run_dsrom("extract", "--rom", str(src), "--path", str(work))
    rebuilt = out / f"roundtrip_{code}.nds"
    print(f"Ricostruzione in {rebuilt.relative_to(ROOT)} ...")
    run_dsrom("build", "--config", str(work / "config.yaml"), "--rom", str(rebuilt))

    new = rebuilt.read_bytes()
    print(f"\noriginale {len(rom)} byte, ricostruita {len(new)} byte")
    ranges = diff_ranges(rom, new)
    if not ranges:
        print("IDENTICHE byte per byte.")
        return 0
    unexpected = 0
    total = sum(e - s for s, e in ranges)
    print(f"{len(ranges)} intervalli diversi, {total} byte in totale:")
    for s, e in ranges[:40]:
        name = field_name(s)
        if not name:
            unexpected += 1
        print(f"  0x{s:08X}-0x{e:08X} ({e - s} byte){'  [' + name + ']' if name else ''}")
    if len(ranges) > 40:
        print(f"  ... altri {len(ranges) - 40}")
    print("ESITO:", "OK (solo CRC header)" if unexpected == 0 else f"{unexpected} differenze inattese: da analizzare")
    return 0 if unexpected == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
