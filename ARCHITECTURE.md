# ARCHITECTURE.md — Uniplexity Migration Agent Technical Architecture

## 1. Executive Architecture Overview

The **Uniplexity Migration Agent** is an event-driven, multimodal agentic swarm designed to migrate legacy business records (sales ledgers, inventory counts, purchase orders) into Uniplexity ERP.

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│  React 18 UI    │ ────▶ │  FastAPI Server │ ────▶ │  Cloud Pub/Sub  │
│  (Vite App)     │ ◀──── │  (Cloud Run)    │ ◀──── │  Async Queue    │
└─────────────────┘       └─────────────────┘       └─────────────────┘
                                   │                         │
                                   ▼                         ▼
                          ┌─────────────────┐       ┌─────────────────┐
                          │    Firestore    │ ◄───  │ Google ADK      │
                          │   State DB      │       │ Agent Swarm     │
                          └─────────────────┘       └─────────────────┘
```

---

## 2. Agent Swarm Pipeline Design

The migration workflow executes as a sequential agent pipeline using Google ADK:

### Pipeline Execution Order:
1. **Document Understanding Agent:** Parses uploaded PDF/Image/Excel documents. Uses Gemini 3.5 Flash vision capability to transcribe tables, classify document type, detect column headers, and identify raw text.
2. **Schema Mapping Agent:** Maps extracted raw columns to Uniplexity ERP target schema (e.g. `sale_date`, `customer_name`, `product_name`, `quantity`, `unit_price`). Checks client learned memory for past mappings. If mapping confidence is under 70%, generates a `ClarificationRequest`.
3. **Data Cleaning & Anomaly Agent:** Standardizes formats (ISO 8601 dates, numeric currencies), fuzzy-groups product variants (e.g., "Coke" -> "Coca-Cola"), flags duplicates, and identifies business rule anomalies.
4. **Validation & Import Agent:** Generates a dry-run preview, verifies human approval, writes to the target ERP database, and writes an indelible step-by-step audit record.

---

## 3. Data Flow & State Machine

Every migration job transitions through explicit lifecycle states:

```
[uploading] ──▶ [processing] ──▶ [clarifying] (if ambiguous)
                                      │
                                      ▼
[awaiting_approval] ◀─────────────────┘
         │
         ├──▶ [importing] ──▶ [completed]
         │
         └──▶ [failed]
```

---

## 4. Firestore Database Collections

- `jobs`: Tracks overall job metadata, completion status, record counts, and timers.
- `documents`: Individual files uploaded within a job along with extracted JSON representation.
- `clarifications`: Active and resolved questions asked by agents during schema mapping.
- `client_mappings`: Learned mapping rules and product normalizations per client.
- `audit_trails`: Event timeline capturing every decision made by each agent.
