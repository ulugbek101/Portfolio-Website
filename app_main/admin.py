from django.contrib import admin

from modeltranslation.admin import TabbedTranslationAdmin

from .models import Project


@admin.register(Project)
class ProjectAdmin(TabbedTranslationAdmin):
    list_display = ("title", "is_featured", "order", "created")
    list_editable = ("is_featured", "order")
    search_fields = ("title", "description")
