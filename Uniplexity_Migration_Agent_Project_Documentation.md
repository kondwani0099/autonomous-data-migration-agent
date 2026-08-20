# Uniplexity Migration Agent
## All Things Agentic Hackathon — Project Documentation

---

## 1. Executive Summary

**Project Name:** Uniplexity Migration Agent  
**Track:** The Taskmaster  
**Prize Targets:** The Taskmaster ($20,000), Best Architectural Design ($5,000), Best Multimodal UX ($5,000)  
**Deadline:** September 1, 2026

**One-Liner:** An autonomous AI employee that ingests years of messy historical business records — handwritten ledgers, Excel files, scanned PDFs — and migrates them into Uniplexity ERP with minimal human intervention.

**The Problem:** As Uniplexity onboards new clients, they bring 2–3 years of sales, inventory, purchase, and patient records stored in physical books, Excel files, PDFs, and other formats. Every business records information differently: different columns, abbreviations, product names, date formats, and templates. Simple OCR extracts text but doesn't understand meaning. Manual data entry is impossible at scale.

**The Solution:** An agentic system that takes responsibility for the entire data migration workflow — understanding each client's unique format, extracting structured data via multimodal AI, mapping to Uniplexity's schema, cleaning and normalizing, detecting anomalies, asking clarifying questions only when necessary, and processing thousands of records asynchronously in the background.

---

## 2. Why This Wins

### Hackathon Judging Criteria Mapping

| Criteria (Weight) | How We Deliver |
|-------------------|----------------|
| **Innovation & Operational Utility (40%)** | Removes *real, massive* friction. Not a chatbot — an agent that works overnight, processes thousands of records, and makes decisions autonomously. |
| **Architectural Discipline & Tech Stack (30%)** | Agent swarm architecture with clear separation of concerns. State management, memory, audit trails, human-in-the-loop gates, failure handling. |
| **Demo & Production Readiness (30%)** | Live demo: upload scanned ledger → watch agent extract, map, clean, preview, and import. Cloud Run dashboard visible. Clean architecture diagram. |

### Differentiators
- **Real business problem** — happening now at Uniplexity, not hypothetical
- **Multimodal by necessity** — vision OCR for handwritten books, structured parsing for Excel, text extraction for PDFs
- **Learning agent** — remembers each client's format and abbreviations across migrations
- **Minimally invasive** — asks 5 questions, not 500 manual mappings
- **Enterprise-grade** — full audit trail, validation gates, dry-run previews

---

## 3. System Architecture

### High-Level Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              CLIENT BROWSER                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │ Upload      │  │ Migration   │  │ Clarification│  │ Data Preview &      │ │
│  │ Dropzone    │  │ Dashboard   │  │ UI           │  │ Import Approval     │ │
│  │ (PDF, Excel,│  │ (progress,  │  │ (agent asks  │  │ (dry-run, anomalies,│ │
│  │  images)    │  │  status)    │  │  when stuck) │  │  audit trail)       │ │
│  └──────┬──────┘  └─────────────┘  └─────────────┘  └─────────────────────┘ │
└─────────┼────────────────────────────────────────────────────────────────────┘
          │ HTTPS
          ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CLOUD RUN (FastAPI)                                │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │  API Layer: /api/jobs, /api/upload, /api/clarify, /api/preview,         │ │
