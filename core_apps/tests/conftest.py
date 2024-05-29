from .factories import (
    ChatMessageFactory,
    UserFactory,
)

import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient


register(UserFactory)
register(ChatMessageFactory)


@pytest.fixture
def get_user(user_factory: UserFactory):
    new_user = user_factory.create()
    return new_user


@pytest.fixture
def get_superuser(user_factory: UserFactory):
    new_user = user_factory.create(is_superuser=True, is_staff=True)
    return new_user


@pytest.fixture
def api_client(get_user):
    client = APIClient()
    client.force_authenticate(get_user)
    return client


api_client2 = api_client
# making a copy of the api client to use two authenticated
# users in one function


@pytest.fixture
def superuser_api_client(get_superuser):
    client = APIClient()
    client.force_authenticate(user=get_superuser)
    return client
