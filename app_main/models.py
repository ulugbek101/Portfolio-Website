import uuid
from django.db import models
from django.urls import reverse

from django_ckeditor_5.fields import CKEditor5Field


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


class Tag(models.Model):
    name = models.CharField(max_length=255)

    id = models.UUIDField(default=uuid.uuid4, editable=False,
                          primary_key=True, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, null=True)
<<<<<<< HEAD
    tags = models.ManyToManyField(Tag)
    body = CKEditor5Field(config_name="extends")
=======
    tags = models.ManyToManyField(Tag, blank=True)
    body = RichTextField()
>>>>>>> 6d1cd843a1ac22523c0dbe937ec5eaf39a8b9078
    requests = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    id = models.UUIDField(default=uuid.uuid4, editable=False,
                          primary_key=True, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('post', kwargs={"slug": self.slug})

    def __str__(self):
        return f"{self.title[:50]} ..."

    class Meta:
        ordering = ("created", "requests")
