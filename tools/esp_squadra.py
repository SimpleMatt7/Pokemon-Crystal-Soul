"""Esp. Squadra (D56): Condividi Esperienza di tutta la squadra, accesa e spenta con uno strumento chiave.

Strumento: la Scheda Punti (Point Card, 432), avanzo di Diamante/Perla mai dato da HGSS (nessuno script la usa),
già strumento chiave registrabile che si "usa" come il Salvadanaio: Borsa → Usa e tasto Y chiamano entrambi
TryFormatRegisteredKeyItemUseMessage (ARM9, bag_view.c). Il ramo della Scheda Punti viene riscritto: inverte il flag
nostro FLAG_PCN_ESP_SQUADRA e mostra il messaggio 129 (spenta) o 130 (accesa) di msg_0010. Nome, descrizione e
icona (quella del Condividi Esp.) cambiano con i testi e la tabella delle icone (build.py).

Lotta (overlay 12), stile moderno: accesa, chi lotta riceve il 100% e il resto della squadra il 50%.
- BtlCmd_CalcExpGain: nel conteggio dei Pokémon "con Condividi Esp." l'effetto dello strumento tenuto vale
  HOLD_EFFECT_EXP_SHARE per tutti (così si entra nel ramo con Condividi Esp.); in quel ramo le due divisioni
  (metà Esp. / partecipanti, metà Esp. / portatori) non dividono più: gainedExp = partyGainedExp = metà Esp.
- Task_GetExp: ogni Pokémon della squadra viene considerato (ciclo di scelta) e riceve partyGainedExp (controllo
  "tiene Condividi Esp."); chi ha lottato riceve gainedExp + partyGainedExp = Esp. intera. Uovo Fortunato, lotte con
  allenatori e Pokémon scambiati restano come prima (l'effetto vero dello strumento non viene toccato lì).
Le Uova restano escluse. Per chi non ha lottato niente messaggio "ha guadagnato N Punti Esp." (come nei giochi
recenti); gli aumenti di livello e le mosse nuove si vedono ancora. Spenta: tutto come nel gioco originale (anche il Condividi Esp. tenuto).

Il codice nuovo sta nella ARM9 al posto di ScrCmd_062 (scorrimento del riquadro di testo) e della sua funzione
d'appoggio: comando che nessuno script usa (verificato sugli script della decomp, identici alla ROM), raggiunto solo
dalla sua voce nella tabella dei comandi, che viene puntata a ScrCmd_Dummy. Tutto è trovato per contenuto: vale per
ITA e USA.
"""
import struct

from titolo_ciclo import Asm, EQ, NE, H, bl_target, find_unique

FLAG = 0x54B              # FLAG_PCN_ESP_SQUADRA (FLAG_UNK_54B: non usato da nessuno script)
MSG_SPENTA = 129          # msg_0010: 129 spenta, 130 accesa (testi aggiunti in data/testi/<lingua>/msg_0010.csv)
ITEM = 432                # ITEM_POINT_CARD
ICON_FROM = 216           # ITEM_EXP_SHARE
HOLD_EFFECT_EXP_SHARE = 0x33
MON_DATA_IS_EGG = 76
ARM9 = 0x02000000


def bl_any(b, k):
    """Destinazione di BL o BLX (assoluta solo per BLX: allineata a 4)."""
    h1, h2 = H(b, k), H(b, k + 2)
    assert h1 >> 11 == 0b11110 and h2 >> 11 in (0b11111, 0b11101), f"non è un BL/BLX a 0x{k:X}"
    off = ((h1 & 0x7FF) << 12) | ((h2 & 0x7FF) << 1)
    if off & 0x400000:
        off -= 0x800000
    return k + 4 + off, h2 >> 11 == 0b11101


