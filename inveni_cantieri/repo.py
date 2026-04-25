"""Data layer: legge i cantieri da un file JSON e localizza le cartelle reali.

Configurazione tramite due variabili d'ambiente:

- `INVENI_CANTIERI_DATA`: percorso del file JSON anagrafica (es. dentro MEGA).
  Default: file di esempio nel package.

- `INVENI_CANTIERI_BASE`: percorso della cartella `cantieri e contratti` su
  MEGA, contenitore delle sottocartelle dei singoli cantieri.
  Serve a `checklist_preparazione` per leggere i file effettivi sul filesystem.
  Default: `data/cantieri_demo` nel package (folder fittizio per test).

Nessuna cache: il file viene riletto ad ogni chiamata, così le modifiche
sincronizzate da MEGA sono visibili subito senza riavviare l'MCP.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

_PKG_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_DATA = _PKG_ROOT / "data" / "cantieri.json"
_DEFAULT_BASE = _PKG_ROOT / "data" / "cantieri_demo"

ENV_DATA = "INVENI_CANTIERI_DATA"
ENV_BASE = "INVENI_CANTIERI_BASE"


def data_path() -> Path:
    custom = os.environ.get(ENV_DATA)
    return Path(custom).expanduser() if custom else _DEFAULT_DATA


def base_path() -> Path:
    custom = os.environ.get(ENV_BASE)
    return Path(custom).expanduser() if custom else _DEFAULT_BASE


def _load() -> dict:
    path = data_path()
    if not path.exists():
        raise FileNotFoundError(
            f"File dati cantieri non trovato: {path}. "
            f"Imposta la variabile d'ambiente {ENV_DATA} sul percorso "
            f"del file 'cantieri.json' (es. dentro la cartella MEGA condivisa)."
        )
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def list_cantieri() -> list[dict]:
    return list(_load()["cantieri"])


def get_cantiere(cantiere_id: str) -> dict:
    cantieri = _load()["cantieri"]
    for c in cantieri:
        if c["id"].upper() == cantiere_id.upper():
            return c
    raise ValueError(
        f"Cantiere '{cantiere_id}' non trovato. ID disponibili: "
        + ", ".join(c["id"] for c in cantieri)
    )


def azienda() -> dict:
    return _load().get("azienda", {})


def cantiere_folder(cantiere: dict) -> Path:
    base = base_path()
    folder = base / cantiere["cartella"]
    return folder
