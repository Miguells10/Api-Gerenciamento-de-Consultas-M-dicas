from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework import serializers

from .models import Professional


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Exemplo válido",
            summary="Dados para criar um profissional",
            description="Exemplo completo para o POST e PUT",
            value={
                "social_name": "Dra. Ana Silva",
                "profession": "Cardiologista",
                "address": "Av. Paulista, 1000 - São Paulo, SP",
                "contact": "+5511999998888",
            },
            request_only=True,
        )
    ]
)
class ProfessionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professional
        fields = [
            "id", "social_name", "profession", "address",
            "contact", "created_at", "updated_at"
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_social_name(self, value: str) -> str:
        if len(value.strip()) < 2:
            raise serializers.ValidationError(
                "O nome social deve ter ao menos 2 caracteres."
            )
        return value.strip()

    def validate_contact(self, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise serializers.ValidationError("O contato não pode ser vazio.")
        return cleaned
