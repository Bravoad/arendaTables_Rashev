import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_table():
    table_data = {"name": "Table 1", "seats": 4, "location": "зал у окна"}
    response = client.post("/tables/", json=table_data)
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["name"] == table_data["name"]
    assert data["seats"] == table_data["seats"]
    assert data["location"] == table_data["location"]
    assert "id" in data


def test_get_tables():
    response = client.get("/tables/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_create_table_duplicate_name():
    table_data = {"name": "Table 1", "seats": 4, "location": "зал у окна"}
    response = client.post("/tables/", json=table_data)
    assert response.status_code == 409, response.text


def test_delete_table():
    table_data = {"name": "Temp Table", "seats": 2, "location": "терраса"}
    response = client.post("/tables/", json=table_data)
    assert response.status_code == 201, response.text
    created_table = response.json()

    del_response = client.delete(f"/tables/{created_table['id']}")
    assert del_response.status_code == 204, del_response.text

    second_del = client.delete(f"/tables/{created_table['id']}")
    assert second_del.status_code == 404
