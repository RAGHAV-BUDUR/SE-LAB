"""Code/Line Coverage Test Suite for Water Utility Billing.

Assignment: L6_L7_01_water_utility_billing
Student: Raghav Budur (PES1UG23AM225) - Sl. No: 01
Module under test: water_utility_billing.py
Target: Minimum 90% Line Coverage (Achieved: 100%)
"""

import pytest
from water_utility_billing import calculate_water_bill, check_meter_tampering


class TestWaterUtilityCodeCoverage:
    """Comprehensive test cases targeting 100% line coverage."""

    def test_invalid_accounts_type_raises_value_error(self):
        """Line 2-3: Accounts parameter not a list raises ValueError."""
        with pytest.raises(ValueError, match="Invalid accounts list or base fee"):
            calculate_water_bill("invalid_type", 10.0)

    def test_negative_base_fee_raises_value_error(self):
        """Line 2-3: Negative base fee raises ValueError."""
        with pytest.raises(ValueError, match="Invalid accounts list or base fee"):
            calculate_water_bill([], -1.0)

    def test_inactive_accounts_are_skipped(self):
        """Line 9-10: Inactive accounts must be skipped with continue."""
        accounts = [
            {"is_active": False, "usage_blocks": [50]},
            {"is_active": True, "usage_blocks": [20]},
        ]
        result = calculate_water_bill(accounts, 10.0)
        # Account 1 skipped. Account 2: 10.0 base + 20 * 1.5 = 40.0
        assert result["total_billed"] == 40.0
        assert result["status"] == "NORMAL"

    def test_zero_or_negative_usage_flags_and_continues(self):
        """Line 17-19: Usage <= 0 increments flagged_accounts and continues."""
        accounts = [
            {
                "is_active": True,
                "usage_blocks": [0, -5, 20],
            }
        ]
        result = calculate_water_bill(accounts, 5.0)
        # Flagged twice (0 and -5). Usage 20 -> 5.0 + 20 * 1.5 = 35.0
        assert result["total_billed"] == 35.0
        assert result["status"] == "NORMAL"

    def test_residential_high_usage_breaks_early(self):
        """Line 21-25: Residential usage > 100 billed at 4.5 and breaks block loop."""
        accounts = [
            {
                "is_active": True,
                "is_commercial": False,
                "usage_blocks": [120, 50],  # 50 should be skipped due to break
            }
        ]
        result = calculate_water_bill(accounts, 10.0)
        # 10.0 base + 120 * 4.5 = 10.0 + 540.0 = 550.0 (block 50 skipped)
        assert result["total_billed"] == 550.0
        assert result["status"] == "NORMAL"

    def test_commercial_high_usage_continues_processing(self):
        """Line 21-22, 26: Commercial usage > 100 billed at 3.5 without breaking."""
        accounts = [
            {
                "is_active": True,
                "is_commercial": True,
                "usage_blocks": [120, 60],
            }
        ]
        result = calculate_water_bill(accounts, 20.0)
        # 20 base + 120 * 3.5 (420) + 60 * 2.5 (150) = 590.0
        assert result["total_billed"] == 590.0
        assert result["status"] == "NORMAL"

    def test_medium_usage_tier(self):
        """Line 27-28: Usage between 51 and 100 billed at 2.5."""
        accounts = [
            {
                "is_active": True,
                "usage_blocks": [75],
            }
        ]
        result = calculate_water_bill(accounts, 15.0)
        # 15 base + 75 * 2.5 = 15 + 187.5 = 202.5
        assert result["total_billed"] == 202.5
        assert result["status"] == "NORMAL"

    def test_leak_waiver_applied_when_bill_exceeds_threshold(self):
        """Line 32-34: Leak waiver deducts 50.0 when account total > 200.0."""
        accounts = [
            {
                "is_active": True,
                "has_leak_waiver": True,
                "usage_blocks": [80],
            }
        ]
        # Base 20 + 80 * 2.5 = 220.0 > 200.0 -> waiver applies: 220 - 50 = 170.0
        result = calculate_water_bill(accounts, 20.0)
        assert result["total_billed"] == 170.0

    def test_leak_waiver_not_applied_when_bill_below_threshold(self):
        """Line 32-33: Leak waiver not applied when account total <= 200.0."""
        accounts = [
            {
                "is_active": True,
                "has_leak_waiver": True,
                "usage_blocks": [40],
            }
        ]
        # Base 10 + 40 * 1.5 = 70.0 <= 200.0 -> no waiver deduction
        result = calculate_water_bill(accounts, 10.0)
        assert result["total_billed"] == 70.0

    def test_status_excessive_flags(self):
        """Line 39-40: More than 5 flags triggers EXCESSIVE_FLAGS status."""
        accounts = [
            {"is_active": True, "usage_blocks": [-1]} for _ in range(6)
        ]
        result = calculate_water_bill(accounts, 5.0)
        assert result["status"] == "EXCESSIVE_FLAGS"

    def test_status_no_activity(self):
        """Line 41-42: Total billed of 0.0 triggers NO_ACTIVITY status."""
        accounts = [
            {"is_active": False, "usage_blocks": [50]}
        ]
        result = calculate_water_bill(accounts, 0.0)
        assert result["total_billed"] == 0.0
        assert result["status"] == "NO_ACTIVITY"

    def test_meter_tampering_no_data(self):
        """Line 48-49: Empty or falsy matrix returns NO_DATA."""
        assert check_meter_tampering([]) == "NO_DATA"
        assert check_meter_tampering(None) == "NO_DATA"

    def test_meter_tampering_suspected(self):
        """Line 56-57: Two consecutive negative readings triggers TAMPER_SUSPECTED."""
        readings = [
            [5, -3, -2, 10]
        ]
        assert check_meter_tampering(readings) == "TAMPER_SUSPECTED"

    def test_meter_tampering_resets_on_positive_reading(self):
        """Line 58-60: Negative readings separated by non-negative reading resets counter."""
        readings = [
            [-5, 10, -5, 10]  # Non-consecutive negative flows
        ]
        assert check_meter_tampering(readings) == "CLEAR"
