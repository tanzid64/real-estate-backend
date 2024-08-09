from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _

def validate_email_address(email:str):
  try:
    validate_email(email)
  except ValidationError:
    raise ValidationError(
      _("Please enter a valid email address."),
      code='invalid',
    )
  
class UserManager(DjangoUserManager):
  def _create_user(self, username: str, email: str, password: str | None, **extra_fileds):
    if not username:
      raise ValueError(_('Username is required'))
    if not email:
      raise ValueError(_('Email is required'))
    email = self.normalize_email(email)
    validate_email_address(email)
    global_user_model = apps.get_model(
      self.model._meta.app_label, self.model._meta.object_name
    )
    username = global_user_model.normalize_username(username)
    user = self.model(
      username = username,
      email = email,
      **extra_fileds
    )
    user.password = make_password(password)
    user.save(using=self._db)
    return user
  
  def create_user(self, username: str, email: str, password: str | None = None, **extra_fileds):
    extra_fileds.setdefault('is_staff', False)
    extra_fileds.setdefault('is_superuser', False)
    return self._create_user(username, email, password, **extra_fileds)
  
  def create_superuser(self, username: str, email: str, password: str | None = None, **extra_fileds):
    extra_fileds.setdefault('is_staff', True)
    extra_fileds.setdefault('is_superuser', True)
    extra_fileds.setdefault('is_active', True)
    if extra_fileds.get('is_staff') is not True:
      raise ValueError(_('Superuser must have is_staff=True.'))
    if extra_fileds.get('is_superuser') is not True:
      raise ValueError(_('Superuser must have is_superuser=True.'))
    return self._create_user(username, email, password, **extra_fileds)