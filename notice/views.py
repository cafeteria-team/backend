from django.db import transaction

from rest_framework import generics, status, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema

from core.exceptions.exceptions import ValidateException, NotFoundException
from .models import Notice
from .serializers import (
    NoticeSerializer,
    NoticeCreateSerializer,
    NoticeUpdateSerializer,
)


class NoticeView(generics.ListCreateAPIView):
    """
    공지사항 검색(*)
    """

    queryset = Notice.objects.exclude(deleted=True)
    permission_classes = [IsAuthenticated]
    lookup_field = "store_id"
    lookup_url_kwarg = "store_id"

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "GET":
            return NoticeSerializer
        elif self.request.method == "POST":
            return NoticeCreateSerializer

    @swagger_auto_schema(operation_summary="공지사항 리스트(*)")
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="공지사항 등록(*)")
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        user = request.user
        store_id = kwargs.get("store_id", None)

        if store_id == None:
            raise ValidateException("Store id is required in path")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(store_id=store_id, created_by=user)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class NoticeDetailView(
    generics.GenericAPIView, mixins.UpdateModelMixin, mixins.DestroyModelMixin
):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "PATCH":
            return NoticeUpdateSerializer

    def get_object(self):
        kwargs = self.request.parser_context.get("kwargs", None)

        if kwargs == None:
            raise ValidateException("Need store_id and notice_id is required in path")

        try:
            notice = Notice.objects.get(
                store_id=kwargs["store_id"], id=kwargs["notice_id"]
            )
        except:
            raise ValidateException("Notice not found")

        return notice

    @swagger_auto_schema(operation_summary="공지사항 수정(*)")
    @transaction.atomic
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="공지사항 삭제(*)")
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.deleted = True
        instance.save()
        return Response("200")
