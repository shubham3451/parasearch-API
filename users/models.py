from django.db import models
from typing import Any
from django.contrib.auth.models import BaseUserManager
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin



class UserManager(BaseUserManager):
  """Manager class for creating users and superusers."""

  def create_user(
      self,
      email: str,
      name: str,
      password: str | None = None,
      **extra_fields: Any
  ):
    """Creates and returns a new user.

    Args:
      email: The user's email.
      name: The user's name.
      password: The user's password.
      extra_fields: Additional fields.

    Returns:
      The created user instance.

    Raises:
      ValueError: If email is not provided.
    """
    if not email:
      raise ValueError('Email must be provided.')
    email = self.normalize_email(email)
    user = self.model(email=email, name=name, **extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_superuser(
      self,
      email: str,
      name: str,
      password: str,
      **extra_fields: Any
  ):
    """Creates and returns a new superuser.

    Args:
      email: The user's email.
      name: The user's name.
      password: The user's password.
      extra_fields: Additional fields.

    Returns:
      The created superuser instance.
    """
    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault('is_superuser', True)
    return self.create_user(email, name, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
  """User model with email as unique identifier."""

  id = models.UUIDField(
      primary_key=True, default=uuid.uuid4, editable=False)
  name = models.CharField(max_length=100)
  email = models.EmailField(unique=True)
  dob = models.DateField(null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  modified_at = models.DateTimeField(auto_now=True)

  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)

  objects = UserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['name']

  def __str__(self) -> str:
    """Returns the email of the user.

    Returns:
      A string representing the user's email.
    """
    return self.email