from django.urls import path
from .views import NoticeView, NoticeCreateView

urlpatterns = [
    path("notice/<int:user_id>", NoticeView.as_view(), name="notice"),
    path("notice/", NoticeCreateView.as_view(), name="notice_create"),
]
