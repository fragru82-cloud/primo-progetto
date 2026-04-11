# primo-progetto

## Installazione di Ollama su macOS

Questo repository contiene uno script per installare [Ollama](https://ollama.com)
su macOS e scaricare automaticamente il miglior modello linguistico compatibile
con la RAM del tuo Mac.

### Uso rapido

```bash
chmod +x install-ollama-mac.sh
./install-ollama-mac.sh
```

Lo script si occupa di:

1. Verificare che tu stia usando macOS.
2. Installare Homebrew se non è già presente.
3. Installare Ollama tramite `brew install --cask ollama`.
4. Avviare il servizio Ollama (`http://127.0.0.1:11434`).
5. Rilevare la RAM e scaricare il modello più capace compatibile.

### Scelta del modello (automatica)

| RAM del Mac | Modello scelto                 | Note                                |
|-------------|--------------------------------|-------------------------------------|
| ≥ 128 GB    | `llama3.1:405b-instruct-q2_K`  | Top assoluto, molto grande          |
| ≥ 64 GB     | `llama3.3:70b`                 | Miglior rapporto qualità/risorse    |
| ≥ 32 GB     | `qwen2.5:32b`                  | Eccellente su reasoning e coding    |
| ≥ 16 GB     | `llama3.1:8b`                  | Veloce e versatile                  |
| < 16 GB     | `llama3.2:3b`                  | Per Mac con RAM limitata            |

Puoi anche forzare un modello specifico:

```bash
./install-ollama-mac.sh llama3.3:70b
```

### Esecuzione

Dopo l'installazione, per chattare con il modello:

```bash
ollama run llama3.3:70b
```

Per elencare i modelli installati:

```bash
ollama list
```

### Requisiti

- macOS (Apple Silicon consigliato per i modelli più grandi).
- Connessione Internet per scaricare Ollama e i modelli.
- Spazio libero su disco sufficiente (da ~2 GB per `llama3.2:3b` fino a oltre
  150 GB per `llama3.1:405b`).
