from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('create_review/', views.create_review, name='create_review'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('social-auth/', include('social_django.urls', namespace='social')),
]
