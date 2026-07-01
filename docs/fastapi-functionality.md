# FastAPI Functionality Guide

This guide documents the FastAPI features used by this simple backend API over
the cached Pokemon dataset. It is based on the current FastAPI package and
tutorial documentation reviewed through Context7.

Primary references:

- https://fastapi.tiangolo.com/
- https://fastapi.tiangolo.com/tutorial/
- https://fastapi.tiangolo.com/reference/

## Design Defaults

- Use Python 3.11+ and modern `typing.Annotated[...]` declarations for
  parameters with FastAPI metadata.
- Keep route handlers thin. Load and query `data/pokemon_151.json` through
  `app.repository.PokemonRepository`.
- Prefer Pydantic models for request, response, and query validation instead of
  hand-parsing dictionaries.
- Use FastAPI's generated OpenAPI schema and interactive docs as the first API
  contract for this learning project.

## Functionality Matrix

| Area | FastAPI functionality | How this app should use it |
| --- | --- | --- |
| App setup | `FastAPI(...)` | Configure title, version, summary, docs URLs, and tags metadata for Pokemon endpoints. |
| OpenAPI docs | Automatic `/docs`, `/redoc`, `/openapi.json` | Treat generated docs as the public contract while the app is small. |
| Routing | `@app.get`, `@router.get` | The app exposes read-only `GET /health`, `GET /pokemon`, and `GET /pokemon/{id_or_name}`. |
| Routers | `APIRouter`, `include_router` | Health and Pokemon endpoints are split into tagged routers. |
| Path params | `Path` | Validate `id_or_name` if separate numeric and name routes are not used. |
| Query params | `Query` and model-backed query parameters | Validate `limit`, `offset`, `type`, and `name` filters. |
| Request bodies | Pydantic `BaseModel` parameters | Not currently needed because the API is read-only. |
| Headers | `Header` | Use for optional request tracing or API version demonstrations. |
| Cookies | `Cookie` | Document as available, but avoid using cookies for this basic API unless a UI needs them. |
| Forms | `Form` | Useful for login or browser form examples, not required for Pokemon reads. |
| Files | `File`, `UploadFile` | Useful for future import/upload exercises; not required for the cached dataset. |
| Models | Pydantic models | Define `Pokemon`, `Ability`, and query/filter models for typed responses. |
| Response models | `response_model=...` | Filter outgoing data and keep API responses stable. |
| Status codes | `status_code`, `fastapi.status` | Return `200` for reads and `404` for missing Pokemon. |
| Errors | `HTTPException` | Raise `404` for unknown IDs/names and let validation errors produce `422`. |
| Exception handlers | `@app.exception_handler` | Add only if the default validation/error shape needs customization. |
| Response classes | `JSONResponse`, `PlainTextResponse`, `RedirectResponse`, streaming/file responses | Default JSON is enough; use explicit response classes for health text, redirects, or downloads if added. |
| Dependencies | `Depends` | Share dataset loading, pagination defaults, filtering, and auth placeholders. |
| Yield dependencies | `Depends` with `yield` | Use for resources that need cleanup; likely unnecessary for static JSON. |
| Security helpers | `Security`, OAuth2/API key helpers | Document for future protected endpoints, but keep this sample public. |
| Middleware | `add_middleware` | The app registers CORS middleware for local frontend origins. |
| CORS | `CORSMiddleware` | Localhost origins are allowed for common frontend dev servers. |
| Lifespan | `FastAPI(lifespan=...)` | Preload the JSON dataset at startup if repeated disk reads become noisy. |
| Background tasks | `BackgroundTasks` | Useful for later refresh/report jobs; do not use for request-time PokeAPI fetches. |
| Static files | `StaticFiles` | Optional if serving local images or a small demo frontend from the backend. |
| Templates | `Jinja2Templates` | Optional if adding server-rendered HTML pages. |
| WebSockets | `WebSocket` | Available for live demos, but out of scope for the simple REST API. |
| Mounted apps | `app.mount` | Useful only if a static frontend or sub-application is added. |
| Testing | `TestClient` | Tests cover route success, filtering, pagination, `404`, and `422` behavior. |

## Implemented Application Shape

This snippet mirrors the style used in the application code.

```python
from typing import Annotated

from fastapi import APIRouter, FastAPI, Path, Query, status
from pydantic import BaseModel, Field


class PokemonQuery(BaseModel):
    limit: int = Field(default=20, ge=1, le=151)
    offset: int = Field(default=0, ge=0, le=150)
    type: str | None = None
    name: str | None = None


class Ability(BaseModel):
    name: str
    is_hidden: bool
    slot: int


class Pokemon(BaseModel):
    id: int
    name: str
    height: int
    weight: int
    base_experience: int | None
    types: list[str]
    abilities: list[Ability]
    stats: dict[str, int]
    sprite_default: str | None
    official_artwork: str | None
    source_url: str


router = APIRouter(prefix="/pokemon", tags=["pokemon"])


@router.get("", response_model=list[Pokemon], status_code=status.HTTP_200_OK)
async def list_pokemon(filters: Annotated[PokemonQuery, Query()]):
    """Return cached Pokemon records using validated query parameters."""


@router.get("/{id_or_name}", response_model=Pokemon)
async def get_pokemon(
    id_or_name: Annotated[str, Path(description="Pokemon ID or lowercase name")],
):
    """Return one cached Pokemon by ID or name."""


app = FastAPI(
    title="Pokemon API",
    summary="Simple FastAPI backend over a cached PokeAPI sample dataset.",
    version="0.1.0",
)
app.include_router(router)
```

## Request And Response Patterns

Use `Annotated` when adding FastAPI metadata to typed parameters:

```python
from typing import Annotated

from fastapi import Query


Limit = Annotated[int, Query(ge=1, le=151)]
Offset = Annotated[int, Query(ge=0, le=150)]
```

Use `HTTPException` for application-level errors:

```python
from fastapi import HTTPException, status


def require_pokemon(record: dict | None) -> dict:
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pokemon not found",
        )
    return record
```

Use dependencies for shared inputs or services:

```python
from typing import Annotated

from fastapi import Depends


def get_dataset() -> list[dict]:
    return []


Dataset = Annotated[list[dict], Depends(get_dataset)]
```

Use `TestClient` for focused route behavior:

```python
from fastapi.testclient import TestClient


def test_health(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
```

## Implemented API Behavior

- `GET /health` returns a small JSON health response.
- `GET /pokemon` returns paginated cached records and supports validated
  filtering by `type` and `name`.
- `GET /pokemon/{id_or_name}` returns one record for numeric IDs or names.
- Unknown Pokemon return `404`; invalid query parameters return FastAPI's
  standard `422` validation response.
- Tests use `TestClient` and dependency overrides where external state would
  otherwise make tests slow or brittle.
