"""Translation markers for strings Django itself emits.

Django ships an *empty* Uzbek catalog for its password-validator messages, so
they fall back to English on our Uzbek pages. Re-declaring the exact msgids
here (via no-op gettext calls) makes ``makemessages`` keep them in our project
catalog, where we provide the Uzbek translations. This module is never
imported at runtime — it exists only so ``makemessages`` can extract it.
"""
from django.utils.translation import gettext_noop, ngettext

gettext_noop("Your password can’t be too similar to your other personal information.")
gettext_noop("Your password can’t be a commonly used password.")
gettext_noop("This password is too common.")
gettext_noop("Your password can’t be entirely numeric.")
gettext_noop("This password is entirely numeric.")
gettext_noop("The password is too similar to the %(verbose_name)s.")


def _mark_plurals():  # pragma: no cover - never called
    ngettext(
        "This password is too short. It must contain at least %(min_length)d character.",
        "This password is too short. It must contain at least %(min_length)d characters.",
        0,
    )
    ngettext(
        "Your password must contain at least %(min_length)d character.",
        "Your password must contain at least %(min_length)d characters.",
        0,
    )
