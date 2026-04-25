"""MCP server "INVENI Cantieri".

Espone 5 tool per la gestione cantieri:
- cantiere_anagrafica
- genera_documento
- scadenze_compliance
- sal_progressivo
- notifica_committente

Trasporto: stdio. Avviabile via `inveni-cantieri-mcp` (entry point del package)
o `python -m inveni_cantieri.server`.
"""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from . import compliance, documents, notifications, repo, sal

mcp = FastMCP("inveni-cantieri")


@mcp.tool()
def cantiere_anagrafica(cantiere_id: str) -> dict:
    """Restituisce l'anagrafica completa del cantiere indicato.

    Include identificativi (CIG/CUP), ubicazione, committente con RUP e
    contatti, impresa appaltatrice, importo contrattuale, date di inizio
    e fine prevista, direttore lavori, coordinatore sicurezza e stato
    corrente (in_corso/sospeso/ultimato).
    """
    c = repo.get_cantiere(cantiere_id)
    return {
        "id": c["id"],
        "nome": c["nome"],
        "cig": c["cig"],
        "cup": c["cup"],
        "indirizzo": c["indirizzo"],
        "stato": c["stato"],
        "data_inizio": c["data_inizio"],
        "data_fine_prevista": c["data_fine_prevista"],
        "importo_contrattuale": c["importo_contrattuale"],
        "committente": c["committente"],
        "impresa_appaltatrice": c["impresa_appaltatrice"],
        "direttore_lavori": c["direttore_lavori"],
        "coordinatore_sicurezza": c["coordinatore_sicurezza"],
    }


@mcp.tool()
def genera_documento(tipo: str, cantiere_id: str) -> dict:
    """Genera un documento di cantiere in formato markdown.

    Tipi ammessi: verbale_inizio_lavori, verbale_sospensione, verbale_ripresa,
    verbale_ultimazione, sal, certificato_pagamento, comunicazione_committente,
    ordine_di_servizio.
    """
    return documents.genera(tipo, cantiere_id)


@mcp.tool()
def scadenze_compliance(cantiere_id: str) -> dict:
    """Calcola le scadenze di compliance del cantiere (DURC, SOA, antimafia,
    polizze, POS, PSC, formazione sicurezza), con stato ok / in_scadenza
    (≤ 30 giorni) / scaduto e numero di voci critiche.
    """
    return compliance.scadenze(cantiere_id)


@mcp.tool()
def sal_progressivo(cantiere_id: str, mese: str) -> dict:
    """Restituisce il SAL del mese richiesto con importo del periodo,
    importo progressivo, percentuale di completamento, ritenuta di garanzia
    (0,5%), importo netto da liquidare e dettaglio lavorazioni.

    Il parametro `mese` è nel formato 'YYYY-MM' (es. '2026-03').
    """
    return sal.sal_progressivo(cantiere_id, mese)


@mcp.tool()
def notifica_committente(cantiere_id: str, evento: str) -> dict:
    """Costruisce e simula l'invio (PEC) al committente di una notifica
    relativa a un evento di cantiere.

    Eventi ammessi: inizio_lavori, sospensione, ripresa, ultimazione,
    sal_emesso, anomalia, richiesta_variante.
    """
    return notifications.notifica(cantiere_id, evento)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