│  │  /api/import, /api/audit                                                │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                        │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │                     GOOGLE ADK — AGENT SWARM                             │ │
│  │  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────────┐  │ │
│  │  │ DOCUMENT        │───▶│ SCHEMA          │───▶│ DATA                │  │ │
│  │  │ UNDERSTANDING   │    │ MAPPING         │    │ CLEANING            │  │ │
│  │  │ AGENT           │    │ AGENT           │    │ AGENT               │  │ │
│  │  │                 │    │                 │    │                     │  │ │
│  │  │ • Vision OCR    │    │ • Map columns   │    │ • Normalize products│  │ │
│  │  │ • Table detect  │    │ • Infer types   │    │ • Deduplicate       │  │ │
│  │  │ • Classify doc  │    │ • Ask if        │    │ • Fix dates/currency│  │ │
│  │  │   type          │    │   ambiguous     │    │ • Detect anomalies  │  │ │
│  │  │ • Extract raw   │    │ • Learn & store │    │ • Validate rules    │  │ │
│  │  │   text/tables   │    │   mappings      │    │                     │  │ │
│  │  └─────────────────┘    └─────────────────┘    └─────────────────────┘  │ │
│  │           │                      │                      │                │ │
│  │           └──────────────────────┼──────────────────────┘                │ │
│  │                                  ▼                                       │ │
│  │  ┌─────────────────────────────────────────────────────────────────────┐ │ │
│  │  │              VALIDATION & IMPORT AGENT                               │ │ │
│  │  │  • Business rule checks  • Dry-run preview  • Human approval gate   │ │ │
│  │  │  • Commit to DB          • Rollback support  • Generate audit log   │ │ │
│  │  └─────────────────────────────────────────────────────────────────────┘ │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
          │           │           │           │
          ▼           ▼           ▼           ▼
┌─────────────┐ ┌──────────┐ ┌──────────┐ ┌─────────────────┐
│  Cloud      │ │  Cloud   │ │  Cloud   │ │  Cloud SQL /    │
│  Storage    │ │  Pub/Sub │ │  Firestore│ │  Uniplexity DB  │
│  (raw docs) │ │  (queue) │ │  (state) │ │  (import target)│
└─────────────┘ └──────────┘ └──────────┘ └─────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         EXTERNAL SERVICES                                    │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────────────┐  │
│  │  Vertex AI      │  │  Document AI    │  │  Uniplexity ERP API         │  │
│  │  (Gemini 3.5    │  │  (OCR / table   │  │  (final import endpoint)    │  │
│  │   Flash)        │  │   extraction)   │  │                             │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Architecture Principles
1. **Decoupled ingestion** — Upload via API, processing via Pub/Sub queue. Supports thousands of files.
2. **Agent swarm** — Specialized agents for each phase, orchestrated sequentially. Easier to debug, test, and extend.
3. **Stateful** — Every job, document, and agent decision persisted in Firestore. UI shows real-time progress.
4. **Human-in-the-loop** — Agent asks questions via Firestore → React polls → user answers → agent resumes.
5. **Audit everything** — Every mapping decision, every data transformation, every import action is logged.
6. **Learned memory** — Successful schema mappings stored per client. Next migration for same client is faster.

---

## 4. Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | React 18 + Vite + TypeScript + Tailwind CSS | Upload UI, dashboard, preview tables, clarification cards |
| **Backend** | FastAPI + Python 3.11 | API layer, agent orchestration, webhook handlers |
| **Agent Framework** | **Google ADK** | Hackathon requirement. Agent swarm definition, tool calling, session management |
| **AI Model** | Gemini 3.5 Flash (Vertex AI) | Document understanding, schema inference, data cleaning, reasoning |
| **Vision/OCR** | Document AI (or Gemini multimodal) | Extract text and tables from scanned images and PDFs |
| **Database (State)** | Firestore | Job status, document progress, agent memory, clarifications, audit logs |
| **Database (Target)** | Cloud SQL (PostgreSQL) or Uniplexity API | Final imported data. Mock for hackathon if API unavailable. |
| **File Storage** | Cloud Storage | Raw uploaded documents, processed extracts, export files |
| **Message Queue** | Cloud Pub/Sub | Async document processing, decouples upload from agent work |
| **Scheduler** | Cloud Scheduler | Nightly batch jobs, cleanup, retry failed documents |
| **Hosting** | **Cloud Run** | Serverless, scales to zero, single container for frontend + backend |
| **Monitoring** | Cloud Logging + Cloud Monitoring | Agent trace logs, error tracking, performance metrics |

---

## 5. Agent Swarm Design (Google ADK)

### Orchestrator: Sequential Pipeline

```python
from google.adk.agents import Agent, SequentialAgent

migration_pipeline = SequentialAgent(
    name="UniplexityMigrationPipeline",
    description="End-to-end historical data migration for Uniplexity clients",
    sub_agents=[
        document_understanding_agent,
        schema_mapping_agent,
        data_cleaning_agent,
        validation_import_agent
    ]
)
```

### Agent 1: Document Understanding Agent

**Role:** Extract structured data from any input format.

