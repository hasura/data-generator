from ....helpers import BaseEnum
from enum import auto


class CreditDebitIndicator(BaseEnum):
    """Indicators for whether a balance is a credit or debit."""
    CREDIT = auto()
    DEBIT = auto()

    # Default weights for random selection
    _DEFAULT_WEIGHTS = [
        80.0,  # CREDIT
        20.0  # DEBIT
    ]
