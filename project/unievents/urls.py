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
    EventView,
    RSOView,
    RSOListView,
    UniversityView,
    UniversityListView,
    create_comment_view,
    create_event_view,
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
    path("rso/<int:university_id>/create/", create_rso_view, name="rso_create"),
    path("rso/<int:university_id>/list", RSOListView.as_view(), name="rso_list"),
    path("rso/<int:university_id>/<pk>/", RSOView.as_view(), name="rso_view"),
    path("event/<int:university_id>/<int:rso_id>/create", create_event_view, name="event_create"),
    path("event/<int:university_id>/<int:rso_id>/list", home_view, name="event_list"),
    path("event/<int:university_id>/<int:rso_id>/<pk>", EventView.as_view(), name="event_view"),
    path(
        "event/<int:university_id>/<int:rso_id>/<int:event_id>/create_comment",
        create_comment_view,
        name="comment_create",
    ),
]
