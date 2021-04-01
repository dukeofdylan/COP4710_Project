from django.contrib.auth.forms import UserCreationForm
from unievents.models import University
from django import forms


class CreateUniversityForm(forms.ModelForm):
    name = forms.fields.CharField(widget=forms.TextInput)
    description = forms.fields.CharField(widget=forms.Textarea)
    email_domain = forms.fields.CharField(widget=forms.TextInput)

    class Meta:

        model = University
        fields = ("name", "avatar_image", "email_domain", "description")
