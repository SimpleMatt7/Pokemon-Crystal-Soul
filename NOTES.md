# NOTES — diario di progetto

Ultimo aggiornamento: 2026-09-30 (rifiniture: titolo SoulSilver (Lugia, cielo azzurro) con logo "Versione Crystal Soul"
generato da `tools/logo.py`; Ho-Oh/Lugia lv 60. Da chiarire: schermata "oro" dopo il titolo. §11).

## 1. Obiettivo
Esperienza "Pokémon Cristallo" con **solo le 251 specie di gen 1-2, tutte ottenibili in una partita**, grafica
più moderna del GBC. Base scelta: **Oro HeartGold italiano (IPKI)**. Preferenza per l'italiano (soddisfatta
partendo dalla ROM ITA).

## 2. Stato attuale
- [x] Fase 0 — repository, `.gitignore`, hook anti-ROM, CLAUDE.md/NOTES.md, script di lettura ROM.
- [x] Fase 1 — toolchain e round-trip sulla ROM ITA: **OK**, differenze solo nei 4 byte di CRC dell'header
      (0x6C area sicura, 0x15E header). Mancano: avvio di `out/roundtrip_IPKI.nds` in melonDS e apertura IPKI in DSPRE (utente).
- [x] Fase 2 — audit completo in sola lettura (`docs/audit.md`, `docs/oggetti.md`; §5b).
- [x] Fase 3 — tabelle di design in `data/design/` (verificate in memoria: 0 > 251, 251/251).
- [~] Fase 4 — `build.py`: dati fatti (verifica sui file costruiti: 0 > 251); da fare script (assemblatore), Pokédex di Johto, patch codice Pichu.
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
| D16 | Le 10 esclusive SS (Vulpix, Meowth, Ledyba, Teddiursa, Delibird, Skarmory + evoluzioni) diventano **selvatiche nelle aree dove stanno in SoulSilver** | Scelta utente (2026-09-29): la più fedele |
| D17 | Rocco (T11R0701) regala **Chikorita/Cyndaquil/Totodile** al posto di Treecko/Torchic/Mudkip | Scelta utente (2026-09-29) |
| D18 | I 12 sciami gen 3-4 vengono **sostituiti** con specie gen 1-2 (gli 8 sciami gen 1-2 restano) | Scelta utente (2026-09-29) |
| D19 | Kabuto: **Domofossile al posto del Frammento Blu** nella tabella Spaccaroccia delle Rovine d'Alfa (come SS); Fossilunghia della Grotta Falesia → Fossilhelix/Ambra Vecchia | Scelta utente (2026-09-29) |
| D20 | **Mew** alla Torre Inclusa al posto di Groudon (lv 50), **sbloccato dopo la Lega** (non più con la Sfera Rossa dopo Red). Anche le stanze Kyogre/Rayquaza (irraggiungibili in HG) → Mew | Scelta utente 2026-09-29: dopo Red era troppo tardi. L'ingresso (Percorso 47) è raggiungibile già a metà gioco |
| D21 | **Celebi** al santuario del Bosco di Lecci **dopo la Lega**, catturato con la lotta "fatidica" (`ScrCmd_686`, esiste nel gioco ma non è usata): Celebi ha il flag evento ⇒ **il viaggio nel passato funziona** senza patch al codice | Scelta utente + proposta Claude |
| D25 | **Pichu Spunzorecchio** sbloccabile: dopo la Lega, Pichu qualsiasi in testa alla squadra al santuario. Fatto **solo nello script** (`GetPartyMonSpecies` al posto di `FollowerPokeIsEventTrigger EVENT_SPIKY_EARED_PICHU`): nessuna patch al codice | Scelta utente |
| D26 | Script modificati come **diff** sui sorgenti della decomp (`data/scripts/scr_seq_NNNN.diff`), assemblati da `tools/scrasm.py` | Nel repo solo differenze; assemblatore verificato 965/965 byte per byte |
| D28 | Nome: **"Pokémon Crystal Soul"** nel banner del DS, **"Versione Crystal Soul"** nel logo del titolo | Scelta utente 2026-09-30 |
| D31 | **Titolo in versione SoulSilver**: Lugia e cielo azzurro cristallo (il titolo legge la versione da gGameVersion = 0x020F566C; patch `ldrb r1,[r0]` → `mov r1,#8` nell'overlay 60, in codice.csv). Ho-Oh resta nell'intro (HG), Suicune è già nella scena 3 dell'intro | Richiesta utente: vedere sia Ho-Oh sia Lugia, sfondo azzurro |
| D33 | **Titolo: Ho-Oh o Lugia a caso** a ogni avvio: routine Thumb di 28 byte aggiunta in coda all'overlay 60 (posizione e salto calcolati al build: l'overlay 60 USA è 64 byte più lungo) (senza bss; nessun overlay caricato insieme parte dopo la sua fine), chiamata al posto di `ldr/ldrb gGameVersion`: 7 + ((VCOUNT + timer 3) & 1). La variante Ho-Oh usa le risorse SS copiate (`copia_membri.csv`: tavolozze, cielo, scintille) e lo stesso logo; scritta "Tocca per iniziare" ciano | Richiesta utente: alternare Ho-Oh e Lugia |
| D34 | **Intro scena 1: Ho-Oh poi Lugia** (`tools/intro.py`): sprite combinato nei membri 23-26 di a/2/6/2 (tile Ho-Oh + Lugia, tavolozza 2 = Lugia, celle 7-12 = Lugia, sequenza: Ho-Oh esce dal sole 36 fotogrammi (scala ~0.42), rientra (un fotogramma ogni 2), poi Lugia dal fotogramma 8). Codice ov060: 3 tavolozze invece di 2, comparsa subito (era 128), dissolvenza dopo 218 (era 90): durata della scena invariata, musica sincronizzata | Richiesta utente |
| D35 | **Suicune nel titolo**: sprite frontale di Suicune della ROM (a/0/0/4, file 245*6+3, decifrato: XOR con LCG, seme = prima parola), specchiato, disegnato nel cielo in basso a sinistra (membri 36/37 e copia 34/35). Colori: tavolozza del titolo, e per i colori senza equivalente (viola della criniera, rosso) i posti liberi 117-123 (124-126 usati dalla riga "Developed by") | Idea utente: in Cristallo il titolo aveva Suicune; nell'intro HGSS Suicune non compare (compaiono Entei e Raikou) |
| D36 | **Loghi disegnati dall'utente** (fatti con un'altra IA): ITA "Versione Cristallo Crystal Soul", ENG "Crystal Soul Version". `tools/prepara_logo.py` (Pillow, facoltativo) toglie lo sfondo bianco, ridimensiona nella zona del logo e scrive `locale/logo_titolo_ITA.png` / `_ENG.png` (cartella ignorata); il build sceglie quello della lingua della ROM di partenza e lo converte alla tavolozza del titolo (ITA 370 tile, ENG 387; massimo 512: tile da 0x0000, mappa SUB_2 a 0x8000). Suicune nel cielo disattivato con logo disegnato (si sovrapponeva): `SUICUNE_WITH_CUSTOM_LOGO` in logo.py | Scelta utente 2026-09-30 |
| D32 | **Ho-Oh e Lugia al livello 60** come in Cristallo (HG: 45/70), script 0021 e 0104 | Richiesta utente |
| D29 | **Versione inglese possibile**: `python tools/build.py --base IPKE` applica lo stesso design alla ROM USA (dati e script sono identici tra IPKI e IPKE); servono solo i testi in `data/testi/ENG/` | Verificato 2026-09-29: build IPKE con verifica a zero |
| D30 | **Pokédex di Johto = le 251**: tolte le 5 evoluzioni gen 4 e rinumerato 1-251 (a/1/3/8; lista "johto" = membro 12 di a/0/7/4 e a/2/1/4, il gioco ne legge la lunghezza come size/2). Codice (`data/design/codice.csv`, per contesto di byte, vale anche per USA): completamento con 249 catturati (era 254 = 256 - Mew - Celebi), messaggio di Oak "completo" sopra 248 (era 253) | Coerenza; senza le soglie il diploma sarebbe irraggiungibile |
| D27 | Flag nostri nel blocco **0x51F-0x54F** (mai usato né da script né dal codice C): `FLAG_PCN_CELEBI_CAUGHT` = 0x54E; Rocco: `FLAG_PCN_STEVEN_GREEN/RED/BLUE` = 0x54B-0x54D | Serve un flag permanente; MAPTEMP si azzera cambiando mappa |
| D22 | Oak (Kanto) e Rocco (Johto, D17) lasciano **tutte e 3 le Poké Ball**: si possono prendere tutti gli starter | Scelta utente (2026-09-29) |
| D23 | Radio Suono Hoenn/Sinnoh **neutra**: le sue specie = slot erba 2/4 (giorno) della stessa mappa | Proposta Claude, scelta di minimo impatto (la radio non può avere specie 0) |
| D24 | Tutte le altre specie > 251 (allenatori, Parco Lotta, Pokéathlon, Bottintesta, Safari, Gara) con la **tabella globale** `data/design/sostituzioni.csv` (242 righe riviste) | Coerenza; starter e leggendari mai negli incontri casuali |

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