**Inputs:** Raw file (PDF, image, Excel, CSV)
**Outputs:** `ExtractedDocument` — raw text, detected tables, document type, confidence

**Capabilities:**
- Multimodal vision analysis for scanned books and images
- Table structure detection (rows, columns, headers)
- Document classification: SALES_LEDGER, INVENTORY_SHEET, PURCHASE_RECORD, PATIENT_RECORD, INVOICE, UNKNOWN
- Handwriting recognition
- Excel/CSV structured parsing

**Tools:**
- `extract_from_image(pdf_or_image)` → Document AI / Gemini vision
- `extract_from_excel(file)` → pandas + openpyxl
- `classify_document(extracted_text)` → Gemini classification
- `detect_tables(raw_text)` → Table extraction

**Example Prompt:**
```
You are a document analyst specializing in business records. 
Given a scanned sales ledger page:
1. Extract ALL text and tabular data accurately
2. Identify column headers (even if abbreviated or handwritten)
3. Detect the date format used (DD/MM/YY, MM-DD-YYYY, etc.)
4. Classify the document type
5. Note any unusual abbreviations or shorthand

Return structured JSON with: raw_text, tables[], detected_columns[], 
date_format, abbreviations[], confidence_score
```

### Agent 2: Schema Mapping Agent

**Role:** Map extracted data to Uniplexity's ERP schema.

**Inputs:** `ExtractedDocument` + client_id
**Outputs:** `MappedRecords` — fields mapped to Uniplexity schema, confidence per field

**Capabilities:**
- Load previously learned mappings for this client
- Infer column meanings from context ("Qt." near price columns = quantity, not quarts)
- Map to Uniplexity tables: `sales`, `products`, `customers`, `inventory`, `purchases`
- Detect ambiguous mappings and request clarification
- Store successful mappings for future use

**Tools:**
- `load_client_mappings(client_id)` → Firestore
- `save_client_mapping(client_id, mapping)` → Firestore
- `get_uniplexity_schema(table_name)` → Schema reference
- `request_clarification(question, options, document_id)` → Firestore + UI notification

**Clarification Triggers:**
- Confidence < 70% on column mapping
- Unknown abbreviation with multiple possible meanings
- Column doesn't match any known Uniplexity field
- Ambiguous date format (02/03/2024 — Feb 3 or Mar 2?)

**Example Prompt:**
```
You are a database migration specialist. Given extracted sales data:
1. Map each detected column to the correct Uniplexity field
2. Use client's historical mappings if available
3. For ambiguous mappings, call request_clarification()
4. Infer data types and relationships
5. Validate required fields are present

Uniplexity Sales Schema:
- sale_date (DATE, required)
- customer_name (STRING, required)
- product_name (STRING, required)
- quantity (INTEGER, required)
- unit_price (DECIMAL, required)
- total_amount (DECIMAL, calculated)
- payment_method (STRING: cash, credit, transfer)
```

### Agent 3: Data Cleaning Agent

**Role:** Normalize, deduplicate, and validate data.

**Inputs:** `MappedRecords`
**Outputs:** `CleanRecords` + `Anomalies[]` + `DuplicateGroups[]`

**Capabilities:**
- Normalize product names ("Coke", "Coca-Cola", "Coca Cola 330ml" → unified product)
- Standardize dates to ISO format
- Normalize currency and units
- Detect duplicates across the entire migration job
- Flag anomalies (negative quantities, future dates, impossible prices, orphaned records)
- Validate against business rules

**Tools:**
- `normalize_product_name(name)` → Fuzzy matching + Gemini reasoning
- `standardize_date(date_str, format)` → dateutil
- `detect_duplicates(records, fields)` → Record linkage
- `validate_business_rules(record)` → Rule engine
- `flag_anomaly(record, reason)` → Anomaly log

**Example Prompt:**
```
You are a data quality engineer. Given mapped sales records:
1. Normalize product names — group variants of the same product
2. Standardize all dates to ISO 8601
3. Detect exact and fuzzy duplicates
4. Flag anomalies:
   - Negative quantities or prices
   - Dates in the future
   - Prices exceeding 3 standard deviations
   - Missing required fields
5. Validate: total_amount ≈ quantity × unit_price (within rounding)

Return: clean_records[], anomalies[], duplicate_groups[]
```

