# Pokémon Crystal Soul

**English** · [Italiano](README.it.md)

A data hack of **Pokémon HeartGold** that keeps the HGSS engine, graphics and story, but contains **only the 251
Pokémon of Generations 1 and 2 — and all 251 can be obtained in a single playthrough**, with no trades and no
other games. A "Pokémon Crystal" experience with the look of HeartGold/SoulSilver.

Available in **Italian** (from *Pokémon Oro HeartGold*, IPKI) and **English** (from *Pokémon HeartGold* USA, IPKE).

> **Status: beta.** The data is checked automatically on every build, but a full playthrough has not been
> completed yet. Feedback and bug reports are welcome (open an issue: say where you were and what you did).

<p align="center">
  <img width="190" alt="Title: Ho-Oh" src="https://github.com/user-attachments/assets/18016320-c22b-48cf-8334-0975d92451ea" />
  <img width="190" alt="Title: Lugia" src="https://github.com/user-attachments/assets/2af44e05-ea03-4cf8-871b-d3859a07943f" />
  <img width="190" alt="Intro" src="https://github.com/user-attachments/assets/ebf75db8-4b31-4838-a7ae-b63db017e849" />
  <img width="190" alt="Starter" src="https://github.com/user-attachments/assets/58c2180c-ab8f-46d8-94cb-ba9984339ec1" />
</p>
<p align="center">
  <img width="190" alt="New Bark Town" src="https://github.com/user-attachments/assets/5fdbb63e-2cf6-4d55-8fd6-a967c04e5d84" />
  <img width="190" alt="Route 29" src="https://github.com/user-attachments/assets/9dc3775c-1a75-40dd-9262-e9d9df050c94" />
  <img width="190" alt="Battle" src="https://github.com/user-attachments/assets/887fed71-369c-4d6f-8e39-4b436707a926" />
</p>

## Highlights

