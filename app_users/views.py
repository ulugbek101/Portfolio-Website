from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from . import forms

CV_PATH = "cv/CV ( Ulugbek Umaraliyev ).pdf"


def download_cv(request):
    try:
        response = FileResponse(open(CV_PATH, "rb"), content_type="application/pdf")
    except FileNotFoundError:
        raise Http404("CV not found")
    response["Content-Disposition"] = 'attachment; filename="Ulugbek-Umaraliyev-CV.pdf"'
    return response


def login_view(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.POST.get("next") or "index")
        messages.error(request, _("Invalid username or password."))
        return render(request, "app_users/login.html", {"username": username or ""})

    return render(request, "app_users/login.html", {"next": request.GET.get("next", "")})


def logout_view(request):
    logout(request)
    messages.success(request, _("You have been signed out."))
    return redirect("index")


@login_required
@require_POST
def create_review(request):
    form = forms.ReviewForm(request.POST, request.FILES)
    if form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.approved = False
        review.save()
        messages.success(
            request,
            _("Thank you! Your review was submitted and will appear once approved."),
        )
    else:
        messages.error(request, _("Please check the review form and try again."))
    return redirect("/#reviews")
