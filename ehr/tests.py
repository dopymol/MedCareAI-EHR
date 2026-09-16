from datetime import date
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import Encounter, Patient, Prescription
from .services.clinical_summary import allergy_warnings, generate_soap_summary


class EHRTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("doctor", password="testpass123")
        self.patient = Patient.objects.create(full_name="Test Patient", date_of_birth=date(1990, 1, 1), gender="F", phone="9999999999", allergies="Penicillin")

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)

    def test_logged_in_patient_list(self):
        self.client.login(username="doctor", password="testpass123")
        response = self.client.get(reverse("patient_list"))
        self.assertContains(response, "Test Patient")

    def test_summary_and_allergy_warning(self):
        encounter = Encounter(patient=self.patient, doctor=self.user, chief_complaint="Rash", symptoms="Itching", diagnosis="Allergic rash")
        summary = generate_soap_summary(encounter)
        self.assertIn("SUBJECTIVE", summary)
        encounter.save()
        rx = Prescription.objects.create(encounter=encounter, medicine="Penicillin", dosage="1", frequency="daily", duration="1 day")
        self.assertTrue(allergy_warnings(self.patient, [rx]))
