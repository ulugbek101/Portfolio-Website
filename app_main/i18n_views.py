"""Language switching that works with ``prefix_default_language=False``.

Django's built-in :func:`django.views.i18n.set_language` cannot translate a
``next`` URL that already carries a language prefix (``/en/…``, ``/ru/…``).
The switcher POSTs to ``/i18n/setlang/``, which has no language prefix, and
because our ``i18n_patterns`` use ``prefix_default_language=False`` the
``LocaleMiddleware`` forces the active language back to ``settings.LANGUAGE_CODE``
(Uzbek) for that request. ``translate_url`` then tries to ``resolve`` the
prefixed ``next`` URL under the Uzbek URLconf (which has no ``/en/`` prefix),
fails, and returns the URL unchanged -- so once you are on ``/en/`` or ``/ru/``
you can never switch away.

This view fixes it by activating the *source* language (derived from the
``next`` URL's own prefix) before calling ``translate_url``, so the URL resolves
and reverses correctly for every language pair.
"""

from urllib.parse import urlsplit

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import translate_url
from django.utils import translation
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.translation import check_for_language, get_language_from_path


def set_language(request):
    """Set the language cookie and redirect, translating the ``next`` URL."""
    next_url = request.POST.get("next", request.GET.get("next"))
    if (
        next_url or request.accepts("text/html")
    ) and not url_has_allowed_host_and_scheme(
        url=next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        next_url = request.META.get("HTTP_REFERER")
        if not url_has_allowed_host_and_scheme(
            url=next_url,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        ):
            next_url = "/"

    response = HttpResponseRedirect(next_url) if next_url else HttpResponse(status=204)

    if request.method == "POST":
        lang_code = request.POST.get("language")
        if lang_code and check_for_language(lang_code):
            if next_url:
                # Activate the language the ``next`` URL is currently in so
                # that ``translate_url`` can resolve its prefixed path; without
                # this the LocaleMiddleware leaves the default language active
                # and prefixed URLs (/en/…, /ru/…) fail to resolve.
                source_lang = (
                    get_language_from_path(urlsplit(next_url).path)
                    or settings.LANGUAGE_CODE
                )
                with translation.override(source_lang):
                    next_trans = translate_url(next_url, lang_code)
                if next_trans != next_url:
                    response = HttpResponseRedirect(next_trans)
            response.set_cookie(
                settings.LANGUAGE_COOKIE_NAME,
                lang_code,
                max_age=settings.LANGUAGE_COOKIE_AGE,
                path=settings.LANGUAGE_COOKIE_PATH,
                domain=settings.LANGUAGE_COOKIE_DOMAIN,
                secure=settings.LANGUAGE_COOKIE_SECURE,
                httponly=settings.LANGUAGE_COOKIE_HTTPONLY,
                samesite=settings.LANGUAGE_COOKIE_SAMESITE,
            )

    return response
