# TASKS.md — Project Sprint Roadmap

## Milestone 1: Core Foundation & Scaffold (Days 1–2)
- [x] Create project repository structure and governance baseline
- [x] Write implementation plan and comprehensive README.md
- [x] Build FastAPI backend application shell
- [x] Build React 18 + Vite + TypeScript frontend web app shell
- [x] Configure AFAC validation scripts (`scripts/validate.py` & `scripts/verify.py`)

## Milestone 2: Upload & Async Ingestion (Days 3–4)
- [ ] Implement direct GCS upload URL generation endpoint
- [ ] Build React drag-and-drop UploadDropzone component
- [ ] Set up Firestore job and document status models
- [ ] Implement Pub/Sub async trigger handler

## Milestone 3: Agent Swarm Implementation (Days 5–8)
- [ ] Implement Document Understanding Agent (multimodal OCR & table extraction)
- [ ] Implement Schema Mapping Agent with client memory
- [ ] Build Clarification UI card and human-in-the-loop endpoint
- [ ] Implement Data Cleaning Agent (fuzzy product grouping, date standardization)

## Milestone 4: Validation, Import & Audit (Days 9–11)
- [ ] Build Validation & Import Agent (dry-run preview generation)
- [ ] Build DataPreviewTable and AuditTrailViewer UI components
- [ ] Execute end-to-end demo walkthrough verification
