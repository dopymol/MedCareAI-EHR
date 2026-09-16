from datetime import date, timedelta
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from ehr.models import Encounter, Patient, Prescription
from ehr.services.clinical_summary import generate_soap_summary


class Command(BaseCommand):
    help = "Create safe fictional demo records and a demo doctor account"

    def handle(self, *args, **options):
        User = get_user_model()
        doctor, _ = User.objects.get_or_create(username="doctor", defaults={"first_name": "Ananya", "last_name": "Rao", "is_staff": True})
        doctor.set_password("Demo@123")
        doctor.save()
        patient, _ = Patient.objects.get_or_create(patient_id="MCR-DEMO001", defaults={
            "full_name": "Meera Krishnan", "date_of_birth": date(1991, 6, 14), "gender": "F",
            "phone": "9876543210", "email": "meera@example.com", "blood_group": "B+",
            "allergies": "Penicillin", "existing_conditions": "Mild asthma",
            "emergency_contact": "Arun Krishnan — 9876500000",
        })
        if not patient.encounters.exists():
            encounter = Encounter(patient=patient, doctor=doctor, chief_complaint="Fever and dry cough",
                symptoms="Low-grade fever, dry cough and tiredness", symptom_duration="three days",
                temperature=100.6, blood_pressure="118/76", diagnosis="Viral upper respiratory infection",
                clinical_notes="No breathing difficulty. Hydration is adequate.",
                treatment_plan="Supportive care, hydration and rest", follow_up_date=date.today() + timedelta(days=5),
                doctor_approved=True)
            encounter.ai_summary = generate_soap_summary(encounter)
            encounter.save()
            Prescription.objects.create(encounter=encounter, medicine="Paracetamol", dosage="500 mg",
                frequency="Twice daily after food", duration="3 days", instructions="Use only if fever persists")
        self.stdout.write(self.style.SUCCESS("Demo ready — username: doctor | password: Demo@123"))
