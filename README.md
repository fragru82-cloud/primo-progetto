# INVENI Cantieri - MCP server

Estensione MCP del Windows VPS Manager con tool dedicati alla gestione
cantieri (edilizia / appalti pubblici, dominio italiano).

## Tool esposti

| Tool | Parametri | Cosa fa |
|---|---|---|
| `cantiere_anagrafica` | `cantiere_id` | Anagrafica completa: CIG/CUP, ubicazione, committente con RUP, impresa, importo, date, DL, CSE, stato. |
| `genera_documento` | `tipo`, `cantiere_id` | Genera in markdown verbali (inizio / sospensione / ripresa / ultimazione), SAL, certificato di pagamento, comunicazione al committente, ordine di servizio. |
| `scadenze_compliance` | `cantiere_id` | Stato DURC, SOA, antimafia, polizze CAR/RC, POS, PSC, formazione sicurezza, con flag `ok` / `in_scadenza` (≤ 30 gg) / `scaduto`. |
| `sal_progressivo` | `cantiere_id`, `mese` (`YYYY-MM`) | SAL del mese con importo periodo, progressivo, % completamento, ritenuta 0,5%, netto da liquidare, dettaglio lavorazioni. |
| `notifica_committente` | `cantiere_id`, `evento` | Costruisce e simula invio PEC al RUP per: inizio, sospensione, ripresa, ultimazione, SAL emesso, anomalia, richiesta variante. |

## Requisiti

- Python 3.10+ (Mac: già preinstallato; Windows: scaricare da [python.org](https://www.python.org/))
- Claude Desktop (Mac e/o Windows)
- (Opzionale) MEGA installato e sincronizzato sulle macchine che vuoi tengano allineati i dati

## Installazione

Da dentro la cartella del progetto:

```bash
pip install -e .
```

Crea il comando `inveni-cantieri-mcp` (su Windows: `inveni-cantieri-mcp.exe`).

## Setup condiviso via MEGA (Mac + PC ufficio)

L'MCP server è un programma **locale**: lo installi su ogni macchina che vuoi
usare. Per condividere i dati dei cantieri tra Mac e PC ufficio, il file
`cantieri.json` va salvato nella cartella **MEGA condivisa**: entrambe le
installazioni leggono lo stesso file e MEGA si occupa della sincronizzazione.

### 1. Prepara la cartella in MEGA (una sola volta, da Mac o da PC)

Crea dentro la tua cartella MEGA una sottocartella `INVENI` e copiaci dentro
il file `cantieri.json` di esempio del progetto:

```
MEGA/INVENI/cantieri.json
```

MEGA lo sincronizzerà automaticamente sulla seconda macchina.

### 2. Configurazione su Mac

Modifica il file di configurazione di Claude Desktop:

`~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "inveni-cantieri": {
      "command": "inveni-cantieri-mcp",
      "env": {
        "INVENI_CANTIERI_DATA": "/Users/aloefrancesco/Documents/MEGA/INVENI/cantieri.json"
      }
    }
  }
}
```

> ⚠️ Verifica il nome esatto della tua cartella MEGA. Da Terminale:
> `ls -d ~/Documents/MEGA*` — potrebbe essere `MEGA`, `MEGAsync`, ecc.
> Adatta il percorso di conseguenza.

Riavvia Claude Desktop. Lo strumento `inveni-cantieri` deve comparire fra gli
MCP attivi.

### 3. Configurazione su PC ufficio (Windows)

Modifica il file:

`%APPDATA%\Claude\claude_desktop_config.json`
(percorso completo: `C:\Users\<TUO_UTENTE>\AppData\Roaming\Claude\claude_desktop_config.json`)

```json
{
  "mcpServers": {
    "inveni-cantieri": {
      "command": "inveni-cantieri-mcp.exe",
      "env": {
        "INVENI_CANTIERI_DATA": "C:/Users/<TUO_UTENTE>/Documents/MEGA/INVENI/cantieri.json"
      }
    }
  }
}
```

> ⚠️ Sostituisci `<TUO_UTENTE>` col tuo nome utente Windows. Usa le **slash
> normali** `/` nel JSON (più semplici); in alternativa raddoppia i backslash:
> `"C:\\Users\\..."`.

Riavvia Claude Desktop sul PC.

### 4. Caricamento insieme al Windows VPS Manager

Sono due server MCP indipendenti, quindi convivono nella stessa configurazione:

```json
{
  "mcpServers": {
    "windows-vps-manager": { "command": "vps-manager-mcp" },
    "inveni-cantieri": {
      "command": "inveni-cantieri-mcp",
      "env": { "INVENI_CANTIERI_DATA": "/Users/aloefrancesco/Documents/MEGA/INVENI/cantieri.json" }
    }
  }
}
```

## Come funziona la sincronizzazione

- Il server MCP **rilegge il file ad ogni chiamata**, quindi quando MEGA
  sincronizza una modifica fatta sull'altra macchina la vedi subito senza
  riavviare Claude Desktop.
- Oggi i tool sono **read-only**: nessuna scrittura, nessun rischio di
  conflitti MEGA. Se in futuro aggiungiamo funzioni di scrittura conviene
  passare a un file per cantiere o a un piccolo SQLite condiviso.

## Esempi di chiamata da Claude

Una volta installato e configurato, in Claude Desktop puoi chiedere cose tipo:

> "Quali scadenze critiche ha il cantiere C001?"
> "Generami il verbale di sospensione per il cantiere C003"
> "Quanto vale il SAL di febbraio del cantiere di Milano?"
> "Prepara la PEC al RUP del cantiere C001 per l'emissione del SAL"

## Variabile d'ambiente

| Variabile | Default | Descrizione |
|---|---|---|
| `INVENI_CANTIERI_DATA` | `<package>/data/cantieri.json` | Percorso assoluto del file JSON dei cantieri. Imposta su file dentro MEGA per la sincronizzazione cross-PC. |

Se la variabile non è impostata, il server usa il file di esempio incluso nel
package (utile per test, ma non condiviso).

## Note v0.1

- Read-only: i tool non modificano `cantieri.json`.
- `notifica_committente` non invia PEC reali (`stato: "simulata"`); per l'invio
  reale sostituire `inveni_cantieri/notifications.py::notifica` con un client
  PEC/SMTP.
- `genera_documento` produce markdown; per esportare in PDF si può aggiungere
  un passaggio con `weasyprint` o simile.
- Per integrare un backend INVENI reale (DB / REST) sostituire solo
  `inveni_cantieri/repo.py`: l'interfaccia resta invariata.
