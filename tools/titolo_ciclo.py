"""Titolo: Ho-Oh per un giro completo di telecamera, lampo bianco, poi Lugia per il suo giro (D39).

Il titolo parte come HeartGold (Ho-Oh). Si aggancia la chiamata a TitleScreenAnim_GetCameraNextPosition nel ciclo
principale (TitleScreen_Main): una routine Thumb aggiunta in coda all'overlay 60 chiama la funzione originale e,
quando il giro di telecamera di Ho-Oh finisce (cameraScene torna a 0) e la versione è ancora HG:
  1. schermo 3D (motore A) subito bianco (MASTER_BRIGHT) + dissolvenza da bianco (BeginNormalPaletteFade, solo main)
  2. scarica i modelli di Ho-Oh e delle scintille, distrugge e ricrea il gestore della memoria video 3D (le texture
     di Ho-Oh e Lugia insieme non stanno nei 128 KB del banco A), carica Lugia (20-24) e le scintille SS (41-43)
  3. gameVersion = SoulSilver, telecamera sull'inquadratura iniziale di Lugia
La durata del titolo passa da 2340 a 2436 fotogrammi: giro di Ho-Oh (1270) + giro di Lugia (1146) + 20.

Indirizzi e offset: cercati per contenuto (schemi univoci) così vale per la ROM ITA e USA; offset dei campi da
include/title_screen.h (animData in TitleScreenOverlayData a +0xCC; verificati sul codice compilato).
"""
import struct

BASE_OV60 = None          # letto da overlays.yaml (base_address dell'overlay 60)
TITLE_DURATION = 2436

# offset in TitleScreenAnimData
OFF_HOOH = 0x04           # TitleScreenAnimObject hooh_lugia (0xBC byte)
OFF_SPARKLES = 0xC0
OFF_CAMERA = 0xB8         # hooh_lugia.camera
OFF_SUBSTATE_H = 0x04 + 0xB8
OFF_SUBSTATE_S = 0xC0 + 0xB8
OFF_POS_END = 0x1B8
OFF_TARGET_END = 0x1D0
OFF_SCENE = 0x1F0
OFF_VERSION = 0x200
ANIMDATA_IN_DATA = 0xCC
HEAP_TITLE = 0x1E         # HEAP_ID_TITLE_SCREEN
FADE_MAIN_ONLY, FADE_BRIGHTNESS_IN = 3, 1


def H(b, k):
    return struct.unpack_from("<H", b, k)[0]


def bl_target(b, k):
    h1, h2 = H(b, k), H(b, k + 2)
    assert h1 >> 11 == 0b11110 and h2 >> 11 == 0b11111, f"non è un BL a 0x{k:X}"
    off = ((h1 & 0x7FF) << 12) | ((h2 & 0x7FF) << 1)
    if off & 0x400000:
        off -= 0x800000
    return k + 4 + off


def find_unique(b, words, what):
    """words: lista di mezze parole o None (qualsiasi). Ritorna l'offset dell'unica occorrenza."""
    hits = []
    for k in range(0, len(b) - 2 * len(words), 2):
        if all(w is None or H(b, k + 2 * i) == w for i, w in enumerate(words)):
            hits.append(k)
    if len(hits) != 1:
        raise SystemExit(f"titolo_ciclo: '{what}' trovato {len(hits)} volte")
    return hits[0]


def find_all(b, words):
    return [k for k in range(0, len(b) - 2 * len(words), 2)
            if all(w is None or H(b, k + 2 * i) == w for i, w in enumerate(words))]


def same_bl(b, words, delta, what):
    """Più occorrenze ammesse, purché il BL a +delta porti sempre allo stesso indirizzo."""
    hits = find_all(b, words)
    targets = {bl_target(b, k + delta) for k in hits}
    if not hits or len(targets) != 1:
        raise SystemExit(f"titolo_ciclo: '{what}': {len(hits)} occorrenze, destinazioni {targets}")
    return targets.pop()


