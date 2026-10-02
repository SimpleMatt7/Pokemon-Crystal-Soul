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
squadra è vuota 30 Ultra Ball e 10 Master Ball, la MT10 (D55), l'Esp. Squadra (D56), tutte le 16 medaglie e (la prima volta, se c'è posto) un Pidgeot lv 40 (D60), poi porta sul posto. Si può usare subito dopo l'inizio di una partita nuova.

| Voce | Stato impostato | Arrivo | Cosa provare |
|---|---|---|---|
| Suicune giro | prima della Lega (`FLAG_GAME_CLEAR` tolto) | prossimo avvistamento attivo: Fiorlisopoli (176,335), Percorso 42 (460,184, da sud: 3 passi a nord) o Percorso 36 (382,242); se nessuno è attivo accende Fiorlisopoli | D50: un passo avanti → Suicune scappa (dal secondo giro senza Eusine). Dopo ogni avvistamento la ROM di prova riporta in cameretta (solo qui: patch in data/debug/scripts/ di 0875, 0252, 0243); sul Percorso 42 l'albero da tagliare, che sta proprio sul punto dell'avvistamento, viene tolto entrando nella mappa (0252, 0497); riscegliendo la voce si va al successivo: Fiorlisopoli → P.42 → P.36 → Fiorlisopoli... |
| Mew | lotta non ancora fatta | Torre Inclusa (stanza usata da HeartGold) | D20/D46: Mew in fondo alla stanza; lotta al livello 50; se scappi o lo sconfiggi ricompare rientrando (provato); catturato non ricompare |
| Celebi | Rocket della Radio sconfitti, Celebi non catturato | Bosco di Lecci, davanti al santuario | D21 (provato, funziona): esaminare il santuario → lotta con Celebi lv 30. Dopo la cattura: Celebi **primo in squadra** (menu Pokémon → Sposta) e riesaminare il santuario → deve partire il **viaggio nel passato** |
| Pichu | dà un Pichu lv 30 | come sopra | D25 (provato, funziona): Pichu deve essere **primo in squadra** (se avevi già Pokémon, spostalo in cima); esaminare il santuario → evento di Pichu Spunzorecchio |
| Oak (Kanto) | `VAR_UNK_4131 = 1` (dopo Rosso), Poké Ball visibili | Laboratorio di Oak, sulla porta (parte la scena di Oak: 5 passi a nord) | D22 (provato, funziona): si possono prendere tutte e tre le Poké Ball, una alla volta (la squadra non deve essere piena) |
| Rocco (Johto) | `VAR_UNK_4130 = 2`, `VAR_UNK_40FD = 1`, starter da Elm = Cyndaquil | Silph S.p.A. di Zafferanopoli | D17/D22/D47: il menu offre solo pietra verde e blu (Chikorita, Totodile), uno alla volta; Rocco se ne va dopo il secondo |
| Uovo Strano | uovo non ancora ricevuto (squadra non piena) | Percorso 34, due passi sotto il nonno della Pensione | D48/D53 (nella ROM di prova l'uovo è **sempre shiny** e si **schiude subito**: patch di debug su 0237): parlando col nonno → Uovo Strano (baby a caso tra Pichu, Cleffa, Igglybuff, Smoochum, Magby, Elekid, Tyrogue) con Stordipugno; la seconda volta fa da Pensione come sempre. Per vedere cosa nasce: camminare finché si schiude (o riscegliere la voce per un altro uovo) |
| Diplomi | Pokédex e Pokédex Nazionale, diplomi non ancora visti | Condominio di Azzurropoli, 3° piano, davanti all'ascensore (3,3): la prima volta parte la scena di Cetra; il game designer è al centro (8,5) | D51 (provato, funziona): prima segnare le 251 nel salvataggio (in cameretta: salvare, chiudere il gioco, `python tools/pokedex_sav.py segna "out/Pokemon Crystal Soul (ITA) DEBUG.sav"`, riaprire con Continua). Parlando col designer: diploma di Johto, poi diploma Nazionale. Dal PC (valutazione del Pokédex) Oak deve dire che il Nazionale è completo |
| (tasto B) | esce dal menu | — | il menu regge al massimo 8 voci: niente voce Esci |

Gli stati restano nel salvataggio della ROM di prova: per ripetere una prova basta riscegliere la voce.

**Stati salvati di melonDS**: valgono solo per la ROM con cui sono stati fatti. Dopo ogni ricostruzione i file
dentro la ROM si spostano e uno stato vecchio legge dati sbagliati (testi e finestre rovinati). Usare il salvataggio
del gioco.

## Nature neutre (D49)

Nel riepilogo di HGSS l'effetto della natura non si vede (niente colori, e le statistiche dipendono anche da IV/EV).
Per verificarlo: salvare in gioco e lanciare `python tools/verifica_nature.py "out/Pokemon Crystal Soul (ITA) DEBUG.sav"`
(o il salvataggio normale): per ogni Pokémon in squadra confronta le statistiche salvate con quelle calcolate con e
senza natura. I Pokémon creati o saliti di livello con la ROM nuova devono risultare "SENZA effetto".

## Musiche GB (D54)

In una partita nuova: dopo aver ricevuto lo starter da Elm, parlare con la mamma (piano terra): Pokégear, poi GB Sounds.
Con un salvataggio che ha già il Pokégear: la prima volta che si parla con la mamma arriva GB Sounds. Usarlo dalla Borsa:
le musiche passano a quelle di Oro/Argento/Cristallo, e di nuovo a quelle di HGSS.

## Esp. Squadra (D56)

Nel kit c'è l'Esp. Squadra (strumenti chiave). Borsa → Usa: deve dire accesa/spenta e cambiare a ogni uso (anche registrata sul tasto Y). Accesa, sconfiggendo un Pokémon: chi ha lottato riceve i Punti Esp. interi (con messaggio), gli altri della squadra la metà senza messaggio (si vedono solo gli aumenti di livello e le mosse nuove); i Pokémon esausti e le Uova niente. Per controllare i Punti Esp. degli altri: riepilogo del Pokémon prima e dopo la lotta. Spenta: solo chi ha lottato, come prima.

## Velocità del testo (D57)

Solo nelle partite nuove: Opzioni → Veloc. testo deve essere già su 3. I salvataggi esistenti tengono la loro impostazione.

## Assistente di Elm (D56)

Partita nuova: uscendo dal laboratorio con lo starter l'assistente dà 5 Pozioni e poi l'Esp. Squadra, con la spiegazione.

## MN senza mosse (D60)

Con un Pokémon che *può imparare* la MN ma non la conosce (Typhlosion: Taglio, Forza, Spaccaroccia, Scalaroccia; Pidgeot: Volo): davanti a un albero/masso/parete/acqua il gioco deve proporre la mossa. Menu Pokémon del Pidgeot: deve comparire Volo. Flash (D63): nel menu di un Pokémon che può impararla, per esempio il Pichu della voce omonima. Bottintesta: davanti a un albero da Bottintesta con un Pokémon che il maestro del Bosco di Lecci potrebbe istruire.
