from rest_framework import serializers

from core.exceptions.exceptions import DuplicationException

from .models import Store, Facility, JoinFacility


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


class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        exclude = ["deleted", "created", "updated"]


class JoinFacilitySerializer(serializers.ModelSerializer):
    facility = FacilitySerializer()

    class Meta:
        model = JoinFacility
        exclude = ["store"]


class JoinFacilityCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JoinFacility
        fields = ["facility"]

    def create(self, validated_data):
        try:
            JoinFacility.objects.get(**validated_data)
            raise DuplicationException("The facility is already registered")
        except JoinFacility.DoesNotExist:
            return super().create(validated_data)


class StoreWithFacility(serializers.ModelSerializer):
    store_facility = JoinFacilitySerializer(many=True)

    class Meta:
        model = Store
        fields = ["store_facility"]
