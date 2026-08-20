# SECURITY.md — Security & Compliance Guidelines

## 1. Data Protection & Privacy

- **Client Data Isolation:** Client historical data is stored isolated per client ID in GCS buckets and Firestore collections.
- **PII Protection:** Personal Identifiable Information (customer names, phone numbers) parsed during document ingestion is encrypted at rest and in transit.
- **Secret Management:** Secrets, API credentials, and database passwords must be stored in Google Secret Manager or passed via environment variables. NEVER hardcode API keys in source code.

## 2. Input Validation & File Handling

- Uploaded files are restricted to supported extensions: `.pdf`, `.png`, `.jpg`, `.jpeg`, `.xlsx`, `.csv`.
- Files undergo mime-type verification prior to ingestion into the Document Understanding pipeline.
- Input parameters in API routes are strictly validated through Pydantic schemas.

## 3. Human Approval & Audit Trails

- High-impact database mutations require explicit human approval (`/api/jobs/{job_id}/approve`).
- Every transformation, column mapping decision, and human response is permanently recorded in Firestore audit logs.
