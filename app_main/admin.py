from django.contrib import admin

from modeltranslation.admin import TabbedTranslationAdmin

from .models import Job, Project


@admin.register(Project)
class ProjectAdmin(TabbedTranslationAdmin):
    list_display = ("title", "is_featured", "order", "created")
    list_editable = ("is_featured", "order")
    search_fields = ("title", "description")


@admin.register(Job)
class JobAdmin(TabbedTranslationAdmin):
    list_display = ("company", "start_date", "end_date", "is_current", "order")
    list_editable = ("is_current", "order")
    list_filter = ("is_current",)
    search_fields = ("company", "responsibilities")
