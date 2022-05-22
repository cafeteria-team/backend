import boto3

from django.conf import settings

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .messages import FileMessage
from .manager import FileManager


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
        file_manager = FileManager()
        s3_client = file_manager.get_s3_client()
        files = request.FILES.getlist("files")

        results = []

        for file in files:
            s3_path = f"media/{request.user}/{file.name}"
            s3_client.upload_fileobj(
                file,
                settings.AWS_STORAGE_BUCKET_NAME,
                s3_path,
                ExtraArgs={
                    "ContentType": file.content_type,
                },
            )
            location = s3_client.get_bucket_location(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME
            )["LocationConstraint"]

            image_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{location}.amazonaws.com/{s3_path}"

            results.append(image_url)

        return Response(data=results, status=status.HTTP_200_OK)
