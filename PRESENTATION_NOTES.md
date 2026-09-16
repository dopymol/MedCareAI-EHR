# Five-minute presentation notes

## Opening (30 seconds)

“I built MedCare AI, a mini electronic health record and clinical documentation assistant.
 I chose this problem because digital-health platforms need a secure way to connect patient history
  with online consultations while reducing repetitive documentation for doctors.”

## Problem and solution (45 seconds)

“Medical information may be fragmented across consultations and uploaded reports.
This prototype creates a longitudinal patient record. Authenticated doctors can retrieve
a patient, record a visit, prescribe medicines, and receive a structured SOAP summary.
The application also checks prescriptions against recorded allergies.”

## Live demonstration (2 minutes)

1. Log in using the fictional doctor account.
2. Explain the four dashboard metrics.
3. Search for “Meera” and open her patient record.
4. Point out the allergy banner and consultation timeline.
5. Add a new consultation and show the generated SOAP note.
6. Add a prescription and demonstrate the allergy warning.

## Technical explanation (45 seconds)

“I used Django because its authentication, ORM, validation, CSRF protection, and administration
 interface are appropriate for a rapid but structured healthcare prototype. Patient, Encounter,
 and Prescription are related database models. The summarizer is isolated in a service layer so
 it can later be replaced by an approved language model without rewriting the clinical workflow.”

## Safety and privacy (30 seconds)

“The assistant never diagnoses or prescribes. Its output is visibly labelled as a draft, and the
record includes doctor approval. The demonstration uses fictional data. A production version needs
role-based access, encryption, audit logs, consent, secure deployment, and a formal compliance review.”

## Future development (30 seconds)

“Next I would add PostgreSQL, REST APIs, document upload, teleconsultation integration, ABDM/ABHA support,
and FHIR-compatible exchange. For generative AI I would add de-identification, evidence grounding,
 clinical evaluation, and mandatory human approval.”

## Likely questions

**Why is this called AI if it is rule-based?**  
The MVP proves the end-to-end product workflow without sending sensitive data to an external service.
The summary generator has a defined interface that can safely be upgraded to a validated LLM.

**How would you prevent one doctor viewing every patient?**  
Add organisation and care-team relationships, Django Groups/Permissions, and queryset-level
access control. Log every view and modification.

**How do you avoid AI hallucinations?**  
Generate only from structured encounter fields, forbid unsupported additions, show source fields,
 measure factual consistency, and require clinician approval.

**Why Django rather than Flask?**  
Django provides secure authentication, ORM migrations, forms, validation, CSRF protection,
and admin functionality in a consistent full-stack framework.

**Is the allergy checker clinically complete?**  
No. It is a demonstrative exact-text warning. A clinical product would use normalized drug/allergen
terminology and a validated drug-safety knowledge base.
