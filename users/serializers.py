from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "last_login", "username", "email", "date_joined", "phone"]


class UserSignInSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class UserSignInResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]


class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password", "email", "phone"]

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user
