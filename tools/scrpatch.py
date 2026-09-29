"""Modifiche agli script di campo come patch testuali (diff unificati) sui sorgenti .s della decomp.

Nel repository stanno solo le differenze (`data/scripts/scr_seq_NNNN.diff`), non gli script interi.
Flusso di lavoro:
  python tools/scrpatch.py apri 0133      copia scr_seq_0133*.s (con la patch esistente) in work/script_edit/
  (modificare il file in work/script_edit/)
  python tools/scrpatch.py salva          riscrive data/scripts/*.diff per i file in work/script_edit/ e li assembla
  python tools/scrpatch.py verifica       applica tutte le patch e le assembla (errori di sintassi, etichette...)
Da codice: patched_scripts() → {indice NARC: bytes assemblati}.
"""
import difflib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import scrasm  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
PATCHES = ROOT / "data" / "scripts"
EDIT = ROOT / "work" / "script_edit"


def source(idx):
    m = sorted(scrasm.SCR.glob(f"scr_seq_{idx:04d}*.s"))
    m = [p for p in m if scrasm.script_index(p) == idx]
    if len(m) != 1:
        raise SystemExit(f"script {idx}: trovati {len(m)} sorgenti")
    return m[0]


def apply_diff(text, diff):
    """Applica un diff unificato (contesto verificato esattamente) a `text`."""
    src = text.splitlines()
    out, pos = [], 0
    lines = diff.splitlines()
    i = 0
    while i < len(lines) and not lines[i].startswith("@@"):
        i += 1
    while i < len(lines):
        m = re.match(r"@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@", lines[i])
        if not m:
            raise ValueError(f"riga di hunk non valida: {lines[i]}")
        start = int(m.group(1)) - (0 if m.group(2) == "0" else 1)
        out += src[pos:start]
        pos = start
        i += 1
        while i < len(lines) and not lines[i].startswith("@@"):
            ln = lines[i]
            tag, body = ln[:1], ln[1:]
            if tag in (" ", "-"):
                if pos >= len(src) or src[pos] != body:
                    raise ValueError(f"contesto diverso alla riga {pos + 1}: atteso {body!r}, trovato "
                                     f"{src[pos] if pos < len(src) else 'EOF'!r}")
                if tag == " ":
                    out.append(body)
                pos += 1
            elif tag == "+":
                out.append(body)
            elif ln.startswith("\\"):
                pass
            i += 1
    out += src[pos:]
    return "\n".join(out) + "\n"


def patched_text(idx):
    text = source(idx).read_text(errors="replace")
    d = PATCHES / f"scr_seq_{idx:04d}.diff"
    return apply_diff(text, d.read_text(encoding="utf-8")) if d.exists() else text


def patched_scripts():
    out = {}
    for d in sorted(PATCHES.glob("scr_seq_*.diff")):
        idx = int(re.match(r"scr_seq_(\d+)", d.stem).group(1))
        out[idx] = scrasm.assemble(patched_text(idx), f"scr_seq_{idx:04d} (patch)")
    return out


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    cmd = sys.argv[1]
    if cmd == "apri":
        EDIT.mkdir(parents=True, exist_ok=True)
        for a in sys.argv[2:]:
            idx = int(a)
            dst = EDIT / source(idx).name
            dst.write_text(patched_text(idx), encoding="utf-8")
            print(f"{dst.relative_to(ROOT)}")
    elif cmd == "salva":
        PATCHES.mkdir(parents=True, exist_ok=True)
        for p in sorted(EDIT.glob("scr_seq_*.s")):
            idx = scrasm.script_index(p)
            orig = source(idx).read_text(errors="replace").splitlines()
            new = p.read_text(encoding="utf-8").splitlines()
            scrasm.assemble("\n".join(new), p.name)  # errore subito se non si assembla
            diff = list(difflib.unified_diff(orig, new, f"a/{p.name}", f"b/{p.name}", n=2, lineterm=""))
            dst = PATCHES / f"scr_seq_{idx:04d}.diff"
            if diff:
                dst.write_text("\n".join(diff) + "\n", encoding="utf-8")
                print(f"{dst.relative_to(ROOT)}: {sum(1 for x in diff if x[:1] in '+-') - 2} righe cambiate")
            elif dst.exists():
                dst.unlink()
                print(f"{dst.relative_to(ROOT)}: rimosso (nessuna differenza)")
    elif cmd == "verifica":
        for idx, b in patched_scripts().items():
            print(f"scr_seq_{idx:04d}: {len(b)} byte")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
