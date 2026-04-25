"""Calcolo SAL (Stato Avanzamento Lavori) progressivo per mese."""

from __future__ import annotations

import re

from . import repo

_MESE_REGEX = re.compile(r"^\d{4}-(0[1-9]|1[0-2])$")
_RITENUTA_GARANZIA = 0.005  # 0,5% ex art. 30 c. 5-bis D.Lgs. 50/2016


def sal_progressivo(cantiere_id: str, mese: str) -> dict:
    if not _MESE_REGEX.match(mese):
        raise ValueError(
            f"Formato mese non valido: '{mese}'. Atteso 'YYYY-MM' (es. '2026-03')."
        )

    cantiere = repo.get_cantiere(cantiere_id)
    sal_list = sorted(cantiere.get("sal", []), key=lambda s: s["mese"])

    sal_target = next((s for s in sal_list if s["mese"] == mese), None)
    if sal_target is None:
        mesi_disponibili = ", ".join(s["mese"] for s in sal_list) or "(nessuno)"
        raise ValueError(
            f"Nessun SAL per il mese '{mese}' sul cantiere '{cantiere_id}'. "
            f"Mesi disponibili: {mesi_disponibili}."
        )

    progressivo = sum(s["importo_periodo"] for s in sal_list if s["mese"] <= mese)
    importo_periodo = sal_target["importo_periodo"]
    importo_contrattuale = cantiere["importo_contrattuale"]
    percentuale = round(progressivo / importo_contrattuale * 100, 2)

    ritenuta = round(importo_periodo * _RITENUTA_GARANZIA, 2)
    netto = round(importo_periodo - ritenuta, 2)

    return {
        "cantiere_id": cantiere_id,
        "numero_sal": sal_target["numero"],
        "mese": mese,
        "importo_periodo": importo_periodo,
        "importo_progressivo": round(progressivo, 2),
        "importo_contrattuale": importo_contrattuale,
        "percentuale_completamento": percentuale,
        "ritenuta_garanzia": ritenuta,
        "importo_netto_da_liquidare": netto,
        "lavorazioni": sal_target.get("lavorazioni", []),
    }
