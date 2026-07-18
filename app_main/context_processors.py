from django.conf import settings


def site_meta(request):
    """Expose canonical site info to every template (for SEO / Open Graph)."""
    return {
        "SITE_URL": settings.SITE_URL,
        "SITE_DOMAIN": settings.SITE_DOMAIN,
    }
