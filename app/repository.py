from functools import lru_cache
import json
from pathlib import Path

from app.models import Pokemon


DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "pokemon_151.json"
EXPECTED_STATS = {
    "hp",
    "attack",
    "defense",
    "special-attack",
    "special-defense",
    "speed",
}


class PokemonRepository:
    def __init__(self, records: list[Pokemon]) -> None:
        self._records = sorted(records, key=lambda record: record.id)
        self._by_id = {record.id: record for record in self._records}
        self._by_name = {record.name.lower(): record for record in self._records}

    @classmethod
    def from_json(cls, path: Path = DATA_PATH) -> "PokemonRepository":
        raw_records = json.loads(path.read_text(encoding="utf-8"))
        records = [Pokemon(**record) for record in raw_records]
        repository = cls(records)
        repository.validate()
        return repository

    @property
    def count(self) -> int:
        return len(self._records)

    def validate(self) -> None:
        ids = [record.id for record in self._records]
        if ids != list(range(1, 152)):
            raise ValueError("Pokemon dataset must contain IDs 1 through 151.")

        for record in self._records:
            if set(record.stats) != EXPECTED_STATS:
                raise ValueError(f"Pokemon {record.id} has invalid stat keys.")

    def list(
        self,
        *,
        limit: int,
        offset: int,
        name: str | None = None,
        type: str | None = None,
    ) -> tuple[int, list[Pokemon]]:
        matches = self._records

        if name:
            normalized_name = name.strip().lower()
            matches = [
                record for record in matches if normalized_name in record.name.lower()
            ]

        if type:
            normalized_type = type.strip().lower()
            matches = [
                record
                for record in matches
                if normalized_type in {pokemon_type.lower() for pokemon_type in record.types}
            ]

        total = len(matches)
        return total, matches[offset : offset + limit]

    def get(self, id_or_name: str) -> Pokemon | None:
        value = id_or_name.strip().lower()
        if value.isdecimal():
            return self._by_id.get(int(value))
        return self._by_name.get(value)


@lru_cache(maxsize=1)
def get_repository() -> PokemonRepository:
    return PokemonRepository.from_json()
