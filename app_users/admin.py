from django.contrib import admin

from . import models

@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    # list_display_links = ['user']
    list_display = ['to_representation', 'verified']

