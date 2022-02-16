from rest_framework import status
from rest_framework.exceptions import APIException


class DuplicationException(APIException):
    status_code = status.HTTP_409_CONFLICT

    def __init__(self, detail=None):
        super().__init__(detail=detail)
