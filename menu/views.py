from datetime import datetime, timedelta

from rest_framework import generics, status, mixins
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from core.exceptions.exceptions import ValidateException
from core.pagination.pagination import CustomPagination
from .models import Menu
from .serializers import MenuSerializer, MenuCreateSerializer, MenuUpdateSerializer


class MenuView(generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    lookup_field = "store_id"
    lookup_url_kwarg = "store_id"
    pagination_class = CustomPagination

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "GET":
            return MenuSerializer
        elif self.request.method == "POST":
            return MenuCreateSerializer

    @swagger_auto_schema(operation_summary="메뉴 리스트 조회(*)")
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

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
