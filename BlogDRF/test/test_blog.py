import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from Blog.models import Blog

from .conftest import api_client, blog, category, user


@pytest.mark.django_db
def test_get_blog_list(api_client, blog):
    url = reverse("blog-list")
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data[0]["title"] == blog.title


@pytest.mark.django_db
def test_create_blog(api_client, user, category):
    api_client.force_authenticate(user=user)
    url = reverse("blog-list")

    data = {
        "user": str(user.id),
        "title": "New Blog",
        "content": "Blog content here.",
        "category": category.id, 
    }
    print(data)

    # Ensure the format is JSON (not multipart)
    response = api_client.post(url,data= data, format="json")

    print(response.data)

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_get_blog_detail(api_client, blog):
    url = reverse("blog-detail", args=[blog.id])
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data["title"] == blog.title


@pytest.mark.django_db
def test_update_blog(api_client, blog, user):
    api_client.force_authenticate(user=user)
    url = reverse("blog-detail", args=[blog.id])
    data = {
        "title": "Updated Title",
        "content": "Updated content",
        "category": str(blog.category.id),
    }
    response = api_client.put(url, data)
    assert response.status_code == 200
    assert response.data["title"] == "Updated Title"


@pytest.mark.django_db
def test_delete_blog(api_client, blog, user):
    api_client.force_authenticate(user=user)
    url = reverse("blog-detail", args=[blog.id])
    response = api_client.delete(url)
    assert response.status_code == 204
    assert not Blog.objects.filter(id=blog.id).exists()