- **Only #001–#251, all obtainable.** No Generation 3–4 species anywhere: wild encounters, swarms, Headbutt trees,
  Safari Zone, Bug-Catching Contest, trainers (Gym Leaders, Elite Four, rematches, Red), Battle Frontier,
  Pokéathlon, in-game trades, breeding (the incenses that hatch Generation 3–4 babies such as Azurill or Happiny
  can't be found).
- **No trades needed.** Kadabra, Machoke, Graveler and Haunter evolve at **level 37**; Onix and Scyther (Metal Coat),
  Seadra (Dragon Scale), Slowpoke and Poliwhirl (King's Rock) and Porygon (Up-Grade) evolve by **using the item like
  an evolution stone**. Evolutions into Generation 4 species are removed.
- **Both version mascots:** Ho-Oh *and* Lugia can be caught in the same game, both at **level 60** as in Crystal.
- **SoulSilver exclusives** (Vulpix, Meowth, Ledyba, Teddiursa, Delibird, Skarmory and their evolutions) appear in
  the wild where they live in SoulSilver.
- **Every starter:** Professor Oak (after Red) lets you take all three Kanto starters; Steven in Saffron City
  (post-game) gives the two Johto starters you did not pick from Elm, instead of the Hoenn starters.
- **Mythicals without events:** after the Pokémon League, **Mew** waits in the Embedded Tower and **Celebi** at the
  Ilex Forest shrine (the time-travel story works). **Spiky-eared Pichu** can be unlocked too.
- **Johto Pokédex = the 251**, renumbered, with a reachable completion diploma; the **National Pokédex diploma**
  is also awarded once all 251 are caught (Mew and Celebi are not required, as in the original game).
- **Fossils:** Kabuto (Dome Fossil) from the Ruins of Alph as in SoulSilver; Cliff Cave gives Helix Fossil/Old Amber.
- **Natures without effect**, as in Crystal where they did not exist: each Pokémon still shows one, but it no
  longer changes its stats.
- **Odd Egg** as in Crystal: the Day-Care Man on Route 34 gives it once (a random baby Pokémon that knows Dizzy
  Punch, with a 14% chance of being shiny).
- **Game Boy music from the start:** Mom gives you the GB Sounds right after the Pokégear; use it from the Bag
  (or register it to Y) to switch between the original Gold/Silver/Crystal music and the HGSS one.
- **Suicune as in Crystal:** it also shows up on **Route 36** in front of the National Park gate, and until the
  Pokémon League it keeps reappearing in a loop (Cianwood, Route 42, Route 36); Eusine joins only the first time.
  After the League the HGSS chase continues in Kanto as usual.
- **New presentation:** "Crystal Soul" logo, title screen with Ho-Oh and Lugia one after the other (the first one is
  random; golden and blue skies) and Suicune in the corner, intro with both birds, crystal-blue DS menu icon.
- **Modern conveniences:**
  - **Reusable TMs:** teaching a TM no longer uses it up.
  - **Exp. All:** a key item from Professor Elm's aide (with the Potions, at the start). Turn it on or off from the
    Bag or the Y button. When on, the Pokémon that battled get full Exp. Points and the rest of the team gets half,
    without a message for each one (level-ups and new moves are still shown).
  - **HMs without using a move slot:** Cut, Surf, Strength, Rock Smash, Waterfall, Whirlpool, Rock Climb and
    Headbutt work if any Pokémon in your party *can learn* the move (badges still required). Fly and Flash appear
    in the party menu of any Pokémon that can learn them.
  - **Fast text** by default in a new game (still changeable in Options).
  - **"L=A R=B" button option:** in that mode R works as B (hold R to run).
- **Kept from HGSS:** moves, abilities, the physical/special split, walking Pokémon, graphics, music and story.

## How to play

You need your **own dump** of the original game. This repository contains no ROMs and never will.

| Patch | Original game | SHA-1 of the original `.nds` |
|---|---|---|
| [`Pokemon.Crystal.Soul.ITA.bps`](https://github.com/SimpleMatt7/Pokemon-Crystal-Soul/releases) | Pokémon Oro HeartGold (ITA), IPKI | `6b7f9bff57eb58bc8d6e48e9e5c370719458c721` |
| [`Pokemon.Crystal.Soul.ENG.bps`](https://github.com/SimpleMatt7/Pokemon-Crystal-Soul/releases) | Pokémon HeartGold (USA), IPKE | `4fcded0e2713dc03929845de631d0932ea2b5a37` |

1. Check that your `.nds` has the SHA-1 above (the patch also checks it and refuses a different file).
2. Apply the `.bps` with any BPS patcher, for example [Rom Patcher JS](https://www.marcrobledo.com/RomPatcher.js/)
   (in the browser) or [Flips](https://github.com/Alcaro/Flips), or with this repository:
   `python tools/bps.py applica ORIGINAL.nds patches/Pokemon.Crystal.Soul.ENG.bps OUTPUT.nds`
3. Play the patched `.nds` in an emulator (tested with **melonDS**) or on hardware. Start a **new game**.

The patch contains only the differences from the original game.

## Known limitations

- The National Pokédex still has 493 slots (you will only ever fill the first 251).
- Pokéwalker, Migration from GBA (so the Pal Park stays empty), Pokémon Ranger connection and Mystery Gift are removed
  from the main menu, since they would bring in species above #251. Trades (local, Wi-Fi, GTS) are kept: trading
  with unmodified games can still bring in other species; trading between copies of Crystal Soul is fine.
- The new events (Suicune loop, Odd Egg, Mew, Celebi and time travel, Pichu, Steven/Oak starters) have been tested
  one by one with a test build, but not yet in a full playthrough. Save before them.
- The English version is built from the same data as the Italian one, but it has had less in-game testing.

## Building from source

Everything is built by scripts from your own ROM: Python 3 (standard library only), no manual editing.

```
python tools/roms.py          # put your ROMs in roms/ (checked by SHA-1)
python tools/get_tools.py     # downloads dsrom 0.8.0 (hash-verified)
python tools/roundtrip.py     # extracts the ROM into work/
python tools/get_pret.py      # pret decompilation (format documentation, scripts)
python tools/build.py         # Italian version → out/  (English: --base IPKE)
python tools/build.py --debug # test build with shortcuts to the new events (never published): docs/DEBUG.md
```

The design lives in readable tables (`data/design/*.csv`), script changes as diffs (`data/scripts/`), new texts
in `data/testi/`. Full setup guide: [docs/SETUP.md](docs/SETUP.md). Project journal and all decisions:
[NOTES.md](NOTES.md). (Development notes are in Italian.)

## Credits

- [pret/pokeheartgold](https://github.com/pret/pokeheartgold) — the decompilation, used as documentation of the
  formats and scripts.
- [ds-rom (dsrom)](https://github.com/AetiasHax/ds-rom) — ROM extraction and rebuilding.
- [DSPRE](https://github.com/DS-Pokemon-Rom-Editor/DSPRE) and [melonDS](https://melonds.kuribo64.net) — inspection
  and testing.

## License

The scripts, tables and documentation in this repository are released under the [MIT License](LICENSE).
This covers only the original work of this project, not Pokémon or any game data.

## Legal

This is an unofficial fan project, not affiliated with or endorsed by Nintendo, Game Freak, Creatures or The
Pokémon Company. Pokémon and all related names are trademarks of their respective owners. No copyrighted game data
is distributed here: you need a legally obtained copy of the original game.
