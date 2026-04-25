"""Generazione documenti tipici della fase di preparazione cantiere
(condomini privati). Output in markdown, pronto da copiare in Word.
"""

from __future__ import annotations

import uuid
from datetime import date

from . import repo

TIPI_AMMESSI = (
    "dichiarazione_organico_medio",
    "dichiarazione_idoneita_tecnico_professionale",
    "autodichiarazione_patente_crediti",
    "elenco_personale_impiegato",
    "lettera_accompagnamento_pos",
    "accettazione_psc",
    "verbale_presa_visione_psc",
    "pec_riscontro_cse",
    "comunicazione_subappalto",
    "comunicazione_amministratore",
)


def _intestazione_azienda(az: dict) -> str:
    parti = [f"**{az.get('ragione_sociale') or 'INVENI S.R.L.'}**"]
    if az.get("sede_legale"):
        parti.append(f"Sede legale: {az['sede_legale']}")
    if az.get("partita_iva"):
        parti.append(f"P.IVA: {az['partita_iva']}")
    if az.get("titolare"):
        parti.append(f"Legale rappresentante: {az['titolare']}")
    if az.get("pec"):
        parti.append(f"PEC: {az['pec']}")
    return "  \n".join(parti)


def _intestazione_cantiere(c: dict) -> str:
    ind = c.get("indirizzo", {})
    addr = " ".join(filter(None, [ind.get("via"), ind.get("cap"), ind.get("comune"), f"({ind['provincia']})" if ind.get("provincia") else None]))
    return (
        f"**Cantiere**: {c['nome']}\n"
        f"**Ubicazione**: {addr or '___'}\n"
        f"**Committente**: {c['committente'].get('denominazione') or '___'}\n"
    )


def _dichiarazione_organico_medio(c: dict, az: dict, oggi: str) -> str:
    return (
        f"# Dichiarazione organico medio annuo\n"
        f"_Resa ai sensi del DPR 445/2000 e ss.mm.ii._\n\n"
        f"{_intestazione_azienda(az)}\n\n"
        f"{_intestazione_cantiere(c)}\n\n"
        f"Il sottoscritto **{az.get('titolare') or '___'}**, in qualità di "
        f"legale rappresentante di **{az.get('ragione_sociale') or 'INVENI S.R.L.'}**, "
        f"consapevole delle responsabilità penali in caso di dichiarazioni mendaci,\n\n"
        f"## DICHIARA\n\n"
        f"che l'organico medio annuo, suddiviso per qualifica, impiegato dall'impresa "
        f"per i lavori del cantiere in oggetto è il seguente:\n\n"
        f"| Qualifica | n. lavoratori |\n|---|---:|\n"
        f"| Operai specializzati | __ |\n"
        f"| Operai qualificati | __ |\n"
        f"| Operai comuni | __ |\n"
        f"| Impiegati tecnici | __ |\n"
        f"| Apprendisti | __ |\n"
        f"| **Totale** | **__** |\n\n"
        f"L'impresa applica il **CCNL Edilizia** ed è iscritta a **Cassa Edile**.\n\n"
        f"Luogo e data: ___________, {oggi}\n\n"
        f"Firma del legale rappresentante  \n"
        f"_______________________________\n"
    )


def _dichiarazione_idoneita_tecnico_professionale(c: dict, az: dict, oggi: str) -> str:
    return (
        f"# Dichiarazione di idoneità tecnico-professionale\n"
        f"_ai sensi dell'art. 90 c. 9 lett. a) e All. XVII del D.Lgs. 81/2008_\n\n"
        f"{_intestazione_azienda(az)}\n\n"
        f"{_intestazione_cantiere(c)}\n\n"
        f"Il sottoscritto **{az.get('titolare') or '___'}**, legale rappresentante di "
        f"**{az.get('ragione_sociale') or 'INVENI S.R.L.'}**,\n\n"
        f"## DICHIARA\n\n"
        f"sotto la propria responsabilità che l'impresa è in possesso dei requisiti di "
        f"idoneità tecnico-professionale di cui all'All. XVII del D.Lgs. 81/2008 e in "
        f"particolare:\n\n"
        f"- iscrizione alla CCIAA con oggetto sociale coerente con i lavori da eseguire;\n"
        f"- DVR aziendale redatto e aggiornato;\n"
        f"- DURC regolare in corso di validità;\n"
        f"- nomina del RSPP, del Medico Competente, degli addetti emergenze e primo soccorso;\n"
        f"- formazione e informazione dei lavoratori (art. 37 D.Lgs. 81/2008);\n"
        f"- consegna ai lavoratori dei DPI necessari;\n"
        f"- polizza RCT/RCO in corso di validità;\n"
        f"- iscrizione alla Cassa Edile e applicazione del CCNL di settore.\n\n"
        f"Si allega copia della documentazione comprovante quanto sopra dichiarato.\n\n"
        f"Luogo e data: ___________, {oggi}\n\n"
        f"Firma del legale rappresentante  \n"
        f"_______________________________\n"
    )


