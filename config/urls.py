from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from rest_framework.permissions import AllowAny

from drf_yasg import openapi
from drf_yasg.views import get_schema_view


"""Swagger Setting"""
schema_url_patterns = [
    path("api/", include("users.urls")),
    path("api/", include("phone.urls")),
]

schema_view_v1 = get_schema_view(
    openapi.Info(
        title="Open API",
        default_version="v1",
        description="시스템 API",
        terms_of_service="https://www.google.com/policies/terms/",
    ),
    public=True,
    permission_classes=[AllowAny],
    patterns=schema_url_patterns,
)

swagger_urlpatterns = [
    url(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view_v1.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    url(
        r"^swagger/$",
        schema_view_v1.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    url(
        r"^redoc/$",
        schema_view_v1.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("users.urls")),
    path("api/", include("phone.urls")),
] + swagger_urlpatterns
