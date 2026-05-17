# Security Architecture

## Threat Model Assumptions

- Certification data includes ITAR/EAR-controlled technical data
- Insiders and compromised connectors are in scope
- Public LLM APIs are untrusted for controlled data

## Controls

| Control | Implementation |
|---------|----------------|
| Authentication | OIDC / SAML via enterprise IdP |
| Authorization | RBAC + attribute-based (program, classification) |
| Encryption in transit | TLS 1.2+, mTLS service-to-service |
| Encryption at rest | DB TDE, SSE-S3/MinIO |
| Audit | Append-only audit log (who, what, when, source IP) |
| Network | Zero-trust; no implicit service trust |
| Secrets | Vault / K8s secrets; never in repo |
| Data residency | Per-tenant partition; air-gap bundle |

## Deployment Profiles

1. **Private cloud** — Customer VPC, managed K8s
2. **On-premises** — Full stack in customer DC
3. **Air-gapped** — Offline install bundle, manual update channel

## AI-Specific Security

- Prompt and response logging with redaction rules
- Retrieval scoped by user's program clearance
- Model weights and embeddings stay inside trust boundary
- Output filtering for export-controlled content in wrong context
