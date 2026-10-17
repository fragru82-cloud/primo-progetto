# Sofia Voce

Sintesi vocale con voce clonata per l'assistente Sofia (vocali WhatsApp/Telegram).

## Configurazione approvata
- Motore: Chatterbox Multilingual (licenza MIT), lingua `it`
- Riferimento: registrazione "01. Presentazione" (voce 1)
- Parametri: `exaggeration=0.5`, `cfg_weight=0.4`, `temperature=0.6`
- Velocità: +15% (`atempo=1.15`, timbro invariato)
- Controllo pronuncia: fino a 5 tentativi per frase, ritrascrizione con faster-whisper `medium`, si tiene la versione con meno errori
- Uscita: OGG/Opus mono 48 kHz 32 kbps (formato vocale WhatsApp/Telegram)

## Installazione
Python 3.11. Su PC con GPU NVIDIA installare torch CUDA, poi:

    pip install -r requirements.txt

## Uso
    python sofia_voce.py <riferimento.wav> <cartella_uscita>

Il file di riferimento (voce di Cristina Melito) NON va nel repository: è un dato
personale coperto dalla liberatoria firmata con Globalink S.r.l.s.

## Correzioni di pronuncia
Dizionario `LESSICO` in `sofia_voce.py`: aggiungere qui le parole che il motore legge male.

## Servizio per il bridge WhatsApp (server.py)
Stesso contratto del servizio "Voce Sofia" chiamato da `send-voice-paracadute.js` sulla VPS:
`GET /health` e `POST /tts` con `Authorization: Bearer <token>`, risposta `audio/ogg`.
Risponde 422 quando il testo non va letto a voce (file, link, elenchi, testo lungo) o la
pronuncia supera il 15% di errori: il bridge passa allora a Elsa / testo.

    set SOFIA_TOKEN=<token di sofia-voice.json>
    set SOFIA_REF=<percorso>\ref1.wav
    set SOFIA_PORT=8196
    set SOFIA_TENTATIVI=2
    set SOFIA_WHISPER=small
    python server.py

Su CPU (senza NVIDIA) un vocale breve richiede circa 1-1,5 minuti; con GPU pochi secondi.
