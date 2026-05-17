# Knowledge Graph

## Schema Philosophy

The graph is the **certification source of truth for relationships**. Document storage is secondary; edges encode traceability and impact paths.

## Node Labels

- `Program` — Aircraft or system program
- `Subsystem` — LRU, software partition, hardware item
- `Requirement` — High-level, system, software, hardware requirements
- `SoftwareBuild` — Versioned deliverable
- `TestCase` / `TestResult`
- `Hazard` / `Mitigation`
- `SafetyAnalysis` — FHA, FMEA, SSA artifacts
- `CertificationObjective` — DO-178C Table A-* objectives, etc.
- `Approval` — Signed review records
- `Supplier` / `SupplierEvidence`
- `Document` — Parsed document reference
- `RegulatoryObligation` — Machine-readable standard clause

## Relationship Types

| Edge | Meaning |
|------|---------|
| `TRACES_TO` | Requirement decomposition / parent-child |
| `IMPLEMENTS` | Code/build satisfies requirement |
| `VERIFIES` | Test validates requirement or build |
| `SATISFIES` | Evidence meets certification objective |
| `MITIGATES` | Mitigation addresses hazard |
| `AFFECTS` | Change impacts downstream artifact |
| `DERIVES_FROM` | Safety/process derivation |
| `APPROVES` | Human authority sign-off |
| `REFERENCES` | Document cites standard or requirement |

## Impact Analysis

When node `N` changes (attribute or version):

1. Traverse outbound `AFFECTS`, `IMPLEMENTS`, `VERIFIES`, `SATISFIES` paths (configurable depth).
2. Collect impacted `CertificationObjective`, `Hazard`, `Approval` nodes.
3. Flag stale approvals and open gaps.
4. Emit `ImpactReport` for UI and agents.

Cypher templates live in `services/graph/src/graph_engine/queries/`.
