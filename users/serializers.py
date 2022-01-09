from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User
from store.models import Store
from store.serializers import StoreSerializer


class UserSerializer(serializers.ModelSerializer):
    store = StoreSerializer()

    class Meta:
        model = User
        fields = [
            "id",
            "last_login",
            "username",
            "email",
            "date_joined",
            "phone",
            "store",
        ]


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
        user.save()

        store = Store()
        store.user_id = user.id
        store.addr = validated_data["store"]["addr"]
        store.zip_code = validated_data["store"]["zip_code"]
        store.detail_addr = validated_data["store"]["detail_addr"]
        store.busi_num = validated_data["store"]["busi_num"]
        store.save()

        return validated_data
