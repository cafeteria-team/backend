from django.contrib.auth.models import AbstractUser
from django.db import models

from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Custom User Model"""

    class UserRoles(models.TextChoices):
        ADMIN = "ADMIN", _("Admin")
        STORE = "STORE", _("Store")

    phone = models.CharField(max_length=11)
    role = models.CharField(
        max_length=20, choices=UserRoles.choices, default=UserRoles.STORE
    )
    deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "user"
