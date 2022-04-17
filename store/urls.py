from django.urls import path

from .views import (
    FacilityAdminView,
    FacilityAdminDetailView,
    FacilityJoinView,
    FacilityJoinDetailView,
)

urlpatterns = [
    path(
        "facility",
        FacilityAdminView.as_view(),
        name="facility_admin",
    ),
    path(
        "facility/<int:facility_id>",
        FacilityAdminDetailView.as_view(),
        name="facility_admin_detail",
    ),
    path(
        "facility/join/<int:store_id>",
        FacilityJoinView.as_view(),
        name="facility_join",
    ),
    path(
        "facility/join/<int:store_id>/<int:join_facility_id>",
        FacilityJoinDetailView.as_view(),
        name="facility_join",
    ),
]
