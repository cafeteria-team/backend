from datetime import datetime, timedelta
from rest_framework import generics, status, mixins
from rest_framework.response import Response

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

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

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

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

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

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
