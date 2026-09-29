# Fonti degli oggetti rilevanti — HeartGold ITA (IPKI)

Generato da `python tools/items.py`. Oggetti a terra/nascosti e tipo Spaccaroccia letti dalla ROM ITA; script e tabelle del codice dalla decomp pret, cercate byte per byte nella ROM ITA (controlli sotto). Solo nomi e ID.

## Controlli di coerenza ROM ↔ decomp

| Controllo | Esito | Dettaglio |
|---|---|---|
| Tabella oggetti nascosti (sHiddenItemParam) | OK | 231 voci, arm9.bin+0xFA4D0 |
| Eventi di zona: oggetti a terra/nascosti decomp = ROM | OK | 491/491 mappe |
| Negozio Pokéathlon per giorno: decomp = ROM | OK | 14/14 tabelle |
| Tabelle oggetti Spaccaroccia (HG): decomp = ROM | OK | Default, RuinsOfAlph, CliffCave |

## Riepilogo per oggetto

Le righe `script` sono punti in cui uno script prepara l'oggetto per darlo (regalo, premio, scambio con PL): il file indica la mappa. `tenuto da selvatici` = ottenibile con Furto/Covo o catturando.

| Oggetto | Categoria | Serve per | Fonti |
|---|---|---|---|
| FIRE_STONE | evoluzione 251 | Vulpix, Growlithe, Eevee | **negozio Pokéathlon**: prima del Nazionale: martedì; dopo il Nazionale: domenica, martedì, giovedì<br>**script**: 0217_R25R0101:182<br>**script**: 0217_R25R0101:277 |
| WATER_STONE | evoluzione 251 | Poliwhirl, Shellder, Staryu, Eevee | **a terra**: D11R0103 (Seafoam Islands B2F)<br>**negozio Pokéathlon**: prima del Nazionale: mercoledì; dopo il Nazionale: lunedì, martedì, mercoledì, venerdì<br>**script**: 0217_R25R0101:197<br>**script**: 0217_R25R0101:272 |
| THUNDERSTONE | evoluzione 251 | Pikachu, Eevee | **negozio Pokéathlon**: prima del Nazionale: giovedì; dopo il Nazionale: mercoledì, giovedì, sabato<br>**script**: 0217_R25R0101:192<br>**script**: 0217_R25R0101:282 |
| LEAF_STONE | evoluzione 251 | Gloom, Weepinbell, Exeggcute | **a terra**: D46R0101 (Viridian Forest)<br>**negozio Pokéathlon**: prima del Nazionale: sabato; dopo il Nazionale: martedì, giovedì, sabato<br>**script**: 0217_R25R0101:177<br>**script**: 0217_R25R0101:267 |
| MOON_STONE | evoluzione 251 | Nidorina, Nidorino, Clefairy, Jigglypuff | **a terra**: D45R0101 (Tohjo Falls)<br>**a terra**: D24R0213 (Ruins Of Alph Southeast Entrance Second Room)<br>**negozio Pokéathlon**: prima del Nazionale: lunedì; dopo il Nazionale: lunedì, mercoledì<br>**tenuto da selvatici**: Clefairy (5%), Clefable (5%), Cleffa (5%) |
| SUN_STONE | evoluzione 251 | Gloom (Bellossom), Sunkern | **negozio Pokéathlon**: dopo il Nazionale: domenica, lunedì, venerdì |
| KINGS_ROCK | evoluzione 251 | Poliwhirl (Politoed), Slowpoke (Slowking) — D7 | **negozio Pokéathlon**: prima del Nazionale: domenica; dopo il Nazionale: domenica, lunedì, giovedì<br>**script**: 0061_D26R0103:19<br>**tenuto da selvatici**: Poliwhirl (5%), Poliwrath (5%), Slowbro (5%), Politoed (5%), Slowking (5%) |
| METAL_COAT | evoluzione 251 | Onix, Scyther — D7 | **negozio Pokéathlon**: prima del Nazionale: venerdì; dopo il Nazionale: martedì, venerdì, sabato<br>**script**: 0161_P01R0306:73<br>**tenuto da selvatici**: Magnemite (5%), Magneton (5%), Steelix (5%) |
| DRAGON_SCALE | evoluzione 251 | Seadra — D7 | **a terra**: D38R0103 (Mount Mortar 2F)<br>**negozio Pokéathlon**: dopo il Nazionale: mercoledì, venerdì<br>**tenuto da selvatici**: Horsea (5%), Seadra (5%), Dratini (5%), Dragonair (5%), Dragonite (5%), Kingdra (5%) |
| UPGRADE | evoluzione 251 | Porygon — D7 | **script**: 0837_T11R0701:84 |
| HELIX_FOSSIL | fossile | Omanyte | **Spaccaroccia**: tabella RuinsOfAlph (10% per roccia con oggetto) — mappe: D24R0101 (Ruins Of Alph) 30% |
| DOME_FOSSIL | fossile | Kabuto | **nessuna trovata** |
| OLD_AMBER | fossile | Aerodactyl | **Spaccaroccia**: tabella RuinsOfAlph (10% per roccia con oggetto) — mappe: D24R0101 (Ruins Of Alph) 30% |
| ROOT_FOSSIL | fossile gen 3-4 | Lileep — da togliere | **nessuna trovata** |
| CLAW_FOSSIL | fossile gen 3-4 | Anorith — da togliere | **Spaccaroccia**: tabella CliffCave (20% per roccia con oggetto) — mappe: D50R0101 (Cliff Cave) 25% |
| ARMOR_FOSSIL | fossile gen 3-4 | Shieldon — da togliere | **nessuna trovata** |
| SKULL_FOSSIL | fossile gen 3-4 | Cranidos — da togliere | **nessuna trovata** |
| SEA_INCENSE | aroma (D9) | Marill → Azurill | **a terra**: D03R0101 (Cerulean Cave 1F) |
| LAX_INCENSE | aroma (D9) | Snorlax → Munchlax | **a terra**: R38 (Route 38) |
| ROSE_INCENSE | aroma (D9) | Roselia → Budew (gen 3-4, innocuo) | **a terra**: R15 (Route 15) |
| PURE_INCENSE | aroma (D9) | Chimecho → Chingling (gen 3-4, innocuo) | **a terra**: D41R0102 (Mount Silver Cave Upper Mountainside) |
| ROCK_INCENSE | aroma (D9) | Sudowoodo → Bonsly | **a terra**: D01R0101 (Diglett Cave) |
| ODD_INCENSE | aroma (D9) | Mr. Mime → Mime Jr. | **a terra**: D03R0102 (Cerulean Cave 2F) |
| LUCK_INCENSE | aroma (D9) | Chansey → Happiny | **a terra**: T06 (Vermilion) |
| WAVE_INCENSE | aroma (D9) | Mantine → Mantyke | **a terra**: R47 (Route 47) |
| FULL_INCENSE | aroma (D9) | Snorlax → Munchlax | **a terra**: D38R0102 (Mount Mortar 1F Back) |
| SHINY_STONE | solo gen 4 | Togetic → Togekiss (D8) | **a terra**: D22R0101 (National Park)<br>**a terra**: D22R0102 (National Park Bug Catching Contest)<br>**negozio Pokéathlon**: dopo il Nazionale: domenica, lunedì, mercoledì, giovedì, sabato |
| DUSK_STONE | solo gen 4 | Murkrow, Misdreavus (D8) | **a terra**: D03R0103 (Cerulean Cave B1F)<br>**negozio Pokéathlon**: dopo il Nazionale: lunedì, martedì, giovedì, venerdì, sabato |
| DAWN_STONE | solo gen 4 | Kirlia/Snorunt (gen 3) | **a terra**: D41R0102 (Mount Silver Cave Upper Mountainside)<br>**negozio Pokéathlon**: dopo il Nazionale: domenica, martedì, mercoledì, venerdì, sabato |
| OVAL_STONE | solo gen 4 | Happiny | **a terra**: D05R0102 (Rock Tunnel B1F)<br>**tenuto da selvatici**: Chansey (50%), Blissey (50%) |
| PROTECTOR | solo gen 4 | Rhydon (D8) | **a terra**: D38R0102 (Mount Mortar 1F Back) |
| ELECTIRIZER | solo gen 4 | Electabuzz (D8) | **a terra**: D03R0103 (Cerulean Cave B1F) |
| MAGMARIZER | solo gen 4 | Magmar (D8) | **a terra**: T09 (Cinnabar Island) |
| DUBIOUS_DISC | solo gen 4 | Porygon2 (D8) | **a terra**: R42 (Route 42) |
| RAZOR_CLAW | solo gen 4 | Sneasel (D8) | **script**: 0076_D32:540 |
| RAZOR_FANG | solo gen 4 | Gligar (D8) | **script**: 0076_D32:546 |
| REAPER_CLOTH | solo gen 4 | Dusclops | **a terra**: T31 (Mount Silver) |
| DEEPSEATOOTH | solo gen 3 | Clamperl | **nascosto**: W20 (Route 20) |
| DEEPSEASCALE | solo gen 3 | Clamperl | **nascosto**: W20 (Route 20)<br>**tenuto da selvatici**: Chinchou (5%), Lanturn (5%) |

