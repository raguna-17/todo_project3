# backend/todo/tests/test_models.py
import pytest
from django.contrib.auth import get_user_model
from todo.models import Todo

User = get_user_model()

@pytest.mark.django_db
def test_create_todo():
    user = User.objects.create_user(username="testuser", password="password")
    todo = Todo.objects.create(owner=user, title="テストTodo")
    assert todo.title == "テストTodo"
    assert todo.completed is False
    assert todo.owner == user
