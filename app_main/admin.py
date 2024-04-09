from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from django import forms

from . import models


admin.site.register(models.Project)
admin.site.register(models.Tag)


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ['title'],
    }
