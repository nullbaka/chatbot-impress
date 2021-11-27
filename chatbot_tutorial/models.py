from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import six
from django.contrib.auth.validators import ASCIIUsernameValidator, UnicodeUsernameValidator
from django.core.validators import MinLengthValidator

from django.contrib.auth.models import UserManager


class User(AbstractBaseUser):
    username_validator = UnicodeUsernameValidator() if six.PY3 else ASCIIUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=20,
        unique=True,
        help_text=_('Required. Between 6 to 20 characters. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator, MinLengthValidator(6)],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    objects = UserManager()

    USERNAME_FIELD = 'username'


class CallCount(models.Model):
    user = models.OneToOneField(User, related_name="count")

    dumb = models.IntegerField(default=0)
    stupid = models.IntegerField(default=0)
    fat = models.IntegerField(default=0)
    query = models.IntegerField(default=0)
