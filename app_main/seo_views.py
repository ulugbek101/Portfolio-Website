from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.cache import cache_control


@cache_control(max_age=86400)
def robots_txt(request):
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "Disallow: /users/social-auth/",
        "",
        f"Sitemap: {settings.SITE_URL.rstrip('/')}/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
