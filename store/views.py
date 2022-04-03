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

    queryset = Facility.objects.all()
    serializer_class = FacilityAdminSerializer
    permission_class = [IsAuthenticated, AdminPermission]

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
    permission_class = [IsAuthenticated, AdminPermission]
    lookup_field = "id"
    lookup_url_kwarg = "facility_id"

    def patch(self, request, *args, **kwargs):
        data = request.data
        facility_manager = FacilityManager()
        facility_manager.exists_check(data=data)
        return super().update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.deleted = True

        return Response(FacilityMessages.DELETE_SUCCESS)


# class FacilityStoreView(generics.ListCreateAPIView):
#     """
#     편의시설 및 서비스(*)


#     ---
#     """

#     # permission_class = [IsAuthenticated, AdminPermission]
#     permission_class = [AllowAny]
#     lookup_url_kwarg = "store_id"

#     def get_queryset(self):
#         store_id = self.kwargs.get(self.lookup_url_kwarg, "None")

#         """
#         Swagger 오류로 인해 소스코드를 추가했지만 해당 코드에 대해서 정확히 파악하지 못함

#         Error
#         =====
#         UserWarning: <class 'store.views.FacilityView'> is not compatible with schema generation
#         """
#         if getattr(self, "swagger_fake_view", False):
#             return Facility.objects.none()

#         if store_id == None:
#             raise ValidateException(FacilityMessages.GET_FACILITY_ERROR)
#         queryset = Facility.objects.filter(store_id=store_id, deleted=False)

#         return queryset

#     def get_serializer_class(self):
#         method = self.request.method
#         if method == "GET":
#             return FacilityListSerializer
#         elif method == "POST":
#             return FacilityRegisterSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     @swagger_auto_schema(
#         request_body=FacilityRegisterSerializer(many=True),
#         responses={status.HTTP_200_OK: FacilityRegisterSerializer},
#     )
#     @transaction.atomic
#     def post(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         facilities = request.data
#         store_id = kwargs.get("store_id", None)

#         for facility in facilities:
#             count = facilities.count(facility)
#             if count > 1:
#                 raise ValidateException(
#                     FacilityMessages.FACILITY_CONFICT_ERROR.format(facility["name"])
#                 )

#             facility_exists = queryset.filter(name=facility["name"])

#             if facility_exists.exists():
#                 raise DuplicationException(
#                     FacilityMessages.ALREADY_EXISTS_ERROR.format(
#                         facility["name"], facility["name"]
#                     )
#                 )

#         serializer = self.get_serializer(data=facilities, many=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save(store_id=store_id)

#         return Response(FacilityMessages.CREAT_SUCCESS)
