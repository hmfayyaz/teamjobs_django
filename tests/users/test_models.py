from hypothesis import given
from hypothesis.extra import django

from users import models


class TeamUserModelTestCase(django.TestCase):
    @given(django.from_model(models.TeamUser))
    def test_teamuser_save(self, instance: models.TeamUser) -> None:
        instance.save()
        assert instance.pk != 0

    @given(django.from_model(models.TeamUser))
    def test_teamuser_str(self, instance: models.TeamUser) -> None:
        instance.save()
        assert isinstance(str(instance), str)
