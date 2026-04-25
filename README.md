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

## Installazione

Richiede Python 3.10+.

```bash
pip install -e .
```

Il comando installa il package e crea l'entry point `inveni-cantieri-mcp`.

## Configurazione client MCP

### Claude Desktop (`claude_desktop_config.json`)

```json
{
  "mcpServers": {
    "inveni-cantieri": {
      "command": "inveni-cantieri-mcp"
    }
  }
}
```

Caricabile insieme al Windows VPS Manager esistente (sono due server
indipendenti):

```json
{
  "mcpServers": {
    "windows-vps-manager": { "command": "vps-manager-mcp" },
    "inveni-cantieri":     { "command": "inveni-cantieri-mcp" }
  }
}
```

### Claude Code (`.mcp.json` nel progetto o globale)

```json
{
  "mcpServers": {
    "inveni-cantieri": {
      "type": "stdio",
      "command": "inveni-cantieri-mcp"
    }
  }
}
```

## Dati

Lo stato corrente è alimentato dal file `data/cantieri.json` (3 cantieri di
esempio: restauro Palazzo Comunale Roma, scuola primaria Milano, manutenzione
SP12 Treviso). Per integrare un backend reale (DB / REST INVENI) sostituire
solo `inveni_cantieri/repo.py`: l'interfaccia (`get_cantiere`, `list_cantieri`)
resta invariata, i tool non vanno toccati.

## Esempi di chiamata

```python
cantiere_anagrafica(cantiere_id="C001")
scadenze_compliance(cantiere_id="C003")        # SP12 sospesa: include voci critiche
sal_progressivo(cantiere_id="C002", mese="2026-02")
genera_documento(tipo="sal", cantiere_id="C001")
notifica_committente(cantiere_id="C001", evento="sal_emesso")
```

## Note v0.1

- Read-only: i tool non modificano `data/cantieri.json`.
- `notifica_committente` non invia PEC reali (`stato: "simulata"`); per l'invio
  reale sostituire `inveni_cantieri/notifications.py::notifica` con un client
  PEC/SMTP.
- `genera_documento` produce markdown; per esportare in PDF si può aggiungere
  un passaggio con `weasyprint` o simile.
