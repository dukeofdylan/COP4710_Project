from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.http import HttpRequest
from django.urls.base import reverse_lazy
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from mapwidgets.widgets import GooglePointFieldInlineWidget, GooglePointFieldWidget, GoogleStaticMapWidget
from cop4710.settings import MAP_WIDGETS
from unievents.forms import (
    CreateLocationForm,
    CreateUniversityForm,
    DynamicForm,
)

from unievents.models import University

# Create your views here.


@login_required(login_url="accounts_login")
def home_view(request: HttpRequest):
    return render(request, "unievents/home.html")


def create_university_view(request):
    university_form = CreateUniversityForm(request.POST or None, request.FILES or None)
    location_form = CreateLocationForm(request.POST or None)
    context = {"university_form": university_form, "location_form": location_form}
    if request.method == "GET":
        return render(request, "unievents/create_university.html", context)
    elif request.method == "POST":
        if university_form.is_valid() and location_form.is_valid():
            location = location_form.save()
            university_form.save(location)
            return redirect("home")
        else:
            return render(request, "unievents/create_university.html", context)
    else:
        return render(request, "unievents/create_university.html", context)


# class CreateUniversityView(TemplateView):
#     form_class = CreateUniversityForm
#     template_name = "unievents/create_university.html"
#     model = University
#     success_url = reverse_lazy("home")

#     def


class UniversityView(DetailView):
    template_name = "unievents/university.html"
    model = University


class UniversityListView(ListView):
    template_name = "unievents/universities_list.html"
    model = University