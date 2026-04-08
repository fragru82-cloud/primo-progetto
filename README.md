# Strapi MCP Server per Claude

MCP Server che collega Claude a Strapi CMS, permettendo la gestione completa dei contenuti via chat.

## Funzionalità

- **CRUD completo** su qualsiasi content type di Strapi
- **Media Library** — upload, elenco, eliminazione file
- **Ricerca** — cerca testo nelle collection
- **Schema** — esplora i content type e i loro campi
- **Utenti** — elenco utenti (con permessi admin)

## Prerequisiti

- Python 3.10+
- Strapi v4/v5 in esecuzione (locale o su VPS)
- Un API Token Strapi con accesso Full Access

## Setup rapido

### 1. Installa Strapi (se non l'hai già)

```bash
npx create-strapi-app@latest my-project --quickstart
```

### 2. Genera un API Token

1. Vai su **Settings → API Tokens → Create new API Token**
2. Nome: `Claude MCP`
3. Tipo: **Full Access**
4. Copia il token

### 3. Installa le dipendenze del MCP server

```bash
cd strapi-mcp-server
pip install -r requirements.txt
```

### 4. Configura Claude Desktop

Aggiungi al file `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "strapi": {
      "command": "python",
      "args": ["/PERCORSO/COMPLETO/strapi-mcp-server/server.py"],
      "env": {
        "STRAPI_URL": "http://localhost:1337",
        "STRAPI_TOKEN": "IL-TUO-TOKEN-STRAPI"
      }
    }
  }
}
```

> **VPS**: sostituisci `localhost:1337` con `http://TUO-IP:1337`

### 5. Riavvia Claude Desktop

Il server Strapi apparirà tra gli MCP disponibili.

## Strumenti disponibili

| Tool | Descrizione |
|------|-------------|
| `list_content_types` | Elenca i content type disponibili |
| `get_content_type_schema` | Mostra i campi di un content type |
| `list_entries` | Elenca entry con filtri, paginazione, ordinamento |
| `get_entry` | Ottieni una entry per ID |
| `create_entry` | Crea una nuova entry |
| `update_entry` | Aggiorna una entry |
| `delete_entry` | Elimina una entry |
| `search_entries` | Cerca testo nelle entry |
| `list_media` | Elenca i file nella media library |
| `upload_media` | Carica un file |
| `delete_media` | Elimina un file |
| `list_users` | Elenca gli utenti |

## Esempi di utilizzo in Claude

Una volta configurato, puoi chiedere a Claude:

- *"Mostrami tutti i content type di Strapi"*
- *"Crea un nuovo articolo con titolo 'Hello World'"*
- *"Cerca tutti gli articoli che contengono 'marketing'"*
- *"Elenca le ultime 10 entry della collection 'products'"*
- *"Aggiorna l'articolo 5 cambiando il titolo"*
