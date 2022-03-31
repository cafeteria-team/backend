from django.urls import path

from .views import FacilityView

urlpatterns = [
    path("facility/<int:store_id>", FacilityView.as_view(), name="facility_list"),
]
