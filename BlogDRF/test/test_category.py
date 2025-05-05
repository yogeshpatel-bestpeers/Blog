import pytest
from django.urls import reverse
from rest_framework import status

from Blog.models import Category

from .conftest import admin_user, category


@pytest.mark.django_db
def test_category_get_all(api_client, category):

    response = api_client.get(reverse("category-view"))

    assert response.status_code == status.HTTP_200_OK
    assert any(cat["name"] == "Tech" for cat in response.data)


@pytest.mark.django_db
def test_create_category_admin(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    data = {"name": "Science"}

    response = api_client.post("/api/categories/", data=data)
    assert response.status_code == 201
    assert Category.objects.filter(name="Science").exists()


@pytest.mark.django_db
def test_create_category_non_admin(api_client, user):
    api_client.force_authenticate(user=user)
    data = {"name": "Unauthorized Category"}

    response = api_client.post("/api/categories/", data=data)
    assert response.status_code == 403
    assert not Category.objects.filter(name="Unauthorized Category").exists()


@pytest.mark.django_db
def test_delete_category_as_admin(api_client, admin_user):
    category = Category.objects.create(name="Delete")
    api_client.force_authenticate(user=admin_user)

    response = api_client.delete(f"/api/categories/{category.pk}/")
    assert response.status_code == 204
    assert not Category.objects.filter(pk=category.pk).exists()


@pytest.mark.django_db
def test_delete_category_as_non_admin(api_client, user):
    category = Category.objects.create(name="Delete")
    api_client.force_authenticate(user=user)

    response = api_client.delete(f"/api/categories/{category.pk}/")
    assert response.status_code == 403
