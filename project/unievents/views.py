from typing import Any, Dict, Type, Union, cast
from django.db import models
from django.http.response import Http404, HttpResponseNotAllowed
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpRequest
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from accounts.views import login_required, super_admin_required
from accounts.models import User
from unievents.forms import CreateEventForm, CreateLocationForm, CreateRSOForm, CreateUniversityForm
from django.core.exceptions import PermissionDenied

from unievents.models import Comment, Event, Event_tag, RSO, University
from django.contrib.auth.mixins import LoginRequiredMixin


def being_a_student_required(func):
    @login_required()
    def inner(request, university_id, *args, **kwargs):
        if request.user.university_id != int(university_id):
            raise PermissionError("Being a student at the university is required to view this page.")
        return func(request, university_id, *args, **kwargs)

    return inner


def being_an_admin_required(func):
    def inner(request, rso_id: int, *args, **kwargs):
        if not request.user.is_admin(rso_id):
            raise PermissionDenied("Admin privileges required to view this page.")
        return func(request, rso_id, *args, **kwargs)

    return inner


def post_requests_only(func):
    def inner(request, *args, **kwargs):
        if request.method != "POST":
            return HttpResponseNotAllowed("Only POST requests are allowed on this url.")
        return func(request, *args, **kwargs)

    return inner


def add_to_context_decorator(**models: Type[models.Model]):
    """ @decorator(model1, model2, model3_pk_name=model3, ...) """

    def arghandler(cls: Union[Type[DetailView], Type[ListView]]):
        original_get_context_data = cls.get_context_data

        def inner(self, **kwargs: Any) -> Any:
            context = original_get_context_data(self, **kwargs)
            for kwargname, model in models.items():
                context[model._meta.db_table] = get_object_or_404(model, pk=self.kwargs[kwargname])
            return context

        cls.get_context_data = inner
        return cls

    return arghandler


def get_by_pk_decorator(model: Type[models.Model]):
    def arghandler(func):
        def inner(request, pk, *args, **kwargs):
            return func(request, get_object_or_404(model, pk=int(pk)), *args, **kwargs)

        return inner

    return arghandler


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
            university = university_form.save(location)
            return redirect("university_view", university.university_id)
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


class RSOView(LoginRequiredMixin, DetailView):
    template_name = "unievents/rso_view.html"
    model = RSO

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        # There is a liskov problem here...
        user: User = cast(User, self.request.user)
        rso: RSO = ctx["rso"]
        ctx["filtered_events"] = Event.safe_filter(user, rso_id=rso.rso_id)
        ctx["is_admin"] = user.is_admin(rso.rso_id)
        user_is_already_member = bool(user.rso_memberships.filter(pk=rso.rso_id))
        ctx["user_is_already_member"] = user_is_already_member
        ctx["user_can_join"] = user.university == rso.university and not user_is_already_member
        return ctx


@being_a_student_required
@get_by_pk_decorator(University)
def create_rso_view(request, university):
    students = university.students.exclude(pk=request.user.id)
    form = CreateRSOForm(request.user, students, request.POST or None)
    context = {"form": form, "university": university}
    if request.method == "GET":
        return render(request, "unievents/rso_create.html", context)
    elif request.method == "POST":
        if form.is_valid():
            rso = form.save()
            return redirect("rso_view", rso.rso_id)
        else:
            return render(request, "unievents/rso_create.html", context)
    else:
        return render(request, "unievents/rso_create.html", context)


@post_requests_only
@get_by_pk_decorator(RSO)
def join_rso_view(request, rso):
    existing_rso = request.user.rso_memberships.filter(pk=rso.rso_id).first()
    if existing_rso is not None:
        raise PermissionError("Member of an RSO cannot join it again.")
    rso.members.add(request.user)
    return redirect("rso_view", rso.rso_id)


@post_requests_only
@get_by_pk_decorator(RSO)
def leave_rso_view(request, rso):
    user: User = request.user
    if user.is_admin(rso.rso_id):
        raise PermissionError("Admin of an RSO cannot leave it.")
    # Only RSO members can leave it
    get_object_or_404(user.rso_memberships, pk=rso.rso_id)
    user.rso_memberships.remove(rso)
    return redirect("rso_view", rso.rso_id)


@being_an_admin_required
@get_by_pk_decorator(RSO)
def create_event_view(request, rso):
    event_form = CreateEventForm(request.POST or None, university_id=rso.university_id, rso_id=rso.rso_id)
    location_form = CreateLocationForm(request.POST or None)
    context = {
        "event_form": event_form,
        "location_form": location_form,
        "is_admin": request.user.is_admin(rso.rso_id),
        "rso": rso,
        "possible_tags": Event_tag.objects.all(),
    }
    if request.method == "GET":
        return render(request, "unievents/event_create.html", context)
    elif request.method == "POST":
        if event_form.is_valid() and location_form.is_valid():
            location = location_form.save()
            event = event_form.save(location)
            return redirect("event_view", event.event_id)
        else:
            return render(request, "unievents/event_create.html", context)
    else:
        return render(request, "unievents/event_create.html", context)


class EventView(LoginRequiredMixin, DetailView):
    template_name = "unievents/event_view.html"
    model = Event

    def get(self, request, *args, **kwargs):
        user = request.user
        event: Event = self.get_object()
        if (event.privacy_level == Event.PrivacyLevel.RSO_Private and not event.rso in user.rso_memberships.all()) or (
            event.privacy_level == Event.PrivacyLevel.University_Private and user.university_id != event.university_id
        ):
            raise Http404()
        return super().get(request, *args, **kwargs)


@post_requests_only
@get_by_pk_decorator(Event)
def create_comment_view(request, event):
    Comment(
        event_id=event.event_id,
        user_id=request.user.id,
        text=request.POST["text"],
        rating=request.POST["rating"],
    ).save()
    return redirect("event_view", event.event_id)


@login_required()
def event_list_view(request):
    user: User = request.user
    context = {"filtered_events": Event.safe_filter(user)}
    return render(request, "unievents/event_list.html", context)