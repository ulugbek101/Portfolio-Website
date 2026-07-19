from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Comment, Post
from .notifications import notify_new_comment, notify_new_post


@receiver(post_save, sender=Comment)
def comment_created(sender, instance, created, **kwargs):
    if created:
        notify_new_comment(instance)


@receiver(post_save, sender=Post)
def post_published(sender, instance, created, **kwargs):
    """Email newsletter subscribers the first time a post becomes published."""
    if instance.is_published and not instance.newsletter_sent:
        notify_new_post(instance)
        # Mark as sent without re-triggering this signal.
        Post.objects.filter(pk=instance.pk).update(newsletter_sent=True)
