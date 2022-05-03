from django.urls import path

from .views import FileUploadView


urlpatterns = [
    path("file/upload", FileUploadView.as_view(), name="file_upload"),
]