def _autodichiarazione_patente_crediti(c: dict, az: dict, oggi: str) -> str:
    return (
        f"# Autodichiarazione patente a crediti\n"
        f"_ai sensi dell'art. 27 D.Lgs. 81/2008 (D.L. 19/2024 conv. L. 56/2024)_\n\n"
        f"{_intestazione_azienda(az)}\n\n"
        f"{_intestazione_cantiere(c)}\n\n"
        f"Il sottoscritto **{az.get('titolare') or '___'}**, legale rappresentante di "
        f"**{az.get('ragione_sociale') or 'INVENI S.R.L.'}**,\n\n"
        f"## DICHIARA\n\n"
        f"di essere in possesso della **patente a crediti** rilasciata ai sensi "
        f"dell'art. 27 D.Lgs. 81/2008, e segnatamente:\n\n"
        f"- **Codice impresa**: ____________________\n"
        f"- **Data di rilascio**: ____________________\n"
        f"- **Punteggio attuale**: ____ crediti (≥ 15 richiesti per operare in cantieri temporanei o mobili).\n\n"
        f"Si allega ricevuta del portale INL.\n\n"
        f"Luogo e data: ___________, {oggi}\n\n"
        f"Firma del legale rappresentante  \n"
        f"_______________________________\n"
    )


def _elenco_personale_impiegato(c: dict, az: dict, oggi: str) -> str:
    return (
        f"# Elenco del personale impiegato\n\n"
        f"{_intestazione_azienda(az)}\n\n"
        f"{_intestazione_cantiere(c)}\n\n"
        f"Si trasmette l'elenco del personale dipendente impiegato presso il cantiere "
        f"in oggetto, completo di qualifica, mansione e estremi formativi:\n\n"
        f"| Cognome e Nome | Mansione | Qualifica | N° matr. INAIL | Form. base art. 37 | Form. specifica | Visita medica |\n"
        f"|---|---|---|---|---|---|---|\n"
        f"| | | | | | | |\n"
        f"| | | | | | | |\n\n"
        f"Eventuali aggiornamenti saranno tempestivamente comunicati al CSE.\n\n"
        f"Luogo e data: ___________, {oggi}\n\n"
        f"Firma del legale rappresentante  \n"
        f"_______________________________\n"
    )


def _lettera_accompagnamento_pos(c: dict, az: dict, oggi: str) -> str:
    cse = c.get("cse", {})
    return (
        f"# Trasmissione POS al Coordinatore per la Sicurezza in fase di Esecuzione\n\n"
        f"Spett.le {cse.get('nome') or 'Sig. CSE'},\n"
        f"{('e-mail/PEC: ' + cse.get('email')) if cse.get('email') else ''}\n\n"
        f"{_intestazione_cantiere(c)}\n\n"
        f"Con la presente, in data {oggi}, **{az.get('ragione_sociale') or 'INVENI S.R.L.'}** "
        f"trasmette il **Piano Operativo di Sicurezza (POS)** redatto ai sensi dell'art. 89 "
        f"e All. XV del D.Lgs. 81/2008, riferito alle proprie lavorazioni nel cantiere in oggetto.\n\n"
        f"Il POS è coordinato con il PSC ricevuto e tiene conto delle prescrizioni "
        f"contenute nei documenti di sicurezza già consegnati.\n\n"
        f"Si resta a disposizione per qualsiasi integrazione o chiarimento.\n\n"
        f"Cordiali saluti,\n\n"
        f"Il legale rappresentante  \n"
        f"_{az.get('titolare') or '___'}_\n"
    )


