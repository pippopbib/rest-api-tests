import requests
import pytest

# GET список пользователей (users)
def test_get_users():
    response = requests.get("https://jsonplaceholder.typicode.com/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

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


# Параметризация
@pytest.mark.parametrize("name, job", [("Bob", "QA"), ("Eve", "DevOps")])
def test_create_user_params(name, job):
    response = requests.post(f"https://jsonplaceholder.typicode.com/users/", json={"name": name, "job": job})
    assert response.status_code == 201


# Ошибка — пользователь не существует
def test_user_not_found():
    response = requests.get("https://jsonplaceholder.typicode.com/users/9999")
    assert response.status_code == 404 or response.json() == {}

# DELETE — удалить пост (на jsonplaceholder работает как фикция)
def test_delete_post():
    response = requests.delete("https://jsonplaceholder.typicode.com/posts/1")
    assert response.status_code == 200