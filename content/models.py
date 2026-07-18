import math
import re
import uuid

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from django_ckeditor_5.fields import CKEditor5Field


def poster_upload_to(instance, filename):
    """Store posters under post-posters/ or news-posters/ by model."""
    return f"{instance._meta.model_name}-posters/{filename}"


class Tag(models.Model):
    """A topic tag. `name` and `slug` are translatable (see translation.py)."""

    name = models.CharField(_("name"), max_length=64)
    slug = models.SlugField(_("slug"), max_length=80, blank=True)

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("name",)
        verbose_name = _("tag")
        verbose_name_plural = _("tags")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Entry(models.Model):
    """Shared base for Posts and News.

    Concrete subclasses only differ in their URLs and admin section, but they
    are stored in separate tables (two distinct models, per project decision).
    """

    title = models.CharField(_("title"), max_length=255)
    slug = models.SlugField(_("slug"), max_length=255, blank=True, db_index=True)
    excerpt = models.CharField(
        _("excerpt"), max_length=300, blank=True,
        help_text=_("Short summary shown in listings and link previews."),
    )
    body = CKEditor5Field(_("body"), config_name="extends")

    poster = models.ImageField(
        _("poster image"), upload_to=poster_upload_to,
        help_text=_("Shown as the preview image when the link is shared."),
    )

    meta_description = models.CharField(
        _("meta description"), max_length=160, blank=True,
        help_text=_("Up to 160 chars for search engines. Falls back to excerpt."),
    )

    tags = models.ManyToManyField(Tag, blank=True, related_name="%(class)ss")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="%(class)ss",
    )

    is_published = models.BooleanField(_("published"), default=False)
    published_at = models.DateTimeField(_("published at"), null=True, blank=True)
    views = models.PositiveIntegerField(default=0, editable=False)

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ("-published_at", "-created")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=False)
        if self.is_published and self.published_at is None:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    @property
    def reading_time(self):
        """Rough reading time in minutes based on body word count."""
        words = len(re.sub(r"<[^>]+>", " ", self.body or "").split())
        return max(1, math.ceil(words / 200))

    @property
    def summary(self):
        return self.excerpt or self.meta_description

    def __str__(self):
        return self.title


class Post(Entry):
    class Meta(Entry.Meta):
        verbose_name = _("post")
        verbose_name_plural = _("posts")

    def get_absolute_url(self):
        return reverse("content:post_detail", kwargs={"slug": self.slug})


class News(Entry):
    class Meta(Entry.Meta):
        verbose_name = _("news item")
        verbose_name_plural = _("news")

    def get_absolute_url(self):
        return reverse("content:news_detail", kwargs={"slug": self.slug})


class Comment(models.Model):
    """A comment on a Post or News item.

    Exactly one of `post` / `news` is set. `parent` gives threaded replies
    (reply-to-reply). Only authenticated users may comment; comments appear
    immediately and can be deleted in-page by the site owner.
    """

    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, null=True, blank=True, related_name="comments",
    )
    news = models.ForeignKey(
        News, on_delete=models.CASCADE, null=True, blank=True, related_name="comments",
    )
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments",
    )
    body = models.TextField(_("comment"), max_length=3000)

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("created",)
        verbose_name = _("comment")
        verbose_name_plural = _("comments")

    @property
    def target(self):
        """The Post or News item this comment belongs to."""
        return self.post or self.news

    @property
    def is_reply(self):
        return self.parent_id is not None

    def __str__(self):
        who = self.author.display_name if self.author_id else "?"
        return f"{who}: {self.body[:40]}"
