from django.urls import path

from .views import FacilityView, FacilityRegisterView

urlpatterns = [
    path("facility", FacilityRegisterView.as_view(), name="facility_register"),
    path("facility/<int:store_id>", FacilityView.as_view(), name="facility_list"),
]
