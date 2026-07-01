from typing import Annotated

from fastapi import APIRouter, Depends

from app.models import HealthResponse
from app.repository import PokemonRepository, get_repository


router = APIRouter(tags=["health"])
RepositoryDependency = Annotated[PokemonRepository, Depends(get_repository)]


@router.get("/health", response_model=HealthResponse)
async def health(repository: RepositoryDependency) -> HealthResponse:
    return HealthResponse(status="ok", pokemon_count=repository.count)
