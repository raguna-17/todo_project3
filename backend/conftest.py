import pytest
from django.contrib.auth import get_user_model


User = get_user_model()

@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()

@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="password123")

#backend/conftest.py