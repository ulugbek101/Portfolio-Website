from django.urls import path

from . import views

app_name = "content"

urlpatterns = [
    path("posts/", views.post_list, name="post_list"),
    path("news/", views.news_list, name="news_list"),

    path("posts/<slug:slug>/", views.post_detail, name="post_detail"),
    path("news/<slug:slug>/", views.news_detail, name="news_detail"),

    path("comment/<str:kind>/<uuid:pk>/", views.comment_create, name="comment_create"),
    path("comment/<uuid:pk>/delete/", views.comment_delete, name="comment_delete"),
]
