# Pokémon Crystal Soul

[English](README.md) · **Italiano**

Una hack di dati di **Pokémon Oro HeartGold** che mantiene motore, grafica e trama di HGSS, ma contiene **solo i 251
Pokémon della prima e della seconda generazione, tutti ottenibili in una sola partita**, senza scambi e senza altri
giochi. Un'esperienza "Pokémon Cristallo" con l'aspetto di HeartGold/SoulSilver.

Disponibile in **italiano** (da *Pokémon Oro HeartGold*, IPKI) e in **inglese** (da *Pokémon HeartGold* USA, IPKE).

> **Stato: beta.** I dati vengono verificati automaticamente a ogni build, ma una partita completa non è ancora
> stata fatta. Segnalazioni e commenti sono benvenuti (apri una issue: scrivi dov'eri e cosa hai fatto).

<p align="center">
  <img width="190" alt="Titolo: Ho-Oh" src="https://github.com/user-attachments/assets/7b3bd10a-350c-450b-81ce-65de93a9f8c1" />
  <img width="190" alt="Titolo: Lugia" src="https://github.com/user-attachments/assets/e14fdc9b-2246-483a-ab03-98fb75789436" />
  <img width="190" alt="Intro" src="https://github.com/user-attachments/assets/1dbdefda-0523-40e8-9597-186f658f160b" />
  <img width="190" alt="Starter" src="https://github.com/user-attachments/assets/58c2180c-ab8f-46d8-94cb-ba9984339ec1" />
</p>
<p align="center">
  <img width="190" alt="Borgo Foglianova" src="https://github.com/user-attachments/assets/5fdbb63e-2cf6-4d55-8fd6-a967c04e5d84" />
  <img width="190" alt="Percorso 29" src="https://github.com/user-attachments/assets/9dc3775c-1a75-40dd-9262-e9d9df050c94" />
  <img width="190" alt="Lotta" src="https://github.com/user-attachments/assets/887fed71-369c-4d6f-8e39-4b436707a926" />
</p>

## Novità

- **Solo i Pokémon dal n. 001 al 251, tutti ottenibili.** Nessuna specie di terza o quarta generazione da nessuna parte:
  incontri selvatici, sciami, alberi da Bottintesta, Zona Safari, Gara Pigliamosche, allenatori (Capipalestra,
  Superquattro, rivincite, Rosso), Parco Lotta, Pokéathlon, scambi con i personaggi.
- **Nessuno scambio necessario.** Kadabra, Machoke, Graveler e Haunter si evolvono al **livello 37**; Onix e
  Scyther (Metalcoperta), Seadra (Squama Drago), Slowpoke e Poliwhirl (Roccia di Re) e Porygon (Upgrade) si evolvono
  **usando lo strumento come una pietra evolutiva**. Tolte le evoluzioni verso specie di quarta generazione.
- **Tutti e due i leggendari di copertina:** Ho-Oh *e* Lugia nella stessa partita, entrambi al **livello 60** come
  in Cristallo.
- **Le esclusive di SoulSilver** (Vulpix, Meowth, Ledyba, Teddiursa, Delibird, Skarmory e le loro evoluzioni) sono
  selvatiche dove si trovano in SoulSilver.
- **Tutti gli starter:** il Prof. Oak (dopo Rosso) ti lascia prendere tutti e tre gli starter di Kanto; Rocco a
  Zafferanopoli (post-game) regala i due starter di Johto che non hai scelto da Elm, al posto di quelli di Hoenn.
- **Mitici senza eventi:** dopo la Lega Pokémon, **Mew** ti aspetta alla Torre Inclusa e **Celebi** al santuario del
  Bosco di Lecci (la storia del viaggio nel tempo funziona). Si può sbloccare anche **Pichu Spunzorecchio**.
- **Pokédex di Johto = le 251**, rinumerate, con diploma raggiungibile; anche il **diploma del Pokédex Nazionale**
  si ottiene con le 251 (Mew e Celebi non servono, come nel gioco originale).
- **Fossili:** Kabuto (Domofossile) alle Rovine d'Alfa come in SoulSilver; nella Grotta Falesia Helixfossile/Ambra Antica.
- **Nature senza effetto**, come in Cristallo dove non esistevano: ogni Pokémon ne ha ancora una, ma non cambia
  più le sue statistiche.
- **Uovo Strano** come in Cristallo: il nonno della Pensione sul Percorso 34 lo regala una volta (un baby Pokémon a
  caso che conosce Stordipugno, shiny nel 14% dei casi).
- **Musiche del Game Boy fin dall'inizio:** la mamma ti dà GB Sounds subito dopo il Pokégear; usalo dalla Borsa (o
  registralo sul tasto Y) per passare dalle musiche originali di Oro/Argento/Cristallo a quelle di HGSS e viceversa.
- **Suicune come in Cristallo:** si fa vedere anche sul **Percorso 36** davanti al cancello del Parco Nazionale, e
  fino alla Lega continua a ricomparire a giro (Fiorlisopoli, Percorso 42, Percorso 36); Eusine c'è solo la prima
  volta. Dopo la Lega la caccia di HGSS prosegue a Kanto come sempre.
