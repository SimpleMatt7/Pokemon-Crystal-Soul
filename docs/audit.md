# Audit HeartGold ITA (IPKI) — specie > #251 e ottenibilità delle 251

Generato da `python tools/audit.py`. Dati letti da `work/IPKI` (ROM ITA estratta); nomi e script dalla decomp pret/pokeheartgold (commit in `tools/get_pret.py`). Contiene solo nomi e ID.

## Controlli di coerenza ROM ↔ decomp

| Controllo | Esito | Dettaglio |
|---|---|---|
| Nomi tabelle selvatici (gs_enc_data.json) | OK | 142 nomi / 142 tabelle |
| Layout Safari coerente con la decomp | OK | 12 aree |
| Nomi allenatori (trainers.json) | OK | 738 nomi / 738 allenatori |
| Squadre allenatori: decomp = ROM | OK | 738/738 identiche |


## Riepilogo: dove compaiono specie > #251

| Fonte | slot gen 3 | slot gen 4 | specie distinte |
|---|---|---|---|
| Selvatici — slot normali | 0 | 0 | 0 |
| Selvatici — radio Hoenn/Sinnoh | 225 | 199 | 19 |
| Selvatici — sciami | 10 | 2 | 12 |
| Bottintesta | 112 | 80 | 9 |
| Safari — base | 0 | 0 | 0 |
| Safari — bonus oggetti | 222 | 57 | 61 |
| Gara Pigliamosche | 10 | 6 | 11 |
| Allenatori | 65 | 67 | 99 |
| Scambi in gioco (ricevuti) | 0 | 0 | 10 |
| Script (regali/statici/vaganti) | 12 | 3 | 11 |
| Parco Lotta set A (con allenatori a/1/2/8) | 229 | 243 | 197 |
| Parco Lotta set B (con allenatori a/2/0/2) | 228 | 243 | 197 |
| Parco Lotta set C (478, probabilmente noleggi Factory) | 130 | 101 | 229 |
| Pokédex di Johto (voci) | 5 | 0 | 5 |


## Evoluzioni verso specie > #251 (da rimuovere, D8)

| Da | A | Metodo | Parametro |
|---|---|---|---|
| Magneton | Magnezone | CORONET | 0 |
| Lickitung | Lickilicky | HAS_MOVE | 205 |
| Rhydon | Rhyperior | TRADE_ITEM | ITEM_PROTECTOR |
| Tangela | Tangrowth | HAS_MOVE | 246 |
| Electabuzz | Electivire | TRADE_ITEM | ITEM_ELECTIRIZER |
| Magmar | Magmortar | TRADE_ITEM | ITEM_MAGMARIZER |
| Eevee | Leafeon | ETERNA | 0 |
| Eevee | Glaceon | ROUTE217 | 0 |
| Togetic | Togekiss | STONE | ITEM_SHINY_STONE |
| Aipom | Ambipom | HAS_MOVE | 458 |
| Yanma | Yanmega | HAS_MOVE | 246 |
| Murkrow | Honchkrow | STONE | ITEM_DUSK_STONE |
| Misdreavus | Mismagius | STONE | ITEM_DUSK_STONE |
| Gligar | Gliscor | ITEM_NIGHT | ITEM_RAZOR_FANG |
| Sneasel | Weavile | ITEM_NIGHT | ITEM_RAZOR_CLAW |
| Piloswine | Mamoswine | HAS_MOVE | 246 |
| Porygon2 | Porygon-Z | TRADE_ITEM | ITEM_DUBIOUS_DISC |


## Evoluzioni tra le 251 impossibili senza scambio (D7)

| Da | A | Metodo | Oggetto |
|---|---|---|---|
| Poliwhirl | Politoed | TRADE_ITEM | ITEM_KINGS_ROCK |
| Kadabra | Alakazam | TRADE | - |
| Machoke | Machamp | TRADE | - |
| Graveler | Golem | TRADE | - |
| Slowpoke | Slowking | TRADE_ITEM | ITEM_KINGS_ROCK |
| Haunter | Gengar | TRADE | - |
| Onix | Steelix | TRADE_ITEM | ITEM_METAL_COAT |
| Seadra | Kingdra | TRADE_ITEM | ITEM_DRAGON_SCALE |
| Scyther | Scizor | TRADE_ITEM | ITEM_METAL_COAT |
| Porygon | Porygon2 | TRADE_ITEM | ITEM_UPGRADE |


## Selvatici: radio e sciami per mappa

