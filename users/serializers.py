from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User
from store.models import Store
from store.serializers import StoreSerializer


class UserSerializer(serializers.ModelSerializer):
    store = StoreSerializer()

    class Meta:
        model = User
        fields = "__all__"


class UserSignInSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class UserSignInResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]


class UserRegisterSerializer(serializers.ModelSerializer):
    store = StoreSerializer()

    class Meta:
        model = User
        fields = ["id", "username", "password", "email", "phone", "store"]

    def create(self, validated_data):
        user = User()
        user.username = validated_data["username"]
        user.set_password(validated_data["password"])
        user.email = validated_data["email"]
        user.phone = validated_data["phone"]
        user.save()

        return validated_data
