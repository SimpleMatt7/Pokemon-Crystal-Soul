"""Assemblatore degli script di campo (a/0/1/2) dai sorgenti .s della decomp pret, solo libreria standard.

Riproduce quello che fa la toolchain della decomp (cpp + mwasmarm + objcopy) per il sottoinsieme usato dagli script:
macro di asm/macros/script.inc e movement.inc (parametri con default, .if/.else/.endif, .set, macro annidate),
direttive .byte/.short/.word/.long/.balign, etichette, #include/#define del preprocessore C per le costanti.
Due passate: la prima calcola gli indirizzi delle etichette, la seconda emette i byte.

Collaudo: `python tools/scrasm.py --verifica` riassembla tutti gli script e li confronta byte per byte con
la ROM IPKI (a/0/1/2). Uso da codice: assemble(path_or_text, name) → bytes.
"""
import re
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRET = ROOT / "work" / "pret"
SCR = PRET / "files/fielddata/script/scr_seq"


class AsmError(Exception):
    pass


# ------------------------------------------------------------------ costanti C
_CAST = re.compile(r"\(\s*(?:u8|u16|u32|s8|s16|s32|int|unsigned|signed)\s*\)")


class Symbols:
    def __init__(self):
        self.raw = {}      # nome → testo dell'espressione
        self.val = {}      # nome → valore calcolato
        self.funcs = {"GX_RGB": (["r", "g", "b"], "((r) | ((g) << 5) | ((b) << 10))")}  # macro a funzione
        self.loaded = set()

    def load_header(self, path):
        path = Path(path)
        if path in self.loaded or not path.exists():
            return
        self.loaded.add(path)
        text = path.read_text(errors="replace")
        text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
        text = re.sub(r"//[^\n]*", "", text)
        for inc in re.findall(r'#include\s+"([^"]+)"', text):
            for base in (PRET / "include", PRET / "files", PRET, path.parent):
                if (base / inc).exists():
                    self.load_header(base / inc)
                    break
        for m in re.finditer(r"^[ \t]*#define[ \t]+(\w+)\(([^)]*)\)[ \t]*(.*)$", text, re.M):
            self.funcs.setdefault(m.group(1), ([a.strip() for a in m.group(2).split(",")], m.group(3).strip()))
        for m in re.finditer(r"^[ \t]*#define[ \t]+(\w+)(?![\w(])[ \t]*(.*)$", text, re.M):
            if m.group(2).strip():
                self.raw.setdefault(m.group(1), m.group(2).strip())
        for m in re.finditer(r"enum\s*\w*\s*\{(.*?)\}", text, re.S):
            cur = -1
            for item in m.group(1).split(","):
                item = item.strip()
                if not item:
                    continue
                if "=" in item:
                    name, expr = (x.strip() for x in item.split("=", 1))
                    self.raw.setdefault(name, expr)
                    try:
                        cur = self.get(name)
                    except AsmError:
                        cur = None
                else:
                    name = item
                    if cur is None:
                        continue
                    cur += 1
                    self.raw.setdefault(name, str(cur))

    def expand(self, expr, depth=0):
        """Espande le macro a funzione del preprocessore C (es. RGB(0, 0, 0), MAPLOC(x))."""
        for name, (params, body) in self.funcs.items():
            pat = re.compile(r"(?<![\w.])" + name + r"\s*\(")
            pos = 0
            while True:
                m = pat.search(expr, pos)
                if not m:
                    break
                k, lvl = m.end(), 1
                while lvl:
                    lvl += {"(": 1, ")": -1}.get(expr[k], 0)
                    k += 1
                body2 = body
                for pn, av in zip(params, split_args(expr[m.end():k - 1])):
                    body2 = re.sub(r"(?<!\w)" + pn + r"(?!\w)", lambda _m, av=av: "(" + av + ")", body2)
                expr = expr[:m.start()] + "(" + body2 + ")" + expr[k:]
                pos = m.start()
        if depth < 5 and any(re.search(r"(?<![\w.])" + n + r"\s*\(", expr) for n in self.funcs):
            return self.expand(expr, depth + 1)
        return expr

    def get(self, name, depth=0):
        if name in self.val:
            return self.val[name]
        if name not in self.raw or depth > 50:
            raise AsmError(f"simbolo sconosciuto: {name}")
        v = evaluate(_CAST.sub("", self.expand(self.raw[name])), lambda n: self.get(n, depth + 1))
        self.val[name] = v
        return v


