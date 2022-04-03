from django.urls import path

from .views import FacilityAdminView, FacilityAdminDetailView

urlpatterns = [
    path("facility", FacilityAdminView.as_view(), name="facility_admin"),
    path(
        "facility/<int:facility_id>",
        FacilityAdminDetailView.as_view(),
        name="facility_admin_detail",
    ),
]
