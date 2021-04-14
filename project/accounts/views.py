from django.contrib.auth import authenticate, decorators, login
from django.urls import reverse_lazy
from django.utils.decorators import classonlymethod
from django.views.generic.base import View
from django.views.generic.edit import CreateView
from django.views.generic import DetailView
import django.contrib.auth.views as defaultviews
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import User

from accounts.forms import UserWithEmailCreationForm
from django.core.exceptions import PermissionDenied


default_login_url = "accounts_login"
# TODO: Make these two decorators function properly (i.e. without calling them on each method)


def super_admin_required(login_url=default_login_url):
    def decorator(func):
        @login_required(login_url=login_url)
        def inner(request, *args, **kwargs):
            if not request.user.is_superadmin:
                raise PermissionDenied("Superadmin privileges required to view this page.")
            return func(request, *args, **kwargs)

        return inner

    return decorator


def login_required(login_url=default_login_url, *args, **kwargs):
    return decorators.login_required(*args, **kwargs)


class SuperAdminRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superadmin:
            raise PermissionDenied("Superadmin privileges required to view this page.")
        return super().dispatch(request, *args, **kwargs)


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
        return redirect_if_logged_in(super().as_view(*args, **kwargs), "home")  # type: ignore


class LoginView(HomeIfLoggedInMixin, defaultviews.LoginView):
    template_name = "accounts/login.html"


class LogoutView(defaultviews.LogoutView):
    template_name = "accounts/logout.html"


class SignupView(HomeIfLoggedInMixin, CreateView):
    form_class = UserWithEmailCreationForm
    success_url = reverse_lazy("home")
    template_name = "accounts/signup.html"

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, *kwargs)
        form = self.get_form()
        # FIXME: We check if form is valid twice. (both in super and in this method). Fix it
        if form.is_valid():
            new_user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password1"],
            )
            login(request, new_user)
        return response


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "accounts/profile.html"


def redirect_to_default_user_profile(request):
    return redirect(f"/accounts/{request.user.id}/")