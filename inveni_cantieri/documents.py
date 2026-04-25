"""Generazione documenti tipici di cantiere in formato markdown."""

from __future__ import annotations

import uuid
from datetime import date

from . import repo, sal as sal_module

TIPI_AMMESSI = (
    "verbale_inizio_lavori",
    "verbale_sospensione",
    "verbale_ripresa",
    "verbale_ultimazione",
    "sal",
    "certificato_pagamento",
    "comunicazione_committente",
    "ordine_di_servizio",
)


def _intestazione(cantiere: dict) -> str:
    ind = cantiere["indirizzo"]
    return (
        f"# {cantiere['nome']}\n\n"
        f"- **Cantiere ID**: {cantiere['id']}\n"
        f"- **CIG**: {cantiere['cig']} - **CUP**: {cantiere['cup']}\n"
        f"- **Ubicazione**: {ind['via']}, {ind['cap']} {ind['comune']} ({ind['provincia']})\n"
        f"- **Committente**: {cantiere['committente']['denominazione']}\n"
        f"- **RUP**: {cantiere['committente']['rup']}\n"
        f"- **Impresa**: {cantiere['impresa_appaltatrice']['ragione_sociale']}\n"
        f"- **Direttore lavori**: {cantiere['direttore_lavori']}\n"
        f"- **CSE**: {cantiere['coordinatore_sicurezza']}\n"
    )


def _verbale_inizio(cantiere: dict, oggi: str) -> str:
    return (
        _intestazione(cantiere)
        + f"\n## Verbale di consegna e inizio lavori\n\n"
        f"In data {oggi}, presso il cantiere in oggetto, il Direttore dei Lavori "
        f"{cantiere['direttore_lavori']} ha proceduto alla consegna dei lavori "
        f"all'Impresa {cantiere['impresa_appaltatrice']['ragione_sociale']}.\n\n"
        f"L'Impresa dichiara di aver preso visione dei luoghi e di accettare "
        f"la consegna senza riserve. I lavori avranno inizio in data {cantiere['data_inizio']} "
        f"e dovranno concludersi entro il {cantiere['data_fine_prevista']}.\n\n"
        f"Importo contrattuale: € {cantiere['importo_contrattuale']:,.2f}.\n"
    )


def _verbale_sospensione(cantiere: dict, oggi: str) -> str:
    return (
        _intestazione(cantiere)
        + f"\n## Verbale di sospensione lavori\n\n"
        f"In data {oggi}, il Direttore dei Lavori dispone la sospensione "
        f"delle lavorazioni per cause da specificare nel corpo del verbale "
        f"(es. avverse condizioni meteo, cause di forza maggiore, "
        f"ritrovamenti archeologici).\n\n"
        f"La sospensione decorre dal {oggi}. La ripresa sarà comunicata "
        f"con apposito verbale.\n"
    )


def _verbale_ripresa(cantiere: dict, oggi: str) -> str:
    return (
        _intestazione(cantiere)
        + f"\n## Verbale di ripresa lavori\n\n"
        f"In data {oggi}, essendo cessate le cause che avevano determinato "
        f"la sospensione, il Direttore dei Lavori dispone la ripresa "
        f"delle lavorazioni a far data da oggi.\n\n"
        f"Il termine contrattuale è prorogato in misura corrispondente "
        f"al periodo di sospensione.\n"
    )


def _verbale_ultimazione(cantiere: dict, oggi: str) -> str:
    return (
        _intestazione(cantiere)
        + f"\n## Verbale di ultimazione lavori\n\n"
        f"In data {oggi}, l'Impresa appaltatrice comunica al Direttore "
        f"dei Lavori l'avvenuta ultimazione delle opere oggetto del contratto.\n\n"
        f"Il Direttore dei Lavori, effettuata visita in cantiere, "
        f"prende atto dell'ultimazione e dispone le verifiche propedeutiche "
        f"al collaudo / certificato di regolare esecuzione.\n"
    )


