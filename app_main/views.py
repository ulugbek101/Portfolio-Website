from django.shortcuts import render

from app_users.forms import ReviewForm
from app_users.models import Review
from content.models import News, Post

from .models import Project


def index(request):
    context = {
        "featured_posts": Post.objects.filter(is_published=True)[:3],
        "latest_news": News.objects.filter(is_published=True)[:2],
        "projects": Project.objects.filter(is_featured=True)[:6],
        "reviews": Review.objects.filter(approved=True).select_related("user"),
        "review_form": ReviewForm(),
    }
    return render(request, "app_main/index.html", context)


def portfolio(request):
    context = {
        "projects": Project.objects.all(),
        "meta_title": "Projects — Ulug'bek Umaraliyev",
    }
    return render(request, "app_main/portfolio.html", context)
