from rest_framework import serializers

from core.exceptions.exceptions import DuplicationException

from .models import Store, Facility, JoinFacility


class StoreSerializer(serializers.ModelSerializer):
    facilities = serializers.SerializerMethodField()

    def get_facilities(self, obj):
        store_facilities = obj.store_facility.all()
        return [item.facility.name for item in store_facilities]

    class Meta:
        model = Store

        fields = [
            "name",
            "addr",
            "zip_code",
            "detail_addr",
            "busi_num",
            "busi_num_img",
            "facilities",
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
    store_facility = serializers.SerializerMethodField()

    def get_store_facility(self, obj):
        join_facility = JoinFacility.objects.filter(store=obj, facility__deleted=False)
        serializer = JoinFacilitySerializer(data=join_facility, many=True)
        serializer.is_valid()
        return serializer.data

    class Meta:
        model = Store
        fields = ["store_facility"]


class StorePriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ["price"]
