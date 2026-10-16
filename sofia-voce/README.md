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
