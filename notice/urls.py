from django.urls import path
from .views import NoticeView, NoticeDetailView

urlpatterns = [
    path("notice/<int:store_id>", NoticeView.as_view(), name="notice"),
    path(
        "notice/<int:store_id>/<int:notice_id>",
        NoticeDetailView.as_view(),
        name="notice_detail",
    ),
]
