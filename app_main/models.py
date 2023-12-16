import uuid
from django.db import models

from ckeditor.fields import RichTextField


class Project(models.Model):
    title = models.CharField(max_length=255, unique=True)
    link = models.URLField(max_length=255)
    description = models.TextField(null=True, blank=True)
    photo = models.ImageField(upload_to='thedevu101-media/projects')

    id = models.UUIDField(default=uuid.uuid4, editable=False,
                          primary_key=True, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, null=True)
    body = RichTextField()
    requests = models.IntegerField(default=0)

    id = models.UUIDField(default=uuid.uuid4, editable=False,
                          primary_key=True, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title[:50]} ..."

    class Meta:
        ordering = ("requests", "created")

