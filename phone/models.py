from django.db import models


class PhoneAuthLog(models.Model):
    phone_num = models.CharField(max_length=12)
    auth_num = models.CharField(max_length=6)
    confirmed = models.BooleanField(default=False)

    class Meta:
        db_table = "phone_auth_log"
