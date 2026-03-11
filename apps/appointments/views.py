"""
ViewSet for Appointment — provides list, create, retrieve, update, destroy.
Supports filtering by professional via ?professional=<uuid>.
select_related("professional") prevents N+1 queries on list/retrieve.
"""

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.viewsets import ModelViewSet

from .models import Appointment
from .serializers import AppointmentSerializer

_TAG = ["Consultas"]


@extend_schema_view(
    list=extend_schema(summary="Listar consultas (suporta ?professional=<uuid>)", tags=_TAG),
    create=extend_schema(summary="Agendar consulta", tags=_TAG),
    retrieve=extend_schema(summary="Detalhar consulta", tags=_TAG),
    update=extend_schema(summary="Atualizar consulta (completo)", tags=_TAG),
    partial_update=extend_schema(summary="Atualizar consulta (parcial)", tags=_TAG),
    destroy=extend_schema(summary="Cancelar consulta", tags=_TAG),
)
class AppointmentViewSet(ModelViewSet):
    queryset = Appointment.objects.select_related("professional").all()
    serializer_class = AppointmentSerializer
    filterset_fields = ["professional", "status"]
