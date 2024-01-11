import zoneinfo

from django.utils import timezone


class TimezoneMiddleware:  # pylint: disable=too-few-public-methods
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if tzname := request.session.get("django_timezone"):
            timezone.activate(zoneinfo.ZoneInfo(tzname))
        elif request.user.is_authenticated and request.user.timezone is not None:
            timezone.activate(request.user.timezone)
            request.session["django_timezone"] = str(request.user.timezone)
        else:
            timezone.activate(zoneinfo.ZoneInfo("Australia/Brisbane"))
        return self.get_response(request)
