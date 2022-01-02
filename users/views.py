from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, mixins
from drf_yasg.utils import swagger_auto_schema

from .models import User
from .serializers import UserSerializer, UserSignUpSerializer, UserSignInSerializer

from django.contrib.auth import authenticate, login


class UserListView(
    generics.GenericAPIView,
    mixins.ListModelMixin,
):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(operation_summary="유저 정보")
    def get(self, request, *args, **kwargs):

        return self.list(request, *args, **kwargs)


class UserSignInView(APIView):
    serializer_class = UserSignInSerializer

    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response(
                status=200,
            )
        else:
            return Response(status=401)


class UserSignUpView(generics.GenericAPIView, mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSignUpSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=200)
