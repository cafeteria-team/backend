from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, id, email, password):
        if not id:
            raise ValueError("must have user id")
        if not email:
            raise ValueError("must have user email")
        if not password:
            raise ValueError("must have user password")

        user = self.model(id=id, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, id, email, password):
        user = self.create_user(
            id=id,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(max_length=20, primary_key=True, unique=True)
    email = models.CharField(max_length=100, unique=True)
    register_date = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = "id"
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()

    def __str__(self):
        return self.id

    @property
    def is_staff(self):
        return self.is_admin
