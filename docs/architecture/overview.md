# Architecture Overview

## Problem Statement

Aerospace certification requires proving relationships across requirements, design, implementation, verification, safety analyses, and approvals — often stored in disconnected PLM, ALM, ERP, test, and document systems. Without a unified relationship model, AI reasoning lacks context and cannot be trusted for certification decisions.

## Core Architectural Pillars

### 1. Centralized Ingestion & Traceability

All evidence enters through a single ingestion plane with:

- **Connectors** for engineering systems (PLM, CAD vaults, ERP, test DBs, MRO, RM tools, SharePoint, email, files)
- **Normalization** into a canonical `CertificationEntity` model
- **Provenance** on every record: source system, URI, ingest job, content hash, classification labels
- **Processing pipelines**: OCR → parse → metadata extract → semantic chunk → aerospace NER

### 2. Knowledge Graph Intelligence Engine

Neo4j-backed graph storing typed nodes and edges:

- Nodes: `Requirement`, `Subsystem`, `SoftwareBuild`, `TestCase`, `TestResult`, `Hazard`, `Mitigation`, `Approval`, `CertificationObjective`, `Supplier`, `Document`
- Edges: `TRACES_TO`, `VERIFIES`, `IMPLEMENTS`, `MITIGATES`, `AFFECTS`, `APPROVES`, `DERIVES_FROM`, `SATISFIES`

Impact propagation traverses the graph when artifacts change (e.g., firmware update → requirements → tests → hazards → DO-178C objectives).

### 3. Grounded AI Layer

Multi-agent architecture with shared constraints:

| Agent | Responsibility |
|-------|----------------|
| Traceability | Link discovery, gap detection |
| Impact | Change propagation, affected artifact reports |
| Gap Analysis | Objective coverage vs. evidence |
| Evidence Validator | Test/report completeness checks |
| Audit Prep | Package assembly, readiness scoring |
| Risk Scorer | Hazard and schedule risk signals |

**RAG pipeline:** embed (aerospace-tuned) → retrieve from vector + graph context → generate → **deterministic validators** → attach `EvidenceRef[]`.

### 4. Regulatory Intelligence

Internal ontology mapping obligations from DO-178C, DO-254, ARP4754A, AS9100, DO-326A, FAA ACs, EASA guidance, MIL-STDs. Cross-framework relationships (e.g., ARP4754A safety process → DO-178C software objectives) are first-class edges.

### 5. Security & Trust

- Zero-trust API gateway with RBAC and immutable audit logs
- Encryption at rest (DB, object store) and in transit (TLS/mTLS)
- Deployment profiles: SaaS-private, customer VPC, on-prem, air-gapped
- Enterprise LLM hosting (vLLM, Azure OpenAI private, etc.) — no mandatory public API

### 6. Operational Interface

Role-based dashboards for engineers, quality, certification leads, suppliers (limited), executives, and regulator views (export-controlled).

## Data Flow

```
Source Systems → Connectors → Raw Store → Parsers → Normalized Entities
                                                      ↓
                                            Graph + Vector Index
                                                      ↓
                              Agents ← RAG ← Graph Context + Retrieval
                                                      ↓
                                    Validated Response + Citations
                                                      ↓
                                              Web / API / Exports
```

## Technology Choices

| Concern | Technology | Rationale |
|---------|------------|-----------|
| Graph | Neo4j | Dependency tracing, Cypher impact queries |
| Relational metadata | PostgreSQL | Jobs, users, config, audit |
| Vectors | Qdrant (or pgvector) | Semantic retrieval with filters |
| Object storage | MinIO / S3 | Raw documents, parsed artifacts |
| Queue | Redis + ARQ | Async ingestion jobs |
| API | FastAPI | Typed Python, OpenAPI |
| Web | Next.js 14 | Dashboards, graph visualization |
| Auth | OIDC-ready (Keycloak-compatible) | Enterprise SSO |

## Non-Goals (Phase 1)

- Fully autonomous certification sign-off
- Replacing authoritative CM/RM systems of record
- Public-cloud-only deployment assumption
