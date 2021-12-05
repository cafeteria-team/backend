from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import generics, mixins

from .models import User
from .serializers import UserSerializers, UserSignUpSerializers

from django.contrib.auth import authenticate, login


class UserListView(generics.GenericAPIView, mixins.ListModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializers

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class UserLoginView(APIView):
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
    serializer_class = UserSignUpSerializers

    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]
        email = request.data["email"]
        try:
            user = User.objects.get(username=username)
            raise ValidationError("User already exists!")
        except User.DoesNotExist:

            user = User.objects.create(
                username=username, password=password, email=email
            )
            print(user)

            return Response(status=200, data={"id": user.username})
