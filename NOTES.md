# NOTES — diario di progetto

Ultimo aggiornamento: 2026-09-30 (titolo Ho-Oh → lampo → Lugia con cielo oro → azzurro, D39-D40; rifiniture: titolo SoulSilver (Lugia, cielo azzurro) con logo "Versione Crystal Soul"
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
- [x] Fase 5 — opzioni meccaniche: nature neutre (D49).
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
| D34 | **Intro scena 1: Ho-Oh e Lugia insieme** (`tools/intro.py`): sprite combinato nei membri 23-26 di a/2/6/2 (tile Ho-Oh + Lugia, tavolozza 2 = Lugia). Ho-Oh esce dal sole da solo (30 fotogrammi), poi Lugia spunta da dietro e i due si separano (12 fotogrammi, celle "coppia" con distanza crescente fino a 40), poi arrivano affiancati e grandi fino alla dissolvenza. Codice ov060: 3 tavolozze invece di 2, comparsa dopo 64 tick (era 128), dissolvenza dopo 154 (era 90): durata invariata, musica sincronizzata | Richiesta utente: vederli tutti e due grandi |
| D37 | **Loghi: "Pokémon" originale e colori originali**: sopra la riga di taglio (ITA y<100, ENG y<104, solo nella zona della parola) si usa la parola "Pokémon" del logo SS originale della stessa lingua; il resto del logo disegnato usa solo i colori delle scritte del logo originale (`ORIGINAL_STYLE`). prepara_logo allinea la parola gialla a quella originale della lingua (ITA x 37 y 42 larga 185; ENG x 31 y 47 larga 181) | Richiesta utente |
| D38 | **Testi inglesi** in `data/testi/ENG/` (stessi archivi e indici dell'italiano): la ROM USA è coerente | |
| D39 | **Titolo: Ho-Oh, lampo bianco, poi Lugia** (sostituisce D33, il "a caso"; checkpoint della versione a caso: tag `checkpoint-titolo-casuale`). `tools/titolo_ciclo.py`, passo del build: routine Thumb (~214 byte) in coda all'overlay 60 agganciata alla chiamata a `TitleScreenAnim_GetCameraNextPosition`; quando il giro di telecamera di Ho-Oh finisce (cameraScene torna a 0, versione 7): schermo bianco (MASTER_BRIGHT) e dissolvenza da bianco, scarica Ho-Oh e scintille, reinizializza gli allocatori a lista di texture e tavolozze del gestore VRAM 3D (le texture dei due non stanno insieme nei 128 KB del banco A; distruggere e ricreare il gestore rifà NNS_G3dInit e azzera proiezione/luci: schermo nero, provato), carica Lugia (20-24) e scintille SS (41-43), versione = 8, telecamera iniziale di Lugia. Durata del titolo 2340 → 2436 fotogrammi (Ho-Oh 1270 + Lugia 1146 + 20, simulazione esatta dello script di telecamera). Funzioni e indirizzi trovati per contenuto (vale per ITA e USA) | Richiesta utente: vederli tutti e due nel video del titolo |
| D40 | **Cielo del titolo alternato: oro con Ho-Oh, azzurro con Lugia**. Stessi tile del cielo azzurro; la tavolozza della variante HG (membro 4 di a/0/4/6) ha i colori 128-255 (solo cielo, il logo usa gli altri) rifatti su una sfumatura nei toni del cielo di HeartGold (`logo.gold_colors`, per luminosità). Al lampo (D39) la routine carica la tavolozza azzurra (membro 2: GfGfxLoader_GXLoadPal + PaletteData_LoadPaletteSlotFromHardware, perché il bagliore del logo rimanda la copia allo schermo) e il lampo bianco è su tutti e due gli schermi. Scritta "Tocca per iniziare": arancio originale HG con Ho-Oh (tolta la riga di codice.csv che la rendeva ciano), al lampo il colore 1 della tavolozza 2 principale (0x05000042) diventa il ciano SS | Richiesta utente |
| D41 | **Icona del banner**: la Poké Ball dorata di HeartGold in azzurro cristallo (tinta 195°, `BANNER_HUE` in build.py, immagine e tavolozza del banner ricolorate insieme) | Richiesta utente |
| D42 | **Menu principale invariato** (Pokéwalker, Ranger, Migrazione dal GBA, Dono Segreto restano). Provato a nasconderli, poi rimessi su scelta dell'utente: non si può chiudere tutto (scambi/GTS con giochi originali restano), giocando da soli non entrano specie oltre la 251. Il meccanismo resta pronto: `data/design/menu.csv` (tabella sMainMenuButtons dell'overlay 74; la funzione del pulsante punta a `sub_02074490` dell'ARM9, return 0). **Pokédex Nazionale non bloccato né accorciato**: sblocca contenuti post-Lega (prove di Baoba, suoni Hoenn/Sinnoh alla radio, Gara Pigliamosche) e la lista mostra solo fino alla specie più alta vista | Scelta utente |
| D43 | **Pubblicazione**: repository rinominato in `Pokemon-Crystal-Soul` (stesso repository, GitHub reindirizza il vecchio indirizzo); README inglese (`README.md`) e italiano (`README.it.md`); patch BPS in `patches/` con `build.py --rilascio`, verificate (applicate alle ROM originali danno le ROM costruite). Licenza **MIT** per il lavoro nostro (script, tabelle, note), non per Pokémon/dati del gioco; release GitHub rimandata a quando il repository diventa pubblico, dopo il playtest (es. v0.1-beta) | Richiesta utente 2026-09-30 |
| D44 | **Logo: scritta più piccola, ™ originale, Suicune nel titolo**. `prepara_logo.py` separa le parti del disegno (componenti collegate): "Pokémon" scalata come l'originale, ™ scartato (il build copia quello originale, `ORIG_TM` in logo.py), scritta sotto adattata al riquadro della scritta del logo SS originale della stessa lingua (ITA 216x58 da (24,107), ENG 203x49 da (37,111)), in italiano all'85% (`SUB_SCALE`) per lasciare spazio a Suicune. Suicune (sprite frontale, specchiato) di nuovo nell'angolo in basso a sinistra del cielo (`SUICUNE_WITH_CUSTOM_LOGO`); i suoi colori evitano quelli del cielo (128-255) così resta uguale col cielo oro | Richiesta utente |
| D45 | **Suicune anche sul Percorso 36**, come in Cristallo: davanti al cancello del Parco Nazionale, dopo l'avvistamento del Percorso 42 e prima di Aranciopoli. Catena HGSS: Fiorlisopoli (T24) mette `VAR_UNK_4092 = 1` → Percorso 42; ora il Percorso 42 mette `VAR_UNK_4092 = 2` (invece di accendere Aranciopoli) e lo script nuovo `scr_seq_R36_011` fa comparire/scappare Suicune e accende Aranciopoli (4092 = 0, 4070/4071 = 1, via `FLAG_HIDE_VERMILION_SUICUNE`) come faceva il Percorso 42. Oggetto 9 (sprite statico di Suicune, flag nostro 0x54A gestito dallo script di caricamento della mappa: visibile solo con 4092 = 2, vale anche per salvataggi già avviati) e due punti di attivazione (corridoio a sud x 380-383 z 241; colonna x 375 davanti al cancello) aggiunti da `data/design/eventi_zona.csv` (passo `apply_zone_events`, formato verificato sui file). Posizione scelta leggendo i permessi di movimento della mappa (land_data a/0/6/5, matrice 0). **ROM di prova**: `build.py --debug` (docs/DEBUG.md) | Richiesta utente; provato dall'utente con la ROM di prova (2026-09-30): funziona |
| D46 | **Correzione Mew (D20)**: in HeartGold la porta della Torre Inclusa (Percorso 47) porta alla stanza di **Kyogre** (D52R0102, MoveWarp per versione: HG = Sfera Blu/Kyogre, SS = Sfera Rossa/Groudon), non a quella di Groudon dove avevamo messo Mew: senza correzione Mew non sarebbe mai comparso. Ora anche D52R0102 (script 0134 + sprite in oggetti_mappa.csv, zona 477) mostra Mew dopo la Lega, come D52R0101. Trovato preparando il menu di prova (docs/DEBUG.md: menu nella cameretta per Suicune, Mew, Celebi, Pichu, Oak, Rocco) | Provato: funziona |
| D47 | **Rocco offre solo gli starter di Johto che mancano**: all'inizio del dialogo `GetStarterChoice` (specie scelta da Elm, `VAR_PLAYER_STARTER`) accende il flag nostro corrispondente (0x54B-0x54D) e le pietre già "usate" non compaiono nel menu; Rocco se ne va dopo gli altri due. Prove del post-game con la ROM di prova (utente, 2026-09-30): Suicune P.36, Mew (dopo la correzione D46), Celebi con viaggio nel tempo, Pichu Spunzorecchio, Oak, Rocco: tutto funziona | Richiesta utente |
| D48 | **Uovo Strano** come in Cristallo: il nonno della Pensione (Percorso 34, oggetto 10) usa `scr_seq_R34_013` invece di `std_daycare_man` (campo script in oggetti_mappa.csv): la prima volta, con posto in squadra, `GiveEgg` di un baby a caso (Pichu 9%, Cleffa 19%, Igglybuff 19%, Smoochum 16%, Magby 12%, Elekid 14%, Tyrogue 11%: tabella di Cristallo con le varianti shiny sommate, a memoria) e `SetMonMove` di Stordipugno nel primo posto libero (Tyrogue: al posto di Preveggenza); flag nostro 0x549; poi `CallStd std_daycare_man`. Testi 50-53 aggiunti a msg_0384 (ITA/ENG). **Niente probabilità di shiny più alta**: `GiveEgg` non la permette, servirebbe una patch al codice | Richiesta utente; provato con la ROM di prova: funziona |
| D49 | **Nature neutre** (opzione O1, D6 superata): la natura resta un'etichetta senza effetto sulle statistiche. Patch in `codice.csv`: prima istruzione di `ModifyStatByNature` (ARM9 0x6FE3C) da `cmp r2,#1` a `b` verso `return n`. Scartato l'azzeramento della tabella `gNatureStatMods` (0xFF5B1): stesso effetto, ma essendo più in fondo all'ARM9 compressa (BLZ) la ricompressione cambiava quasi tutto il file (BPS 891 KB invece di 457 KB). Il BPS ora cerca i blocchi spostati a ogni byte. I Pokémon già catturati ricalcolano le statistiche al primo aumento di livello (o evoluzione, caramella). Verificato su salvataggio con `tools/verifica_nature.py` (Totodile Ingenua, Pidgey Gentile: statistiche senza natura) | Scelta utente |
| D50 | **Giro degli avvistamenti di Suicune come in Cristallo, fino alla Lega**: Fiorlisopoli (VAR_UNK_4076 = 1) → Percorso 42 (VAR_UNK_4092 = 1) → Percorso 36 (4092 = 2) → di nuovo Fiorlisopoli... Il Percorso 36, se non c'è `FLAG_GAME_CLEAR`, rimette 4076 = 1 e mostra Suicune a Fiorlisopoli e accende il flag nostro `FLAG_PCN_SUICUNE_GIRO` (0x548): dal secondo giro Fiorlisopoli e Percorso 42 hanno la scena breve senza Eusine (in Cristallo Eusine compariva solo la prima volta a Fiorlisopoli). Dopo la Lega: il Percorso 36 accende Aranciopoli come prima; inoltre lo script di caricamento di Aranciopoli (T06_009), se il giro è ancora in corso, lo chiude e accende l'avvistamento di Aranciopoli, così non serve ritrovare Suicune a Johto. Salvataggi già oltre il Percorso 36: nessun cambiamento. Lettore delle mappe corretto: alcuni land_data hanno una sezione in più (u16 a 0x12) prima dei permessi. ROM di prova: voci «Suicune giro» e «Suicune Kanto» | Richiesta utente; provato (primo giro con Eusine, giro successivo senza, passaggio ad Aranciopoli dopo la Lega): funziona |
| D51 | **Diploma del Pokédex Nazionale con le 251**: `Pokedex_NationalDexIsComplete` (ARM9 0x29F40) chiede 249 catturati (251 meno Mew e Celebi, che il gioco non conta) invece di 484 (493 - 9 mitici): `mov r1,#0xF9` + nop al posto di `mov r1,#0x79; lsl r1,#2`. Vale per il diploma del game designer (Azzurropoli, Game Freak), per i complimenti di Oak in laboratorio e per la valutazione dal PC. `GetOakNationalDexRating` (0x5BC78): fasce riscalate su 249 (51/77/103/129/154/180/206/224/239/244/248, poi messaggio e fanfara del Pokédex completo). Verificato a codice e in gioco (2026-10-01): salvataggio della ROM di prova con le 251 segnate da `tools/pokedex_sav.py`, il game designer dà diploma di Johto e Nazionale | Richiesta utente |
| D52 | **Fonti esterne di specie oltre la 251 chiuse** (sostituisce D42): nel menu principale nascosti Pokéwalker, Dono Segreto, Collegamento a Pokémon Ranger e Migrazione dal GBA (quindi Parco Amici vuoto), con `data/design/menu.csv`. Restano gli scambi (locali, Wi-Fi, GTS): servono tra copie di Crystal Soul; bloccare solo le specie > 251 richiederebbe modifiche al codice della schermata di scambio. Motivo: con il diploma Nazionale raggiungibile con le 251 (D51) il Pokédex completo della hack è quello | Scelta utente; provato (menu principale): funziona |
| D53 | **Uovo Strano shiny al 14%** come in Cristallo: il comando di script 204 (`ScrCmd_BufferDPPtRivalStarterSpeciesName`, avanzo di Diamante/Perla mai usato, 80 byte all'ARM9 0x488F4; in ITA e USA uguali i primi 52 byte, usati come contesto, e uguali tutte le funzioni chiamate) è riscritto in Thumb (codice.csv): prende l'ultimo Pokémon della squadra e chiama `SetMonPersonality` (0x0207235C, trovata nel codice del Dono Segreto) con parte alta del PID = TID ^ SID ^ parte bassa, cioè shiny, con sesso e abilità invariati (cambia solo la natura, che non ha effetto). Lo script del nonno della Pensione lo chiama dopo `GiveEgg` se `Random 100 < 14`; le altre uova (Primo, Togepi) non passano di lì. ROM di prova: sempre shiny e schiusa immediata | Richiesta utente; provato: funziona |
| D54 | **Musiche GB dall'inizio**: GB Sounds (strumento chiave, dal Game Freak di Azzurropoli con la Medaglia Terra) lo regala la mamma subito dopo il Pokégear; a chi ha già il Pokégear ma non GB Sounds, la prima volta che le riparla. Si usa dalla Borsa o col tasto Y: attiva e disattiva le musiche di Oro/Argento/Cristallo. Testi 39-40 in msg_0545 (ITA/ENG). Il dipendente Game Freak, se lo hai già, dice la frase prevista dal gioco | Richiesta utente; provato: funziona |
| D55 | **MT riutilizzabili** (comodità moderna, stile gen 5): in `PartyMenu_LearnMoveToSlot` (ARM9 0x825A0, uguale in ITA e USA) il controllo `if (!MoveIsHM(move)) Bag_TakeItem(...)` salta sempre la chiamata (`bne` → `b`, codice.csv): le MT restano nella Borsa come le MN. Unico punto in cui il gioco consuma una MT (gli altri usi di MoveIsHM riguardano il dimenticare le MN). ROM di prova: il kit dà la MT10 | Richiesta utente; da provare |
| D56 | **Esp. Squadra** (Condividi Esperienza moderna, stile gen 6): strumento chiave che la accende/spegne; accesa, chi lotta riceve il 100% dei Punti Esp. e il resto della squadra (non esausti, non Uova) il 50%, con Uovo Fortunato, bonus allenatore e bonus scambio come prima; spenta tutto come l'originale. Strumento: la **Scheda Punti** (432, avanzo di DP mai dato da HGSS; il Portabolli e la Scatola Chic invece HGSS li usa) rinominata Esp. Squadra/Exp. All, icona del Condividi Esp. (tabella icone ARM9), descrizione nuova; si usa dalla Borsa o dal tasto Y perché entrambi passano da TryFormatRegisteredKeyItemUseMessage, il cui ramo della Scheda Punti ora inverte il flag nostro 0x54F e mostra msg_0010 129/130. Lotta (overlay 12): in BtlCmd_CalcExpGain l'effetto tenuto conta come Condividi Esp. per tutti e le due divisioni del ramo Condividi Esp. non dividono (metà Esp. a testa); in Task_GetExp ogni Pokémon è scelto e riceve la quota Condividi Esp. (chi ha lottato: metà + metà). Codice nuovo (176 byte) nella ARM9 al posto di ScrCmd_062 (nessuno script lo usa, raggiunto solo dalla tabella dei comandi, ora puntata a ScrCmd_Dummy). `tools/esp_squadra.py`, tutto trovato per contenuto (ITA e USA). Niente messaggio «ha guadagnato N Punti Esp.» per chi non ha lottato (Esp. Squadra accesa): la routine al posto del confronto «Esp. > 0» di Task_GetExp porta direttamente allo stato del controllo del livello, così aumenti di livello e mosse nuove si vedono ancora (come nei giochi recenti). Si ottiene dall'**assistente di Elm** insieme alle 5 Pozioni, uscendo dal laboratorio con lo starter (scr_seq_0843, testo 106 di msg_0543). ROM di prova: anche nel kit | Richiesta utente; interruttore provato (Borsa e Y), lotta da provare |
| D57 | **Velocità del testo 3 (veloce) di serie** nelle partite nuove: `Options_Init` (ARM9 0x2ACA8) mette textSpeed = 2 invece di 1 (codice.csv). Si può cambiare dalle Opzioni come prima | Richiesta utente; da provare |
| D58 | **Pulsanti «L=A» diventa «L=A R=B»** (Opzioni → Pulsanti): in `ApplyButtonModeToInput` (ARM9 0x1A6C2, caso BUTTONMODE_LEQUALSA, riscritto sul posto in 40 dei suoi 74 byte, codice.csv) per tasti tenuti/nuovi/ripetuti L aggiunge A e R aggiunge B, poi L e R vengono nascosti come prima: in quella modalità L e R erano già spenti in tutto il gioco, quindi non si perde niente. R tenuto = corsa con le Scarpe da corsa. Testo del pulsante: msg_0045 indice 19 | Richiesta utente (Ally X); da provare |
| D59 | **Titolo: primo uccello a caso, poi l'altro**. `titolo_ciclo.py`: al posto della lettura di gGameVersion in TitleScreen_Init la versione iniziale è 7 o 8 a caso (VCOUNT + timer 3, come D33) e viene ricordata in una parola in coda alla routine; a fine giro di telecamera si passa all'altro uccello una volta sola (Lugia → Ho-Oh: modelli 25-29, scintille 38-40, cielo dorato membro 4, scritta arancio nel colore 2 usato dalla variante SS). Durata invariata. **Suicune guarda a destra** (sprite non più specchiato, `logo.SUICUNE_MIRROR`) | Richiesta utente; da provare |
| — | Livelli dei Pokémon speciali confrontati con Cristallo: Suicune 40, Raikou/Entei 40 (vaganti), Lapras 20, Electrode 23, Snorlax 50, Sudowoodo 20, Gyarados rosso 30, Celebi 30 già uguali; Ho-Oh/Lugia portati a 60 (D32); Articuno/Zapdos/Moltres 50 e Mewtwo 70 non esistono in Cristallo (restano come in HGSS); Mew 50 (D20) | Verifica (2026-10-01) |
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
- **Flag nostri** (FLAG_UNK_54x, liberi nel gioco originale): 0x548 giro di Suicune (D50), 0x549 Uovo Strano (D48), 0x54A Suicune sul Percorso 36 (D45), 0x54B-0x54D starter di Rocco (D47), 0x54E Celebi catturato (D21), 0x54F Esp. Squadra (D56). Altri liberi: 0x51F-0x547 (D27); prima di usarne uno cercarlo anche in data/ e tools/
- **O2 — MN senza slot di mossa** (richiesta utente 2026-10-01, da discutere): nei giochi recenti Taglio, Surf ecc.
  non occupano più un posto tra le 4 mosse. Da valutare come renderle usabili fuori dalla lotta senza insegnarle.
- **O4 — Schermata del titolo**: fatto D59 (primo uccello a caso, Suicune verso destra).
- **O3 — Condividi Esperienza di squadra, stile moderno** (scelta utente 2026-10-01): strumento chiave che la
  accende/spegne; accesa, chi combatte prende il 100% e il resto della squadra il 50%. Implementato (D56).

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
3. (Fatto, D43) Pubblicazione: BPS in `patches/`, README IT/EN. Da aggiornare con `build.py --rilascio` dopo ogni modifica.
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
   c. (Fatto, D34) Intro scena 1: Ho-Oh poi Lugia. Da provare in melonDS. Titolo "ciclico": fatto (D39),
      Ho-Oh → lampo bianco → Lugia nella stessa schermata. Da provare in melonDS (se qualcosa si rompe: tag
      `checkpoint-titolo-casuale`).
   d. (Fatto, D41) Icona del banner.
   e. (Fatto) Grafiche per Steam ROM Manager: `tools/steam_art.py` → out/steam/<lingua>/ (poster 600x900, grid 920x430,
      hero 1920x620, logo, icona). Cielo del titolo oro/azzurro, sprite di Ho-Oh e Lugia, logo da locale/: solo uso personale.

## 11b. Revisione dei rischi (2026-09-30)
Verificato sui file costruiti o negli script:
- Parco Lotta: nessun allenatore scende sotto le specie distinte che aveva; per ogni allenatore esiste una squadra da 4
  con specie e strumenti diversi (doppi), tranne 2 casi speciali (classe 102) che erano identici già nell'originale.
- Allenatori (compresi doppi, rivincite, Lega e Red): numero di Pokémon invariato, specie <= 251, livelli coerenti.
- Script: tutti i riferimenti a specie > 251 rimasti sono innocui o irraggiungibili (Sinjoh/Lati solo con eventi,
  versi di Chatot/Deoxys, controlli su Rotom, Elm che accetta anche Togekiss); la variabile di Oak (4131) non è usata
  altrove in modo dipendente dal vecchio valore 6.
Da provare in gioco (non verificabile dai dati): sprite "da compagno" come oggetti delle mappe (Mew alla Torre Inclusa,
Ditto da Copiona: il gioco originale non lo fa mai, usa sprite "statici"); lotta fatidica di Celebi (ScrCmd_686, esiste
ma non è usata dal gioco originale) e viaggio nel passato; Pichu; Rocco/Oak con tutti e 3 gli starter.
(Fatto) Zone del Pokédex per le esclusive SS: a/1/3/3 (membro 2 + metodo*495 + specie, elenco u32 terminato da 0)
= unione degli elenchi HG e SS della decomp (build: apply_dex_areas; 36 elenchi; ROM = elenco HG verificato 3960/3960).
Limiti noti (non bloccanti): Pokédex Nazionale a 493 posti; Pokéwalker, Ranger, migrazione GBA e Dono Segreto nascosti dal
menu (D52); restano gli scambi/GTS con giochi originali.

## 12. Problemi aperti
- Nessuno bloccante.
