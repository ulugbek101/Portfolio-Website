from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from . import views

urlpatterns = [
    path('create_review/', views.create_review, name='create_review'),
    path('download-cv/', views.download_cv, name='download_cv'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),

    # Password reset flow (custom templates under app_users/password_reset/).
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='app_users/password_reset/form.html',
            email_template_name='app_users/password_reset/email.txt',
            html_email_template_name='app_users/password_reset/email.html',
            subject_template_name='app_users/password_reset/subject.txt',
            success_url=reverse_lazy('password_reset_done'),
        ),
        name='password_reset',
    ),
    path(
        'password-reset/sent/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='app_users/password_reset/done.html',
        ),
        name='password_reset_done',
    ),
    path(
        'password-reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='app_users/password_reset/confirm.html',
            success_url=reverse_lazy('password_reset_complete'),
        ),
        name='password_reset_confirm',
    ),
    path(
        'password-reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='app_users/password_reset/complete.html',
        ),
        name='password_reset_complete',
    ),
]