- **Presentazione nuova:** logo "Crystal Soul", schermata del titolo con Ho-Oh e poi Lugia (cielo oro e cielo
  azzurro) e Suicune nell'angolo, intro con entrambi gli uccelli, icona azzurro cristallo nel menu del DS.
- **MT riutilizzabili:** insegnare una MT non la consuma più (come nelle generazioni successive).
- **Mantenuti da HGSS:** mosse, abilità, divisione fisico/speciale, Pokémon che ti seguono, grafica, musica e trama.

## Come giocare

Ti serve un **dump tuo** del gioco originale. Questo repository non contiene ROM e non ne conterrà mai.

| Patch | Gioco originale | SHA-1 del `.nds` originale |
|---|---|---|
| [`patches/Pokemon Crystal Soul (ITA).bps`](patches/) | Pokémon Oro HeartGold (ITA), IPKI | `6b7f9bff57eb58bc8d6e48e9e5c370719458c721` |
| [`patches/Pokemon Crystal Soul (ENG).bps`](patches/) | Pokémon HeartGold (USA), IPKE | `4fcded0e2713dc03929845de631d0932ea2b5a37` |

1. Controlla che il tuo `.nds` abbia lo SHA-1 qui sopra (lo controlla anche la patch, che rifiuta un file diverso).
2. Applica la `.bps` con un qualsiasi programma per patch BPS, per esempio
   [Rom Patcher JS](https://www.marcrobledo.com/RomPatcher.js/) (nel browser) o [Flips](https://github.com/Alcaro/Flips),
   oppure con questo repository:
   `python tools/bps.py applica ORIGINALE.nds "patches/Pokemon Crystal Soul (ITA).bps" USCITA.nds`
3. Gioca il `.nds` risultante con un emulatore (provato con **melonDS**) o su console. Inizia una **nuova partita**.

La patch contiene solo le differenze rispetto al gioco originale.

## Limiti noti

- Il Pokédex Nazionale ha ancora 493 posti (riempirai solo i primi 251).
- Pokéwalker, Migrazione dal GBA (quindi il Parco Amici resta vuoto), collegamento a Pokémon Ranger e Dono Segreto sono
  tolti dal menu principale, perché porterebbero specie oltre la 251. Gli scambi (locali, Wi-Fi, GTS) restano: con
  giochi non modificati possono ancora entrare altre specie; tra copie di Crystal Soul nessun problema.
- Gli eventi nuovi (giro di Suicune, Uovo Strano, Mew, Celebi e il viaggio nel tempo, Pichu, starter di Rocco e Oak)
  sono stati provati uno per uno con una versione di prova, ma non ancora in una partita completa. Salva prima di
  affrontarli.
- La versione inglese è costruita dagli stessi dati di quella italiana, ma è stata provata meno in gioco.

## Costruire la hack dai sorgenti

Tutto viene costruito da script partendo dalla tua ROM: Python 3 (solo libreria standard), nessuna modifica a mano.

```
python tools/roms.py          # metti le ROM in roms/ (riconosciute tramite SHA-1)
python tools/get_tools.py     # scarica dsrom 0.8.0 (hash verificato)
python tools/roundtrip.py     # estrae la ROM in work/
python tools/get_pret.py      # decompilazione pret (documentazione dei formati, script)
python tools/build.py         # versione italiana → out/  (inglese: --base IPKE)
python tools/build.py --debug # versione di prova con scorciatoie agli eventi nuovi (mai pubblicata): docs/DEBUG.md
```

Il design è in tabelle leggibili (`data/design/*.csv`), le modifiche agli script sono diff (`data/scripts/`), i testi
nuovi sono in `data/testi/`. Guida completa: [docs/SETUP.md](docs/SETUP.md). Diario del progetto e tutte le decisioni:
[NOTES.md](NOTES.md).

## Ringraziamenti

- [pret/pokeheartgold](https://github.com/pret/pokeheartgold): la decompilazione, usata come documentazione dei
  formati e degli script.
- [ds-rom (dsrom)](https://github.com/AetiasHax/ds-rom): estrazione e ricostruzione della ROM.
- [DSPRE](https://github.com/DS-Pokemon-Rom-Editor/DSPRE) e [melonDS](https://melonds.kuribo64.net): ispezione e prove.

## Licenza

Script, tabelle e documentazione di questo repository sono rilasciati con [licenza MIT](LICENSE).
Riguarda solo il lavoro originale del progetto, non Pokémon né i dati del gioco.

## Note legali

Progetto amatoriale non ufficiale, non affiliato né approvato da Nintendo, Game Freak, Creatures o The Pokémon
Company. Pokémon e tutti i nomi collegati sono marchi dei rispettivi proprietari. Qui non viene distribuito alcun
dato del gioco protetto da copyright: serve una copia legittima del gioco originale.
