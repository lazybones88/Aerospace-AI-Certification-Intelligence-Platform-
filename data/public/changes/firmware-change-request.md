# Change Request — FCC Firmware v2.4.1 (Demo)

**CR ID:** CR-FCC-241  
**Program:** DAP-100  
**Title:** Avionics firmware update v2.4.1  
**Status:** In review

---

## Description

Update Flight Control Computer firmware from **FCC-SW-2.3.0** to **FCC-SW-2.4.1**.

### Changes included

1. Sensor fusion algorithm optimization (SW-REQ-1042 implementation)
2. Boot loader path update (SW-REQ-1060)
3. Minor scheduling adjustments in control loop (SYS-REQ-1001)

---

## Impacted artifacts (identified by engineering)

| Artifact ID | Impact |
|-------------|--------|
| SW-REQ-1042 | Implementation changed — retest required |
| SW-REQ-1060 | Boot path changed — retest required |
| TC-FCC-020 | Must re-execute on build 2.4.1 |
| TC-FCC-040 | Must re-execute on build 2.4.1 |
| HAZ-FCC-003 | Mitigation effectiveness re-analysis required |
| OBJ-A7-FCC | Certification objective evidence set incomplete |
| FT-GATE-3 | **Flight test gate at risk** if RISK-CERT-07 / RISK-CERT-14 remain open |

---

## Approval

| Role | Status |
|------|--------|
| Software lead | Approved |
| Certification | **Pending** — awaiting test evidence |
| Safety board | **Pending** — HAZ-FCC-003 review |
