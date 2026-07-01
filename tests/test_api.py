from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_reports_dataset_count() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "pokemon_count": 151}


def test_list_pokemon_returns_default_page() -> None:
    response = client.get("/pokemon")

    assert response.status_code == 200
    payload = response.json()
    assert payload["total"] == 151
    assert payload["limit"] == 20
    assert payload["offset"] == 0
    assert len(payload["items"]) == 20
    assert payload["items"][0]["name"] == "bulbasaur"


def test_list_pokemon_supports_pagination() -> None:
    response = client.get("/pokemon", params={"limit": 5, "offset": 20})

    assert response.status_code == 200
    payload = response.json()
    assert payload["limit"] == 5
    assert payload["offset"] == 20
    assert len(payload["items"]) == 5
    assert payload["items"][0]["id"] == 21


def test_list_pokemon_filters_by_type() -> None:
    response = client.get("/pokemon", params={"type": "fire", "limit": 151})

    assert response.status_code == 200
    payload = response.json()
    assert payload["total"] > 0
    assert all("fire" in item["types"] for item in payload["items"])


def test_list_pokemon_filters_by_name_fragment() -> None:
    response = client.get("/pokemon", params={"name": "saur", "limit": 151})

    assert response.status_code == 200
    names = [item["name"] for item in response.json()["items"]]
    assert names == ["bulbasaur", "ivysaur", "venusaur"]


def test_get_pokemon_by_id() -> None:
    response = client.get("/pokemon/25")

    assert response.status_code == 200
    payload = response.json()
    assert payload["id"] == 25
    assert payload["name"] == "pikachu"
    assert "electric" in payload["types"]


def test_get_pokemon_by_name() -> None:
    response = client.get("/pokemon/pikachu")

    assert response.status_code == 200
    assert response.json()["id"] == 25


def test_get_pokemon_returns_404_for_unknown_identifier() -> None:
    response = client.get("/pokemon/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Pokemon not found"}


def test_query_validation_errors_return_422() -> None:
    response = client.get("/pokemon", params={"limit": 0})

    assert response.status_code == 422
