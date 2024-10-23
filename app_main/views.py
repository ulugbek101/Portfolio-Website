from django.shortcuts import render, get_object_or_404
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.views.generic import CreateView

from . import models
from . import forms

from app_users.models import Review
from app_users.forms import ReviewForm


# class CreatePost(LoginRequiredMixin, CreateView):
#     template_name = 'form.html'
#     model = models.Post
#     form_class = forms.PostForm


def index(request):
    form = ReviewForm()
    context = {
        "reviews": Review.objects.filter(verified=True),
        "rate": range(1, 6),
        "form": form,
    }
    return render(request, 'app_main/index.html', context)


def portfolio(request):
    context = {
        'projects': models.Project.objects.all(),
    }
    return render(request, 'app_main/portfolio.html', context)


def services(request):
    context = {}
    return render(request, 'app_main/services.html', context)


def posts(request):
    posts = models.Post.objects.filter(is_active=True).order_by("-created")

    context = {
        'posts': posts,
    }
    return render(request, 'app_main/posts.html', context)


def post(request, slug):
    post = get_object_or_404(models.Post, slug=slug)

    context = {
        'post': post,
    }
    return render(request, 'app_main/post.html', context)
