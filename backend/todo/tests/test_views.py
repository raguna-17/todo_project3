# todo/tests/test_views.py
import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from todo.models import Todo

from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

@pytest.mark.django_db
def test_todo_list_api():
    client = APIClient()

    # ユーザー作成
    user = User.objects.create_user(username="testuser", password="password")

    # JWT トークン発行
    token = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.access_token}')

    # Todo を作成
    Todo.objects.create(owner=user, title="サンプルTodo")

    # router の basename-list を使って URL を取得
    url = reverse("todo-list")

    # GET リクエスト
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 1
