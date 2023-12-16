from django.shortcuts import render, get_object_or_404

from . import models
from app_users.models import Review
from app_users.forms import ReviewForm

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
    posts = models.Post.objects.all()

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
