from datetime import date
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import EncounterForm, PatientForm, PrescriptionForm
from .models import Encounter, Patient
from .services.clinical_summary import allergy_warnings, generate_soap_summary


@login_required
def dashboard(request):
    today = timezone.localdate()
    context = {
        "patient_count": Patient.objects.count(),
        "today_count": Encounter.objects.filter(visit_date__date=today).count(),
        "follow_up_count": Encounter.objects.filter(follow_up_date__gte=today).count(),
        "allergy_count": Patient.objects.exclude(allergies="").count(),
        "recent_encounters": Encounter.objects.select_related("patient", "doctor")[:6],
    }
    return render(request, "ehr/dashboard.html", context)


@login_required
def patient_list(request):
    query = request.GET.get("q", "").strip()
    patients = Patient.objects.all()
    if query:
        patients = patients.filter(Q(full_name__icontains=query) | Q(patient_id__icontains=query) | Q(phone__icontains=query))
    return render(request, "ehr/patient_list.html", {"patients": patients, "query": query})


@login_required
def patient_create(request):
    form = PatientForm(request.POST or None)
    if form.is_valid():
        patient = form.save()
        messages.success(request, f"Patient {patient.full_name} was added successfully.")
        return redirect(patient)
    return render(request, "ehr/form.html", {"form": form, "title": "Register patient", "submit_label": "Save patient"})


@login_required
def patient_update(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    form = PatientForm(request.POST or None, instance=patient)
    if form.is_valid():
        form.save()
        messages.success(request, "Patient information was updated.")
        return redirect(patient)
    return render(request, "ehr/form.html", {"form": form, "title": "Edit patient", "submit_label": "Update patient"})


@login_required
def patient_detail(request, pk):
    patient = get_object_or_404(Patient.objects.prefetch_related("encounters__prescriptions"), pk=pk)
    encounters = patient.encounters.all()
    warning_map = {enc.pk: allergy_warnings(patient, enc.prescriptions.all()) for enc in encounters}
    return render(request, "ehr/patient_detail.html", {"patient": patient, "encounters": encounters, "warning_map": warning_map})


@login_required
def encounter_create(request, patient_pk):
    patient = get_object_or_404(Patient, pk=patient_pk)
    form = EncounterForm(request.POST or None)
    if form.is_valid():
        encounter = form.save(commit=False)
        encounter.patient = patient
        encounter.doctor = request.user
        encounter.ai_summary = generate_soap_summary(encounter)
        encounter.save()
        messages.success(request, "Consultation saved and SOAP summary generated.")
        return redirect("prescription_add", encounter_pk=encounter.pk)
    return render(request, "ehr/form.html", {"form": form, "title": f"New consultation — {patient.full_name}", "submit_label": "Save & add prescription"})


@login_required
def prescription_add(request, encounter_pk):
    encounter = get_object_or_404(Encounter, pk=encounter_pk)
    form = PrescriptionForm(request.POST or None)
    if form.is_valid():
        prescription = form.save(commit=False)
        prescription.encounter = encounter
        prescription.save()
        warnings = allergy_warnings(encounter.patient, [prescription])
        if warnings:
            messages.warning(request, warnings[0])
        else:
            messages.success(request, "Prescription added.")
        if "add_another" in request.POST:
            return redirect("prescription_add", encounter_pk=encounter.pk)
        return redirect(encounter.patient)
    return render(request, "ehr/prescription_form.html", {"form": form, "encounter": encounter})
