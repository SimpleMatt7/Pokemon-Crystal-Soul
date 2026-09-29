# Pokemon Crystal New — HeartGold con solo i 251

Hack di dati di **Pokémon Oro HeartGold ITA (IPKI)**: tutte e sole le specie di gen 1-2 (#001-#251),
tutte ottenibili in una singola partita, grafica HGSS. Stato, decisioni e prossimi passi: **[NOTES.md](NOTES.md)**.

## Vincoli (non negoziabili)
- **Nessun contenuto del gioco nel repository**: niente ROM, zip, salvataggi, file estratti (NARC, bin, grafica),
  cartelle DSPRE, output. Solo note, script, tabelle scritte da noi e patch BPS (solo differenze) in `patches/`.
- Prima di ogni commit: `git status` + controllo che nulla di protetto sia in staging. L'hook
  `tools/hooks/pre-commit` blocca estensioni/cartelle protette, file > 512 KB e header ROM.
- ROM solo da dump propri; mai aiutare a procurarle altrove.
- Git: identità e credenziali **solo a livello di repository** (account personale `SimpleMatt7`). Mai toccare config globali
  o credenziali di altri account. Il push lo lancia l'utente se serve autenticarsi.
- Lavoro portabile: script Python (solo libreria standard, finché possibile), niente percorsi assoluti.
- Lingua: note e testi di gioco in italiano.
- Commit e push frequenti sul branch `dev`; aggiornare NOTES.md (e questo file se serve) a ogni fase e prima di ogni push.

## Struttura
- `roms/` (ignorata) — ROM originali, `.nds` o `.zip`; riconosciute tramite SHA1 (`tools/roms.py`).
- `work/`, `out/` (ignorate) — estrazioni e ROM generate.
- `tools/` — script: `roms.py` (trova/verifica ROM), `ndsfs.py` (lettura FNT/FAT/NARC), `probe.py` (audit specie > 251).
- `data/` — tabelle nostre (`species.csv`: ID→costante, dalla decomp pret).
- `patches/` — patch BPS pubblicabili (quando esisteranno).

## Comandi utili
```
python tools/roms.py          # verifica le ROM in roms/
python tools/probe.py         # dove compaiono specie > 251 (evoluzioni, selvatici, allenatori)
git config core.hooksPath tools/hooks   # una volta per clone: attiva l'hook anti-ROM
```

## Setup su un nuovo PC
Vedi NOTES.md → "Setup su un nuovo PC".