def _accettazione_psc(c: dict, az: dict, oggi: str) -> str:
    return (
        f"# Verbale di accettazione del PSC\n\n"
        f"{_intestazione_azienda(az)}\n\n"
        f"{_intestazione_cantiere(c)}\n\n"
        f"Il sottoscritto **{az.get('titolare') or '___'}**, in qualità di legale "
        f"rappresentante di **{az.get('ragione_sociale') or 'INVENI S.R.L.'}**, "
        f"impresa appaltatrice/esecutrice delle lavorazioni nel cantiere in oggetto,\n\n"
        f"## DICHIARA\n\n"
        f"di aver ricevuto, esaminato e compreso il **Piano di Sicurezza e Coordinamento (PSC)** "
        f"redatto dal Coordinatore per la Sicurezza in fase di Progettazione, e\n\n"
        f"## ACCETTA\n\n"
        f"integralmente i contenuti del PSC, impegnandosi a darne attuazione e a renderne "
        f"edotti i lavoratori e gli eventuali subappaltatori.\n\n"
        f"Eventuali proposte di modifica saranno presentate al CSE prima dell'inizio "
        f"delle lavorazioni interessate, ai sensi dell'art. 100 c. 5 D.Lgs. 81/2008.\n\n"
        f"Luogo e data: ___________, {oggi}\n\n"
        f"Firma del legale rappresentante  \n"
        f"_______________________________\n"
    )


def _verbale_presa_visione_psc(c: dict, az: dict, oggi: str) -> str:
    return (
        f"# Verbale di presa visione del PSC da parte dei lavoratori\n\n"
        f"{_intestazione_azienda(az)}\n\n"
        f"{_intestazione_cantiere(c)}\n\n"
        f"I sottoscritti lavoratori dichiarano di aver preso visione del **Piano di "
        f"Sicurezza e Coordinamento (PSC)** del cantiere in oggetto, illustrato dal "
        f"datore di lavoro / preposto _{az.get('preposto') or '___'}_, e di averne "
        f"compreso i contenuti in materia di rischi specifici e misure di prevenzione.\n\n"
        f"| Cognome e Nome | Mansione | Firma | Data |\n|---|---|---|---|\n"
        f"| | | | {oggi} |\n"
        f"| | | | {oggi} |\n"
        f"| | | | {oggi} |\n\n"
        f"Il preposto: _{az.get('preposto') or '___'}_  \n"
        f"Firma: _______________________________\n"
    )


def _pec_riscontro_cse(c: dict, az: dict, oggi: str) -> str:
    cse = c.get("cse", {})
    return (
        f"# PEC al Coordinatore per la Sicurezza in fase di Esecuzione\n\n"
        f"**A**: {cse.get('email') or '<pec_cse@...>'}\n"
        f"**Oggetto**: Riscontro CSE - {c['nome']} - trasmissione documentazione\n\n"
        f"Spett.le {cse.get('nome') or 'CSE'},\n\n"
        f"in riscontro alla Sua richiesta del __/__/____, **{az.get('ragione_sociale') or 'INVENI S.R.L.'}** "
        f"trasmette in allegato la seguente documentazione relativa al cantiere {c['nome']}:\n\n"
        f"- POS aggiornato\n"
        f"- Dichiarazione di idoneità tecnico-professionale (All. XVII D.Lgs. 81/2008)\n"
        f"- Autodichiarazione patente a crediti\n"
        f"- DURC in corso di validità\n"
        f"- Polizza RCT/RCO\n"
        f"- Elenco del personale impiegato con relativi attestati\n"
        f"- Elenco attrezzature e mezzi d'opera\n\n"
        f"Si resta a disposizione per ogni integrazione.\n\n"
        f"Distinti saluti,\n\n"
        f"_{az.get('titolare') or '___'}_  \n"
        f"Legale rappresentante {az.get('ragione_sociale') or 'INVENI S.R.L.'}\n"
        f"\n_PEC inviata in data {oggi}_\n"
    )


