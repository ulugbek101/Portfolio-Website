from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
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
        identifier = (request.POST.get("username") or "").strip()
        password = request.POST.get("password")

        # Allow signing in with either a username or an email address.
        user = authenticate(request, username=identifier, password=password)
        if user is None and identifier and "@" in identifier:
            from django.contrib.auth import get_user_model

            match = get_user_model().objects.filter(email__iexact=identifier).first()
            if match:
                user = authenticate(request, username=match.get_username(), password=password)

        if user:
            login(request, user)
            return redirect(request.POST.get("next") or "index")
        messages.error(request, _("Invalid username/email or password."))
        return render(request, "app_users/login.html", {"username": identifier})

    return render(request, "app_users/login.html", {"next": request.GET.get("next", "")})


def logout_view(request):
    logout(request)
    messages.success(request, _("You have been signed out."))
    return redirect("index")


def register_view(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, _("Welcome! Your account has been created."))
            return redirect(request.POST.get("next") or "index")
    else:
        form = forms.RegistrationForm()

    return render(
        request,
        "app_users/register.html",
        {"form": form, "next": request.GET.get("next", "")},
    )


@login_required
def profile_view(request):
    profile_form = forms.ProfileForm(instance=request.user)
    password_form = SetPasswordForm(request.user)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "password":
            password_form = SetPasswordForm(request.user, request.POST)
            if password_form.is_valid():
                password_form.save()
                # Keep the current session signed in after the password change.
                update_session_auth_hash(request, request.user)
                messages.success(request, _("Your password has been updated."))
                return redirect("profile")
            messages.error(request, _("Please correct the errors below."))
        else:
            profile_form = forms.ProfileForm(
                request.POST, request.FILES, instance=request.user
            )
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, _("Your profile has been updated."))
                return redirect("profile")
            messages.error(request, _("Please correct the errors below."))

    return render(
        request,
        "app_users/profile.html",
        {"profile_form": profile_form, "password_form": password_form},
    )


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
