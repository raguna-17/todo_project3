# todo/tests/test_register.py
import pytest
from rest_framework.test import APIClient
from django.urls import reverse

@pytest.mark.django_db
def test_register_view():
    client = APIClient()
    url = reverse("register")
    data = {"username": "testuser", "password": "password123"}
    response = client.post(url, data)
    assert response.status_code == 201
    assert response.data["username"] == "testuser"
    assert "id" in response.data
