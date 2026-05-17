# AI Layer

## Design Constraint: No Ungrounded Answers

Every generative output must include:

1. **Evidence references** — Document ID, chunk ID, graph node ID, standard clause
2. **Confidence tier** — `AUTHORITATIVE` | `INFERRED` | `INSUFFICIENT_EVIDENCE`
3. **Validator results** — Pass/fail per deterministic rule

If retrieval returns insufficient evidence, the system responds with `INSUFFICIENT_EVIDENCE` rather than hallucinating.

## RAG Stack

```
Query → Query expansion (optional) → Hybrid retrieval
         ├─ Vector search (filtered by program/subsystem)
         └─ Graph neighborhood (k-hop context)
      → Rerank → Context assembly → LLM → Validators → Response
```

## Agent Orchestration

Agents implement a common `AgentTask` interface:

- Input: structured context (entity IDs, change set, objective scope)
- Tools: `graph_query`, `vector_search`, `validate_trace`, `list_gaps`
- Output: `AgentResult` with citations and recommended human actions

Orchestration is sequential for auditability in Phase 1; parallel tool calls allowed where logged.

## Deterministic Validators (Examples)

- **Trace completeness** — Every software requirement has ≥1 test or review record
- **Objective coverage** — All in-scope DO-178C objectives have linked evidence
- **Stale approval** — Approved artifact has downstream change without re-approval
- **Citation integrity** — Every claim maps to retrieved chunk IDs

Validators run **after** generation and can veto or downgrade responses.

## Model Hosting

| Profile | Deployment |
|---------|------------|
| Enterprise private | vLLM / TGI on customer GPU cluster |
| Air-gapped | Bundled quantized models, no egress |
| Hybrid | Embeddings on-prem, optional cloud burst (disabled by default) |

Embedding model default: aerospace/regulatory corpus fine-tune path documented in `services/intelligence/README.md`.