| Mappa | Categoria | Specie > 251 |
|---|---|---|
| D01R0101 | radio Hoenn | Makuhita, Absol |
| D01R0101 | radio Sinnoh | Chingling, Bronzor |
| D02R0101 | radio Hoenn | Makuhita, Absol |
| D02R0101 | radio Sinnoh | Chingling, Bronzor |
| D02R0102 | radio Hoenn | Makuhita, Absol |
| D02R0102 | radio Sinnoh | Chingling, Bronzor |
| D03R0101 | radio Hoenn | Makuhita, Absol |
| D03R0101 | radio Sinnoh | Chingling, Bronzor |
| D03R0102 | radio Hoenn | Makuhita, Absol |
| D03R0102 | radio Sinnoh | Chingling, Bronzor |
| D03R0103 | radio Hoenn | Makuhita, Absol |
| D03R0103 | radio Sinnoh | Chingling, Bronzor |
| D05R0101 | radio Hoenn | Makuhita, Absol |
| D05R0101 | radio Sinnoh | Chingling, Bronzor |
| D05R0102 | radio Hoenn | Makuhita, Absol |
| D05R0102 | radio Sinnoh | Chingling, Bronzor |
| D11R0101 | radio Hoenn | Makuhita, Absol |
| D11R0101 | radio Sinnoh | Chingling, Bronzor |
| D11R0102 | radio Hoenn | Makuhita, Absol |
| D11R0102 | radio Sinnoh | Chingling, Bronzor |
| D11R0103 | radio Hoenn | Makuhita, Absol |
| D11R0103 | radio Sinnoh | Chingling, Bronzor |
| D11R0104 | radio Hoenn | Makuhita, Absol |
| D11R0104 | radio Sinnoh | Chingling, Bronzor |
| D11R0105 | radio Hoenn | Makuhita, Absol |
| D11R0105 | radio Sinnoh | Chingling, Bronzor |
| D15R0102 | radio Hoenn | Zigzagoon, Spinda |
| D15R0102 | radio Sinnoh | Meditite, Chatot |
| D15R0103 | radio Hoenn | Zigzagoon, Spinda |
| D15R0103 | radio Sinnoh | Meditite, Chatot |
| D17R0102 | radio Hoenn | Zigzagoon, Spinda |
| D17R0102 | radio Sinnoh | Meditite, Chatot |
| D17R0103 | radio Hoenn | Zigzagoon, Spinda |
| D17R0103 | radio Sinnoh | Meditite, Chatot |
| D17R0104 | radio Hoenn | Zigzagoon, Spinda |
| D17R0104 | radio Sinnoh | Meditite, Chatot |
| D17R0105 | radio Hoenn | Zigzagoon, Spinda |
| D17R0105 | radio Sinnoh | Meditite, Chatot |
| D17R0106 | radio Hoenn | Zigzagoon, Spinda |
| D17R0106 | radio Sinnoh | Meditite, Chatot |
| D17R0107 | radio Hoenn | Zigzagoon, Spinda |
| D17R0107 | radio Sinnoh | Meditite, Chatot |
| D17R0108 | radio Hoenn | Zigzagoon, Spinda |
| D17R0108 | radio Sinnoh | Meditite, Chatot |
| D17R0109 | radio Hoenn | Zigzagoon, Spinda |
| D17R0109 | radio Sinnoh | Meditite, Chatot |
| D17R0112 | radio Hoenn | Zigzagoon, Spinda |
| D17R0112 | radio Sinnoh | Meditite, Chatot |
| D18R0101 | radio Hoenn | Zigzagoon, Spinda |
| D18R0101 | radio Sinnoh | Meditite, Chatot |
| D18R0102 | radio Hoenn | Zigzagoon, Spinda |
| D18R0102 | radio Sinnoh | Meditite, Chatot |
| D22R0101 | radio Hoenn | Plusle, Minun |
| D22R0101 | radio Sinnoh | Shinx×2 |
| D24R0101 | radio Hoenn | Linoone, Whismur |
| D24R0101 | radio Sinnoh | Bidoof, Buizel |
| D25R0101 | radio Hoenn | Makuhita, Absol |
| D25R0101 | radio Sinnoh | Chingling, Bronzor |
| D25R0102 | radio Hoenn | Makuhita, Absol |
| D25R0102 | radio Sinnoh | Chingling, Bronzor |
| D25R0103 | radio Hoenn | Makuhita, Absol |
| D25R0103 | radio Sinnoh | Chingling, Bronzor |
| D26R0102 | radio Hoenn | Makuhita, Absol |
| D26R0102 | radio Sinnoh | Chingling, Bronzor |
| D26R0103 | radio Hoenn | Makuhita, Absol |
| D26R0103 | radio Sinnoh | Chingling, Bronzor |
| D36R0101 | radio Hoenn | Numel, Spoink |
| D36R0101 | radio Sinnoh | Budew, Carnivine |
| D38R0101 | radio Hoenn | Makuhita, Absol |
| D38R0101 | radio Sinnoh | Chingling, Bronzor |
| D38R0102 | radio Hoenn | Makuhita, Absol |
| D38R0102 | radio Sinnoh | Chingling, Bronzor |
| D38R0103 | radio Hoenn | Makuhita, Absol |
| D38R0103 | radio Sinnoh | Chingling, Bronzor |
| D38R0104 | radio Hoenn | Makuhita, Absol |
| D38R0104 | radio Sinnoh | Chingling, Bronzor |
| D39R0101 | radio Hoenn | Makuhita, Absol |
| D39R0101 | radio Sinnoh | Chingling, Bronzor |
| D39R0102 | radio Hoenn | Makuhita, Absol |
| D39R0102 | radio Sinnoh | Chingling, Bronzor |
| D39R0103 | radio Hoenn | Makuhita, Absol |
| D39R0103 | radio Sinnoh | Chingling, Bronzor |
| D39R0104 | radio Hoenn | Makuhita, Absol |
| D39R0104 | radio Sinnoh | Chingling, Bronzor |
| D40R0101 | radio Hoenn | Makuhita, Absol |
| D40R0101 | radio Sinnoh | Chingling, Bronzor |
| D40R0102 | radio Hoenn | Makuhita, Absol |
| D40R0102 | radio Sinnoh | Chingling, Bronzor |
| D40R0104 | radio Hoenn | Makuhita, Absol |
| D40R0104 | radio Sinnoh | Chingling, Bronzor |
| D40R0106 | radio Hoenn | Makuhita, Absol |
| D40R0106 | radio Sinnoh | Chingling, Bronzor |
| D41R0101 | radio Hoenn | Makuhita, Absol |
| D41R0101 | radio Sinnoh | Chingling, Bronzor |
| D41R0102 | radio Hoenn | Makuhita, Absol |
| D41R0102 | radio Sinnoh | Chingling, Bronzor |
| D41R0103 | radio Hoenn | Makuhita, Absol |
| D41R0103 | radio Sinnoh | Chingling, Bronzor |
| D41R0104 | radio Hoenn | Makuhita, Absol |
| D41R0104 | radio Sinnoh | Chingling, Bronzor |
| D41R0105 | radio Hoenn | Makuhita, Absol |
| D41R0105 | radio Sinnoh | Chingling, Bronzor |
| D41R0106 | radio Hoenn | Makuhita, Absol |
| D41R0106 | radio Sinnoh | Chingling, Bronzor |
| D41R0107 | radio Hoenn | Makuhita, Absol |
| D41R0107 | radio Sinnoh | Chingling, Bronzor |
| D42R0101 | radio Hoenn | Makuhita, Absol |
| D42R0101 | radio Sinnoh | Chingling, Bronzor |
| D42R0102 | radio Hoenn | Makuhita, Absol |
| D42R0102 | radio Sinnoh | Chingling, Bronzor |
| D43R0101 | radio Hoenn | Makuhita, Absol |
| D43R0101 | radio Sinnoh | Chingling, Bronzor |
| D43R0102 | radio Hoenn | Makuhita, Absol |
| D43R0102 | radio Sinnoh | Chingling, Bronzor |
| D43R0103 | radio Hoenn | Makuhita, Absol |
| D43R0103 | radio Sinnoh | Chingling, Bronzor |
| D45R0101 | radio Hoenn | Makuhita, Absol |
| D45R0101 | radio Sinnoh | Chingling, Bronzor |
| D46R0101 | radio Hoenn | Numel, Spoink |
| D46R0101 | radio Sinnoh | Budew, Carnivine |
| D46R0101 | sciami | Kricketot |
| D47R0102 | radio Hoenn | Zigzagoon×2 |
| D47R0102 | radio Sinnoh | Bidoof×2 |
| D50R0101 | radio Hoenn | Makuhita, Absol |
| D50R0101 | radio Sinnoh | Chingling, Bronzor |
| R01 | radio Hoenn | Plusle, Minun |
| R01 | radio Sinnoh | Shinx×2 |
| R01 | sciami | Poochyena |
| R02 | radio Hoenn | Plusle, Minun |
| R02 | radio Sinnoh | Shinx×2 |
| R02R0101 | radio Hoenn | Plusle, Minun |
| R02R0101 | radio Sinnoh | Shinx×2 |
| R03 | radio Hoenn | Plusle, Minun |
| R03 | radio Sinnoh | Shinx×2 |
| R03 | sciami | Baltoy |
| R04 | radio Hoenn | Linoone, Whismur |
| R04 | radio Sinnoh | Bidoof, Buizel |
| R05 | radio Hoenn | Plusle, Minun |
| R05 | radio Sinnoh | Shinx×2 |
| R06 | radio Hoenn | Linoone, Whismur |
| R06 | radio Sinnoh | Bidoof, Buizel |
| R07 | radio Hoenn | Plusle, Minun |
| R07 | radio Sinnoh | Shinx×2 |
| R08 | radio Hoenn | Plusle, Minun |
| R08 | radio Sinnoh | Shinx×2 |
| R09 | radio Hoenn | Linoone, Whismur |
| R09 | radio Sinnoh | Bidoof, Buizel |
| R09 | sciami | Sableye |
| R10 | radio Hoenn | Linoone, Whismur |
| R10 | radio Sinnoh | Bidoof, Buizel |
| R11 | radio Hoenn | Plusle, Minun |
| R11 | radio Sinnoh | Shinx×2 |
| R12 | sciami | Relicanth |
| R13 | radio Hoenn | Linoone, Whismur |
| R13 | radio Sinnoh | Bidoof, Buizel |
| R14 | radio Hoenn | Plusle, Minun |
| R14 | radio Sinnoh | Shinx×2 |
| R15 | radio Hoenn | Plusle, Minun |
| R15 | radio Sinnoh | Shinx×2 |
| R16R0301 | radio Hoenn | Plusle, Minun |
| R16R0301 | radio Sinnoh | Shinx×2 |
| R17 | radio Hoenn | Plusle, Minun |
| R17 | radio Sinnoh | Shinx×2 |
| R18 | radio Hoenn | Plusle, Minun |
| R18 | radio Sinnoh | Shinx×2 |
| R22 | radio Hoenn | Linoone, Whismur |
| R22 | radio Sinnoh | Bidoof, Buizel |
| R24 | radio Hoenn | Linoone, Whismur |
| R24 | radio Sinnoh | Bidoof, Buizel |
| R25 | radio Hoenn | Linoone, Whismur |
| R25 | radio Sinnoh | Bidoof, Buizel |
| R25 | sciami | Buneary |
| R26 | radio Hoenn | Linoone, Whismur |
| R26 | radio Sinnoh | Bidoof, Buizel |
| R27 | radio Hoenn | Linoone, Whismur |
| R27 | radio Sinnoh | Bidoof, Buizel |
| R27 | sciami | Luvdisc |
| R28 | radio Hoenn | Linoone, Whismur |
| R28 | radio Sinnoh | Bidoof, Buizel |
| R29 | radio Hoenn | Plusle, Minun |
| R29 | radio Sinnoh | Shinx×2 |
| R30 | radio Hoenn | Linoone, Whismur |
| R30 | radio Sinnoh | Bidoof, Buizel |
| R31 | radio Hoenn | Linoone, Whismur |
| R31 | radio Sinnoh | Bidoof, Buizel |
| R32 | radio Hoenn | Linoone, Whismur |
| R32 | radio Sinnoh | Bidoof, Buizel |
| R33 | radio Hoenn | Plusle, Minun |
| R33 | radio Sinnoh | Shinx×2 |
| R34 | radio Hoenn | Linoone, Whismur |
| R34 | radio Sinnoh | Bidoof, Buizel |
| R34 | sciami | Ralts |
| R35 | radio Hoenn | Linoone, Whismur |
| R35 | radio Sinnoh | Bidoof, Buizel |
| R36 | radio Hoenn | Plusle, Minun |
| R36 | radio Sinnoh | Shinx×2 |
| R37 | radio Hoenn | Plusle, Minun |
| R37 | radio Sinnoh | Shinx×2 |
| R38 | radio Hoenn | Plusle, Minun |
| R38 | radio Sinnoh | Shinx×2 |
| R39 | radio Hoenn | Plusle, Minun |
| R39 | radio Sinnoh | Shinx×2 |
| R42 | radio Hoenn | Linoone, Whismur |
| R42 | radio Sinnoh | Bidoof, Buizel |
| R43 | radio Hoenn | Linoone, Whismur |
| R43 | radio Sinnoh | Bidoof, Buizel |
| R44 | radio Hoenn | Linoone, Whismur |
| R44 | radio Sinnoh | Bidoof, Buizel |
| R45 | radio Hoenn | Linoone, Whismur |
| R45 | radio Sinnoh | Bidoof, Buizel |
| R45 | sciami | Swablu |
| R46 | radio Hoenn | Plusle, Minun |
| R46 | radio Sinnoh | Shinx×2 |
| R47 | radio Hoenn | Linoone, Whismur |
| R47 | radio Sinnoh | Bidoof, Buizel |
| R48 | radio Hoenn | Plusle, Minun |
| R48 | radio Sinnoh | Shinx×2 |
| T06 | sciami | Wingull |
| T22 | sciami | Whiscash |
| T31 | radio Hoenn | Linoone, Whismur |
| T31 | radio Sinnoh | Bidoof, Buizel |
| W19 | sciami | Clamperl |
| W21 | radio Hoenn | Linoone, Whismur |
| W21 | radio Sinnoh | Bidoof, Buizel |


