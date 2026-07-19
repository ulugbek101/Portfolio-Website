import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext


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


class Job(models.Model):
    """A position in the work-history timeline (newest first)."""

    company = models.CharField(_("company"), max_length=255)
    logo = models.ImageField(
        _("logo"), upload_to="job-logos/", null=True, blank=True,
        help_text=_("Shown as a round avatar."),
    )
    responsibilities = models.TextField(
        _("responsibilities"),
        help_text=_("What you did here — one item per line is rendered as a list."),
    )
    start_date = models.DateField(_("worked from"))
    end_date = models.DateField(
        _("worked until"), null=True, blank=True,
        help_text=_("Leave empty and tick “currently working here” for an ongoing job."),
    )
    is_current = models.BooleanField(
        _("currently working here"), default=False,
        help_text=_("Ongoing — the end date is treated as today when computing duration."),
    )
    order = models.PositiveIntegerField(
        _("order"), default=0,
        help_text=_("Lower numbers appear first. Ties fall back to newest start date."),
    )

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("order", "-start_date")
        verbose_name = _("job")
        verbose_name_plural = _("work history")

    @property
    def effective_end(self):
        """Actual end date, or today for an ongoing position."""
        if self.is_current or not self.end_date:
            return timezone.localdate()
        return self.end_date

    @property
    def duration(self):
        """Human, translated span like “4 years 3 months”."""
        start, end = self.start_date, self.effective_end
        if not start:
            return ""
        months = (end.year - start.year) * 12 + (end.month - start.month)
        if end.day < start.day:
            months -= 1
        months = max(months, 0)
        years, months = divmod(months, 12)
        parts = []
        if years:
            parts.append(ngettext("%(n)d year", "%(n)d years", years) % {"n": years})
        if months:
            parts.append(ngettext("%(n)d month", "%(n)d months", months) % {"n": months})
        if not parts:
            parts.append(_("Less than a month"))
        return " ".join(parts)

    def __str__(self):
        end = _("present") if self.is_current else (self.end_date or "—")
        return f"{self.company} ({self.start_date} – {end})"
