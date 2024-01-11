import pytest
from django.db.utils import IntegrityError

from users import models


@pytest.mark.django_db
def test_create_user(faker):
    email = faker.email()
    user = models.TeamUser.objects.create_user(  # nosec
        email=email,
        password=faker.password(length=42),
        phone=faker.phone_number(),
        timezone=faker.timezone(),
    )
    assert email == user.email
    assert user.is_active is True
    assert user.is_staff is False
    assert user.is_superuser is False
    assert user.phone.is_valid()


def test_create_user_noargs():
    with pytest.raises(TypeError):
        # pylint:disable=no-value-for-parameter
        models.TeamUser.objects.create_user()  # nomypy


def test_create_user_no_password(faker):
    with pytest.raises(TypeError):
        # pylint:disable=no-value-for-parameter
        models.TeamUser.objects.create_user(email=faker.email())  # nomypy


def test_create_user_blank_email(faker):
    with pytest.raises(ValueError):
        models.TeamUser.objects.create_user(
            email="", password=faker.password(length=41)
        )  # nosec


@pytest.mark.django_db
def test_create_superuser(faker):
    email = faker.email()
    admin_user = models.TeamUser.objects.create_superuser(  # nosec
        email=email, password=faker.password(length=42)
    )
    assert admin_user.email == email
    assert admin_user.is_active is True
    assert admin_user.is_staff is True
    assert admin_user.is_superuser is True

    db_user = models.TeamUser.objects.get(email=email)
    assert admin_user.email == db_user.email
    assert admin_user.pk == db_user.pk


@pytest.mark.django_db
def test_user_unique_email(faker):
    email = faker.email()
    models.TeamUser.objects.create_user(
        email=email, password=faker.password(length=64)
    )  # nosec
    with pytest.raises(IntegrityError):
        models.TeamUser.objects.create_superuser(  # nosec
            email=email, password=faker.password(length=42)
        )


@pytest.mark.django_db
def test_user_unique_email_ci(faker):
    email = faker.email()
    name, domain = email.split("@", 1)
    email_upper = f"{name.upper()}@{domain}"
    email_lower = f"{name.lower()}@{domain}"
    models.TeamUser.objects.create_user(
        email=email_upper, password=faker.password(length=64)
    )  # nosec
    with pytest.raises(IntegrityError):
        models.TeamUser.objects.create_superuser(  # nosec
            email=email_lower, password=faker.password(length=42)
        )


@pytest.mark.django_db
@pytest.mark.parametrize(
    "raises_exc,attrs",
    [(ValueError, {"is_staff": False}), (ValueError, {"is_superuser": False})],
    ids=["not_staff", "not_superuser"],
)
def test_create_superuser_invalid_attributes(faker, raises_exc, attrs):
    with pytest.raises(raises_exc):
        models.TeamUser.objects.create_superuser(  # nosec
            email=faker.email(), password=faker.password(length=42), is_staff=False
        )


@pytest.mark.django_db
def test_create_superuser_is_superuser(faker):
    with pytest.raises(ValueError):
        models.TeamUser.objects.create_superuser(  # nosec
            email=faker.email(), password=faker.password(length=42), is_superuser=False
        )
