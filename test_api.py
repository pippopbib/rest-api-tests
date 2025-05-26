import requests
import pytest
from jsonschema import validate

# Схема ответа для запроса списка пользователей
user_list_schema = {
    "type": "object",
    "properties": {
        "page": {"type": "integer"},
        "per_page": {"type": "integer"},
        "total": {"type": "integer"},
        "total_pages": {"type": "integer"},
        "data": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "email": {"type": "string"},
                    "first_name": {"type": "string"},
                    "last_name": {"type": "string"},
                    "avatar": {"type": "string"}
                },
                "required": ["id", "email", "first_name", "last_name", "avatar"]
            }
        }
    },
    "required": ["page", "data"]
}

def test_get_users_schema():
    response = requests.get("https://reqres.in/api/users?page=2")
    assert response.status_code == 200
    validate(instance=response.json(), schema=user_list_schema)

# GET список пользователей (users)
def test_get_users():
    response = requests.get("https://reqres.in/api/users?page=2")
    assert response.status_code == 200
    assert "data" in response.json()

# POST — создать пользователя
def test_create_user():
    payload = {"name": "Alice", "job": "Engineer"}
    response = requests.post("https://reqres.in/api/users", json=payload)
    assert response.status_code == 201
    assert "id" in response.json()

# Параметризация
@pytest.mark.parametrize("name, job", [("Bob", "QA"), ("Eve", "DevOps")])
def test_create_user_params(name, job):
    response = requests.post("https://reqres.in/api/users", json={"name": name, "job": job})
    assert response.status_code == 201
    assert "id" in response.json()

# DELETE — удалить пользователя (мнимая операция)
def test_delete_user():
    response = requests.delete("https://reqres.in/api/users/2")
    assert response.status_code == 204