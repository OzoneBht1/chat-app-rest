from django.test.html import normalize_attributes
from django.urls import reverse
import pytest
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from core_apps.tests.factories import UserFactory


@pytest.mark.django_db
def test_user_registration(api_client):
    user = UserFactory.build()
    url = reverse("register_user")
    data = {
        "email": user.email,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "password": user.password,
        "password2": user.password,
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert "email" in response.data
    assert "username" in response.data
    assert "first_name" in response.data
    assert "last_name" in response.data


@pytest.mark.django_db
def test_user_registration_password_mismatch(api_client):
    user = UserFactory.build()
    url = reverse("register_user")
    data = {
        "email": user.email,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "password": user.password,
        "password2": "randomstring123",
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "password" in response.data


@pytest.mark.django_db
def test_user_registration_existing_user(api_client, get_user):
    user = UserFactory.build()
    url = reverse("register_user")
    data = {
        "email": get_user.email,
        "username": get_user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "password": user.password,
        "password2": user.password,
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "username" in response.data or "email" in response.data


@pytest.mark.django_db
def test_user_logout(api_client, get_user):
    logout_url = reverse("logout_user")
    refresh = RefreshToken.for_user(get_user)
    data = {"refresh_token": str(refresh)}
    response = api_client.post(logout_url, data)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    refresh_token_url = reverse("token_refresh")
    response = api_client.post(refresh_token_url, data)
    # can no longer refresh with the token, it is already blacklisted
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    with pytest.raises(TokenError):
        # trying to logout with same token will throw TokenError
        response = api_client.post(logout_url, data)


@pytest.mark.django_db
def test_superuser_user_list(superuser_api_client):
    url = reverse("users_list")
    normal_users_to_create, staff_users_to_create = 2, 2
    UserFactory.create_batch(normal_users_to_create, is_staff=False)
    UserFactory.create_batch(staff_users_to_create, is_staff=True)
    response = superuser_api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    total_users_count = 1 + normal_users_to_create + staff_users_to_create
    assert response.data["count"] == total_users_count
    assert "results" in response.data


@pytest.mark.django_db
def test_regular_user_list(api_client):
    url = reverse("users_list")
    normal_users_to_create, staff_users_to_create = 2, 2
    UserFactory.create_batch(normal_users_to_create, is_staff=False)
    UserFactory.create_batch(staff_users_to_create, is_staff=True)
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    total_users_count = 1 + normal_users_to_create + staff_users_to_create
    # user cannot see staff users accounts
    assert response.data["count"] == total_users_count - staff_users_to_create
    assert "results" in response.data
