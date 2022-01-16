from rest_framework import serializers


from .models import User
from store.models import Store
from store.serializers import StoreSerializer


class UserSerializer(serializers.ModelSerializer):
    store = StoreSerializer()

    class Meta:
        model = User
        fields = ["id", "username", "email", "phone", "role", "store"]


class UserSignInSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class UserSignInResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]


class UserRegisterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=128, source="store.name")
    addr = serializers.CharField(max_length=128, source="store.addr")
    zip_code = serializers.CharField(max_length=6, source="store.zip_code")
    detail_addr = serializers.CharField(max_length=128, source="store.detail_addr")
    busi_num = serializers.CharField(
        max_length=10, source="store.busi_num", required=False
    )
    busi_num_img = serializers.CharField(max_length=256, source="store.busi_num_img")

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "email",
            "phone",
            "role",
            "name",
            "addr",
            "zip_code",
            "detail_addr",
            "busi_num",
            "busi_num_img",
        ]

    def create(self, validated_data):
        user = User()
        user_roles = User.UserRoles

        user.username = validated_data["username"]
        user.set_password(validated_data["password"])
        user.email = validated_data["email"]
        user.phone = validated_data["phone"]

        if validated_data["role"] == user_roles.ADMIN:
            user.is_active = True
        else:
            user.is_active = False

        user.save()

        store_data = validated_data["store"]
        store_data["user"] = user

        store = Store(**store_data)
        store.save()

        return validated_data


class UserRegisterResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]
