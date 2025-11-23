# todo/tests/test_todo_crud.py
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from todo.tests.factories import UserFactory, TodoFactory
from rest_framework_simplejwt.tokens import RefreshToken

@pytest.mark.django_db
def test_todo_list_and_create():
    client = APIClient()
    user = UserFactory()
    token = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.access_token}')

    # Create
    response = client.post(reverse("todo-list"), {"title": "タスク1"})
    assert response.status_code == 201
    assert response.data["title"] == "タスク1"

    # List
    response = client.get(reverse("todo-list"))
    assert response.status_code == 200
    assert len(response.data) == 1

@pytest.mark.django_db
def test_todo_update_and_delete():
    client = APIClient()
    user = UserFactory()
    token = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.access_token}')

    todo = TodoFactory(owner=user)

    # Update
    url = reverse("todo-detail", args=[todo.id])
    response = client.patch(url, {"completed": True})
    assert response.status_code == 200
    assert response.data["completed"] is True

    # Delete
    response = client.delete(url)
    assert response.status_code == 204
