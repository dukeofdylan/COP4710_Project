from typing import Any, Type
from django.db import models
from django.db.models.base import ModelBase
from django.shortcuts import redirect, render
from django.http import HttpRequest
from django.views.generic.base import ContextMixin, View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from accounts.views import login_required, super_admin_required
from unievents.forms import CreateLocationForm, CreateRSOForm, CreateUniversityForm

from unievents.models import RSO, University
from django.contrib.auth.mixins import LoginRequiredMixin


def being_a_student_required(func):
    @login_required()
    def inner(request, university_id: int):
        if request.user.university_id != university_id:
            return redirect("home")
        return func(request, university_id)

    return inner


@login_required()
def home_view(request: HttpRequest):
    return render(request, "unievents/home.html")


@super_admin_required()
def create_university_view(request):
    university_form = CreateUniversityForm(request.POST or None, request.FILES or None)
    location_form = CreateLocationForm(request.POST or None)
    context = {"university_form": university_form, "location_form": location_form}
    if request.method == "GET":
        return render(request, "unievents/university_create.html", context)
    elif request.method == "POST":
        if university_form.is_valid() and location_form.is_valid():
            location = location_form.save()
            university_form.save(location)
            return redirect("home")
        else:
            return render(request, "unievents/university_create.html", context)
    else:
        return render(request, "unievents/university_create.html", context)


class UniversityView(LoginRequiredMixin, DetailView):
    template_name = "unievents/university_view.html"
    model = University


class UniversityListView(LoginRequiredMixin, ListView):
    template_name = "unievents/university_list.html"
    model = University


def add_to_context_decorator(**models: Type[models.Model]):
    """ @decorator(model1, model2, model3_pk_name=model3, ...) """

    def arghandler(cls: Type[ContextMixin]):
        def inner(self, **kwargs: Any) -> Any:
            context = super(type(self), self).get_context_data(**kwargs)
            for kwargname, model in models.items():
                context[model._meta.db_table] = model.objects.get(pk=self.kwargs[kwargname])
            return context

        cls.get_context_data = inner
        return cls

    return arghandler


# class UniversityInContextMixin:
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)  # type: ignore
#         context["university"] = University.objects.get(pk=self.kwargs.pop("university_id"))  # type: ignore
#         return context


@add_to_context_decorator(university_id=University)
class RSOView(LoginRequiredMixin, DetailView):
    template_name = "unievents/rso_view.html"
    model = RSO


@add_to_context_decorator(university_id=University)
class RSOListView(LoginRequiredMixin, ListView):
    template_name = "unievents/rso_list.html"
    model = RSO


@being_a_student_required
def create_rso_view(request, university_id: int):
    university = University.objects.get(pk=university_id)  # TODO: Handle university_does_not_exist_error
    students = university.students.exclude(pk=request.user.id)
    form = CreateRSOForm(request.user, students, request.POST or None)
    context = {"form": form, "university": university}
    if request.method == "GET":
        return render(request, "unievents/rso_create.html", context)
    elif request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("home")
        else:
            return render(request, "unievents/rso_create.html", context)
    else:
        return render(request, "unievents/rso_create.html", context)
