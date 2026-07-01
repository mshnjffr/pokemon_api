# PokeAPI Sample Data Guide

The sample dataset in `data/pokemon_151.json` contains normalized data for the
first 151 Pokemon from PokeAPI v2. It is cached locally so the FastAPI app can
serve consistent data without making runtime calls to PokeAPI.

Primary references:

- https://pokeapi.co/docs/v2
- https://pokeapi.co/api/v2/pokemon/?limit=151&offset=0

## Source

Use the PokeAPI resource list endpoint to discover the first 151 Pokemon:

```text
GET https://pokeapi.co/api/v2/pokemon/?limit=151&offset=0
```

Then fetch each detail resource from the returned `results[].url`. PokeAPI list
responses include `count`, `next`, `previous`, and `results`. Each named result
has a `name` and `url`.

PokeAPI is a read-only API and does not require authentication. Its fair-use
policy asks clients to cache resources locally and avoid unnecessary repeated
requests, which is why this repository stores the normalized dataset.

## Normalized Schema

Each item in `data/pokemon_151.json` has this shape:

```json
{
  "id": 1,
  "name": "bulbasaur",
  "height": 7,
  "weight": 69,
  "base_experience": 64,
  "types": ["grass", "poison"],
  "abilities": [
    {
      "name": "overgrow",
      "is_hidden": false,
      "slot": 1
    }
  ],
  "stats": {
    "hp": 45,
    "attack": 49,
    "defense": 49,
    "special-attack": 65,
    "special-defense": 65,
    "speed": 45
  },
  "sprite_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png",
  "official_artwork": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/1.png",
  "source_url": "https://pokeapi.co/api/v2/pokemon/1/"
}
```

Field notes:

- `height` is measured in decimetres, matching PokeAPI.
- `weight` is measured in hectograms, matching PokeAPI.
- `types` preserves PokeAPI slot order.
- `abilities` preserves PokeAPI slot order and includes hidden abilities.
- `stats` uses PokeAPI stat names as keys.
- `sprite_default` comes from `sprites.front_default`.
- `official_artwork` comes from `sprites.other.official-artwork.front_default`.

## Refresh Process

Refresh the dataset only when there is a clear reason to update the cached copy.
Do not fetch from PokeAPI during normal API requests.

The refresh logic should:

- Request `https://pokeapi.co/api/v2/pokemon/?limit=151&offset=0`.
- Fetch every detail URL from `results`.
- Normalize each detail response to the schema above.
- Sort records by `id`.
- Write the result to `data/pokemon_151.json` with two-space JSON formatting.

## Validation Checklist

Before committing a refreshed dataset, verify:

- The file contains exactly 151 records.
- IDs are unique and exactly cover `1` through `151`.
- The first record is `bulbasaur`.
- The last record is `mew`.
- Every record has at least one type and all six expected stats:
  `hp`, `attack`, `defense`, `special-attack`, `special-defense`, and `speed`.
- Every record has a `source_url` beginning with
  `https://pokeapi.co/api/v2/pokemon/`.

## API Usage

The FastAPI app loads this file as local application data. Endpoint behavior:

- `GET /pokemon` returns a paginated subset of records.
- `GET /pokemon?type=fire` returns records whose `types` include `fire`.
- `GET /pokemon?name=saur` returns records whose names contain `saur`.
- `GET /pokemon/25` and `GET /pokemon/pikachu` return the same record.
