from django.db import models
from django.utils.translation import gettext_lazy as _


class PhoneAuthLog(models.Model):
    class PhoneAuthCategory(models.TextChoices):
        AUTH = "AUTH", _("AUTH")
        PASSWORD = "PASSWORD", _("PASSWORD")

    phone_num = models.CharField(max_length=12, verbose_name="휴대폰 번호")
    auth_num = models.CharField(max_length=6, verbose_name="인증번호")
    confirmed = models.BooleanField(default=False, verbose_name="인증 여부")
    purpose = models.CharField(
        max_length=8, choices=PhoneAuthCategory.choices, verbose_name="인증 목적"
    )

    class Meta:
        db_table = "phone_auth_log"
