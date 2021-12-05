from django.urls import path
from .views import UserListView, UserLoginView, UserSignUpView


urlpatterns = [
    path("user", UserListView.as_view()),
    path("user/login", UserLoginView.as_view()),
    path("user/sign-up", UserSignUpView.as_view()),
]
