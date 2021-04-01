from django.http.request import HttpRequest
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import DetailView
import django.contrib.auth.views as defaultviews
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from accounts.models import User

from accounts.forms import UserWithEmailCreationForm


class LoginView(defaultviews.LoginView):
    template_name = "accounts/login.html"


class LogoutView(defaultviews.LogoutView):
    template_name = "accounts/logout.html"


class SignupView(CreateView):
    form_class = UserWithEmailCreationForm
    success_url = reverse_lazy("login")
    template_name = "accounts/signup.html"


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "accounts/profile.html"


@login_required
def redirect_to_default_user_profile(request):
    return redirect(f"/accounts/profile/{request.user.id}/")