_TOKEN = re.compile(r"\s*(0[xX][0-9a-fA-F]+|\d+|'.'|[A-Za-z_.$][\w.$]*|<<|>>|<=|>=|==|!=|&&|\|\||[-+*/%()&|^~!<>?:])")


def evaluate(expr, lookup):
    """Valuta un'espressione intera in sintassi C/GAS. lookup(nome) → valore."""
    toks, pos = [], 0
    expr = expr.strip()
    while pos < len(expr):
        m = _TOKEN.match(expr, pos)
        if not m:
            raise AsmError(f"espressione non valida: {expr!r}")
        toks.append(m.group(1))
        pos = m.end()
    out = []
    for t in toks:
        if re.fullmatch(r"0[xX][0-9a-fA-F]+|\d+", t):
            out.append(str(int(t, 0)))
        elif t.startswith("'"):
            out.append(str(ord(t[1])))
        elif re.fullmatch(r"[A-Za-z_.$][\w.$]*", t):
            if t in ("TRUE", "FALSE") and False:
                pass
            out.append(str(lookup(t)))
        else:
            out.append({"&&": " and ", "||": " or ", "!": " not ", "/": "//"}.get(t, t))
    py = " ".join(out).replace("not  =", "!=")
    try:
        v = eval(py, {"__builtins__": {}}, {})
    except Exception as e:  # noqa: BLE001
        raise AsmError(f"espressione {expr!r}: {e}")
    return int(v)


# ------------------------------------------------------------------ macro
class Macro:
    def __init__(self, name, params, body):
        self.name, self.body = name, body
        self.params = []  # (nome, default)
        for p in [p.strip() for p in params.split(",") if p.strip()]:
            if "=" in p:
                n, d = p.split("=", 1)
                self.params.append((n.strip(), d.strip()))
            else:
                self.params.append((p.split(":")[0], None))


def strip_comment(line):
    line = re.sub(r"/\*.*?\*/", "", line)
    for c in ("@", "//"):
        # i commenti non compaiono dentro stringhe negli script, tranne .error "..."
        if c in line and '"' not in line:
            line = line.split(c, 1)[0]
    if ";" in line and '"' not in line:
        line = line.split(";", 1)[0]
    return line.rstrip()


def load_macros(path, macros, syms):
    lines = Path(path).read_text(errors="replace").splitlines()
    text = re.sub(r"/\*.*?\*/", "", "\n".join(lines), flags=re.S).splitlines()
    i = 0
    while i < len(text):
        ln = strip_comment(text[i]).strip()
        m = re.match(r"\.macro\s+(\w+)\s*(.*)$", ln)
        if m:
            body = []
            i += 1
            while not strip_comment(text[i]).strip().startswith(".endm"):
                body.append(strip_comment(text[i]))
                i += 1
            macros[m.group(1)] = Macro(m.group(1), m.group(2), body)
        else:
            inc = re.match(r'#include\s+"([^"]+)"', ln)
            if inc:
                for base in (PRET / "include", PRET / "asm", PRET):
                    if (base / inc.group(1)).exists():
                        if inc.group(1).endswith(".inc"):
                            load_macros(base / inc.group(1), macros, syms)
                        else:
                            syms.load_header(base / inc.group(1))
                        break
            s = re.match(r"\.set\s+(\w+)\s*,\s*(.+)$", ln)
            if s:
                syms.raw[s.group(1)] = s.group(2)
        i += 1


