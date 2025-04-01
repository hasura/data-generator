from ....helpers import BaseEnum
from enum import auto


class BenefitType(BaseEnum):
    """Types of statement benefits."""
    CASHBACK = auto()
    POINTS = auto()
    MILES = auto()
    INTEREST = auto()
    DISCOUNT = auto()
    INSURANCE = auto()
    FEE_WAIVER = auto()
    PROMOTIONAL = auto()
    LOYALTY = auto()
    REFERRAL = auto()
    ANNIVERSARY = auto()
    OTHER = auto()

    # Default weights for random selection
    _DEFAULT_WEIGHTS = [
        25.0,  # CASHBACK
        20.0,  # POINTS
        15.0,  # MILES
        10.0,  # INTEREST
        8.0,  # DISCOUNT
        5.0,  # INSURANCE
        5.0,  # FEE_WAIVER
        5.0,  # PROMOTIONAL
        3.0,  # LOYALTY
        2.0,  # REFERRAL
        1.0,  # ANNIVERSARY
        1.0  # OTHER
    ]
