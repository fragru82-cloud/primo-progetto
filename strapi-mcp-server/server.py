"""
MCP Server per Strapi CMS
Permette a Claude di gestire contenuti Strapi via chat.
"""

import os
import json
import httpx
from mcp.server.fastmcp import FastMCP

# --- Configurazione ---
STRAPI_URL = os.environ.get("STRAPI_URL", "http://localhost:1337")
STRAPI_TOKEN = os.environ.get("STRAPI_TOKEN", "")

mcp = FastMCP(
    "Strapi CMS",
    description="Gestisci contenuti Strapi: CRUD, media, ricerca",
)


def _headers() -> dict:
    return {
        "Authorization": f"Bearer {STRAPI_TOKEN}",
        "Content-Type": "application/json",
    }


def _api(path: str) -> str:
    return f"{STRAPI_URL}/api/{path.lstrip('/')}"


# ──────────────────────────────────────────────
#  CONTENT TYPES
# ──────────────────────────────────────────────

@mcp.tool()
async def list_content_types() -> str:
    """Elenca tutti i content type disponibili in Strapi."""
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{STRAPI_URL}/api/content-type-builder/content-types",
            headers=_headers(),
        )
        resp.raise_for_status()
        data = resp.json().get("data", [])

    # Filtra solo i tipi API (non plugin/admin)
    api_types = [
        {"uid": ct["uid"], "name": ct.get("schema", {}).get("displayName", ct["uid"])}
        for ct in data
        if ct["uid"].startswith("api::")
    ]
    return json.dumps(api_types, indent=2, ensure_ascii=False)


@mcp.tool()
async def get_content_type_schema(content_type_uid: str) -> str:
    """
    Mostra lo schema (campi) di un content type.
    content_type_uid: es. "api::article.article"
    """
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{STRAPI_URL}/api/content-type-builder/content-types/{content_type_uid}",
            headers=_headers(),
        )
        resp.raise_for_status()
    schema = resp.json().get("data", {}).get("schema", {})
    return json.dumps(schema, indent=2, ensure_ascii=False)


# ──────────────────────────────────────────────
#  CRUD — ENTRIES
# ──────────────────────────────────────────────

@mcp.tool()
async def list_entries(
    collection: str,
    page: int = 1,
    page_size: int = 25,
    sort: str = "createdAt:desc",
    filters: str = "",
    populate: str = "*",
) -> str:
    """
    Elenca le entry di una collection.
    collection: nome plurale, es. "articles"
    filters: JSON string per filtrare, es. '{"title":{"$contains":"hello"}}'
    populate: campi da popolare, default "*" (tutti)
    """
    params: dict = {
        "pagination[page]": page,
        "pagination[pageSize]": page_size,
        "sort": sort,
        "populate": populate,
    }
    if filters:
        filter_dict = json.loads(filters)
        _flatten_filters(filter_dict, "filters", params)

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            _api(collection), headers=_headers(), params=params
        )
        resp.raise_for_status()
    return json.dumps(resp.json(), indent=2, ensure_ascii=False)


@mcp.tool()
async def get_entry(collection: str, entry_id: int, populate: str = "*") -> str:
    """
    Ottieni una singola entry per ID.
    collection: nome plurale, es. "articles"
    entry_id: ID numerico dell'entry
    """
    params = {"populate": populate}
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            _api(f"{collection}/{entry_id}"),
            headers=_headers(),
            params=params,
        )
        resp.raise_for_status()
    return json.dumps(resp.json(), indent=2, ensure_ascii=False)


@mcp.tool()
async def create_entry(collection: str, data: str) -> str:
    """
    Crea una nuova entry.
    collection: nome plurale, es. "articles"
    data: JSON string con i campi, es. '{"title":"Nuovo articolo","content":"Testo..."}'
    """
    payload = {"data": json.loads(data)}
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            _api(collection), headers=_headers(), json=payload
        )
        resp.raise_for_status()
    return json.dumps(resp.json(), indent=2, ensure_ascii=False)


@mcp.tool()
async def update_entry(collection: str, entry_id: int, data: str) -> str:
    """
    Aggiorna una entry esistente.
    collection: nome plurale, es. "articles"
    entry_id: ID numerico
    data: JSON string con i campi da aggiornare
    """
    payload = {"data": json.loads(data)}
    async with httpx.AsyncClient() as client:
        resp = await client.put(
            _api(f"{collection}/{entry_id}"),
            headers=_headers(),
            json=payload,
        )
        resp.raise_for_status()
    return json.dumps(resp.json(), indent=2, ensure_ascii=False)


