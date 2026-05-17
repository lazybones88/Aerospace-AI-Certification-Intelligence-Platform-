# Functional Hazard Assessment Excerpt — FCC (Demo)

**Program:** DAP-100  
**Document ID:** DAP100-FHA-FCC-001

---

## HAZ-FCC-003 — Erroneous attitude data to control laws

| Attribute | Value |
|-----------|-------|
| Hazard | Erroneous or delayed attitude data causes inappropriate surface commands |
| Severity | Catastrophic (under single-failure assumptions per ARP4754A process) |
| DAL | Level A software |
| Mitigation | SW-REQ-1042 (fusion rate), monitor M-FC-09, dual-channel cross-check |
| Status | Mitigation **under review** after fusion algorithm change in v2.4.1 |

**Certification impact:** Safety board has not re-approved mitigation closure for v2.4.1. This is tracked as **RISK-CERT-14** and may block flight test authorization if unresolved.

---

## HAZ-FCC-007 — Failure to enter fail-safe on channel disagreement

| Mitigation | SW-REQ-1055, TC-FCC-031 |
| Status | Closed for build 2.3.0 |
