import httpx
import respx

from app.main import CAT_API_URL

CAT = {"cat_id": "abc", "url": "https://cdn2.thecatapi.com/images/abc.jpg"}


# --- health ---


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# --- náhodná kočka (Cat API je falešné) ---


@respx.mock
def test_random_cat(client):
    # Když aplikace zavolá Cat API, dostane tuhle odpověď
    respx.get(CAT_API_URL).mock(return_value=httpx.Response(200, json=[{"id": "abc", "url": CAT["url"], "width": 600, "height": 400}]))

    response = client.get("/api/cats/random")

    assert response.status_code == 200
    assert response.json() == {"id": "abc", "url": CAT["url"]}


@respx.mock
def test_random_cat_api_down(client):
    # Cat API vrátí chybu, my máme vrátit 502
    respx.get(CAT_API_URL).mock(return_value=httpx.Response(500))

    response = client.get("/api/cats/random")

    assert response.status_code == 502


# --- oblíbené ---


def test_add_favorite(client):
    response = client.post("/api/favorites", json=CAT)

    assert response.status_code == 201
    data = response.json()
    assert data["cat_id"] == "abc"
    assert "id" in data
    assert "created_at" in data


def test_add_favorite_duplicate(client):
    client.post("/api/favorites", json=CAT)
    response = client.post("/api/favorites", json=CAT)

    assert response.status_code == 409


def test_add_favorite_invalid(client):
    # Chybí "url", FastAPI má vrátit 422
    response = client.post("/api/favorites", json={"cat_id": "abc"})

    assert response.status_code == 422


def test_list_favorites(client):
    client.post("/api/favorites", json=CAT)

    response = client.get("/api/favorites")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_delete_favorite(client):
    favorite = client.post("/api/favorites", json=CAT).json()

    response = client.delete(f"/api/favorites/{favorite['id']}")
    assert response.status_code == 204

    # Podruhé už neexistuje
    response = client.delete(f"/api/favorites/{favorite['id']}")
    assert response.status_code == 404
