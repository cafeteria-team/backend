from django.urls import path

from .views import SmsAuth

urlpatterns = [
    path("phone/auth", SmsAuth.as_view(), name="sms_auth"),
]
