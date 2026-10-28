"""Unit tests for library_system module ensuring regression-free fixes."""

import os
import pytest
from library_system import (
    loans,
    add_book_loan,
    return_book,
    calculate_fine,
    renew_book,
    load_records,
    save_records,
    fine_from_rule,
    print_report,
)


@pytest.fixture(autouse=True)
def reset_loans():
    """Reset the global loans dictionary before and after each test."""
    loans.clear()
    yield
    loans.clear()


def test_add_book_loan():
    """Verify add_book_loan correctly adds books and does not share mutable defaults."""
    add_book_loan("S101", "B-ALGO")
    assert "S101" in loans
    assert loans["S101"] == ["B-ALGO"]

    # Verify second student does not share default dates
    add_book_loan("S102", "B-NETW")
    assert loans["S102"] == ["B-NETW"]

    # Empty student ID should be ignored
    add_book_loan("", "B-DBMS")
    assert "" not in loans


def test_return_book():
    """Verify book return logic including removal and cleanup."""
    add_book_loan("S101", "B-ALGO")
    add_book_loan("S101", "B-DATA")

    # Returning one book
    assert return_book("S101", "B-ALGO") is True
    assert loans["S101"] == ["B-DATA"]

    # Returning the last book removes student entry
    assert return_book("S101", "B-DATA") is True
    assert "S101" not in loans

    # Non-existent student or book returns False safely without error
    assert return_book("S999", "B-NONE") is False
    add_book_loan("S102", "B-NETW")
    assert return_book("S102", "B-MISSING") is False


def test_calculate_fine():
    """Verify fine calculation for positive, zero, and negative overdue days."""
    assert calculate_fine(5) == 10
    assert calculate_fine(0) == 0
    assert calculate_fine(-3) == 0


def test_renew_book(capsys):
    """Verify renewal output and standard vs extended renewal rates."""
    renew_book("S101", "B-ALGO", 7)
    captured = capsys.readouterr()
    assert "Renewed B-ALGO for S101 by 7 days" in captured.out
    assert "rate: 2/day" in captured.out

    renew_book("S101", "B-ALGO", 21)
    captured = capsys.readouterr()
    assert "Renewed B-ALGO for S101 by 21 days" in captured.out
    assert "rate: 3/day" in captured.out


def test_save_and_load_records(tmp_path):
    """Verify JSON file persistence using context managers."""
    test_file = str(tmp_path / "test_loans.json")
    add_book_loan("S101", "B-ALGO")
    save_records(test_file)

    assert os.path.exists(test_file)
    loans.clear()
    assert len(loans) == 0

    load_records(test_file)
    assert loans == {"S101": ["B-ALGO"]}


def test_fine_from_rule_safe_evaluation():
    """Verify safe AST evaluation of arithmetic rules."""
    assert fine_from_rule("days * 2 + 10", 4) == 18
    assert fine_from_rule("days * 3", 5) == 15
    assert fine_from_rule("days - 2", 10) == 8


def test_fine_from_rule_unsafe_rejection():
    """Verify rejection of unsafe expressions and unauthorized calls."""
    with pytest.raises(ValueError):
        fine_from_rule("__import__('os').system('dir')", 5)


def test_print_report(capsys):
    """Verify report formatting."""
    add_book_loan("S101", "B-ALGO")
    print_report()
    captured = capsys.readouterr()
    assert "Loan Report" in captured.out
    assert "S101 -> ['B-ALGO']" in captured.out
