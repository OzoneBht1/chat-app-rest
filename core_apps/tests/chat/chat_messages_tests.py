import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core_apps.tests.factories import UserFactory, ChatMessageFactory
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_chat_message_ordering():
    user = UserFactory.create()
    user2 = UserFactory.create()

    client = APIClient()
    client.force_authenticate(user)

    ChatMessageFactory.create_batch(3, sender=user, receiver=user2)
    ChatMessageFactory.create_batch(3, sender=user2, receiver=user)
    url = reverse("chat_message_history", kwargs={"user_id": user2.id})
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data, dict)
    assert "results" in response.data
    assert isinstance(response.data["results"], list)

    results = response.data["results"]
    assert len(results) == 6

    first_message_created_at = results[0]["created_at"]
    last_message_created_at = results[-1]["created_at"]
    # make sure the ordering is descending based on created_at
    assert first_message_created_at >= last_message_created_at


@pytest.mark.django_db
def test_chat_message_history_no_messages(api_client):
    user1 = UserFactory.create()
    user2 = UserFactory.create()
    url = reverse("chat_message_history", kwargs={"user_id": user2.id})

    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data, dict)
    assert "results" in response.data
    assert len(response.data["results"]) == 0


@pytest.mark.django_db
def test_chat_message_history_invalid_user(api_client):
    invalid_user_id = 999
    url = reverse("chat_message_history", kwargs={"user_id": invalid_user_id})

    response = api_client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "detail" in response.data
    assert (
        response.data["detail"]
        == f"User with requested ID {invalid_user_id} does not exist."
    )
