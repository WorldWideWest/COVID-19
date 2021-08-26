from django.urls import path
from .views import analysis_view, about_view

urlpatterns = [
    path("", analysis_view, name = "analysis"),
    path("about", about_view, name = "about"),
]