from datetime import datetime, timedelta
from tempfile import NamedTemporaryFile
from .factories import (
    UserFactory,
)

import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient


register(UserFactory)


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


@pytest.fixture
def superuser_api_client(get_superuser):
    client = APIClient()
    client.force_authenticate(user=get_superuser)
    return client
