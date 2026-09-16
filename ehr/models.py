import uuid
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse


class Patient(models.Model):
    class Gender(models.TextChoices):
        FEMALE = "F", "Female"
        MALE = "M", "Male"
        OTHER = "O", "Other"

    patient_id = models.CharField(max_length=12, unique=True, blank=True)
    full_name = models.CharField(max_length=120)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=Gender.choices)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    blood_group = models.CharField(max_length=5, blank=True)
    allergies = models.TextField(blank=True, help_text="Comma-separated, e.g. Penicillin, peanuts")
    existing_conditions = models.TextField(blank=True)
    emergency_contact = models.CharField(max_length=120, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.patient_id:
            self.patient_id = f"MCR-{uuid.uuid4().hex[:7].upper()}"
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("patient_detail", args=[self.pk])

    def __str__(self):
        return f"{self.patient_id} — {self.full_name}"


class Encounter(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="encounters")
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="encounters")
    visit_date = models.DateTimeField(auto_now_add=True)
    chief_complaint = models.CharField(max_length=250)
    symptoms = models.TextField()
    symptom_duration = models.CharField(max_length=80, blank=True)
    temperature = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True,
        validators=[MinValueValidator(85), MaxValueValidator(115)])
    blood_pressure = models.CharField(max_length=12, blank=True, help_text="Example: 120/80")
    diagnosis = models.CharField(max_length=250)
    clinical_notes = models.TextField(blank=True)
    treatment_plan = models.TextField(blank=True)
    follow_up_date = models.DateField(blank=True, null=True)
    ai_summary = models.TextField(blank=True)
    doctor_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["-visit_date"]

    def __str__(self):
        return f"{self.patient.full_name} — {self.visit_date:%d %b %Y}"


class Prescription(models.Model):
    encounter = models.ForeignKey(Encounter, on_delete=models.CASCADE, related_name="prescriptions")
    medicine = models.CharField(max_length=120)
    dosage = models.CharField(max_length=80)
    frequency = models.CharField(max_length=80)
    duration = models.CharField(max_length=80)
    instructions = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return f"{self.medicine} — {self.dosage}"
