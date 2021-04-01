from unievents.models import University
from django import forms
from mapwidgets.widgets import GooglePointFieldWidget


class CreateUniversityForm(forms.ModelForm):
    name = forms.fields.CharField(widget=forms.TextInput)
    description = forms.fields.CharField(widget=forms.Textarea)
    email_domain = forms.fields.CharField(widget=forms.TextInput)
    avatar_image = forms.fields.ImageField(max_length=10000, allow_empty_file=False)

    class Meta:

        model = University
        fields = ("coordinates", "name", "avatar_image", "email_domain", "description")
        widgets = {
            "coordinates": GooglePointFieldWidget,
        }