def _sal(cantiere: dict, oggi: str) -> str:
    sal_list = sorted(cantiere.get("sal", []), key=lambda s: s["mese"])
    if not sal_list:
        return _intestazione(cantiere) + "\n## SAL\n\n_Nessun SAL emesso._\n"
    ultimo = sal_list[-1]
    dati = sal_module.sal_progressivo(cantiere["id"], ultimo["mese"])
    righe = "\n".join(
        f"| {l['voce']} | {l['quantita']} | € {l['importo']:,.2f} |"
        for l in dati["lavorazioni"]
    )
    return (
        _intestazione(cantiere)
        + f"\n## Stato Avanzamento Lavori n. {dati['numero_sal']} - mese {dati['mese']}\n\n"
        f"Emesso il {oggi}.\n\n"
        f"- Importo del periodo: € {dati['importo_periodo']:,.2f}\n"
        f"- Importo progressivo: € {dati['importo_progressivo']:,.2f} "
        f"({dati['percentuale_completamento']}% del contratto)\n"
        f"- Ritenuta di garanzia (0,5%): € {dati['ritenuta_garanzia']:,.2f}\n"
        f"- Importo netto da liquidare: € {dati['importo_netto_da_liquidare']:,.2f}\n\n"
        f"### Lavorazioni del periodo\n\n"
        f"| Voce | Quantità | Importo |\n|---|---:|---:|\n{righe}\n"
    )


def _certificato_pagamento(cantiere: dict, oggi: str) -> str:
    sal_list = sorted(cantiere.get("sal", []), key=lambda s: s["mese"])
    if not sal_list:
        return (
            _intestazione(cantiere)
            + "\n## Certificato di pagamento\n\n_Nessun SAL disponibile._\n"
        )
    dati = sal_module.sal_progressivo(cantiere["id"], sal_list[-1]["mese"])
    return (
        _intestazione(cantiere)
        + f"\n## Certificato di pagamento n. {dati['numero_sal']}\n\n"
        f"Emesso il {oggi} a fronte del SAL n. {dati['numero_sal']} "
        f"(mese {dati['mese']}).\n\n"
        f"Si certifica che all'Impresa {cantiere['impresa_appaltatrice']['ragione_sociale']} "
        f"compete il pagamento di **€ {dati['importo_netto_da_liquidare']:,.2f}** "
        f"(al netto della ritenuta di garanzia dello 0,5%).\n\n"
        f"Il Direttore dei Lavori: {cantiere['direttore_lavori']}.\n"
    )


def _comunicazione_committente(cantiere: dict, oggi: str) -> str:
    return (
        _intestazione(cantiere)
        + f"\n## Comunicazione al committente\n\n"
        f"Spett.le {cantiere['committente']['denominazione']},\n"
        f"alla c.a. del RUP {cantiere['committente']['rup']}.\n\n"
        f"Con la presente, in data {oggi}, si trasmette aggiornamento "
        f"sull'andamento dei lavori del cantiere in oggetto. "
        f"Per ogni dettaglio o richiesta di chiarimento si resta "
        f"a disposizione ai recapiti contrattuali.\n\n"
        f"Cordiali saluti,\n{cantiere['direttore_lavori']}\n"
    )


def _ordine_di_servizio(cantiere: dict, oggi: str) -> str:
    return (
        _intestazione(cantiere)
        + f"\n## Ordine di servizio\n\n"
        f"In data {oggi} il Direttore dei Lavori {cantiere['direttore_lavori']} "
        f"impartisce all'Impresa {cantiere['impresa_appaltatrice']['ragione_sociale']} "
        f"il presente ordine di servizio relativamente alle lavorazioni "
        f"oggetto del contratto.\n\n"
        f"L'Impresa è tenuta ad eseguire quanto disposto, fatta salva la facoltà "
        f"di iscrivere riserva nei termini e con le modalità di legge.\n"
    )


_GENERATORI = {
    "verbale_inizio_lavori": _verbale_inizio,
    "verbale_sospensione": _verbale_sospensione,
    "verbale_ripresa": _verbale_ripresa,
    "verbale_ultimazione": _verbale_ultimazione,
    "sal": _sal,
    "certificato_pagamento": _certificato_pagamento,
    "comunicazione_committente": _comunicazione_committente,
    "ordine_di_servizio": _ordine_di_servizio,
}


def genera(tipo: str, cantiere_id: str) -> dict:
    if tipo not in _GENERATORI:
        raise ValueError(
            f"Tipo documento non supportato: '{tipo}'. "
            f"Tipi ammessi: {', '.join(TIPI_AMMESSI)}."
        )

    cantiere = repo.get_cantiere(cantiere_id)
    oggi = date.today().isoformat()
    contenuto = _GENERATORI[tipo](cantiere, oggi)

    return {
        "documento_id": f"DOC-{uuid.uuid4().hex[:8].upper()}",
        "tipo": tipo,
        "cantiere_id": cantiere_id,
        "data_emissione": oggi,
        "contenuto_markdown": contenuto,
    }
