from django.shortcuts import render

from . import models

def index(request):
    context = {}
    return render(request, 'app_main/index.html', context)

def portfolio(request):
    context = {
        'projects': models.Project.objects.all(),
    }
    return render(request, 'app_main/portfolio.html', context)

def services(request):
    context = {}
    return render(request, 'app_main/services.html', context)