## Bottintesta

Tabelle con alberi: 60. Voci con specie > 251: 192.
| Mappa | Gruppo | Specie |
|---|---|---|
| D22R0101 | segreto | Cherubi×4 |
| D46R0101 | comune | Seedot×2, Shroomish |
| D46R0101 | raro | Seedot×2, Shroomish |
| R01 | comune | Wurmple×3 |
| R01 | raro | Wurmple×3 |
| R02 | comune | Wurmple×3 |
| R02 | raro | Wurmple×3 |
| R02R0101 | comune | Wurmple×3 |
| R02R0101 | raro | Wurmple×3 |
| R03 | comune | Wurmple×3 |
| R03 | raro | Wurmple×3 |
| R04 | comune | Wurmple×3 |
| R04 | raro | Wurmple×3 |
| R05 | comune | Combee×3 |
| R05 | raro | Combee×3 |
| R06 | comune | Combee×3 |
| R06 | raro | Combee×3 |
| R07 | comune | Combee×3 |
| R07 | raro | Combee×3 |
| R08 | comune | Combee×3 |
| R08 | raro | Combee×3 |
| R11 | comune | Combee×3 |
| R11 | raro | Combee×3 |
| R12 | comune | Wurmple×3 |
| R12 | raro | Wurmple×3 |
| R13 | comune | Wurmple×3 |
| R13 | raro | Wurmple×3 |
| R14 | comune | Wurmple×3 |
| R14 | raro | Wurmple×3 |
| R15 | comune | Wurmple×3 |
| R15 | raro | Wurmple×3 |
| R16 | comune | Combee×3 |
| R16 | raro | Combee×3 |
| R16R0301 | comune | Combee×3 |
| R16R0301 | raro | Combee×3 |
| R18 | comune | Wurmple×3 |
| R18 | raro | Wurmple×3 |
| R22 | comune | Wurmple×3 |
| R22 | raro | Wurmple×3 |
| R25 | comune | Combee×3 |
| R25 | raro | Combee×3 |
| R25 | segreto | Slakoth×4, Combee×2 |
| R38 | segreto | Burmy×4 |
| T01 | comune | Wurmple×3 |
| T01 | raro | Wurmple×3 |
| T02 | comune | Wurmple×3 |
| T02 | raro | Wurmple×3 |
| T03 | comune | Wurmple×3 |
| T03 | raro | Wurmple×3 |
| T03 | segreto | Starly×4, Wurmple×2 |
| T04 | comune | Combee×3 |
| T04 | raro | Combee×3 |
| T06 | comune | Combee×3 |
| T06 | raro | Combee×3 |
| T07 | comune | Combee×3 |
| T07 | raro | Combee×3 |
| T08 | comune | Wurmple×3 |
| T08 | raro | Wurmple×3 |
| T21 | segreto | Taillow×4 |
| W21 | comune | Wurmple×3 |
| W21 | raro | Wurmple×3 |


## Safari