### Agent 4: Validation & Import Agent

**Role:** Final checks, human approval, and database import.

**Inputs:** `CleanRecords` + `Anomalies[]`
**Outputs:** Import confirmation + audit trail

**Capabilities:**
- Generate dry-run preview (what will be imported, what will change)
- Present anomalies for human review
- Create audit trail entry
- Commit to Uniplexity database (or mock API)
- Support rollback if errors detected post-import

**Tools:**
- `generate_preview(clean_records)` → Summary stats
- `create_audit_trail(job_id, actions)` → Firestore
- `import_to_uniplexity(records)` → API call / SQL insert
- `rollback_import(job_id)` → Reverse changes

---

## 6. Data Flow (Detailed)

### Flow 1: New Migration Job

```
1. Client opens React app → clicks "New Migration"
2. Selects client from dropdown (or creates new)
3. Drops files into upload zone (PDFs, images, Excel files)
4. Frontend uploads directly to Cloud Storage (signed URL)
5. Backend creates Firestore job document:
   jobs/{jobId}: {status: "uploading", client_id, files[], created_at}
6. For each file, publishes Pub/Sub message: {jobId, filePath, clientId}
7. Cloud Run subscriber picks up message
8. Pipeline starts: Document Understanding → Schema Mapping → Cleaning → Validation
9. Firestore job document updated in real-time at each stage
10. React polls /api/jobs/{jobId} and shows live progress
```

### Flow 2: Agent Needs Clarification

```
1. Schema Mapping Agent encounters "Qt." — confidence 45%
2. Agent calls request_clarification(
       question: "What does 'Qt.' mean in this context?",
       options: ["Quantity", "Quarts (volume)", "Something else"],
       document_id: "doc_123"
   )
3. Clarification stored in Firestore: clarifications/{clarificationId}
4. React polls and shows ClarificationCard in UI
5. User selects "Quantity"
6. Backend resumes pipeline from Schema Mapping Agent
7. Agent saves mapping: {client_id, abbreviation: "Qt.", meaning: "Quantity"}
8. Future documents for this client auto-resolve "Qt."
```

### Flow 3: Import Approval

```
1. Cleaning Agent completes. Validation Agent generates preview.
2. Firestore job status → "awaiting_approval"
3. React shows DataPreview component:
   - Summary: 2,847 records, 12 anomalies, 3 duplicates
   - Table preview (first 50 rows)
   - Anomaly list with explanations
   - Audit trail of all agent decisions
4. User reviews and clicks "Approve & Import"
5. Validation Agent commits to Uniplexity DB
6. Job status → "completed"
7. Audit trail permanently stored
```

---

## 7. Database Schema (Firestore)

### Collection: `jobs`
```javascript
{
  job_id: "job_abc123",
  client_id: "client_uniplex_retail_01",
  client_name: "ABC Retail Store",
  status: "processing", // uploading, understanding, mapping, cleaning, awaiting_approval, importing, completed, failed
  created_at: Timestamp,
  updated_at: Timestamp,
  total_documents: 12,
  processed_documents: 8,
  total_records_detected: 2847,
  records_imported: 0,
  anomalies_found: 12,
  clarifications_pending: 1,
  clarifications_resolved: 3,
  estimated_completion: Timestamp,
  error_message: null,
  audit_trail_id: "audit_job_abc123"
}
```

### Collection: `documents`
```javascript
{
  document_id: "doc_xyz789",
  job_id: "job_abc123",
  client_id: "client_uniplex_retail_01",
  file_name: "sales_ledger_jan_2024.pdf",
  file_path: "gs://bucket/jobs/job_abc123/sales_ledger_jan_2024.pdf",
  file_type: "pdf", // pdf, image, excel, csv
  status: "cleaning", // queued, understanding, mapping, cleaning, validated, imported, failed
  document_type: "SALES_LEDGER", // detected by Agent 1
  extracted_data: {
    raw_text: "...",
    tables: [...],
    detected_columns: ["Date", "Cust", "Prod", "Qt.", "Price", "Total"],
    date_format: "DD/MM/YY",
    abbreviations: ["Cust", "Qt."]
  },
  mapped_records: [...],
  clean_records: [...],
  anomalies: [...],
  confidence_score: 0.89,
  started_at: Timestamp,
  completed_at: null,
  error_message: null
}
```

