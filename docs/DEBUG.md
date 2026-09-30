# ROM di prova (debug)

`python tools/build.py --debug` (anche `--base IPKE`) costruisce `out/Pokemon Crystal Soul (ITA) DEBUG.nds`:
la stessa hack più alcune scorciatoie per provare in fretta le parti nuove. Le scorciatoie sono patch di script in
`data/debug/scripts/` applicate sopra a quelle normali. **Non si pubblica mai**: `--debug` e `--rilascio` insieme
sono rifiutati, e la patch in `patches/` viene sempre dalla build normale.

Usare un salvataggio a parte (per esempio copiando la ROM di debug con un altro nome): gli stati impostati dalle
scorciatoie restano nel salvataggio.

## Menu di prova

Nella cameretta del protagonista (Borgo Foglianova, 1° piano) esaminare la **console Wii** a destra del PC: compare
un menu. Ogni voce (tranne Suicune) imposta lo stato "dopo la Lega" (`FLAG_GAME_CLEAR`), dà un Typhlosion lv 70 se la
squadra è vuota e 30 Ultra Ball, poi porta sul posto. Si può usare subito dopo l'inizio di una partita nuova.

| Voce | Stato impostato | Arrivo | Cosa provare |
|---|---|---|---|
| Suicune P.36 | `VAR_UNK_4092 = 2` (dopo il Percorso 42) | Percorso 36, corridoio sotto il cancello del Parco Nazionale | D45: un passo a nord → Suicune scappa; parlandoci scappa lo stesso; rientrando non c'è più |
| Mew | lotta non ancora fatta | Torre Inclusa (stanza usata da HeartGold) | D20/D46: Mew in fondo alla stanza; lotta al livello 50; se scappi o lo sconfiggi ricompare rientrando; catturato non ricompare |
| Celebi | Rocket della Radio sconfitti, Celebi non catturato | Bosco di Lecci, davanti al santuario (lato ovest) | D21: esaminare il santuario → lotta con Celebi lv 30. Dopo la cattura: Celebi **primo in squadra** (menu Pokémon → Sposta) e riesaminare il santuario → deve partire il **viaggio nel passato** |
| Pichu | dà un Pichu lv 30 | come sopra | D25: Pichu deve essere **primo in squadra** (se avevi già Pokémon, spostalo in cima); esaminare il santuario → evento di Pichu Spunzorecchio |
| Oak (Kanto) | `VAR_UNK_4131 = 1` (dopo Rosso), Poké Ball visibili | Laboratorio di Oak | D22: si possono prendere tutte e tre le Poké Ball, una alla volta (la squadra non deve essere piena) |
| Rocco (Johto) | `VAR_UNK_4130 = 2`, `VAR_UNK_40FD = 1`, starter non ancora presi | Silph S.p.A. di Zafferanopoli | D17/D22: parlando con Rocco, pietra verde/rossa/blu → Chikorita/Cyndaquil/Totodile, tutti e tre uno alla volta |
| Esci | — | — | — |

Gli stati restano nel salvataggio della ROM di prova: per ripetere una prova basta riscegliere la voce.
