# Lab 5: Static Code Analysis — Issue Documentation

**Repository:** `SETAPESU26/L5_01_library_fines`  
**Student:** Raghav Budur (`PES1UG23AM225`)  
**Target Script:** `library_system.py`  
**Baseline Score:** Pylint 6.07/10 | Bandit: 2 issues (1 Med, 1 Low) | Flake8: 14 violations  
**Final Score:** Pylint **10.00/10** | Bandit: **0 issues** | Flake8: **0 violations**

---

## Documented Issues Table

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| **eval() Arbitrary Code Execution (B307 / W0123)** | Security Vulnerability (High / Medium) | 45 | Function `fine_from_rule` used built-in `eval()` to evaluate arithmetic strings, allowing Remote Code Execution (RCE) and arbitrary code injection (CWE-78/95). | Replaced `eval()` with a secure AST recursive evaluator (`_eval_ast_node`) that explicitly whitelists only math operators, numeric constants, and the bounded variable `days`. |
| **Mutable Default Argument (W0102)** | Bug / Logic Flaw (Medium) | 9 | Function `add_book_loan` defined mutable default `dates=[]`. Because Python evaluates defaults once at definition time, loan dates were shared and accumulated across different students. | Changed default parameter to `dates=None` and initialized `if dates is None: dates = []` inside the function body so every call gets a fresh list instance. |
| **Silent Exception Suppression (B110 / W0702 / E722)** | Security & Error Handling (Medium / Low) | 21 | Bare `except: pass` in `return_book` silently swallowed all errors and interrupts (`KeyboardInterrupt`, `SystemExit`), masking application bugs. | Removed bare try/except and replaced with explicit dictionary checks (`if student_id not in loans` and `if book_id in ...`), returning boolean success status. |
| **Global State Mutation Corrupting Rates (W0603)** | Code Smell / Bug (Medium / Low) | 28, 35 | `renewBook` mutated `global FINE_PER_DAY = FINE_PER_DAY + 1`, permanently corrupting the daily fine rate for all future calculations. `load_records` used `global loans`. | Removed global mutation in `renew_book` so penalty is local to the calculation; refactored `load_records` to mutate in-place via `loans.clear()` and `loans.update()`. |
| **Missing Context Manager & Encoding (R1732 / W1514)** | Resource Management (Low) | 34, 40 | File operations `open(file, "r")` and `open(file, "w")` without context managers risk leaving file descriptors open on exceptions, and lacked explicit UTF-8 encoding. | Refactored both `load_records` and `save_records` to use `with open(file, mode, encoding="utf-8") as f:` context managers for deterministic cleanup. |
| **Non-PEP 8 Naming Convention (C0103)** | Style / Convention (Low) | 27 | Function name `renewBook` used camelCase, violating PEP 8 snake_case standards. | Renamed function to `renew_book` strictly adhering to PEP 8 snake_case convention. |
| **Missing Module & Function Docstrings (C0114 / C0116)** | Documentation Standard (Low) | 1, 9, 16, 24, 27, 33, 39, 44, 47, 52 | Module and top-level functions completely lacked docstrings describing purpose, arguments, and return types. | Added comprehensive module-level docstring and PEP 257 compliant docstrings for every function. |
| **PEP 8 Formatting Violations (E501 / E302 / E305)** | PEP 8 Formatting (Low) | Multiple | Missing two blank lines between top-level functions, lines exceeding 79 characters, and outdated `%` string formatting. | Added required blank lines, split long lines under 79 characters, and upgraded to modern Python f-strings. |

---

## Detailed Tool & Verification Breakdown

| # | Tool | Issue Code | Severity | Original Line | Problem Summary | Remediation Details | Verification Status |
|---|------|------------|----------|---------------|-----------------|---------------------|---------------------|
| 1 | Bandit / Pylint | B307 / W0123 | Medium | Line 45 | `eval()` usage in fine rule calculation | Safe AST arithmetic recursion evaluator | **Verified**: Bandit B307 & Pylint W0123 eliminated. Untrusted input rejected. |
| 2 | Pylint | W0102 | Medium | Line 9 | Mutable default list `dates=[]` | Default `dates=None`, dynamic initialization | **Verified**: No state leakage across students. Pylint W0102 resolved. |
| 3 | Bandit / Pylint / Flake8 | B110 / W0702 / E722 | Med/Low | Line 21 | Bare `except: pass` suppressing all errors | Explicit conditional membership checking | **Verified**: B110, W0702, E722 resolved; returns boolean. |
| 4 | Pylint | W0603 | Low | Lines 28, 35 | `global FINE_PER_DAY` rate corruption | Removed global mutation; in-place dict update | **Verified**: Rate preserved at 2/day; Pylint W0603 resolved. |
| 5 | Pylint | R1732 / W1514 | Low | Lines 34, 40 | File handle leak & unspecified encoding | `with open(..., encoding="utf-8")` | **Verified**: Deterministic file closing; R1732 & W1514 resolved. |
| 6 | Pylint | C0103 | Low | Line 27 | camelCase `renewBook` naming violation | Renamed to PEP 8 `renew_book` | **Verified**: Pylint C0103 resolved. |
| 7 | Pylint | C0114 / C0116 | Low | Throughout | Missing module and function docstrings | Added PEP 257 compliant docstrings | **Verified**: Pylint C0114 & C0116 resolved across file. |
| 8 | Flake8 | E501 / E302 / E305 | Low | Throughout | Line length > 79, blank lines, `%` formatting | Wrapped lines, 2 blank lines, f-strings | **Verified**: Flake8 reports 0 violations; exit code 0. |
