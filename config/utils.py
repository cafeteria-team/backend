from rest_framework.views import exception_handler


def custom_exception_handler(exe, context):
    response = exception_handler(exe, context)

    if response is not None:
        response.data["status_code"] = response.status_code
    return response
