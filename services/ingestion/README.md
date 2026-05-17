# Ingestion Service

Connectors acquire raw evidence; parsers extract structure; the pipeline normalizes into domain entities and publishes to the graph and vector index.

## Connectors (planned)

| Connector | Module | Status |
|-----------|--------|--------|
| File upload / watch folder | `connectors/file_upload.py` | Implemented |
| Polarion | `connectors/polarion.py` | Planned |
| IBM DOORS | `connectors/doors.py` | Planned |
| SharePoint | `connectors/sharepoint.py` | Planned |
| Git / ALM | `connectors/git.py` | Planned |

## Pipeline stages

See [docs/architecture/ingestion.md](../../docs/architecture/ingestion.md).

## Running tests

```bash
pip install -e "../../packages/domain" -e ".[dev]"
pytest
```
