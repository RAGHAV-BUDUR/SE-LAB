"""Library Fine and Book Renewal System module.

Provides functionality to track student book loans, manage renewals,
calculate overdue fines, and persist loan records.
"""

import ast
import json
import operator
from datetime import datetime

# Global state
loans = {}
FINE_PER_DAY = 2

# Allowed arithmetic operators for safe expression evaluation
_SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def _eval_ast_node(node, variables):
    """Recursively evaluate an AST node containing simple arithmetic."""
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.Name) and node.id in variables:
        return variables[node.id]
    if isinstance(node, ast.BinOp) and type(node.op) in _SAFE_OPERATORS:
        left = _eval_ast_node(node.left, variables)
        right = _eval_ast_node(node.right, variables)
        return _SAFE_OPERATORS[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return -_eval_ast_node(node.operand, variables)
    raise ValueError(
        f"Unsafe or unsupported token in expression: {ast.dump(node)}"
    )


def add_book_loan(student_id, book_id, dates=None):
    """Record a book loan for a student with timestamps."""
    if not student_id:
        return
    if dates is None:
        dates = []
    dates.append(str(datetime.now()))
    loans[student_id] = loans.get(student_id, []) + [book_id]
    print(
        f"{student_id} borrowed {book_id} (loan dates on record: {len(dates)})"
    )


def return_book(student_id, book_id):
    """Process a returned book and update student loan records safely."""
    if student_id not in loans:
        return False
    student_loans = loans[student_id]
    if book_id in student_loans:
        student_loans.remove(book_id)
        if len(student_loans) == 0:
            del loans[student_id]
        return True
    return False


def calculate_fine(days_overdue):
    """Calculate overdue fine based on days overdue and daily rate."""
    return max(0, days_overdue * FINE_PER_DAY)


def renew_book(student_id, book_id, extra_days):
    """Renew a book loan for a student for the specified extra days."""
    penalty_rate = FINE_PER_DAY + 1 if extra_days > 14 else FINE_PER_DAY
    print(
        f"Renewed {book_id} for {student_id} by {extra_days} days "
        f"(rate: {penalty_rate}/day)"
    )


def load_records(file="loans.json"):
    """Load loan records from a JSON file into the loans registry."""
    with open(file, "r", encoding="utf-8") as f:
        data = json.loads(f.read())
        loans.clear()
        loans.update(data)


def save_records(file="loans.json"):
    """Persist current loan records into a JSON file."""
    with open(file, "w", encoding="utf-8") as f:
        f.write(json.dumps(loans))


def fine_from_rule(rule, days):
    """Safely calculate fine from an arithmetic rule string without eval."""
    parsed = ast.parse(rule, mode="eval")
    return int(_eval_ast_node(parsed.body, {"days": days}))


def print_report():
    """Display the summary report of all active student book loans."""
    print("Loan Report")
    for student, book_list in loans.items():
        print(student, "->", book_list)


def main():
    """Main execution flow demonstrating library system operations."""
    add_book_loan("S101", "B-ALGO")
    add_book_loan("S102", "B-NETW")
    add_book_loan("", "B-DBMS")
    add_book_loan("S103", "4521")
    return_book("S999", "B-NONE")
    renew_book("S101", "B-ALGO", 21)
    print("Fine for 5 days:", calculate_fine(5))
    print("Fine for -3 days:", calculate_fine(-3))
    print("Fine via rule:", fine_from_rule("days * 2 + 10", 4))
    days = input("Days overdue for S102 (press Enter for 0): ") or "0"
    print("S102 owes:", calculate_fine(int(days)))
    save_records()
    load_records()
    print_report()


if __name__ == "__main__":
    main()
