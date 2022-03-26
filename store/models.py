from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import User
from core.models import TimeStampModel

# Create your models here.
class Store(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="store")
    name = models.CharField(max_length=128)
    addr = models.CharField(max_length=128)
    zip_code = models.CharField(max_length=6)
    detail_addr = models.CharField(max_length=128, blank=True)
    busi_num = models.CharField(max_length=10)
    busi_num_img = models.CharField(max_length=256)
    price = models.JSONField(default=dict)

    class Meta:
        db_table = "store"
        verbose_name_plural = "store"


class Facility(TimeStampModel):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="facility")
    name = models.CharField(max_length=24)
    deleted = models.BooleanField(default=False)

    class Meta:
        db_table = "facility"
        verbose_name_plural = "facility"
