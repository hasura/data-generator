from ....helpers import BaseEnum
from enum import auto


class StandingOrderStatusCode(BaseEnum):
    """Status codes for standing orders."""
    ACTIVE = auto()
    PENDING = auto()
    CANCELLED = auto()
    SUSPENDED = auto()
    COMPLETED = auto()
    FAILED = auto()
    ON_HOLD = auto()
    EXPIRED = auto()
    OTHER = auto()

    # Default weights for random selection
    _DEFAULT_WEIGHTS = [
        70.0,  # ACTIVE
        10.0,  # PENDING
        5.0,  # CANCELLED
        5.0,  # SUSPENDED
        3.0,  # COMPLETED
        3.0,  # FAILED
        2.0,  # ON_HOLD
        1.5,  # EXPIRED
        0.5  # OTHER
    ]


class StandingOrderType(BaseEnum):
    """Types of standing orders."""
    FIXED_AMOUNT = auto()
    VARIABLE_AMOUNT = auto()
    BALANCE_SWEEP = auto()
    FULL_BALANCE = auto()
    PERCENTAGE = auto()
    INTEREST_ONLY = auto()
    OTHER = auto()

    # Default weights for random selection
    _DEFAULT_WEIGHTS = [
        75.0,  # FIXED_AMOUNT
        10.0,  # VARIABLE_AMOUNT
        5.0,  # BALANCE_SWEEP
        3.0,  # FULL_BALANCE
        3.0,  # PERCENTAGE
        2.0,  # INTEREST_ONLY
        2.0  # OTHER
    ]


class StandingOrderCategory(BaseEnum):
    """Categories or purposes of standing orders."""
    BILL_PAYMENT = auto()
    SAVINGS = auto()
    INVESTMENT = auto()
    LOAN_PAYMENT = auto()
    SUBSCRIPTION = auto()
    CHARITY = auto()
    FAMILY_SUPPORT = auto()
    RENT = auto()
    BUSINESS_EXPENSE = auto()
    OTHER = auto()

    # Default weights for random selection
    _DEFAULT_WEIGHTS = [
        25.0,  # BILL_PAYMENT
        20.0,  # SAVINGS
        10.0,  # INVESTMENT
        15.0,  # LOAN_PAYMENT
        10.0,  # SUBSCRIPTION
        5.0,  # CHARITY
        5.0,  # FAMILY_SUPPORT
        7.0,  # RENT
        2.0,  # BUSINESS_EXPENSE
        1.0  # OTHER
    ]
