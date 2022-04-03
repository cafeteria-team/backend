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


class FacilityAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        exclude = ["deleted"]
        read_only_fields = ["created", "updated"]


class FacilityAdminRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = ["category", "name"]


class FacilityAdminDetailUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = ["category", "name"]


class MemberStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ["name"]


class MemberDetailStoreSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ["name", "busi_num", "busi_num_img"]