### Collection: `client_mappings`
```javascript
{
  client_id: "client_uniplex_retail_01",
  mappings: {
    "Qt.": { meaning: "Quantity", field: "quantity", confidence: 1.0, learned_from: "doc_xyz789" },
    "Cust": { meaning: "Customer Name", field: "customer_name", confidence: 1.0 },
    "Prod": { meaning: "Product Name", field: "product_name", confidence: 1.0 },
    "Price": { meaning: "Unit Price", field: "unit_price", confidence: 0.95 }
  },
  product_normalizations: {
    "Coca-Cola": ["Coke", "Coca Cola", "Coca-Cola 330ml"],
    "Bread": ["Bred", "Brd", "Sliced Bread"]
  },
  updated_at: Timestamp
}
```

### Collection: `clarifications`
```javascript
{
  clarification_id: "clar_001",
  job_id: "job_abc123",
  document_id: "doc_xyz789",
  agent: "SchemaMappingAgent",
  question: "What does 'Qt.' mean in this context?",
  options: ["Quantity", "Quarts (volume)", "Something else"],
  context: "Column appears near 'Price' and 'Total' in sales ledger",
  status: "pending", // pending, answered, applied
  answer: null,
  answered_by: null,
  answered_at: null,
  created_at: Timestamp
}
```

### Collection: `audit_trails`
```javascript
{
  audit_id: "audit_job_abc123",
  job_id: "job_abc123",
  client_id: "client_uniplex_retail_01",
  actions: [
    {
      timestamp: Timestamp,
      agent: "DocumentUnderstandingAgent",
      action: "extracted_tables",
      document_id: "doc_xyz789",
      details: "Detected 47 rows, 6 columns",
      before: null,
      after: { rows: 47, columns: ["Date", "Cust", "Prod", "Qt.", "Price", "Total"] }
    },
    {
      timestamp: Timestamp,
      agent: "SchemaMappingAgent",
      action: "mapped_column",
      document_id: "doc_xyz789",
      details: "Mapped 'Qt.' to 'quantity'",
      before: { column: "Qt.", meaning: "unknown" },
      after: { column: "Qt.", meaning: "quantity", source: "clarification" }
    },
    {
      timestamp: Timestamp,
      agent: "DataCleaningAgent",
      action: "normalized_product",
      document_id: "doc_xyz789",
      details: "Grouped 'Coke' and 'Coca Cola' into 'Coca-Cola'",
      before: ["Coke", "Coca Cola"],
      after: "Coca-Cola"
    }
  ],
  created_at: Timestamp
}
```

---

## 8. API Design (FastAPI)

### Jobs
```
POST   /api/jobs                          → Create new migration job
GET    /api/jobs                          → List jobs (with filters)
GET    /api/jobs/{job_id}                 → Get job status & progress
DELETE /api/jobs/{job_id}                 → Cancel/delete job
```

### Upload
```
POST   /api/jobs/{job_id}/upload-url      → Get signed URL for direct-to-GCS upload
POST   /api/webhook/upload-complete       → GCS notification webhook (triggers Pub/Sub)
```

### Processing
```
POST   /api/jobs/{job_id}/process         → Manually trigger/retry processing
GET    /api/jobs/{job_id}/documents       → List all documents in job
GET    /api/jobs/{job_id}/documents/{id}  → Get document details & extracted data
```

### Clarifications
```
GET    /api/jobs/{job_id}/clarifications          → List pending clarifications
POST   /api/clarifications/{id}/answer            → Submit answer (resumes pipeline)
```

### Preview & Import
```
GET    /api/jobs/{job_id}/preview         → Get dry-run preview (stats + sample records)
POST   /api/jobs/{job_id}/approve         → Approve and trigger import
POST   /api/jobs/{job_id}/reject          → Reject and provide feedback
GET    /api/jobs/{job_id}/audit           → Get full audit trail
```

