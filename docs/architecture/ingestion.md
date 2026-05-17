# Ingestion Layer

## Connector Taxonomy

| Category | Examples | Ingest Mode |
|----------|----------|-------------|
| Requirements Management | DOORS, Polarion, Jama | API / export |
| PLM / CAD | Teamcenter, Windchill, CATIA vault | API / event |
| ALM / SCM | Git, Jira, Azure DevOps | Webhook / poll |
| Test & V&V | TestRail, custom test DBs | API / DB |
| ERP / Supply Chain | SAP, Oracle | Batch |
| Documents | SharePoint, PDF, XLSX, email | Crawl / upload |
| Regulatory | FAA AC PDFs, EASA XML | Scheduled fetch |

## Processing Pipeline Stages

1. **Acquire** — Connector pulls or receives payload; stores raw blob with checksum.
2. **Classify** — Document type, program, subsystem, ITAR/export flags.
3. **Extract** — OCR (scanned PDFs), structure parse (tables, headers), metadata.
4. **Chunk** — Semantic chunking with section awareness; preserve requirement IDs.
5. **Enrich** — Aerospace NER (subsystems, DAL levels, part numbers, standards refs).
6. **Normalize** — Map to `CertificationEntity` subclasses; attach provenance.
7. **Publish** — Upsert graph nodes/edges; index chunks in vector store.

## Provenance Model

Every ingested artifact carries:

```json
{
  "source_system": "polarion",
  "source_uri": "project/REQ-1042",
  "ingested_at": "2026-05-16T12:00:00Z",
  "ingest_job_id": "job_abc123",
  "content_hash": "sha256:...",
  "classification": ["software", "flight_control"],
  "export_control": "EAR99"
}
```

## Idempotency

Re-ingestion keyed by `(source_system, source_uri, content_hash)`. Unchanged hashes skip downstream processing; changed hashes trigger impact re-analysis.
