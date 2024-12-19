import pytz
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views import View

from sage_timezone.forms.timezone import TimezoneForm


class TimezoneSelectionView(View):
    """View to render the timezone selection page and handle POST requests."""

    def get(self, request: HttpRequest) -> HttpResponse:
        form = TimezoneForm()
        timezones = pytz.all_timezones
        print(timezones)
        return render(
            request,
            "admin/timezone_selection.html",
            {
                "form": form,
                "timezones": timezones,
            },
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        tzname = request.POST.get("timezone")
        if tzname in pytz.all_timezones:
            name = getattr(settings, "TIME_ZONE_SESSION_NAME", "user_timezone")
            request.session[name] = tzname
            print(f"Timezone set to: {request.session[name]}")
            timezone.activate(pytz.timezone(tzname))

        referer_url = request.META.get("HTTP_REFERER", "/")
        return redirect(referer_url)