def locate(arm9, ov12, ov12_base):
    a = {}
    # --- ARM9: flag (save_vars_flags.c): Check; Get è 12 byte prima, Set e Clear dopo
    k = find_unique(arm9, [0xB538, 0x1C0C, None, None, 0x2800, 0xD00C, 0x0FE3, 0x0762], "Save_VarsFlags_CheckFlagInArray")
    a["check"] = ARM9 + k
    a["get"] = a["check"] - 0xC
    assert arm9[k - 0xC:k - 0x6] == bytes.fromhex("014b04211847"), "Save_VarsFlags_Get inatteso"
    a["set"], a["clear"] = a["check"] + 0x2C, a["check"] + 0x54
    for f in ("set", "clear"):
        assert H(arm9, a[f] - ARM9) == 0xB570 and H(arm9, a[f] - ARM9 + 2) == 0x1C0C, f
    save_array_get = struct.unpack_from("<I", arm9, k - 0xC + 8)[0] & ~1
    # SaveData_Get: subito prima di SaveArray_Get (save.c)
    a["save_get"] = save_array_get - 0x18
    s = a["save_get"] - ARM9
    assert [H(arm9, s + i) for i in (0, 4, 6, 8)] == [0xB508, 0x6800, 0x2800, 0xD101], "SaveData_Get inatteso"
    # TryFormatRegisteredKeyItemUseMessage, ramo della Scheda Punti: mov r1,#0x1B; lsl r1,#4 (=432); cmp r5,r1; bne
    k = find_unique(arm9, [0x211B, 0x0109, 0x428D, 0xD111, 0x1C30, 0x2164], "ramo della Scheda Punti")
    a["pc_branch"] = ARM9 + k + 8                      # 36 byte, fino al salto alla parte comune
    a["new_string"] = ARM9 + bl_target(arm9, k + 12)
    end = k + 8 + 34
    x = H(arm9, end)
    assert x >> 11 == 0b11100, "salto finale del ramo della Scheda Punti"
    a["pc_common"] = ARM9 + end + 4 + ((((x & 0x7FF) ^ 0x400) - 0x400) * 2)
    # ScrCmd_062 + sub (ARM9): spazio libero
    k = find_unique(arm9, [0xB5F0, 0xB083, 0x1C05, 0x3080, 0x6804, 0x2132, 0x1C20], "ScrCmd_062")
    a["free"], a["free_len"] = ARM9 + k, 0x150
    assert H(arm9, k + 0x92) == 0xBDF0 and H(arm9, k + 0x98) == 0xB5F0 and H(arm9, k + 0x14C) == 0xBDF0, "ScrCmd_062: forma inattesa"
    ptr = struct.pack("<I", a["free"] | 1)
    assert arm9.count(ptr) == 1, "ScrCmd_062: puntatori"
    a["cmd62_entry"] = arm9.find(ptr)
    a["dummy_ptr"] = struct.unpack_from("<I", arm9, a["cmd62_entry"] - 61 * 4)[0]   # voce 1: ScrCmd_Dummy
    # tabella delle icone degli strumenti (item.c): {dati, icona, tavolozza, agb} u16
    k = arm9.find(struct.pack("<7H", 0, 793, 794, 0, 1, 2, 3))
    assert k > 0 and arm9.count(struct.pack("<7H", 0, 793, 794, 0, 1, 2, 3)) == 1, "tabella delle icone"
    a["icons"] = k
    # --- overlay 12
    o = lambda k: ov12_base + k  # noqa: E731
    # BtlCmd_CalcExpGain, conteggio: mov r0,r5; mov r2,#1; BL GetItemVar; cmp r0,#0x33; bne
    k = find_unique(ov12, [0x1C28, 0x2201, None, None, 0x2833, 0xD102], "conteggio Condividi Esp.")
    a["site_cnt"] = k + 4
    a["get_item_var"] = o(bl_any(ov12, k + 4)[0])
    # divisioni: lsr r4,r0,#1; ldr r1,[sp,#4]; mov r0,r4; BLX div  /  ldr r1,[sp]; mov r0,r4; BLX div; mov r1,r5; add r1,#0xA0
    k = find_unique(ov12, [0x0844, 0x9901, 0x1C20, None, None], "divisione Esp. partecipanti")
    a["site_div1"] = k + 6
    t, x = bl_any(ov12, k + 6)
    assert x, "divisione: BLX atteso"
    a["div"] = (o(k + 6 + 4) & ~3) + (t - (k + 6 + 4))
    k = find_unique(ov12, [0x9900, 0x1C20, None, None, 0x1C29, 0x31A0], "divisione Esp. portatori")
    a["site_div2"] = k + 4
    # Task_GetExp, scelta: mov r1,#1; mov r2,#5; BL GetItemAttr; cmp r0,#0x33; beq
    k = find_unique(ov12, [0x2101, 0x2205, None, None, 0x2833, 0xD011], "scelta dei Pokémon")
    a["site_sel"] = k + 4
    a["get_item_attr"] = o(bl_any(ov12, k + 4)[0])
    assert H(ov12, k - 4) == 0x0400 and H(ov12, k - 2) == 0x0C00, "scelta: GetMonData"
    a["get_mon_data"] = o(bl_any(ov12, k - 8)[0])
    # Task_GetExp, Esp. ai portatori: ldr r0,[sp,#0x18]; cmp r0,#0x33; bne; ldr r0,[sp,#0x24]; add r0,#0xA0
    k = find_unique(ov12, [0x9806, 0x2833, 0xD106, 0x9809, 0x30A0], "Esp. ai portatori")
    a["site_share"] = k
    # Task_GetExp, messaggio "ha guadagnato N Punti Esp.": ldr r0,[sp,#0x38]; cmp r0,#0; beq; mov r1,#0x11; add r0,sp,#0xB4
    k = find_unique(ov12, [0x980E, 0x2800, 0xD018, 0x2111, 0xA82D, 0x7041], "messaggio Punti Esp.")
    assert H(ov12, k + 0x30) == 0xB036 and H(ov12, k + 0x36) == 0xBDF8, "Task_GetExp: epilogo inatteso"
    find_unique(ov12, [0x2001, 0x4008, 0x9011, 0x6820, 0x1C39], "Task_GetExp: lato in [sp+0x44]")
    a["site_msg"] = k
    return a