## 5b. Scoperte della fase 2 (finora)
- **IPKI e IPKE hanno archivi di dati identici byte per byte** (SHA1): personal, mosse, oggetti, evoluzioni,
  learnset, incontri, allenatori, **script (a/0/1/2)**, eventi di zona, Safari, Bottintesta, scambi, Gara, uova.
  Differiscono solo testi (a/0/2/7) e a/0/7/4 (dati Pokédex, probabilmente ordine alfabetico).
  ⇒ la decomp pret (che ricostruisce la versione USA) documenta anche la ROM ITA: nomi mappe/allenatori e script in chiaro.
  Scaricata in `work/pret` con `tools/get_pret.py` (commit fissato 9d8b7591).
- Mappa archivi (da `filesystem.mk` della decomp): a/0/0/2 personal, a/0/1/1 mosse, a/0/1/2 script, a/0/1/7 oggetti,
  a/0/2/7 testi, a/0/3/2 eventi zona, a/0/3/3 learnset, a/0/3/4 evoluzioni, a/0/3/7 incontri HG (a/1/3/6 SS),
  a/0/5/5-6 allenatori, a/1/3/8 Pokédex Johto, a/2/2/9 mosse uovo, a/2/3/0 Safari, a/2/5/2 Bottintesta,
  **a/1/1/2 scambi** (`data/tradelist.narc` è grafica, non gli scambi: corretto 2026-09-29), `data/mushi/mushi_encount.bin` Gara Pigliamosche (4 tabelle × 10).