_BASE = None


def base_env():
    global _BASE
    if _BASE is None:
        syms = Symbols()
        syms.raw.update({"TRUE": "1", "FALSE": "0"})
        syms.load_header(PRET / "include/constants/scrcmd.h")
        syms.load_header(PRET / "include/constants/events.h")
        for h in sorted((PRET / "include/constants").glob("*.h")):  # es. gx.h (RGB) non incluso da scrcmd.h
            syms.load_header(h)
        macros = {}
        load_macros(PRET / "asm/macros/script.inc", macros, syms)
        _BASE = (syms, macros)
    return _BASE


# ------------------------------------------------------------------ assemblatore
class Assembler:
    def __init__(self, text, name="script"):
        base_syms, self.macros = base_env()
        self.syms = Symbols()
        self.syms.raw = dict(base_syms.raw)
        self.syms.funcs = dict(base_syms.funcs)
        self.syms.loaded = set(base_syms.loaded)
        self.name = name
        self.lines = []
        for ln in text.splitlines():
            inc = re.match(r'\s*#include\s+"([^"]+)"', ln)
            if inc:
                p = inc.group(1)
                for base in (PRET / "include", PRET / "files", PRET):
                    if (base / p).exists():
                        self.syms.load_header(base / p)
                        break
                continue
            d = re.match(r"\s*#define\s+(\w+)\s+(.+)$", ln)
            if d:
                self.syms.raw[d.group(1)] = d.group(2).strip()
                continue
            self.lines.append(ln)

    def lookup(self, name):
        if name == ".":
            return self.pc
        if name in self.labels:
            return self.labels[name]
        if name in self.local_set:
            return self.local_set[name]
        try:
            return self.syms.get(name)
        except AsmError:
            m = re.fullmatch(r"msg_\d+(?:_\w+?)?_(\d+)", name)
            if m:
                return int(m.group(1))
            m = re.fullmatch(r"msg_(\d{4})_\w+", name)
            if m and name in gmm_index(m.group(1)):
                return gmm_index(m.group(1))[name]
            if self.first_pass:
                self.unresolved.add(name)
                return 0
            raise

    def ev(self, expr):
        return evaluate(self.syms.expand(expr), self.lookup)

    def emit(self, size, value):
        if not self.first_pass:
            self.out += (value & ((1 << (8 * size)) - 1)).to_bytes(size, "little")
        self.pc += size

    def run_lines(self, lines, depth=0):
        stack = []  # per .if: (attivo_prima, preso, attivo)
        active = True
        for raw in lines:
            ln = strip_comment(raw).strip()
            if not ln:
                continue
            if ln.startswith((".ifndef", ".ifdef")):
                stack.append((active, True)); continue
            m = re.match(r"\.if\s+(.+)$", ln)
            if m:
                cond = active and bool(self.ev(m.group(1)))
                stack.append((active, cond)); active = cond; continue
            if ln.startswith(".else"):
                outer, taken = stack[-1]
                active = outer and not taken
                stack[-1] = (outer, True); continue
            if ln.startswith(".endif"):
                active = stack.pop()[0]; continue
            if not active:
                continue
            while True:
                m = re.match(r"([A-Za-z_.$][\w.$]*):\s*(.*)$", ln)
                if not m:
                    break
                if self.first_pass:
                    if m.group(1) in self.labels:
                        raise AsmError(f"etichetta doppia {m.group(1)}")
                    self.labels[m.group(1)] = self.pc
                ln = m.group(2).strip()
            if not ln:
                continue
            self.statement(ln, depth)

    def statement(self, ln, depth):
        parts = ln.split(None, 1)
        op, args = parts[0], (parts[1] if len(parts) > 1 else "")
        if op in (".byte", ".short", ".hword", ".2byte", ".word", ".long", ".4byte"):
            size = {".byte": 1, ".short": 2, ".hword": 2, ".2byte": 2}.get(op, 4)
            for a in split_args(args):
                self.emit(size, self.ev(a))
        elif op == ".balign":
            a = split_args(args)
            n = self.ev(a[0])
            fill = self.ev(a[1]) if len(a) > 1 else 0
            while self.pc % n:
                self.emit(1, fill)
        elif op == ".set":
            name, expr = (x.strip() for x in args.split(",", 1))
            self.local_set[name] = self.ev(expr)
        elif op == ".error":
            raise AsmError(f"{self.name}: .error {args}")
        elif op in (".include", ".rodata", ".text", ".data", ".option", ".global", ".public", ".align"):
            pass
        elif op in self.macros:
            if depth > 30:
                raise AsmError("macro annidate troppo in profondità")
            mac = self.macros[op]
            vals = split_args(args)
            body = []
            subst = {}
            for k, (pn, default) in enumerate(mac.params):
                v = vals[k] if k < len(vals) and vals[k] != "" else default
                if v is None:
                    raise AsmError(f"{self.name}: {op}: manca il parametro {pn}")
                subst[pn] = v
            for b in mac.body:
                for pn in sorted(subst, key=len, reverse=True):
                    b = re.sub(r"\\" + pn + r"(?!\w)", lambda _m, v=subst[pn]: "(" + v + ")" if re.search(r"[-+*/&|<>]", v) else v, b)
                body.append(b)
            self.run_lines(body, depth + 1)
        else:
            raise AsmError(f"{self.name}: istruzione sconosciuta: {ln}")

    def assemble(self):
        self.labels = {}
        for self.first_pass in (True, False):
            self.pc, self.out, self.local_set, self.unresolved = 0, bytearray(), {}, set()
            self.run_lines(self.lines)
        return bytes(self.out)


