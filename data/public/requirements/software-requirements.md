# Software Requirements — FCC Avionics (Demo)

**Program:** DAP-100 (fictional)  
**Subsystem:** Flight Control Computer (FCC)  
**DAL:** Level A  
**Document ID:** DAP100-SRD-FCC-001  
**Revision:** C  
**Status:** Approved

---

## SYS-REQ-1001 — Flight control loop latency

The flight control software shall complete the primary control loop within **10 milliseconds** under nominal load conditions.

- **Rationale:** Latency beyond 10 ms may degrade handling qualities.
- **Verification method:** Test
- **Linked tests:** TC-FCC-012, TC-FCC-013

---

## SW-REQ-1042 — Sensor fusion update rate

The sensor fusion module shall publish fused attitude data at a minimum rate of **100 Hz** to downstream consumers.

- **Rationale:** Supports control law stability per system safety assessment.
- **Verification method:** Test + Review
- **Linked tests:** TC-FCC-020
- **Safety link:** HAZ-FCC-003

---

## SW-REQ-1055 — Fail-safe mode entry

Upon detection of redundant channel disagreement exceeding configured thresholds, the software shall enter **fail-safe mode** within **50 ms**.

- **Verification method:** Test
- **Linked tests:** TC-FCC-031, TC-FCC-032
- **Certification objective:** DO-178C Table A-7 (verification of software integration)

---

## SW-REQ-1060 — Firmware integrity check at boot

At power-up, the FCC shall verify the digital signature of the active firmware image before executing application code.

- **Verification method:** Test
- **Linked tests:** TC-FCC-040
- **Open item:** Re-test required after firmware v2.4.1 (see CR-FCC-241)

---

## Open certification risks (engineering note)

| Risk ID | Description | Potential schedule impact |
|---------|-------------|---------------------------|
| RISK-CERT-07 | SW-REQ-1042 regression not re-run after firmware v2.4.1 | **May delay flight test readiness** |
| RISK-CERT-11 | Trace gap: SW-REQ-1060 ↔ TC-FCC-040 evidence stale post-CR | Audit finding likely |
| RISK-CERT-14 | HAZ-FCC-003 mitigation review pending after fusion algorithm change | Safety board hold possible |

**Engineering lead note:** Unresolved items RISK-CERT-07 and RISK-CERT-14 are on the critical path for **flight testing gate FT-GATE-3** scheduled for Q3.
