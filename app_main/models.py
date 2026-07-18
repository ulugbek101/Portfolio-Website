import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Project(models.Model):
    """A portfolio project / achievement to showcase."""

    title = models.CharField(_("title"), max_length=255, unique=True)
    link = models.URLField(_("link"), max_length=255, blank=True)
    description = models.TextField(_("description"), null=True, blank=True)
    photo = models.ImageField(_("photo"), upload_to="project-photos/")

    is_featured = models.BooleanField(_("featured"), default=False)
    order = models.PositiveIntegerField(_("order"), default=0)

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("order", "-created")
        verbose_name = _("project")
        verbose_name_plural = _("projects")

    def __str__(self):
        return self.title
