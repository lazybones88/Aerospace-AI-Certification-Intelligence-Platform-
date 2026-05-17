# Aerospace AI Certification Intelligence Platform

A traceability-first certification intelligence platform that unifies engineering evidence, regulatory obligations, and AI-assisted reasoning into a living digital certification model.

## Vision

Aerospace certification is a **relationship-management problem**: every requirement, design decision, software change, test result, risk analysis, and approval must be connected and provable. This platform centralizes ingestion, normalizes heterogeneous evidence, maps relationships in a knowledge graph, and grounds AI outputs in authoritative, auditable sources.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Operational Interface (Web)                          │
│   Dashboards · NL queries · Impact maps · Audit readiness · Risk heat maps   │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
┌─────────────────────────────────────────────────────────────────────────────┐
│                            API Gateway (gateway)                             │
│         Auth · RBAC · Audit logging · Rate limits · Request routing          │
└─────────────────────────────────────────────────────────────────────────────┘
          │              │              │              │              │
          ▼              ▼              ▼              ▼              ▼
   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
   │ Ingestion│   │  Graph   │   │Intelligence│  │Regulatory│   │ Security │
   │  Layer   │   │  Engine  │   │  (AI/RAG) │   │ Ontology │   │  Layer   │
   └──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘
          │              │              │              │
          └──────────────┴──────────────┴──────────────┘
                              │
                    ┌─────────┴─────────┐
                    │  Data Stores      │
                    │  Neo4j · Postgres │
                    │  Vector DB · S3   │
                    └───────────────────┘
```

## Monorepo Structure

| Path | Purpose |
|------|---------|
| `packages/domain` | Shared ontology, entities, traceability primitives |
| `services/ingestion` | Connectors, parsers, normalization pipelines |
| `services/graph` | Knowledge graph API, impact propagation, Cypher schema |
| `services/intelligence` | RAG, agents, embeddings, deterministic validation |
| `services/regulatory` | Standards ingestion, obligation mapping |
| `services/gateway` | Unified REST API, auth integration |
| `apps/web` | Engineer-facing operational interface |
| `infrastructure` | Docker Compose, deployment manifests |
| `docs/architecture` | Detailed architecture specifications |

## Phase 1 Focus (Current)

Per industry adoption constraints, the initial release targets **human-reviewable augmentation**, not full automation:

- Centralized data ingestion with full provenance (`source_system`, `ingested_at`, `content_hash`)
- Normalized certification entities (requirements, tests, hazards, approvals)
- Knowledge graph traceability and **impact analysis**
- RAG-grounded Q&A with mandatory source citations
- Deterministic validation layered on generative outputs

See [docs/roadmap.md](docs/roadmap.md) for phased expansion.

## Quick Start

### Prerequisites

- Docker Desktop (or Docker Engine + Compose v2)
- Node.js 20+ (for web app)
- Python 3.11+ (for backend services)

### Local Development

**Quick demo (no Docker):** uses synthetic documents in [`data/public/`](data/public/).

```powershell
# From repo root
pip install -e "packages/domain[dev]" -e "services/intelligence"
$env:PYTHONPATH = "packages/domain/src;services/intelligence/src;services/graph/src;services/gateway/src"
python -m uvicorn gateway.main:app --port 8000
```

Then follow [docs/TESTING.md](docs/TESTING.md) or run `scripts/verify_demo.ps1`.

```bash
# Full stack (optional — requires Docker)
docker compose -f infrastructure/docker-compose.yml up -d
cd apps/web && npm install && npm run dev
```

Open http://localhost:3000 (web) and http://localhost:8000/docs (API).  
Use program ID **`dap-100`** for demo queries.

## Supported Standards (Regulatory Layer)

DO-178C, DO-254, ARP4754A, AS9100, DO-326A, FAA ACs, EASA CS/GMs, MIL-STDs — structured as machine-readable obligations linked to engineering artifacts.

## Security Posture

Designed for **hybrid deployment**: on-premises, air-gapped, and private cloud. Zero-trust access, encryption at rest/in transit, RBAC, immutable audit logs, and optional ITAR-controlled partitions. No dependency on public LLM APIs for sensitive workloads — enterprise model hosting is a first-class deployment mode.

## Documentation

- [Architecture Overview](docs/architecture/overview.md)
- [Ingestion Layer](docs/architecture/ingestion.md)
- [Knowledge Graph](docs/architecture/knowledge-graph.md)
- [AI & Agents](docs/architecture/ai-layer.md)
- [Regulatory Intelligence](docs/architecture/regulatory.md)
- [Security](docs/architecture/security.md)
- [Product Roadmap](docs/roadmap.md)

## License

Proprietary — All rights reserved unless otherwise specified.
