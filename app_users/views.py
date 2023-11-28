from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from . import forms


def login_view(request):

    if request.user.is_authenticated:
        # error message: Logout first to log in again
        return redirect('index')

    if request.method == 'POST':
        next_page = request.POST.get('next')
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

def create_review(request):
    user = request.user
    
    form = forms.ReviewForm(request.POST, request.FILES)
    if form.is_valid:
        review = form.save(commit=False)
        review.user = user
        review.save()
        # success message
        return redirect('index')
    else:
        # error message
        return render('index')
