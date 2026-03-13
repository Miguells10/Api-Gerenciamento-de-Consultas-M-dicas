"""
Serializer for the Appointment model.
Validates: date must be in the future on creation.
Uses select_related to avoid N+1 on professional reads.
"""

from django.utils import timezone
from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework import serializers

from apps.professionals.serializers import ProfessionalSerializer

from .models import Appointment


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Exemplo válido",
            summary="Agendar consulta",
            description="Exemplo completo para o POST (data deve ser no futuro).",
            value={
                "professional": "123e4567-e89b-12d3-a456-426614174000",
                "date": (
                    timezone.now() + timezone.timedelta(days=7)
                ).replace(microsecond=0).isoformat(),
            },
            request_only=True,
        ),
        OpenApiExample(
            "Atualização de Status",
            summary="Mudar status (PATCH)",
            description="Exemplo para atualizar o status da consulta.",
            value={
                "status": "COMPLETED",
            },
            request_only=True,
        ),
    ]
)
class AppointmentSerializer(serializers.ModelSerializer):
    professional_detail = ProfessionalSerializer(source="professional", read_only=True)

    class Meta:
        model = Appointment
        fields = [
            "id",
            "professional",
            "professional_detail",
            "date",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "professional_detail", "created_at", "updated_at"]

    def validate_date(self, value: timezone.datetime) -> timezone.datetime:
        if self.instance is None and value <= timezone.now():
            raise serializers.ValidationError(
                "A data da consulta deve ser uma data futura."
            )
        return value
