from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("projects/", views.portfolio, name="portfolio"),
]
