import json

from django.conf import settings
from django.shortcuts import render

from .challenge_texts import OG, SEO, TEXTS

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
    return render(request, "twelve_day_challenge.html", {
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
        "copy_msgs": {k: t[k] for k in ("copiedNumber", "copiedName", "copyFail")},
    })
