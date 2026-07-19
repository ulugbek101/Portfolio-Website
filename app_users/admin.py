from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("__str__", "rate", "order", "approved", "created")
    list_filter = ("approved", "rate", "created")
    list_editable = ("order", "approved")
    search_fields = ("user__username", "user__first_name", "user__last_name", "body", "address")
    actions = ("approve_selected", "unapprove_selected")

    @admin.action(description=_("Approve selected reviews"))
    def approve_selected(self, request, queryset):
        queryset.update(approved=True)

    @admin.action(description=_("Unapprove selected reviews"))
    def unapprove_selected(self, request, queryset):
        queryset.update(approved=False)
