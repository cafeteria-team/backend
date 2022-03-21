from django.db import transaction
from django.db.models import Q
from django.contrib.auth import logout


from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from drf_yasg.utils import swagger_auto_schema

from core.permissions.permissions import AdminPermission
from core.pagination.pagination import CustomPagination
from core.exceptions.exceptions import NotFoundException

from .models import User
from .serializers import (
    UserSerializer,
    UserRegisterSerializer,
    UserRegisterResponseSerializer,
    UserSignInSerializer,
    UserDetailSerializer,
    UserDetailUpdateSerializer,
    CustomTokenRefreshSerializer,
    UserApproveSerializer,
)

# generics.ListAPIView: 쿼리셋을 리스트 형태로 나열하기 위한 함수 (GET)
#


class UserListView(
    generics.ListAPIView,
):
    """
    유저 리스트


    page = 페이지 숫자
    page_size = 페이지 내 표현해야할 사이즈
    """

    queryset = User.objects.exclude(Q(is_superuser=True) | Q(deleted=True))
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, AdminPermission]
    pagination_class = CustomPagination


class UserLoginView(TokenObtainPairView):

    serializer_class = UserSignInSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="로그인(토큰 발급)",
    )
    def post(self, request, *args, **kwargs):
        username = request.data["username"]

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFoundException("사용자 정보를 찾을 수 없습니다.")

        if user.is_active:
            return super().post(request, *args, **kwargs)

        else:
            data = {"msg": "사용자 계정이 활성화 되지 않았습니다. 관리자에게 문의하세요."}
            return Response(data=data, status=status.HTTP_200_OK)


class CustomUserRefreshTokenView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="토큰 갱신",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserRegisterView(generics.GenericAPIView, mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="유저 생성",
        responses={status.HTTP_201_CREATED: UserRegisterResponseSerializer},
    )
    @transaction.atomic
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = {"msg": "회원가입에 성공하였습니다."}
        return Response(data=data, status=status.HTTP_201_CREATED)


class UserLogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="로그 아웃",
        responses={status.HTTP_200_OK: "User logged out"},
    )
    def get(self, request):
        logout(request)
        return Response(data="User logged out", status=status.HTTP_200_OK)


class UserDetailView(
    generics.GenericAPIView,
    mixins.UpdateModelMixin,
):

    permission_classes = [IsAuthenticated]
    serializer_class = UserDetailSerializer

    def get_queryset(self, pk):
        try:
            user = User.objects.get(id=pk)
            return user
        except User.DoesNotExist:
            raise NotFound("유저 정보를 찾을 수 없습니다. 확인 후 다시 시도해주세요.")

    @swagger_auto_schema(
        operation_summary="사용자 정보",
        responses={status.HTTP_200_OK: UserDetailSerializer()},
    )
    def get(self, request, pk):
        queryset = self.get_queryset(pk=pk)
        serializer = self.get_serializer(queryset)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="사용자 정보 수정",
        request_body=UserDetailUpdateSerializer(),
        responses={status.HTTP_200_OK: "사용자 정보 수정 완료"},
    )
    @transaction.atomic
    def patch(self, request, pk):
        user = self.get_queryset(pk=pk)
        serializer = UserDetailUpdateSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        msg = {"msg": "사용자 정보가 수정되었습니다."}
        return Response(msg)

    @swagger_auto_schema(
        operation_summary="사용자 삭제",
        responses={status.HTTP_200_OK: "사용자 정보가 삭제되었습니다."},
    )
    @transaction.atomic
    def delete(self, request, pk):
        user = self.get_queryset(pk)
        user.deleted = True
        user.save()
        msg = {"msg": "사용자 정보가 삭제되었습니다."}
        return Response(msg)


class UserApproveView(generics.GenericAPIView, mixins.UpdateModelMixin):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserApproveSerializer

    @swagger_auto_schema(
        operation_summary="사용자 승인 요청",
    )
    @transaction.atomic
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