@mcp.tool()
async def delete_entry(collection: str, entry_id: int) -> str:
    """
    Elimina una entry.
    collection: nome plurale, es. "articles"
    entry_id: ID numerico
    """
    async with httpx.AsyncClient() as client:
        resp = await client.delete(
            _api(f"{collection}/{entry_id}"), headers=_headers()
        )
        resp.raise_for_status()
    return json.dumps(resp.json(), indent=2, ensure_ascii=False)


# ──────────────────────────────────────────────
#  MEDIA / UPLOAD
# ──────────────────────────────────────────────

@mcp.tool()
async def list_media(page: int = 1, page_size: int = 25) -> str:
    """Elenca i file caricati nella media library."""
    params = {
        "pagination[page]": page,
        "pagination[pageSize]": page_size,
        "sort": "createdAt:desc",
    }
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            _api("upload/files"), headers=_headers(), params=params
        )
        resp.raise_for_status()
    return json.dumps(resp.json(), indent=2, ensure_ascii=False)


@mcp.tool()
async def upload_media(file_path: str, name: str = "") -> str:
    """
    Carica un file nella media library di Strapi.
    file_path: percorso locale del file
    name: nome opzionale per il file
    """
    headers = {"Authorization": f"Bearer {STRAPI_TOKEN}"}
    with open(file_path, "rb") as f:
        files = {"files": (name or os.path.basename(file_path), f)}
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                _api("upload"), headers=headers, files=files
            )
            resp.raise_for_status()
    return json.dumps(resp.json(), indent=2, ensure_ascii=False)


@mcp.tool()
async def delete_media(file_id: int) -> str:
    """Elimina un file dalla media library."""
    async with httpx.AsyncClient() as client:
        resp = await client.delete(
            _api(f"upload/files/{file_id}"), headers=_headers()
        )
        resp.raise_for_status()
    return json.dumps(resp.json(), indent=2, ensure_ascii=False)


# ──────────────────────────────────────────────
#  SEARCH
# ──────────────────────────────────────────────

@mcp.tool()
async def search_entries(
    collection: str,
    query: str,
    fields: str = "title,name,description",
    page_size: int = 10,
) -> str:
    """
    Cerca testo nelle entry di una collection.
    collection: nome plurale
    query: testo da cercare
    fields: campi in cui cercare (separati da virgola)
    """
    field_list = [f.strip() for f in fields.split(",")]
    or_filters = []
    for field in field_list:
        or_filters.append({field: {"$containsi": query}})

    params: dict = {
        "pagination[pageSize]": page_size,
        "populate": "*",
    }
    for i, f in enumerate(or_filters):
        for key, val in f.items():
            for op, term in val.items():
                params[f"filters[$or][{i}][{key}][{op}]"] = term

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            _api(collection), headers=_headers(), params=params
        )
        resp.raise_for_status()
    return json.dumps(resp.json(), indent=2, ensure_ascii=False)


# ──────────────────────────────────────────────
#  USERS (opzionale, per admin)
# ──────────────────────────────────────────────

@mcp.tool()
async def list_users(page: int = 1, page_size: int = 25) -> str:
    """Elenca gli utenti registrati (richiede permessi admin)."""
    params = {
        "pagination[page]": page,
        "pagination[pageSize]": page_size,
    }
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            _api("users"), headers=_headers(), params=params
        )
        resp.raise_for_status()
    return json.dumps(resp.json(), indent=2, ensure_ascii=False)


# ──────────────────────────────────────────────
#  HELPERS
# ──────────────────────────────────────────────

def _flatten_filters(obj: dict, prefix: str, out: dict) -> None:
    """Converte filtri annidati in query params piatti per Strapi."""
    for key, value in obj.items():
        new_key = f"{prefix}[{key}]"
        if isinstance(value, dict):
            _flatten_filters(value, new_key, out)
        else:
            out[new_key] = value


# ──────────────────────────────────────────────
#  RESOURCES (contesto per Claude)
# ──────────────────────────────────────────────

@mcp.resource("strapi://config")
async def strapi_config() -> str:
    """Configurazione corrente del server Strapi."""
    return json.dumps(
        {
            "strapi_url": STRAPI_URL,
            "token_configured": bool(STRAPI_TOKEN),
        },
        indent=2,
    )


if __name__ == "__main__":
    mcp.run()
