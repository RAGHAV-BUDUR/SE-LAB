# Lab 5: Static Code Analysis — Reflection and Technical Review

**Student:** Raghav Budur (`PES1UG23AM225`)  
**Course:** Software Engineering Lab (SE Lab)  
**Topic:** Static Code Analysis (Pylint, Bandit, Flake8)

---

## 1. Reflection on Static Code Analysis Tools

### Question 1: What distinct roles do Pylint, Bandit, and Flake8 play in software development, and how do their findings complement each other?
- **Pylint (Code Quality & Logic Checker):** Pylint functions as a thorough, deep static reviewer. Beyond superficial formatting, it inspects Python ASTs to detect subtle programmatic bugs—such as mutable default parameters (`dates=[]`), variable shadowing, improper global state mutation, resource management leaks (missing `with` statements), and adherence to naming conventions. In `library_system.py`, Pylint immediately identified the dangerous accumulation of loan dates across function calls and the corruption of the global `FINE_PER_DAY` variable.
- **Bandit (Security Vulnerability Scanner):** Bandit acts as an automated application security inspector. It specifically targets security flaws and unsafe coding patterns mapped to Common Weakness Enumerations (CWEs). It flagged the critical use of `eval()` (`B307` / CWE-78/95), which exposed the library application to arbitrary code execution, and flagged bare `try/except/pass` blocks (`B110` / CWE-703) that suppress critical execution signals.
- **Flake8 (PEP 8 Style and Syntax Enforcement):** Flake8 combines `PyFlakes`, `pycodestyle`, and `McCabe` to enforce PEP 8 consistency. It focuses on syntactic clarity, indentation, blank lines, line lengths, and unused imports. While Pylint and Bandit focus on logic and security, Flake8 guarantees uniformity and readability across team codebases.
- **Complementary Synergy:** Together, the three tools form a comprehensive defense-in-depth static analysis pipeline: Flake8 guarantees readable syntax, Pylint ensures logical correctness and maintainability, and Bandit safeguards application security.

---

## 2. Technical Evaluation of Issues and Fixes

### Question 2: Why are mutable default arguments particularly dangerous in Python, and how does `None` idiom resolve it?
In Python, default parameter expressions are evaluated **once at function definition time**, not dynamically on each function call. When a mutable object like a list (`dates=[]`) is used as a default, every invocation that omits the parameter shares the **exact same in-memory object instance**. In `library_system.py`, every student loan appended timestamps to the shared default list, leading to severe state contamination across different student loans. Replacing the default with `None` and initializing `dates = []` inside the function body ensures a fresh, independent list instance is allocated for each invocation.

### Question 3: What security risks did `eval()` introduce in `fine_from_rule()`, and why is an AST-based parser the appropriate remediation?
Using `eval(rule.replace("days", str(days)))` allowed arbitrary Python expressions to execute with the privileges of the running process. An attacker or untrusted input could pass payloads such as `__import__('os').system('rm -rf /')` or read unauthorized system files. 
Replacing `eval()` with a recursive AST evaluator (`_eval_ast_node`) parses the mathematical expression into an Abstract Syntax Tree and explicitly whitelists only mathematical binary operators (`+`, `-`, `*`, `/`), numeric constants, and the bounded variable `days`. Any disallowed token, function call, attribute access, or statement immediately raises a `ValueError`, eliminating injection vulnerabilities without sacrificing the required rule calculation functionality.

---

## 3. Practical Software Engineering Insights

### Question 4: How does integrating static analysis into automated CI/CD pipelines impact software maintainability and team productivity?
1. **Early Defect Detection ("Shift-Left"):** Static analysis catches defects at authoring or pull-request time before code enters testing or production. This drastically decreases remediation costs.
2. **Automated Quality Gates:** Setting thresholds (e.g., minimum Pylint score of 9.5/10, zero high/medium Bandit findings, zero Flake8 errors) prevents technical debt from accumulating in mainline branches.
3. **Objective Code Reviews:** Automating style and trivial bug checks frees human code reviewers to focus on architectural decisions, algorithmic efficiency, and domain logic rather than arguing about whitespace or naming.
4. **Consistency Across Teams:** Standardized linters enforce architectural guidelines uniformly across distributed contributors.

---

## Summary of Results
- **Baseline:** Pylint: 6.07/10 | Bandit: 2 issues (1 Medium, 1 Low) | Flake8: 14 violations
- **Final:** Pylint: **10.00/10** | Bandit: **0 issues** | Flake8: **0 violations**
- **Test Suite:** 8 passing pytest unit tests verifying functionality and security boundaries.
