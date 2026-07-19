from modeltranslation.translator import TranslationOptions, register

from .models import Job, Project


@register(Project)
class ProjectTranslationOptions(TranslationOptions):
    fields = ("title", "description")


@register(Job)
class JobTranslationOptions(TranslationOptions):
    fields = ("company", "responsibilities")