_GMM = {}


def gmm_index(num):
    """{id: indice} dei messaggi di files/msgdata/msg/msg_NNNN.gmm (letto con git dalla decomp, senza checkout)."""
    if num not in _GMM:
        import subprocess
        p = subprocess.run(["git", "show", f"HEAD:files/msgdata/msg/msg_{num}.gmm"], cwd=PRET,
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        _GMM[num] = {m.group(1): int(m.group(2)) for m in re.finditer(r'<row id="(\w+)" index="(\d+)"', p.stdout)}
    return _GMM[num]


def split_args(s):
    out, depth, cur = [], 0, ""
    for ch in s:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == "," and depth == 0:
            out.append(cur.strip()); cur = ""
        else:
            cur += ch
    if cur.strip() or out:
        out.append(cur.strip())
    return out


def assemble(src, name=None):
    text = Path(src).read_text(errors="replace") if isinstance(src, Path) else src
    return Assembler(text, name or (src.name if isinstance(src, Path) else "script")).assemble()


def script_index(path):
    return int(re.match(r"scr_seq_(\d+)", Path(path).stem).group(1))


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if "--verifica" not in sys.argv:
        sys.exit(__doc__)
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from ndsfs import parse_narc
    rom = parse_narc((ROOT / "work/IPKI/files/a/0/1/2").read_bytes())
    ok, bad = 0, []
    for p in sorted(SCR.glob("scr_seq_*.s")):
        i = script_index(p)
        try:
            b = assemble(p)
        except AsmError as e:
            bad.append((p.name, str(e))); continue
        ref = rom[i]
        if b == ref or (b.rstrip(b"\0") == ref.rstrip(b"\0") and abs(len(b) - len(ref)) < 4):
            ok += 1
        else:
            k = next((j for j in range(min(len(b), len(ref))) if b[j] != ref[j]), min(len(b), len(ref)))
            bad.append((p.name, f"diverso da 0x{k:X} (nostro {len(b)} B, ROM {len(ref)} B)"))
    print(f"Identici alla ROM: {ok}/{ok + len(bad)}")
    for n, e in bad[:30]:
        print(f"  {n}: {e}")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
