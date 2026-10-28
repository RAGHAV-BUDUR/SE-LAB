# Software Engineering Laboratory (SE Lab) — Submission Package

**Student Name:** Raghav Budur  
**SRN:** `PES1UG23AM225`  
**Roll / Sl. No:** 01  
**GitHub Portfolio:** [https://github.com/RAGHAV-BUDUR/SE-LAB](https://github.com/RAGHAV-BUDUR/SE-LAB)  
**Assigned Repositories:**
- **Lab 5 (Static Analysis):** `SETAPESU26/L5_01_library_fines`
- **Lab 6 (Coverage Analysis):** `SETAPESU26/L6_L7_01_water_utility_billing`

---

## 1. Lab 5 — Static Code Analysis Summary

### Objective
Audit and remediate quality defects, security vulnerabilities, and PEP 8 style issues in `library_system.py`.

### Results & Metrics
- **Pylint Score:** Improved from **6.07/10** to **10.00/10** (100% clean).
- **Bandit Security:** Reduced from **2 issues** (Medium severity `eval()` B307 and Low severity `try-except-pass` B110) to **0 issues** (zero security findings).
- **Flake8 Violations:** Reduced from **14 violations** to **0 violations** (clean exit code 0).
- **Automated Tests:** 8/8 unit tests passing in `test_library_system.py`.

### Git Commits (Lab 5)
1. `d5a135a` — `fix(lab5): resolve pylint code quality issues`
2. `c1ed769` — `fix(lab5): address bandit security findings`
3. `e7eedab` — `fix(lab5): resolve flake8 formatting violations`

### Deliverables
- PDF Report: [`Lab5_Static_Code_Analysis_Report.pdf`](file:///c:/Users/Lenovo/Desktop/SELAB/SELAB5/submission/lab5/Lab5_Static_Code_Analysis_Report.pdf)
- Issue Documentation: [`lab5_issue_table.md`](file:///c:/Users/Lenovo/Desktop/SELAB/SELAB5/submission/lab5/lab5_issue_table.md)
- Technical Reflection: [`lab5_reflection.md`](file:///c:/Users/Lenovo/Desktop/SELAB/SELAB5/submission/lab5/lab5_reflection.md)
- Tool Reports: `submission/lab5/before/` and `submission/lab5/after/`

---

## 2. Lab 6 — Code and Branch Coverage Analysis Summary

### Objective
Design and implement targeted white-box test suites achieving minimum 90% (achieved 100%) line coverage and branch coverage on `water_utility_billing.py`.

### Results & Metrics
- **Line / Code Coverage:** Increased from **46% (25 missing stmts)** to **100% (46/46 statements covered)**.
- **Branch Coverage:** Increased from **41% (34 missing/partial branches)** to **100% (34/34 branches covered)**.
- **Test Suites:**
  - `CodeCoverageTest_01_water_utility.py`: 14 test cases covering every statement.
  - `BranchCoverageTest_01_water_utility.py`: 26 test cases covering all conditional branches, boolean combinations, and boundary values.
  - Total: 40 tests passing at 100%.

### Git Commits (Lab 6)
1. `7e228e6` — `test(lab6): add code coverage test cases`
2. `9ee504b` — `test(lab6): add branch coverage test cases`

### Deliverables
- PDF Report: [`Lab6_Code_and_Branch_Coverage_Report.pdf`](file:///c:/Users/Lenovo/Desktop/SELAB/SELAB6/submission/lab6/Lab6_Code_and_Branch_Coverage_Report.pdf)
- Terminal Screenshots:
  - Code Coverage: `submission/lab6/screenshots/code_coverage.png`
  - Branch Coverage: `submission/lab6/screenshots/branch_coverage.png`
- Coverage Reports: `submission/lab6/coverage_reports/`

---

## 3. Directory Layout

```text
submission/
├── lab5/
│   ├── Lab5_Static_Code_Analysis_Report.pdf
│   ├── lab5_issue_table.md
│   ├── lab5_reflection.md
│   ├── before/
│   │   ├── pylint_report.txt
│   │   ├── bandit_report.txt
│   │   └── flake8_report.txt
│   └── after/
│       ├── pylint_report.txt
│       ├── bandit_report.txt
│       └── flake8_report.txt
├── lab6/
│   ├── Lab6_Code_and_Branch_Coverage_Report.pdf
│   ├── CodeCoverageTest_01_water_utility.py
│   ├── BranchCoverageTest_01_water_utility.py
│   ├── screenshots/
│   │   ├── code_coverage.png
│   │   └── branch_coverage.png
│   └── coverage_reports/
│       ├── code_coverage_report.txt
│       └── branch_coverage_report.txt
└── README.md
```
