import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.utils.translation import gettext_lazy as _
from core_apps.users.managers import UserManager

class UsernameValidator(validators.RegexValidator):
  regex = r'^[\w.@+-]+$'
  message = _(
    'Enter a valid username. This value may contain only letters, '
    'numbers, and @/./+/-/_ characters.'
  )
  flags = 0 # No special flag or pattern is being used

class User(AbstractUser):
  pkid = models.BigAutoField(primary_key=True, editable=False)
  id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
  first_name = models.CharField(verbose_name=_("First Name"), max_length=60)
  last_name = models.CharField(verbose_name=_("Last Name"), max_length=60)
  email = models.EmailField(verbose_name=_("Email Address"), unique=True, db_index=True)
  username = models.CharField(
    verbose_name=_("Username"),
    max_length=60,
    unique=True,
    validators=[UsernameValidator],
  )

  EMAIL_FIELD = 'email'
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

  objects = UserManager()

  class Meta:
    verbose_name = _("User")
    verbose_name_plural = _("Users")
    ordering = ['-date_joined'] # Desc order
    

  @property
  def get_full_name(self) -> str:
    full_name = f"{self.first_name} {self.last_name}"
    return full_name.strip()

  def __str__(self):
    return self.email
  


