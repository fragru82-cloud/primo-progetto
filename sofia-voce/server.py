"""Servizio HTTP "Voce Sofia" con la voce di Cristina.

Stesso contratto del servizio che chiama il bridge WhatsApp sulla VPS
(send-voice-paracadute.js), così basta cambiare l'URL in sofia-voice.json:

  GET  /health  -> {"loaded": bool, "queue": int, "max_queue": int}
  POST /tts     {"text": "..."} -> audio/ogg (Opus), oppure
                422 se il testo non va letto a voce o la pronuncia non è affidabile
                (il bridge passa allora a Elsa / testo scritto).

Entrambi richiedono l'header  Authorization: Bearer <SOFIA_TOKEN>.

Variabili d'ambiente:
  SOFIA_TOKEN   token condiviso con la VPS (obbligatorio, min 16 caratteri)
  SOFIA_REF     file WAV di riferimento della voce (obbligatorio)
  SOFIA_HOST    default 0.0.0.0
  SOFIA_PORT    default 8196
  SOFIA_MAX_QUEUE  richieste in attesa accettate, default 3
  SOFIA_TENTATIVI / SOFIA_WHISPER  vedi sofia_voce.py
"""
import asyncio
import hmac
import os
import tempfile
import threading
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel

from sofia_voce import NonAdattoAVoce, SofiaVoce

TOKEN = os.environ.get("SOFIA_TOKEN", "")
REF = os.environ.get("SOFIA_REF", "")
MAX_QUEUE = int(os.environ.get("SOFIA_MAX_QUEUE", "3"))
MAX_TESTO = 1000

app = FastAPI(title="Sofia Voce")
stato = {"motore": None, "queue": 0}
lock = threading.Lock()          # una sintesi alla volta: il modello non è thread-safe


def controlla_token(authorization):
    atteso = "Bearer " + TOKEN
    if not authorization or not hmac.compare_digest(authorization.encode(), atteso.encode()):
        raise HTTPException(status_code=401, detail="non autorizzato")


class Richiesta(BaseModel):
    text: str


@app.on_event("startup")
def carica():
    if len(TOKEN) < 16:
        raise SystemExit("SOFIA_TOKEN mancante o troppo corto")
    if not Path(REF).is_file():
        raise SystemExit(f"SOFIA_REF non trovato: {REF}")
    threading.Thread(target=lambda: stato.update(motore=SofiaVoce(REF)), daemon=True).start()


@app.get("/health")
def health(authorization: str = Header(None)):
    controlla_token(authorization)
    return {"loaded": stato["motore"] is not None, "queue": stato["queue"], "max_queue": MAX_QUEUE}


def _sintetizza(testo):
    with lock, tempfile.TemporaryDirectory() as d:
        out = Path(d) / "voce.ogg"
        report = stato["motore"].sintetizza(testo, str(out))
        return out.read_bytes(), report


@app.post("/tts")
async def tts(req: Richiesta, authorization: str = Header(None)):
    controlla_token(authorization)
    testo = req.text.strip()
    if not testo or len(testo) > MAX_TESTO:
        raise HTTPException(status_code=400, detail="testo vuoto o troppo lungo")
    if stato["motore"] is None:
        raise HTTPException(status_code=503, detail="modello non caricato")
    if stato["queue"] >= MAX_QUEUE:
        raise HTTPException(status_code=429, detail="coda piena")
    stato["queue"] += 1
    try:
        audio, report = await asyncio.to_thread(_sintetizza, testo)
    except NonAdattoAVoce as e:
        raise HTTPException(status_code=422, detail=str(e))
    finally:
        stato["queue"] -= 1
    errori = max((r[0] for r in report), default=0)
    print(f"[tts] ok {len(audio)}B errore_max={errori} | {testo[:80]}", flush=True)
    return Response(content=audio, media_type="audio/ogg")


if __name__ == "__main__":
    uvicorn.run(app, host=os.environ.get("SOFIA_HOST", "0.0.0.0"),
                port=int(os.environ.get("SOFIA_PORT", "8196")))
