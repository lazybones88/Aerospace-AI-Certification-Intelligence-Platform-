# Requirements Traceability Matrix Excerpt — FCC (Demo)

**Program:** DAP-100

| Requirement | Implements / Verifies | Test | Hazard | DO-178C Objective |
|-------------|----------------------|------|--------|-------------------|
| SYS-REQ-1001 | SW build | TC-FCC-012 | — | A-7 |
| SW-REQ-1042 | Fusion module | TC-FCC-020 | HAZ-FCC-003 | A-7 |
| SW-REQ-1055 | Fail-safe logic | TC-FCC-031 | HAZ-FCC-007 | A-7 |
| SW-REQ-1060 | Boot verifier | TC-FCC-040 | — | A-7 |

## Traceability gaps (auto-review flags)

1. **SW-REQ-1042 → TC-FCC-020:** No test execution on build FCC-SW-2.4.1.
2. **SW-REQ-1060 → TC-FCC-040:** Evidence stale after CR-FCC-241.
3. **HAZ-FCC-003:** Mitigation not re-verified for v2.4.1.

**Impact preview:** A change to SW-REQ-1042 or firmware build 2.4.1 affects HAZ-FCC-003, objective A-7 evidence, and flight test gate FT-GATE-3.
