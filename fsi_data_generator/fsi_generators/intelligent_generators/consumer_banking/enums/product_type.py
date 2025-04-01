from ....helpers import BaseEnum
from enum import auto


class ProductType(BaseEnum):
    """Types of consumer banking products."""
    CHECKING = auto()
    SAVINGS = auto()
    MONEY_MARKET = auto()
    CERTIFICATE_OF_DEPOSIT = auto()
    IRA = auto()
    HSA = auto()
    STUDENT = auto()
    YOUTH = auto()
    SENIOR = auto()
    BUSINESS_CHECKING = auto()
    BUSINESS_SAVINGS = auto()
    PREMIUM = auto()
    FOREIGN_CURRENCY = auto()
    SPECIALIZED = auto()

    # Default weights for random selection
    _DEFAULT_WEIGHTS = [
        30.0,  # CHECKING
        25.0,  # SAVINGS
        10.0,  # MONEY_MARKET
        10.0,  # CERTIFICATE_OF_DEPOSIT
        5.0,  # IRA
        3.0,  # HSA
        5.0,  # STUDENT
        3.0,  # YOUTH
        5.0,  # SENIOR
        7.0,  # BUSINESS_CHECKING
        5.0,  # BUSINESS_SAVINGS
        5.0,  # PREMIUM
        2.0,  # FOREIGN_CURRENCY
        5.0  # SPECIALIZED
    ]
