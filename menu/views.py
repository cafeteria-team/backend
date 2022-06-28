from datetime import datetime, timedelta

from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance

from rest_framework import generics, status, mixins
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema
from drf_yasg.openapi import Parameter
from drf_yasg.openapi import IN_QUERY

from core.exceptions.exceptions import ValidateException
from core.pagination.pagination import CustomPagination

from menu.models import Menu

from util.trans_date import TransDate

from .models import Menu
from .serializers import (
    MenuSerializer,
    MenuCreateSerializer,
    MenuUpdateSerializer,
    NearbyTodayMenuSerializer,
)

from .filters import MenuFilter


class MenuView(generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    lookup_field = "store_id"
    lookup_url_kwarg = "store_id"
    pagination_class = CustomPagination
    filterset_class = MenuFilter

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "GET":
            return MenuSerializer
        elif self.request.method == "POST":
            return MenuCreateSerializer

    @swagger_auto_schema(operation_summary="메뉴 리스트 조회(*)")
    def get(self, request, *args, **kwargs):
        store_id = kwargs.get("store_id", None)
        queryset = self.filter_queryset(self.get_queryset().filter(store_id=store_id))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(operation_summary="메뉴 생성(*)")
    def post(self, request, *args, **kwargs):
        store_id = kwargs.get("store_id", None)

        if store_id == None:
            raise ValidateException("Store id is required in path")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(store_id=store_id)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class MenuDetailView(
    generics.GenericAPIView, mixins.DestroyModelMixin, mixins.UpdateModelMixin
):
    queryset = Menu.objects.all()
    serializer_class = MenuUpdateSerializer
    lookup_field = "id"
    lookup_url_kwarg = "menu_id"

    @swagger_auto_schema(operation_summary="메뉴 상세 수정(*)")
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="메뉴 삭제(*)")
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class MenuTodayListView(generics.ListAPIView):
    serializer_class = MenuSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        today_start_date = datetime.combine(datetime.today(), datetime.min.time())
        today_end_date = datetime.combine(
            datetime.today() + timedelta(days=1), datetime.min.time()
        ) - timedelta(seconds=1)

        queryset = Menu.objects.filter(
            provide_at__range=(today_start_date, today_end_date)
        )
        return queryset

    @swagger_auto_schema(operation_summary="메뉴 리스트(오늘)(*)")
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class NearbyTodayMenusView(generics.ListAPIView):
    serializer_class = NearbyTodayMenuSerializer
    pagination_class = CustomPagination

    lat_param = Parameter(
        "lat",
        IN_QUERY,
        type="string",
        required=True,
        description="위도",
    )
    lon_param = Parameter(
        "lon",
        IN_QUERY,
        type="string",
        required=True,
        description="경도",
    )

    def get_queryset(self):
        try:
            lat = float(self.request.GET["lat"])
        except ValueError:
            raise ValidateException("Latitude's type must be float")

        try:
            lon = float(self.request.GET["lon"])
        except ValueError:
            raise ValidateException("Longitude's type must be float")

        point = Point(lat, lon, srid=4326)

        trans_date = TransDate(datetime.now())
        today_start_date = trans_date.get_today_min()
        today_end_date = trans_date.get_today_max()

        today_menus = (
            Menu.objects.filter(
                provide_at__range=(today_start_date, today_end_date),
                store__location__distance_lte=(point, D(km=5)),
            )
            .annotate(distance=Distance("store__location", point))
            .order_by("distance")
        )
        return today_menus

    @swagger_auto_schema(
        operation_summary="내 주변 구내식당 정보",
        operation_description="현재 날짜 기준으로 5KM 반경 내에 메뉴가 등록되어 있는 구내삭당들의 메뉴 정보를 가지고 오는 API",
        manual_parameters=[lat_param, lon_param],
        tags=["menu"],
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
