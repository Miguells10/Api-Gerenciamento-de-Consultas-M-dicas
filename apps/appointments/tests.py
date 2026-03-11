"""
Tests for the Appointment CRUD endpoints.
Covers: list, create, retrieve, update, delete + 400 (past date), 404, 401, filter by professional.
Pattern: AAA (Arrange / Act / Assert) on every test.
"""

import uuid
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from apps.professionals.models import Professional

from .models import Appointment, AppointmentStatus

User = get_user_model()

BASE_URL = "/api/v1/appointments/"


def _create_professional() -> Professional:
    return Professional.objects.create(
        social_name="Dr. Carlos Melo",
        profession="Ortopedista",
        address="Av. Brasil, 456, Rio de Janeiro - RJ",
        contact="+5521988888888",
    )


def _future_date() -> str:
    return (timezone.now() + timedelta(days=7)).isoformat()


class AppointmentCRUDTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="testuser2", password="testpass123")
        token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")
        self.professional = _create_professional()

    # ── Create ──────────────────────────────────────────────────────────────
    def test_create_appointment_returns_201(self) -> None:
        payload = {"professional": str(self.professional.id), "date": _future_date()}
        response = self.client.post(BASE_URL, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)

    def test_create_with_past_date_returns_400(self) -> None:
        past_date = (timezone.now() - timedelta(days=1)).isoformat()
        payload = {"professional": str(self.professional.id), "date": past_date}
        response = self.client.post(BASE_URL, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_with_missing_professional_returns_400(self) -> None:
        response = self.client.post(BASE_URL, {"date": _future_date()}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # ── List ────────────────────────────────────────────────────────────────
    def test_list_appointments_returns_200(self) -> None:
        Appointment.objects.create(professional=self.professional, date=timezone.now() + timedelta(days=1))
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # ── Retrieve ────────────────────────────────────────────────────────────
    def test_retrieve_existing_appointment_returns_200(self) -> None:
        appointment = Appointment.objects.create(
            professional=self.professional, date=timezone.now() + timedelta(days=1)
        )
        response = self.client.get(f"{BASE_URL}{appointment.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_nonexistent_appointment_returns_404(self) -> None:
        response = self.client.get(f"{BASE_URL}{uuid.uuid4()}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # ── Update ──────────────────────────────────────────────────────────────
    def test_partial_update_status_returns_200(self) -> None:
        appointment = Appointment.objects.create(
            professional=self.professional, date=timezone.now() + timedelta(days=1)
        )
        response = self.client.patch(
            f"{BASE_URL}{appointment.id}/",
            {"status": AppointmentStatus.COMPLETED},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], AppointmentStatus.COMPLETED)

    # ── Delete ──────────────────────────────────────────────────────────────
    def test_delete_appointment_returns_204(self) -> None:
        appointment = Appointment.objects.create(
            professional=self.professional, date=timezone.now() + timedelta(days=1)
        )
        response = self.client.delete(f"{BASE_URL}{appointment.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # ── Auth ────────────────────────────────────────────────────────────────
    def test_unauthenticated_request_returns_401(self) -> None:
        self.client.credentials()
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AppointmentFilterTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="filteruser", password="testpass123")
        token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")
        self.professional_a = _create_professional()
        self.professional_b = Professional.objects.create(
            social_name="Dra. Maria Silva",
            profession="Pediatra",
            address="Rua Augusta, 789, São Paulo - SP",
            contact="+5511977777777",
        )

    def test_filter_by_professional_returns_only_matching(self) -> None:
        Appointment.objects.create(professional=self.professional_a, date=timezone.now() + timedelta(days=1))
        Appointment.objects.create(professional=self.professional_b, date=timezone.now() + timedelta(days=2))

        response = self.client.get(BASE_URL, {"professional": str(self.professional_a.id)})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["professional"], str(self.professional_a.id))
