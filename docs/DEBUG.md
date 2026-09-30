# ROM di prova (debug)

`python tools/build.py --debug` (anche `--base IPKE`) costruisce `out/Pokemon Crystal Soul (ITA) DEBUG.nds`:
la stessa hack più alcune scorciatoie per provare in fretta le parti nuove. Le scorciatoie sono patch di script in
`data/debug/scripts/` applicate sopra a quelle normali. **Non si pubblica mai**: `--debug` e `--rilascio` insieme
sono rifiutati, e la patch in `patches/` viene sempre dalla build normale.

Usare un salvataggio a parte (per esempio copiando la ROM di debug con un altro nome): gli stati impostati dalle
scorciatoie restano nel salvataggio.

## Menu di prova

Nella cameretta del protagonista (Borgo Foglianova, 1° piano) esaminare la **console Wii** a destra del PC: compare
un menu. La console accende anche i pulsanti del menu del gioco (Borsa, Scheda, **Salva**, Opzioni; Pokémon quando dà il primo Pokémon): la prima volta,
subito dopo l'introduzione, esaminarla e scegliere Esci, poi **salvare in cameretta**. Con le ROM di prova successive
basta Continua (il salvataggio vale per tutte; gli stati salvati di melonDS no, vedi sotto). Ogni voce (tranne Suicune) imposta lo stato "dopo la Lega" (`FLAG_GAME_CLEAR`), dà un Typhlosion lv 70 se la
squadra è vuota 30 Ultra Ball e 10 Master Ball, poi porta sul posto. Si può usare subito dopo l'inizio di una partita nuova.

| Voce | Stato impostato | Arrivo | Cosa provare |
|---|---|---|---|
| Suicune P.36 | `VAR_UNK_4092 = 2` (dopo il Percorso 42) | Percorso 36, corridoio sotto il cancello del Parco Nazionale | D45: un passo a nord → Suicune scappa; parlandoci scappa lo stesso; rientrando non c'è più |
| Mew | lotta non ancora fatta | Torre Inclusa (stanza usata da HeartGold) | D20/D46: Mew in fondo alla stanza; lotta al livello 50; se scappi o lo sconfiggi ricompare rientrando (provato); catturato non ricompare |
| Celebi | Rocket della Radio sconfitti, Celebi non catturato | Bosco di Lecci, davanti al santuario | D21 (provato, funziona): esaminare il santuario → lotta con Celebi lv 30. Dopo la cattura: Celebi **primo in squadra** (menu Pokémon → Sposta) e riesaminare il santuario → deve partire il **viaggio nel passato** |
| Pichu | dà un Pichu lv 30 | come sopra | D25 (provato, funziona): Pichu deve essere **primo in squadra** (se avevi già Pokémon, spostalo in cima); esaminare il santuario → evento di Pichu Spunzorecchio |
| Oak (Kanto) | `VAR_UNK_4131 = 1` (dopo Rosso), Poké Ball visibili | Laboratorio di Oak, sulla porta (parte la scena di Oak: 5 passi a nord) | D22 (provato, funziona): si possono prendere tutte e tre le Poké Ball, una alla volta (la squadra non deve essere piena) |
| Rocco (Johto) | `VAR_UNK_4130 = 2`, `VAR_UNK_40FD = 1`, starter da Elm = Cyndaquil | Silph S.p.A. di Zafferanopoli | D17/D22/D47: il menu offre solo pietra verde e blu (Chikorita, Totodile), uno alla volta; Rocco se ne va dopo il secondo |
| Uovo Strano | uovo non ancora ricevuto (squadra non piena) | Percorso 34, due passi sotto il nonno della Pensione | D48: parlando col nonno → Uovo Strano (baby a caso tra Pichu, Cleffa, Igglybuff, Smoochum, Magby, Elekid, Tyrogue) con Stordipugno; la seconda volta fa da Pensione come sempre. Per vedere cosa nasce: camminare finché si schiude (o riscegliere la voce per un altro uovo) |
| Squadra di prova | Typhlosion (se vuota), Totodile, Chikorita, Pidgey lv 30 | resta in cameretta | D49: salvare e lanciare `tools/verifica_nature.py`: i Pokémon nuovi devono risultare SENZA effetto della natura |
| Esci | — | — | — |

Gli stati restano nel salvataggio della ROM di prova: per ripetere una prova basta riscegliere la voce.

**Stati salvati di melonDS**: valgono solo per la ROM con cui sono stati fatti. Dopo ogni ricostruzione i file
dentro la ROM si spostano e uno stato vecchio legge dati sbagliati (testi e finestre rovinati). Usare il salvataggio
del gioco.

## Nature neutre (D49)

Nel riepilogo di HGSS l'effetto della natura non si vede (niente colori, e le statistiche dipendono anche da IV/EV).
Per verificarlo: salvare in gioco e lanciare `python tools/verifica_nature.py "out/Pokemon Crystal Soul (ITA) DEBUG.sav"`
(o il salvataggio normale): per ogni Pokémon in squadra confronta le statistiche salvate con quelle calcolate con e
senza natura. I Pokémon creati o saliti di livello con la ROM nuova devono risultare "SENZA effetto".
