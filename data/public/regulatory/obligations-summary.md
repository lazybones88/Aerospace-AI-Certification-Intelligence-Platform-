# Regulatory Obligations Summary (Demo Paraphrases)

> **Disclaimer:** These are **short educational paraphrases** for platform testing.  
> They are **not** substitutes for official DO-178C, ARP4754A, or FAA/EASA publications.  
> Always use authority-approved standard editions for certification work.

---

## DO-178C — Software verification (Table A-7, paraphrased)

**Objective A-7 (demo label):** Verify that the outputs of the software verification process comply with software verification standards and cover all high-level requirements.

**Expected evidence types:** Test procedures, test results, reviews, coverage analysis.

**DAP-100 applicability:** All Level A FCC software requirements (SW-REQ-1042, SW-REQ-1055, SW-REQ-1060).

---

## ARP4754A — Safety assessment process (Section 5.2, paraphrased)

Development assurance activities shall be consistent with the assigned DAL. Safety assessments must be updated when design changes affect hazard mitigations.

**DAP-100 note:** HAZ-FCC-003 mitigation review is required after fusion algorithm change.

---

## Cross-framework link (demo)

| Engineering activity | Framework |
|---------------------|-----------|
| Re-run TC-FCC-020 on new build | DO-178C A-7 |
| Re-approve HAZ-FCC-003 mitigation | ARP4754A safety process |
