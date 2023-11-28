from django.shortcuts import render

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

