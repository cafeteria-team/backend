from rest_framework import serializers

from .models import Menu
from store.serializers import StoreSerializer


class MenuSerializer(serializers.ModelSerializer):
    store = StoreSerializer()

    class Meta:
        model = Menu
        fields = "__all__"


class MenuCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        exclude = ["store"]


class MenuUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        exclude = ["store", "created", "updated"]


class NearbyTodayMenuSerializer(serializers.ModelSerializer):
    store = StoreSerializer()
    distance = serializers.SerializerMethodField()

    def get_distance(self, obj):
        return f"{obj.distance.km:.2f}"[:-1] + "km"

    class Meta:
        model = Menu
        fields = "__all__"