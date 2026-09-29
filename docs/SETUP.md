# Setup da zero su un nuovo PC

Obiettivo: arrivare in ~15 minuti allo stesso stato di lavoro del PC originale
(repository clonato, ROM al loro posto, `dsrom` scaricato, round-trip verificato).

## 1. Software da installare

| Cosa | Versione | Windows | Linux | macOS | Serve per |
|---|---|---|---|---|---|
| Git | ≥ 2.40 | https://git-scm.com (include Git Credential Manager) | pacchetto `git` | `xcode-select --install` o Homebrew | repository |
| Python | ≥ 3.12 | https://python.org (spuntare "Add to PATH") | pacchetto `python3` | Homebrew `python` | tutti gli script (solo libreria standard, niente `pip install`) |
| melonDS | ultima stabile | https://melonds.kuribo64.net | idem | idem | provare le ROM generate |
| DSPRE Reloaded | 2.3.2 | https://github.com/DS-Pokemon-Rom-Editor/DSPRE/releases → `DSPRE-win-Portable.zip` (richiede .NET Framework 4.8, già presente su Windows 10/11) | build "canary Avalonia" linux-x64 (sperimentale) | non disponibile | ispezione visiva dei dati (opzionale) |
| PKHeX | ultima | https://github.com/kwsch/PKHeX | — | — | controllo dei salvataggi (opzionale) |
| Claude Code | ultima | desktop app o CLI | CLI | desktop app o CLI | per continuare il lavoro con l'assistente |

`dsrom` (estrazione/ricostruzione ROM) **non** si installa a mano: lo scarica lo script al passo 5,
a versione fissata e con verifica SHA256. Su macOS non c'è un binario ufficiale (e il crate non è su
crates.io): installare Rust (https://rustup.rs) e poi
`cargo install --git https://github.com/AetiasHax/ds-rom --tag v0.8.0 ds-rom-cli --root tools/bin-cargo`,
quindi copiare `tools/bin-cargo/bin/dsrom` in `tools/bin/dsrom`.

## 2. Clonare il repository

```
git clone https://github.com/SimpleMatt7/Pokemon-Crystal-New.git
cd Pokemon-Crystal-New
git switch dev
```
Alla prima operazione con GitHub, Git Credential Manager apre il browser: accedere con **SimpleMatt7**.

## 3. Configurazione locale del clone (una volta)

Solo a livello di repository (niente `--global`, così non si toccano altri account):
```
git config user.name "SimpleMatt7"
git config user.email "9123042+SimpleMatt7@users.noreply.github.com"
git config credential.https://github.com.username SimpleMatt7
git config core.hooksPath tools/hooks
```
L'ultima riga attiva l'hook che impedisce di committare ROM e file estratti. Verifica:
`git config --local --list`.

Su Linux/macOS, se l'hook non parte: `chmod +x tools/hooks/pre-commit`.

## 4. Mettere le ROM

Copiare i propri dump in `roms/` (cartella ignorata da git), come `.nds` o dentro `.zip`, con qualsiasi nome:
```
roms/
  Pokemon - Versione Oro HeartGold (Italy).zip      <- indispensabile (IPKI)
  ... (IPGI, IPKE, IPGE opzionali)
```
Verifica:
```
python tools/roms.py
```
Deve stampare `IPKI  OK`. Gli SHA1 attesi sono in NOTES.md §9. Se dice `HASH DIVERSO`, il dump non è quello
di riferimento: le patch BPS non si applicheranno.

## 5. Scaricare i tool e verificare la catena

```
python tools/get_tools.py      # scarica dsrom v0.8.0 in tools/bin/ e ne verifica lo SHA256
python tools/roundtrip.py      # estrae IPKI in work/IPKI, ricostruisce out/roundtrip_IPKI.nds, confronta
```
Esito atteso dell'ultimo comando (circa 25 s):
```
2 intervalli diversi, 4 byte in totale:
  0x0000006C-0x0000006E (2 byte)  [CRC area sicura]
  0x0000015E-0x00000160 (2 byte)  [CRC header]
ESITO: OK (solo CRC header)
```
Poi:
```
python tools/probe.py          # dove compaiono specie > #251 (deve dare gli stessi numeri di NOTES.md §5)
```

## 6. Riprendere il lavoro con Claude Code

Aprire Claude Code nella cartella del clone. Legge automaticamente `CLAUDE.md`, che rimanda a `NOTES.md`
(stato, decisioni, prossimi passi). Primo messaggio suggerito:
"Leggi NOTES.md e riprendi dai prossimi passi."

## Cosa NON viene dal repository (e perché)
| Cosa | Dove sta | Come si ricrea |
|---|---|---|
| ROM | `roms/` | dump propri, copiati a mano |
| `dsrom` | `tools/bin/` | `python tools/get_tools.py` |
| Estrazioni | `work/` | `python tools/roundtrip.py` |
| ROM generate | `out/` | script di build (fase 4) |
| DSPRE, melonDS | installati nel sistema | link sopra |
