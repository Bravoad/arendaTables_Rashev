import pytest
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# Фикстура для создания столика для тестирования бронирований
@pytest.fixture(scope="module")
def create_table_for_reservations():
    table_data = {"name": "Reservation Table", "seats": 4, "location": "зал"}
    response = client.post("/tables/", json=table_data)
    assert response.status_code == 201, response.text
    return response.json()


def test_create_reservation(create_table_for_reservations):
    table = create_table_for_reservations
    reservation_data = {
        "customer_name": "Ivan",
        "table_id": table["id"],
        "reservation_time": (datetime.now() + timedelta(hours=1)).isoformat(),
        "duration_minutes": 90
    }
    response = client.post("/reservations/", json=reservation_data)
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["customer_name"] == reservation_data["customer_name"]
    assert data["table_id"] == reservation_data["table_id"]
    assert "id" in data


def test_create_reservation_conflict(create_table_for_reservations):
    table = create_table_for_reservations
    # Создаем первую бронь
    start_time = datetime.now() + timedelta(hours=2)
    reservation_data = {
        "customer_name": "Alex",
        "table_id": table["id"],
        "reservation_time": start_time.isoformat(),
        "duration_minutes": 60
    }
    first_response = client.post("/reservations/", json=reservation_data)
    assert first_response.status_code == 201, first_response.text

    # Пытаемся создать пересекающуюся бронь
    overlapping_start = start_time + timedelta(minutes=30)  # Пересекается с предыдущей
    conflict_reservation_data = {
        "customer_name": "Nina",
        "table_id": table["id"],
        "reservation_time": overlapping_start.isoformat(),
        "duration_minutes": 45
    }
    conflict_response = client.post("/reservations/", json=conflict_reservation_data)
    assert conflict_response.status_code == 409, conflict_response.text
    conflict_data = conflict_response.json()
    assert "Table already reserved" in conflict_data["detail"]


def test_delete_reservation(create_table_for_reservations):
    table = create_table_for_reservations
    reservation_data = {
        "customer_name": "Mark",
        "table_id": table["id"],
        "reservation_time": (datetime.now() + timedelta(hours=3)).isoformat(),
        "duration_minutes": 30
    }
    create_response = client.post("/reservations/", json=reservation_data)
    assert create_response.status_code == 201, create_response.text
    reservation = create_response.json()
    del_response = client.delete(f"/reservations/{reservation['id']}")
    assert del_response.status_code == 204, del_response.text
    second_del = client.delete(f"/reservations/{reservation['id']}")
    assert second_del.status_code == 404
