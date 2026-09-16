def generate_soap_summary(encounter):
    patient = encounter.patient
    objective_parts = []
    if encounter.temperature:
        objective_parts.append(f"temperature {encounter.temperature}°F")
    if encounter.blood_pressure:
        objective_parts.append(f"blood pressure {encounter.blood_pressure} mmHg")
    objective = ", ".join(objective_parts) if objective_parts else "No vital signs were recorded"
    follow_up = encounter.follow_up_date.strftime("%d %b %Y") if encounter.follow_up_date else "as clinically required"
    return (
        f"SUBJECTIVE: {patient.full_name} presented with {encounter.chief_complaint}. "
        f"Reported symptoms: {encounter.symptoms}"
        f"{' for ' + encounter.symptom_duration if encounter.symptom_duration else ''}.\n\n"
        f"OBJECTIVE: {objective.capitalize()}.\n\n"
        f"ASSESSMENT: Clinician-recorded diagnosis: {encounter.diagnosis}.\n\n"
        f"PLAN: {encounter.treatment_plan or 'Treatment plan to be confirmed by the clinician.'} "
        f"Follow-up {follow_up}."
    )


def allergy_warnings(patient, prescriptions):
    allergy_terms = [item.strip().lower() for item in patient.allergies.split(",") if item.strip()]
    warnings = []
    for prescription in prescriptions:
        medicine = prescription.medicine.lower()
        for allergy in allergy_terms:
            if allergy in medicine or medicine in allergy:
                warnings.append(f"Possible allergy conflict: {prescription.medicine} matches recorded allergy '{allergy}'.")
    return warnings
