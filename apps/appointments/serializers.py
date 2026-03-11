"""
Serializer for the Appointment model.
Validates: date must be in the future on creation.
Uses select_related to avoid N+1 on professional reads.
"""

from django.utils import timezone
from rest_framework import serializers

from apps.professionals.serializers import ProfessionalSerializer

from .models import Appointment


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
            raise serializers.ValidationError("A data da consulta deve ser uma data futura.")
        return value
