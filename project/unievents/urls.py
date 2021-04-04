"""cop4710 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from unievents.views import (
    RSOView,
    RSOListView,
    UniversityView,
    UniversityListView,
    create_rso_view,
    home_view,
    create_university_view,
)
from django.views.generic import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="home")),
    path("home", home_view, name="home"),
    path("university/create", create_university_view, name="universities_create"),
    path("university/list", UniversityListView.as_view(), name="universities_list"),
    path("university/<pk>/", UniversityView.as_view(), name="universities_view"),
    path("event/<pk>/", home_view, name="events_view"),
    path("rso/<int:university_id>/create/", create_rso_view, name="rso_create"),
    path("rso/<int:university_id>/list", RSOListView.as_view(), name="rso_list"),
    path("rso/<int:university_id>/<pk>/", RSOView.as_view(), name="rso_view"),
    path("event/<int:rso_id>/create", home_view, name="events_create"),
]
