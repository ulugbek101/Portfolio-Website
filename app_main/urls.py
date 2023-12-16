from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('services/', views.services, name='services'),
    path('posts/', views.posts, name='posts'),
    path('post/<str:slug>/', views.post, name='post'),
]
