# Verifica del design (fase 3)

Generato da `python tools/design.py`: applica `data/design/*.csv` ai dati di IPKI in memoria. Nessuna ROM scritta.

## Obiettivi

- Specie > #251 rimaste: **0** ✔
- Ottenibili in una partita: **251/251** ✔

## Specie > #251 rimaste per fonte

| Fonte | Voci |
|---|---|
| selvatici | 0 |
| bottintesta | 0 |
| safari | 0 |
| gara | 0 |
| allenatori | 0 |
| scambi | 0 |
| script | 0 |
| Parco Lotta | 0 |
| Pokéathlon (a/2/5/8) | 0 |
| starter/leggendari negli incontri casuali | 0 |
| evoluzioni verso > 251 | 0 |
| evoluzioni impossibili da solo | 0 |

## Modifiche applicate (conteggio)

| Gruppo | Voci |
|---|---|
| evoluzioni | 27 |
| selvatici (dedicate) | 594 |
| bottintesta | 192 |
| safari | 279 |
| gara | 16 |
| allenatori | 132 |
| scambi | 2 |
| Parco Lotta | 1174 |
| script | 13 |

## Da dove arrivano le specie che mancavano

| # | Specie | Fonti |
|---|---|---|
| 001 | Bulbasaur | regalo [0740_T01R0301] |
| 002 | Ivysaur | evoluzione da Bulbasaur |
| 003 | Venusaur | evoluzione da Ivysaur |
| 004 | Charmander | regalo [0740_T01R0301] |
| 005 | Charmeleon | evoluzione da Charmander |
| 006 | Charizard | evoluzione da Charmeleon |
| 007 | Squirtle | regalo [0740_T01R0301] |
| 008 | Wartortle | evoluzione da Squirtle |
| 009 | Blastoise | evoluzione da Wartortle |
| 037 | Vulpix | selvatico |
| 038 | Ninetales | evoluzione da Vulpix |
| 052 | Meowth | selvatico |
| 053 | Persian | selvatico |
| 065 | Alakazam | evoluzione da Kadabra |
| 068 | Machamp | evoluzione da Machoke |
| 076 | Golem | evoluzione da Graveler |
| 094 | Gengar | evoluzione da Haunter |
| 140 | Kabuto | fossile DOME_FOSSIL (Spaccaroccia) rianimato [T03R0101] |
| 141 | Kabutops | evoluzione da Kabuto |
| 151 | Mew | statico [0133_D52R0101]; statico [0134_D52R0102]; statico [0135_D52R0103] |
| 152 | Chikorita | regalo [0837_T11R0701] |
| 153 | Bayleef | evoluzione da Chikorita |
| 154 | Meganium | evoluzione da Bayleef |
| 155 | Cyndaquil | regalo [0837_T11R0701] |
| 156 | Quilava | evoluzione da Cyndaquil |
| 157 | Typhlosion | evoluzione da Quilava |
| 158 | Totodile | regalo [0837_T11R0701] |
| 159 | Croconaw | evoluzione da Totodile |
| 160 | Feraligatr | evoluzione da Croconaw |
| 165 | Ledyba | bottintesta; gara coleottero t2 (dopo il Nazionale); gara coleottero t3 (dopo il Nazionale); selvatico |
| 166 | Ledian | gara coleottero t2 (dopo il Nazionale); safari (bonus oggetti); selvatico |
| 186 | Politoed | evoluzione da Poliwhirl |
| 199 | Slowking | evoluzione da Slowpoke |
| 208 | Steelix | safari (bonus oggetti); scambio (Rusty (Steelix)); selvatico |
| 212 | Scizor | evoluzione da Scyther |
| 216 | Teddiursa | bottintesta; selvatico |
| 217 | Ursaring | safari (bonus oggetti); selvatico |
| 225 | Delibird | selvatico |
| 227 | Skarmory | selvatico |
| 230 | Kingdra | evoluzione da Seadra |
| 233 | Porygon2 | evoluzione da Porygon |
| 251 | Celebi | nuovo evento [D36R0101 (santuario del Bosco di Lecci)] (dopo aver battuto la Lega; lotta 'fatidica' (ScrCmd_686) => Celebi con flag evento) |

## Da fare in fase 4 (build)

- Allenatori: se il sostituto non è coerente con il livello (es. forma base a livello alto), evolverlo o farlo regredire secondo i livelli di evoluzione; se l'allenatore ha mosse personalizzate, ricalcolarle dal learnset.
- Parco Lotta: sostituire anche le mosse dei set (le mosse dei set gen 3-4 potrebbero non essere imparabili).
- Pokédex di Johto: togliere le 5 voci gen 4 e rinumerare (tabella a/1/3/8 + liste di ordinamento).
- Oggetti D7 usabili come pietre (`uso_pietra` in oggetti.csv): campo uso sul campo nei dati oggetto.
- Script: Oak e Rocco con tutte e 3 le Poké Ball; Mew alla Torre Inclusa; Celebi al santuario; vaganti Lati tolti.
