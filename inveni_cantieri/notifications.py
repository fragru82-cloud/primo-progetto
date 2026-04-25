"""Costruzione e 'invio' notifiche al committente.

v0.1: invio simulato (stato='simulata'). Per integrare un reale invio PEC/SMTP,
sostituire `_invia` con un client appropriato senza toccare i template.
"""

from __future__ import annotations

import logging
import uuid
from datetime import datetime

from . import repo

log = logging.getLogger(__name__)

EVENTI_AMMESSI = (
    "inizio_lavori",
    "sospensione",
    "ripresa",
    "ultimazione",
    "sal_emesso",
    "anomalia",
    "richiesta_variante",
)


def _template(evento: str, cantiere: dict) -> tuple[str, str]:
    nome = cantiere["nome"]
    rup = cantiere["committente"]["rup"]
    impresa = cantiere["impresa_appaltatrice"]["ragione_sociale"]

    if evento == "inizio_lavori":
        return (
            f"[Cantiere {cantiere['id']}] Avvio lavori - {nome}",
            f"Spett.le RUP {rup},\nsi comunica l'avvio dei lavori del cantiere "
            f"'{nome}' a far data odierna. Restiamo a disposizione per la firma "
            f"del verbale di consegna.\n\nL'Impresa: {impresa}.",
        )
    if evento == "sospensione":
        return (
            f"[Cantiere {cantiere['id']}] Sospensione lavori - {nome}",
            f"Spett.le RUP {rup},\nsi comunica la sospensione delle lavorazioni "
            f"per cause da circostanziare nel verbale di sospensione. "
            f"La ripresa sarà tempestivamente comunicata.",
        )
    if evento == "ripresa":
        return (
            f"[Cantiere {cantiere['id']}] Ripresa lavori - {nome}",
            f"Spett.le RUP {rup},\nessendo cessate le cause della sospensione, "
            f"si comunica la ripresa delle lavorazioni a far data odierna.",
        )
    if evento == "ultimazione":
        return (
            f"[Cantiere {cantiere['id']}] Ultimazione lavori - {nome}",
            f"Spett.le RUP {rup},\nsi comunica l'avvenuta ultimazione delle opere. "
            f"Si richiede l'avvio delle procedure di collaudo / CRE.",
        )
    if evento == "sal_emesso":
        return (
            f"[Cantiere {cantiere['id']}] Emissione SAL - {nome}",
            f"Spett.le RUP {rup},\nsi trasmette nuovo Stato Avanzamento Lavori "
            f"per il cantiere in oggetto, ai fini della liquidazione "
            f"del relativo certificato di pagamento.",
        )
    if evento == "anomalia":
        return (
            f"[Cantiere {cantiere['id']}] Segnalazione anomalia - {nome}",
            f"Spett.le RUP {rup},\nsi segnala un'anomalia riscontrata in cantiere "
            f"che richiede valutazione congiunta. Restiamo in attesa di "
            f"sopralluogo o riscontro scritto.",
        )
    if evento == "richiesta_variante":
        return (
            f"[Cantiere {cantiere['id']}] Richiesta perizia di variante - {nome}",
            f"Spett.le RUP {rup},\nstante l'insorgenza di circostanze sopravvenute "
            f"non prevedibili, si richiede l'autorizzazione a redigere perizia "
            f"di variante ai sensi della normativa vigente.",
        )
    raise ValueError(
        f"Evento non supportato: '{evento}'. Eventi ammessi: {', '.join(EVENTI_AMMESSI)}."
    )


def notifica(cantiere_id: str, evento: str) -> dict:
    cantiere = repo.get_cantiere(cantiere_id)
    oggetto, corpo = _template(evento, cantiere)

    destinatario = cantiere["committente"].get("pec") or cantiere["committente"]["email"]
    notifica_id = f"NOT-{uuid.uuid4().hex[:8].upper()}"
    inviata_at = datetime.now().isoformat(timespec="seconds")

    log.info("Notifica simulata %s -> %s [%s]", notifica_id, destinatario, evento)

    return {
        "notifica_id": notifica_id,
        "cantiere_id": cantiere_id,
        "evento": evento,
        "destinatario": destinatario,
        "canale": "PEC",
        "oggetto": oggetto,
        "corpo": corpo,
        "inviata_at": inviata_at,
        "stato": "simulata",
    }
