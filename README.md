# Uniplexity Migration Agent

[![AFAC Version](https://img.shields.io/badge/AFAC-version-1.0.0-blue.svg)](https://github.com/google-cloud-hackathons/all-things-agentic)
<!-- AFAC version-1.0.0 -->
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Google%20Cloud-orange.svg)](https://cloud.google.com)

> **All Things Agentic Hackathon Submission**  
> **Track:** The Taskmaster ($20,000)  
> **Target Prizes:** The Taskmaster, Best Architectural Design ($5,000), Best Multimodal UX ($5,000)

An autonomous AI employee built on the **Google Agent Development Kit (ADK)** and **Gemini 3.5 Flash** that ingests years of messy, unstructured historical business records — handwritten ledgers, Excel spreadsheets, scanned PDFs — and migrates them into Uniplexity ERP with minimal human intervention.

---

## 1. The Problem & Solution

### The Problem
When onboarding new clients, Uniplexity inherits 2–3 years of sales, inventory, purchase, and patient records. These records exist in physical notebooks, legacy Excel files, and scanned PDFs. Every client formats their data differently: varying column titles, handwritten abbreviations, inconsistent date formats, and custom product names. Standard OCR extracts characters but fails to interpret context or business meaning, making manual data entry slow, expensive, and error-prone.

### The Solution
The **Uniplexity Migration Agent** is an enterprise-grade agentic swarm that takes end-to-end responsibility for historical data migration:
1. **Multimodal Ingestion:** Extracts text and complex table structures from scanned handwritten ledgers, PDFs, and spreadsheets via Document AI and Gemini Vision.
2. **Context-Aware Schema Mapping:** Maps non-standard columns to Uniplexity's core ERP schemas using learned client memory.
3. **Human-in-the-Loop Clarification:** Identifies ambiguous abbreviations or low-confidence mappings and prompts the user with concise, targeted questions.
4. **Data Cleaning & Anomaly Detection:** Standardizes date/currency formats, groups fuzzy product variants, and flags impossible prices or future dates.
5. **Dry-Run & Audit Trail:** Provides a full dry-run preview and permanent step-by-step decision audit logs before committing changes to the production ERP.

---

## 2. Agent Swarm Architecture

The core migration pipeline uses a sequential 4-agent swarm built using Google ADK:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                 GOOGLE ADK AGENT SWARM                                  │
│                                                                                        │
│  ┌────────────────────┐    ┌────────────────────┐    ┌──────────────────────────────┐  │
│  │ 1. Document        │───▶│ 2. Schema          │───▶│ 3. Data Cleaning             │  │
│  │    Understanding   │    │    Mapping         │    │    & Anomaly Agent           │  │
│  │    Agent           │    │    Agent           │    │                              │  │
│  │  • Multimodal OCR  │    │  • Column mapping  │    │  • Fuzzy product grouping    │  │
│  │  • Table structure │    │  • Type inference  │    │  • ISO date standardization  │  │
│  │  • Classification  │    │  • Ask clarification│   │  • Deduplication & anomalies │  │
│  └────────────────────┘    └────────────────────┘    └──────────────────────────────┘  │
│                                                                     │                  │
│                                                                     ▼                  │
│                                                      ┌──────────────────────────────┐  │
│                                                      │ 4. Validation & Import       │  │
│                                                      │    Agent                     │  │
│                                                      │  • Business rule validation  │  │
│                                                      │  • Dry-run preview           │  │
│                                                      │  • Audit trail generation    │  │
│                                                      │  • ERP DB Commit / Rollback   │  │
│                                                      └──────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. High-Level Technology Stack

| Layer | Technology | Description |
|-------|------------|-------------|
| **Frontend** | React 18 + Vite + TypeScript + Tailwind CSS | Interactive dashboard, file dropzone, clarification UI, preview table |
| **Backend** | FastAPI + Python 3.11 | Async API server, Cloud Run host, Pub/Sub webhook receiver |
| **Agent Framework** | **Google ADK** | Sequential agent pipeline, tool binding, state orchestration |
| **AI Models** | Gemini 3.5 Flash (Vertex AI / Google AI Studio) | Multimodal reasoning, document extraction, schema mapping |
| **Database (State)** | Firestore | Persistent job states, document progress, client memory, audit logs |
| **Database (Target)** | Cloud SQL (PostgreSQL) / Uniplexity API | Final target destination for validated ERP records |
| **Storage & Queue** | Cloud Storage & Cloud Pub/Sub | Scalable document storage and asynchronous processing queue |
| **Deployment** | Google Cloud Run | Serverless single/multi container deployment |

---

## 4. Repository Structure

```text
.
├── .agents/                 # AFAC workspace configuration, personas, skills
├── backend/                 # FastAPI server & Google ADK Agent Swarm
│   ├── app/
│   │   ├── agents/          # Document, Schema, Cleaning, Validation ADK agents
│   │   ├── api/             # REST API routers (jobs, upload, clarification, preview)
│   │   ├── core/            # App configuration & settings
│   │   ├── models/          # Pydantic schemas & data types
│   │   ├── services/        # Firestore, Storage, Pub/Sub integrations
│   │   └── main.py          # FastAPI application entry point
│   ├── tests/               # Pytest suite
│   ├── Dockerfile           # Cloud Run production container file
│   └── requirements.txt     # Python dependencies
├── frontend/                # React 18 + Vite + TypeScript web application
│   ├── src/
│   │   ├── components/      # UI components (Dropzone, Progress, Clarifications, Table)
│   │   ├── pages/           # Views (Dashboard, New Migration, Detail, Clarification Center)
│   │   ├── services/        # API client bindings
│   │   ├── types/           # TypeScript interfaces
│   │   ├── App.tsx          # Main shell component
│   │   └── main.tsx         # Bootstrap entry point
│   ├── index.html           # Single page application HTML template
│   ├── package.json         # Node.js dependencies & scripts
│   └── vite.config.ts       # Vite configuration with backend proxy
├── data/
│   └── sample_documents/    # Sample ledgers and spreadsheets for testing
├── docs/                    # Project walkthroughs and architectural documentation
├── scripts/                 # Verification and validation scripts
├── AGENTS.md                # System policy & execution protocol (Source of Truth)
├── ARCHITECTURE.md          # Full technical architecture specification
├── INSTRUCTIONS.md          # Code standards & design rules
├── SECURITY.md              # Security & data privacy policies
├── TASKS.md                 # Project roadmap & milestone tracking
└── README.md                # Main repository guide (this file)
```

---

## 5. Quickstart & Local Setup

### Prerequisites
- **Python:** 3.11+
- **Node.js:** 18+
- **Google Cloud SDK** (optional for local mock mode)

### 1. Clone & Set Up Environment
```bash
git clone https://github.com/kondwani0099/autonomous-data-migration-agent.git
cd autonomous-data-migration-agent
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

Set environment variables (or create `.env` file in root):
```env
GEMINI_API_KEY="your-gemini-api-key"
GCP_PROJECT_ID="your-gcp-project"
MOCK_GCP="true"  # Set true to run locally without active GCP credentials
```

Run backend server:
```bash
uvicorn app.main:app --reload --port 8000
```
Backend API will be available at `http://localhost:8000`. OpenAPI docs at `http://localhost:8000/docs`.

### 3. Frontend Setup
```bash
cd ../frontend
npm install
npm run dev
```
Frontend UI will be available at `http://localhost:5173`.

---

## 6. API Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Server status check |
| `POST` | `/api/jobs` | Create a new data migration job |
| `GET` | `/api/jobs` | List all active/historical migration jobs |
| `GET` | `/api/jobs/{job_id}` | Get detailed job progress & document list |
| `POST` | `/api/jobs/{job_id}/upload-url` | Generate direct upload URL for files |
| `GET` | `/api/jobs/{job_id}/clarifications` | Fetch pending agent questions |
| `POST` | `/api/clarifications/{id}/answer` | Submit human user response to resume pipeline |
| `GET` | `/api/jobs/{job_id}/preview` | Retrieve dry-run preview & anomaly summary |
| `POST` | `/api/jobs/{job_id}/approve` | Approve final data import to ERP |
| `GET` | `/api/jobs/{job_id}/audit` | Retrieve complete step-by-step audit log |

---

## 7. Running Verification & Checks

The repository includes dynamic verification scripts to validate structural integrity and code quality:

```bash
# Validate workspace structure and manifest policy
python scripts/validate.py

# Run backend pytest suite & frontend quality checks
python scripts/verify.py
```

---

## 8. License

Distributed under the MIT License. See `LICENSE` for details.