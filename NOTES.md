# NOTES — diario di progetto

Ultimo aggiornamento: 2026-09-29 (fase 0 completata, fase 1 da iniziare).

## 1. Obiettivo
Esperienza "Pokémon Cristallo" con **solo le 251 specie di gen 1-2, tutte ottenibili in una partita**, grafica
più moderna del GBC. Base scelta: **Oro HeartGold italiano (IPKI)**. Preferenza per l'italiano (soddisfatta
partendo dalla ROM ITA).

## 2. Stato attuale
- [x] Fase 0 — repository, `.gitignore`, hook anti-ROM, CLAUDE.md/NOTES.md, script di lettura ROM.
- [ ] Fase 1 — toolchain e round-trip (estrai → ricostruisci → confronta) sulla ROM ITA.
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
  individuabile per firma di byte (indipendente dalla lingua). Da confermare in fase 1/2 (posizione in ARM9, eventuali altri usi della tabella, es. colore delle statistiche nel sommario).
  Non si possono "rimuovere" dal menu senza modificare codice. Decisione dell'utente dopo la verifica.
- Mew: luogo definitivo (provvisorio: Torre Inclusa).
- Uovo Strano (Crystal): extra finale.

## 8. Strumenti
| Strumento | Versione vista | Note |
|---|---|---|
| Python | 3.12+ (qui 3.14.6) | script del progetto, solo stdlib |
| Git | 2.4x+ | |
| DSPRE Reloaded | 2.3.2 (13/09/2026); canary Avalonia win/linux | https://github.com/DS-Pokemon-Rom-Editor/DSPRE — Windows + .NET Framework 4.8; supporto ITA "Extensive"; solo GUI |
| ds-rom (`dsrom`) | 0.8.0 | https://github.com/AetiasHax/ds-rom — estrazione/ricostruzione da CLI (fase 1) |
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
1. Installare Git e Python ≥ 3.12. (Windows: anche DSPRE 2.3.2 portable; melonDS.)
2. `git clone https://github.com/SimpleMatt7/Pokemon-Crystal-New.git` e `git switch dev`.
3. Nel clone: `git config user.name "SimpleMatt7"`, `git config user.email "matt.sandon@gmail.com"`,
   `git config core.hooksPath tools/hooks`.
4. Copiare le proprie ROM (`.nds` o `.zip`) in `roms/` e lanciare `python tools/roms.py`: deve dire `OK` per IPKI.
5. Aprire Claude Code nella cartella: leggerà CLAUDE.md → NOTES.md.

## 11. Prossimi passi
1. Fase 1: script che scarica `dsrom` (con verifica hash) in `tools/bin/`; estrazione IPKI in `work/`; ricostruzione;
   confronto byte a byte (atteso: differenze solo nei CRC dell'header).
2. Fase 1: l'utente apre IPKI in DSPRE e conferma che si carica (Windows).
3. Fase 2: estendere `probe.py` → audit completo (§6), report in `docs/audit.md` (solo nomi/ID, nessun dato binario).

## 12. Problemi aperti
- Nessuno bloccante.
