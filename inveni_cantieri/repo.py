"""Data layer: legge i cantieri da un file JSON.

Per default usa il file di esempio dentro il package (`data/cantieri.json`).
Se è impostata la variabile d'ambiente `INVENI_CANTIERI_DATA`, legge invece
da quel percorso (es. file dentro la cartella MEGA condivisa con l'ufficio).

Nessuna cache: il file viene riletto ad ogni chiamata, così le modifiche
sincronizzate da MEGA / OneDrive sono visibili subito senza riavviare l'MCP.

Unico punto da rifattorizzare per integrare un backend reale (DB / REST INVENI):
le funzioni pubbliche `list_cantieri` / `get_cantiere` restano invariate,
cambia solo l'implementazione interna.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

_DEFAULT_PATH = Path(__file__).resolve().parent.parent / "data" / "cantieri.json"
_ENV_VAR = "INVENI_CANTIERI_DATA"


def data_path() -> Path:
    custom = os.environ.get(_ENV_VAR)
    return Path(custom).expanduser() if custom else _DEFAULT_PATH


def _load() -> dict:
    path = data_path()
    if not path.exists():
        raise FileNotFoundError(
            f"File dati cantieri non trovato: {path}. "
            f"Imposta la variabile d'ambiente {_ENV_VAR} sul percorso "
            f"del file 'cantieri.json' (es. dentro la cartella MEGA condivisa)."
        )
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def list_cantieri() -> list[dict]:
    return list(_load()["cantieri"])


def get_cantiere(cantiere_id: str) -> dict:
    cantieri = _load()["cantieri"]
    for c in cantieri:
        if c["id"] == cantiere_id:
            return c
    raise ValueError(
        f"Cantiere '{cantiere_id}' non trovato. ID disponibili: "
        + ", ".join(c["id"] for c in cantieri)
    )
