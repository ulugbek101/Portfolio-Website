from modeltranslation.translator import TranslationOptions, register

from .models import News, Post, Tag


@register(Tag)
class TagTranslationOptions(TranslationOptions):
    fields = ("name", "slug")


@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ("title", "slug", "excerpt", "body", "meta_description")


@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ("title", "slug", "excerpt", "body", "meta_description")
