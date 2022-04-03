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
    class FacilityCategory(models.TextChoices):
        CAFE = "CAFE", _("카페")
        COFFEE = "COFFEE", _("커피")
        CONVEIENCE = "CONVEIENCE", _("편의점")
        NOODEL = "NOODEL", _("면")
        BREAD = "BREAD", _("빵")
        BEVERAGE = "BEVERAGE", _("음료")

    name = models.CharField(max_length=24, verbose_name="편의시설 이름")
    category = models.CharField(
        max_length=15,
        choices=FacilityCategory.choices,
        verbose_name="편의시설 카테고리",
        default="",
    )
    deleted = models.BooleanField(default=False)

    class Meta:
        db_table = "facility"
        verbose_name_plural = "facility"
