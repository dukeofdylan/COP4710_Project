from django.contrib.auth.forms import UserCreationForm
from accounts.models import User
from django import forms


class CaseInsensitiveEmail(forms.EmailField):
    def clean(self, value):
        return super().clean(value.lower())


class UserWithEmailCreationForm(UserCreationForm):
    email = CaseInsensitiveEmail(max_length=254, help_text="Required. Inform a valid email address.")

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "password1",
            "password2",
        )