- **Parco Lotta**: a/2/0/3 (951 set) + a/2/0/2 (allenatori) = Torre Lotta (`unk_0204B538.c`); a/1/2/9 + a/1/2/8 stesso
  formato, altra struttura (codice non decompilato); a/2/0/4 (478 set, forse noleggi Factory). Circa metà dei set è gen 3-4.
  Set (16 B): specie, 4 mosse, EV, natura, strumento, forma. Allenatori (104 B): classe, numero set, indici dei set
  ⇒ per ripulire basta sostituire specie/mosse nei set gen 3-4, gli allenatori non si toccano.
- Archivi residui: a/0/6/6 = dati delle **bacche** (falso positivo, non sono specie); a/2/5/8 (100 voci × 3 specie,
  codice non decompilato; ipotesi: squadre avversarie del Pokéathlon, con 11 specie gen 3-4 tipo Swellow/Lucario/Staraptor);
  a/2/5/4 = photo_data.
- **Gara Pigliamosche**: tabella 0 prima del Nazionale; dopo, martedì/giovedì/sabato → tabelle 1/2/3
  (`overlay_bug_contest.c`). Le specie gen 3-4 (Wurmple, Nincada, Kricketot, Combee, …) sono solo nelle tabelle 2-3.
- **Radio** Suono Hoenn (mercoledì) / Suono Sinnoh (giovedì): solo con il Pokédex Nazionale (`pokemon_music.c`);
  sostituiscono gli slot erba 2-5.
