import pytz

from django import forms
from django.utils.translation import gettext_lazy as _


class TimezoneForm(forms.Form):
    """A form to allow users to select a timezone from a dropdown list."""

    timezone = forms.ChoiceField(
        choices=[(tz, tz) for tz in pytz.all_timezones], label=_("Select Timezone")
    )
