from django.urls import path
from .views import UserListView, UserSignInView, UserSignUpView, UserLogoutView


urlpatterns = [
    path("user", UserListView.as_view()),
    path("user/login", UserSignInView.as_view()),
    path("user/sign-up", UserSignUpView.as_view()),
    path("user/logout", UserLogoutView.as_view()),
]
