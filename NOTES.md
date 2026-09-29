# NOTES — diario di progetto

Ultimo aggiornamento: 2026-09-29 (fase 1 completata lato script; restano 2 verifiche manuali dell'utente, §11).

## 1. Obiettivo
Esperienza "Pokémon Cristallo" con **solo le 251 specie di gen 1-2, tutte ottenibili in una partita**, grafica
più moderna del GBC. Base scelta: **Oro HeartGold italiano (IPKI)**. Preferenza per l'italiano (soddisfatta
partendo dalla ROM ITA).

## 2. Stato attuale
- [x] Fase 0 — repository, `.gitignore`, hook anti-ROM, CLAUDE.md/NOTES.md, script di lettura ROM.
- [x] Fase 1 — toolchain e round-trip sulla ROM ITA: **OK**, differenze solo nei 4 byte di CRC dell'header
      (0x6C area sicura, 0x15E header). Mancano: avvio di `out/roundtrip_IPKI.nds` in melonDS e apertura IPKI in DSPRE (utente).
- [ ] Fase 2 — audit completo in sola lettura (vedi §6).
- [ ] Fase 3 — tabelle di design (nuove distribuzioni, allenatori sostitutivi, regali).
- [ ] Fase 4 — `build.py`: applica le tabelle, ricostruisce, genera BPS; audit = 0 specie > 251, 251/251 ottenibili.
- [ ] Fase 5 — opzioni meccaniche (nature neutre?).
- [ ] Fase 6 — playtest dell'utente con checklist.
- [ ] Fase 7 — estensioni (SoulSilver, versione EN, Uovo Strano).

