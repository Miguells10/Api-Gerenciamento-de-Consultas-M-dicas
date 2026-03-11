"""
JWT auth URL configuration.
Exposes token obtain and refresh endpoints.
"""

from django.urls import path
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

_TAG = ["Autenticação"]

urlpatterns = [
    path(
        "token/",
        extend_schema(summary="Obter token de acesso (JWT)", tags=_TAG)(
            TokenObtainPairView.as_view()
        ),
        name="token_obtain_pair",
    ),
    path(
        "token/refresh/",
        extend_schema(summary="Renovar token de acesso", tags=_TAG)(
            TokenRefreshView.as_view()
        ),
        name="token_refresh",
    ),
]
