import pytz
from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def get_session_value(request, key):
    """Retrieves the value from the session for the given key."""
    name = getattr(settings, "TIME_ZONE_SESSION_NAME", "user_timezone")
    return request.session.get(name, "Default")


@register.simple_tag
def get_timezones():
    """Returns a list of all available timezones."""
    return pytz.all_timezones
