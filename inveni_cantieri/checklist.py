"""Master checklist preparazione cantiere e matcher dei file presenti.

Confronta l'elenco dei documenti attesi con i file effettivamente presenti
nella cartella del cantiere su MEGA.

Strategia di matching: per ogni documento atteso, una lista di **keyword**.
Un file presente nella cartella matcha se *tutte* le keyword (case-insensitive,
con gestione di spazi/underscore/trattini) compaiono nel suo nome.

Ogni voce della checklist indica anche:
- `obbligatorieta`: 'obbligatorio' (bloccante) o 'opzionale' (non bloccante).
- `ambito`: 'azienda' (doc valido per tutti i cantieri INVENI) o 'cantiere'
  (specifico del singolo cantiere).
"""

from __future__ import annotations

import re
import unicodedata
from pathlib import Path

from . import repo

# (display_name, keywords, obbligatorieta, ambito)
Voce = tuple[str, list[str], str, str]

CHECKLIST: dict[str, list[Voce]] = {
    "01 - Documenti Aziendali": [
        ("Visura Camerale INVENI", ["visura"], "obbligatorio", "azienda"),
        ("Certificato INAIL", ["inail"], "obbligatorio", "azienda"),
        ("DOMA INVENI", ["doma"], "obbligatorio", "azienda"),
        ("Polizza RCT/RCO INVENI", ["polizza", "rct"], "obbligatorio", "azienda"),
        ("Visite Mediche INVENI", ["visite", "mediche"], "obbligatorio", "azienda"),
        ("Ricevuta Patente Crediti", ["patente", "crediti"], "obbligatorio", "azienda"),
        ("Documento Identità Titolare", ["documento", "identita"], "obbligatorio", "azienda"),
        ("DURC INVENI", ["durc"], "obbligatorio", "azienda"),
    ],
    "02 - Sicurezza Cantiere": [
        ("DVR INVENI", ["dvr"], "obbligatorio", "azienda"),
        ("Verbale RSPP", ["verbale", "rspp"], "obbligatorio", "azienda"),
        ("Attestato RSPP", ["attestato", "rspp"], "obbligatorio", "azienda"),
        ("Nomina Medico Competente", ["nomina", "medico"], "obbligatorio", "azienda"),
        ("Verbale RLS", ["verbale", "rls"], "obbligatorio", "azienda"),
        ("Verbale Preposto", ["verbale", "preposto"], "obbligatorio", "azienda"),
        ("Verbale Emergenze", ["verbale", "emergenze"], "obbligatorio", "azienda"),
        ("POS specifico cantiere", ["pos"], "obbligatorio", "cantiere"),
        ("Elenco Personale Impiegato", ["elenco", "personale"], "obbligatorio", "cantiere"),
        ("Elenco Attrezzature/Mezzi d'Opera", ["elenco", "attrezzature"], "obbligatorio", "cantiere"),
        ("Verbale Presa Visione PSC", ["verbale", "presa", "visione", "psc"], "obbligatorio", "cantiere"),
    ],
    "04 - Dichiarazioni e Autocertificazioni": [
        ("Dichiarazione Idoneità Tecnico-Professionale", ["idoneita", "tecnico"], "obbligatorio", "cantiere"),
        ("Autodichiarazione Patente Crediti", ["autodichiarazione", "patente"], "obbligatorio", "cantiere"),
        ("Dichiarazione Organico Medio Annuo", ["organico", "medio"], "obbligatorio", "cantiere"),
    ],
    "05 - Deleghe e Contrattualistica": [
        ("Preventivo firmato", ["preventivo"], "obbligatorio", "cantiere"),
        ("Capitolato firmato", ["capitolato"], "opzionale", "cantiere"),
        ("Accettazione PSC", ["accettazione", "psc"], "obbligatorio", "cantiere"),
        ("Delega Fattura/Pagamento", ["delega"], "opzionale", "cantiere"),
    ],
    "06 - Corrispondenza CSE": [
        ("PEC riscontro CSE", ["pec", "cse"], "opzionale", "cantiere"),
    ],
    "07 - Subappalti": [
        # Voci dinamiche per subappaltatore (vedi _voci_subappalto). Qui può
        # comunque restare un check generico se sono attesi documenti generali.
    ],
}


