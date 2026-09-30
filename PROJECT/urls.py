from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from app_main.challenge_views import twelve_day_challenge
from app_main.i18n_views import set_language
from app_main.seo_views import robots_txt
from content.sitemaps import sitemaps


# Non-translated URLs (admin, editor, i18n switcher, OAuth callbacks, SEO).
# OAuth callbacks must stay unprefixed so provider redirect URIs stay stable.
urlpatterns = [
    path("twelve-day-challenge/", twelve_day_challenge, {"lang": "ru"}, name="twelve_day_challenge"),
    path("twelve-day-challenge/uz/", twelve_day_challenge, {"lang": "uz"}, name="twelve_day_challenge_uz"),
    path("admin/", admin.site.urls),
    path("ckeditor5/", include("django_ckeditor_5.urls")),
    path("i18n/setlang/", set_language, name="set_language"),
    path("i18n/", include("django.conf.urls.i18n")),
    path("users/social-auth/", include("social_django.urls", namespace="social")),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    path("robots.txt", robots_txt, name="robots_txt"),
]

# Translated URLs. Uzbek is the default and carries no prefix; Russian and
# English are served under /ru/ and /en/. The user-facing auth pages live here
# too so the language switcher works on login/register/profile/reset pages.
urlpatterns += i18n_patterns(
    path("users/", include("app_users.urls")),
    path("", include("app_main.urls")),
    path("", include("content.urls")),
    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