## 3. Decisioni prese (con motivazione)
| # | Decisione | Motivo |
|---|---|---|
| D1 | Approccio: **hack di dati** su HGSS, pipeline di script ripetibile + DSPRE per ispezione | Formati dati identici tra lingue; grafica HGSS; modifiche versionabili come codice/tabelle |
| D2 | Base **HeartGold ITA (IPKI)**, non tradurre dopo | Testo italiano già presente (~50k stringhe); scriviamo in italiano solo i dialoghi nuovi |
| D3 | **Si resta a 251**, si tolgono sia gen 3 sia gen 4 | Lo sporco è poco e negli stessi meccanismi per entrambe (vedi §5): pulire solo la 4 non fa risparmiare lavoro |
| D4 | Split fisico/speciale **mantenuto** | Scelta utente: niente "downgrade" meccanico, si tolgono solo le specie |
| D5 | Mosse di gen 3-4 nei moveset/MT/tutor **mantenute** | Scelta utente |
| D6 | Abilità, nature, strumenti tenuti: **mantenuti** (motore gen 4) | Scelta utente; nature: vedi opzione O1 |
| D7 | Evoluzioni per scambio → Kadabra/Machoke/Graveler/Haunter a **livello 37**; Onix/Scyther (Metallopatina), Seadra (Squama Drago), Slowpoke/Poliwhirl (Roccia di Re), Porygon (Upgrade) → **uso dello strumento come una pietra** (metodo 7) | Semplice, indipendente dall'ora; va verificato che gli strumenti siano ottenibili in una partita |
| D8 | Rimuovere le 17 evoluzioni gen1-2 → gen4 (Magnezone, Lickilicky, Rhyperior, Tangrowth, Electivire, Magmortar, Leafeon, Glaceon, Togekiss, Ambipom, Yanmega, Honchkrow, Mismagius, Gliscor, Weavile, Mamoswine, Porygon-Z) | Dati puri (NARC evoluzioni) |
| D9 | Baby di gen 3-4 (Azurill, Mime Jr., Happiny, Munchlax, Bonsly, Mantyke): rendere **introvabili gli Aromi** | L'allevamento li genera solo con l'incenso; senza, nasce la forma base (da verificare in fase 2) |
| D10 | **Celebi** al Santuario del Bosco di Lecci con incontro statico nuovo | L'evento originale al santuario (per quanto noto) richiede un Celebi-evento già posseduto; da verificare negli script |
| D11 | **Mew** alla **Torre Inclusa** al posto di Groudon (provvisorio, l'utente non ha ancora scelto) | Riusa mappa ed evento esistenti che comunque vanno ripuliti |
| D12 | Parco Lotta: **solo ripulire** i set di Pokémon (nessuna Torre Lotta stile Crystal) | Costo; rivalutare dopo l'audit |
| D13 | Contenuti Crystal: **solo pulizia**; Uovo Strano come extra opzionale finale | HGSS ha già trama di Suicune/Eusine, Ragazze Kimono, protagonista femminile |
| D14 | Tool esterni **non** versionati: `tools/get_tools.py` li scarica a versione fissata con SHA256 verificato | Stessa riproducibilità senza binari nella history (ogni versione × OS resterebbe per sempre nel repo; l'hook blocca > 512 KB). Licenze permetterebbero la ridistribuzione (dsrom MIT, DSPRE AGPL) ma non serve |
| D15 | Estrazione/ricostruzione con **dsrom 0.8.0** (CLI), non DSPRE | Scriptabile, multipiattaforma, round-trip verificato su IPKI; DSPRE resta per ispezione visiva |

## 4. Alternative scartate
- **pret/pokeheartgold (decomp)**: WIP, compila solo USA, serve MWCC (msys2/wine); usarla = perdere l'italiano. Tenuta come *documentazione dei formati*.
- **Universal Pokemon Randomizer ZX**: supporta IPKI/IPGI ma produce risultati casuali; non aggiornato da nov 2024. Utile come riferimento di offset ITA.
- **hg-engine**: solo HG USA, aggiunge generazioni (opposto dell'obiettivo).
- **Base Emerald/FireRed** (Heart & Soul, Liquid Crystal, CrystalDust): già provato (fork "HnS" = Pokémon Heart & Soul, base Emerald): troppa roba da togliere.
- **Crystal GBC migliorati** (Polished, Legacy, Ultimate): grafica GBC, non è l'obiettivo.

## 5. Dati misurati sulla ROM IPKI (da `tools/probe.py`)
- Evoluzioni: 508 voci da 44 byte; 17 evoluzioni gen1-2 → gen4 (lista in D8).
- Selvatici (`a/0/3/7`, 142 tabelle da 196 byte): **nessuna** specie > 251 negli slot normali
  (erba mattino/giorno/notte, surf, pesca, spaccaroccia). Specie > 251 solo in:
  - radio "Suono Hoenn" (Absol, Makuhita, Whismur, Linoone, Plusle, Minun, Zigzagoon, Spinda, Spoink, Numel)
  - radio "Suono Sinnoh" (Shinx, Bronzor, Chingling, Bidoof, Buizel, Chatot, Meditite, Budew, Carnivine)
  - 12 sciami (Whiscash, Ralts, Swablu, Relicanth, Clamperl, Wingull, Luvdisc, Poochyena, Baltoy, Sableye, Buneary, Kricketot)
  - 134 specie gen1-2 distinte sono catturabili negli slot selvatici.
- Allenatori (`a/0/5/5` + `a/0/5/6`): 1776 Pokémon in squadra, **132 > 251** (65 gen3, 67 gen4) in **75 allenatori**.
- Layout incontri usato (offset in byte): erba 20..91 (3×12 u16), radio Hoenn 92/94, radio Sinnoh 96/98,
  surf 100+4k (+2 specie), spaccaroccia 120+4k, pesca 128+4k (15 slot), sciami 188..195.

## 6. Da verificare (fase 2)
- Safari di Johto: secondo Serebii ~25-30 specie gen3-4 su 80+, sbloccate con oggetti + giorni. Formato dati ignoto.
- Headbutt, Gara Bug: dove sono i dati (NARC vs codice).
- Script: regali (Rocco → starter Hoenn), leggendari statici (Torre Inclusa: Groudon; Rovine di Sinjoh: Dialga/Palkia/Giratina), vaganti (Latios/Latias), scambi di gioco, evento Santuario di Lecci.
- Quando si sbloccano i suoni Hoenn/Sinnoh della radio.
- Pokédex di Johto (256 voci): include evoluzioni gen 4? L'ordine è un dato modificabile?
- Ottenibilità in una partita di: Metallopatina, Squama Drago, Roccia di Re, Upgrade, pietre; Aromi (da togliere).
- Disponibilità reale 1-251 in una sola cartuccia (esclusivi di versione, 2 starter Johto mancanti, fossili).
- Parco Lotta: formato dei set Pokémon.
- Percorsi NARC equivalenti su SoulSilver (alcuni differiscono).

## 7. Opzioni aperte
- **O1 — Nature neutre.** Le nature (gen 3+) danno +10% a una statistica e -10% a un'altra (5 su 25 sono neutre).
  Nel motore c'è la tabella `gNatureStatMods[25][5]` (s8, valori +1/0/-1; `src/pokemon.c` della decomp pret).
  Azzerandola nella ARM9 le nature restano solo un'etichetta senza effetto sulle statistiche. Modifica solo di dati,
  individuabile per firma di byte (indipendente dalla lingua).
  **Verificato (fase 1):** su IPKI la tabella compare **una sola volta**, in `work/IPKI/arm9/arm9.bin` (decompresso)
  all'offset `0xFF5B1` (`tools/find_nature_table.py`). Da verificare: altre funzioni che la leggono (es. colore delle
  statistiche nel riepilogo: se usa la stessa tabella diventa neutro anch'esso, il che è coerente).
  Non si possono "rimuovere" dal menu senza modificare codice. Decisione dell'utente dopo la verifica.
- Mew: luogo definitivo (provvisorio: Torre Inclusa).
- Uovo Strano (Crystal): extra finale.

## 8. Strumenti
| Strumento | Versione vista | Note |
|---|---|---|
| Python | 3.12+ (qui 3.14.6) | script del progetto, solo stdlib |
| Git | 2.4x+ | |
| DSPRE Reloaded | 2.3.2 (13/09/2026); canary Avalonia win/linux | https://github.com/DS-Pokemon-Rom-Editor/DSPRE — Windows + .NET Framework 4.8; supporto ITA "Extensive"; solo GUI |
| ds-rom (`dsrom`) | 0.8.0 (MIT) | https://github.com/AetiasHax/ds-rom — estrazione/ricostruzione da CLI. Binari ufficiali Windows/Linux x86_64 (scaricati da `get_tools.py`); macOS: compilare con cargo (docs/SETUP.md). Ignora `RUST_LOG`: il log verboso viene catturato dagli script. Estrazione IPKI: `work/IPKI/{arm9,arm7,arm9_overlays,files,banner}` + `config.yaml`; i NARC sono in `files/a/...` |
| dspre-mcp | — (push 12/09/2026) | https://github.com/webadeva/dspre-mcp — opzionale; validato solo su HG inglese; Node ≥ 22.18; usarlo solo dopo round-trip su IPKI |
| melonDS | ultima | test di gioco; risoluzione interna 3D aumentabile |
| PKHeX | opzionale | verifica salvataggi |

## 9. ROM di riferimento (SHA1 del `.nds`)
| Codice | Gioco | SHA1 |
|---|---|---|
| IPKI | Oro HeartGold (ITA) | 6b7f9bff57eb58bc8d6e48e9e5c370719458c721 |
| IPGI | Argento SoulSilver (ITA) | e137acf711e0b14c297abf0254e5b4a9263338e7 |
| IPKE | HeartGold (USA) | 4fcded0e2713dc03929845de631d0932ea2b5a37 |
| IPGE | SoulSilver (USA) | f8dc38ea20c17541a43b58c5e6d18c1732c7e582 |
Tutte rev0. Non confrontate con il DAT No-Intro (non accessibile).

## 10. Setup su un nuovo PC
Procedura completa passo passo: **[docs/SETUP.md](docs/SETUP.md)** (software, clone, config locale git, ROM,
`get_tools.py` → `roundtrip.py` → `probe.py`, ripresa con Claude Code).

## 11. Prossimi passi
1. (Fatto) Primo push di `main` e `dev` su GitHub come SimpleMatt7; da qui in avanti si lavora e si pusha su `dev`.
2. **Utente**: avviare `out/roundtrip_IPKI.nds` in melonDS fino al menu/intro (verifica che i CRC di header
   non ricalcolati non diano problemi); aprire la ROM IPKI in DSPRE 2.3.2 e confermare che carica senza errori.
3. Fase 2: estendere `probe.py` → audit completo (§6), report in `docs/audit.md` (solo nomi/ID, nessun dato binario).
   Leggere i dati da `work/IPKI/files/` invece che dalla ROM in memoria.
4. Opzionale: provare dspre-mcp su IPKI (round-trip dei suoi parser) se servirà per gli script di evento.

## 12. Problemi aperti
- Nessuno bloccante.
