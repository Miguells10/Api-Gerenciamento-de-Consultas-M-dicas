from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

from apps.professionals.models import Professional
from .models import Appointment, AppointmentStatus


class AppointmentAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.force_authenticate(user=self.user)
        self.professional = Professional.objects.create(
            social_name="Dr. Strange",
            profession="Sorcerer Supreme",
            address="177A Bleecker Street",
            contact="+1-212-970-4133",
        )
        self.list_url = reverse("appointment-list")
        self.future_date = (timezone.now() + timezone.timedelta(days=7)).replace(microsecond=0)
        self.valid_payload = {
            "professional": str(self.professional.id),
            "date": self.future_date.isoformat(),
        }

    def test_create_appointment_success(self):
        """Test creating an appointment with valid data."""
        response = self.client.post(self.list_url, self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Appointment.objects.count(), 1)
        self.assertEqual(Appointment.objects.get().professional, self.professional)

    def test_create_appointment_past_date(self):
        """Test creating an appointment with a date in the past."""
        past_date = (timezone.now() - timezone.timedelta(days=1)).isoformat()
        payload = self.valid_payload.copy()
        payload["date"] = past_date
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("date", response.data)
        self.assertEqual(Appointment.objects.count(), 0)

    def test_create_appointment_missing_professional(self):
        """Test creating an appointment without a professional."""
        payload = {"date": self.future_date.isoformat()}
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("professional", response.data)
        self.assertEqual(Appointment.objects.count(), 0)

    def test_list_appointments(self):
        """Test listing appointments."""
        Appointment.objects.create(
            professional=self.professional,
            date=self.future_date
        )
        response = self.client.get(self.list_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"] if "results" in response.data else response.data), 1)

    def test_retrieve_appointment(self):
        """Test retrieving a single appointment."""
        appointment = Appointment.objects.create(
            professional=self.professional,
            date=self.future_date
        )
        url = reverse("appointment-detail", args=[appointment.id])
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(response.data["professional"]), str(self.professional.id))

    def test_update_appointment_status(self):
        """Test updating an appointment's status."""
        appointment = Appointment.objects.create(
            professional=self.professional,
            date=self.future_date
        )
        url = reverse("appointment-detail", args=[appointment.id])
        payload = {"status": AppointmentStatus.COMPLETED}
        response = self.client.patch(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        appointment.refresh_from_db()
        self.assertEqual(appointment.status, AppointmentStatus.COMPLETED)

    def test_delete_appointment(self):
        """Test canceling/deleting an appointment."""
        appointment = Appointment.objects.create(
            professional=self.professional,
            date=self.future_date
        )
        url = reverse("appointment-detail", args=[appointment.id])
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Appointment.objects.count(), 0)

    def test_professional_protection(self):
        """Test that a professional cannot be deleted if they have appointments."""
        Appointment.objects.create(
            professional=self.professional,
            date=self.future_date
        )
        from django.db.models import ProtectedError
        with self.assertRaises(ProtectedError):
            self.professional.delete()
