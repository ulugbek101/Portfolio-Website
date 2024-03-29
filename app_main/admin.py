from django.contrib import admin

from . import models


admin.site.register(models.Project)
admin.site.register(models.Tag)


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ['title'],
    }
