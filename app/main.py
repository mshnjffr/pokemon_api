from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from app.routes import health, pokemon


def create_app() -> FastAPI:
    app = FastAPI(
        title="Pokemon API",
        summary="Simple FastAPI backend over a cached PokeAPI sample dataset.",
        version="0.1.0",
        openapi_tags=[
            {"name": "health", "description": "Service health and readiness."},
            {"name": "pokemon", "description": "Read-only Pokemon catalog endpoints."},
        ],
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "http://localhost:5173",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5173",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/", include_in_schema=False)
    async def docs_redirect() -> RedirectResponse:
        return RedirectResponse(url="/docs")

    app.include_router(health.router)
    app.include_router(pokemon.router)
    return app


app = create_app()
