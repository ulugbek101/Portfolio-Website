from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Custom user model.

    Extends Django's AbstractUser so we can add profile attributes over time
    (avatar, headline, location, social handles, ...) without another painful
    migration of the user model down the line.
    """

    # A friendly avatar used across reviews and comments. Optional — social
    # logins may populate this later from the provider.
    avatar = models.ImageField(
        _("avatar"), upload_to="avatars/", null=True, blank=True,
    )
    headline = models.CharField(
        _("headline"), max_length=160, blank=True,
        help_text=_("Short professional headline, e.g. 'Backend Engineer'."),
    )
    location = models.CharField(_("location"), max_length=120, blank=True)
    newsletter = models.BooleanField(
        _("email newsletter"), default=True,
        help_text=_("Receive occasional email updates and newsletters."),
    )

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    @property
    def display_name(self):
        full = self.get_full_name()
        return full or self.username

    @property
    def initials(self):
        parts = [p for p in (self.first_name, self.last_name) if p]
        if parts:
            return "".join(p[0].upper() for p in parts)[:2]
        return (self.username[:1] or "?").upper()

    def __str__(self):
        return self.display_name
