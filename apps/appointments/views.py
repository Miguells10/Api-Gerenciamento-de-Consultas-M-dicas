"""
ViewSet for Appointment — provides list, create, retrieve, update, destroy.
Supports filtering by professional via ?professional=<uuid>.
select_related("professional") prevents N+1 queries on list/retrieve.
"""

from rest_framework.viewsets import ModelViewSet

from .models import Appointment
from .serializers import AppointmentSerializer


class AppointmentViewSet(ModelViewSet):
    queryset = Appointment.objects.select_related("professional").all()
    serializer_class = AppointmentSerializer
    filterset_fields = ["professional", "status"]
