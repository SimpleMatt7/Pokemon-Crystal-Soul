"""Individua e verifica le ROM di partenza in roms/ (.nds sciolti o dentro .zip).

Uso:  python tools/roms.py            -> elenca le ROM trovate e il loro stato
      from roms import load_rom; data = load_rom("IPKI")
"""
import hashlib
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ROM_DIR = ROOT / "roms"

# SHA1 dei dump verificati (vedi NOTES.md, sezione "ROM di riferimento")
KNOWN = {
    "IPKI": ("Oro HeartGold (ITA)", "6b7f9bff57eb58bc8d6e48e9e5c370719458c721"),
    "IPGI": ("Argento SoulSilver (ITA)", "e137acf711e0b14c297abf0254e5b4a9263338e7"),
    "IPKE": ("HeartGold (USA)", "4fcded0e2713dc03929845de631d0932ea2b5a37"),
    "IPGE": ("SoulSilver (USA)", "f8dc38ea20c17541a43b58c5e6d18c1732c7e582"),
}
BASE = "IPKI"  # ROM su cui lavora il progetto


def _candidates():
    for p in sorted(ROM_DIR.glob("*")):
        if p.suffix.lower() == ".nds":
            yield p, lambda p=p: p.read_bytes()
        elif p.suffix.lower() == ".zip":
            with zipfile.ZipFile(p) as zf:
                for info in zf.infolist():
                    if info.filename.lower().endswith(".nds"):
                        yield p, lambda p=p, n=info.filename: zipfile.ZipFile(p).read(n)


def find_all():
    """Ritorna {codice: (path, sha1, ok)} per ogni ROM trovata."""
    found = {}
    for path, reader in _candidates():
        data = reader()
        code = data[12:16].decode("ascii", "replace")
        sha1 = hashlib.sha1(data).hexdigest()
        ok = code in KNOWN and KNOWN[code][1] == sha1
        if code not in found or (ok and not found[code][2]):
            found[code] = (path, sha1, ok)
    return found


def load_rom(code=BASE):
    """Legge in memoria la ROM con quel codice, verificandone lo SHA1."""
    for path, reader in _candidates():
        data = reader()
        if data[12:16].decode("ascii", "replace") != code:
            continue
        if hashlib.sha1(data).hexdigest() == KNOWN[code][1]:
            return data
    raise SystemExit(f"ROM {code} ({KNOWN[code][0]}) con SHA1 {KNOWN[code][1]} non trovata in {ROM_DIR}")


if __name__ == "__main__":
    found = find_all()
    for code, (name, sha1) in KNOWN.items():
        if code in found:
            path, got, ok = found[code]
            print(f"{code}  {'OK ' if ok else 'HASH DIVERSO'}  {name:26} {path.name}")
        else:
            print(f"{code}  MANCANTE  {name}")
    sys.exit(0 if found.get(BASE, (0, 0, False))[2] else 1)
