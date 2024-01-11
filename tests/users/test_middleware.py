import zoneinfo

import pytest
from django.utils import timezone


class TestTimezoneMiddleware:
    @pytest.fixture
    def tzname(self):
        yield "Australia/Melbourne"

    @pytest.fixture
    def tz(self, tzname):
        yield zoneinfo.ZoneInfo(tzname)

    @pytest.fixture
    def user_tz(self, user_factory, tz):
        yield user_factory(timezone=tz)

    @pytest.mark.django_db
    def test_timezone_middleware_user_sets_session_tz(self, settings, user_tz, client):
        settings.TIME_ZONE = "UTC"
        client.force_login(user_tz)
        _ = client.get("/admin/")
        assert client.session["django_timezone"] == str(user_tz.timezone)

    @pytest.mark.django_db
    def test_timezone_middleware_user_activates_tz(self, settings, user_tz, client):
        settings.TIME_ZONE = "UTC"
        client.force_login(user_tz)
        _ = client.get("/admin/")
        assert timezone.get_current_timezone() == user_tz.timezone

    def test_timezone_middleware_default_activates_tz(self, settings, client):
        settings.TIME_ZONE = "UTC"
        _ = client.get("/admin/")
        assert timezone.get_current_timezone() == zoneinfo.ZoneInfo(
            "Australia/Brisbane"
        )

    def test_timezone_middleware_activate_from_session(self, settings, client, tzname):
        settings.TIME_ZONE = "UTC"
        session = client.session  # needed to save to session
        session["django_timezone"] = tzname
        session.save()
        _ = client.get("/admin/")
        assert timezone.get_current_timezone() == zoneinfo.ZoneInfo(tzname)