def blx(s, target):
    """BLX (Thumb → ARM) verso un indirizzo allineato a 4."""
    off = target - ((s.pos() + 4) & ~3)
    assert target % 4 == 0 and off % 4 == 0
    s.h(0xF000 | ((off >> 12) & 0x7FF)); s.h(0xE800 | ((off >> 1) & 0x7FF))


def routines(a):
    s = Asm(a["free"])
    fn = {}
    # on() → r0 = flag acceso
    fn["on"] = s.pos()
    s.h(0xB508)                                  # push {r3,lr}
    s.bl(a["save_get"]); s.bl(a["get"])
    s.big(1, FLAG); s.bl(a["check"])
    s.h(0xBD08)                                  # pop {r3,pc}
    # toggle(saveData) → r0 = nuovo stato
    fn["toggle"] = s.pos()
    s.h(0xB510)                                  # push {r4,lr}
    s.bl(a["get"]); s.movr(4, 0)
    s.big(1, FLAG); s.bl(a["check"])
    s.cmp(0, 0); s.bcond(NE, "spegni")
    s.movr(0, 4); s.big(1, FLAG); s.bl(a["set"]); s.mov(0, 1); s.h(0xBD10)
    s.label("spegni")
    s.movr(0, 4); s.big(1, FLAG); s.bl(a["clear"]); s.mov(0, 0); s.h(0xBD10)
    # effetto dello strumento tenuto (conteggio e scelta): acceso → Condividi Esp., altrimenti funzione originale
    for name, orig in (("attr_cnt", a["get_item_var"]), ("attr_sel", a["get_item_attr"])):
        fn[name] = s.pos()
        s.h(0xB507)                              # push {r0-r2,lr}
        s.bl(fn["on"]); s.cmp(0, 0)
        s.h(0xBC07)                              # pop {r0-r2} (i flag restano)
        s.bcond(NE, name + "_on")
        s.bl(orig); s.h(0xBD00)                  # pop {pc}
        s.label(name + "_on")
        s.mov(0, HOLD_EFFECT_EXP_SHARE); s.h(0xBD00)
    # div(n, d): acceso → n, altrimenti n / d
    fn["div"] = s.pos()
    s.h(0xB513)                                  # push {r0,r1,r4,lr}
    s.bl(fn["on"]); s.movr(4, 0)
    s.h(0xBC03)                                  # pop {r0,r1}
    s.cmp(4, 0); s.bcond(NE, "div_on")
    blx(s, a["div"])
    s.label("div_on")
    s.h(0xBD10)                                  # pop {r4,pc}
    # share(): Z = 1 se il Pokémon tiene Condividi Esp. ([sp+0x18] del chiamante) o se Esp. Squadra è accesa
    # (accesa: solo se non è un Uovo; prima non capitava mai, le Uova non lottano né tengono strumenti.
    # r6 = Pokémon nel chiamante)
    fn["share"] = s.pos()
    s.h(0x9806)                                  # ldr r0,[sp,#0x18]
    s.cmp(0, HOLD_EFFECT_EXP_SHARE); s.bcond(EQ, "share_ret")
    s.h(0xB500)                                  # push {lr}
    s.bl(fn["on"]); s.cmp(0, 0); s.bcond(EQ, "share_off")
    s.movr(0, 6); s.mov(1, MON_DATA_IS_EGG); s.mov(2, 0); s.bl(a["get_mon_data"])
    s.cmp(0, 0)                                  # Z = 1: non è un Uovo
    s.h(0xBD00)                                  # pop {pc}
    s.label("share_off")
    s.cmp(0, 1)                                  # r0 = 0 → Z = 0
    s.h(0xBD00)                                  # pop {pc}
    s.label("share_ret")
    s.h(0x4770)                                  # bx lr
    # msg(): nel chiamante r4 = GetterWork, r5 = posto in squadra, [sp+0x38] = Esp. guadagnati, [sp+0x44] = lato.
    # Esp. 0 → Z = 1 (come prima). Esp. Squadra accesa e Pokémon che non ha lottato: niente messaggio, si passa
    # subito a STATE_GET_EXP_GAUGE (3), che per chi non è in campo va al controllo del livello (aumenti di livello e
    # mosse nuove si vedono ancora); si esce direttamente da Task_GetExp col suo epilogo. Altrimenti Z = 0.
    fn["msg"] = s.pos()
    s.h(0x980E)                                  # ldr r0,[sp,#0x38]
    s.cmp(0, 0); s.bcond(EQ, "msg_ret")
    s.h(0xB500)                                  # push {lr}
    s.bl(fn["on"])
    s.h(0xBC02); s.h(0x468E)                     # pop {r1}; mov lr,r1
    s.cmp(0, 0); s.bcond(EQ, "msg_loud")
    s.ldri(0, 4, 4)                              # ctx
    s.h(0x9911)                                  # ldr r1,[sp,#0x44]
    s.lsl(1, 1, 2); s.addr(0, 0, 1); s.add8(0, 0xA4)
    s.ldri(0, 0, 0)                              # ctx->unk_A4[lato]: chi ha lottato
    s.h(0x40E8)                                  # lsr r0,r5
    s.lsl(0, 0, 31); s.bcond(NE, "msg_loud")
    s.mov(0, 3); s.h(0x62A0)                     # data->state = STATE_GET_EXP_GAUGE
    s.h(0xB036); s.h(0xBDF8)                     # add sp,#0xD8; pop {r3-r7,pc}
    s.label("msg_loud")
    s.mov(0, 1); s.cmp(0, 0)                     # Z = 0
    s.label("msg_ret")
    s.h(0x4770)                                  # bx lr
    code = s.bytes()
    assert len(code) <= a["free_len"], len(code)
    return code, fn


