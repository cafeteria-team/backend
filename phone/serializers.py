from rest_framework import serializers

from users.models import User
from core.exceptions.exceptions import DuplicationException
from .models import PhoneAuthLog


class AuthPhoneSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        try:
            User.objects.get(phone=attrs["phone_num"])
            raise DuplicationException("이미 휴대전화 정보가 존재합니다. 휴대전화를 중복해서 사용할 수 없습니다.")
        except User.DoesNotExist:
            pass

        return super().validate(attrs)

    class Meta:
        model = PhoneAuthLog
        fields = ["phone_num"]
