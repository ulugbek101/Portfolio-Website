from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from modeltranslation.admin import TabbedTranslationAdmin

from .models import Comment, News, Post, Tag


@admin.register(Tag)
class TagAdmin(TabbedTranslationAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "slug")
    # modeltranslation's admin expands this to slug_uz <- title_uz, etc.
    prepopulated_fields = {"slug": ("name",)}


class PostTagInline(admin.TabularInline):
    """Assign tags inline on the entry page — and create new ones on the fly
    via the '+' button next to the tag picker."""

    model = Post.tags.through
    extra = 1
    autocomplete_fields = ("tag",)
    verbose_name = _("tag")
    verbose_name_plural = _("tags")


class NewsTagInline(PostTagInline):
    model = News.tags.through


class EntryAdmin(TabbedTranslationAdmin):
    list_display = ("title", "is_published", "published_at", "views", "created")
    list_filter = ("is_published", "created", "tags")
    date_hierarchy = "published_at"
    search_fields = ("title", "excerpt", "body")
    readonly_fields = ("views", "created", "updated")
    prepopulated_fields = {"slug": ("title",)}
    exclude = ("tags",)  # managed via the tabular inline instead
    fieldsets = (
        (None, {"fields": ("title", "slug", "excerpt", "body")}),
        (_("Media & SEO"), {"fields": ("poster", "meta_description")}),
        (_("Publishing"), {"fields": ("author", "is_published", "published_at", "views")}),
        (_("Timestamps"), {"classes": ("collapse",), "fields": ("created", "updated")}),
    )

    def save_model(self, request, obj, form, change):
        if obj.author_id is None:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Post)
class PostAdmin(EntryAdmin):
    inlines = (PostTagInline,)


@admin.register(News)
class NewsAdmin(EntryAdmin):
    inlines = (NewsTagInline,)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("__str__", "author", "target", "is_reply", "created")
    list_filter = ("created",)
    search_fields = ("body", "author__username")
    autocomplete_fields = ("author", "parent")
    readonly_fields = ("created", "updated")
