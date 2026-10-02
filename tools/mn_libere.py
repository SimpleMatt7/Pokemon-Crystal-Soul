"""MN senza occupare mosse (D60): sul campo basta un Pokémon in squadra che *può imparare* la MN (o Bottintesta dal
maestro del Bosco di Lecci); nel menu Pokémon compaiono Volo e Flash (MT70, D63) per chi può impararli.

Sul campo il gioco cerca "un Pokémon che conosce la mossa" in due funzioni (ARM9), con lo stesso blocco di quattro
confronti GetMonData(MOVE1..4) == mossa:
- GetIdxOfFirstPartyMonWithMove (script_pokemon_util.c): Surf e Cascata (field_control.c);
- ScrCmd_GetPartySlotWithMove (scrcmd_party.c): script comune 0146 per Taglio, Forza, Spaccaroccia, Mulinello,
  Scalaroccia e Bottintesta.
Il blocco diventa una chiamata a can_use(mon, mossa): la conosce; oppure è una delle 8 MN (sTMHMMoves[92..99]) e
GetMonTMHMCompat dice che può impararla; oppure è Bottintesta e GetLearnableTutorMoves(mon, maestro di Bottintesta,
NULL) la trova (lo stesso controllo del maestro, ScrCmd_656; è nell'overlay 1, caricato sul campo, l'unico posto da
cui arrivano queste chiamate). Uova escluse come prima (il controllo sta prima del blocco); medaglie controllate come
prima dagli script e dal campo.
Menu Pokémon (sub_0207B0B0): finito il ciclo delle mosse, se resta uno dei 4 posti per le mosse da campo, il Pokémon
può imparare Volo (MN02) e Volo non è già in lista, viene aggiunto (la medaglia la controlla l'uso di Volo, come
prima). Il salto "mossa vuota → fine" diventa "→ mossa successiva" (le mosse dopo una vuota sono vuote), così la
fine del ciclo passa sempre dalla routine.

Codice nuovo nella ARM9 al posto di ScrCmd_563 (sposta un personaggio verso un punto): nessuno script lo usa
(verificato sugli script della decomp, identici alla ROM, e sui nostri), raggiunto solo dalla sua voce nella tabella
dei comandi, puntata a ScrCmd_Dummy. La funzione che lo segue (sub_02041C70) resta: la usa altro codice.
Tutto trovato per contenuto e forma (ITA e USA); da applicare prima di esp_squadra (usa la voce di ScrCmd_062 per
trovare la tabella dei comandi).
"""
import struct

from titolo_ciclo import Asm, EQ, NE, H, find_unique, find_all
from esp_squadra import bl_any, bl_bytes, ARM9

CS = 2
MOVE_FLY, MOVE_HEADBUTT, MOVE_FLASH = 19, 29, 148
HM_FIRST, HM_FLY, TM_FLASH = 92, 93, 69
MENU_EXTRA = ((MOVE_FLY, HM_FLY), (MOVE_FLASH, TM_FLASH))    # mosse da campo nel menu per chi può impararle
TUTOR_HEADBUTT = 3                     # MOVE_TUTOR_NPC_HEADBUTT
CMD_FREE, CMD_656, CMD_SLOT = 563, 656, 141
HM_MOVES = (15, 19, 57, 70, 250, 249, 127, 431)   # Taglio, Volo, Surf, Forza, Mulinello, Spaccaroccia, Cascata, Scalaroccia
MOVE_BLOCK = [0x1C20, 0x2136, 0x2200, None, None, 0x4285, None,
              0x1C20, 0x2137, 0x2200, None, None, 0x4285, None,
              0x1C20, 0x2138, 0x2200, None, None, 0x4285, None,
              0x1C20, 0x2139, 0x2200, None, None, 0x4285, None]       # 56 byte: r4 = Pokémon, r5 = mossa


