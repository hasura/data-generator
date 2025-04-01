from ....helpers import BaseEnum
from enum import auto


class BalanceType(BaseEnum):
    """Types of account balances."""
    AVAILABLE = auto()
    CURRENT = auto()
    CLOSING = auto()
    PENDING = auto()
    BLOCKED = auto()
    RESERVED = auto()
    OVERDRAFT = auto()
    HOLD = auto()
    INTEREST_BEARING = auto()
    MINIMUM_REQUIRED = auto()
    PROJECTED = auto()
    LEDGER = auto()
    OTHER = auto()

    # Default weights for random selection
    _DEFAULT_WEIGHTS = [
        30.0,  # AVAILABLE
        30.0,  # CURRENT
        15.0,  # CLOSING
        10.0,  # PENDING
        2.0,  # BLOCKED
        5.0,  # RESERVED
        3.0,  # OVERDRAFT
        5.0,  # HOLD
        8.0,  # INTEREST_BEARING
        5.0,  # MINIMUM_REQUIRED
        5.0,  # PROJECTED
        10.0,  # LEDGER
        2.0  # OTHER
    ]
