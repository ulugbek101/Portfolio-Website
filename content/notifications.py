"""Email notifications to the owner when new comments / reviews arrive."""
import logging

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

logger = logging.getLogger(__name__)


def _send(subject, body):
    recipients = getattr(settings, "NOTIFY_EMAILS", [])
    if not recipients:
        return
    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipients,
            fail_silently=True,
        )
    except Exception:  # never let a notification break the request
        logger.exception("Failed to send notification email")


def _stamp():
    return timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S %Z")


def notify_new_comment(comment):
    target = comment.target
    kind = "reply" if comment.is_reply else "comment"
    url = f"{settings.SITE_URL.rstrip('/')}{target.get_absolute_url()}#comments" if target else settings.SITE_URL
    subject = f"[thedevu101] New {kind} from {comment.author.display_name}"
    body = (
        f"A new {kind} was posted.\n\n"
        f"From:     {comment.author.display_name} ({comment.author.email or 'no email'})\n"
        f"On:       {target}\n"
        f"When:     {_stamp()}\n\n"
        f"Comment:\n{comment.body}\n\n"
        f"View: {url}\n"
    )
    _send(subject, body)


def notify_new_review(review):
    subject = f"[thedevu101] New review from {review.user.display_name} ({review.rate}/5)"
    body = (
        f"A new review was submitted and is awaiting approval.\n\n"
        f"From:     {review.user.display_name} ({review.user.email or 'no email'})\n"
        f"Location: {review.address}\n"
        f"Rating:   {review.rate}/5\n"
        f"When:     {_stamp()}\n\n"
        f"Review:\n{review.body}\n\n"
        f"Approve it in the admin: {settings.SITE_URL.rstrip('/')}/admin/app_users/review/\n"
    )
    _send(subject, body)
