import faker
from factory import Faker, post_generation
from factory.django import DjangoModelFactory

from users.models import TeamUser


# noinspection PyUnresolvedReferences
class UserFactory(DjangoModelFactory):
    first_name: Faker = Faker("first_name")
    last_name: Faker = Faker("first_name")
    email: Faker = Faker("email")
    phone: Faker = Faker("phone_number", locale="en-AU")
    timezone: Faker = Faker("timezone")
    is_staff = False
    is_superuser = False

    @post_generation
    def password(obj: TeamUser, create: bool, extracted: str | None, **kwargs) -> None:
        password: str | None = (
            extracted
            if extracted
            else faker.Faker().password(
                length=42,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            )
        )
        obj.set_password(password)

    class Meta:
        model = TeamUser
        django_get_or_create = ["email"]
