# Software Verification Results — FCC (Demo)

**Program:** DAP-100  
**Document ID:** DAP100-SVR-FCC-002  
**Revision:** B

---

## TC-FCC-012 — Control loop latency measurement

| Field | Value |
|-------|-------|
| Requirement | SYS-REQ-1001 |
| Build tested | FCC-SW-2.3.0 |
| Result | **PASS** |
| Max observed latency | 7.8 ms |
| Date | 2026-03-12 |

---

## TC-FCC-020 — Sensor fusion output rate

| Field | Value |
|-------|-------|
| Requirement | SW-REQ-1042 |
| Build tested | FCC-SW-2.3.0 |
| Result | **PASS** |
| Observed rate | 120 Hz |
| Date | 2026-03-14 |

**Note:** Build FCC-SW-2.4.1 (firmware CR-FCC-241) has **not** been tested against TC-FCC-020. Status: **NOT RUN** — blocks closure of RISK-CERT-07.

---

## TC-FCC-031 — Fail-safe entry timing

| Field | Value |
|-------|-------|
| Requirement | SW-REQ-1055 |
| Build tested | FCC-SW-2.3.0 |
| Result | **PASS** |
| Observed entry time | 38 ms |

---

## TC-FCC-040 — Boot-time firmware signature verification

| Field | Value |
|-------|-------|
| Requirement | SW-REQ-1060 |
| Build tested | FCC-SW-2.3.0 |
| Result | **PASS** |

**Stale evidence warning:** Results above apply to build 2.3.0 only. CR-FCC-241 introduces new boot loader path — **re-test mandatory** before certification package update.
