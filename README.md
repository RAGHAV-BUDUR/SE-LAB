# Software Engineering Laboratory (SE-LAB)

**Student Name:** Raghav Budur  
**SRN:** PES1UG23AM225  
**Course:** Software Engineering Lab (SE Lab)  
**Institution:** PES University  

---

## Repository Index & Lab Overview

| Lab Module | Topic | Artifacts & Documentation | Status |
|---|---|---|---|
| **Lab 1** | Requirement Engineering & Modeling | [SELAB1.pdf](SELAB1.pdf) | Complete |
| **Lab 2** | Architecture & Design Modeling | [SELAB2.pdf](SELAB2.pdf) | Complete |
| **Lab 3** | Component & Deployment Diagrams | [SELAB3.pdf](SELAB3.pdf) | Complete |
| **Lab 4** | Autonomous Game Refactoring | [SELAB4/](SELAB4/) (Frogger) | Complete |
| **Lab 5** | Static Code Analysis & Remediation | [SELAB5/](SELAB5/) | [Lab 5 PDF Report](SELAB5/Lab5_Static_Code_Analysis_Report.pdf) | Complete (10.00/10 Pylint, 0 Bandit, 0 Flake8) |
| **Lab 6** | Code & Branch Coverage Analysis | [SELAB6/](SELAB6/) | [Lab 6 PDF Report](SELAB6/Lab6_Code_and_Branch_Coverage_Report.pdf) | Complete (100% Line, 100% Branch Coverage) |

---

## Lab 5 — Static Code Analysis
- **Assigned Module:** `library_system.py`
- **Pylint Score:** **10.00 / 10** (improved from 6.07/10)
- **Bandit Security Issues:** **0 issues** (resolved eval CWE-78/95 and try-except-pass)
- **Flake8 Violations:** **0 violations** (100% PEP 8 compliant)
- **Automated Tests:** 8/8 tests passing in `test_library_system.py`
- **Full Report:** [Lab 5 Report (PDF)](SELAB5/Lab5_Static_Code_Analysis_Report.pdf)

## Lab 6 — Code and Branch Coverage
- **Assigned Module:** `water_utility_billing.py`
- **Line / Code Coverage:** **100%** (increased from baseline 46%)
- **Branch Coverage:** **100%** (increased from baseline 41%)
- **Test Suites:**
  - `CodeCoverageTest_01_water_utility.py` (14 tests)
  - `BranchCoverageTest_01_water_utility.py` (26 tests)
- **Terminal Evidence:** Screenshots in `SELAB6/reports/lab6/screenshots/`
- **Full Report:** [Lab 6 Report (PDF)](SELAB6/Lab6_Code_and_Branch_Coverage_Report.pdf)