def locate(b):
    """→ dizionario di offset (nell'overlay) e indirizzi assoluti (ARM9) delle funzioni che servono."""
    a = {}
    # ciclo principale: mov r0,r4; add r0,#0xCC; BL GetCameraNextPosition; add r4,#0xCC; mov r0,r4; BL FadeIn...
    k = find_unique(b, [0x1C20, 0x30CC, None, None, 0x34CC, 0x1C20], "chiamata alla telecamera")
    a["hook"] = k + 4
    a["get_camera_next"] = bl_target(b, k + 4)
    # durata: ldr r6,[r4,r0]; ldr r3,=durata; cmp r6,r3; ble
    k = find_unique(b, [0x5826, None, 0x429E], "confronto della durata")
    ins = H(b, k + 2)
    assert ins >> 11 == 0b01001
    a["duration_lit"] = ((k + 2 + 4) & ~3) + (ins & 0xFF) * 4
    assert struct.unpack_from("<I", b, a["duration_lit"])[0] == 2340, "durata del titolo inattesa"
    # InitObjectsAndCamera: push; sub sp; mov r5,r0; mov r6,r1; mov r4,r2; BL SetCameraInitialPos
    k = find_unique(b, [0xB578, 0xB083, 0x1C05, 0x1C0E, 0x1C14], "inizializzazione dei modelli")
    a["set_camera_initial"] = bl_target(b, k + 10)
    k = find_unique(b, [0x2119, 0x221A, 0x231B, 0x9402], "caricamento modello Ho-Oh")
    a["load3d"] = bl_target(b, k + 8)
    a["unload3d"] = find_unique(b, [0xB5F8, 0x1C07, 0x1C3E, 0x2400, 0x1C3D, 0x3680], "scaricamento modello")
    a["vram_delete"] = find_unique(b, [0x4B01, 0x6880, 0x4718], "distruzione gestore VRAM 3D")
    a["vram_create"] = find_unique(b, [0xB510, 0xB082, 0x1C04, 0x2004, 0x2100, 0x9000, 0x9101], "creazione gestore VRAM 3D")
    # animazione (setup): mov r1,r5; mov r0,#0x1D; add r1,#0xB8; lsl r0,#4; ldr r1,[r1]; add r0,r5,r0; BL target
    a["cam_target"] = same_bl(b, [0x1C29, 0x201D, 0x31B8, 0x0100, 0x6809, 0x1828], 12, "telecamera: bersaglio")
    a["cam_pos"] = same_bl(b, [0x1C29, 0x206E, 0x31B8, 0x0080, 0x6809, 0x1828], 12, "telecamera: posizione")
    # dissolvenza (PROCEED_FLASH_2): mov r0,#12; str; mov r1,#1; str; mov r0,#0x1E; str; ldr r3,=bianco; mov r0,#0; mov r2,r1; BL
    k = find_unique(b, [0x200C, 0x9000, 0x2101, 0x9101, 0x201E, 0x9002, None, 0x2000, 0x1C0A], "dissolvenza")
    a["fade"] = bl_target(b, k + 18)
    return a


