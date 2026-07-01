# pokemon_api

Simple FastAPI backend that serves a cached sample dataset of the first 151
Pokemon from PokeAPI.

The API reads from `data/pokemon_151.json` at runtime. It does not call PokeAPI
while handling requests.

## Repository Contents

- [FastAPI functionality guide](docs/fastapi-functionality.md): practical
  FastAPI features to use in the future backend.
- [PokeAPI sample data guide](docs/pokeapi-sample-data.md): source,
  normalization rules, refresh process, and validation expectations.
- [Cached Pokemon dataset](data/pokemon_151.json): normalized records for
  National Pokedex IDs 1 through 151.
- [FastAPI application](app/main.py): app factory, CORS, docs redirect, and
  router registration.
- [API tests](tests/test_api.py): health, list, filtering, detail, 404, and
  validation coverage.

## API

Implemented endpoints:

- `GET /health`
- `GET /pokemon`
- `GET /pokemon/{id_or_name}`

`GET /pokemon` supports optional query parameters:

- `limit`: page size from `1` to `151`, default `20`
- `offset`: starting index from `0` to `150`, default `0`
- `type`: exact Pokemon type filter, such as `fire`
- `name`: case-insensitive name fragment filter, such as `saur`

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Run

```bash
fastapi dev app/main.py
```

Then open http://127.0.0.1:8000/docs for the generated OpenAPI UI.

## Test

```bash
pytest
```

## Dataset Check

The cached dataset should always contain exactly 151 unique records, ordered by
Pokemon ID, with `bulbasaur` first and `mew` last. The detailed schema and
refresh instructions live in [docs/pokeapi-sample-data.md](docs/pokeapi-sample-data.md).
