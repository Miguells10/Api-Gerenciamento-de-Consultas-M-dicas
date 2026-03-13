from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

_TAG = ["Autenticação"]


@extend_schema_view(
    post=extend_schema(summary="Obter token de acesso (JWT)", tags=_TAG)
)
class CustomTokenObtainPairView(TokenObtainPairView):
    pass


@extend_schema_view(post=extend_schema(summary="Renovar token de acesso", tags=_TAG))
class CustomTokenRefreshView(TokenRefreshView):
    pass
