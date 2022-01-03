from django.contrib.auth import authenticate, login

from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from drf_yasg.utils import swagger_auto_schema

from .models import User
from .serializers import (
    UserSerializer,
    UserSignUpSerializer,
    UserSignInSerializer,
    UserSignInResponseSerializer,
)


class UserListView(
    generics.GenericAPIView,
    mixins.ListModelMixin,
):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(operation_summary="유저 정보")
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
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class UserSignUpView(generics.GenericAPIView, mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSignUpSerializer

    @swagger_auto_schema(operation_summary="유저 생성")
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=200)
