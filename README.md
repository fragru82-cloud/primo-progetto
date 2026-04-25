# INVENI Cantieri - MCP server (fase di preparazione)

Server MCP per Claude Desktop dedicato alla **fase di preparazione** dei
cantieri INVENI (condomini privati). Aiuta a sapere cosa hai e cosa ti manca
prima di poter avviare un cantiere, e a generare i documenti standard.

## Tool esposti (4)

| Tool | Cosa fa |
|---|---|
| `cantiere_anagrafica` | Anagrafica del cantiere: indirizzo, condominio + amministratore, CSE, importo, date previste, stato, subappaltatori. |
| `checklist_preparazione` | Va a leggere la **vera cartella** del cantiere su MEGA, confronta i file presenti con la master checklist (Documenti aziendali, Sicurezza, Dichiarazioni, Contrattualistica, Corrispondenza CSE, Subappalti) e dice per ognuno se è presente o manca. |
| `stato_preparazione` | Sintesi rapida: % completamento, documenti **obbligatori** mancanti (bloccanti), opzionali mancanti, flag `pronto_a_partire`. |
| `genera_documento` | Template markdown di: dichiarazione organico medio, idoneità tecnico-professionale, autodichiarazione patente crediti, elenco personale, lettera accompagnamento POS, accettazione PSC, verbale presa visione PSC, PEC riscontro CSE, comunicazione subappalto, comunicazione amministratore. |

## Cantieri tracciati (v0.2)

- `DONBOSCO` - Condominio Don Bosco 7
- `PETTIROSSO` - Condominio Il Pettirosso
- `CASALETTO` - Cantiere Casaletto Vaprio

## Master checklist (cosa cerca il tool)

### 01 - Documenti Aziendali (uguali per tutti i cantieri INVENI)
Visura camerale, Certificato INAIL, DOMA, Polizza RCT/RCO, Visite mediche,
Ricevuta patente crediti, Documento identità titolare, **DURC**.

### 02 - Sicurezza Cantiere
DVR, Verbale RSPP, Attestato RSPP, Nomina medico competente, Verbale RLS,
Verbale preposto, Verbale emergenze, **POS** (specifico cantiere), Elenco
personale, Elenco attrezzature/mezzi, Verbale presa visione PSC.

### 04 - Dichiarazioni e Autocertificazioni
Idoneità tecnico-professionale, Autodichiarazione patente crediti,
Dichiarazione organico medio annuo.

### 05 - Deleghe e Contrattualistica
Preventivo firmato, Capitolato firmato, Accettazione PSC, Delega fattura/pagamento.

### 06 - Corrispondenza CSE
PEC riscontro CSE.

### 07 - Subappalti
Per ogni subappaltatore registrato in anagrafica: visura, DURC, INAIL,
polizza, POS, idoneità tecnico-professionale.

## Requisiti

- Python 3.10+ (Mac: già preinstallato)
- Claude Desktop
- MEGA installato e sincronizzato

## Installazione (Mac)

Da Terminale:

```bash
mkdir -p ~/Projects
cd ~/Projects
git clone -b claude/add-inveni-cantieri-tools-w1SXo \
  https://github.com/fragru82-cloud/primo-progetto.git inveni-cantieri
cd inveni-cantieri
python3 -m venv .venv
.venv/bin/pip install -e .
echo "$PWD/.venv/bin/inveni-cantieri-mcp"
```

L'ultimo `echo` stampa il percorso assoluto del comando: ti servirà nel
config di Claude Desktop.

## Configurazione Claude Desktop

File: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "inveni-cantieri": {
      "command": "/Users/aloefrancesco/Projects/inveni-cantieri/.venv/bin/inveni-cantieri-mcp",
      "env": {
        "INVENI_CANTIERI_DATA": "/Users/aloefrancesco/MEGA/SOCIETA/Inveni/MCP-Cantieri/cantieri.json",
        "INVENI_CANTIERI_BASE": "/Users/aloefrancesco/MEGA/SOCIETA/Inveni/cantieri e contratti"
      }
    }
  }
}
```

Riavvia Claude Desktop dopo aver salvato.

### Variabili d'ambiente

| Variabile | Cosa indica |
|---|---|
| `INVENI_CANTIERI_DATA` | Percorso del file JSON con anagrafica + dati azienda. Va dentro `MEGA/SOCIETA/Inveni/MCP-Cantieri/cantieri.json` per essere sincronizzato col PC ufficio. |
| `INVENI_CANTIERI_BASE` | Percorso della cartella `cantieri e contratti` che contiene le sottocartelle dei singoli cantieri. Il tool `checklist_preparazione` la legge per verificare quali file sono presenti. |

## Setup PC ufficio (Windows)

Stesse istruzioni, percorsi adattati. Esempio config:

```json
{
  "mcpServers": {
    "inveni-cantieri": {
      "command": "C:/Projects/inveni-cantieri/.venv/Scripts/inveni-cantieri-mcp.exe",
      "env": {
        "INVENI_CANTIERI_DATA": "C:/Users/<UTENTE>/MEGA/SOCIETA/Inveni/MCP-Cantieri/cantieri.json",
        "INVENI_CANTIERI_BASE": "C:/Users/<UTENTE>/MEGA/SOCIETA/Inveni/cantieri e contratti"
      }
    }
  }
}
```

## Esempi di chiamata da Claude

> "Quanto è pronto il cantiere Don Bosco?"
> → `stato_preparazione("DONBOSCO")` → "55% completato, mancano 4 documenti bloccanti."
>
> "Cosa manca per avviare Pettirosso?"
> → `checklist_preparazione("PETTIROSSO")` → tabella PRESENTE/MANCANTE per categoria.
>
> "Generami la dichiarazione di organico medio per Casaletto."
> → `genera_documento("dichiarazione_organico_medio", "CASALETTO")` → markdown pronto da copiare in Word.

## Aggiungere un nuovo cantiere

1. Crea la cartella su MEGA: `<base>/Nuovo Cantiere/01 - Documenti Aziendali/...` ecc.
2. Aggiungi un nuovo blocco al file `cantieri.json` con `id`, `nome`, `cartella` (= nome esatto della cartella su MEGA), e gli altri campi.
3. Niente da reinstallare: il server rilegge il JSON ad ogni chiamata.

## Aggiungere/modificare voci della checklist

Modifica `inveni_cantieri/checklist.py`: la struttura `CHECKLIST` è una mappa
categoria → lista voci, ogni voce è una tupla `(nome_visualizzato, keyword,
obbligatorieta, ambito)`. Il matching è case-insensitive e ignora accenti,
spazi, underscore e trattini, quindi le keyword vanno scelte come radici
significative (es. `"durc"`, `"polizza", "rct"`).

## Note

- Tool **read-only** sul filesystem: non sposta né cancella file, solo legge nomi.
- Per `genera_documento` l'output è markdown — copialo in Word e completa i campi `___` con i dati specifici.
- Per integrare un backend reale (DB / REST INVENI) sostituire solo
  `inveni_cantieri/repo.py`.