def locate(arm9, ov1, ov1_base):
    a = {}
    # tabella dei comandi di script: voce di ScrCmd_062 (vedi esp_squadra.locate)
    k = find_unique(arm9, [0xB5F0, 0xB083, 0x1C05, 0x3080, 0x6804, 0x2132, 0x1C20], "ScrCmd_062")
    e62 = arm9.find(struct.pack("<I", ARM9 + k + 1))
    assert e62 > 0 and arm9.count(struct.pack("<I", ARM9 + k + 1)) == 1, "tabella dei comandi"
    table = e62 - 62 * 4
    cmd = lambda n: struct.unpack_from("<I", arm9, table + 4 * n)[0]  # noqa: E731
    a["dummy_ptr"], a["cmd_free_entry"] = cmd(1), table + 4 * CMD_FREE
    # spazio libero: ScrCmd_563 fino alla funzione successiva (push {r3,lr})
    f = (cmd(CMD_FREE) & ~1) - ARM9
    assert arm9.count(struct.pack("<I", cmd(CMD_FREE))) == 1, "ScrCmd_563: puntatori"
    assert H(arm9, f) == 0xB5F8 and H(arm9, f + 0xFA) == 0xBDF8 and H(arm9, f + 0xFC) == 0xB508, "ScrCmd_563: forma"
    a["free"], a["free_len"] = ARM9 + f, 0xFC
    # ScrCmd_GetPartySlotWithMove: blocco dei confronti; trovata → +56 (ldr r0,[sp]; strh r6,[r0]); avanti → bne
    s = (cmd(CMD_SLOT) & ~1) - ARM9
    hits = [h for h in find_all(arm9[s:s + 0xC0], MOVE_BLOCK)]
    assert len(hits) == 1, "GetPartySlotWithMove"
    a["slot_block"] = s + hits[0]
    # GetIdxOfFirstPartyMonWithMove: stesso blocco, trovata → mov r0,r6; pop {r3-r7,pc}
    hits = [h for h in find_all(arm9, MOVE_BLOCK) if H(arm9, h + 56) == 0x1C30 and H(arm9, h + 58) == 0xBDF8]
    assert len(hits) == 1, "GetIdxOfFirstPartyMonWithMove"
    a["idx_block"] = hits[0]
    for blk in ("slot_block", "idx_block"):
        x = H(arm9, a[blk] + 54)
        assert x >> 8 == 0xD1, blk
        a[blk + "_next"] = ARM9 + a[blk] + 54 + 4 + ((((x & 0xFF) ^ 0x80) - 0x80) * 2)
        a[blk + "_found"] = ARM9 + a[blk] + 56
        a["get_mon_data"] = ARM9 + bl_any(arm9, a[blk] + 6)[0]
    # GetMonTMHMCompat (rimando a GetBoxMonTMHMCompat: push {r4-r6,lr}; mov r6,r1; mov r1,#0xAE...)
    k = find_unique(arm9, [0xB570, 0x1C0E, 0x21AE, 0x2200, 0x1C05], "GetBoxMonTMHMCompat")
    assert H(arm9, k - 8) == 0x4B00 and H(arm9, k - 6) == 0x4718 and struct.unpack_from("<I", arm9, k - 4)[0] == ARM9 + k + 1
    a["tmhm_compat"] = ARM9 + k - 8
    # sTMHMMoves[92..99]
    p = struct.pack("<8H", *HM_MOVES)
    assert arm9.count(p) == 1, "sTMHMMoves"
    a["hm_moves"] = ARM9 + arm9.find(p)
    # GetLearnableTutorMoves (overlay 1): in ScrCmd_656 ... mov r1,#3; mov r2,#0; BL
    s = (cmd(CMD_656) & ~1) - ov1_base
    hits = [h for h in find_all(ov1[s:s + 0x60], [0x2103, 0x2200])]
    assert len(hits) == 1, "ScrCmd_656"
    a["tutor_moves"] = ov1_base + bl_any(ov1, s + hits[0] + 4)[0]
    # menu Pokémon, ciclo delle mosse: mov r6,#0; mov r1,r6; ldr r0,[sp,#8]; add r1,#0x36; mov r2,#0
    k = find_unique(arm9, [0x2600, 0x1C31, 0x9802, 0x3136, 0x2200], "menu Pokémon: mosse da campo")
    assert H(arm9, k + 0x12) == 0xD02A and H(arm9, k + 0x38) == 0x1C70, "menu Pokémon: mossa vuota"
    assert H(arm9, k + 0x3E) == 0x2E04 and H(arm9, k + 0x40) == 0xD3DF and H(arm9, k + 0x42) >> 11 == 0b11100
    a["menu_loop"] = k
    a["field_effect_id"] = ARM9 + bl_any(arm9, k + 0x16)[0]
    a["add_field_move"] = ARM9 + bl_any(arm9, k + 0x2E)[0]
    return a


