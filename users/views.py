from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User


class UserListView(APIView):
    queryset = User.objects.all()

    def get(self, request):
        users = User.objects.all()
        return Response(users)


class UserAuthView(APIView):
    queryset = User.objects.all()

    def get(self, request):
        content = {"id": "tpdnrzz", "pw": "test123!"}
        return Response(content)
