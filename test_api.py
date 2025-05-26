import requests
import pytest
from jsonschema import validate

# GET список пользователей
def test_get_users():
    response = requests.get("https://jsonplaceholder.typicode.com/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

def test_get_users_schema():
    schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "id": {"type": "number"},
                "name": {"type": "string"},
                "username": {"type": "string"},
                "email": {"type": "string"},
            },
            "required": ["id", "name", "username", "email"]
        }
    }
    response = requests.get("https://jsonplaceholder.typicode.com/users")
    assert validate(response.json(), schema) is None

# GET конкретный пользователь
def test_get_single_user():
    response = requests.get("https://jsonplaceholder.typicode.com/users/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "name" in data

# POST — создать пост
def test_create_post():
    payload = {"title": "foo", "body": "bar", "userId": 1}
    response = requests.post("https://jsonplaceholder.typicode.com/posts", json=payload)
    assert response.status_code == 201
    result = response.json()
    assert result["title"] == "foo"
    assert "id" in result

# Параметризация для создания поста
@pytest.mark.parametrize("title, body, userId", [
    ("Test Title 1", "Test Body 1", 1),
    ("Test Title 2", "Test Body 2", 2),
])
def test_create_post_params(title, body, userId):
    payload = {"title": title, "body": body, "userId": userId}
    response = requests.post("https://jsonplaceholder.typicode.com/posts", json=payload)
    assert response.status_code == 201
    result = response.json()
    assert result["title"] == title
    assert result["body"] == body
    assert result["userId"] == userId

# PUT — обновить пост
def test_update_post_put():
    payload = {"id": 1, "title": "Updated Title", "body": "Updated Body", "userId": 1}
    response = requests.put("https://jsonplaceholder.typicode.com/posts/1", json=payload)
    assert response.status_code == 200
    result = response.json()
    assert result["title"] == "Updated Title"

# PATCH — частично обновить пост
def test_update_post_patch():
    payload = {"title": "Patched Title"}
    response = requests.patch("https://jsonplaceholder.typicode.com/posts/1", json=payload)
    assert response.status_code == 200
    result = response.json()
    assert result["title"] == "Patched Title"

# DELETE — удалить пост
def test_delete_post():
    response = requests.delete("https://jsonplaceholder.typicode.com/posts/1")
    assert response.status_code == 200
    assert response.json() == {}

# Ошибка — пользователь не существует
def test_user_not_found():
    response = requests.get("https://jsonplaceholder.typicode.com/users/9999")
    assert response.status_code == 404

# Ошибка — неверные данные для создания поста
def test_create_post_invalid_data():
    payload = {"title": "foo"}  # Только title
    response = requests.post("https://jsonplaceholder.typicode.com/posts", json=payload)
    assert response.status_code == 201  # API принимает неполные данные
    result = response.json()
    assert "id" in result  # Проверяем, что пост создан
