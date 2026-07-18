from django import template
from django.conf import settings
from django.urls import translate_url

register = template.Library()


@register.simple_tag(takes_context=True)
def alternate_links(context):
    """Return [{'code', 'url'}] absolute alternate URLs for each language.

    For pages whose path is the same across languages (home, lists, static),
    Django's translate_url swaps the language prefix correctly. Detail pages
    with translated slugs pass an explicit ``alternate_urls`` dict in context,
    which takes precedence.
    """
    request = context.get("request")
    explicit = context.get("alternate_urls")  # {'uz': '/...', 'ru': '/ru/...'}
    links = []
    for code, _name in settings.LANGUAGES:
        if explicit and code in explicit:
            path = explicit[code]
        elif request is not None:
            path = translate_url(request.get_full_path(), code)
        else:
            continue
        links.append({"code": code, "url": _absolute(path)})
    return links


@register.simple_tag(takes_context=True)
def canonical_url(context):
    explicit = context.get("canonical")
    if explicit:
        return _absolute(explicit)
    request = context.get("request")
    return _absolute(request.get_full_path()) if request else settings.SITE_URL


def _absolute(path):
    if path.startswith("http"):
        return path
    return f"{settings.SITE_URL.rstrip('/')}{path}"


@register.filter
def stars(rate):
    """Return a list [True, True, ..., False] of length 5 for star rendering."""
    rate = int(rate or 0)
    return [i < rate for i in range(5)]
