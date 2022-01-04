from rest_framework import serializers
from .models import Store


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store

        fields = [
            "addr",
            "zip_code",
            "detail_addr",
            "busi_num",
        ]
