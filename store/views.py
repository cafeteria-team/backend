from django.db import transaction

from rest_framework import generics, status, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from drf_yasg.utils import swagger_auto_schema
from core.exceptions.exceptions import ValidateException

from core.permissions.permissions import AdminPermission
from store.messages import FacilityMessages
from store.models import Store

from .models import Facility, JoinFacility
from .serializers import (
    FacilityAdminSerializer,
    FacilityAdminRegisterSerializer,
    FacilityAdminDetailUpdateSerializer,
    StoreWithFacility,
    JoinFacilityCreateSerializer,
    StorePriceSerializer,
)

from .manager import FacilityManager


class FacilityAdminView(generics.ListCreateAPIView):
    """
    편의시설 및 서비스(*)


    ---
    """

    queryset = Facility.objects.exclude(deleted=True)
    serializer_class = FacilityAdminSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            permission_classes = [AllowAny]
        else:
            permission_classes = [AdminPermission]

        return [permission() for permission in permission_classes]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=FacilityAdminRegisterSerializer,
        responses={status.HTTP_200_OK: FacilityAdminSerializer},
    )
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        data = request.data
        facility_manager = FacilityManager()
        facility_manager.exists_check(data=data)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class FacilityAdminDetailView(
    generics.GenericAPIView, mixins.UpdateModelMixin, mixins.DestroyModelMixin
):
    """
    편의시설 및 서비스(*)


    ---
    """

    queryset = Facility.objects.all()
    serializer_class = FacilityAdminDetailUpdateSerializer
    permission_class = [AllowAny]
    lookup_field = "id"
    lookup_url_kwarg = "facility_id"

    def patch(self, request, *args, **kwargs):
        facility_id = kwargs.get("facility_id", None)
        data = request.data
        facility_manager = FacilityManager()
        facility_manager.exists_check(data=data, facility_id=facility_id)
        return super().update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.deleted = True
        instance.save()
        return Response(FacilityMessages.DELETE_SUCCESS)


class FacilityJoinView(
    generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.CreateModelMixin
):
    queryset = Store.objects.all()
    lookup_field = "id"
    lookup_url_kwarg = "store_id"

    def get_serializer_class(self):
        if self.request.method == "GET":
            return StoreWithFacility
        else:
            return JoinFacilityCreateSerializer

    @swagger_auto_schema(operation_summary="업체 편의시설 리스트(*)")
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="업체 편의시설 등록(*)")
    def post(self, request, *args, **kwargs):
        store_id = kwargs.get("store_id", None)
        if store_id == None:
            raise ValidateException("Store id is required!")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(store_id=store_id)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class FacilityJoinDetailView(generics.DestroyAPIView):
    def get_object(self):
        kwargs = self.request.parser_context.get("kwargs", None)

        if kwargs == None:
            raise ValidateException(
                "Need store_id and join_facility_id is required in path"
            )

        try:
            join_facility = JoinFacility.objects.get(
                store_id=kwargs["store_id"], id=kwargs["join_facility_id"]
            )
        except:
            raise ValidateException("Join facility not found")

        return join_facility

    @swagger_auto_schema(operation_summary="업체 편의시설 삭제(*)")
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class StorePriceView(
    generics.GenericAPIView,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
):
    queryset = Store.objects.all()
    serializer_class = StorePriceSerializer
    lookup_field = "id"
    lookup_url_kwarg = "store_id"

    @swagger_auto_schema(operation_summary="가격 정보(*)")
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="가격 생성(*)")
    def post(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="가격 수정(*)")
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="가격 일괄 삭제(*)")
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.price = None
        instance.save()

        data = {"price": instance.price}

        return Response(data=data, status=status.HTTP_200_OK)
