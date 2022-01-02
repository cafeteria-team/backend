from django.urls import path
from .views import UserListView, UserSignInView, UserSignUpView


urlpatterns = [
    path("user", UserListView.as_view()),
    path("user/sign-in", UserSignInView.as_view()),
    path("user/sign-up", UserSignUpView.as_view()),
]
