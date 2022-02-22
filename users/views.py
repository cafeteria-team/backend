from django.db import transaction
from django.contrib.auth import authenticate, login, logout

from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema

from core.permissions.permissions import AdminPermission
from core.pagination.pagination import CustomPagination

from .models import User
from .serializers import (
    UserSerializer,
    UserRegisterSerializer,
    UserRegisterResponseSerializer,
    UserSignInSerializer,
    UserSignInResponseSerializer,
    UserDetailSerializer,
    UserDetailUpdateSerializer,
)


class UserListView(
    generics.GenericAPIView,
    mixins.ListModelMixin,
):

    queryset = User.objects.exclude(is_superuser=True)
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    @swagger_auto_schema(operation_summary="유저 리스트")
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class UserSignInView(generics.GenericAPIView):
    serializer_class = UserSignInSerializer

    @swagger_auto_schema(
        operation_summary="로그인",
        responses={status.HTTP_200_OK: UserSignInResponseSerializer},
    )
    def post(self, request):
        serializer = UserSignInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = request.data["username"]
        password = request.data["password"]

        user = authenticate(request, username=username, password=password)

        if user == None:
            raise NotFound(
                "Authentication failed.\nPlease check your username or password data"
            )

        login(request, user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UserRegisterView(generics.GenericAPIView, mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

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
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
):

    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserDetailSerializer

    def get_object(self, pk):
        try:
            user = User.objects.get(pk=pk)
            return user
        except User.DoesNotExist:
            raise NotFound("유저 정보를 찾을 수 없습니다. 확인 후 다시 시도해주세요.")

    @swagger_auto_schema(
        operation_summary="사용자 정보",
        responses={status.HTTP_200_OK: UserDetailSerializer()},
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="사용자 정보 수정",
        request_body=UserDetailUpdateSerializer(),
        responses={status.HTTP_200_OK: "사용자 정보 수정 완료"},
    )
    @transaction.atomic
    def patch(self, request, pk):
        user = self.get_object(pk)
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
        user = self.get_object(pk)
        user.delete()
        msg = {"msg": "사용자 정보가 삭제되었습니다."}
        return Response(msg)
