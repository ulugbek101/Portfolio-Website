from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from app_main.seo_views import robots_txt
from content.sitemaps import sitemaps

# Non-translated URLs (admin, editor, auth machinery, i18n switcher, SEO).
urlpatterns = [
    path("admin/", admin.site.urls),
    path("ckeditor5/", include("django_ckeditor_5.urls")),
    path("i18n/", include("django.conf.urls.i18n")),
    path("users/", include("app_users.urls")),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    path("robots.txt", robots_txt, name="robots_txt"),
]

# Translated URLs. Uzbek is the default and carries no prefix; Russian and
# English are served under /ru/ and /en/.
urlpatterns += i18n_patterns(
    path("", include("app_main.urls")),
    path("", include("content.urls")),
    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
