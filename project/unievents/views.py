from django import forms
from django.shortcuts import render
from django.http import HttpRequest
from django.urls.base import reverse_lazy
from django.views.generic.edit import CreateView
from unievents.forms import CreateUniversityForm

from unievents.models import University

# Create your views here.


def home_view(request: HttpRequest):
    return render(request, "unievents/home.html")


class CreateUniversityView(CreateView):
    form_class = CreateUniversityForm
    template_name = "unievents/create_university.html"
    model = University
    success_url = reverse_lazy("home")
