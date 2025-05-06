import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient

from Blog.models import Blog, Category, CustomUser



@pytest.fixture(autouse=True)
def media_root(tmp_path, settings):
    settings.MEDIA_ROOT = tmp_path


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return CustomUser.objects.create_user(
        email="testuser@example.com", username="testuser", password="testpassword123"
    )


@pytest.fixture
def admin_user():
    return CustomUser.objects.create_superuser(
        username="admin", password="admin123", email="admin@example.com"
    )


@pytest.fixture
def category():
    return Category.objects.create(name="Tech")


@pytest.fixture
def blog(user, category):
    return Blog.objects.create(
        title="Test Blog",
        content="This is test content.",
        category=category,
        user=user,
        featured_image=SimpleUploadedFile("test.jpg", b"file_content"),
    )
