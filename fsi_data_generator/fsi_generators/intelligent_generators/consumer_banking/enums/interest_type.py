from ....helpers import BaseEnum
from enum import auto


class InterestType(BaseEnum):
    """Types of interest on account statements."""
    DEPOSIT = auto()
    SAVINGS = auto()
    CERTIFICATE = auto()
    MONEY_MARKET = auto()
    CHECKING = auto()
    BONUS = auto()
    PROMOTIONAL = auto()
    PENALTY = auto()
    LOAN = auto()
    CREDIT_CARD = auto()
    OVERDRAFT = auto()
    LINE_OF_CREDIT = auto()
    ADJUSTMENT = auto()
    OTHER = auto()

    # Default weights for random selection
    _DEFAULT_WEIGHTS = [
        25.0,  # DEPOSIT
        20.0,  # SAVINGS
        10.0,  # CERTIFICATE
        8.0,  # MONEY_MARKET
        5.0,  # CHECKING
        5.0,  # BONUS
        5.0,  # PROMOTIONAL
        3.0,  # PENALTY
        5.0,  # LOAN
        5.0,  # CREDIT_CARD
        3.0,  # OVERDRAFT
        3.0,  # LINE_OF_CREDIT
        2.0,  # ADJUSTMENT
        1.0  # OTHER
    ]
