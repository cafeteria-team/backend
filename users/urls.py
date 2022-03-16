from django.urls import path

from .views import (
    UserListView,
    UserLoginView,
    UserLogoutView,
    UserRegisterView,
    UserDetailView,
    UserSecession,
    CustomUserRefreshTokenView,
)


urlpatterns = [
    path("user", UserListView.as_view(), name="user_lists"),
    path("user/login", UserLoginView.as_view(), name="user_login"),
    path("user/register", UserRegisterView.as_view(), name="user_register"),
    path("user/logout", UserLogoutView.as_view(), name="user_logout"),
    path("user/<int:pk>", UserDetailView.as_view(), name="user_detail"),
    path("user/<int:pk>/secession", UserSecession.as_view(), name="user_sign_out"),
    path(
        "user/token/refresh/",
        CustomUserRefreshTokenView.as_view(),
        name="token_refresh",
    ),
]
