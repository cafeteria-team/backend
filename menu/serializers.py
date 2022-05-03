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