- **Sciami**: attivati da Oak insieme al Nazionale (`EnableMassOutbreaks`, P01R0101); ogni giorno una di 20 mappe
  (`sSwarmMapLUT`, verificata in arm9 ITA). 12 sciami su 20 sono gen 3-4; gli altri 8 sono gen 1-2 (Marill, Dunsparce,
  Chansey, Qwilfish, Yanma, Snubbull, Remoraid, Ditto). I 4 u16 finali della tabella incontri sono: sciame erba,
  sciame surf, **pesca notturna** (sempre attiva, prima l'audit la contava come sciame), sciame pesca.
- **Pokédex di Johto** (a/1/3/8): è una tabella numero nazionale → numero di Johto (0 = assente), non una lista di specie.
  256 voci = tutte le 251 + 5 evoluzioni gen 4 (Yanmega J102, Ambipom J124, Lickilicky J181, Tangrowth J183,
  Mamoswine J197). Togliendole restano 5 buchi: da rinumerare (fase 4; controllare anche le liste di ordinamento in zkn_data).
- **Scambi in gioco** (13, a/1/1/2, 0x54 byte: specie data a 0x00, chiesta a 0x4C): Iron dà **Beldum**;
  Hornlette (dà Rhyhorn) **chiede Bonsly** (gen 4). Il resto è gen 1-2.
- **Script** (regali/statici): Ho-Oh (D17R0110, lv 45/70) e Lugia (D40R0107, lv 70/45) entrambi in HG.
  Rocco dà **Treecko/Torchic/Mudkip** lv 5 (T11R0701) → idea: sostituirli con **Chikorita/Cyndaquil/Totodile**
  (risolve i 2 starter di Johto mancanti). Torre Inclusa: Groudon (D52R0101), Kyogre (D52R0102), Rayquaza (D52R0103).
  Rovine di Sinjoh (D51R0201): Dialga/Palkia/Giratina (solo con Arceus evento). Lati: statico lv 40 a Plumbeopoli
  (T03, Pietrenigma evento) e vaganti (T06, CreateRoamer 2/3). Riferimenti cosmetici (versi, controlli party) a Chatot,
  Banette, Deoxys, Rotom, Togekiss: innocui.
- Oggetti negli script: Roccia di Re (Pozzo Slowpoke D26R0103), Metallopatina (M/N Acqua P01R0306). Squama Drago,
  Upgrade, Aromi, fossili **non** compaiono per costante: probabilmente item ball / oggetti nascosti / negozi nel codice.
  Il Museo di Plumbeopoli (T03R0101) rianima Ambra Vecchia, Helix, Dome: da verificare come si ottengono i fossili.

- **Primo giro audit** (controlli ROM↔decomp tutti OK: 142 tabelle selvatici, 12 aree Safari, 738/738 squadre allenatori
  identiche): **230/251 ottenibili**. Mancanti (21): esclusive SS (Vulpix, Ninetales, Meowth, Persian, Ledyba, Ledian,
  Teddiursa, Ursaring, Delibird, Skarmory), evoluzioni per scambio (Alakazam, Machamp, Golem, Gengar, Politoed, Slowking,
  Scizor, Kingdra, Porygon2), Mew, Celebi. Limite noto: i 3 starter di Johto sono contati tutti come ottenibili
  (in realtà 1 su 3) — da correggere nella matrice. → **Corretto** (vedi sotto).

- **Fonti degli oggetti** (`tools/items.py` → `docs/oggetti.md`; controlli tutti OK: tabella oggetti nascosti trovata
  in arm9, 491/491 mappe con oggetti a terra/nascosti uguali tra decomp e ROM, 14/14 tabelle del negozio Pokéathlon e
  3 tabelle Spaccaroccia trovate byte per byte nella ROM ITA):
  - Tutti gli **oggetti evolutivi delle 251** sono ottenibili in HG: pietre base (a terra, nonno di Bill R25R0101,
    negozio Pokéathlon), Pietrasolare (Pokéathlon, solo dopo il Nazionale), Roccia di Re (Pozzo Slowpoke + Pokéathlon),
    Metallopatina (M/N Acqua + Pokéathlon), **Squama Drago** (a terra al Monte Scodella 2F + Pokéathlon dopo il
    Nazionale), **Upgrade** (regalo della guardia a Zafferanopoli, T11R0701). ⇒ D7 fattibile in una partita.
  - **Fossili**: solo con Spaccaroccia. Rovine d'Alfa (30% di oggetto per roccia): Fossilhelix 10%, Ambra Vecchia 10%.
    **Il Domofossile in HG non esiste** (è nella tabella SS) ⇒ Kabuto/Kabutops mancano. Grotta Falesia: Fossilunghia
    (gen 3, da togliere). Radice/Corazza/Cranio: nessuna fonte in HG.
  - **Aromi** (D9): 9 strumenti a terra, uno per mappa (R15, R38, R47, T06, D01R0101, D03R0101/0102, D38R0102, D41R0102).
    Per toglierli basta cambiare l'oggetto delle voci di scr_seq_0141 corrispondenti.
  - Strumenti che servono solo a evoluzioni gen 4 (Protezione, Elettritore, Magmatore, Dubbiodisco, Rasoartiglio,
    Rasozanna, Pietra Ovale, Pietrabrillo/Neropietra/Pietralbore, Terrorpanno) restano innocui una volta tolte le
    evoluzioni (D8); si possono sostituire con altro se si vuole.
- **Starter di Kanto**: anche Oak (T01R0301, dopo aver battuto Red) ne dà **uno solo su 3** (le altre Poké Ball
  spariscono). L'audit ora tratta Oak e Rocco come scelte "1 su 3" ⇒ **216/251** (una famiglia per scelta).
  Catena post-game: Red → Oak (starter di Kanto) → Sig. Pokémon (Sfera Rossa, R30R0201) → Torre Inclusa (Groudon).
  Celebi: HGSS non ha la GS Ball; l'evento del santuario di Lecci richiede un Celebi evento ⇒ D10 richiede un incontro nuovo.
- **Audit corretto** (primo giro): un solo starter di Johto; fossili solo se presenti nelle tabelle Spaccaroccia; cercava
  `ITEM_UP_GRADE` invece di `ITEM_UPGRADE`. Risultato: **222/251** (con 1 famiglia di starter). Mancano 23 + 6 starter:
  esclusive SS (10), evoluzioni per scambio (9, D7), **Kabuto, Kabutops**, Mew, Celebi, + 2 famiglie di starter
  (idea: Rocco dà Chikorita/Cyndaquil/Totodile al posto degli starter di Hoenn). Nessuna delle 222 dipende solo da
  radio, sciami, bonus Safari o gara post-Nazionale.

## 6. Da verificare (fase 2)
Fase 2 chiusa: Safari, Bottintesta, Gara, script, radio, sciami, Pokédex di Johto, oggetti, Parco Lotta → §5b.
Restano per dopo:
- Evento del Santuario di Lecci (Celebi): leggere lo script quando si progetta D10.
- Pokédex di Johto: come si rinumera (tabella a/1/3/8 + eventuali liste di ordinamento in zkn_data).
- a/2/5/8: conferma che sia il Pokéathlon (in gioco o dal codice quando sarà decompilato).
- Percorsi NARC equivalenti su SoulSilver (alcuni differiscono) — solo per la fase 7.

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
1. **Utente**: provare `out/Pokemon Crystal Soul (ITA).nds` (ENG: `(ENG).nds`). Controlli nuovi: nome nel menu del DS; Rocco a Zafferanopoli
   (post-game): pietra verde/rossa/blu → Chikorita/Cyndaquil/Totodile, Rocco resta finché non li hai presi tutti e 3;
   Oak dopo Red: tutte e 3 le Poké Ball; dopo la Lega: Mew alla Torre Inclusa (sprite), Celebi al santuario di Lecci
   (lv 30) e poi viaggio nel passato con Celebi in testa, Pichu in testa al santuario.
2. Fase 4 — fatto: dati (`build.py`), script (`scrasm.py` + `scrpatch.py`, 8 script: 0092, 0133-0135, 0740 Oak,
   0776, 0825, 0837 Rocco), testi (`msg.py`, nessuna modifica per ora: il menu di Rocco usa i colori delle pietre),
   banner. `build.py --base IPKE` per la versione USA.
   Da fare:
   a. (Fatto: Pokédex di Johto, D30.) Il Pokédex Nazionale resta a 493 posti: le voci oltre 251 non si vedranno mai.
   b. (Fatto) BPS: corrispondenze a passo 4 dentro i file che cambiano (FAT) → 64 KB.
   c. (Fatto 2026-09-29) Testi: ricerca di nomi di specie 252-493 e di "Hoenn"/"Sinnoh" in tutti gli 829 archivi.
      Corretti (data/testi/ITA): Brock nella Grotta Diglett (scambio con Geodude), Rocco (scambio: Magnemite), museo di
      Plumbeopoli (Cuorugiada senza Lati), mosse eccelse (solo starter di Kanto/Johto), casa di Copiona (la bambola che
      si muove è un Ditto: sprite in oggetti_mappa.csv, verso in scr_seq_0841; arredi Cherrim/Nosepass senza nome).
      Oak: niente più catena della Sfera Rossa (i suoi testi su Groudon/Kyogre non si vedono più).
      Lasciati: citazioni delle sole regioni (Hoenn/Sinnoh esistono ancora), testi irraggiungibili (Sinjoh, Rotom,
      Shaymin, Manaphy, Piazza Wi-Fi, forme), discorso di Rocco sul suo Beldum/Metagross.
3. Pubblicazione della BPS in `patches/`: dopo i test.
4. Rifiniture (in corso):
   a. (Fatto) Logo: `tools/logo.py` parte dal logo SS della ROM (membro 1 di a/0/4/6, tavolozza 2), cancella
      "ARGENTO" e scrive "CRYSTAL" con lettere nostre (maschere nello script) colorate con la sfumatura della E
      originale; riga grande: "SOUL" + ala di Lugia centrati, senza "SILVER". build.py lo codifica (294 tile, <= 459)
      nei membri 1 e 0 (la mappa 0 era condivisa col logo HG, che non si usa più). Ritocchi possibili: trattino
      spurio sopra "SOUL", distanza ala/L.
   b. (Fatto) Lo "sfondo oro" era la schermata iniziale di una nuova partita / discorso di Oak (oaks_speech.c):
      tavolozze 1/30 (HG) di a/1/2/0 sostituite con 2/31 (SS) e spostate verso l'azzurro cristallo
      (`data/design/tavolozze.csv`, passo apply_palettes).
   b2. Logo rifatto a mano (idea utente: farlo ridisegnare): se esiste `locale/logo_titolo.png` (256x256, trasparente,
      cartella ignorata da git perché contiene il marchio ufficiale) il build lo usa al posto di quello generato,
      convertendolo alla tavolozza del logo SS (condivisa con il cielo del titolo). File di partenza per l'utente
      in work/per_utente/.
   c. (Fatto, D34) Intro scena 1: Ho-Oh poi Lugia. Da provare in melonDS. Titolo "ciclico" dentro la stessa
      schermata: richiederebbe codice nuovo per ricaricare i modelli 3D a metà schermata e una memoria che
      sopravviva al ricaricamento dell'overlay (Main_RunOverlayManager scarica/ricarica a ogni cambio). Per ora: a caso.
   d. Icona del banner.

## 12. Problemi aperti
- Nessuno bloccante.
