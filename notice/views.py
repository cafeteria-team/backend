from django.db import transaction

from rest_framework import generics
from rest_framework.response import Response

from .models import Notice
from .serializers import NoticeSerializer, NoticeCreateSerializer


class NoticeView(generics.GenericAPIView):
    serializer_class = NoticeSerializer

    def get_queryset(self, user_id):
        notices = Notice.objects.filter(created_by=user_id)
        return notices

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset(user_id=kwargs["user_id"])
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class NoticeCreateView(generics.CreateAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeCreateSerializer

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
