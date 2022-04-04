from django.db import transaction

from rest_framework import generics, status, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from drf_yasg.utils import swagger_auto_schema

from core.permissions.permissions import AdminPermission
from store.messages import FacilityMessages

from .models import Facility
from .serializers import (
    FacilityAdminSerializer,
    FacilityAdminRegisterSerializer,
    FacilityAdminDetailUpdateSerializer,
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
            permission_classes = [IsAuthenticated]
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
    queryset = Facility.objects.all()
    serializer_class = FacilityAdminDetailUpdateSerializer
    permission_class = [AdminPermission]
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
        return Response(FacilityMessages.DELETE_SUCCESS)
