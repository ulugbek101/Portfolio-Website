from django.shortcuts import render
from django.utils.translation import gettext as _

from app_users.forms import ReviewForm
from app_users.models import Review
from content.models import News, Post

from .models import Job, Project


def index(request):
    context = {
        "featured_posts": Post.objects.filter(is_published=True)[:3],
        "latest_news": News.objects.filter(is_published=True)[:2],
        "projects": Project.objects.filter(is_featured=True)[:6],
        "reviews": Review.objects.filter(approved=True).select_related("user"),
        "review_form": ReviewForm(),
        "meta_title": _("Ulugbek Umaraliyev — Full-Stack Developer"),
        "meta_description": _(
            "Full-Stack developer with 5+ years of experience building web apps and "
            "Telegram bots. Projects, posts, news and reviews."
        ),
    }
    return render(request, "app_main/index.html", context)


def portfolio(request):
    context = {
        "projects": Project.objects.all(),
        "meta_title": _("Projects — Ulugbek Umaraliyev"),
        "meta_description": _("Web apps, Telegram bots and other projects built by Ulugbek Umaraliyev."),
    }
    return render(request, "app_main/portfolio.html", context)


def work_history(request):
    context = {
        "jobs": Job.objects.all(),
        "meta_title": _("Work history — Ulugbek Umaraliyev"),
        "meta_description": _("Work experience and career history of Full-Stack developer Ulugbek Umaraliyev."),
    }
    return render(request, "app_main/work_history.html", context)
