from django.forms import ModelForm
from . import models


class UserLogInForm(ModelForm):
    class Meta:
        model = models.UserAccount
        fields = ("email", "password")


class UserSignUpForm(ModelForm):
    class Meta:
        model = models.UserAccount
        fields = ("username", "image", "email", "password", "first_name", "last_name")
