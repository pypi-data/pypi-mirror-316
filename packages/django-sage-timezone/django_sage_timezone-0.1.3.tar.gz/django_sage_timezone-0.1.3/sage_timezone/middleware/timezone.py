import logging
from typing import Any

from django.conf import settings
from django.http import HttpRequest
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

try:
    import pytz
except ImportError:
    raise ImportError("Install `pytz` package. Run `pip install pytz`.")  # noqa: B904


class TimezoneMiddleware(MiddlewareMixin):
    """Middleware to handle setting the user's timezone based on their session
    data.
    """

    def process_request(self, request: HttpRequest) -> None:
        name = getattr(settings, "TIME_ZONE_SESSION_NAME", "user_timezone")
        tzname = request.session.get(name)
        if tzname:
            try:
                timezone.activate(pytz.timezone(tzname))
                # Set Django's timezone to the user's timezone
                settings.TIME_ZONE = tzname
            except pytz.UnknownTimeZoneError:
                logger.error(f"Unknown timezone: {tzname}")
                timezone.deactivate()
        else:
            timezone.deactivate()

    def process_response(self, request: HttpRequest, response) -> Any:
        """Ensure the timezone is deactivated after the response is
        processed.
        """
        timezone.deactivate()
        return response
