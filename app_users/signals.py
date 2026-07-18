from django.db.models.signals import post_save
from django.dispatch import receiver

from content.notifications import notify_new_review

from .models import Review


@receiver(post_save, sender=Review)
def review_created(sender, instance, created, **kwargs):
    if created:
        notify_new_review(instance)
