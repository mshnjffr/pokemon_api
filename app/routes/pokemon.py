from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

from app.models import Pokemon, PokemonFilters, PokemonListResponse
from app.repository import PokemonRepository, get_repository


router = APIRouter(prefix="/pokemon", tags=["pokemon"])
RepositoryDependency = Annotated[PokemonRepository, Depends(get_repository)]


@router.get("", response_model=PokemonListResponse)
async def list_pokemon(
    filters: Annotated[PokemonFilters, Query()],
    repository: RepositoryDependency,
) -> PokemonListResponse:
    total, items = repository.list(
        limit=filters.limit,
        offset=filters.offset,
        name=filters.name,
        type=filters.type,
    )
    return PokemonListResponse(
        total=total,
        limit=filters.limit,
        offset=filters.offset,
        items=items,
    )


@router.get("/{id_or_name}", response_model=Pokemon)
async def get_pokemon(
    id_or_name: Annotated[
        str,
        Path(
            min_length=1,
            max_length=50,
            description="Pokemon National Pokedex ID or lowercase name.",
        ),
    ],
    repository: RepositoryDependency,
) -> Pokemon:
    pokemon = repository.get(id_or_name)
    if pokemon is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pokemon not found",
        )
    return pokemon
