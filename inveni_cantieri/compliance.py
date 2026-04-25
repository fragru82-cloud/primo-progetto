"""Calcolo scadenze compliance per un cantiere."""

from __future__ import annotations

from datetime import date

from . import repo

# Etichette leggibili per le voci di compliance presenti nel JSON.
_DESCRIZIONI = {
    "durc": "DURC - Documento Unico di Regolarità Contributiva",
    "soa": "Attestazione SOA",
    "antimafia": "Comunicazione antimafia",
    "polizza_car": "Polizza CAR (Contractors All Risks)",
    "polizza_rc": "Polizza RC verso terzi",
    "pos": "Piano Operativo di Sicurezza (POS)",
    "psc": "Piano di Sicurezza e Coordinamento (PSC)",
    "formazione_sicurezza": "Formazione sicurezza lavoratori",
}

_SOGLIA_IN_SCADENZA_GG = 30


def _stato(giorni_residui: int) -> str:
    if giorni_residui < 0:
        return "scaduto"
    if giorni_residui <= _SOGLIA_IN_SCADENZA_GG:
        return "in_scadenza"
    return "ok"


def scadenze(cantiere_id: str, oggi: date | None = None) -> dict:
    cantiere = repo.get_cantiere(cantiere_id)
    oggi = oggi or date.today()

    voci = []
    for chiave, scadenza_iso in cantiere.get("compliance", {}).items():
        scadenza = date.fromisoformat(scadenza_iso)
        giorni = (scadenza - oggi).days
        voci.append(
            {
                "tipo": chiave,
                "descrizione": _DESCRIZIONI.get(chiave, chiave),
                "data_scadenza": scadenza_iso,
                "giorni_residui": giorni,
                "stato": _stato(giorni),
            }
        )

    voci.sort(key=lambda v: v["giorni_residui"])
    critiche = sum(1 for v in voci if v["stato"] != "ok")

    return {
        "cantiere_id": cantiere_id,
        "data_riferimento": oggi.isoformat(),
        "totale_critiche": critiche,
        "scadenze": voci,
    }
