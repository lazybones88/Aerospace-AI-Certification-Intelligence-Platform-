# Product Roadmap

## Phase 1 — Traceability & Impact (Current)

**Goal:** Measurable ROI through AI-assisted traceability while keeping humans in the loop.

| Capability | Status | Notes |
|------------|--------|-------|
| Connector framework (PLM, RM, files, email) | Scaffolded | IBM DOORS, Polarion, SharePoint, PDF/XLSX |
| Document parsing (OCR, chunking, NER) | Scaffolded | Aerospace terminology lexicon |
| Provenance & audit trail on every artifact | Implemented | `TraceableRecord` domain primitive |
| Knowledge graph schema | Implemented | Requirements ↔ tests ↔ hazards ↔ objectives |
| Impact analysis API | Scaffolded | Change → affected artifacts propagation |
| RAG with mandatory citations | Scaffolded | No answer without `EvidenceRef` |
| Deterministic validators | Scaffolded | Gap detection, trace completeness |
| Engineer dashboards | Scaffolded | NL query, dependency map placeholders |

## Phase 2 — Evidence Validation & Audit Prep

- Automated evidence gap detection against DO-178C / ARP4754A objectives
- Audit-readiness scoring and package assembly
- Supplier evidence ingestion and risk signals
- Regulatory change monitoring (delta alerts on standards updates)

## Phase 3 — Predictive Intelligence

- Certification delay risk models (schedule integration)
- Weak traceability chain detection
- Audit failure likelihood scoring
- Supplier and subsystem risk heat maps

## Phase 4 — Semi-Autonomous Workflows

- Certification package generation (human sign-off required)
- Change-request impact workflows with approval routing
- Regulator-facing evidence exports (controlled views)

## Design Principles

1. **Explainability over fluency** — Every AI output must cite sources and pass validators.
2. **Graph before chat** — Relationships are the source of truth; RAG retrieves from the graph context.
3. **Augment, don't replace** — Engineers retain authority; the platform accelerates review.
4. **Deploy anywhere** — On-prem, air-gapped, and private cloud are equal citizens.
