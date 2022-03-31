from django.db import transaction

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema

from core.exceptions.exceptions import ValidateException, DuplicationException

from .models import Facility
from .serializers import FacilityListSerializer, FacilityRegisterSerializer
from .messages import FacilityMessages


class FacilityView(generics.ListCreateAPIView):
    """
    편의시설 및 서비스(*)


    ---
    """

    permission_class = [IsAuthenticated]
    lookup_url_kwarg = "store_id"

    def get_queryset(self):
        store_id = self.kwargs.get(self.lookup_url_kwarg, "None")
        if getattr(self, "swagger_fake_view", False):
            return Facility.objects.none()

        if store_id == None:
            raise ValidateException(FacilityMessages.GET_FACILITY_ERROR)
        queryset = Facility.objects.filter(store_id=store_id, deleted=False)

        return queryset

    def get_serializer_class(self):
        method = self.request.method
        if method == "GET":
            return FacilityListSerializer
        elif method == "POST":
            return FacilityRegisterSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=FacilityRegisterSerializer(many=True),
        responses={status.HTTP_200_OK: FacilityRegisterSerializer},
    )
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        facilities = request.data
        store_id = kwargs.get("store_id", None)

        for facility in facilities:
            count = facilities.count(facility)
            if count > 1:
                raise ValidateException(
                    FacilityMessages.FACILITY_CONFICT_ERROR.format(facility["name"])
                )

            facility_exists = queryset.filter(name=facility["name"])

            if facility_exists.exists():
                raise DuplicationException(
                    FacilityMessages.ALREADY_EXISTS_ERROR.format(
                        facility["name"], facility["name"]
                    )
                )

        serializer = self.get_serializer(data=facilities, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(store_id=store_id)

        return Response(FacilityMessages.CREAT_SUCCESS)
