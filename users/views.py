from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import generics, mixins

from .models import User
from .serializers import UserSerializers


class UserListView(
    generics.GenericAPIView,
    mixins.ListModelMixin,
):
    queryset = User.objects.all()
    serializer_class = UserSerializers

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class UserAuthView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers

    def get(self, request):
        content = {"id": "tpdnrzz", "pw": "test123!"}
        return Response(content)
