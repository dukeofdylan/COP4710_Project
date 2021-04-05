from typing import Type, cast

from django.core.exceptions import ValidationError
from django.db.models.query import QuerySet
from accounts.models import User
from unievents.models import Event, Location, RSO, University
from django import forms
from mapwidgets.widgets import GooglePointFieldWidget, GoogleStaticMapWidget
from django.contrib.gis.geos import GEOSGeometry, Point

from unievents.util import download
from cop4710.settings import MEDIA_ROOT


class DynamicForm(forms.Form):
    def __init__(self, extra: dict, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for key, value in extra.items():
            self.fields[key] = value


class CreateLocationForm(forms.ModelForm):
    point = forms.fields.Field(widget=GooglePointFieldWidget, label="Location")

    class Meta:
        model = Location
        exclude = ("latitude", "longitude", "image")

    def save(self, commit=True):
        instance = super().save(commit=False)
        point = cast(Point, GEOSGeometry(self.cleaned_data["point"]))
        instance.longitude = point.x
        instance.latitude = point.y
        existing_locations = self.Meta.model.objects.filter(longitude=point.x, latitude=point.y)
        if len(existing_locations):
            return existing_locations[0]
        fname = (MEDIA_ROOT / "location" / f"{instance.longitude}|{instance.latitude}").with_suffix(".png")
        download(GoogleStaticMapWidget().get_image_url(point), fname)
        instance.image = "location/" + fname.name
        if commit:
            instance.save()
        return instance


class CreateUniversityForm(forms.ModelForm):
    name = forms.fields.CharField(widget=forms.TextInput)
    description = forms.fields.CharField(widget=forms.Textarea)
    email_domain = forms.fields.CharField(widget=forms.TextInput)
    avatar_image = forms.fields.ImageField(max_length=10000, allow_empty_file=False)

    class Meta:
        model = University
        fields = ("name", "email_domain", "avatar_image", "description")

    # Am I breaking Liskov substitution principle? HELL YEAH.
    def save(self, location, commit=True):
        instance = super().save(commit=False)
        instance.location_id = location.location_id
        if commit:
            instance.save()
        return instance

    def clean_image(self):
        image = self.cleaned_data.get("avatar_image", False)
        if image:
            if image._size > University.max_avatar_size:
                raise ValidationError("Image file too large ( > 5mb )")
            return image
        else:
            raise ValidationError("Couldn't read uploaded image")


class ModelMultipleChoiceFieldWithMinNumberOfChoices(forms.ModelMultipleChoiceField):
    def __init__(self, min_choices, *args, **kwargs):
        self.min_choices = min_choices
        super().__init__(*args, **kwargs)

    def clean(self, value):
        if len(value) < self.min_choices:
            raise ValidationError(f"{len(value)} choices provided. {self.min_choices} required.")
        return super().clean(value)


class CreateRSOForm(forms.ModelForm):
    members = ModelMultipleChoiceFieldWithMinNumberOfChoices(
        min_choices=4,
        widget=forms.widgets.CheckboxSelectMultiple,
        help_text="Pick 4 more students to create the RSO.",
        queryset=None,
    )
    name = forms.fields.CharField(widget=forms.TextInput)

    class Meta:
        model = RSO
        fields = ("name", "description", "members")

    def __init__(self, future_admin, university_students, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.future_admin = future_admin
        self.fields["members"].queryset = university_students

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.admin_id = self.future_admin.id
        instance.university_id = self.future_admin.university_id
        if commit:
            instance.save()
            # Very important for saving members
            self.cleaned_data["members"] |= User.objects.filter(pk=self.future_admin.id)
            self.save_m2m()
        return instance


class CreateEventForm(forms.ModelForm):
    # description = models.TextField(db_column="description", blank=True, null=True)
    phone = forms.fields.CharField(widget=forms.TextInput, label="Contact phone")
    # dtstart = models.DateTimeField(db_column="dtstart", auto_now_add=True)
    # dtend = models.DateTimeField(db_column="dtend", auto_now_add=True)
    # until = models.DateTimeField(db_column="until", auto_now_add=True)
    summary = forms.fields.CharField(widget=forms.TextInput, label="Name")
    email = forms.fields.CharField(widget=forms.TextInput)
    # location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, null=False)
    # rso = models.ForeignKey(RSO, on_delete=models.CASCADE, blank=True, null=False)

    class Meta:
        model = Event
        exclude = ("location", "rso", "dtstart", "dtend", "until")

    def __init__(self, *args, university_id, rso_id, **kwargs):
        super().__init__(*args, **kwargs)
        self.university_id = university_id
        self.rso_id = rso_id

    # Am I breaking Liskov substitution principle? HELL YEAH.
    def save(self, location, dtstart, dtend, until, commit=True):
        instance = super().save(commit=False)
        instance.university_id = self.university_id
        instance.rso_id = self.rso_id
        instance.location_id = location.location_id
        instance.dtstart = dtstart
        instance.dtend = dtend
        instance.until = until
        if commit:
            instance.save()
        return instance
