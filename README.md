# Pokémon Crystal Soul

**English** · [Italiano](README.it.md)

A data hack of **Pokémon HeartGold** that keeps the HGSS engine, graphics and story, but contains **only the 251
Pokémon of Generations 1 and 2 — and all 251 can be obtained in a single playthrough**, with no trades and no
other games. A "Pokémon Crystal" experience with the look of HeartGold/SoulSilver.

Available in **Italian** (from *Pokémon Oro HeartGold*, IPKI) and **English** (from *Pokémon HeartGold* USA, IPKE).

> **Status: beta.** The data is checked automatically on every build, but a full playthrough has not been
> completed yet. Feedback and bug reports are welcome (open an issue: say where you were and what you did).

## Highlights

- **Only #001–#251, all obtainable.** No Generation 3–4 species anywhere: wild encounters, swarms, Headbutt trees,
  Safari Zone, Bug-Catching Contest, trainers (Gym Leaders, Elite Four, rematches, Red), Battle Frontier,
  Pokéathlon, in-game trades.
- **No trades needed.** Kadabra, Machoke, Graveler and Haunter evolve at **level 37**; Onix and Scyther (Metal Coat),
  Seadra (Dragon Scale), Slowpoke and Poliwhirl (King's Rock) and Porygon (Up-Grade) evolve by **using the item like
  an evolution stone**. Evolutions into Generation 4 species are removed.
- **Both version mascots:** Ho-Oh *and* Lugia can be caught in the same game, both at **level 60** as in Crystal.
- **SoulSilver exclusives** (Vulpix, Meowth, Ledyba, Teddiursa, Delibird, Skarmory and their evolutions) appear in
  the wild where they live in SoulSilver.
- **Every starter:** Professor Oak (after Red) lets you take all three Kanto starters; Steven in Saffron City
  (post-game) gives Chikorita, Cyndaquil and Totodile instead of the Hoenn starters.
- **Mythicals without events:** after the Pokémon League, **Mew** waits in the Embedded Tower and **Celebi** at the
  Ilex Forest shrine (the time-travel story works). **Spiky-eared Pichu** can be unlocked too.
- **Johto Pokédex = the 251**, renumbered, with a reachable completion diploma.
- **Fossils:** Kabuto (Dome Fossil) from the Ruins of Alph as in SoulSilver; Cliff Cave gives Helix Fossil/Old Amber.
- **Kept from HGSS:** moves, abilities, natures, the physical/special split, walking Pokémon, graphics and music.
- **New presentation:** "Crystal Soul" logo, title screen with Ho-Oh then Lugia (golden and blue skies),
  intro with both birds, crystal-blue DS menu icon.

## How to play

You need your **own dump** of the original game. This repository contains no ROMs and never will.

| Patch | Original game | SHA-1 of the original `.nds` |
|---|---|---|
| [`patches/Pokemon Crystal Soul (ITA).bps`](patches/) | Pokémon Oro HeartGold (ITA), IPKI | `6b7f9bff57eb58bc8d6e48e9e5c370719458c721` |
| [`patches/Pokemon Crystal Soul (ENG).bps`](patches/) | Pokémon HeartGold (USA), IPKE | `4fcded0e2713dc03929845de631d0932ea2b5a37` |

1. Check that your `.nds` has the SHA-1 above (the patch also checks it and refuses a different file).
2. Apply the `.bps` with any BPS patcher, for example [Rom Patcher JS](https://www.marcrobledo.com/RomPatcher.js/)
   (in the browser) or [Flips](https://github.com/Alcaro/Flips), or with this repository:
   `python tools/bps.py applica ORIGINAL.nds "patches/Pokemon Crystal Soul (ENG).bps" OUTPUT.nds`
3. Play the patched `.nds` in an emulator (tested with **melonDS**) or on hardware. Start a **new game**.

The patch contains only the differences from the original game.

## Known limitations

- The National Pokédex still has 493 slots (you will only ever fill the first 251).
- Features that connect to other games — Pokéwalker, Pal Park (migration from GBA), Pokémon Ranger, trades or GTS with
  unmodified games, Mystery Gift — are left untouched: if you use them, species above #251 can come in. Playing on
  your own, they cannot.
- Not tested yet in a full playthrough: the post-game events (Mew, Celebi and time travel, Pichu, Steven/Oak
  starters). Save before them.

## Building from source

Everything is built by scripts from your own ROM: Python 3 (standard library only), no manual editing.

```
python tools/roms.py          # put your ROMs in roms/ (checked by SHA-1)
python tools/get_tools.py     # downloads dsrom 0.8.0 (hash-verified)
python tools/roundtrip.py     # extracts the ROM into work/
python tools/get_pret.py      # pret decompilation (format documentation, scripts)
python tools/build.py         # Italian version → out/  (English: --base IPKE)
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
