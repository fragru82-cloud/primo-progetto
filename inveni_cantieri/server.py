"""MCP server "INVENI Cantieri" - fase di preparazione cantiere.

Espone 4 tool per gestire la preparazione documentale di un cantiere
(condomini privati):

- cantiere_anagrafica: dati del cantiere e committente
- checklist_preparazione: confronta i file presenti nella cartella MEGA con
  la master checklist (DURC, POS, dichiarazioni, ecc.)
- stato_preparazione: sintesi % completamento + bloccanti
- genera_documento: template di dichiarazioni, autocertificazioni, lettere

Trasporto: stdio. Avviabile via `inveni-cantieri-mcp` (entry point del package)
o `python -m inveni_cantieri.server`.

Variabili d'ambiente:

- INVENI_CANTIERI_DATA: percorso del file JSON (anagrafica + azienda)
- INVENI_CANTIERI_BASE: percorso della cartella `cantieri e contratti`
"""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from . import checklist, documents, repo, stato

mcp = FastMCP("inveni-cantieri")


@mcp.tool()
def cantiere_anagrafica(cantiere_id: str) -> dict:
    """Restituisce l'anagrafica del cantiere: indirizzo, committente
    (condominio + amministratore), CSE, importo, date previste, stato
    (in_preparazione/attivo/chiuso) ed eventuali subappaltatori.

    ID disponibili: DONBOSCO, PETTIROSSO, CASALETTO.
    """
    c = repo.get_cantiere(cantiere_id)
    return {
        "id": c["id"],
        "nome": c["nome"],
        "tipo": c.get("tipo"),
        "stato": c.get("stato"),
        "indirizzo": c.get("indirizzo", {}),
        "committente": c.get("committente", {}),
        "cse": c.get("cse", {}),
        "importo_contrattuale": c.get("importo_contrattuale"),
        "data_inizio_prevista": c.get("data_inizio_prevista"),
        "data_fine_prevista": c.get("data_fine_prevista"),
        "subappaltatori": c.get("subappaltatori", []),
        "cartella": str(repo.cantiere_folder(c)),
        "note": c.get("note", ""),
    }


@mcp.tool()
def checklist_preparazione(cantiere_id: str) -> dict:
    """Verifica i file presenti nella cartella del cantiere su MEGA contro la
    master checklist (Documenti aziendali, Sicurezza, Dichiarazioni,
    Contrattualistica, Corrispondenza CSE, Subappalti).

    Per ogni voce attesa indica `presente: true/false`, l'eventuale file
    riconosciuto, e se è obbligatorio o opzionale. Utile per capire cosa
    manca prima di poter avviare il cantiere.
    """
    return checklist.checklist_preparazione(cantiere_id)


@mcp.tool()
def stato_preparazione(cantiere_id: str) -> dict:
    """Riepilogo sintetico dello stato di preparazione del cantiere:
    percentuale di completamento, lista documenti obbligatori mancanti
    (bloccanti), opzionali mancanti, e flag `pronto_a_partire`.
    """
    return stato.stato_preparazione(cantiere_id)


@mcp.tool()
def genera_documento(tipo: str, cantiere_id: str) -> dict:
    """Genera il template di un documento della fase di preparazione.

    Tipi ammessi: dichiarazione_organico_medio,
    dichiarazione_idoneita_tecnico_professionale,
    autodichiarazione_patente_crediti, elenco_personale_impiegato,
    lettera_accompagnamento_pos, accettazione_psc,
    verbale_presa_visione_psc, pec_riscontro_cse,
    comunicazione_subappalto, comunicazione_amministratore.

    Output in markdown, pronto da copiare in Word.
    """
    return documents.genera(tipo, cantiere_id)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
