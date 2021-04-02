from django.urls import reverse_lazy
from django.utils.decorators import classonlymethod
from django.views.generic.base import View
from django.views.generic.edit import CreateView
from django.views.generic import DetailView
import django.contrib.auth.views as defaultviews
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import User

from accounts.forms import UserWithEmailCreationForm


def redirect_if_logged_in(runnable, to):
    def inner_func(request):
        if request.user.is_authenticated:
            return redirect(to)
        else:
            return runnable(request)

    return inner_func


class HomeIfLoggedInMixin:
    @classonlymethod
    def as_view(cls, *args, **kwargs):
        return redirect_if_logged_in(super().as_view(*args, **kwargs), "home")


class LoginView(HomeIfLoggedInMixin, defaultviews.LoginView):
    template_name = "accounts/login.html"


class LogoutView(defaultviews.LogoutView):
    template_name = "accounts/logout.html"


class SignupView(HomeIfLoggedInMixin, CreateView):
    form_class = UserWithEmailCreationForm
    success_url = reverse_lazy("accounts_login")
    template_name = "accounts/signup.html"


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "accounts/profile.html"


def redirect_to_default_user_profile(request):
    return redirect(f"/accounts/{request.user.id}/")