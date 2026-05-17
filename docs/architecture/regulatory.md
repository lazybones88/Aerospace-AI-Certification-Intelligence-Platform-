# Regulatory Intelligence

## Ontology Structure

```
Standard (e.g., DO-178C)
  └── Part / Section
        └── Obligation (machine-readable clause)
              └── Objective (Table A-*)
                    └── Activity (engineering activity type)
                          └── EvidenceType (expected artifact)
```

## Cross-Framework Mapping

Example edges in the regulatory subgraph:

- `ARP4754A` safety assessment process → `DO-178C` software lifecycle objectives
- `DO-254` hardware objectives → shared verification evidence with `DO-178C` at system level
- `DO-326A` cybersecurity → supplemental objectives linked to software requirements

## Ingestion Sources

- Structured: XML/HTML from EASA, some FAA datasets
- Semi-structured: PDF advisory circulars (parsed to clauses)
- Curated: Internal SME mappings for MIL-STDs and company supplements

## Continuous Monitoring (Phase 2+)

Scheduled jobs diff new standard revisions against stored obligations; emit `RegulatoryChangeAlert` for impacted programs.

## Usage in Agents

Gap analysis agents query: *"Which DO-178C Level A objectives lack linked test evidence for subsystem X?"* by joining `RegulatoryObligation` → `SATISFIES` ← evidence nodes.
