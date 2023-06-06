from typing import Any, Dict, Mapping, Optional, Type, Union
from django.core.files.base import File
from django.db.models.base import Model
from django.forms import ModelForm
from django.forms.utils import ErrorList
from django.forms.widgets import HiddenInput
from . import models


class UserLogInForm(ModelForm):
    class Meta:
        model = models.UserAccount
        fields = ("email", "password")


class UserSignUpForm(ModelForm):
    class Meta:
        model = models.UserAccount
        fields = ("username", "image", "email", "password", "first_name", "last_name")


class LeaveArticles(ModelForm):
    class Meta:
        model = models.Articles
        fields = "__all__"


class AddComment(ModelForm):
    def __init__(self, article=None, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["article"].widget = HiddenInput()
        self.fields["author"].widget = HiddenInput()
        self.fields["article"].initial = article
        self.fields["author"].initial = user

    class Meta:
        model = models.Comments
        fields = "__all__"
