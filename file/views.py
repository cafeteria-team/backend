import boto3

from django.conf import settings

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .messages import FileMessage


class FileUploadView(generics.GenericAPIView):
    """
    파일 업로드(*)


    ---
    """

    parser_classes = (MultiPartParser,)
    permission_class = [IsAuthenticated]

    files = openapi.Parameter(
        "files",
        in_=openapi.IN_FORM,
        description="upload files",
        type=openapi.TYPE_ARRAY,
        items=openapi.Items(type=openapi.TYPE_FILE),
        required=True,
    )

    @swagger_auto_schema(
        manual_parameters=[files],
        responses={status.HTTP_200_OK: FileMessage.UPLOAD_SUCCESS},
    )
    def post(self, request, *args, **kwargs):
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        files = request.FILES.getlist("files")

        for file in files:
            s3_client.upload_fileobj(
                file,
                settings.AWS_STORAGE_BUCKET_NAME,
                f"media/{request.user}/{file.name}",
                ExtraArgs={
                    "ContentType": file.content_type,
                },
            )

        return Response(FileMessage.UPLOAD_SUCCESS)
