from django.urls import path

from sage_timezone.views.timezone import TimezoneSelectionView

urlpatterns = [
    path("time-zone/", TimezoneSelectionView.as_view(), name="timezone_select_view"),
]