def _normalize(s: str) -> str:
    """Normalizza per match case-insensitive: rimuove accenti, abbassa, sostituisce
    underscore/trattini/punti con spazi, comprime spazi multipli."""
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = s.lower()
    s = re.sub(r"[_\-.,/\\]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def _index_files(folder: Path, max_depth: int = 3) -> list[tuple[Path, str]]:
    """Indicizza i file dentro `folder` (fino a profondità max_depth) come
    coppie (path_assoluto, nome_normalizzato)."""
    if not folder.exists():
        return []
    base_depth = len(folder.parts)
    out: list[tuple[Path, str]] = []
    for p in folder.rglob("*"):
        if not p.is_file():
            continue
        depth = len(p.parts) - base_depth
        if depth > max_depth:
            continue
        out.append((p, _normalize(p.name)))
    return out


def _match(file_index: list[tuple[Path, str]], keywords: list[str]) -> list[Path]:
    """Ritorna i file il cui nome normalizzato contiene tutte le keyword."""
    kws = [_normalize(k) for k in keywords]
    return [p for p, name in file_index if all(k in name for k in kws)]


def _voci_subappalto(subappaltatori: list[dict]) -> list[Voce]:
    """Genera dinamicamente le voci attese per ciascun subappaltatore."""
    voci: list[Voce] = []
    for sub in subappaltatori:
        rs = sub.get("ragione_sociale", "Subappaltatore")
        # match per nome subappaltatore + tipo doc
        token = rs.split()[0].lower()  # primo token come "marker" del fornitore
        voci.append((f"{rs} - Visura", [token, "visura"], "obbligatorio", "subappalto"))
        voci.append((f"{rs} - DURC", [token, "durc"], "obbligatorio", "subappalto"))
        voci.append((f"{rs} - INAIL", [token, "inail"], "obbligatorio", "subappalto"))
        voci.append((f"{rs} - Polizza", [token, "polizza"], "obbligatorio", "subappalto"))
        voci.append((f"{rs} - POS", [token, "pos"], "obbligatorio", "subappalto"))
        voci.append((f"{rs} - Idoneità Tecnico-Professionale", [token, "idoneita"], "obbligatorio", "subappalto"))
    return voci


def checklist_preparazione(cantiere_id: str) -> dict:
    """Per ogni voce della master checklist verifica la presenza di file
    corrispondenti nella cartella del cantiere. Ritorna report dettagliato.
    """
    cantiere = repo.get_cantiere(cantiere_id)
    folder = repo.cantiere_folder(cantiere)

    if not folder.exists():
        raise FileNotFoundError(
            f"Cartella del cantiere non trovata: {folder}. "
            f"Verifica la variabile d'ambiente INVENI_CANTIERI_BASE e "
            f"il campo 'cartella' del cantiere '{cantiere_id}'."
        )

    file_index = _index_files(folder)
    cantiere_root = folder

    categorie = []
    totale_attesi = 0
    totale_presenti = 0
    totale_obbligatori_mancanti = 0

    voci_per_categoria: dict[str, list[Voce]] = dict(CHECKLIST)
    voci_per_categoria["07 - Subappalti"] = (
        list(voci_per_categoria.get("07 - Subappalti", []))
        + _voci_subappalto(cantiere.get("subappaltatori", []))
    )

    for cat_name, voci in voci_per_categoria.items():
        cat = {"categoria": cat_name, "voci": []}
        for display, keywords, obbligatorieta, ambito in voci:
            matches = _match(file_index, keywords)
            present = bool(matches)
            cat["voci"].append({
                "documento": display,
                "obbligatorieta": obbligatorieta,
                "ambito": ambito,
                "presente": present,
                "file": [str(p.relative_to(cantiere_root)) for p in matches[:3]],
                "altri_match": max(0, len(matches) - 3),
            })
            totale_attesi += 1
            if present:
                totale_presenti += 1
            elif obbligatorieta == "obbligatorio":
                totale_obbligatori_mancanti += 1
        categorie.append(cat)

    return {
        "cantiere_id": cantiere_id,
        "cantiere_nome": cantiere["nome"],
        "cartella": str(folder),
        "totale_attesi": totale_attesi,
        "totale_presenti": totale_presenti,
        "totale_obbligatori_mancanti": totale_obbligatori_mancanti,
        "percentuale_completamento": round(totale_presenti / totale_attesi * 100, 1) if totale_attesi else 0,
        "categorie": categorie,
    }
