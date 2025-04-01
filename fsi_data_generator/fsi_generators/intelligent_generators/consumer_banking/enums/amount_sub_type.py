from ....helpers import BaseEnum
from enum import auto


class AmountSubType(BaseEnum):
    """Subtypes of amounts on account statements."""
    PRINCIPAL = auto()
    INTEREST = auto()
    FEES = auto()
    PENALTIES = auto()
    REWARDS = auto()
    PROMOTIONAL = auto()
    TEMPORARY = auto()
    ESTIMATED = auto()
    ADJUSTED = auto()
    CORRECTED = auto()
    NONE = auto()

    # Default weights for random selection
    _DEFAULT_WEIGHTS = [
        30.0,  # PRINCIPAL
        15.0,  # INTEREST
        15.0,  # FEES
        8.0,  # PENALTIES
        8.0,  # REWARDS
        5.0,  # PROMOTIONAL
        5.0,  # TEMPORARY
        5.0,  # ESTIMATED
        4.0,  # ADJUSTED
        3.0,  # CORRECTED
        2.0  # NONE
    ]