def routines(a):
    s = Asm(a["free"])
    fn, lits = {}, []
    # can_use(mon, mossa) → r0 = 1/0
    fn["can_use"] = s.pos()
    s.h(0xB570)                                  # push {r4-r6,lr}
    s.movr(4, 0); s.movr(5, 1)
    s.mov(6, 0x36)                               # MON_DATA_MOVE1
    s.label("mosse")
    s.movr(0, 4); s.movr(1, 6); s.mov(2, 0); s.bl(a["get_mon_data"])
    s.h(0x42A8)                                  # cmp r0,r5
    s.bcond(EQ, "si")
    s.add8(6, 1); s.cmp(6, 0x3A); s.bcond(NE, "mosse")
    lits.append((len(s.code), 6, a["hm_moves"])); s.h(0)    # ldr r6,=sTMHMMoves[92]
    s.mov(3, 0)
    s.label("mn")
    s.lsl(0, 3, 1); s.h(0x5A30)                  # ldrh r0,[r6,r0]
    s.h(0x42A8); s.bcond(EQ, "mn_si")            # cmp r0,r5
    s.add8(3, 1); s.cmp(3, 8); s.bcond(NE, "mn")
    s.h(0x2D00 | MOVE_HEADBUTT)                  # cmp r5,#29
    s.bcond(NE, "no")
    s.movr(0, 4); s.mov(1, TUTOR_HEADBUTT); s.mov(2, 0); s.bl(a["tutor_moves"])
    s.b("esito")
    s.label("mn_si")
    s.movr(0, 4); s.movr(1, 3); s.add8(1, HM_FIRST); s.bl(a["tmhm_compat"])
    s.label("esito")
    s.cmp(0, 0); s.bcond(EQ, "no")
    s.label("si")
    s.mov(0, 1); s.h(0xBD70)                     # pop {r4-r6,pc}
    s.label("no")
    s.mov(0, 0); s.h(0xBD70)
    # fine del ciclo del menu Pokémon (r4 = posti usati, r5 = voci, r6 = mossa, [sp] menu, [sp+4] voci, [sp+8] Pokémon)
    fn["menu_end"] = s.pos()
    s.cmp(6, 4); s.bcond(CS, "fine")
    s.h(0x4770)                                  # bx lr: mossa successiva
    s.label("fine")
    for n, (move, tmhm) in enumerate(MENU_EXTRA):     # Volo (MN02), poi Flash (MT70, D63)
        nxt = f"extra{n + 1}"
        s.cmp(4, 4); s.bcond(CS, "uscita")           # i 4 posti per le mosse da campo sono pieni
        s.h(0x9802); s.mov(1, tmhm); s.bl(a["tmhm_compat"])       # ldr r0,[sp,#8]
        s.cmp(0, 0); s.bcond(EQ, nxt)
        s.mov(0, move); s.bl(a["field_effect_id"]); s.movr(7, 0)
        s.mov(1, 0)
        s.label(f"cerca{n}")
        s.h(0x42A9); s.bcond(CS, f"aggiungi{n}")     # cmp r1,r5
        s.h(0x9A01); s.h(0x5C52)                     # ldr r2,[sp,#4]; ldrb r2,[r2,r1]
        s.h(0x42BA); s.bcond(EQ, nxt)                # cmp r2,r7: c'è già (la conosce)
        s.add8(1, 1); s.b(f"cerca{n}")
        s.label(f"aggiungi{n}")
        s.h(0x9901); s.h(0x554F)                     # ldr r1,[sp,#4]; strb r7,[r1,r5]
        s.add8(5, 1)
        s.h(0x9800); s.mov(1, move); s.movr(2, 4); s.bl(a["add_field_move"])
        s.add8(4, 1)                                 # un posto in meno
        s.label(nxt)
    s.label("uscita")
    s.movr(0, 5); s.h(0xB003); s.h(0xBDF0)       # mov r0,r5; add sp,#12; pop {r4-r7,pc}
    if len(s.code) % 2:
        s.h(0x46C0)
    s.label("lit")
    for i, (_, _, v) in enumerate(lits):
        s.h(v & 0xFFFF); s.h(v >> 16)
    code = bytearray(s.bytes())
    for i, (idx, rd, _) in enumerate(lits):
        pc = (a["free"] + 2 * idx + 4) & ~3
        off = s.labels["lit"] + 4 * i - pc
        assert 0 <= off < 1024 and off % 4 == 0
        struct.pack_into("<H", code, 2 * idx, 0x4800 | rd << 8 | off // 4)
    assert len(code) <= a["free_len"], len(code)
    return bytes(code), fn


def apply(arm9: bytearray, ov1: bytes, ov1_base: int):
    a = locate(bytes(arm9), ov1, ov1_base)
    code, fn = routines(a)
    f = a["free"] - ARM9
    arm9[f:f + a["free_len"]] = code + b"\x00" * (a["free_len"] - len(code))
    struct.pack_into("<I", arm9, a["cmd_free_entry"], a["dummy_ptr"])
    for blk in ("slot_block", "idx_block"):
        s = Asm(ARM9 + a[blk])
        s.movr(0, 4); s.movr(1, 5); s.bl(fn["can_use"])
        s.cmp(0, 0)
        off = (a[blk + "_found"] - (s.pos() + 4)) // 2
        s.h(0xD100 | (off & 0xFF))               # bne trovata
        off = (a[blk + "_next"] - (s.pos() + 4)) // 2
        s.h(0xE000 | (off & 0x7FF))              # b avanti
        while len(s.code) < 28:
            s.h(0x46C0)
        arm9[a[blk]:a[blk] + 56] = s.bytes()
    k = a["menu_loop"]
    struct.pack_into("<H", arm9, k + 0x12, 0xD000 | ((0x38 - (0x12 + 4)) // 2))      # beq → mossa successiva
    arm9[k + 0x3E:k + 0x42] = bl_bytes(ARM9 + k + 0x3E, fn["menu_end"])
    off = (0x02 - (0x42 + 4)) // 2                     # b → corpo del ciclo (k + 2; k azzera il contatore)
    struct.pack_into("<H", arm9, k + 0x42, 0xE000 | (off & 0x7FF))
    return a, fn, len(code)
