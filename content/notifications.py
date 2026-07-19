"""Email notifications.

Owner is alerted on new comments / reviews; newsletter subscribers are alerted
on newly published posts. All emails are sent as multipart (plain-text +
styled HTML) using the shared templates under ``templates/emails/``.
"""
import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import gettext as _

logger = logging.getLogger(__name__)


def _send(subject, text_body, html_body=None, recipients=None, bcc=None):
    """Send one multipart email. ``recipients`` defaults to the owner list."""
    to = recipients if recipients is not None else getattr(settings, "NOTIFY_EMAILS", [])
    if not to and not bcc:
        return
    try:
        msg = EmailMultiAlternatives(
            subject=subject.strip(),
            body=text_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=to or [settings.DEFAULT_FROM_EMAIL],
            bcc=bcc or None,
        )
        if html_body:
            msg.attach_alternative(html_body, "text/html")
        msg.send(fail_silently=True)
    except Exception:  # never let a notification break the request
        logger.exception("Failed to send notification email")


def _stamp():
    return timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S %Z")


def _site_url():
    return settings.SITE_URL.rstrip("/")


def notify_new_comment(comment):
    target = comment.target
    kind = _("reply") if comment.is_reply else _("comment")
    url = (
        f"{_site_url()}{target.get_absolute_url()}#comments" if target else settings.SITE_URL
    )
    ctx = {
        "comment": comment,
        "kind": kind,
        "target": target,
        "url": url,
        "stamp": _stamp(),
        "site_url": _site_url(),
    }
    subject = "[thedevu101] " + _("New %(kind)s from %(name)s") % {
        "kind": kind, "name": comment.author.display_name,
    }
    text = (
        _("A new %(kind)s was posted.") % {"kind": kind} + "\n\n"
        f"{_('From')}: {comment.author.display_name} ({comment.author.email or '—'})\n"
        f"{_('On')}: {target}\n"
        f"{_('When')}: {ctx['stamp']}\n\n"
        f"{comment.body}\n\n{url}\n"
    )
    html = render_to_string("emails/new_comment.html", ctx)
    _send(subject, text, html)


def notify_new_review(review):
    stars = "★" * review.rate + "☆" * (5 - review.rate)
    admin_url = f"{_site_url()}/admin/app_users/review/"
    ctx = {
        "review": review,
        "stars": stars,
        "stamp": _stamp(),
        "admin_url": admin_url,
        "site_url": _site_url(),
    }
    subject = "[thedevu101] " + _("New review from %(name)s (%(rate)s/5)") % {
        "name": review.user.display_name, "rate": review.rate,
    }
    text = (
        _("A new review was submitted and is awaiting approval.") + "\n\n"
        f"{_('From')}: {review.user.display_name} ({review.user.email or '—'})\n"
        f"{_('Location')}: {review.address}\n"
        f"{_('Rating')}: {review.rate}/5\n"
        f"{_('When')}: {ctx['stamp']}\n\n"
        f"{review.body}\n\n{admin_url}\n"
    )
    html = render_to_string("emails/new_review.html", ctx)
    _send(subject, text, html)


def notify_new_post(post):
    """Email newsletter subscribers about a newly published post."""
    User = get_user_model()
    emails = list(
        User.objects.filter(newsletter=True, is_active=True)
        .exclude(email="")
        .values_list("email", flat=True)
    )
    if not emails:
        return
    url = f"{_site_url()}{post.get_absolute_url()}"
    profile_url = f"{_site_url()}/users/profile/"
    ctx = {
        "post": post,
        "url": url,
        "profile_url": profile_url,
        "site_url": _site_url(),
    }
    subject = "[thedevu101] " + _("New post: %(title)s") % {"title": post.title}
    text = (
        _("A new post was just published:") + f"\n\n{post.title}\n\n"
        f"{post.summary}\n\n{url}\n"
    )
    html = render_to_string("emails/new_post.html", ctx)
    # BCC subscribers so their addresses stay private.
    _send(subject, text, html, recipients=[], bcc=emails)
