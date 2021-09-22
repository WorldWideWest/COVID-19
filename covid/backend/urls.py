from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from .views import CovidDataView, MetricsView

urlpatterns = [
    path('api/', CovidDataView.as_view(), name = "api"),
    path('metrics-api/', MetricsView.as_view(), name = "metrics"),
]

urlpatterns = format_suffix_patterns(urlpatterns)