## Spaccaroccia: tabelle complete (HeartGold)

- **Default**: MAX_ETHER 25%, REVIVE 20%, HEART_SCALE 10%, RED_SHARD 10%, BLUE_SHARD 10%, GREEN_SHARD 10%, YELLOW_SHARD 10%, STAR_PIECE 5%. Mappe: R03 (Route 3) 10%, T03 (Pewter) 20%, T06 (Vermilion) 25%, T22 (Violet) 50%, T24 (Cianwood) 20%, W19 (Route 19) 20%, D03R0101 (Cerulean Cave 1F) 25%, D42R0102 (Dark Cave Route 31 Side) 50%, D43R0103 (Victory Road 3F) 10%, D39R0104 (Ice Path B3F) 20%, D45R0102 (Tohjo Falls Hidden Room) 15%, D03R0102 (Cerulean Cave 2F) 20%, D03R0103 (Cerulean Cave B1F) 30%, D05R0102 (Rock Tunnel B1F) 30%, D41R0106 (Mount Silver Cave 2F) 25%.
- **RuinsOfAlph**: RED_SHARD 25%, YELLOW_SHARD 20%, HELIX_FOSSIL 10%, MAX_ETHER 10%, BLUE_SHARD 10%, GREEN_SHARD 10%, OLD_AMBER 10%, MAX_REVIVE 5%. Mappe: D24R0101 (Ruins Of Alph) 30%.
- **CliffCave**: MAX_ETHER 25%, PEARL 20%, BIG_PEARL 10%, RED_SHARD 10%, YELLOW_SHARD 10%, CLAW_FOSSIL 10%, CLAW_FOSSIL 10%, RARE_BONE 5%. Mappe: D50R0101 (Cliff Cave) 25%.

