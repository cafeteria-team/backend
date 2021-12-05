from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom User Model"""

    birth = models.DateField(blank=True, null=True)
    superhost = models.BooleanField(default=False)
