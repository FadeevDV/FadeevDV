from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager

ROLE_CHOICES = settings.ROLE_CHOICES
USER = 'user'


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField('Имя', max_length=30, blank=True)
    last_name = models.CharField('Фамилия', max_length=30, blank=True)
    username = models.CharField('Username', max_length=30, unique=True)
    bio = models.TextField('О себе', blank=True)
    email = models.EmailField(_('Адрес электронной почты'), unique=True)
    role = models.CharField(
        'Роль пользователя', max_length=9, default=USER, choices=ROLE_CHOICES
    )
    confirmation_code = models.TextField('Код подтверждения', blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    class Meta:
        ordering = ['username']

    def __str__(self):
        return self.email
