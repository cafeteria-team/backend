from .base import *

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": SECRET["DB_NAME"],
        "USER": SECRET["DB_USER"],
        "PASSWORD": SECRET["DB_PASSWORD"],
        "HOST": SECRET["DB_HOST"],
        "PORT": "5432",
    }
}
