"""Scarica i tool esterni a versione fissata, verificandone lo SHA256, in tools/bin/.

Uso:  python tools/get_tools.py
I binari non vanno nel repository: si riscaricano sempre da qui (stessa versione, stesso hash).
"""
import hashlib
import os
import platform
import stat
import sys
import urllib.request
from pathlib import Path

BIN = Path(__file__).resolve().parent / "bin"

# ds-rom (MIT) — https://github.com/AetiasHax/ds-rom
DSROM_VERSION = "v0.8.0"
DSROM = {
    ("Windows", "AMD64"): ("dsrom-windows-x86_64.exe", "38c1e5f8bf4663bdf6ce7c896283ee7049909b236da57f49c55950c2515458d7"),
    ("Linux", "x86_64"): ("dsrom-linux-x86_64", "b12e3c594a880c5399d659bbc5e4148e33b63696a6b168a7645fd069466c1b3e"),
}


def dsrom_path():
    return BIN / ("dsrom.exe" if os.name == "nt" else "dsrom")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def get_dsrom():
    key = (platform.system(), platform.machine())
    if key not in DSROM and dsrom_path().exists():
        print(f"dsrom compilato localmente (nessun hash di riferimento per {key}): {dsrom_path()}")
        return dsrom_path()
    if key not in DSROM:
        sys.exit(f"Nessun binario dsrom per {key}: compilarlo con cargo (vedi docs/SETUP.md) "
                 f"e copiarlo in {dsrom_path()}")
    asset, want = DSROM[key]
    dest = dsrom_path()
    if dest.exists() and sha256(dest) == want:
        print(f"dsrom {DSROM_VERSION} già presente e verificato: {dest}")
        return dest
    BIN.mkdir(parents=True, exist_ok=True)
    url = f"https://github.com/AetiasHax/ds-rom/releases/download/{DSROM_VERSION}/{asset}"
    tmp = dest.with_suffix(".part")
    print(f"Scarico {url}")
    urllib.request.urlretrieve(url, tmp)
    got = sha256(tmp)
    if got != want:
        tmp.unlink()
        sys.exit(f"SHA256 non corrisponde!\n atteso {want}\n ottenuto {got}")
    tmp.replace(dest)
    dest.chmod(dest.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    print(f"OK: {dest} (sha256 verificato)")
    return dest


if __name__ == "__main__":
    get_dsrom()
