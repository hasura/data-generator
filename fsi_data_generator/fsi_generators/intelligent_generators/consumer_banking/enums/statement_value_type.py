from enum import auto
from fsi_data_generator.fsi_generators.helpers import BaseEnum


class StatementValueType(BaseEnum):
    """Types of statement values."""
    LOYALTY_POINTS = auto()
    REWARD_BALANCE = auto()
    CASH_BACK_EARNED = auto()
    POINTS_EARNED = auto()
    POINTS_REDEEMED = auto()
    TIER_LEVEL = auto()
    CREDIT_SCORE = auto()
    CARBON_FOOTPRINT = auto()
    SPENDING_CATEGORY = auto()
    MILES_EARNED = auto()
    MILES_BALANCE = auto()
    MERCHANT_CATEGORY = auto()
    NEXT_TIER_PROGRESS = auto()
    ANNUAL_REWARDS_SUMMARY = auto()
    ANNUAL_SPENDING_SUMMARY = auto()
    OTHER = auto()

    # Default weights for random selection
    _DEFAULT_WEIGHTS = [
        15.0,  # LOYALTY_POINTS
        15.0,  # REWARD_BALANCE
        12.0,  # CASH_BACK_EARNED
        12.0,  # POINTS_EARNED
        10.0,  # POINTS_REDEEMED
        5.0,  # TIER_LEVEL
        5.0,  # CREDIT_SCORE
        2.0,  # CARBON_FOOTPRINT
        5.0,  # SPENDING_CATEGORY
        8.0,  # MILES_EARNED
        8.0,  # MILES_BALANCE
        5.0,  # MERCHANT_CATEGORY
        3.0,  # NEXT_TIER_PROGRESS
        5.0,  # ANNUAL_REWARDS_SUMMARY
        5.0,  # ANNUAL_SPENDING_SUMMARY
        2.0  # OTHER
    ]
