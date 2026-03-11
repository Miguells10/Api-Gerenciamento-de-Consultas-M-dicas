"""
Tests for the Professional CRUD endpoints.
Covers: 200 list, 201 create, 400 bad input, 404 not found, 401 unauthenticated.
Pattern: AAA (Arrange / Act / Assert) on every test.
"""

import uuid

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Professional

User = get_user_model()

BASE_URL = "/api/v1/professionals/"


def _build_professional_payload(**overrides: object) -> dict:
    payload = {
        "social_name": "Dra. Ana Lima",
        "profession": "Cardiologista",
        "address": "Rua das Flores, 123, São Paulo - SP",
        "contact": "+5511999999999",
    }
    payload.update(overrides)
    return payload


class ProfessionalCRUDTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")

    # ── Create ──────────────────────────────────────────────────────────────
    def test_create_professional_returns_201(self) -> None:
        response = self.client.post(BASE_URL, _build_professional_payload(), format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)

    def test_create_with_missing_field_returns_400(self) -> None:
        response = self.client.post(BASE_URL, {"social_name": "Ana"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_with_short_social_name_returns_400(self) -> None:
        payload = _build_professional_payload(social_name="A")
        response = self.client.post(BASE_URL, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # ── List ────────────────────────────────────────────────────────────────
    def test_list_professionals_returns_200(self) -> None:
        Professional.objects.create(**_build_professional_payload())
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    # ── Retrieve ────────────────────────────────────────────────────────────
    def test_retrieve_existing_professional_returns_200(self) -> None:
        professional = Professional.objects.create(**_build_professional_payload())
        response = self.client.get(f"{BASE_URL}{professional.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(response.data["id"]), str(professional.id))

    def test_retrieve_nonexistent_professional_returns_404(self) -> None:
        response = self.client.get(f"{BASE_URL}{uuid.uuid4()}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # ── Update ──────────────────────────────────────────────────────────────
    def test_partial_update_professional_returns_200(self) -> None:
        professional = Professional.objects.create(**_build_professional_payload())
        response = self.client.patch(
            f"{BASE_URL}{professional.id}/",
            {"social_name": "Dra. Ana Souza"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["social_name"], "Dra. Ana Souza")

    # ── Delete ──────────────────────────────────────────────────────────────
    def test_delete_professional_returns_204(self) -> None:
        professional = Professional.objects.create(**_build_professional_payload())
        response = self.client.delete(f"{BASE_URL}{professional.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # ── Auth ────────────────────────────────────────────────────────────────
    def test_unauthenticated_request_returns_401(self) -> None:
        self.client.credentials()
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
