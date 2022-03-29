from django.urls import path

from .views import SmsAuth, PhoneAuthFindPasswordView

urlpatterns = [
    path("phone/auth", SmsAuth.as_view(), name="sms_auth"),
    path(
        "phone/auth/password",
        PhoneAuthFindPasswordView.as_view(),
        name="phone_auth_find_password",
    ),
]
