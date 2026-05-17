# Testing the Platform (Demo Data)

This walkthrough uses **synthetic public documents** in `data/public/` to prove traceability, grounded Q&A, and impact analysis work end-to-end — no Docker or external AI APIs required.

## 1. Start the API

From the repository root (PowerShell):

```powershell
$env:PYTHONPATH = "packages/domain/src;services/intelligence/src;services/graph/src;services/gateway/src"
python -m uvicorn gateway.main:app --host 127.0.0.1 --port 8000
```

Open **http://127.0.0.1:8000/docs**

## 2. Confirm demo documents are loaded

**GET** `/api/v1/documents` — should list 6 markdown files under `data/public/`.

## 3. Ask a certification question (grounded)

**POST** `/api/v1/ask`

```json
{
  "question": "Which unresolved certification risks could delay flight testing?",
  "program_id": "dap-100"
}
```

**Expected:** `confidence` is `authoritative` (not `insufficient_evidence`), with `evidence` citing chunks from `software-requirements.md` and related files. The answer references RISK-CERT-07, RISK-CERT-14, and FT-GATE-3.

## 4. Firmware impact question

```json
{
  "question": "Show all requirements impacted by the avionics firmware update",
  "program_id": "dap-100"
}
```

**Expected:** Answer mentions SW-REQ-1042, SW-REQ-1060, TC-FCC-020, HAZ-FCC-003, CR-FCC-241.

## 5. Impact analysis (knowledge graph)

**POST** `/api/v1/impact/analyze`

```json
{
  "entity_id": "sw-req-1042",
  "program_id": "dap-100",
  "change_description": "Avionics firmware v2.4.1 update"
}
```

**Expected:** Multiple impacted items including `haz-fcc-003`, `obj-a7-fcc`, `ft-gate-3`.

## 6. Dashboard metrics

**GET** `/api/v1/programs/dap-100/dashboard`

**Expected:** Non-zero `open_gaps`, `unresolved_risks`, and `requirements_traced_pct`.

## 7. Web UI (optional)

```powershell
cd apps/web
npm run dev
```

Open http://localhost:3000 — use program **`dap-100`** in future UI wiring; default questions already match demo content.

## 8. Automated tests

```powershell
python -m pytest packages/domain/tests services/intelligence/tests -q
```

## What this proves

| Capability | Demo proof |
|------------|------------|
| Centralized evidence | Markdown in `data/public/` |
| Normalization / chunking | `LocalDocumentRetriever` |
| Grounded AI (no hallucination) | Answers refuse without evidence; cite chunks with data loaded |
| Knowledge graph impact | `dap-100-graph.json` + `InMemoryGraphStore` |
| Operational metrics | Dashboard endpoint |

## Full stack (optional)

With Docker Desktop:

```powershell
docker compose -f infrastructure/docker-compose.yml up -d
```

Then connect Neo4j for persistent graph storage (future; demo uses in-memory JSON today).
