# Graph Report - autonomous-data-migration-agent  (2026-08-22)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 303 nodes · 461 edges · 24 communities (18 shown, 6 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 21 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `05f7ffc9`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- agents/__init__.py
- schemas.py
- MigrationDetail.tsx
- devDependencies
- compilerOptions
- services/__init__.py
- main.py
- FirestoreService
- dependencies
- router.py
- validate.py
- services
- run_command
- generate_report.py
- project_analyzer.py
- security_check.py
- app/__init__.py
- tests/__init__.py
- install.sh script

## God Nodes (most connected - your core abstractions)
1. `FirestoreService` - 17 edges
2. `compilerOptions` - 16 edges
3. `ValidationImportAgent` - 10 edges
4. `JobStatus` - 10 edges
5. `ClarificationRequest` - 9 edges
6. `MigrationJob` - 9 edges
7. `fail()` - 9 edges
8. `main()` - 9 edges
9. `DataCleaningAgent` - 8 edges
10. `DocumentUnderstandingAgent` - 8 edges

## Surprising Connections (you probably didn't know these)
- `DocumentUnderstandingAgent` --uses--> `DocumentType`  [INFERRED]
  backend/app/agents/document_understanding.py → backend/app/models/schemas.py
- `ValidationImportAgent` --uses--> `DataPreview`  [INFERRED]
  backend/app/agents/validation_import.py → backend/app/models/schemas.py
- `FirestoreService` --uses--> `ClarificationRequest`  [INFERRED]
  backend/app/services/firestore.py → backend/app/models/schemas.py
- `FirestoreService` --uses--> `DocumentItem`  [INFERRED]
  backend/app/services/firestore.py → backend/app/models/schemas.py
- `FirestoreService` --uses--> `JobStatus`  [INFERRED]
  backend/app/services/firestore.py → backend/app/models/schemas.py

## Import Cycles
- None detected.

## Communities (24 total, 6 thin omitted)

### Community 0 - "agents/__init__.py"
Cohesion: 0.07
Nodes (26): DataCleaningAgent, Any, DataAnomaly, Agent 3: Data Cleaning, Normalization & Anomaly Detection Agent., Normalize values, standardize dates, group product variants, flag anomalies., DocumentUnderstandingAgent, Any, Agent 1: Multimodal Document Understanding Agent. (+18 more)

### Community 1 - "schemas.py"
Cohesion: 0.10
Nodes (37): list_clarifications(), get, post, Clarifications human-in-the-loop API endpoints., submit_answer(), create_job(), get_job(), list_jobs() (+29 more)

### Community 2 - "MigrationDetail.tsx"
Cohesion: 0.09
Nodes (28): App(), AgentLog(), AgentLogProps, AuditTrailViewerProps, ClarificationCard(), ClarificationCardProps, DataPreviewTable(), DataPreviewTableProps (+20 more)

### Community 3 - "devDependencies"
Cohesion: 0.07
Nodes (28): autoprefixer, devDependencies, autoprefixer, postcss, tailwindcss, @types/react, @types/react-dom, typescript (+20 more)

### Community 4 - "compilerOptions"
Cohesion: 0.09
Nodes (21): compilerOptions, allowImportingTsExtensions, isolatedModules, jsx, lib, module, moduleResolution, noEmit (+13 more)

### Community 5 - "services/__init__.py"
Cohesion: 0.14
Nodes (12): get_upload_url(), BaseModel, post, Upload & GCS signed URL generation endpoints., UploadUrlRequest, UploadUrlResponse, Service abstractions for Firestore, Storage, and Pub/Sub., PubSubService (+4 more)

### Community 6 - "main.py"
Cohesion: 0.13
Nodes (11): Application Settings using Pydantic Settings., Settings, Core configuration module., health_check(), get, FastAPI Application Main Entry Point., root(), serve_spa() (+3 more)

### Community 7 - "FirestoreService"
Cohesion: 0.17
Nodes (5): FirestoreService, Any, MigrationJob, DocumentItem, JobStatus

### Community 8 - "dependencies"
Cohesion: 0.15
Nodes (13): axios, clsx, dependencies, axios, clsx, lucide-react, react, react-dom (+5 more)

### Community 9 - "router.py"
Cohesion: 0.22
Nodes (8): ClientItem, get_client_mappings(), list_clients(), Any, BaseModel, get, Clients & Learned Mappings endpoints., Central API Router aggregation.

### Community 10 - "validate.py"
Cohesion: 0.55
Nodes (10): fail(), load_json(), main(), validate_compatibility(), validate_instruction_budget(), validate_manifest(), validate_markdown_metadata(), validate_mcp() (+2 more)

### Community 11 - "services"
Cohesion: 0.22
Nodes (8): entrypoint, root, framework, root, rewrites, services, backend, frontend

### Community 12 - "run_command"
Cohesion: 0.46
Nodes (7): Path, check_backend(), check_frontend(), check_security(), main(), Execute shell command cleanly and return (success, output)., run_command()

## Knowledge Gaps
- **55 isolated node(s):** `UploadDropzoneProps`, `DashboardProps`, `MigrationDetailProps`, `NewMigrationProps`, `DataAnomaly` (+50 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `FirestoreService` connect `FirestoreService` to `schemas.py`, `services/__init__.py`?**
  _High betweenness centrality (0.043) - this node is a cross-community bridge._
- **Why does `ValidationImportAgent` connect `agents/__init__.py` to `schemas.py`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Why does `DataPreview` connect `schemas.py` to `agents/__init__.py`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `FirestoreService` (e.g. with `ClarificationRequest` and `DocumentItem`) actually correct?**
  _`FirestoreService` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `ValidationImportAgent` (e.g. with `MigrationPipeline` and `DataAnomaly`) actually correct?**
  _`ValidationImportAgent` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `JobStatus` (e.g. with `create_job()` and `approve_job_import()`) actually correct?**
  _`JobStatus` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `ClarificationRequest` (e.g. with `list_clarifications()` and `FirestoreService`) actually correct?**
  _`ClarificationRequest` has 2 INFERRED edges - model-reasoned connections that need verification._