from django.shortcuts import render


def login(request):
    context = {}
    return render(request, 'app_users/login.html', context)
