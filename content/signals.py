from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Comment
from .notifications import notify_new_comment


@receiver(post_save, sender=Comment)
def comment_created(sender, instance, created, **kwargs):
    if created:
        notify_new_comment(instance)
