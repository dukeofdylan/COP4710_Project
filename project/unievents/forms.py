from os import makedirs

from django.core.exceptions import ValidationError
from unievents.models import Location, University
from django import forms
from mapwidgets.widgets import GooglePointFieldWidget, GoogleStaticMapWidget
from django.forms.models import inlineformset_factory
from django.contrib.gis.geos import GEOSGeometry

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
        point = GEOSGeometry(self.cleaned_data["point"])
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
