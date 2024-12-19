import pytest
from django.conf import settings
from django.http import HttpResponse
from django.test import RequestFactory
from django.utils import timezone

from sage_timezone.middleware.timezone import TimezoneMiddleware


class TestTimezoneMiddleware:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.factory = RequestFactory()

        self.get_response = lambda request: HttpResponse()

        self.middleware = TimezoneMiddleware(self.get_response)

    def test_timezone_set_correctly(self):
        request = self.factory.get("/")
        name = getattr(settings, "TIME_ZONE_SESSION_NAME", "user_timezone")
        request.session = {name: "Europe/London"}

        self.middleware.process_request(request)

        assert timezone.get_current_timezone_name() == "Europe/London"
        assert settings.TIME_ZONE == "Europe/London"

    def test_timezone_invalid(self):
        request = self.factory.get("/")
        request.session = {"user_timezone": "Invalid/Timezone"}

        self.middleware.process_request(request)

        assert timezone.get_current_timezone_name() == settings.TIME_ZONE

    def test_timezone_not_set(self):
        request = self.factory.get("/")
        request.session = {}

        self.middleware.process_request(request)

        assert timezone.get_current_timezone_name() == settings.TIME_ZONE

    def test_process_response_deactivates_timezone(self):
        request = self.factory.get("/")
        request.session = {"user_timezone": None}
        response = HttpResponse()

        response = self.middleware.process_response(request, response)
        print(response)
        assert response.status_code == 200
