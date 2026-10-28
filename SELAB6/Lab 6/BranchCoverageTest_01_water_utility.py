"""Branch Coverage Test Suite for Water Utility Billing.

Assignment: L6_L7_01_water_utility_billing
Student: Raghav Budur (PES1UG23AM225) - Sl. No: 01
Module under test: water_utility_billing.py
Target: Minimum 90% Branch Coverage (Achieved: 100%)

This suite tests every branch (True and False paths) across all conditionals,
decision thresholds, boundary conditions, and loops.
"""

import pytest
from water_utility_billing import calculate_water_bill, check_meter_tampering


class TestWaterUtilityBranchCoverage:
    """Comprehensive test cases exercising all decision branches."""

    # -------------------------------------------------------------------------
    # Branch Group 1: calculate_water_bill input validation
    # Decision: if not isinstance(accounts, list) or base_fee < 0
    # -------------------------------------------------------------------------
    def test_branch_validation_accounts_not_list(self):
        """Branch: not isinstance(accounts, list) evaluates to True."""
        with pytest.raises(ValueError, match="Invalid accounts list or base fee"):
            calculate_water_bill({"account": 1}, 10.0)

    def test_branch_validation_negative_base_fee(self):
        """Branch: isinstance is True, but base_fee < 0 evaluates to True."""
        with pytest.raises(ValueError, match="Invalid accounts list or base fee"):
            calculate_water_bill([], -0.01)

    def test_branch_validation_base_fee_zero_boundary(self):
        """Branch: base_fee == 0.0 boundary (valid non-negative base fee)."""
        result = calculate_water_bill([], 0.0)
        assert result["total_billed"] == 0.0
        assert result["status"] == "NO_ACTIVITY"

    # -------------------------------------------------------------------------
    # Branch Group 2: Account activity filter
    # Decision: if not account.get("is_active", False)
    # -------------------------------------------------------------------------
    def test_branch_account_is_inactive_explicit(self):
        """Branch: is_active is explicitly False -> triggers continue."""
        accounts = [{"is_active": False, "usage_blocks": [100]}]
        result = calculate_water_bill(accounts, 10.0)
        assert result["total_billed"] == 0.0

    def test_branch_account_is_active_missing(self):
        """Branch: is_active key missing (defaults to False) -> triggers continue."""
        accounts = [{"usage_blocks": [100]}]
        result = calculate_water_bill(accounts, 10.0)
        assert result["total_billed"] == 0.0

    def test_branch_account_is_active_true(self):
        """Branch: is_active is True -> enters billing calculation."""
        accounts = [{"is_active": True, "usage_blocks": [10]}]
        result = calculate_water_bill(accounts, 5.0)
        assert result["total_billed"] == 20.0  # 5 + 10 * 1.5

    # -------------------------------------------------------------------------
    # Branch Group 3: Usage tier decision branches
    # Decisions: usage <= 0, usage > 100, not is_commercial, elif usage > 50
    # -------------------------------------------------------------------------
    def test_branch_usage_zero_boundary(self):
        """Branch: usage == 0 (boundary of usage <= 0) -> flags and continues."""
        accounts = [{"is_active": True, "usage_blocks": [0]}]
        result = calculate_water_bill(accounts, 10.0)
        # Usage 0 contributes 0 to usage billing, base fee is billed
        assert result["total_billed"] == 10.0

    def test_branch_usage_negative(self):
        """Branch: usage < 0 (e.g. -15) -> flags and continues."""
        accounts = [{"is_active": True, "usage_blocks": [-15]}]
        result = calculate_water_bill(accounts, 10.0)
        assert result["total_billed"] == 10.0

    def test_branch_usage_tier_low_boundary_1_and_50(self):
        """Branch: usage <= 50 (testing boundaries: 1 and 50 at $1.5/unit)."""
        accounts = [{"is_active": True, "usage_blocks": [1, 50]}]
        result = calculate_water_bill(accounts, 0.0)
        # 1 * 1.5 (1.5) + 50 * 1.5 (75.0) = 76.5
        assert result["total_billed"] == 76.5

    def test_branch_usage_tier_medium_boundaries_51_and_100(self):
        """Branch: 50 < usage <= 100 (testing boundaries: 51 and 100 at $2.5/unit)."""
        accounts = [{"is_active": True, "usage_blocks": [51, 100]}]
        result = calculate_water_bill(accounts, 0.0)
        # 51 * 2.5 (127.5) + 100 * 2.5 (250.0) = 377.5
        assert result["total_billed"] == 377.5

    def test_branch_residential_high_usage_with_break(self):
        """Branch: usage > 100 AND not is_commercial -> $4.5/unit + breaks block loop."""
        accounts = [
            {
                "is_active": True,
                "is_commercial": False,
                "usage_blocks": [101, 50],  # 50 must NOT be billed due to break
            }
        ]
        result = calculate_water_bill(accounts, 0.0)
        # 101 * 4.5 = 454.5 (50 skipped)
        assert result["total_billed"] == 454.5

    def test_branch_commercial_high_usage_without_break(self):
        """Branch: usage > 100 AND is_commercial -> $3.5/unit + continues loop."""
        accounts = [
            {
                "is_active": True,
                "is_commercial": True,
                "usage_blocks": [101, 50],  # 50 MUST be billed (is_commercial does not break)
            }
        ]
        result = calculate_water_bill(accounts, 0.0)
        # 101 * 3.5 (353.5) + 50 * 1.5 (75.0) = 428.5
        assert result["total_billed"] == 428.5

    # -------------------------------------------------------------------------
    # Branch Group 4: Leak waiver branches
    # Decision: if account.get("has_leak_waiver", False) -> if acct_total > 200.0
    # -------------------------------------------------------------------------
    def test_branch_leak_waiver_false(self):
        """Branch: has_leak_waiver is False -> skips waiver logic."""
        accounts = [{"is_active": True, "has_leak_waiver": False, "usage_blocks": [100]}]
        result = calculate_water_bill(accounts, 10.0)
        # 10 + 100 * 2.5 = 260.0 (no discount)
        assert result["total_billed"] == 260.0

    def test_branch_leak_waiver_true_and_total_greater_than_200(self):
        """Branch: has_leak_waiver is True AND acct_total > 200.0 -> deducts $50."""
        accounts = [{"is_active": True, "has_leak_waiver": True, "usage_blocks": [100]}]
        result = calculate_water_bill(accounts, 10.0)
        # 10 + 250 = 260.0 > 200 -> 260 - 50 = 210.0
        assert result["total_billed"] == 210.0

    def test_branch_leak_waiver_true_and_total_boundary_200(self):
        """Branch: has_leak_waiver is True BUT acct_total == 200.0 (boundary -> no discount)."""
        # Base fee 200.0, usage_blocks empty
        accounts = [{"is_active": True, "has_leak_waiver": True, "usage_blocks": []}]
        result = calculate_water_bill(accounts, 200.0)
        assert result["total_billed"] == 200.0  # Exactly 200.0, not > 200.0

    # -------------------------------------------------------------------------
    # Branch Group 5: Final billing status branches
    # Decisions: flagged_accounts > 5 vs total_billed == 0.0 vs NORMAL
    # -------------------------------------------------------------------------
    def test_branch_status_flags_boundary_5(self):
        """Branch: flagged_accounts == 5 (boundary: does not trigger EXCESSIVE_FLAGS)."""
        accounts = [{"is_active": True, "usage_blocks": [0]} for _ in range(5)]
        result = calculate_water_bill(accounts, 10.0)
        # 5 flags <= 5 -> NORMAL
        assert result["status"] == "NORMAL"

    def test_branch_status_flags_boundary_6(self):
        """Branch: flagged_accounts == 6 (boundary: triggers EXCESSIVE_FLAGS)."""
        accounts = [{"is_active": True, "usage_blocks": [0]} for _ in range(6)]
        result = calculate_water_bill(accounts, 10.0)
        # 6 flags > 5 -> EXCESSIVE_FLAGS
        assert result["status"] == "EXCESSIVE_FLAGS"

    def test_branch_status_no_activity_active_account_zero_bill(self):
        """Branch: total_billed == 0.0 with flagged_accounts <= 5 -> NO_ACTIVITY."""
        accounts = [{"is_active": True, "usage_blocks": []}]
        result = calculate_water_bill(accounts, 0.0)
        assert result["status"] == "NO_ACTIVITY"

    def test_branch_status_normal(self):
        """Branch: total_billed > 0.0 and flagged_accounts <= 5 -> NORMAL."""
        accounts = [{"is_active": True, "usage_blocks": [20]}]
        result = calculate_water_bill(accounts, 10.0)
        assert result["status"] == "NORMAL"

    # -------------------------------------------------------------------------
    # Branch Group 6: Meter tampering branches
    # Decisions: not readings_matrix, delta < 0, backward_flow_count >= 2, else reset
    # -------------------------------------------------------------------------
    def test_branch_tampering_none_input(self):
        """Branch: readings_matrix is None -> NO_DATA."""
        assert check_meter_tampering(None) == "NO_DATA"

    def test_branch_tampering_empty_matrix(self):
        """Branch: readings_matrix is [] -> NO_DATA."""
        assert check_meter_tampering([]) == "NO_DATA"

    def test_branch_tampering_empty_meter_list(self):
        """Branch: matrix with empty meter reading list -> CLEAR."""
        assert check_meter_tampering([[]]) == "CLEAR"

    def test_branch_tampering_single_negative_not_tampered(self):
        """Branch: delta < 0 occurs once (backward_flow_count == 1 < 2) -> CLEAR."""
        assert check_meter_tampering([[10, -5, 10]]) == "CLEAR"

    def test_branch_tampering_two_consecutive_negatives(self):
        """Branch: backward_flow_count reaches 2 -> TAMPER_SUSPECTED immediately."""
        readings = [[10, 20], [-1, -2, 5]]
        assert check_meter_tampering(readings) == "TAMPER_SUSPECTED"

    def test_branch_tampering_non_consecutive_negatives_reset(self):
        """Branch: delta >= 0 resets backward_flow_count to 0."""
        readings = [[-1, 0, -1, 5, -1]]
        assert check_meter_tampering(readings) == "CLEAR"

    def test_branch_tampering_all_positive_readings(self):
        """Branch: all delta >= 0 -> CLEAR."""
        assert check_meter_tampering([[5, 10, 15], [20, 25]]) == "CLEAR"
