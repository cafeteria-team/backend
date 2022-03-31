from rest_framework import serializers
from .models import Store, Facility


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


class FacilityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        exclude = ["created", "updated", "deleted"]


class FacilityRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = ["name"]


class MemberStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ["name"]


class MemberDetailStoreSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ["name", "busi_num", "busi_num_img"]
