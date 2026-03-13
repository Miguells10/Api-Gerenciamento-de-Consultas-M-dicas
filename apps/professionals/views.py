from django.db.models import ProtectedError
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Professional
from .serializers import ProfessionalSerializer

_TAG = ["Profissionais"]


@extend_schema_view(
    list=extend_schema(summary="Listar profissionais", tags=_TAG),
    create=extend_schema(summary="Cadastrar profissional", tags=_TAG),
    retrieve=extend_schema(summary="Detalhar profissional", tags=_TAG),
    update=extend_schema(summary="Atualizar profissional (completo)", tags=_TAG),
    partial_update=extend_schema(summary="Atualizar profissional (parcial)", tags=_TAG),
    destroy=extend_schema(summary="Remover profissional", tags=_TAG),
)
class ProfessionalViewSet(ModelViewSet):
    queryset = Professional.objects.all()
    serializer_class = ProfessionalSerializer

    def destroy(self, request, *args, **kwargs):
        """
        Custom destroy to handle ProtectedError when a professional has appointments.
        """
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response(
                {
                    "detail": (
                        "Não é possível remover este profissional pois "
                        "ele possui consultas agendadas."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
