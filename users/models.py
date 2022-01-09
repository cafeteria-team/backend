from django.contrib.auth.models import AbstractUser
from django.db import models

from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Custom User Model"""

    # class UserRoles(models.TextChoices):
    #     ADMIN = "ADMIN", _("Admin")

    phone = models.CharField(max_length=11)
    is_active = models.BooleanField(default=False)
    # role = models.CharField(max_length=20, choices=UserRoles.choices)
