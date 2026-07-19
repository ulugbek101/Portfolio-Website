from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("projects/", views.portfolio, name="portfolio"),
    path("work/", views.work_history, name="work_history"),
]
