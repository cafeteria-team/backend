from django.urls import path
from .views import UserListView, UserAuthView


urlpatterns = [
    path("user", UserListView.as_view()),
    path("user-auth", UserAuthView.as_view()),
]
