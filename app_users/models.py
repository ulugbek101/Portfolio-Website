import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Review(models.Model):
    """A testimonial left by a signed-in visitor.

    Hidden from the public site until the owner sets `approved = True`.
    """

    RATE_CHOICES = [(i, str(i)) for i in range(1, 6)]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="reviews",
    )
    address = models.CharField(_("address"), max_length=255)
    profile_photo = models.ImageField(
        _("profile photo"), upload_to="profile-photos/", null=True, blank=True,
        help_text=_("Optional — falls back to your account avatar."),
    )
    country_flag = models.ImageField(
        _("country flag"), null=True, blank=True, upload_to="country-flags/",
    )
    rate = models.IntegerField(_("rating"), choices=RATE_CHOICES, default=5)
    body = models.TextField(_("review"))
    approved = models.BooleanField(_("approved"), default=False)

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created"]
        verbose_name = _("review")
        verbose_name_plural = _("reviews")

    @property
    def photo_url(self):
        if self.profile_photo:
            return self.profile_photo.url
        if getattr(self.user, "avatar", None):
            return self.user.avatar.url
        return ""

    def __str__(self):
        return f"{self.user.display_name} - {self.body[:30]}"