### Clients
```
GET    /api/clients                       → List clients
GET    /api/clients/{id}/mappings         → Get learned mappings for client
PUT    /api/clients/{id}/mappings         → Manually edit mappings
```

---

## 9. Frontend Components

### Pages
- **Dashboard** — List of all migration jobs, status cards, quick stats
- **New Migration** — Multi-step wizard: select client → upload files → confirm
- **Migration Detail** — Real-time progress, document list, agent activity log
- **Clarification Center** — All pending questions across jobs
- **Data Preview** — Tabular preview with anomaly highlighting
- **Audit Trail** — Searchable log of every agent decision

### Key Components
```typescript
// UploadDropzone.tsx
// - Drag & drop multiple files
// - Shows upload progress per file
// - Validates file types (PDF, PNG, JPG, XLSX, CSV)

// MigrationProgress.tsx
// - Real-time progress bar via Firestore polling
// - Stage indicators: Upload → Understand → Map → Clean → Validate → Import
// - Animated agent activity log

// ClarificationCard.tsx
// - Shows agent question with context
// - Multiple choice or free-text input
// - "Why is the agent asking this?" explanation

// DataPreviewTable.tsx
// - Paginated table of records to be imported
// - Anomaly highlighting (red rows, warning icons)
// - Filter by: all, clean, anomalies, duplicates

// AgentLog.tsx
// - Timeline of agent actions
// - Expandable cards showing before/after
// - Filter by agent type

// AuditTrailViewer.tsx
// - Searchable, filterable audit log
// - Export to CSV/PDF
// - Diff view for data transformations
```

---

## 10. Demo Script (4 Minutes)

### Scene Setup
- Have 3-5 realistic files ready:
  - Scanned image of handwritten sales ledger (PNG)
  - Excel file with inconsistent columns
  - PDF invoice
- Pre-create one "client" with some learned mappings

### Minute-by-Minute

**0:00–0:30 — The Problem**
> "Uniplexity onboards businesses with 2–3 years of records in handwritten books, Excel files, and PDFs. Every client formats data differently. Manual entry is impossible. Simple OCR doesn't understand meaning."

Show: Physical book / messy Excel screenshot

**0:30–1:15 — Upload & Agent Starts**
> "Watch what happens when ABC Retail uploads their January sales ledger."

Action: Drop 3 files into upload zone
Visual: Files upload → job created → progress bar starts moving

**1:15–2:00 — Document Understanding**
> "The Document Understanding Agent reads the scanned page, detects tables, extracts text, and identifies abbreviations."

Visual: Show extracted table, detected columns ["Date", "Cust", "Prod", "Qt.", "Price"]
Show: Cloud Run logs / Firestore document updating

**2:00–2:45 — Clarification (The Magic Moment)**
> "The agent encounters 'Qt.' — it could mean Quantity or Quarts. Instead of guessing, it asks."

Visual: ClarificationCard pops up: "What does 'Qt.' mean?"
Action: Click "Quantity"
Visual: Pipeline resumes, mapping applied

> "And it remembers. Next month, when ABC Retail uploads February's ledger, 'Qt.' is auto-mapped."

**2:45–3:30 — Cleaning & Preview**
> "The Cleaning Agent normalizes product names, detects duplicates, and flags anomalies."

Visual: DataPreview table
- "Coke" and "Coca Cola" grouped under "Coca-Cola"
- Red highlight: "Future date detected — March 2027"
- Yellow highlight: "Possible duplicate of record #184"

**3:30–3:50 — Approval & Import**
> "After review, approve and import."

Action: Click "Approve & Import"
Visual: Progress bar → "Importing..." → "Complete! 2,847 records imported."

**3:50–4:00 — Proof & Architecture**
> "Every decision is audited. Every transformation is traceable. And it all runs on Google Cloud."

Visual: 
- Audit trail showing the "Qt. → Quantity" mapping decision
- Cloud Run dashboard screenshot
- Architecture diagram

---

## 11. 11-Day Build Plan

### Days 1–2: Foundation
- [ ] Scaffold FastAPI project structure
- [ ] Set up Cloud Run, Firestore, Cloud Storage, Pub/Sub
- [ ] Create Firestore collections and indexes
- [ ] Build React app shell (Vite + Tailwind + routing)
- [ ] Deploy "hello world" to Cloud Run (prove it works)

