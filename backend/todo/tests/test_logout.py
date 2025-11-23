# todo/tests/test_logout.py
import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from todo.tests.factories import UserFactory
from rest_framework_simplejwt.tokens import RefreshToken

@pytest.mark.django_db
def test_logout_view():
    client = APIClient()
    user = UserFactory()
    refresh = RefreshToken.for_user(user)

    # 正常ログアウト
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    response = client.post(reverse("logout"), {"refresh": str(refresh)})
    assert response.status_code == 205

    # トークンなし
    response = client.post(reverse("logout"), {})
    assert response.status_code == 400