| Area | Categoria | Tipo | Condizione | Specie > 251 |
|---|---|---|---|---|
| SAFARI_ZONE_AREA_DESERT | land | bonus | oggetti tipo 1×14 | Spinda×3 |
| SAFARI_ZONE_AREA_DESERT | land | bonus | oggetti tipo 1×49 | Carnivine×3 |
| SAFARI_ZONE_AREA_DESERT | land | bonus | oggetti tipo 2×35 | Cacnea×3 |
| SAFARI_ZONE_AREA_DESERT | land | bonus | oggetti tipo 2×49 | Vibrava×3 |
| SAFARI_ZONE_AREA_DESERT | land | bonus | oggetti tipo 3×28 | Hippopotas×3 |
| SAFARI_ZONE_AREA_DESERT | land | bonus | oggetti tipo 3×49 | Trapinch×3 |
| SAFARI_ZONE_AREA_DESERT | land | bonus | oggetti tipo 4×42 | Cacturne×3 |
| SAFARI_ZONE_AREA_DESERT | land | bonus | oggetti tipo 4×8 | Lotad×3 |
| SAFARI_ZONE_AREA_DESERT | surf | bonus | oggetti tipo 2×20 | Surskit×6 |
| SAFARI_ZONE_AREA_FOREST | land | bonus | oggetti tipo 1×24 | Budew×3 |
| SAFARI_ZONE_AREA_FOREST | land | bonus | oggetti tipo 2×35 | Shuppet×3 |
| SAFARI_ZONE_AREA_FOREST | land | bonus | oggetti tipo 3×56 + tipo 2×35 | Bronzong×3 |
| SAFARI_ZONE_AREA_FOREST | land | bonus | oggetti tipo 3×63 | Beldum×3 |
| SAFARI_ZONE_AREA_FOREST | land | bonus | oggetti tipo 4×10 | Bidoof×3 |
| SAFARI_ZONE_AREA_FOREST | land | bonus | oggetti tipo 4×24 | Surskit×3 |
| SAFARI_ZONE_AREA_FOREST | surf | bonus | oggetti tipo 2×20 | Surskit×6 |
| SAFARI_ZONE_AREA_MARSHLAND | land | bonus | oggetti tipo 1×35 | Seviper×3 |
| SAFARI_ZONE_AREA_MARSHLAND | land | bonus | oggetti tipo 2×35 | Carnivine×3 |
| SAFARI_ZONE_AREA_MARSHLAND | land | bonus | oggetti tipo 2×42 | Croagunk×3 |
| SAFARI_ZONE_AREA_MARSHLAND | land | bonus | oggetti tipo 2×49 | Roselia×3 |
| SAFARI_ZONE_AREA_MARSHLAND | land | bonus | oggetti tipo 3×49 | Banette×3 |
| SAFARI_ZONE_AREA_MARSHLAND | superrod | bonus | oggetti tipo 4×4 | Barboach×3 |
| SAFARI_ZONE_AREA_MARSHLAND | superrod | bonus | oggetti tipo 4×5 | Barboach×3 |
| SAFARI_ZONE_AREA_MEADOW | land | bonus | oggetti tipo 1×35 | Seedot×3 |
| SAFARI_ZONE_AREA_MEADOW | land | bonus | oggetti tipo 2×28 | Nuzleaf×3 |
| SAFARI_ZONE_AREA_MEADOW | land | bonus | oggetti tipo 2×35 | Nuzleaf×3 |
| SAFARI_ZONE_AREA_MEADOW | land | bonus | oggetti tipo 3×35 | Nosepass×3 |
| SAFARI_ZONE_AREA_MEADOW | land | bonus | oggetti tipo 3×42 + tipo 2×28 | Riolu×3 |
| SAFARI_ZONE_AREA_MEADOW | surf | bonus | oggetti tipo 4×10 | Masquerain×3 |
| SAFARI_ZONE_AREA_MEADOW | surf | bonus | oggetti tipo 4×14 | Masquerain×3 |
| SAFARI_ZONE_AREA_MOUNTAIN | land | bonus | oggetti tipo 1×10 | Volbeat×3 |
| SAFARI_ZONE_AREA_MOUNTAIN | land | bonus | oggetti tipo 2×10 | Chingling×3 |
| SAFARI_ZONE_AREA_MOUNTAIN | land | bonus | oggetti tipo 2×20 | Meditite×3 |
| SAFARI_ZONE_AREA_MOUNTAIN | land | bonus | oggetti tipo 2×35 | Dusclops×3 |
| SAFARI_ZONE_AREA_MOUNTAIN | land | bonus | oggetti tipo 3×15 | Lunatone×3 |
| SAFARI_ZONE_AREA_MOUNTAIN | land | bonus | oggetti tipo 3×56 | Metang×3 |
| SAFARI_ZONE_AREA_MOUNTAIN | land | bonus | oggetti tipo 4×49 + tipo 3×21 | Sealeo×3 |
| SAFARI_ZONE_AREA_MOUNTAIN | surf | bonus | oggetti tipo 2×20 | Surskit×6 |
| SAFARI_ZONE_AREA_PEAK | land | bonus | oggetti tipo 1×12 | Zangoose×3 |
| SAFARI_ZONE_AREA_PEAK | land | bonus | oggetti tipo 1×5 | Linoone×3 |
| SAFARI_ZONE_AREA_PEAK | land | bonus | oggetti tipo 2×56 + tipo 1×28 | Vigoroth×3 |
| SAFARI_ZONE_AREA_PEAK | land | bonus | oggetti tipo 3×24 | Lairon×3 |
| SAFARI_ZONE_AREA_PEAK | land | bonus | oggetti tipo 3×35 + tipo 2×14 | Bronzor×3 |
| SAFARI_ZONE_AREA_PEAK | land | bonus | oggetti tipo 4×35 | Spheal×3 |
| SAFARI_ZONE_AREA_PEAK | surf | bonus | oggetti tipo 2×20 | Surskit×6 |
| SAFARI_ZONE_AREA_PLAINS | land | bonus | oggetti tipo 1×10 | Shinx×3 |
| SAFARI_ZONE_AREA_PLAINS | land | bonus | oggetti tipo 1×15 | Manectric×3 |
| SAFARI_ZONE_AREA_PLAINS | land | bonus | oggetti tipo 2×15 | Zigzagoon×3 |
| SAFARI_ZONE_AREA_PLAINS | land | bonus | oggetti tipo 3×15 | Zangoose×3 |
| SAFARI_ZONE_AREA_PLAINS | land | bonus | oggetti tipo 4×12 | Lotad×3 |
| SAFARI_ZONE_AREA_PLAINS | land | bonus | oggetti tipo 4×28 | Surskit×3 |
| SAFARI_ZONE_AREA_PLAINS | surf | bonus | oggetti tipo 2×20 | Surskit×6 |
| SAFARI_ZONE_AREA_ROCKY_BEACH | land | bonus | oggetti tipo 1×10 | Electrike×3 |
| SAFARI_ZONE_AREA_ROCKY_BEACH | land | bonus | oggetti tipo 1×49 + tipo 3×49 | Gible×3 |
| SAFARI_ZONE_AREA_ROCKY_BEACH | land | bonus | oggetti tipo 2×10 | Manectric×3 |
| SAFARI_ZONE_AREA_ROCKY_BEACH | land | bonus | oggetti tipo 2×18 | Budew×3 |
| SAFARI_ZONE_AREA_ROCKY_BEACH | land | bonus | oggetti tipo 3×24 | Aron×3 |
| SAFARI_ZONE_AREA_ROCKY_BEACH | superrod | bonus | oggetti tipo 4×15 | Corphish×3 |
| SAFARI_ZONE_AREA_ROCKY_BEACH | superrod | bonus | oggetti tipo 4×20 | Corphish×3 |
| SAFARI_ZONE_AREA_SAVANNAH | land | bonus | oggetti tipo 1×10 | Zigzagoon×3 |
| SAFARI_ZONE_AREA_SAVANNAH | land | bonus | oggetti tipo 1×24 | Luxio×3 |
| SAFARI_ZONE_AREA_SAVANNAH | land | bonus | oggetti tipo 2×35 | Cacturne×3 |
| SAFARI_ZONE_AREA_SAVANNAH | land | bonus | oggetti tipo 2×35 + tipo 1×12 | Shroomish×3 |
| SAFARI_ZONE_AREA_SAVANNAH | land | bonus | oggetti tipo 3×35 | Torkoal×3 |
| SAFARI_ZONE_AREA_SAVANNAH | land | bonus | oggetti tipo 4×5 | Azurill×3 |
| SAFARI_ZONE_AREA_SAVANNAH | surf | bonus | oggetti tipo 2×20 | Surskit×6 |
| SAFARI_ZONE_AREA_SWAMP | land | bonus | oggetti tipo 1×10 | Pachirisu×3 |
| SAFARI_ZONE_AREA_SWAMP | land | bonus | oggetti tipo 2×15 | Chimecho×3 |
| SAFARI_ZONE_AREA_SWAMP | land | bonus | oggetti tipo 3×28 | Duskull×3 |
| SAFARI_ZONE_AREA_SWAMP | land | bonus | oggetti tipo 3×56 + tipo 2×35 | Bagon×3 |
| SAFARI_ZONE_AREA_SWAMP | land | bonus | oggetti tipo 4×10 | Floatzel×3 |
| SAFARI_ZONE_AREA_SWAMP | surf | bonus | oggetti tipo 4×35 | Duskull×3 |
| SAFARI_ZONE_AREA_WASTELAND | land | bonus | oggetti tipo 1×10 | Illumise×3 |
| SAFARI_ZONE_AREA_WASTELAND | land | bonus | oggetti tipo 1×3 | Manectric×3 |
| SAFARI_ZONE_AREA_WASTELAND | land | bonus | oggetti tipo 2×35 | Medicham×3 |
| SAFARI_ZONE_AREA_WASTELAND | land | bonus | oggetti tipo 2×42 | Breloom×3 |
| SAFARI_ZONE_AREA_WASTELAND | land | bonus | oggetti tipo 3×28 | Skorupi×3 |
| SAFARI_ZONE_AREA_WASTELAND | land | bonus | oggetti tipo 3×42 | Solrock×3 |
| SAFARI_ZONE_AREA_WASTELAND | surf | bonus | oggetti tipo 2×20 | Surskit×6 |
| SAFARI_ZONE_AREA_WETLAND | goodrod | bonus | oggetti tipo 4×10 | Corphish×3 |
| SAFARI_ZONE_AREA_WETLAND | goodrod | bonus | oggetti tipo 4×14 | Corphish×3 |
| SAFARI_ZONE_AREA_WETLAND | land | bonus | oggetti tipo 1×14 | Lombre×3 |
| SAFARI_ZONE_AREA_WETLAND | land | bonus | oggetti tipo 1×6 | Surskit×3 |
| SAFARI_ZONE_AREA_WETLAND | land | bonus | oggetti tipo 2×8 | Pachirisu×3 |
| SAFARI_ZONE_AREA_WETLAND | land | bonus | oggetti tipo 3×63 | Shelgon×3 |
| SAFARI_ZONE_AREA_WETLAND | land | bonus | oggetti tipo 4×35 | Buizel×3 |


## Gara Pigliamosche

| Tabella | Specie |
|---|---|
| 0 | Caterpie, Weedle, Metapod, Kakuna, Butterfree, Beedrill, Venonat, Paras, Scyther, Pinsir |
| 1 | Caterpie, Weedle, Metapod, Kakuna, Butterfree, Beedrill, Venonat, Paras, Scyther, Pinsir |
| 2 | Wurmple, Silcoon, Nincada, Volbeat, Kricketot, Kricketune, Dustox, Combee, Scyther, Pinsir |
| 3 | Wurmple, Cascoon, Nincada, Illumise, Kricketot, Kricketune, Beautifly, Combee, Scyther, Pinsir |


## Allenatori con specie > #251

