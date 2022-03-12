from django.db import transaction

from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


from drf_yasg.utils import swagger_auto_schema
from drf_yasg.openapi import Parameter
from drf_yasg.openapi import IN_QUERY
from drf_yasg.openapi import TYPE_STRING

from phone.models import PhoneAuthLog
from core.exceptions.exceptions import ValidateException, NotFoundException

from .manager import PhoneManager
from .serializers import AuthPhoneSerializer
from .models import PhoneAuthLog


class SmsAuth(generics.GenericAPIView):
    queryset = PhoneAuthLog.objects.exclude(confirmed=True)
    serializer_class = AuthPhoneSerializer
    permission_classes = [AllowAny]

    phone_num_param = Parameter(
        name="phone_num",
        in_=IN_QUERY,
        description="휴대전화 번호",
        required=True,
        type=TYPE_STRING,
    )
    auth_num_param = Parameter(
        name="auth_num",
        in_=IN_QUERY,
        description="인증번호",
        required=True,
        type=TYPE_STRING,
    )

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: "인증 완료"},
        manual_parameters=[phone_num_param, auth_num_param],
    )
    def get(self, request, *args, **kwargs):
        """
        인증번호 조회


        ----
        """
        phone_num = request.query_params.get("phone_num")
        auth_num = request.query_params.get("auth_num")

        if phone_num == None or auth_num == None:
            raise ValidateException("정상적인 요청이 아닙니다. 휴대전화 및 인증번호를 확인하세요.")

        queryset = self.get_queryset().filter(phone_num=phone_num)

        if queryset.exists():
            recent_auth_phone = queryset.last()

            if recent_auth_phone.auth_num == auth_num:
                return Response("인증 완료")
            else:
                raise ValidateException("인증번호가 다릅니다. 확인 후 다시 시도해주세요.")
        else:
            raise NotFoundException("인증정보를 찾을 수 없습니다. 인증요청을 다시 시도해주세요.")

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: "인증번호가 발급되었습니다."},
    )
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """
        인증번호 발송

        ---
        - phone_num: 휴대전화 번호
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_num = serializer.data["phone_num"]
        phone_manager = PhoneManager()
        phone_manager.send_sms(phone_num)

        return Response("success")
