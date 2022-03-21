from django.db import models

from users.models import User

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
