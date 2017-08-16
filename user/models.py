from django.utils import timezone

from zhihu import models as zhihu_models
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.conf import settings


class UserManager(BaseUserManager):
    def create_user(self, name, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(name=name, email=UserManager.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username})

    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):

        users_auto_activate = not settings.USERS_VERIFY_EMAIL  # if "USERS_VERIFY_EMAIL" in settings else True
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)

        is_active = extra_fields.pop('is_active', users_auto_activate)
        user = self.model(email=email, is_staff=is_staff, is_active=is_active,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email=email, password=password,
                                 is_staff=True, is_superuser=True,
                                 is_active=True, **extra_fields)


class User(zhihu_models.BaseModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', unique=True)
    first_name = models.CharField('first name', max_length=30, blank=True)
    last_name = models.CharField('last name', max_length=30, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    reset_token = models.CharField(max_length=30, null=True)
    reset_token_time = models.DateTimeField(null=True)

    serializable_fields = ["email", "first_name", "last_name"]

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_full_name(self):
        """
         Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
         Returns the short name for the user.
        """
        return self.first_name

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)

    def get_natural_key(self):
        return [self.first_name, self.last_name]