| # | Classe | Nome | Squadra (liv.) |
|---|---|---|---|
| 15 | FIREBREATHER | Otis | Magmar, Weezing, **Camerupt** (40-47) |
| 235 | HIKER | Noland | **Bronzor**, Golem (39-42) |
| 239 | SAILOR | Jeff | **Makuhita**, Raticate (40-40) |
| 248 | BUG_CATCHER | Ed | **Burmy**, Butterfree, Beedrill (43-43) |
| 291 | SWIMMER_F | Debbie | **Clamperl** (46-46) |
| 337 | GENTLEMAN | Gregory | Pikachu, Flaaffy, **Electrike** (42-46) |
| 339 | BLACK_BELT | Wai | Machoke, Machoke, **Meditite** (38-42) |
| 346 | BEAUTY | Julia | Paras, **Carnivine**, Parasect (44-47) |
| 368 | MEDIUM | Rebecca | **Bronzor**, Hypno (45-45) |
| 421 | BIRD_KEEPER_GS | Bret | **Taillow**, Fearow (41-41) |
| 422 | PSYCHIC_M | Rodney | **Chingling**, Hypno (37-41) |
| 427 | TEACHER | Shirley | **Chatot**, Jigglypuff (43-43) |
| 433 | SCHOOL_KID_M | Alan | Xatu, **Tangrowth**, Quagsire, **Yanmega** (32-36) |
| 505 | SCHOOL_KID_M | Alan | Xatu, **Tangrowth**, Quagsire, **Yanmega** (47-54) |
| 513 | BUG_CATCHER | Arnie | **Nincada**, Venomoth (45-56) |
| 545 | ACE_TRAINER_M | French | **Absol**, Alakazam (47-47) |
| 553 | YOUNG_COUPLE | Moe & Lulu | **Lotad**, **Seedot** (43-43) |
| 560 | CAMPER | Clark | **Buizel** (40-40) |
| 562 | PICNICKER | Piper | **Spoink** (40-40) |
| 563 | PICNICKER | Ginger | **Whismur** (41-41) |
| 564 | TEACHER | Clarice | **Zigzagoon**, **Roselia** (41-43) |
| 566 | SCHOOL_KID_M | Connor | **Zigzagoon** (42-42) |
| 568 | SCHOOL_KID_M | Travis | **Budew** (42-42) |
| 570 | POKEFAN_M | Boone | **Spinda**, **Volbeat** (41-43) |
| 571 | POKEFAN | Eleanor | **Spinda**, **Illumise** (41-43) |
| 572 | BIKER | Dale | **Gulpin** (47-47) |
| 575 | BIKER | Dan | **Gulpin**, Weezing, Weezing (37-39) |
| 576 | BIKER | Theron | **Croagunk** (45-45) |
| 577 | BIKER | Markey | **Skorupi** (47-47) |
| 578 | BIKER | Teddy | **Seviper** (46-46) |
| 580 | CAMPER | Pedro | **Linoone** (45-45) |
| 581 | PICNICKER | Adrian | **Shroomish** (45-45) |
| 582 | PICNICKER | Cheyenne | **Shinx** (45-45) |
| 583 | BIRD_KEEPER_GS | Bert | **Wingull**, Fearow (43-46) |
| 584 | BIRD_KEEPER_GS | Ernie | **Starly** (48-48) |
| 587 | SWIMMER_F | Leona | **Bidoof** (44-44) |
| 588 | SWIMMER_F | Mina | **Luvdisc**, **Luvdisc**, **Luvdisc** (38-41) |
| 598 | TWINS | Day & Dani | **Plusle**, **Minun** (41-41) |
| 599 | CAMPER | Virgil | **Slakoth** (43-43) |
| 600 | PICNICKER | Selina | **Cherubi** (42-42) |
| 603 | PICNICKER | Erin | **Cherrim**, Sunflora, Bellossom, Rapidash (42-53) |
| 621 | FIREBREATHER | Walt | Magby, Magmar, **Magmortar** (26-58) |
| 637 | TEACHER | Hillary | **Ambipom**, Sunflora (43-43) |
| 638 | TEACHER | Hillary | **Ambipom**, Sunflora (49-49) |
| 639 | TEACHER | Hillary | **Ambipom**, Sunflora (55-55) |
| 667 | PKMN_TRAINER_CHERYL | Cheryl | Wobbuffet, **Drifblim**, **Hariyama**, **Wailord**, Blissey (61-65) |
| 668 | PKMN_TRAINER_BUCK | Marley | **Ninjask**, Electrode, Crobat, **Weavile**, Arcanine (61-65) |
| 669 | PKMN_TRAINER_MARLEY | Mira | **Porygon-Z**, Gengar, **Magnezone**, **Togekiss**, Alakazam (61-65) |
| 670 | PKMN_TRAINER_RILEY | Riley | **Absol**, Ursaring, **Metagross**, **Salamence**, **Lucario** (61-65) |
| 671 | PKMN_TRAINER_MIRA | Buck | Shuckle, Umbreon, **Torkoal**, **Dusknoir**, **Claydol** (61-65) |
| 682 | ACE_TRAINER_M | Bonita | **Spinda**, Sudowoodo (50-52) |
| 683 | ACE_TRAINER_F | Salma | Slowking, **Lickilicky** (50-53) |
| 689 | SUPER_NERD | Cary | **Torkoal** (53-53) |
| 690 | SUPER_NERD | Waldo | **Numel** (53-53) |
| 700 | ROCKET_BOSS | Giovanni | Nidoking, Kangaskhan, **Honchkrow**, Nidoqueen (40-46) |
| 701 | CHAMPION | Lance | **Salamence**, Gyarados, **Garchomp**, **Altaria**, Charizard, Dragonite (68-75) |
| 702 | ELITE_FOUR_WILL | Will | **Bronzong**, Jynx, **Grumpig**, Slowbro, **Gardevoir**, Xatu (58-62) |
| 703 | ELITE_FOUR_KOGA | Koga | **Skuntank**, Venomoth, **Toxicroak**, Muk, Crobat, **Swalot** (60-64) |
| 704 | ELITE_FOUR_BRUNO | Bruno | Hitmontop, Hitmonlee, Hitmonchan, **Hariyama**, Machamp, **Lucario** (61-64) |
| 705 | ELITE_FOUR_KAREN | Karen | **Weavile**, **Spiritomb**, **Absol**, **Honchkrow**, Houndoom, Umbreon (62-64) |
| 712 | LEADER_FALKNER | Falkner | **Staraptor**, Noctowl, **Swellow**, **Honchkrow**, **Pelipper**, Pidgeot (48-56) |
| 713 | LEADER_BUGSY | Bugsy | Scizor, **Shedinja**, **Yanmega**, Pinsir, Heracross, **Vespiquen** (48-56) |
| 714 | LEADER_WHITNEY | Whitney | Girafarig, **Lickilicky**, **Bibarel**, **Delcatty**, Clefable, Miltank (50-58) |
| 715 | LEADER_MORTY | Morty | **Drifblim**, **Dusknoir**, **Sableye**, **Mismagius**, Gengar, Gengar (52-57) |
| 716 | LEADER_PRYCE | Pryce | **Abomasnow**, Dewgong, **Glalie**, **Froslass**, **Walrein**, **Mamoswine** (52-60) |
| 717 | LEADER_JASMINE | Jasmine | **Metagross**, **Magnezone**, Skarmory, **Bronzong**, **Empoleon**, Steelix (50-62) |
| 718 | LEADER_CHUCK | Chuck | **Medicham**, Hitmonchan, Hitmonlee, **Breloom**, Primeape, Poliwrath (52-60) |
| 720 | LEADER_BROCK | Brock | Golem, **Relicanth**, Omastar, Onix, Kabutops, **Rampardos** (54-61) |
| 721 | LEADER_MISTY | Misty | Starmie, Quagsire, Lapras, Lanturn, **Floatzel**, **Milotic** (54-60) |
| 722 | LEADER_LT_SURGE | Lt. Surge | Raichu, **Manectric**, **Magnezone**, Electrode, **Pachirisu**, **Electivire** (52-60) |
| 723 | LEADER_ERIKA | Erika | **Shiftry**, Jumpluff, Victreebel, Bellossom, **Tangrowth**, **Roserade** (53-60) |
| 724 | LEADER_JANINE | Janine | Crobat, Weezing, **Toxicroak**, Ariados, Venomoth, **Drapion** (52-59) |
| 725 | LEADER_SABRINA | Sabrina | Alakazam, Espeon, Mr-Mime, Jynx, Wobbuffet, **Gallade** (53-60) |
| 726 | LEADER_BLAINE | Blaine | **Torkoal**, **Camerupt**, Rapidash, Magcargo, Houndoom, **Magmortar** (54-62) |
| 727 | LEADER_BLUE | Blue | Exeggutor, Machamp, **Rhyperior**, Arcanine, Tyranitar, Pidgeot (67-72) |


## Scambi in gioco

