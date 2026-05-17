# Intelligence Service

RAG pipeline, specialized agents, and deterministic validators. **No ungrounded answers** — insufficient retrieval yields `INSUFFICIENT_EVIDENCE`.

## Agents

| Agent | ID | Phase |
|-------|-----|-------|
| Impact Analysis | `impact-analysis` | 1 |
| Traceability / Gap | `traceability` | 1 (planned) |
| Evidence Validator | `evidence-validator` | 2 |
| Audit Prep | `audit-prep` | 2 |
| Risk Scorer | `risk-scorer` | 3 |

## Enterprise LLM

Configure via environment — never hardcode API keys:

- `LLM_PROVIDER=local|azure|openai`
- `LLM_BASE_URL` for vLLM/TGI endpoints
- `EMBEDDING_MODEL` for vector index

Air-gapped deployments set `LLM_PROVIDER=local` with bundled weights.
