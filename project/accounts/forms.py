from django.contrib.auth.forms import UserCreationForm
from accounts.models import User
from django import forms


class UserWithEmailCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text="Required. Inform a valid email address.")

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "password1",
            "password2",
        )