import json
import logging
import re

from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .challenge_texts import OG, SEO, TEXTS
from .notifications import send_callback_request

logger = logging.getLogger(__name__)

PATHS = {"ru": "/twelve-day-challenge/", "uz": "/twelve-day-challenge/uz/"}
IMAGE_PATH = "/media/hair-style-og.jpg"


def twelve_day_challenge(request, lang="ru"):
    site = settings.SITE_URL.rstrip("/")
    t = TEXTS[lang]
    seo = SEO[lang]
    json_ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebSite",
                "@id": f"{site}{PATHS['ru']}#website",
                "url": f"{site}{PATHS['ru']}",
                "name": "Stylist Challenge",
                "inLanguage": ["ru", "uz"],
            },
            {
                "@type": "Course",
                "name": seo["title"],
                "description": seo["json_desc"],
                "provider": {"@type": "Organization", "name": "Stylist Challenge", "url": f"{site}{PATHS['ru']}"},
                "inLanguage": lang,
                "image": f"{site}{IMAGE_PATH}",
                "url": f"{site}{PATHS[lang]}",
                "timeRequired": "P12D",
                "courseMode": "online",
                "keywords": seo["keywords"],
            },
        ],
    }
    response = render(request, "twelve_day_challenge.html", {
        "lang": lang,
        "t": t,
        "seo": seo,
        "og": OG,
        "url_ru": PATHS["ru"],
        "url_uz": PATHS["uz"],
        "abs_ru": site + PATHS["ru"],
        "abs_uz": site + PATHS["uz"],
        "canonical": site + PATHS[lang],
        "image_url": site + IMAGE_PATH,
        "json_ld": json.dumps(json_ld, ensure_ascii=False).replace("</", "<\\/"),
        "copy_msgs": {
            k: t[k]
            for k in (
                "copiedNumber", "copiedName", "copyFail",
                "formSending", "formSuccess", "formInvalid", "formError", "formTooMany",
            )
        },
    })
    # Django's default COOP "same-origin" cuts window.opener, which Meta's
    # Events Setup tool needs to detect the pixel. SecurityMiddleware keeps a
    # header a view has already set, so this only affects this page.
    response["Cross-Origin-Opener-Policy"] = "unsafe-none"
    return response


PHONE_RE = re.compile(r"^\+?[\d\s().-]{7,25}$")
RATE_LIMIT = 5          # requests ...
RATE_WINDOW = 10 * 60   # ... per this many seconds, per client IP


def _client_ip(request):
    # nginx overwrites X-Real-IP, so it can't be spoofed by the client.
    return request.META.get("HTTP_X_REAL_IP") or request.META.get("REMOTE_ADDR", "")


@require_POST
def challenge_callback(request):
    # Honeypot: real visitors never fill this hidden field.
    if request.POST.get("website"):
        return JsonResponse({"ok": True})

    lang = "uz" if request.POST.get("lang") == "uz" else "ru"
    name = " ".join(request.POST.get("name", "").split())
    phone = " ".join(request.POST.get("phone", "").split())
    digits = re.sub(r"\D", "", phone)

    if not (2 <= len(name) <= 100) or not PHONE_RE.match(phone) or not (7 <= len(digits) <= 15):
        return JsonResponse({"ok": False, "error": "invalid"}, status=400)

    key = f"challenge-callback:{_client_ip(request)}"
    cache.add(key, 0, RATE_WINDOW)
    try:
        hits = cache.incr(key)
    except ValueError:
        hits = 1
    if hits > RATE_LIMIT:
        return JsonResponse({"ok": False, "error": "too_many"}, status=429)

    submitted_at = timezone.localtime().strftime("%d.%m.%Y %H:%M")
    try:
        result = send_callback_request(name, phone, lang, submitted_at)
    except Exception:
        logger.exception("Callback request could not be sent")
        result = {"sent": 0}
    # Reaching at least one admin counts as success; otherwise let the visitor
    # know so the request is not silently lost.
    if not result["sent"]:
        return JsonResponse({"ok": False, "error": "send_failed"}, status=502)
    return JsonResponse({"ok": True})
