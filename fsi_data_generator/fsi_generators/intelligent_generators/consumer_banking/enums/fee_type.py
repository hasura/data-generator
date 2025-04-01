from ....helpers import BaseEnum
from enum import auto


class FeeType(BaseEnum):
    """Types of statement fees."""
    SERVICE = auto()
    TRANSACTION = auto()
    OVERDRAFT = auto()
    ATM = auto()
    WIRE_TRANSFER = auto()
    FOREIGN_TRANSACTION = auto()
    PAPER_STATEMENT = auto()
    STOP_PAYMENT = auto()
    REPLACEMENT_CARD = auto()
    EARLY_WITHDRAWAL = auto()
    INSUFFICIENT_FUNDS = auto()
    DORMANT_ACCOUNT = auto()
    RESEARCH = auto()
    SPECIAL_STATEMENT = auto()
    LATE_PAYMENT = auto()
    OTHER = auto()

    # Default weights for random selection
    _DEFAULT_WEIGHTS = [
        20.0,  # SERVICE
        15.0,  # TRANSACTION
        12.0,  # OVERDRAFT
        10.0,  # ATM
        5.0,  # WIRE_TRANSFER
        5.0,  # FOREIGN_TRANSACTION
        5.0,  # PAPER_STATEMENT
        4.0,  # STOP_PAYMENT
        4.0,  # REPLACEMENT_CARD
        3.0,  # EARLY_WITHDRAWAL
        5.0,  # INSUFFICIENT_FUNDS
        3.0,  # DORMANT_ACCOUNT
        3.0,  # RESEARCH
        3.0,  # SPECIAL_STATEMENT
        5.0,  # LATE_PAYMENT
        3.0  # OTHER
    ]