def bl_bytes(at, target):
    off = target - (at + 4)
    assert -0x400000 <= off < 0x400000
    return struct.pack("<HH", 0xF000 | ((off >> 12) & 0x7FF), 0xF800 | ((off >> 1) & 0x7FF))


def apply(arm9: bytearray, ov12: bytearray, ov12_base: int):
    a = locate(bytes(arm9), bytes(ov12), ov12_base)
    code, fn = routines(a)
    f = a["free"] - ARM9
    arm9[f:f + a["free_len"]] = code + b"\x00" * (a["free_len"] - len(code))
    struct.pack_into("<I", arm9, a["cmd62_entry"], a["dummy_ptr"])
    # ramo della Scheda Punti: toggle(saveData); msg = 129 + stato; stringa → r5; salto alla parte comune
    s = Asm(a["pc_branch"])
    s.movr(0, 7); s.bl(fn["toggle"])
    s.movr(1, 0); s.add8(1, MSG_SPENTA)
    s.movr(0, 6); s.bl(a["new_string"])
    s.movr(5, 0)
    off = (a["pc_common"] - (s.pos() + 4)) // 2
    s.h(0xE000 | (off & 0x7FF))
    while len(s.code) < 18:
        s.h(0x46C0)                              # nop
    p = a["pc_branch"] - ARM9
    arm9[p:p + 36] = s.bytes()
    # icona: quella del Condividi Esp.
    i = a["icons"]
    arm9[i + 8 * ITEM + 2:i + 8 * ITEM + 6] = arm9[i + 8 * ICON_FROM + 2:i + 8 * ICON_FROM + 6]
    # overlay 12
    for site, target in (("site_cnt", fn["attr_cnt"]), ("site_sel", fn["attr_sel"]),
                         ("site_div1", fn["div"]), ("site_div2", fn["div"]), ("site_share", fn["share"]),
                         ("site_msg", fn["msg"])):
        at = a[site]
        ov12[at:at + 4] = bl_bytes(ov12_base + at, target)
    return a, fn, len(code)
