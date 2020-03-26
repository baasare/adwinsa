from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)
    phone_regex = RegexValidator(regex=r'^\D?(\d{3})\D?\D?(\d{3})\D?(\d{4})$',
                                 message="Phone number must be entered in the format: '020*******'. Up to 10 digits "
                                         "allowed.",
                                 code='invalid_phone_number')
    phone_number = models.CharField(validators=[phone_regex], max_length=10, blank=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        ordering = ['-last_name']
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_absolute_url(self):
        return reverse('user_detail', args=[self.id])

    def get_full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def get_email(self):
        return '%s' % self.email

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)
