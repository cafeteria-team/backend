from .base import *

DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": SECRET["DB_NAME"],
        "USER": SECRET["DB_USER"],
        "PASSWORD": SECRET["DB_PASSWORD"],
        "HOST": SECRET["DB_HOST"], 
        "PORT": "5432",
    }
}
