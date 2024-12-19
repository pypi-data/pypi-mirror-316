import pytest
from django.conf import settings
from django.test import Client, RequestFactory
from django.urls import reverse
from django.utils import timezone

from sage_timezone.views.timezone import TimezoneSelectionView


class TestTimezoneSelectionView:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.factory = RequestFactory()
        self.view = TimezoneSelectionView.as_view()
        self.client = Client()

    def test_get_request_renders_form(self):
        request = self.factory.get(reverse("timezone_select_view"))
        request.session = {}
        response = self.view(request)

        assert response.status_code == 200

    def test_post_request_valid_timezone(self):
        request = self.factory.post(
            reverse("timezone_select_view"), {"timezone": "Europe/London"}
        )
        request.session = {}

        response = self.view(request)
        name = getattr(settings, "TIME_ZONE_SESSION_NAME", "user_timezone")

        assert request.session[name] == "Europe/London"
        assert timezone.get_current_timezone_name() == "Europe/London"
        assert response.status_code == 302
        assert response.url == "/"

    def test_post_request_invalid_timezone(self):
        # Test that an invalid timezone does not set the session and redirects correctly
        request = self.factory.post(
            reverse("timezone_select_view"), {"timezone": "Invalid/Timezone"}
        )
        request.session = {}
        response = self.view(request)

        assert "user_timezone" not in request.session
        assert timezone.get_current_timezone_name() == settings.TIME_ZONE
        assert response.status_code == 302
        assert response.url == "/"

    def test_post_request_without_timezone(self):
        # Test that a missing timezone does not set the session and redirects correctly
        request = self.factory.post(reverse("timezone_select_view"), {"timezone": ""})
        request.session = {}

        response = self.view(request)
        name = getattr(settings, "TIME_ZONE_SESSION_NAME", "user_timezone")

        assert name not in request.session
        assert timezone.get_current_timezone_name() == settings.TIME_ZONE
        assert response.status_code == 302
        assert response.url == "/"

    def test_post_request_redirects_to_referer(self):
        # Test that the view redirects back to the referring URL if available
        referer_url = "/some/random/url/"
        request = self.factory.post(
            reverse("timezone_select_view"),
            {"timezone": "Europe/London"},
            HTTP_REFERER=referer_url,
        )
        request.session = {}

        response = self.view(request)

        assert response.status_code == 302
        assert response.url == referer_url

    def test_post_request_no_referer_fallback(self):
        # Test that the view falls back to /admin/ if no referer is provided
        request = self.factory.post(
            reverse("timezone_select_view"), {"timezone": "Europe/London"}
        )
        request.session = {}

        response = self.view(request)

        assert response.status_code == 302
        assert response.url == "/"
