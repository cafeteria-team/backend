from django.urls import path
from .views import NoticeView, NoticeDetailView, NoticeAdminView, NoticeAdminDetailView

urlpatterns = [
    path("notice/<int:store_id>", NoticeView.as_view(), name="notice"),
    path(
        "notice/<int:store_id>/<int:notice_id>",
        NoticeDetailView.as_view(),
        name="notice_detail",
    ),
    path("notice/admin", NoticeAdminView.as_view(), name="notice_admin"),
    path(
        "notice/admin/<int:notice_id>",
        NoticeAdminDetailView.as_view(),
        name="notice_admin_detail",
    ),
]