def _comunicazione_subappalto(c: dict, az: dict, oggi: str) -> str:
    cse = c.get("cse", {})
    subs = c.get("subappaltatori", [])
    elenco = "\n".join(f"- **{s.get('ragione_sociale')}** ({s.get('categoria') or 'lavorazione da specificare'})" for s in subs) or "- ___"
    return (
        f"# Comunicazione di subappalto\n"
        f"_ai sensi dell'art. 105 D.Lgs. 50/2016 e art. 1656 c.c._\n\n"
        f"Spett.le Committente {c['committente'].get('denominazione') or '___'}\n"
        f"e p.c. CSE {cse.get('nome') or '___'}\n\n"
        f"{_intestazione_cantiere(c)}\n\n"
        f"Con la presente, **{az.get('ragione_sociale') or 'INVENI S.R.L.'}** comunica "
        f"che intende affidare in subappalto le seguenti lavorazioni alle imprese sottoindicate:\n\n"
        f"{elenco}\n\n"
        f"Per ciascun subappaltatore si trasmette la documentazione prevista dall'art. 105 "
        f"D.Lgs. 50/2016 (visura, DURC, INAIL, polizze, POS, dichiarazione di idoneità "
        f"tecnico-professionale, attestati formazione del personale).\n\n"
        f"Si resta in attesa di formale autorizzazione.\n\n"
        f"Luogo e data: ___________, {oggi}\n\n"
        f"_{az.get('titolare') or '___'}_  \n"
        f"Legale rappresentante\n"
    )


def _comunicazione_amministratore(c: dict, az: dict, oggi: str) -> str:
    com = c.get("committente", {})
    return (
        f"# Comunicazione all'Amministratore di Condominio\n\n"
        f"**A**: {com.get('amministratore_studio') or 'Studio amministrazione'} - "
        f"{com.get('amministratore_persona') or 'Sig./Sig.ra ___'}\n"
        f"**E-mail**: {com.get('email') or '___'}\n"
        f"**PEC**: {com.get('pec') or '___'}\n\n"
        f"Oggetto: {c['nome']} - aggiornamento sull'avvio dei lavori\n\n"
        f"Egregio Amministratore,\n\n"
        f"con la presente, in data {oggi}, **{az.get('ragione_sociale') or 'INVENI S.R.L.'}** "
        f"trasmette aggiornamento in merito alla preparazione del cantiere in oggetto.\n\n"
        f"La documentazione di sicurezza e gli adempimenti propedeutici sono in corso "
        f"di completamento. Sarà nostra cura comunicare tempestivamente la data di "
        f"effettivo avvio dei lavori, previa firma del verbale di consegna.\n\n"
        f"Restiamo a disposizione per ogni chiarimento.\n\n"
        f"Cordiali saluti,\n\n"
        f"_{az.get('titolare') or '___'}_  \n"
        f"Legale rappresentante {az.get('ragione_sociale') or 'INVENI S.R.L.'}\n"
    )


_GENERATORI = {
    "dichiarazione_organico_medio": _dichiarazione_organico_medio,
    "dichiarazione_idoneita_tecnico_professionale": _dichiarazione_idoneita_tecnico_professionale,
    "autodichiarazione_patente_crediti": _autodichiarazione_patente_crediti,
    "elenco_personale_impiegato": _elenco_personale_impiegato,
    "lettera_accompagnamento_pos": _lettera_accompagnamento_pos,
    "accettazione_psc": _accettazione_psc,
    "verbale_presa_visione_psc": _verbale_presa_visione_psc,
    "pec_riscontro_cse": _pec_riscontro_cse,
    "comunicazione_subappalto": _comunicazione_subappalto,
    "comunicazione_amministratore": _comunicazione_amministratore,
}


def genera(tipo: str, cantiere_id: str) -> dict:
    if tipo not in _GENERATORI:
        raise ValueError(
            f"Tipo documento non supportato: '{tipo}'. "
            f"Tipi ammessi: {', '.join(TIPI_AMMESSI)}."
        )

    cantiere = repo.get_cantiere(cantiere_id)
    az = repo.azienda()
    oggi = date.today().isoformat()
    contenuto = _GENERATORI[tipo](cantiere, az, oggi)

    return {
        "documento_id": f"DOC-{uuid.uuid4().hex[:8].upper()}",
        "tipo": tipo,
        "cantiere_id": cantiere_id,
        "data_emissione": oggi,
        "contenuto_markdown": contenuto,
    }
