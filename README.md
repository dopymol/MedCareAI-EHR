# MedCare AI — Mini EHR & Clinical Documentation Assistant

An interview-ready Django electronic health record prototype designed for a digital-health workflow.
Doctors can securely register patients, maintain longitudinal consultation history,
prescribe medicines, generate structured SOAP summaries, and see allergy-conflict warnings.

> All included names and records are fictional. This prototype is not a medical device and must not be used for real clinical decisions.

## Features

- Django authentication and protected clinical pages
- Dashboard with patient, consultation, follow-up, and allergy metrics
- Patient registration, editing, search, and longitudinal record
- Consultation notes, vital signs, diagnosis, treatment, and follow-up
- Multiple prescriptions per consultation
- Rule-based, AI-ready SOAP note generator (works without an API key)
- Exact-match allergy warning when a medicine matches a recorded allergy
- Clinician approval status and safety disclaimer
- Responsive Bootstrap interface
- Django Admin and automated tests
- Fictional demonstration dataset

## Quick start on Windows

```powershell
cd MedCareAI
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

Demo login:

- Username: `doctor`
- Password: `Demo@123`

## Quick start on macOS/Linux

```bash
cd MedCareAI
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

## Tests

```bash
python manage.py check
python manage.py test
```

## Demo flow

1. Sign in as the demo doctor.
2. Review dashboard metrics.
3. Open **Patients** and search for Meera.
4. Open her longitudinal record and existing SOAP summary.
5. Register a new fictional patient.
6. Add a consultation and generate the summary.
7. Add a prescription. Enter `Penicillin` for Meera to demonstrate the allergy warning.

## Responsible AI design

The current summary module uses deterministic Python logic, so the demo requires no external API or patient-data transfer. It is intentionally described as **AI-ready**. In production, an approved language model could replace the module behind the same service interface. Generated text would remain a draft until clinician approval.

The system does not predict diagnoses or prescribe medicines. Production requirements would include explicit consent, encryption, audit trails, role-based permissions, retention policies, validated clinical terminology, and applicable Indian privacy and healthcare compliance review.

## Production roadmap

- PostgreSQL and environment-based secrets
- Django REST Framework with a React/mobile client
- Granular doctor, nurse, receptionist, and patient permissions
- Immutable audit logs and access history
- Encrypted report upload and teleconsultation integration
- ABDM/ABHA and HL7 FHIR-compatible data exchange
- Medical terminology coding (SNOMED CT/ICD where licensed and appropriate)
- Validated LLM summarization with redaction, citations, evaluation, and human approval

## Technology

Python · Django · SQLite · Django ORM · Bootstrap 5 · HTML/CSS
