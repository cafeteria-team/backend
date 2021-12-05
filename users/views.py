from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import generics, mixins

from .models import User
from .serializers import UserSerializers

from django.contrib.auth import authenticate, login


class UserListView(
    generics.GenericAPIView,
    mixins.ListModelMixin,
):
    queryset = User.objects.all()
    serializer_class = UserSerializers

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class UserAuthView(APIView):
    def post(self, request):
        user = authenticate(
            username=request.data["id"], password=request.data["password"]
        )
        if user is not None:
            login(request, user)
        else:
            return Response(status=401)
