from pydantic import BaseModel, Field


class Ability(BaseModel):
    name: str
    is_hidden: bool
    slot: int = Field(ge=1)


class Pokemon(BaseModel):
    id: int = Field(ge=1, le=151)
    name: str
    height: int = Field(ge=1, description="Height in decimetres.")
    weight: int = Field(ge=1, description="Weight in hectograms.")
    base_experience: int | None = Field(default=None, ge=0)
    types: list[str] = Field(min_length=1)
    abilities: list[Ability] = Field(min_length=1)
    stats: dict[str, int]
    sprite_default: str | None = None
    official_artwork: str | None = None
    source_url: str


class PokemonFilters(BaseModel):
    limit: int = Field(default=20, ge=1, le=151)
    offset: int = Field(default=0, ge=0, le=150)
    type: str | None = Field(default=None, min_length=1, max_length=30)
    name: str | None = Field(default=None, min_length=1, max_length=50)


class PokemonListResponse(BaseModel):
    total: int = Field(ge=0)
    limit: int = Field(ge=1, le=151)
    offset: int = Field(ge=0, le=150)
    items: list[Pokemon]


class HealthResponse(BaseModel):
    status: str
    pokemon_count: int = Field(ge=0)
