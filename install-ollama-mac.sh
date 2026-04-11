#!/usr/bin/env bash
#
# install-ollama-mac.sh
# Installa Ollama su macOS e scarica il miglior modello compatibile
# con la RAM disponibile sulla macchina.
#
# Uso:
#   ./install-ollama-mac.sh              # sceglie automaticamente il modello in base alla RAM
#   ./install-ollama-mac.sh llama3.3     # forza un modello specifico
#
set -euo pipefail

# ----- utility di output -----
info()  { printf "\033[1;34m[INFO]\033[0m  %s\n" "$*"; }
ok()    { printf "\033[1;32m[OK]\033[0m    %s\n" "$*"; }
warn()  { printf "\033[1;33m[WARN]\033[0m  %s\n" "$*"; }
error() { printf "\033[1;31m[ERR]\033[0m   %s\n" "$*" >&2; }

# ----- controllo sistema operativo -----
if [[ "$(uname -s)" != "Darwin" ]]; then
    error "Questo script è pensato per macOS. Sistema rilevato: $(uname -s)"
    exit 1
fi

info "macOS rilevato: $(sw_vers -productVersion) ($(uname -m))"

# ----- installazione Homebrew se mancante -----
if ! command -v brew >/dev/null 2>&1; then
    info "Homebrew non trovato. Lo installo..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

    # Aggiunge brew al PATH per Apple Silicon
    if [[ -x /opt/homebrew/bin/brew ]]; then
        eval "$(/opt/homebrew/bin/brew shellenv)"
    elif [[ -x /usr/local/bin/brew ]]; then
        eval "$(/usr/local/bin/brew shellenv)"
    fi
else
    ok "Homebrew già installato: $(brew --version | head -n1)"
fi

# ----- installazione Ollama -----
if ! command -v ollama >/dev/null 2>&1; then
    info "Installo Ollama tramite Homebrew..."
    brew install --cask ollama
else
    ok "Ollama già installato: $(ollama --version 2>/dev/null || echo 'sconosciuta')"
fi

# ----- avvio del servizio Ollama in background -----
if ! pgrep -x "ollama" >/dev/null 2>&1; then
    info "Avvio del servizio Ollama..."
    # L'app .cask installa Ollama.app; proviamo prima ad avviarla
    if [[ -d "/Applications/Ollama.app" ]]; then
        open -a Ollama
    else
        nohup ollama serve >/tmp/ollama.log 2>&1 &
    fi
    # Attende che il server sia pronto
    for i in {1..20}; do
        if curl -fsS http://127.0.0.1:11434/api/tags >/dev/null 2>&1; then
            break
        fi
        sleep 1
    done
fi

if curl -fsS http://127.0.0.1:11434/api/tags >/dev/null 2>&1; then
    ok "Servizio Ollama attivo su http://127.0.0.1:11434"
else
    warn "Il servizio Ollama non risponde ancora. Avvialo manualmente con: ollama serve"
fi

# ----- scelta del modello in base alla RAM -----
# RAM totale in GB (macOS: hw.memsize è in byte)
RAM_BYTES=$(sysctl -n hw.memsize)
RAM_GB=$(( RAM_BYTES / 1024 / 1024 / 1024 ))
info "RAM totale rilevata: ${RAM_GB} GB"

MODEL="${1:-}"
if [[ -z "${MODEL}" ]]; then
    # Strategia: prendi il modello più capace che gira comodamente con la RAM disponibile.
    # I requisiti indicativi sono per inference in quantizzazione Q4_K_M.
    if   (( RAM_GB >= 128 )); then MODEL="llama3.1:405b-instruct-q2_K"   # top assoluto (molto grande)
    elif (( RAM_GB >= 64  )); then MODEL="llama3.3:70b"                  # miglior rapporto qualità/risorse
    elif (( RAM_GB >= 48  )); then MODEL="qwen2.5:32b"                   # ottimo reasoning, sta in 48GB
    elif (( RAM_GB >= 32  )); then MODEL="qwen2.5:32b"                   # sta al limite, comunque eccellente
    elif (( RAM_GB >= 24  )); then MODEL="llama3.1:8b"                   # veloce e versatile
    elif (( RAM_GB >= 16  )); then MODEL="llama3.1:8b"                   # default affidabile
    else                           MODEL="llama3.2:3b"                   # per Mac con poca RAM
    fi
fi

info "Modello selezionato: ${MODEL}"
info "Avvio download (può richiedere tempo e diversi GB di spazio)..."
ollama pull "${MODEL}"

ok "Modello '${MODEL}' pronto all'uso."
echo
echo "Per avviare una conversazione:"
echo "    ollama run ${MODEL}"
echo
echo "Per vedere i modelli installati:"
echo "    ollama list"