| NPC | Chiede | Dà |
|---|---|---|
| Rocky (Onix) | #1450333877 | **#1313033298** |
| Muscle (Machop) | #2117284659 | **#933904** |
| Billy (Voltorb) | #401605616 | **#475152** |
| Doris (Dodrio) | #117567500 | **#402448** |
| Sprints (Rapidash) | #1611948308 | **#402448** |
| Rusty (Steelix) | #276906256 | **#402448** |
| Shuckie (Shuckle, prestito) | #722479632 | **#402448** |
| Kenya (Spearow, prestito) | #535830512 | **#2920464** |
| Maggie (Magneton) | #51355726 | **#250384** |
| Paul (Xatu) | #946847792 | **#264720** |
| Volty (Pikachu) | #2683338736 | **#2502672** |
| Hornlette (Rhyhorn) | #1309216512 | **#436752** |
| Iron (Beldum) | #1811951711 | **#442896** |


## Script: regali, incontri statici, uova, vaganti

| Script | Comando | Specie | Note |
|---|---|---|---|
| 0011_D03R0103 | WildBattle | Mewtwo | lv 70 |
| 0014_D11R0105 | WildBattle | Articuno | lv 50 |
| 0021_D17R0110 | WildBattle | Ho-Oh | da variabile lv VAR_SPECIAL_x8004 |
| 0024_D18R0102 | CreateRoamer | Raikou | vagante |
| 0024_D18R0102 | CreateRoamer | Entei | vagante |
| 0024_D18R0102 | WildBattle | Suicune | lv 40 |
| 0058_D25R0103 | WildBattle | Lapras | lv 20 |
| 0090_D35R0103 | WildBattle | Electrode | lv 23 |
| 0090_D35R0103 | WildBattle | Electrode | lv 23 |
| 0090_D35R0103 | WildBattle | Electrode | lv 23 |
| 0092_D36R0101 | GiveSpikyEarPichu | Pichu | solo con Pichu evento |
| 0098_D38R0104 | GiveMon | Tyrogue | lv 10 |
| 0104_D40R0107 | WildBattle | Lugia | da variabile lv VAR_SPECIAL_x8004 |
| 0106_D41R0105 | WildBattle | Moltres | lv 50 |
| 0112_D44R0103 | GiveMon | Dratini | lv 15 |
| 0131_D51R0201 | GiveMon | **Dialga** | lv 1 |
| 0131_D51R0201 | GiveMon | **Palkia** | lv 1 |
| 0131_D51R0201 | GiveMon | **Giratina** | lv 1 |
| 0133_D52R0101 | WildBattle | **Groudon** | lv 50 |
| 0134_D52R0102 | WildBattle | **Kyogre** | lv 50 |
| 0135_D52R0103 | WildBattle | **Rayquaza** | lv 50 |
| 0191_R10 | WildBattle | Zapdos | lv 50 |
| 0197_R11 | WildBattle | Snorlax | lv 50 |
| 0199_R12 | WildBattle | Snorlax | lv 50 |
| 0216_R25 | WildBattle | Suicune | lv 40 |
| 0243_R36 | WildBattle | Sudowoodo | lv 20 |
| 0243_R36 | WildBattle | Sudowoodo | lv 20 |
| 0740_T01R0301 | GiveMon | Bulbasaur, Charmander, Squirtle | da variabile lv 5 |
| 0750_T03 | WildBattle | **Latias**, **Latios** | da variabile lv 40 |
| 0755_T03R0101 | GiveMon | ? | da variabile lv 20 |
| 0776_T06 | CreateRoamer | **Latias** | vagante |
| 0776_T06 | CreateRoamer | **Latios** | vagante |
| 0804_T07R0501 | GiveMon | Mr-Mime, Eevee, Porygon | da variabile lv 15 |
| 0825_T10R0701 | CreateRoamer | Entei | vagante |
| 0825_T10R0701 | CreateRoamer | Raikou | vagante |
| 0825_T10R0701 | CreateRoamer | **Latias** | vagante |
| 0825_T10R0701 | CreateRoamer | **Latios** | vagante |
| 0837_T11R0701 | GiveMon | **Treecko**, **Torchic**, **Mudkip** | da variabile lv 5 |
| 0858_T22FS0101 | GiveTogepiEgg | Togepi | uovo |
| 0860_T22PC0101 | GiveEgg | Mareep | uovo |
| 0860_T22PC0101 | GiveEgg | Wooper | uovo |
| 0860_T22PC0101 | GiveEgg | Slugma | uovo |
| 0878_T24PC0101 | GiveMon | Tentacool | lv 15 |
| 0892_T25R0401 | GiveMon | Eevee | lv 5 |
| 0906_T25R1101 | GiveMon | Ekans, Sandshrew, Abra, Dratini | da variabile lv 15 |
| 0910_T25SP0101 | GiveMon | Ekans, Sandshrew, Abra, Dratini | da variabile lv 15 |
| 0938_T29 | WildBattle | Gyarados | lv 30 |


## Parco Lotta (set di Pokémon)

| Archivio | Descrizione | Set totali | Set gen 3 | Set gen 4 |
|---|---|---|---|---|
| a/1/2/9 | set A (con allenatori a/1/2/8) | 950 | 229 | 243 |
| a/2/0/3 | set B (con allenatori a/2/0/2) | 950 | 228 | 243 |
| a/2/0/4 | set C (478, probabilmente noleggi Factory) | 477 | 130 | 101 |


## Pokédex di Johto

Voci lette da a/1/3/8: 256. Specie > 251 presenti: 5 — Sceptile, Torchic, Treecko, Grovyle, Combusken.

## Oggetti per evoluzioni/allevamento negli script

Solo oggetti dati o trovati tramite script. Negozi, oggetti nascosti e premi PL stanno nel codice: da verificare a parte.
| Oggetto | Script | Tenuto da selvatici |
|---|---|---|
| ITEM_ARMOR_FOSSIL | 0755_T03R0101 | - |
| ITEM_CLAW_FOSSIL | 0755_T03R0101 | - |
| ITEM_DOME_FOSSIL | 0755_T03R0101 | - |
| ITEM_ENIGMA_STONE | 0755_T03R0101 | - |
| ITEM_EVERSTONE | 0843_T20R0101 | Geodude, Golem, Graveler |
| ITEM_HARD_STONE | 0243_R36 | Aggron, Aron, Corsola, Lairon, Nosepass, Probopass |
| ITEM_HELIX_FOSSIL | 0755_T03R0101 | - |
| ITEM_KINGS_ROCK | 0061_D26R0103 | Hariyama, Politoed, Poliwhirl, Poliwrath, Slowbro, Slowking |
| ITEM_METAL_COAT | 0161_P01R0306 | Beldum, Bronzong, Bronzor, Magnemite, Magneton, Magnezone, Metagross, Metang, Steelix |
| ITEM_OLD_AMBER | 0755_T03R0101 | - |
| ITEM_ROOT_FOSSIL | 0755_T03R0101 | - |
| ITEM_SKULL_FOSSIL | 0755_T03R0101 | - |
| ITEM_DRAGON_SCALE | - | Dragonair, Dragonite, Dratini, Horsea, Kingdra, Seadra |


## Matrice di ottenibilità #001-#251 (una partita, HeartGold, senza scambi né eventi)

**Ottenibili: 230/251.** Mancanti: 21.

