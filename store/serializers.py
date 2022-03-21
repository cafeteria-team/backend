from rest_framework import serializers
from .models import Store


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store

        fields = [
            "name",
            "addr",
            "zip_code",
            "detail_addr",
            "busi_num",
            "busi_num_img",
        ]


class MemberStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ["name"]


class MemberDetailStoreSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ["name", "busi_num", "busi_num_img"]
