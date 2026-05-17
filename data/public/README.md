# Public Demo Certification Documents

**Synthetic, fictional data only** — for local testing and demonstrations.  
Not derived from any real aircraft program, supplier data, or export-controlled material.

## Purpose

These files let you verify that the platform can:

1. **Ingest** markdown certification evidence
2. **Retrieve** relevant chunks for natural-language questions
3. **Ground** API answers in cited source excerpts
4. **Trace impact** across requirements, tests, hazards, and objectives

## Program

| Field | Value |
|-------|-------|
| Program ID | `dap-100` |
| Name | Demo Aircraft Program (fictional) |
| Subsystem | Avionics / Flight Control Computer (FCC) |

## Documents

| File | Type |
|------|------|
| [requirements/software-requirements.md](requirements/software-requirements.md) | Software requirements |
| [verification/test-results.md](verification/test-results.md) | Test procedures and results |
| [safety/hazard-assessment.md](safety/hazard-assessment.md) | FHA / hazard log excerpt |
| [traceability/trace-matrix.md](traceability/trace-matrix.md) | Requirements trace matrix |
| [regulatory/obligations-summary.md](regulatory/obligations-summary.md) | Paraphrased obligation summaries (not full standards text) |
| [changes/firmware-change-request.md](changes/firmware-change-request.md) | Change request for firmware v2.4.1 |
| [graph/dap-100-graph.json](graph/dap-100-graph.json) | Demo knowledge-graph relationships |

## Quick test

```powershell
# Start API (from repo root)
$env:PYTHONPATH = "packages/domain/src;services/intelligence/src;services/gateway/src"
python -m uvicorn gateway.main:app --port 8000

# Ask a question grounded in these documents
$body = '{"question":"Which certification risks could delay flight testing?","program_id":"dap-100"}'
Invoke-RestMethod -Uri http://127.0.0.1:8000/api/v1/ask -Method Post -Body $body -ContentType "application/json"
```

See [docs/TESTING.md](../../docs/TESTING.md) for the full test walkthrough.
