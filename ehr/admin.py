from django.contrib import admin
from .models import Encounter, Patient, Prescription


class PrescriptionInline(admin.TabularInline):
    model = Prescription
    extra = 1


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("patient_id", "full_name", "phone", "blood_group", "created_at")
    search_fields = ("patient_id", "full_name", "phone")


@admin.register(Encounter)
class EncounterAdmin(admin.ModelAdmin):
    list_display = ("patient", "doctor", "visit_date", "diagnosis", "doctor_approved")
    list_filter = ("doctor_approved", "visit_date")
    inlines = [PrescriptionInline]


admin.site.register(Prescription)
