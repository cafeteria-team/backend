from django.db import models
from django.contrib.postgres.fields import ArrayField

from core.models import TimeStampModel
from store.models import Store


class Menu(TimeStampModel):
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE, related_name="menu", verbose_name="업체"
    )
    menus = ArrayField(models.CharField(max_length=50, blank=True), size=10)
    provide_at = models.DateTimeField()

    class Meta:
        db_table = "menu"
        verbose_name_plural = "menu"
