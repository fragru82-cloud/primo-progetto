"""Data layer mock: legge i cantieri da data/cantieri.json.

Unico punto da rifattorizzare per integrare un backend reale (DB / REST INVENI):
le funzioni pubbliche restano invariate, cambia solo l'implementazione interna.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

_DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "cantieri.json"


@lru_cache(maxsize=1)
def _load() -> dict:
    with _DATA_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def list_cantieri() -> list[dict]:
    return list(_load()["cantieri"])


def get_cantiere(cantiere_id: str) -> dict:
    for c in _load()["cantieri"]:
        if c["id"] == cantiere_id:
            return c
    raise ValueError(
        f"Cantiere '{cantiere_id}' non trovato. ID disponibili: "
        + ", ".join(c["id"] for c in _load()["cantieri"])
    )
