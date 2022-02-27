from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)

from store.models import Store
from store.serializers import MemberStoreSerializer, MemberDetailStoreSerialzer

from core.exceptions.exceptions import DuplicationException, ValidateException

from .models import User
from .manager import UserMananger


class UserSerializer(serializers.ModelSerializer):
    store = MemberStoreSerializer()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "phone",
            "role",
            "store",
            "date_joined",
            "is_active",
        ]


class UserSignInSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["user_id"] = user.id
        return token


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
    confirm_password = serializers.CharField(max_length=128)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "confirm_password",
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

    def validate(self, attrs):
        password = attrs["password"]
        confirm_password = attrs["confirm_password"]
        email = attrs["email"]
        busi_num = attrs["store"]["busi_num"]
        zip_code = attrs["store"]["zip_code"]

        if password != confirm_password:
            msg = "패스워드가 동일하지 않습니다. 다시 확인해주세요."
            raise ValidationError(msg)

        try:
            User.objects.get(email=email)
            msg = "해당 이메일은 이미 가입되어있습니다. 확인 후 다시 시도해주세요."
            raise DuplicationException(msg)
        except User.DoesNotExist:
            pass

        store = Store.objects.filter(busi_num=busi_num)

        try:
            busi_num = int(busi_num)
        except:
            msg = {"msg": "사업자 번호는 숫자만 사용할 수 있습니다."}
            raise ValidationError(msg)

        if store.exists():
            store = store.first()
            msg = {"msg": "사업자 번호가 이미 존재합니다. 확인 후 다시 시도해주세요."}
            raise DuplicationException(msg)

        try:
            zip_code = int(zip_code)
        except:
            msg = "우편번호는 숫자만 사용할 수 있습니다."
            raise ValidationError(msg)

        return super().validate(attrs)

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


class UserDetailSerializer(serializers.ModelSerializer):
    store = MemberDetailStoreSerialzer()

    class Meta:
        model = User
        fields = ["username", "email", "store"]


class UserDetailUpdateSerializer(serializers.ModelSerializer):
    store = MemberDetailStoreSerialzer()

    class Meta:
        model = User
        fields = ["email", "store"]

    def update(self, instance, validated_data):
        user = User.objects.filter(email=validated_data["email"])
        if user.exists():
            msg = "해당 이메일은 이미 중복입니다. 확인 후 다시 시도해주세요"
            raise DuplicationException(msg)

        type_check_busi_num = UserMananger.type_check_busi_num(
            busi_num=validated_data["store"]["busi_num"]
        )

        if not type_check_busi_num:
            msg = "사업자 번호는 숫자만 사용할 수 있습니다."
            raise ValidateException(msg)

        instance.email = validated_data["email"]
        instance.store.name = validated_data["store"]["name"]
        instance.store.busi_num = validated_data["store"]["busi_num"]
        instance.save()
        return instance


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        return super().validate(attrs)
