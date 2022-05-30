from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField

from core.models import TimeStampModel
from users.models import User

# Create your models here.
class Store(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="store")
    name = models.CharField(max_length=128)
    addr = models.CharField(max_length=128)
    zip_code = models.CharField(max_length=6)
    detail_addr = models.CharField(max_length=128, blank=True)
    busi_num = models.CharField(max_length=10)
    busi_num_img = models.CharField(max_length=256, blank=True)
    price = ArrayField(models.JSONField(default=dict), blank=True, null=True)
    location = models.PointField(srid=4326)

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


class JoinFacility(TimeStampModel):
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name="store_facility",
        verbose_name="업체",
    )
    facility = models.ForeignKey(
        Facility,
        on_delete=models.CASCADE,
        related_name="join_facility",
        verbose_name="편의시설",
    )

    class Meta:
        db_table = "join_facility"
        verbose_name_plural = "join_facility"
