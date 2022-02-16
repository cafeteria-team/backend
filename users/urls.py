from django.urls import path
from .views import (
    UserListView,
    UserSignInView,
    UserLogoutView,
    UserRegisterView,
    UserDeleteView,
)


urlpatterns = [
    path("user", UserListView.as_view()),
    path("user/login", UserSignInView.as_view()),
    path("user/register", UserRegisterView.as_view()),
    path("user/logout", UserLogoutView.as_view()),
    path("user/<int:pk>", UserDeleteView.as_view()),
]
