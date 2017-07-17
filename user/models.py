from django.utils import timezone
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import re
from django.forms import ModelForm, modelform_factory
import datetime


# def validate_is_unique(value):
#     count = User.objects.filter(username=value).count()
#     if count > 0:
#         raise ValidationError(u"The username has been registered.")


def validate_is_blank(value):
    if not value:
        raise ValidationError(u"username or password can't be empty!")


# def validate_mail(email):
#     try:
#         validate_email(email)
#         return True
#     except ValidationError:
#         return False


# 继承
class User(models.Model):
    username = models.CharField(max_length=30, blank=False, null=True)
    password = models.CharField(max_length=30, blank=False, validators=[validate_is_blank])
    register_time = models.DateTimeField(blank=True, default=timezone.now)
    register_email = models.EmailField(unique=True, validators=[validate_is_blank, validate_email])
    reset_token = models.CharField(max_length=30, blank=True, null=True)
    reset_token_time = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return self.username


# UserForm = modelform_factory(User, fields="__all__")

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = "__all__"
