from django.urls import path

from .views import MenuView, MenuDetailView, MenuTodayListView, NearbyTodayMenusView


urlpatterns = [
    path("menu/<int:store_id>", MenuView.as_view(), name="menu_list"),
    path(
        "menu/<int:store_id>/<int:menu_id>",
        MenuDetailView.as_view(),
        name="menu_detail",
    ),
    path("menu/today", MenuTodayListView.as_view(), name="menu_today_list"),
    path(
        "nearby/today/menus", NearbyTodayMenusView.as_view(), name="nearby_today_menus"
    ),
]
