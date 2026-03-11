"""
ViewSet for Professional — provides list, create, retrieve, update, destroy.
All responses are JSON (enforced by DRF settings).
"""

from rest_framework.viewsets import ModelViewSet

from .models import Professional
from .serializers import ProfessionalSerializer


class ProfessionalViewSet(ModelViewSet):
    queryset = Professional.objects.all()
    serializer_class = ProfessionalSerializer