### Days 3–4: Upload & Ingestion
- [ ] React: UploadDropzone with direct-to-GCS signed URLs
- [ ] Backend: Webhook for upload completion
- [ ] Pub/Sub: Document processing queue
- [ ] Firestore: Job and document creation on upload
- [ ] React: MigrationDashboard with real-time status polling

### Days 5–6: Document Understanding Agent
- [ ] Integrate Document AI / Gemini multimodal for OCR
- [ ] Build table extraction logic
- [ ] Document classification (sales, inventory, etc.)
- [ ] Store extracted data in Firestore
- [ ] React: Document detail view showing extracted tables

### Days 7–8: Schema Mapping & Cleaning Agents
- [ ] Build SchemaMappingAgent with ADK
- [ ] Client mapping memory (load/save from Firestore)
- [ ] Clarification flow: agent asks → UI shows → user answers → pipeline resumes
- [ ] Build DataCleaningAgent
- [ ] Product normalization, deduplication, anomaly detection
- [ ] React: ClarificationCard + DataPreview components

### Day 9: Validation, Import & Audit
- [ ] ValidationAgent: business rules, dry-run preview
- [ ] Import to mock Uniplexity DB (or real API if available)
- [ ] Audit trail generation
- [ ] React: Approval flow + AuditTrail viewer

### Day 10: Polish & Demo Prep
- [ ] End-to-end testing with realistic sample data
- [ ] Fix bugs, improve UI polish
- [ ] Record demo video (follow 4-minute script)
- [ ] Write README with spin-up instructions
- [ ] Create architecture diagram

### Day 11: Submit
- [ ] Final code review and cleanup
- [ ] Push to GitHub
- [ ] Submit to Devpost with all required materials
- [ ] Optional: Publish blog post or social media for bonus points

---

## 12. Submission Checklist

### Required
- [ ] **Hosted project URL** (Cloud Run URL)
- [ ] **Text description** (this document, condensed)
- [ ] **Features and functionality** (list with screenshots)
- [ ] **Technologies used** (all GCP services, ADK, Gemini, etc.)
- [ ] **Other data sources used** (sample documents, mock ERP)
- [ ] **Findings and learnings** (what worked, what didn't, future improvements)
- [ ] **Public/private code repository** (GitHub, shared with testing@devpost.com and cloudhackathons@google.com)
- [ ] **README.md** with step-by-step spin-up instructions
- [ ] **Architecture diagram** (system diagram + data flow)
- [ ] **~4-minute demo video** (follow script above)
- [ ] **Proof of GCP deployment** (Cloud Run dashboard, Firestore, logs shown in video)

### Bonus Points
- [ ] **Blog post** on dev.to or Medium: "How We Built an Autonomous Data Migration Agent on Google Cloud"
- [ ] **Social media post** on LinkedIn/X with #AllThingsAgenticHackathon
- [ ] **Gemma integration** (optional — local PII detection or simple classification)

---

## 13. Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| OCR accuracy on handwriting | Use Document AI + Gemini multimodal. For hackathon, use *clear* sample images. Mention "improves with better scans" in learnings. |
| Agent takes too long to process | Process one document at a time for demo. Mention "scales horizontally via Pub/Sub" in architecture. |
| Clarification UI not ready | Hardcode one clarification for demo. Show the flow end-to-end. |
| Uniplexity API not available | Build mock API layer. Structure code so real API drops in with one config change. |
| 11 days is tight | Scope to ONE document type (sales ledgers). Mention extensibility in "future work." |

---

## 14. Future Roadmap (Post-Hackathon)

- **Multi-document-type support:** Inventory, purchases, patient records
- **Gemma integration:** On-premise PII detection for sensitive healthcare data
- **Auto-learning from corrections:** When user fixes an agent mistake, agent learns via few-shot prompting
- **Batch API:** Allow clients to trigger migrations via API without UI
- **Migration templates:** Pre-built mappings for common business types (retail, clinic, restaurant)
- **Real-time sync:** Continuous monitoring of client email for new invoices/receipts

---

*Document version: 1.0*  
*Created for: All Things Agentic Hackathon, August 2026*  
*Team: Uniplexity*
