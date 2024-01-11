import os

import hypothesis
import pytest
from factory.random import reseed_random
from faker import Faker
from hypothesis import strategies as st
from hypothesis.extra.django import register_field_strategy
from phonenumber_field.modelfields import PhoneNumberField
from pytest_factoryboy import register as register_factory
from rest_framework.test import APIClient, APIRequestFactory

from users.factories import UserFactory
from users.models import TeamUser

FAKER_SEED = 3318140460
FAKER_LOCALE = ["en_AU"]

register_factory(UserFactory)


@pytest.fixture
def api_client():
    yield APIClient()


@pytest.fixture
def api_rf():
    yield APIRequestFactory()


@pytest.fixture(scope="module", autouse=True)
def faker_locale():
    return FAKER_LOCALE


@pytest.fixture(scope="module", autouse=True)
def faker_seed():
    return FAKER_SEED


@pytest.fixture
def user(db) -> TeamUser:
    return UserFactory()


@pytest.fixture
def superuser(db) -> TeamUser:
    return UserFactory(is_staff=True, is_superuser=True)


# noinspection PyUnusedLocal
def pytest_configure(config):
    Faker.seed(FAKER_SEED)
    reseed_random(FAKER_SEED)

    register_field_strategy(PhoneNumberField, st.text(max_size=128))
    hypothesis.settings.register_profile("fast", max_examples=10)
    hypothesis.settings.register_profile("ci", max_examples=100)
    hypothesis.settings.load_profile(os.getenv("HYPOTHESIS_PROFILE", "fast"))
