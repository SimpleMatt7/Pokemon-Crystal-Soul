"""Scarica in work/pret/ le parti necessarie della decompilazione pret/pokeheartgold (commit fissato).

Serve come *documentazione* dei dati: nomi di mappe/allenatori, script in chiaro, costanti.
Validità per la ROM ITA: gli archivi di dati (script compresi) di IPKI sono identici byte per byte
a quelli di IPKE (verificato 2026-09-29, vedi NOTES.md §5); differiscono solo testi e dati Pokédex.

Uso:  python tools/get_pret.py
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / "work" / "pret"
REPO = "https://github.com/pret/pokeheartgold.git"
COMMIT = "9d8b7591f09b65804da2fb2dfd56f320633e0d36"
SPARSE = [
    "include/constants",
    "files/fielddata/script",
    "files/fielddata/encountdata",
    "files/arc",
    "files/poketool/trainer",
    "files/data/mushi",
    "files/application/zukanlist/zkn_data",
    "files/fielddata/eventdata",           # eventi di zona: strumenti a terra (script 7000+)
    "files/itemtool/itemdata",             # item_data.csv (prezzi)
    "asm/macros",                          # script.inc: opcode e argomenti dei comandi di script
    "src",                                 # codice C: tabelle oggetti nascosti, negozi, Spaccaroccia, sciami, radio, gara
]


def git(*args, cwd=DEST):
    subprocess.run(["git", *args], cwd=cwd, check=True)


def main():
    if not (DEST / ".git").exists():
        DEST.parent.mkdir(parents=True, exist_ok=True)
        git("clone", "-q", "--filter=blob:none", "--no-checkout", REPO, str(DEST), cwd=ROOT)
        git("sparse-checkout", "init", "--cone")
    git("sparse-checkout", "set", *SPARSE)
    git("fetch", "-q", "origin", COMMIT)
    git("checkout", "-q", COMMIT)
    print(f"pret/pokeheartgold @ {COMMIT[:10]} in {DEST.relative_to(ROOT)}")


if __name__ == "__main__":
    sys.exit(main())
