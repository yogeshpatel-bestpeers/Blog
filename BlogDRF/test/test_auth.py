import pytest
from django.urls import reverse
from rest_framework import status

from .conftest import api_client, user


@pytest.mark.django_db
def test_register_user_success(api_client):
    data = {
        "username": "pytest123",
        "first_name": "test",
        "last_name": "test",
        "email": "pytest@example.com",
        "password": "testPassword123",
    }
    response = api_client.post(reverse("signup_user"), data=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["email"] == data["email"]


@pytest.mark.django_db
def test_register_duplicate_user(api_client):
    data = {
        "username": "pytest123",
        "first_name": "test",
        "last_name": "test",
        "email": "pytest@example.com",
        "password": "testPassword123",
    }
    api_client.post(reverse("signup_user"), data)
    data["username"] = "pytest456"
    response2 = api_client.post(reverse("signup_user"), data)
    assert response2.status_code == status.HTTP_400_BAD_REQUEST
    assert "email" in response2.data


@pytest.mark.django_db
def test_login_user_success(api_client, user):

    data = {"email": "testuser@example.com", "password": "testpassword123"}
    response = api_client.post(reverse("login_user"), data)
    assert response.status_code == status.HTTP_200_OK



@pytest.mark.django_db
def test_login_user_invalid_credentials(api_client):
    data = {"email": "wrong@example.com", "password": "wrongpassword"}
    response = api_client.post(reverse("login_user"), data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data["error"] == "Invalid email or password"


@pytest.mark.django_db
def test_login_user_missing_fields(api_client):
    response = api_client.post(reverse("login_user"), {})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["error"] == "Email and password are required"


@pytest.mark.django_db
def test_logout_authenticated_user(api_client, user):
    api_client.force_authenticate(user=user)
    response = api_client.get(reverse("logout_user"))  
    print(response)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED 