| # | Specie | Stato | Fonti |
|---|---|---|---|
| 001 | Bulbasaur | ok | regalo [0740_T01R0301] |
| 002 | Ivysaur | ok | evoluzione da Bulbasaur |
| 003 | Venusaur | ok | evoluzione da Ivysaur |
| 004 | Charmander | ok | regalo [0740_T01R0301] |
| 005 | Charmeleon | ok | evoluzione da Charmander |
| 006 | Charizard | ok | evoluzione da Charmeleon |
| 007 | Squirtle | ok | regalo [0740_T01R0301] |
| 008 | Wartortle | ok | evoluzione da Squirtle |
| 009 | Blastoise | ok | evoluzione da Wartortle |
| 010 | Caterpie | ok | bottintesta; gara coleottero t0; gara coleottero t1; radio Hoenn; radio Sinnoh; sciami; selvatico |
| 011 | Metapod | ok | bottintesta; gara coleottero t0; gara coleottero t1; selvatico |
| 012 | Butterfree | ok | bottintesta; gara coleottero t0; gara coleottero t1; selvatico |
| 013 | Weedle | ok | gara coleottero t0; gara coleottero t1 |
| 014 | Kakuna | ok | gara coleottero t0; gara coleottero t1 |
| 015 | Beedrill | ok | gara coleottero t0; gara coleottero t1 |
| 016 | Pidgey | ok | safari; sciami; selvatico |
| 017 | Pidgeotto | ok | sciami; selvatico |
| 018 | Pidgeot | ok | evoluzione da Pidgeotto |
| 019 | Rattata | ok | safari; sciami; selvatico |
| 020 | Raticate | ok | safari; safari (bonus oggetti); selvatico |
| 021 | Spearow | ok | bottintesta; safari; sciami; selvatico |
| 022 | Fearow | ok | safari; safari (bonus oggetti); sciami; selvatico |
| 023 | Ekans | ok | regalo [0906_T25R1101]; regalo [0910_T25SP0101]; safari |
| 024 | Arbok | ok | safari |
| 025 | Pikachu | ok | selvatico |
| 026 | Raichu | ok | evoluzione da Pikachu |
| 027 | Sandshrew | ok | regalo [0906_T25R1101]; regalo [0910_T25SP0101]; safari; selvatico |
| 028 | Sandslash | ok | safari; selvatico |
| 029 | Nidoran-F | ok | safari; selvatico |
| 030 | Nidorina | ok | safari; sciami; selvatico |
| 031 | Nidoqueen | ok | evoluzione da Nidorina |
| 032 | Nidoran-M | ok | safari; sciami; selvatico |
| 033 | Nidorino | ok | safari; selvatico |
| 034 | Nidoking | ok | evoluzione da Nidorino |
| 035 | Clefairy | ok | safari; safari (bonus oggetti); selvatico |
| 036 | Clefable | ok | evoluzione da Clefairy |
| 037 | Vulpix | MANCA | - |
| 038 | Ninetales | MANCA | - |
| 039 | Jigglypuff | ok | safari; selvatico |
| 040 | Wigglytuff | ok | evoluzione da Jigglypuff |
| 041 | Zubat | ok | safari; sciami; selvatico |
| 042 | Golbat | ok | safari; sciami; selvatico |
| 043 | Oddish | ok | safari; selvatico |
| 044 | Gloom | ok | safari; safari (bonus oggetti); selvatico |
| 045 | Vileplume | ok | evoluzione da Gloom |
| 046 | Paras | ok | gara coleottero t0; gara coleottero t1; safari; safari (bonus oggetti); selvatico |
| 047 | Parasect | ok | safari (bonus oggetti); selvatico |
| 048 | Venonat | ok | bottintesta; gara coleottero t0; gara coleottero t1; selvatico |
| 049 | Venomoth | ok | selvatico |
| 050 | Diglett | ok | safari (bonus oggetti); sciami; selvatico |
| 051 | Dugtrio | ok | selvatico |
| 052 | Meowth | MANCA | - |
| 053 | Persian | MANCA | - |
| 054 | Psyduck | ok | safari; sciami; selvatico |
| 055 | Golduck | ok | safari; safari (bonus oggetti); selvatico |
| 056 | Mankey | ok | sciami; selvatico |
| 057 | Primeape | ok | selvatico |
| 058 | Growlithe | ok | selvatico |
| 059 | Arcanine | ok | evoluzione da Growlithe |
| 060 | Poliwag | ok | safari; safari (bonus oggetti); sciami; selvatico |
| 061 | Poliwhirl | ok | safari; safari (bonus oggetti); sciami; selvatico |
| 062 | Poliwrath | ok | evoluzione da Poliwhirl |
| 063 | Abra | ok | regalo [0906_T25R1101]; regalo [0910_T25SP0101]; safari; selvatico |
| 064 | Kadabra | ok | sciami; selvatico |
| 065 | Alakazam | MANCA | evoluzione TRADE (impossibile da solo) |
| 066 | Machop | ok | safari; selvatico |
| 067 | Machoke | ok | safari; safari (bonus oggetti); selvatico |
| 068 | Machamp | MANCA | evoluzione TRADE (impossibile da solo) |
| 069 | Bellsprout | ok | safari; safari (bonus oggetti); sciami; selvatico |
| 070 | Weepinbell | ok | safari (bonus oggetti); selvatico |
| 071 | Victreebel | ok | evoluzione da Weepinbell |
| 072 | Tentacool | ok | regalo [0878_T24PC0101]; safari; sciami; selvatico |
| 073 | Tentacruel | ok | selvatico |
| 074 | Geodude | ok | safari; safari (bonus oggetti); sciami; selvatico |
| 075 | Graveler | ok | safari; sciami; selvatico |
| 076 | Golem | MANCA | evoluzione TRADE (impossibile da solo) |
| 077 | Ponyta | ok | safari (bonus oggetti); selvatico |
| 078 | Rapidash | ok | selvatico |
| 079 | Slowpoke | ok | safari; sciami; selvatico |
| 080 | Slowbro | ok | safari; safari (bonus oggetti); selvatico |
| 081 | Magnemite | ok | safari; selvatico |
| 082 | Magneton | ok | safari; safari (bonus oggetti); selvatico |
| 083 | Farfetchd | ok | safari; safari (bonus oggetti); selvatico |
| 084 | Doduo | ok | safari; safari (bonus oggetti); sciami; selvatico |
| 085 | Dodrio | ok | safari (bonus oggetti); selvatico |
| 086 | Seel | ok | sciami; selvatico |
| 087 | Dewgong | ok | sciami; selvatico |
| 088 | Grimer | ok | safari; sciami; selvatico |
| 089 | Muk | ok | safari (bonus oggetti); selvatico |
| 090 | Shellder | ok | sciami; selvatico |
| 091 | Cloyster | ok | evoluzione da Shellder |
| 092 | Gastly | ok | safari; selvatico |
| 093 | Haunter | ok | safari; selvatico |
| 094 | Gengar | MANCA | evoluzione TRADE (impossibile da solo) |
| 095 | Onix | ok | safari; sciami; selvatico |
| 096 | Drowzee | ok | safari; sciami; selvatico |
| 097 | Hypno | ok | safari; safari (bonus oggetti); selvatico |
| 098 | Krabby | ok | safari; safari (bonus oggetti); sciami; selvatico |
| 099 | Kingler | ok | safari; safari (bonus oggetti); selvatico |
| 100 | Voltorb | ok | safari (bonus oggetti); selvatico |
| 101 | Electrode | ok | selvatico; statico [0090_D35R0103] |
| 102 | Exeggcute | ok | bottintesta |
| 103 | Exeggutor | ok | evoluzione da Exeggcute |
| 104 | Cubone | ok | safari; sciami; selvatico |
| 105 | Marowak | ok | safari; safari (bonus oggetti); selvatico |
| 106 | Hitmonlee | ok | evoluzione da Tyrogue |
| 107 | Hitmonchan | ok | evoluzione da Tyrogue |
| 108 | Lickitung | ok | safari; safari (bonus oggetti); selvatico |
| 109 | Koffing | ok | safari; selvatico |
| 110 | Weezing | ok | safari |
| 111 | Rhyhorn | ok | safari; safari (bonus oggetti); selvatico |
| 112 | Rhydon | solo condizionale | safari (bonus oggetti) |
| 113 | Chansey | ok | safari (bonus oggetti); sciami; selvatico |
| 114 | Tangela | ok | bottintesta; sciami; selvatico |
| 115 | Kangaskhan | ok | safari; selvatico |
| 116 | Horsea | ok | sciami; selvatico |
| 117 | Seadra | ok | selvatico |
| 118 | Goldeen | ok | safari; safari (bonus oggetti); sciami; selvatico |
| 119 | Seaking | ok | safari; safari (bonus oggetti); sciami; selvatico |
| 120 | Staryu | ok | sciami; selvatico |
| 121 | Starmie | ok | evoluzione da Staryu |
| 122 | Mr-Mime | ok | regalo [0804_T07R0501]; safari; safari (bonus oggetti); selvatico |
| 123 | Scyther | ok | gara coleottero t0; gara coleottero t1; gara coleottero t2; gara coleottero t3 |
| 124 | Jynx | ok | selvatico |
| 125 | Electabuzz | ok | safari (bonus oggetti); selvatico |
| 126 | Magmar | ok | safari; safari (bonus oggetti); selvatico |
| 127 | Pinsir | ok | gara coleottero t0; gara coleottero t1; gara coleottero t2; gara coleottero t3 |
| 128 | Tauros | ok | safari; safari (bonus oggetti); sciami; selvatico |
| 129 | Magikarp | ok | safari; sciami; selvatico |
| 130 | Gyarados | ok | safari; safari (bonus oggetti); sciami; selvatico; statico [0938_T29] |
| 131 | Lapras | ok | safari; safari (bonus oggetti); statico [0058_D25R0103] |
| 132 | Ditto | ok | safari; safari (bonus oggetti); sciami; selvatico |
| 133 | Eevee | ok | regalo [0804_T07R0501]; regalo [0892_T25R0401] |
| 134 | Vaporeon | ok | evoluzione da Eevee |
| 135 | Jolteon | ok | evoluzione da Eevee |
| 136 | Flareon | ok | evoluzione da Eevee |
| 137 | Porygon | ok | regalo [0804_T07R0501] |
| 138 | Omanyte | ok | fossile HELIX_FOSSIL rianimato [T03R0101] (ottenimento fossile: DA VERIFICARE) |
| 139 | Omastar | ok | evoluzione da Omanyte |
| 140 | Kabuto | ok | fossile DOME_FOSSIL rianimato [T03R0101] (ottenimento fossile: DA VERIFICARE) |
| 141 | Kabutops | ok | evoluzione da Kabuto |
| 142 | Aerodactyl | ok | fossile OLD_AMBER rianimato [T03R0101] (ottenimento fossile: DA VERIFICARE) |
| 143 | Snorlax | ok | statico [0197_R11]; statico [0199_R12] |
| 144 | Articuno | ok | statico [0014_D11R0105] |
| 145 | Zapdos | ok | statico [0191_R10] |
| 146 | Moltres | ok | statico [0106_D41R0105] |
| 147 | Dratini | ok | regalo [0112_D44R0103]; regalo [0906_T25R1101]; regalo [0910_T25SP0101]; safari; safari (bonus oggetti); sciami; selvatico |
| 148 | Dragonair | ok | safari (bonus oggetti); selvatico |
| 149 | Dragonite | ok | evoluzione da Dragonair |
| 150 | Mewtwo | ok | statico [0011_D03R0103] |
| 151 | Mew | MANCA | - |
| 152 | Chikorita | ok | starter (1 dei 3) |
| 153 | Bayleef | ok | evoluzione da Chikorita |
| 154 | Meganium | ok | evoluzione da Bayleef |
| 155 | Cyndaquil | ok | starter (1 dei 3) |
| 156 | Quilava | ok | evoluzione da Cyndaquil |
| 157 | Typhlosion | ok | evoluzione da Quilava |
| 158 | Totodile | ok | starter (1 dei 3) |
| 159 | Croconaw | ok | evoluzione da Totodile |
| 160 | Feraligatr | ok | evoluzione da Croconaw |
| 161 | Sentret | ok | safari; selvatico |
| 162 | Furret | ok | safari (bonus oggetti); selvatico |
| 163 | Hoothoot | ok | bottintesta; selvatico |
| 164 | Noctowl | ok | bottintesta; selvatico |
| 165 | Ledyba | MANCA | - |
| 166 | Ledian | MANCA | - |
| 167 | Spinarak | ok | bottintesta; selvatico |
| 168 | Ariados | ok | bottintesta; selvatico |
| 169 | Crobat | ok | evoluzione da Golbat |
| 170 | Chinchou | ok | selvatico |
| 171 | Lanturn | ok | selvatico |
| 172 | Pichu | ok | allevamento da Pikachu |
| 173 | Cleffa | ok | allevamento da Clefairy |
| 174 | Igglybuff | ok | allevamento da Jigglypuff |
| 175 | Togepi | ok | uovo regalo [0858_T22FS0101] |
| 176 | Togetic | ok | evoluzione da Togepi |
| 177 | Natu | ok | bottintesta; sciami; selvatico |
| 178 | Xatu | ok | evoluzione da Natu |
| 179 | Mareep | ok | safari (bonus oggetti); selvatico; uovo regalo [0860_T22PC0101] |
| 180 | Flaaffy | ok | sciami; selvatico |
| 181 | Ampharos | ok | evoluzione da Flaaffy |
| 182 | Bellossom | ok | evoluzione da Gloom |
| 183 | Marill | ok | safari; sciami; selvatico |
| 184 | Azumarill | ok | evoluzione da Marill |
| 185 | Sudowoodo | ok | statico [0243_R36] |
| 186 | Politoed | MANCA | evoluzione TRADE_ITEM (impossibile da solo) |
| 187 | Hoppip | ok | safari; sciami; selvatico |
| 188 | Skiploom | ok | safari; safari (bonus oggetti); selvatico |
| 189 | Jumpluff | solo condizionale | safari (bonus oggetti) |
| 190 | Aipom | ok | bottintesta |
| 191 | Sunkern | ok | safari; selvatico |
| 192 | Sunflora | ok | evoluzione da Sunkern |
| 193 | Yanma | ok | sciami; selvatico |
| 194 | Wooper | ok | safari; safari (bonus oggetti); sciami; selvatico; uovo regalo [0860_T22PC0101] |
| 195 | Quagsire | ok | safari; safari (bonus oggetti); sciami; selvatico |
| 196 | Espeon | ok | evoluzione da Eevee |
| 197 | Umbreon | ok | evoluzione da Eevee |
| 198 | Murkrow | ok | safari; safari (bonus oggetti); selvatico |
| 199 | Slowking | MANCA | evoluzione TRADE_ITEM (impossibile da solo) |
| 200 | Misdreavus | ok | safari; safari (bonus oggetti); selvatico |
| 201 | Unown | ok | radio Hoenn; radio Sinnoh; sciami; selvatico |
| 202 | Wobbuffet | ok | safari; safari (bonus oggetti); selvatico |
| 203 | Girafarig | ok | safari; safari (bonus oggetti); selvatico |
| 204 | Pineco | ok | bottintesta |
| 205 | Forretress | ok | evoluzione da Pineco |
| 206 | Dunsparce | ok | sciami; selvatico |
| 207 | Gligar | ok | selvatico |
| 208 | Steelix | ok | selvatico; evoluzione TRADE_ITEM (impossibile da solo) |
| 209 | Snubbull | ok | sciami; selvatico |
| 210 | Granbull | ok | evoluzione da Snubbull |
| 211 | Qwilfish | ok | sciami; selvatico |
| 212 | Scizor | MANCA | evoluzione TRADE_ITEM (impossibile da solo) |
| 213 | Shuckle | ok | safari (bonus oggetti); selvatico |
| 214 | Heracross | ok | bottintesta |
| 215 | Sneasel | ok | sciami; selvatico |
| 216 | Teddiursa | MANCA | - |
| 217 | Ursaring | MANCA | - |
| 218 | Slugma | ok | selvatico; uovo regalo [0860_T22PC0101] |
| 219 | Magcargo | ok | evoluzione da Slugma |
| 220 | Swinub | ok | sciami; selvatico |
| 221 | Piloswine | ok | evoluzione da Swinub |
| 222 | Corsola | ok | selvatico |
| 223 | Remoraid | ok | sciami; selvatico |
| 224 | Octillery | ok | evoluzione da Remoraid |
| 225 | Delibird | MANCA | - |
| 226 | Mantine | ok | selvatico |
| 227 | Skarmory | MANCA | - |
| 228 | Houndour | ok | safari (bonus oggetti); selvatico |
| 229 | Houndoom | solo condizionale | safari (bonus oggetti) |
| 230 | Kingdra | MANCA | evoluzione TRADE_ITEM (impossibile da solo) |
| 231 | Phanpy | ok | selvatico |
| 232 | Donphan | ok | selvatico |
| 233 | Porygon2 | MANCA | evoluzione TRADE_ITEM (impossibile da solo) |
| 234 | Stantler | ok | safari; safari (bonus oggetti); selvatico |
| 235 | Smeargle | ok | safari; safari (bonus oggetti); selvatico |
| 236 | Tyrogue | ok | regalo [0098_D38R0104] |
| 237 | Hitmontop | ok | evoluzione da Tyrogue |
| 238 | Smoochum | ok | allevamento da Jynx |
| 239 | Elekid | ok | allevamento da Electabuzz |
| 240 | Magby | ok | allevamento da Magmar |
| 241 | Miltank | ok | selvatico |
| 242 | Blissey | ok | evoluzione da Chansey |
| 243 | Raikou | ok | vagante [0024_D18R0102]; vagante [0825_T10R0701] |
| 244 | Entei | ok | vagante [0024_D18R0102]; vagante [0825_T10R0701] |
| 245 | Suicune | ok | statico [0024_D18R0102]; statico [0216_R25] |
| 246 | Larvitar | ok | safari; safari (bonus oggetti); selvatico |
| 247 | Pupitar | ok | selvatico |
| 248 | Tyranitar | ok | evoluzione da Pupitar |
| 249 | Lugia | ok | statico [0104_D40R0107] |
| 250 | Ho-Oh | ok | statico [0021_D17R0110] |
| 251 | Celebi | MANCA | - |

