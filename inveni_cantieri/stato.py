"""Riepilogo dello stato di preparazione di un cantiere.

Si appoggia a `checklist.checklist_preparazione` aggregando i risultati in
una vista sintetica: % completamento, bloccanti, opzionali mancanti, pronto a
partire.
"""

from __future__ import annotations

from . import checklist


def stato_preparazione(cantiere_id: str) -> dict:
    report = checklist.checklist_preparazione(cantiere_id)

    bloccanti: list[dict] = []
    opzionali_mancanti: list[dict] = []

    for cat in report["categorie"]:
        for voce in cat["voci"]:
            if voce["presente"]:
                continue
            riga = {
                "categoria": cat["categoria"],
                "documento": voce["documento"],
                "ambito": voce["ambito"],
            }
            if voce["obbligatorieta"] == "obbligatorio":
                bloccanti.append(riga)
            else:
                opzionali_mancanti.append(riga)

    pronto = len(bloccanti) == 0

    return {
        "cantiere_id": cantiere_id,
        "cantiere_nome": report["cantiere_nome"],
        "percentuale_completamento": report["percentuale_completamento"],
        "totale_attesi": report["totale_attesi"],
        "totale_presenti": report["totale_presenti"],
        "pronto_a_partire": pronto,
        "documenti_bloccanti_mancanti": bloccanti,
        "documenti_opzionali_mancanti": opzionali_mancanti,
        "cartella": report["cartella"],
    }
