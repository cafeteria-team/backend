from django.db import transaction

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema

from core.exceptions.exceptions import ValidateException

from .models import Facility
from .serializers import FacilityListSerializer, FacilityRegisterSerializer
from .messages import FacilityMessages


class FacilityView(generics.GenericAPIView):
    """
    편의시설 및 서비스(*)


    ---
    """

    queryset = Facility.objects.all()
    serializer_class = FacilityListSerializer
    permission_class = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        store_id = kwargs.get("store_id", None)

        if store_id == None:
            raise ValidateException(FacilityMessages.STORE_ID_PARAM_ERROR)

        queryset = self.get_queryset().filter(store_id=store_id, deleted=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class FacilityRegisterView(generics.CreateAPIView):
    """
    편의시설 및 서비스


    ---
    """

    queryset = Facility.objects.all()
    serializer_class = FacilityRegisterSerializer
    permission_class = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=FacilityRegisterSerializer(many=True),
        responses={status.HTTP_200_OK: FacilityRegisterSerializer},
    )
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        facilities = request.data

        for facility in facilities:
            count = facilities.count(facility)
            if count > 1:
                raise ValidateException(
                    FacilityMessages.FACILITY_CONFICT_ERROR.format(facility["name"])
                )

        serializer = self.get_serializer(data=facilities, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response("200")
