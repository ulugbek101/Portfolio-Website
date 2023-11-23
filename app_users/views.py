from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


def login_view(request):

    if request.user.is_authenticated:
        # error message: Logout first to log in again
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            # success message: invalid credentials
            login(request, user)
            return redirect('index')
        else:
            context = {
                'invalid_credentials': True,
                'username': username if username else '',
            }
            # if not username: del context['username']
            return render(request, 'app_users/login.html', context)

    context = {}
    return render(request, 'app_users/login.html', context)
