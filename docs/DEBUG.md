# ROM di prova (debug)

`python tools/build.py --debug` (anche `--base IPKE`) costruisce `out/Pokemon Crystal Soul (ITA) DEBUG.nds`:
la stessa hack più alcune scorciatoie per provare in fretta le parti nuove. Le scorciatoie sono patch di script in
`data/debug/scripts/` applicate sopra a quelle normali. **Non si pubblica mai**: `--debug` e `--rilascio` insieme
sono rifiutati, e la patch in `patches/` viene sempre dalla build normale.

Usare un salvataggio a parte (per esempio copiando la ROM di debug con un altro nome): gli stati impostati dalle
scorciatoie restano nel salvataggio.

## Scorciatoie

| Dove | Cosa fa | Per provare |
|---|---|---|
| Cameretta del protagonista (Borgo Foglianova, 1° piano): esaminare l'oggetto a destra del PC | Imposta lo stato "Suicune visto sul Percorso 42" (`VAR_UNK_4092 = 2`) e porta nel corridoio sotto la piazzetta del cancello del Parco Nazionale (Percorso 36, 382,242) | D45: Suicune è nella piazzetta; un passo a **nord** (come arrivando giocando): punto esclamativo, Suicune grida, scappa verso nord e sparisce. Parlandoci scappa lo stesso. Dopo, uscendo e rientrando nel Percorso 36 non deve più esserci |

Si può usare subito dopo l'inizio di una partita nuova (anche senza Pokémon: la piazzetta non ha erba alta).
