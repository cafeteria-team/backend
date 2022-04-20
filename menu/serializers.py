from rest_framework import serializers

from .models import Menu


class MenuSerializer(serializers.ModelSerializer):
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