class Asm:
    """Assemblatore Thumb minimo per la routine."""
    def __init__(self, origin):
        self.origin, self.code, self.labels, self.fix = origin, [], {}, []

    def h(self, x):
        self.code.append(x & 0xFFFF)

    def pos(self):
        return self.origin + 2 * len(self.code)

    def label(self, n):
        self.labels[n] = self.pos()

    def bl(self, target):
        off = target - (self.pos() + 4)
        self.h(0xF000 | ((off >> 12) & 0x7FF)); self.h(0xF800 | ((off >> 1) & 0x7FF))

    def bcond(self, cond, lab):
        self.fix.append((len(self.code), cond, lab)); self.h(0)

    def mov(self, rd, imm): self.h(0x2000 | rd << 8 | imm)
    def movr(self, rd, rs): self.h(0x1C00 | rs << 3 | rd)
    def cmp(self, rd, imm): self.h(0x2800 | rd << 8 | imm)
    def add8(self, rd, imm): self.h(0x3000 | rd << 8 | imm)
    def sub8(self, rd, imm): self.h(0x3800 | rd << 8 | imm)
    def addi3(self, rd, rn, imm): self.h(0x1C00 | imm << 6 | rn << 3 | rd)
    def addr(self, rd, rn, rm): self.h(0x1800 | rm << 6 | rn << 3 | rd)
    def lsl(self, rd, rm, imm): self.h(imm << 6 | rm << 3 | rd)
    def ldrr(self, rd, rn, rm): self.h(0x5800 | rm << 6 | rn << 3 | rd)
    def strr(self, rd, rn, rm): self.h(0x5000 | rm << 6 | rn << 3 | rd)
    def ldri(self, rd, rn, off): self.h(0x6800 | (off // 4) << 6 | rn << 3 | rd)
    def strh0(self, rd, rn): self.h(0x8000 | rn << 3 | rd)
    def strsp(self, rd, off): self.h(0x9000 | rd << 8 | off // 4)

    def big(self, rd, value):
        """rd = value (fino a 0x3FFF circa) con mov/lsl/add."""
        if value < 256:
            self.mov(rd, value); return
        sh = 0
        while (value >> sh) > 255 or (value >> sh) << sh != value:
            sh += 1
            if (value >> sh) <= 255:
                break
        base = value >> sh
        self.mov(rd, base); self.lsl(rd, rd, sh)
        rest = value - (base << sh)
        assert 0 <= rest < 256
        if rest:
            self.add8(rd, rest)

    def bytes(self):
        for idx, cond, lab in self.fix:
            off = (self.labels[lab] - (self.origin + 2 * idx + 4)) // 2
            assert -128 <= off < 128
            self.code[idx] = 0xD000 | cond << 8 | (off & 0xFF)
        return struct.pack(f"<{len(self.code)}H", *self.code)


EQ, NE = 0, 1


def routine(origin, a, base):
    """Codice della routine all'offset `origin` dell'overlay (indirizzi ARM9 assoluti convertiti in offset)."""
    rel = lambda addr: addr - base if addr > 0x02000000 else addr  # noqa: E731
    s = Asm(origin)
    s.h(0xB5F0)                      # push {r4-r7, lr}
    s.h(0xB083)                      # sub sp, #12
    s.movr(4, 0)                     # r4 = animData
    s.big(6, OFF_SCENE)
    s.ldrr(5, 4, 6)                  # r5 = cameraScene prima
    s.bl(a["get_camera_next"])       # funzione originale (r0 = animData)
    s.ldrr(0, 4, 6)
    s.cmp(0, 0); s.bcond(NE, "done")         # il giro è appena finito: scena tornata a 0 ...
    s.cmp(5, 0); s.bcond(EQ, "done")         # ... da una scena diversa da 0
    s.big(7, OFF_VERSION)
    s.ldrr(0, 4, 7)
    s.cmp(0, 7); s.bcond(NE, "done")         # solo il primo giro (ancora HeartGold)
    s.mov(0, 8); s.strr(0, 4, 7)             # gameVersion = SoulSilver
    # schermo 3D subito bianco: REG_MASTER_BRIGHT (motore A) = modalità schiarisci, intensità 16
    s.mov(0, 4); s.lsl(0, 0, 24); s.add8(0, 0x6C)
    s.mov(1, 0x80); s.lsl(1, 1, 7); s.add8(1, 0x10)
    s.strh0(1, 0)
    # scarica Ho-Oh e scintille
    s.addi3(0, 4, OFF_HOOH); s.bl(a["unload3d"])
    s.movr(0, 4); s.add8(0, OFF_SPARKLES); s.bl(a["unload3d"])
    # gestore della memoria video 3D: distrutto e ricreato (libera le texture)
    s.movr(6, 4); s.sub8(6, ANIMDATA_IN_DATA)   # r6 = TitleScreenOverlayData
    s.movr(0, 6); s.bl(a["vram_delete"])
    s.movr(0, 6); s.bl(a["vram_create"])
    # Lugia: Load3DObjects(&hooh_lugia, 20, 21, 22, 23, 24, heapID)
    s.mov(0, 23); s.strsp(0, 0)
    s.mov(0, 24); s.strsp(0, 4)
    s.ldri(0, 6, 0); s.strsp(0, 8)
    s.addi3(0, 4, OFF_HOOH); s.mov(1, 20); s.mov(2, 21); s.mov(3, 22)
    s.bl(a["load3d"])
    # scintille SS: Load3DObjects(&sparkles, 41, 42, -1, 43, -1, heapID)
    s.mov(0, 43); s.strsp(0, 0)
    s.mov(0, 0); s.sub8(0, 1); s.strsp(0, 4); s.movr(3, 0)
    s.ldri(0, 6, 0); s.strsp(0, 8)
    s.movr(0, 4); s.add8(0, OFF_SPARKLES); s.mov(1, 41); s.mov(2, 42)
    s.bl(a["load3d"])
    # animazioni in corsa (Load3DObjects le mette ferme)
    s.mov(0, 2)
    s.big(1, OFF_SUBSTATE_H); s.strr(0, 4, 1)
    s.big(1, OFF_SUBSTATE_S); s.strr(0, 4, 1)
    # telecamera: inquadratura iniziale di Lugia
    s.movr(0, 4); s.bl(a["set_camera_initial"])
    s.big(0, OFF_TARGET_END); s.addr(0, 0, 4)
    s.big(1, OFF_CAMERA); s.ldrr(1, 4, 1)
    s.bl(a["cam_target"])
    s.big(0, OFF_POS_END); s.addr(0, 0, 4)
    s.big(1, OFF_CAMERA); s.ldrr(1, 4, 1)
    s.bl(a["cam_pos"])
    # dissolvenza da bianco del solo schermo 3D: (MAIN_ONLY, IN, IN, bianco, 16 passi, 1, heap)
    s.mov(0, 16); s.strsp(0, 0)
    s.mov(0, 1); s.strsp(0, 4)
    s.mov(0, HEAP_TITLE); s.strsp(0, 8)
    s.mov(0, FADE_MAIN_ONLY); s.mov(1, FADE_BRIGHTNESS_IN); s.mov(2, FADE_BRIGHTNESS_IN)
    s.mov(3, 0xFF); s.lsl(3, 3, 7); s.add8(3, 0x7F)     # 0x7FFF bianco
    s.bl(a["fade"])
    s.label("done")
    s.h(0xB003)                      # add sp, #12
    s.h(0xBDF0)                      # pop {r4-r7, pc}
    return s.bytes()


def apply(ov: bytearray, base: int):
    """Modifica l'overlay 60 (già decompresso). Ritorna (nuovo contenuto, offset della routine)."""
    a = locate(bytes(ov))
    for k in ("fade", "cam_target", "cam_pos"):
        a[k] = a[k]                                    # già offset relativi all'overlay (anche se negativi: ARM9)
    while len(ov) % 4:
        ov.append(0)
    origin = len(ov)
    code = routine(origin, a, base)
    ov += code
    # aggancio: BL alla routine al posto di BL GetCameraNextPosition
    off = origin - (a["hook"] + 4)
    struct.pack_into("<HH", ov, a["hook"], 0xF000 | ((off >> 12) & 0x7FF), 0xF800 | ((off >> 1) & 0x7FF))
    struct.pack_into("<I", ov, a["duration_lit"], TITLE_DURATION)
    return ov, origin, a
