"""Testi del gioco (archivio messaggi a/0/2/7): lettura e scrittura, solo libreria standard.

Formato (da tools/msgenc della decomp pret): intestazione u16 numero, u16 chiave; tabella (offset, lunghezza)
cifrata con (765 * i * chiave); caratteri u16 cifrati con chiave i * 596947, +18749 a ogni carattere (i da 1).
Caratteri e comandi dalla charmap.txt della decomp ({STRVAR_1 3, 0, 0}, \\n a capo, \\r nuova finestra,
\\f scorrimento). I nomi degli allenatori compressi (F100) si leggono ma non si riscrivono (non servono).

Uso:  python tools/msg.py mostra 537 [indice ...]     stampa i testi di un file (ROM ITA estratta; --base IPKE = USA)
      python tools/msg.py verifica                    decodifica e ricodifica tutti i file: devono restare identici
Da codice: read(bytes) → (chiave, [testi]); write(chiave, [testi]) → bytes.
"""
import re
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ndsfs import parse_narc  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
PRET = ROOT / "work" / "pret"
MSG_NARC = "a/0/2/7"

_CHAR, _CODE, _CMD, _CMDCODE, _STRVAR = {}, {}, {}, {}, set()


def _load_charmap():
    if _CHAR:
        return
    for ln in (PRET / "charmap.txt").read_text(encoding="utf-8").splitlines():
        if ln.startswith("//") or "=" not in ln:
            continue
        code, ch = ln.split("=", 1)
        code = int(code.strip(), 16)
        if ch.startswith("{") and ch.endswith("}"):
            name = ch[1:-1]
            _CMD[code] = name
            _CMDCODE[name] = code
            if name.startswith("STRVAR_"):
                _STRVAR.add(code)
            continue
        if ch == "\\x0000":
            continue
        _CHAR[code] = ch
        _CODE.setdefault(ch, code)


def _crypt_str(codes, i):
    key = (i * 596947) & 0xFFFF
    out = []
    for c in codes:
        out.append(c ^ key)
        key = (key + 18749) & 0xFFFF
    return out


def decode(codes):
    _load_charmap()
    s, j = [], 0
    while j < len(codes):
        c = codes[j]
        if c == 0xFFFF:
            break
        if c == 0xFFFE:
            cmd, n = codes[j + 1], codes[j + 2]
            args = list(codes[j + 3:j + 3 + n])
            if (cmd & 0xFF00) in _STRVAR:
                name = f"STRVAR_{cmd >> 8:X}"
                s.append("{" + name + " " + ", ".join(str(a) for a in [cmd & 0xFF] + args) + "}")
            else:
                name = _CMD.get(cmd, f"CMD_{cmd:04X}")
                s.append("{" + name + ("" if not args else " " + ", ".join(str(a) for a in args)) + "}")
            j += 3 + n
            continue
        if c == 0xF100:
            return "{TRNAME_RAW " + " ".join(f"{x:04X}" for x in codes[j:]) + "}"
        ch = _CHAR.get(c)
        s.append(ch if ch is not None else f"{{CHAR_{c:04X}}}")
        j += 1
    return "".join(s)


def encode(text):
    _load_charmap()
    out, k = [], 0
    if text.startswith("{TRNAME_RAW "):
        return [int(x, 16) for x in text[12:-1].split()]
    while k < len(text):
        if text[k] == "{":
            e = text.index("}", k)
            body = text[k + 1:e]
            name, _, rest = body.partition(" ")
            args = [int(a) for a in rest.replace(",", " ").split()] if rest.strip() else []
            if name.startswith("CHAR_"):
                out.append(int(name[5:], 16))
            elif name.startswith("STRVAR_"):
                out += [0xFFFE, (int(name[7:], 16) << 8) | args[0], len(args) - 1] + args[1:]
            else:
                code = _CMDCODE[name] if name in _CMDCODE else int(name[4:], 16)
                out += [0xFFFE, code, len(args)] + args
            k = e + 1
            continue
        for ln in (2, 1):  # sequenze come "\n", "\r", "\f" sono di 2 caratteri nella charmap
            piece = text[k:k + ln]
            if len(piece) == ln and piece in _CODE:
                out.append(_CODE[piece]); k += ln
                break
        else:
            raise ValueError(f"carattere non codificabile: {text[k]!r} in {text!r}")
    return out + [0xFFFF]


def read(b):
    count, key = struct.unpack_from("<HH", b, 0)
    texts = []
    for i in range(count):
        ak = ((765 * (i + 1) * key) & 0xFFFF) * 0x10001
        off, ln = (x ^ ak for x in struct.unpack_from("<II", b, 4 + i * 8))
        codes = list(struct.unpack_from(f"<{ln}H", b, off))
        texts.append((codes, _crypt_str(codes, i + 1)))
    return key, texts


def read_texts(b):
    key, raw = read(b)
    return key, [decode(dec) for _, dec in raw]


def write(key, texts_codes):
    """texts_codes: lista di liste di codici u16 già terminate da 0xFFFF (o testi, che vengono codificati)."""
    n = len(texts_codes)
    head = bytearray(struct.pack("<HH", n, key))
    body = bytearray()
    off = 4 + 8 * n
    for i, t in enumerate(texts_codes):
        codes = encode(t) if isinstance(t, str) else t
        ak = ((765 * (i + 1) * key) & 0xFFFF) * 0x10001
        head += struct.pack("<II", (off + len(body)) ^ ak, len(codes) ^ ak)
        body += struct.pack(f"<{len(codes)}H", *_crypt_str(codes, i + 1))
    return bytes(head + body)


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    base = "IPKI"
    if "--base" in sys.argv:
        i = sys.argv.index("--base"); base = sys.argv[i + 1]; del sys.argv[i:i + 2]
    files = parse_narc((ROOT / "work" / base / "files" / MSG_NARC).read_bytes())
    if len(sys.argv) >= 3 and sys.argv[1] == "mostra":
        key, texts = read_texts(files[int(sys.argv[2])])
        sel = [int(x) for x in sys.argv[3:]] or range(len(texts))
        for i in sel:
            print(f"[{i}] {texts[i]}")
    elif len(sys.argv) == 2 and sys.argv[1] == "verifica":
        ok, bad = 0, []
        for n, b in enumerate(files):
            try:
                key, texts = read_texts(b)
                if write(key, texts) == b:
                    ok += 1
                else:
                    bad.append((n, "diverso"))
            except Exception as e:  # noqa: BLE001
                bad.append((n, str(e)[:80]))
        print(f"Identici dopo decodifica+codifica: {ok}/{len(files)}")
        for n, e in bad[:20]:
            print(f"  {n}: {e}")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
