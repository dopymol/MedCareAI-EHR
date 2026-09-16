from django import forms
from .models import Encounter, Patient, Prescription


class DateInput(forms.DateInput):
    input_type = "date"


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ["full_name", "date_of_birth", "gender", "phone", "email", "blood_group",
                  "allergies", "existing_conditions", "emergency_contact"]
        widgets = {"date_of_birth": DateInput(), "allergies": forms.Textarea(attrs={"rows": 2}),
                   "existing_conditions": forms.Textarea(attrs={"rows": 2})}


class EncounterForm(forms.ModelForm):
    class Meta:
        model = Encounter
        fields = ["chief_complaint", "symptoms", "symptom_duration", "temperature", "blood_pressure",
                  "diagnosis", "clinical_notes", "treatment_plan", "follow_up_date", "doctor_approved"]
        widgets = {"follow_up_date": DateInput(), "symptoms": forms.Textarea(attrs={"rows": 3}),
                   "clinical_notes": forms.Textarea(attrs={"rows": 3}),
                   "treatment_plan": forms.Textarea(attrs={"rows": 3})}
        labels = {"doctor_approved": "Doctor has reviewed and approved this record"}


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ["medicine", "dosage", "frequency", "duration", "instructions"]
