from ....helpers import BaseEnum
from enum import auto


class AmountType(BaseEnum):
    """Types of amounts on account statements."""
    OPENING_BALANCE = auto()
    CLOSING_BALANCE = auto()
    PAYMENTS = auto()
    DEPOSITS = auto()
    WITHDRAWALS = auto()
    INTEREST_EARNED = auto()
    INTEREST_CHARGED = auto()
    FEES = auto()
    CREDITS = auto()
    DEBITS = auto()
    TRANSFERS_IN = auto()
    TRANSFERS_OUT = auto()
    MINIMUM_PAYMENT_DUE = auto()
    AVAILABLE_CREDIT = auto()
    AVAILABLE_BALANCE = auto()
    CURRENT_BALANCE = auto()
    PENDING_BALANCE = auto()
    OVERDRAFT_LIMIT = auto()
    OVERDRAFT_USED = auto()
    OTHER = auto()

    # Default weights for random selection
    _DEFAULT_WEIGHTS = [
        10.0,  # OPENING_BALANCE
        10.0,  # CLOSING_BALANCE
        8.0,  # PAYMENTS
        8.0,  # DEPOSITS
        8.0,  # WITHDRAWALS
        6.0,  # INTEREST_EARNED
        6.0,  # INTEREST_CHARGED
        6.0,  # FEES
        5.0,  # CREDITS
        5.0,  # DEBITS
        5.0,  # TRANSFERS_IN
        5.0,  # TRANSFERS_OUT
        4.0,  # MINIMUM_PAYMENT_DUE
        3.0,  # AVAILABLE_CREDIT
        3.0,  # AVAILABLE_BALANCE
        3.0,  # CURRENT_BALANCE
        2.0,  # PENDING_BALANCE
        1.0,  # OVERDRAFT_LIMIT
        1.0,  # OVERDRAFT_USED
        1.0  # OTHER
    ]
